import unittest
from src.lca import ROOT, read_bom, inventory_summary, material_lcia

class ModelTests(unittest.TestCase):
    def test_assignment_mass(self):
        result = inventory_summary(read_bom(ROOT/'data/bom.csv'))
        self.assertEqual(result['materials'], 12)
        self.assertAlmostEqual(result['kettle_g'], 723)
        self.assertAlmostEqual(result['packaging_g'], 137.8)
        self.assertAlmostEqual(result['total_g'], 860.8)

    def test_no_data_does_not_produce_result(self):
        with self.assertRaises(ValueError):
            material_lcia(read_bom(ROOT/'data/bom.csv'), [])

    def example(self):
        # Synthetic arithmetic fixture; never used as an environmental result.
        rows = [{'material':'test', 'scope':'Kettle', 'finished_mass_g':'500'}]
        factors = [dict(material='test',category='test category',impact_unit='test unit',
                        factor_per_kg='4',method='synthetic',method_version='1',
                        dataset_id='synthetic',source='test fixture',
                        boundary='cradle-to-material-gate')]
        return rows, factors

    def test_grams_to_kg(self):
        rows, factors = self.example()
        self.assertEqual(material_lcia(rows, factors)[0]['impact'], 2)

    def test_missing_category(self):
        rows, factors = self.example()
        rows.append(dict(material='missing',scope='Kettle',finished_mass_g='1'))
        with self.assertRaises(ValueError): material_lcia(rows, factors)

    def test_mixed_method(self):
        rows, factors = self.example()
        factors.append(dict(factors[0], category='second', method='different'))
        with self.assertRaises(ValueError): material_lcia(rows, factors)

    def test_duplicate_and_nonfinite(self):
        rows, factors = self.example()
        with self.assertRaises(ValueError): material_lcia(rows, factors+factors)
        factors[0]['factor_per_kg'] = 'nan'
        with self.assertRaises(ValueError): material_lcia(rows, factors)

    def test_incompatible_boundary(self):
        rows, factors = self.example()
        factors[0]['boundary'] = 'cradle-to-grave'
        with self.assertRaises(ValueError): material_lcia(rows, factors)

if __name__ == '__main__': unittest.main()
