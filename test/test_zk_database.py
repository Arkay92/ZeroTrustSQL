import unittest
from src.zk_database import ZKDatabase


class TestZKDatabase(unittest.TestCase):

    def setUp(self):
        """Initialize a ZKDatabase instance before each test."""
        self.db = ZKDatabase()
        self.db.create_table("users", ["user_id", "name", "age", "balance"])
        self.db.create_table("orders", ["order_id", "user_id", "amount"])

        # Insert some test data
        self.db.insert("users", [1, "Alice", 30, 100])
        self.db.insert("users", [2, "Bob", 25, 200])
        self.db.insert("users", [3, "Charlie", 35, 150])
        self.db.insert("orders", [101, 1, 50])
        self.db.insert("orders", [102, 2, 150])
        self.db.insert("orders", [103, 1, 30])

    def test_table_creation(self):
        """Test if tables are created correctly."""
        self.assertIn("users", self.db.tables)
        self.assertIn("orders", self.db.tables)
        self.assertEqual(self.db.tables["users"]["columns"], ["user_id", "name", "age", "balance"])
        self.assertEqual(self.db.tables["orders"]["columns"], ["order_id", "user_id", "amount"])

    def test_data_insertion(self):
        """Test if data is inserted correctly."""
        users = self.db.select("users")
        self.assertEqual(len(users), 3)  # Check if 3 rows are inserted

    def test_select_query(self):
        """Test if the SELECT query works with conditions."""
        result = self.db.select("users", condition=("balance", ">=", 150))
        self.assertEqual(len(result), 2)  # Should return 2 users: Bob and Charlie

    def test_aggregate_sum(self):
        """Test if the SUM aggregation works."""
        total_sum, _ = self.db.aggregate_sum("users", "balance")
        self.assertEqual(total_sum, 450)  # 100 + 200 + 150

    def test_inner_join(self):
        """Test if the JOIN operation works."""
        joined_result = self.db.join("users", "orders", "user_id", "user_id", join_type="inner")
        self.assertEqual(len(joined_result), 2)  # Should return 2 rows, where user_id matches
        self.assertEqual(joined_result[0][0][0], 1)  # First row's user_id should be 1

    def test_aggregate_proof_verification(self):
        """Test if the aggregation result is correctly verified with ZKProof."""
        total_sum, sum_proof = self.db.aggregate_sum("users", "balance")
        self.assertTrue(self.db.zk_proof.verify(sum_proof, None, total_sum))


if __name__ == '__main__':
    unittest.main()
