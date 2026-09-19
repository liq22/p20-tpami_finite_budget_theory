"""Exercise Algorithm 1 through the real command entry on controlled response tables."""
import contextlib
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'S03_Scripts'))
from run_response_basis import main, paired_effect
from test_response_objectives import study


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root=Path(self.directory.name)
        self.arrays={}
        for prefix,seed in zip(('train','select','test'),(101,102,103)):
            b,x=study(seed,n=4)
            for field in ('fit_v','fit_d','score_v','score_d','groups'):
                self.arrays[f'{prefix}_{field}']=getattr(b,field).numpy()
            self.arrays[f'{prefix}_unit_ids']=np.asarray(b.unit_ids)
            if prefix=='train':
                self.arrays['train_x']=x.numpy()

    def run_entry(self,name,arrays=None,matched=True,extra=()):
        data=self.root/f'{name}.npz'
        np.savez(data,**(self.arrays if arrays is None else arrays))
        out=self.root/name
        args=['run_response_basis','--input',str(data),'--output',str(out),
              '--steps','6','--aggregation','mean',*extra]
        if matched:
            args.append('--matched-objectives')
        with patch.object(sys,'argv',args),contextlib.redirect_stdout(io.StringIO()):
            main()
        return out,json.loads((out/'summary.json').read_text())

    def test_all_objectives_execute_with_common_selection_and_paired_rows(self):
        out,result=self.run_entry('complete')
        expected={'learned_selected','reconstruction_selected','coefficient_sparsity_selected',
                  'identity','dct','best_fixed_single'}
        self.assertEqual(set(result['independent_test_results']),expected)
        records=result['objective_records']
        self.assertEqual({len(r['selection_excess']) for r in records.values()},{7})
        self.assertEqual({len(r['training_objectives']) for r in records.values()},{6})
        proxies=('reconstruction_selected','coefficient_sparsity_selected')
        chosen=min(proxies,key=lambda m:records[m]['selection_excess'][records[m]['candidate_index']])
        self.assertEqual(result['primary_reference'],chosen)
        with (out/'responses.csv').open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),24)
        self.assertEqual({r['fit_queries'] for r in rows},{'6'})
        by_method={m:{r['unit_id']:float(r['response_mse']) for r in rows if r['method']==m}
                   for m in expected}
        units=by_method['learned_selected']
        delta=np.mean([units[u]-by_method[chosen][u] for u in units])
        self.assertAlmostEqual(delta,result['primary_paired_effect']['mean_difference'],places=14)
        self.assertEqual(result['primary_paired_effect']['n_units'],4)
        self.assertEqual(result['evidence_kind'],'user_supplied_fixed_responses')

    def test_test_responses_do_not_change_basis_or_reference(self):
        first,a=self.run_entry('original')
        changed=dict(self.arrays)
        changed['test_score_d']=changed['test_score_d']+9
        second,b=self.run_entry('changed',changed)
        self.assertEqual(a['primary_reference'],b['primary_reference'])
        self.assertEqual(a['objective_records'],b['objective_records'])
        with np.load(first/'basis.npz') as left,np.load(second/'basis.npz') as right:
            self.assertEqual(set(left.files),set(right.files))
            for key in left.files:
                np.testing.assert_array_equal(left[key],right[key])
        self.assertNotEqual(a['independent_test_results'],b['independent_test_results'])

    def test_missing_actual_inputs_fails_before_output(self):
        arrays={k:v for k,v in self.arrays.items() if k!='train_x'}
        with self.assertRaisesRegex(ValueError,'actual train_x'):
            self.run_entry('no_inputs',arrays)
        self.assertFalse((self.root/'no_inputs').exists())

    def test_different_construction_budget_fails_before_output(self):
        arrays=dict(self.arrays)
        arrays['test_fit_v']=arrays['test_fit_v'][:,:3]
        arrays['test_fit_d']=arrays['test_fit_d'][:,:3]
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
            self.run_entry('wrong_budget',arrays)
        self.assertFalse((self.root/'wrong_budget').exists())

    def test_legacy_response_mode_needs_no_input_vectors(self):
        arrays={k:v for k,v in self.arrays.items() if k!='train_x'}
        _,result=self.run_entry('legacy',arrays,matched=False)
        self.assertEqual(len(result['independent_test_results']),4)
        self.assertIsNone(result['primary_reference'])
        self.assertNotIn('primary_paired_effect',result)

    def test_unit_overlap_fails_before_output(self):
        arrays=dict(self.arrays)
        arrays['test_unit_ids']=arrays['train_unit_ids']
        with self.assertRaisesRegex(ValueError,'units overlap'):
            self.run_entry('overlap',arrays)
        self.assertFalse((self.root/'overlap').exists())

    def test_paired_interval_uses_negative_improvement_sign(self):
        result=paired_effect([1,2,3],[3,4,5],seed=3)
        self.assertEqual(result['mean_difference'],-2.)
        self.assertEqual(result['confidence_interval_95'],[-2.,-2.])
        self.assertEqual(result['n_units'],3)

    def test_nonfinite_hyperparameter_fails_before_output(self):
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
            self.run_entry('nan',extra=('--ridge','nan'))
        self.assertFalse((self.root/'nan').exists())


if __name__=='__main__':
    unittest.main()
