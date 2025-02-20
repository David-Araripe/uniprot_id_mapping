import unittest

import pandas as pd

from UniProtMapper import ProtMapper

# Test data
test_ids = ["P30542", "Q16678", "Q02880"]

# Initialize the UniProtRetriever object
mapper = ProtMapper()


class TestProtMapper(unittest.TestCase):
    def setUp(self):
        self.fields_table = ProtMapper().fields_table

    def test_supported_dbs(self):
        supported_dbs = mapper._supported_dbs
        self.assertIsInstance(supported_dbs, list)
        self.assertIn("UniProtKB_AC-ID", supported_dbs)

    def test_fields_table(self):
        self.assertIsInstance(self.fields_table, pd.DataFrame)
        self.assertIn("accession", self.fields_table["returned_field"].values)

    def test_retrieve_fields_default(self):
        result_df, failed = mapper.get(test_ids)
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), len(test_ids))
        self.assertEqual(len(failed), 0)

    def test_retrieve_fields_custom(self):
        custom_fields = [
            "accession",
            "id",
            "organism_name",
            "go_id",
            "go_p",
            "go_c",
            "go_f",
            "gene_primary",
            "protein_families",
        ]
        result_columns = self.fields_table[
            self.fields_table["returned_field"].isin(custom_fields)
        ]["label"]
        result_df, failed = mapper.get(test_ids, fields=custom_fields)
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), len(test_ids))
        self.assertEqual(len(failed), 0)
        for field in result_columns:
            self.assertIn(field, result_df.columns)

    def test_retrieve_fields_invalid_field(self):
        with self.assertRaises(ValueError):
            mapper.get(test_ids, fields=["invalid_field"])

    def test_retrieve_fields_invalid_from_db(self):
        with self.assertRaises(ValueError):
            mapper.get(test_ids, from_db="InvalidDB")

    def test_retrieve_fields_invalid_to_db(self):
        with self.assertRaises(ValueError):
            mapper.get(test_ids, to_db="InvalidDB")


if __name__ == "__main__":
    unittest.main()
