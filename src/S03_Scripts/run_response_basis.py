#!/usr/bin/env python3
"""Fit shared response coordinates or a matched three-objective comparison."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys
import numpy as np
import torch
from torch import nn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from S01_Package.response_basis import (ResponseBatch, fixed_responses, losses,
    require_disjoint, train_basis, select_basis)


class DiagnosticPredictor(nn.Module):
    """A fixed nonlinear two-output function, not a fitted benchmark predictor."""
    def __init__(self):
        super().__init__()
        self.register_buffer('w', torch.tensor([0.6,-0.5,0.4,0.3],dtype=torch.float64))
    def forward(self,x):
        score=torch.tanh(x@self.w)
        return torch.stack([score, -score],dim=-1)


def synthetic(seed, *, include_inputs=False):
    rng=torch.Generator().manual_seed(seed)
    f=DiagnosticPredictor().eval()
    batches=[]; calls={}; train_x=None
    for split,n in [('train',24),('select',24),('test',64)]:
        x=torch.randn(n,4,generator=rng,dtype=torch.float64)*0.4
        if split == 'train':
            train_x=x
        groups=torch.arange(n)%2
        scale=torch.where(groups[:,None,None]==0,1.,0.65)
        v=torch.randn(n,72,4,generator=rng,dtype=torch.float64)*0.15*scale
        d,count=fixed_responses(f,x,v,torch.zeros(n,dtype=torch.int64))
        batch=ResponseBatch.build(v[:,:24],d[:,:24],v[:,24:],d[:,24:],groups,
                                  [f'{split}:{i}' for i in range(n)])
        batches.append(batch)
        calls[split]={'fit_forward_examples':n*25, 'score_forward_examples':n*48,
                      'total_forward_examples':count['forward_examples'],
                      'backward_predictor_examples':0}
    if include_inputs:
        return batches, calls, train_x
    return batches, calls


def read_npz(path, *, include_inputs=False):
    with np.load(path,allow_pickle=False) as f:
        batches=[]
        for prefix in ('train','select','test'):
            keys=['fit_v','fit_d','score_v','score_d','groups','unit_ids']
            arrays=[f[f'{prefix}_{key}'].copy() for key in keys]
            batches.append(ResponseBatch.build(*arrays))
        if include_inputs:
            if 'train_x' not in f:
                raise ValueError('matched objectives require actual train_x in train_unit_ids order')
            inputs=f['train_x'].copy()
            if inputs.shape != (len(batches[0].unit_ids),batches[0].fit_v.shape[-1]):
                raise ValueError('train_x must be [train units, features]')
            if not np.isfinite(inputs).all():
                raise ValueError('train_x contains nonfinite values')
            return batches, inputs
    return batches


def fixed_candidates(p, seed, identity, count=8):
    """Finite non-learned family; selection uses development-select only."""
    t=torch.arange(p,dtype=torch.float64)
    dct=torch.cos(torch.pi/p*(t[None,:]+0.5)*t[:,None])*np.sqrt(2/p)
    dct[0]/=np.sqrt(2)
    generator=torch.Generator().manual_seed(seed+1000)
    bases=[identity, dct]
    names=['identity','dct']
    for j in range(count):
        q,_=torch.linalg.qr(torch.randn(p,p,generator=generator,dtype=torch.float64))
        bases.append(q)
        names.append(f'random_orthogonal_{j}')
    return names,bases


def paired_effect(method_loss, reference_loss, seed):
    """Paired percentile interval over rows, each declared to be one independent unit."""
    delta=np.asarray(method_loss)-np.asarray(reference_loss)
    if delta.ndim != 1 or len(delta)<2 or not np.isfinite(delta).all():
        raise ValueError('paired inference requires at least two finite independent-unit differences')
    rng=np.random.default_rng(seed+2000)
    bootstrap=np.array([delta[rng.integers(len(delta),size=len(delta))].mean()
                        for _ in range(2000)])
    return {'n_units':len(delta), 'mean_difference':float(delta.mean()),
            'confidence_interval_95':np.quantile(bootstrap,[.025,.975]).tolist(),
            'bootstrap_resamples':2000, 'direction':'negative favors response',
            'scope':'unit-population mean conditional on frozen development and predictor'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--synthetic',action='store_true')
    source.add_argument('--input',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seed',type=int,default=19)
    parser.add_argument('--k',type=int,default=1)
    parser.add_argument('--steps',type=int,default=80)
    parser.add_argument('--ridge',type=float,default=1e-4)
    parser.add_argument('--learning-rate',type=float,default=0.04)
    parser.add_argument('--matched-objectives',action='store_true',
                        help='run response, actual-input reconstruction and coefficient concentration')
    parser.add_argument('--aggregation',choices=('mean','worst_group'),default='worst_group')
    args=parser.parse_args()
    if args.output.exists():
        parser.error('output path exists; choose a new experiment directory')
    if args.steps<1 or any(not math.isfinite(x) or x<=0 for x in (args.ridge,args.learning_rate)):
        parser.error('steps, ridge and learning rate must be finite and positive')
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    inputs=None
    if args.synthetic:
        batches,calls,inputs=synthetic(args.seed,include_inputs=True)
    else:
        if args.matched_objectives:
            batches,inputs=read_npz(args.input,include_inputs=True)
        else:
            batches=read_npz(args.input)
        calls={'source':'precomputed; predictor access counts must be supplied by data owner'}
    train,select,test=batches
    require_disjoint(*batches)
    shapes={tuple(b.fit_v.shape[1:]) for b in batches}
    if len(shapes)!=1:
        parser.error('train/select/test must share the feature coordinates and fitting-query budget Q')
    p=train.fit_v.shape[-1]
    if not 1<=args.k<=p:
        parser.error('invalid k')
    if set(train.groups.tolist())!=set(select.groups.tolist()):
        parser.error('training and selection must contain the same development groups')
    if args.matched_objectives and len(test.unit_ids)<2:
        parser.error('matched comparison requires at least two independent test units')
    args.output.mkdir(parents=True)

    objectives={'learned_selected':'response'}
    if args.matched_objectives:
        objectives.update(reconstruction_selected='reconstruction',
                          coefficient_sparsity_selected='coefficient_sparsity')
    methods={}; records={}
    for name,objective in objectives.items():
        candidates,history=train_basis(train,k=args.k,ridge=args.ridge,steps=args.steps,
            learning_rate=args.learning_rate,checkpoint_every=max(1,args.steps//8),
            objective=objective,inputs=inputs,aggregation=args.aggregation)
        A,index,values=select_basis(candidates,select,k=args.k,ridge=args.ridge,
                                   aggregation=args.aggregation)
        methods[name]=A
        records[name]={'objective':objective,'candidate_index':index,
                      'selection_excess':values,'training_objectives':history}
    identity=candidates[0]
    fixed_names,fixed_bases=fixed_candidates(p,args.seed,identity)
    fixed_A,fixed_index,fixed_values=select_basis(fixed_bases,select,k=args.k,
        ridge=args.ridge,aggregation=args.aggregation)
    methods.update(identity=identity,dct=fixed_bases[1],best_fixed_single=fixed_A)

    # Freeze the strongest selected proxy before any test-response loss is read.
    primary_reference=None
    if args.matched_objectives:
        proxies=('reconstruction_selected','coefficient_sparsity_selected')
        primary_reference=min(proxies,key=lambda name:
            records[name]['selection_excess'][records[name]['candidate_index']])

    rows=[]; summary={}; unit_losses={}
    with torch.no_grad():
        for name,basis in methods.items():
            values=losses(basis,test,args.k,args.ridge)
            unit_losses[name]=values.cpu().numpy()
            per_group={str(int(g)):float(values[test.groups==g].mean()) for g in torch.unique(test.groups)}
            summary[name]={'mean_response_mse':float(values.mean()),'group_response_mse':per_group}
            for uid,g,value in zip(test.unit_ids,test.groups,values):
                rows.append({'unit_id':uid,'group':int(g),'method':name,'response_mse':float(value),
                             'k':args.k,'fit_queries':test.fit_v.shape[1],
                             'score_queries':test.score_v.shape[1]})
    with (args.output/'responses.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    response_record=records['learned_selected']
    A=methods['learned_selected']
    saved={'basis':A.cpu().numpy(),'candidate_index':response_record['candidate_index'],
           'best_fixed_basis':fixed_A.cpu().numpy(),'best_fixed_candidate_index':fixed_index}
    saved.update({name:basis.cpu().numpy() for name,basis in methods.items()})
    np.savez(args.output/'basis.npz',**saved)
    result={'evidence_kind':'synthetic_only' if args.synthetic else 'user_supplied_fixed_responses',
            'seed':args.seed,'features':p,'k':args.k,'fit_queries':test.fit_v.shape[1],
            'score_queries':test.score_v.shape[1],'ridge':args.ridge,'optimization_steps':args.steps,
            'aggregation':args.aggregation,'matched_objectives':args.matched_objectives,
            'selection_index':response_record['candidate_index'],
            'selection_excess':response_record['selection_excess'],
            'fixed_candidate_names':fixed_names,'best_fixed_candidate_index':fixed_index,
            'best_fixed_candidate_name':fixed_names[fixed_index],
            'fixed_selection_excess':fixed_values,
            'development_objectives':response_record['training_objectives'],
            'objective_records':records,'predictor_access':calls,
            'orthogonality_error':float((A@A.T-torch.eye(p,dtype=A.dtype)).abs().max()),
            'independent_test_results':summary,'primary_reference':primary_reference,
            'claim_boundary':'Matched-objective diagnostic only; structured-support and real-data validation are separate.'}
    if primary_reference is not None:
        result['primary_paired_effect']=paired_effect(unit_losses['learned_selected'],
                                                     unit_losses[primary_reference],args.seed)
    (args.output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ('development_objectives','objective_records')},indent=2))


if __name__=='__main__':main()
