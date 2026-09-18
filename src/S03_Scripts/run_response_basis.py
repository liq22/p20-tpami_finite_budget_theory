#!/usr/bin/env python3
"""Train a shared response basis; run synthetic diagnostics or an explicit NPZ study."""
import argparse
import csv
import json
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


def synthetic(seed):
    rng=torch.Generator().manual_seed(seed)
    f=DiagnosticPredictor().eval()
    batches=[]; calls={}
    for split,n in [('train',24),('select',24),('test',64)]:
        x=torch.randn(n,4,generator=rng,dtype=torch.float64)*0.4
        groups=torch.arange(n)%2
        # Same raw-space intervention law across representations. The second
        # group changes covariance, not the predictor, target, or score budget.
        scale=torch.where(groups[:,None,None]==0,1.,0.65)
        v=torch.randn(n,72,4,generator=rng,dtype=torch.float64)*0.15*scale
        d,count=fixed_responses(f,x,v,torch.zeros(n,dtype=torch.int64))
        batch=ResponseBatch.build(v[:,:24],d[:,:24],v[:,24:],d[:,24:],groups,
                                  [f'{split}:{i}' for i in range(n)])
        batches.append(batch)
        calls[split]={'fit_forward_examples':n*25, 'score_forward_examples':n*48,
                      'total_forward_examples':count['forward_examples'],
                      'backward_predictor_examples':0}
    return batches, calls


def read_npz(path):
    with np.load(path,allow_pickle=False) as f:
        batches=[]
        for prefix in ('train','select','test'):
            keys=['fit_v','fit_d','score_v','score_d','groups','unit_ids']
            arrays=[f[f'{prefix}_{key}'].copy() for key in keys]
            batches.append(ResponseBatch.build(*arrays))
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
    args=parser.parse_args()
    if args.output.exists():
        parser.error('output path exists; choose a new experiment directory')
    if args.steps<1 or args.ridge<=0 or args.learning_rate<=0:
        parser.error('steps, ridge and learning rate must be positive')
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    if args.synthetic:
        (train,select,test),calls=synthetic(args.seed)
    else:
        train,select,test=read_npz(args.input)
        calls={'source':'precomputed; predictor access counts must be supplied by data owner'}
    require_disjoint(train,select,test)
    dims={b.fit_v.shape[-1] for b in (train,select,test)}
    if len(dims)!=1 or not 1<=args.k<=next(iter(dims)):
        parser.error('inconsistent feature dimension or invalid k')
    p=next(iter(dims))
    if set(train.groups.tolist())!=set(select.groups.tolist()):
        parser.error('training and selection must contain the same development groups')
    args.output.mkdir(parents=True)
    # Failures leave a visible directory without a completed summary.
    candidates,history=train_basis(train,k=args.k,ridge=args.ridge,steps=args.steps,
        learning_rate=args.learning_rate,checkpoint_every=max(1,args.steps//8))
    A,index,selection_values=select_basis(candidates,select,k=args.k,ridge=args.ridge)

    fixed_names,fixed_bases=fixed_candidates(p,args.seed,candidates[0])
    fixed_A,fixed_index,fixed_selection_values=select_basis(
        fixed_bases,select,k=args.k,ridge=args.ridge)
    methods={
        'identity':candidates[0],
        'dct':fixed_bases[1],
        'best_fixed_single':fixed_A,
        'learned_selected':A,
    }
    rows=[]; summary={}
    with torch.no_grad():
        for name,basis in methods.items():
            values=losses(basis,test,args.k,args.ridge)
            per_group={str(int(g)):float(values[test.groups==g].mean()) for g in torch.unique(test.groups)}
            summary[name]={'mean_response_mse':float(values.mean()),'group_response_mse':per_group}
            for uid,g,value in zip(test.unit_ids,test.groups,values):
                rows.append({'unit_id':uid,'group':int(g),'method':name,'response_mse':float(value),
                             'k':args.k,'fit_queries':test.fit_v.shape[1],
                             'score_queries':test.score_v.shape[1]})
    with (args.output/'responses.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    np.savez(args.output/'basis.npz',basis=A.cpu().numpy(),candidate_index=index,
             best_fixed_basis=fixed_A.cpu().numpy(),best_fixed_candidate_index=fixed_index)
    result={'evidence_kind':'synthetic_only' if args.synthetic else 'user_supplied_fixed_responses',
            'seed':args.seed,'features':p,'k':args.k,'fit_queries':test.fit_v.shape[1],
            'score_queries':test.score_v.shape[1],'ridge':args.ridge,'optimization_steps':args.steps,
            'selection_index':index,'selection_worst_excess':selection_values,
            'fixed_candidate_names':fixed_names,
            'best_fixed_candidate_index':fixed_index,
            'best_fixed_candidate_name':fixed_names[fixed_index],
            'fixed_selection_worst_excess':fixed_selection_values,
            'development_objectives':history,'predictor_access':calls,
            'orthogonality_error':float((A@A.T-torch.eye(p,dtype=A.dtype)).abs().max()),
            'independent_test_results':summary,
            'claim_boundary':'No benchmark, physical-validity, global-optimality or distribution-free improvement claim.'}
    (args.output/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='development_objectives'},indent=2))


if __name__=='__main__':main()
