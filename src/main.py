from src.zk_database import ZKDatabase

if __name__ == "__main__":
    db = ZKDatabase()
    db.create_table("users", ["user_id", "name", "age", "balance"])
    db.create_table("orders", ["order_id", "user_id", "amount"])

    # Insert rows into the tables (encrypted)
    db.insert("users", [1, "Alice", 30, 100])
    db.insert("users", [2, "Bob", 25, 200])
    db.insert("users", [3, "Charlie", 35, 150])
    db.insert("orders", [101, 1, 50])
    db.insert("orders", [102, 2, 150])
    db.insert("orders", [103, 1, 30])

    # Perform a SELECT query with a condition
    print("\nQuery Results (balance >= 100):")
    results = db.select("users", condition=("balance", ">=", 100))
    db.verify_select(results, condition=("balance", ">=", 100))

    # Perform a SUM aggregation on the 'balance' column
    print("\nSUM of balance:")
    total_sum, sum_proof = db.aggregate_sum("users", "balance")
    print(f"SUM: {total_sum}")
    db.verify_aggregate(total_sum, sum_proof)

    # Perform an INNER JOIN between users and orders on user_id and verify proof
    print("\nInner Join Results (users.name = orders.user_id):")
    join_results = db.join("users", "orders", "user_id", "user_id", join_type="inner")
    for decrypted_joined_row, proof in join_results:
        print(f"Decrypted Joined Row: {decrypted_joined_row}")
        print(f"Proof for Joined Row: {proof}")
