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
    db.insert("orders", [103, 4, 30])  # Order for a non-existent user (for testing joins)

    # Perform INNER JOIN
    print("\nInner Join Results (users.user_id = orders.user_id):")
    inner_join_results = db.join("users", "orders", "user_id", "user_id", join_type="inner")
    for decrypted_joined_row, proof in inner_join_results:
        print(f"Decrypted Joined Row: {decrypted_joined_row}")
        print(f"Proof for Joined Row: {proof}")

    # Perform LEFT JOIN
    print("\nLeft Join Results (users.user_id = orders.user_id):")
    left_join_results = db.join("users", "orders", "user_id", "user_id", join_type="left")
    for decrypted_joined_row, proof in left_join_results:
        print(f"Decrypted Joined Row: {decrypted_joined_row}")
        print(f"Proof for Joined Row: {proof}")

    # Perform RIGHT JOIN
    print("\nRight Join Results (users.user_id = orders.user_id):")
    right_join_results = db.join("users", "orders", "user_id", "user_id", join_type="right")
    for decrypted_joined_row, proof in right_join_results:
        print(f"Decrypted Joined Row: {decrypted_joined_row}")
        print(f"Proof for Joined Row: {proof}")

    # Perform FULL OUTER JOIN
    print("\nFull Outer Join Results (users.user_id = orders.user_id):")
    outer_join_results = db.join("users", "orders", "user_id", "user_id", join_type="outer")
    for decrypted_joined_row, proof in outer_join_results:
        print(f"Decrypted Joined Row: {decrypted_joined_row}")
        print(f"Proof for Joined Row: {proof}")
