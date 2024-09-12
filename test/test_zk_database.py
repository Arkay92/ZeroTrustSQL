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
        self.db.insert("orders", [103, 4, 30])  # Non-existent user for join tests

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

    def test_cache(self):
        """Test if query caching works correctly."""
        # Perform a query that will be cached
        result1 = self.db.select("users", condition=("balance", ">=", 100))
        # Repeat the query (should use cache)
        result2 = self.db.select("users", condition=("balance", ">=", 100))
        self.assertEqual(result1, result2)  # Cached result should match

    def test_transaction_and_rollback(self):
        """Test if transactions and rollback work correctly."""
        self.db.begin_transaction()
        self.db.update("users", ("user_id", "=", 1), {"balance": 300})
        result = self.db.select("users", condition=("user_id", "=", 1))
        decrypted_row, _ = result[0]
        self.assertEqual(decrypted_row[3], 300)  # Check if balance was updated to 300
        
        # Rollback the transaction
        self.db.rollback()
        result = self.db.select("users", condition=("user_id", "=", 1))
        decrypted_row, _ = result[0]
        self.assertEqual(decrypted_row[3], 100)  # Balance should be rolled back to 100

    def test_delete_and_commit(self):
        """Test if delete with transaction commit works."""
        self.db.begin_transaction()
        self.db.delete("users", condition=("balance", "<=", 150))
        self.db.commit()  # Commit the deletion
        result = self.db.select("users", condition=("balance", "<=", 150))
        self.assertEqual(len(result), 0)  # No users with balance <= 150 should remain

    def test_logging(self):
        """Test if logging records all operations."""
        self.db.select("users", condition=("balance", ">=", 150))
        self.db.update("users", ("user_id", "=", 1), {"balance": 300})
        self.db.delete("users", condition=("user_id", "=", 1))

        logs = self.db.logs
        self.assertEqual(len(logs), 3)  # Should log 3 operations
        self.assertEqual(logs[0]['operation'], 'select')
        self.assertEqual(logs[1]['operation'], 'update')
        self.assertEqual(logs[2]['operation'], 'delete')

    def test_inner_join(self):
        """Test if the INNER JOIN operation works."""
        joined_result = self.db.join("users", "orders", "user_id", "user_id", join_type="inner")
        self.assertEqual(len(joined_result), 2)  # Should return 2 rows where user_id matches
        self.assertEqual(joined_result[0][0][0], 1)  # First row's user_id should be 1


if __name__ == '__main__':
    unittest.main()
