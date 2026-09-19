"""Finite-query containment must hold even with noisy responses and redundant bases."""
import sys
import unittest
from pathlib import Path
import torch
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'experiments' / 'p19'))
from comparators import context_matched_union

class UnionEmulationTests(unittest.TestCase):
    def test_same_information_predictions(self):
        gen = torch.Generator().manual_seed(18)
        p = 7
        I = torch.eye(p, dtype=torch.float64)
        A, _ = torch.linalg.qr(torch.randn(p, p, generator=gen, dtype=torch.float64))
        bases = [I, A, I]  # redundancy is deliberate
        for q in [1, 3, 12]:
            V = torch.randn(q, p, generator=gen, dtype=torch.float64)
            d = torch.randn(q, generator=gen, dtype=torch.float64)
            W = torch.randn(19, p, generator=gen, dtype=torch.float64)
            for j in range(len(bases)):
                for k in [1, 3, p]:
                    with self.subTest(q=q, j=j, k=k):
                        routed, union = context_matched_union(V, d, W, bases, j, k=k, ridge=1e-4)
                        torch.testing.assert_close(routed, union, atol=1e-12, rtol=1e-12)

    def test_empty_response_has_no_hidden_signal(self):
        I = torch.eye(3, dtype=torch.float64)
        pred, emulated = context_matched_union(I, torch.zeros(3, dtype=torch.float64),
                                               I, [I, I], 1, k=1, ridge=1e-4)
        self.assertEqual(float(pred.abs().max()), 0.0)
        torch.testing.assert_close(pred, emulated, atol=0, rtol=0)

if __name__ == '__main__':
    unittest.main()
