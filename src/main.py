from src.zk_database import ZKDatabase

if __name__ == "__main__":
    # Initialize the database with admin role
    db = ZKDatabase(user_role='admin')

    # Create tables
    db.create_table("users", ["user_id", "name", "age", "balance"])
    db.create_table("orders", ["order_id", "user_id", "amount"])

    # Insert rows into the tables (encrypted)
    db.insert("users", [1, "Alice", 30, 100])
    db.insert("users", [2, "Bob", 25, 200])
    db.insert("users", [3, "Charlie", 35, 150])
    db.insert("orders", [101, 1, 50])
    db.insert("orders", [102, 2, 150])
    db.insert("orders", [103, 4, 30])  # Order for a non-existent user

    # Perform SELECT query and cache the result
    print("\nPerforming SELECT Query (balance >= 100):")
    result1 = db.select("users", condition=("balance", ">=", 100))
    for decrypted_row, proof in result1:
        print(f"Decrypted Row: {decrypted_row}, Proof: {proof}")

    # Cache retrieval test
    print("\nPerforming SELECT Query again (should use cache):")
    result2 = db.select("users", condition=("balance", ">=", 100))

    # Demonstrate transaction support
    print("\nStarting a transaction to update balance:")
    db.begin_transaction()
    db.update("users", ("user_id", "=", 1), {"balance": 300})
    
    print("\nRolling back transaction (should undo the balance update):")
    db.rollback()

    # Re-select after rollback
    print("\nRe-performing SELECT Query after rollback (balance should remain 100):")
    result3 = db.select("users", condition=("balance", "=", 100))
    for decrypted_row, proof in result3:
        print(f"Decrypted Row: {decrypted_row}, Proof: {proof}")

    # Delete example with commit
    print("\nStarting transaction to delete users with balance <= 150:")
    db.begin_transaction()
    db.delete("users", condition=("balance", "<=", 150))
    db.commit()  # Commit the deletion

    print("\nPerforming SELECT Query after delete (should not find users with balance <= 150):")
    result4 = db.select("users", condition=("balance", "<=", 150))
    print(f"Query Result (after delete): {result4}")

    # Perform INNER JOIN
    print("\nPerforming INNER JOIN (users.user_id = orders.user_id):")
    join_result = db.join("users", "orders", "user_id", "user_id", join_type="inner")
    for decrypted_joined_row, proof in join_result:
        print(f"Decrypted Joined Row: {decrypted_joined_row}, Proof: {proof}")

    # View Logs
    print("\nViewing logs of database operations:")
    db.view_logs()
