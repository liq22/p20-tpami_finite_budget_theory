"""Model invariants and training checks on independent synthetic units."""
import sys
import unittest
from pathlib import Path
import numpy as np
import torch
from torch import nn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from S01_Package.response_basis import (SharedOrthogonalBasis, ResponseBatch,
    require_disjoint, sparse_decoder, losses, train_basis, select_basis, fixed_responses)

torch.set_num_threads(1)


def batch(seed, n=12, p=4):
    g = torch.Generator().manual_seed(seed)
    vf = torch.randn(n, 24, p, generator=g, dtype=torch.float64)
    vs = torch.randn(n, 36, p, generator=g, dtype=torch.float64)
    w = torch.tensor([0.6, -0.5, 0.4, 0.3], dtype=torch.float64)
    df, ds = vf @ w, vs @ w
    return ResponseBatch.build(vf,df,vs,ds,torch.arange(n)%2,
                               [f'{seed}:{i}' for i in range(n)])


class ModelTests(unittest.TestCase):
    def test_orthogonality_and_inverse(self):
        m = SharedOrthogonalBasis(5)
        with torch.no_grad(): m.angles.copy_(torch.linspace(-1,1,10))
        x = torch.arange(15,dtype=torch.float64).reshape(3,5)
        self.assertTrue(torch.allclose(m.matrix()@m.matrix().T, torch.eye(5,dtype=x.dtype),atol=1e-12))
        self.assertTrue(torch.allclose(m.inverse(m(x)),x,atol=1e-11))

    def test_sparse_budget_and_differentiable_fit(self):
        b=batch(1); m=SharedOrthogonalBasis(4)
        a,S=sparse_decoder(b.fit_v[0],b.fit_d[0],m.matrix(),2,1e-3)
        self.assertEqual(len(S),2); self.assertLessEqual(int(a.ne(0).sum()),2)
        loss=losses(m.matrix(),b,2,1e-3).mean(); loss.backward()
        self.assertTrue(torch.isfinite(m.angles.grad).all())
        self.assertGreater(float(m.angles.grad.norm()),0.)

    def test_piecewise_gradient_matches_finite_difference(self):
        b=batch(92); m=SharedOrthogonalBasis(4)
        objective=losses(m.matrix(),b,1,1e-3).mean()
        objective.backward(); analytic=float(m.angles.grad[0])
        values=[]
        for eps in (1e-6,-1e-6):
            with torch.no_grad(): m.angles[0]=eps
            values.append(float(losses(m.matrix(),b,1,1e-3).mean().detach()))
        self.assertAlmostEqual(analytic,(values[0]-values[1])/2e-6,places=7)

    def test_fixed_targets_predictor_unchanged(self):
        torch.manual_seed(5)
        f=nn.Sequential(nn.Linear(4,7),nn.Tanh(),nn.Linear(7,3)).double().eval()
        state={k:v.clone() for k,v in f.state_dict().items()}
        x=torch.randn(3,4,dtype=torch.float64)
        v=torch.randn(3,6,4,dtype=torch.float64)*0.2
        t=torch.tensor([2,1,0])
        d,count=fixed_responses(f,x,v,t)
        expected=torch.stack([f(x[i:i+1])[0,t[i]]-f(x[i]-v[i])[:,t[i]] for i in range(3)])
        self.assertTrue(torch.allclose(d,expected,atol=1e-12))
        self.assertEqual(count,{'forward_examples':21,'backward_examples':0})
        for k,v0 in state.items(): self.assertTrue(torch.equal(v0,f.state_dict()[k]))
        self.assertTrue(all(p.grad is None for p in f.parameters()))
        m=SharedOrthogonalBasis(4)
        with torch.no_grad(): m.angles.fill_(0.3)
        self.assertTrue(torch.allclose(f(m.inverse(m(x))),f(x),atol=1e-12))

    def test_independent_units_must_be_disjoint(self):
        b=batch(10)
        require_disjoint(b,batch(11))
        with self.assertRaises(ValueError): require_disjoint(b,b)

    def test_independent_discrete_draws_may_coincide(self):
        fit=torch.randint(0,2,(1,32,2),generator=torch.Generator().manual_seed(1)).double()
        score=torch.randint(0,2,(1,32,2),generator=torch.Generator().manual_seed(2)).double()
        overlap=(fit[0,:,None,:]==score[0,None,:,:]).all(-1)
        self.assertTrue((overlap & fit[0].ne(0).any(-1)[:,None]).any())
        b=ResponseBatch.build(fit,fit.sum(-1),score,score.sum(-1),[0],['u'])
        self.assertTrue(torch.equal(b.score_v,score))

    def test_discarding_collisions_changes_binary_scoring_law(self):
        # Uniform binary scoring with fit v=1; predictor response d(v)=v and
        # zero decoder. Filtering scoring v=1 changes risk from 1/2 to zero.
        fit=torch.tensor([[[1.,0.]]],dtype=torch.float64)
        score=torch.tensor([[[0.,0.],[1.,0.]]],dtype=torch.float64)
        b=ResponseBatch.build(fit,fit.sum(-1),score,score.sum(-1),[0],['u'])
        self.assertEqual(float(b.score_d.square().mean()),.5)
        filtered=score[0][score[0,:,0]!=fit[0,0,0]]
        self.assertEqual(float(filtered.sum(-1).square().mean()),0.)

    def test_invalid_parameters_and_scaling_fail(self):
        b=batch(3)
        with self.assertRaises(ValueError): losses(2*torch.eye(4,dtype=torch.float64),b,1,0.01)
        with self.assertRaises(ValueError): sparse_decoder(b.fit_v[0],b.fit_d[0],torch.eye(4),0,0.01)
        with self.assertRaises(ValueError): SharedOrthogonalBasis(257)
        with self.assertRaises(ValueError): sparse_decoder(b.fit_v[0],b.fit_d[0],torch.eye(4),1,0.)

    def test_training_and_independent_selection_constructive_case(self):
        train, selection, test = batch(21), batch(22), batch(23, n=24)
        require_disjoint(train,selection,test)
        candidates,_=train_basis(train,k=1,ridge=1e-4,steps=55,learning_rate=0.04,checkpoint_every=10)
        A,index,values=select_basis(candidates,selection,k=1,ridge=1e-4)
        with torch.no_grad():
            initial=float(losses(candidates[0],test,1,1e-4).mean())
            learned=float(losses(A,test,1,1e-4).mean())
        self.assertEqual(values[0],0.)
        self.assertGreater(index,0)
        self.assertLess(learned, initial*0.15)

    def test_identity_only_selection_and_rank_deficient_queries(self):
        b=batch(8); I=torch.eye(4,dtype=torch.float64)
        A,index,values=select_basis([I],b,k=1,ridge=1e-3)
        self.assertEqual(index,0); self.assertEqual(values,[0.])
        V=torch.ones(4,4,dtype=torch.float64); d=torch.ones(4,dtype=torch.float64)
        a,S=sparse_decoder(V,d,A,2,1e-3)
        self.assertTrue(torch.isfinite(a).all())

    def test_model_state_roundtrip(self):
        a=SharedOrthogonalBasis(4); b=SharedOrthogonalBasis(4)
        with torch.no_grad(): a.angles.fill_(0.2)
        b.load_state_dict(a.state_dict(), strict=True)
        self.assertTrue(torch.equal(a.matrix(),b.matrix()))

    def test_predictor_training_and_missing_target_rejected(self):
        f=nn.Linear(4,2).double()
        x=torch.zeros(2,4,dtype=torch.float64); v=torch.ones(2,3,4,dtype=torch.float64)
        with self.assertRaises(ValueError): fixed_responses(f,x,v,[0,1])
        f.eval()
        with self.assertRaises(ValueError): fixed_responses(f,x,v,[0,3])
        with self.assertRaises(ValueError): fixed_responses(f,x,v,[0.,1.])

if __name__=='__main__': unittest.main()
