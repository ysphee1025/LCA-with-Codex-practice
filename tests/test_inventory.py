import csv
import math
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from inventory import load_bom,write_si
ROOT=Path(__file__).resolve().parents[1]

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.rows,self.totals=load_bom(ROOT/'data/input/classroom_bom_supplied.csv')
    def test_authoritative_masses(self):
        self.assertEqual(len(self.rows),12)
        self.assertAlmostEqual(self.totals['Kettle'],723)
        self.assertAlmostEqual(self.totals['Packaging'],137.8)
        self.assertAlmostEqual(self.totals['Total'],860.8)
    def test_si_conversion(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'si.csv';write_si(self.rows,path)
            with path.open() as f: si=list(csv.DictReader(f))
            self.assertAlmostEqual(sum(float(r['quantity']) for r in si),.8608)
            self.assertEqual({r['unit'] for r in si},{'kg'})
            for original,converted in zip(self.rows,si):
                self.assertAlmostEqual(float(original['finished_mass_g'])/1000,float(converted['quantity']))
    def invalid(self,change):
        rows=[dict(r) for r in self.rows];change(rows)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bom.csv'
            with p.open('w') as f:
                w=csv.DictWriter(f,fieldnames=['material','finished_mass_g','scope']);w.writeheader();w.writerows(rows)
            with self.assertRaises(ValueError):load_bom(p)
    def test_mass_mismatch(self):self.invalid(lambda r:r[0].update(finished_mass_g='185'))
    def test_duplicate(self):self.invalid(lambda r:r[1].update(material=r[0]['material']))
    def test_nonfinite(self):self.invalid(lambda r:r[0].update(finished_mass_g='nan'))
    def test_negative(self):self.invalid(lambda r:r[0].update(finished_mass_g='-1'))
    def test_missing_item(self):self.invalid(lambda r:r.pop())
    def test_unknown_scope(self):self.invalid(lambda r:r[0].update(scope='Use'))

if __name__=='__main__':unittest.main()
