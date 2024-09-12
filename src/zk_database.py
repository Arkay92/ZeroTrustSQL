import hashlib
import os
import random
from src.homomorphic_encryption import HomomorphicEncryption
from src.zero_knowledge_proof import ZKProof
from src.utils import str_to_int, int_to_str

# User roles for Role-Based Access Control (RBAC)
USER_ROLES = {
    'admin': ['select', 'insert', 'update', 'delete'],
    'read_only': ['select'],
    'write_only': ['insert'],
    'read_write': ['select', 'insert', 'update'],
}

class ZKDatabase:
    def __init__(self, user_role='admin'):
        self.he = HomomorphicEncryption(lwe_dimension=512)
        self.zk_proof = ZKProof()
        self.tables = {}
        self.indexes = {}
        self.role = user_role
        self.transaction_log = []  # For transaction rollback
        self.cache = {}  # Caching for queries
        self.logs = []  # Logs of operations

    # ----- Caching Functionality -----
    def cache_query(self, query, result):
        """Cache the result of a query."""
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        self.cache[query_hash] = result

    def get_cached_query(self, query):
        """Retrieve cached result if available."""
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        return self.cache.get(query_hash)

    # ----- Role-Based Access Control -----
    def check_permission(self, operation):
        """ Check if the user role has the permission for the operation """
        if operation not in USER_ROLES[self.role]:
            raise PermissionError(f"Role '{self.role}' does not have permission for '{operation}' operation.")

    # ----- Transaction Management -----
    def begin_transaction(self):
        """Start a transaction by capturing a snapshot of the current state."""
        snapshot = {
            'tables': {k: v.copy() for k, v in self.tables.items()},
            'indexes': {k: v.copy() for k, v in self.indexes.items()}
        }
        self.transaction_log.append(snapshot)
        print("Transaction started.")

    def rollback(self):
        """Rollback to the last saved state (undo last transaction)."""
        if self.transaction_log:
            last_snapshot = self.transaction_log.pop()
            self.tables = last_snapshot['tables']
            self.indexes = last_snapshot['indexes']
            print("Transaction rolled back.")
        else:
            print("No transaction to rollback.")

    def commit(self):
        """Commit the transaction by clearing the transaction log."""
        self.transaction_log.clear()
        print("Transaction committed.")

    # ----- Logging and Auditing -----
    def log_operation(self, operation, table_name, data=None, condition=None):
        """Log database operations with encrypted data for auditing purposes."""
        log_entry = {
            'operation': operation,
            'table': table_name,
            'data': hashlib.sha256(str(data).encode()).hexdigest() if data else None,
            'condition': condition,
            'user_role': self.role
        }
        self.logs.append(log_entry)
        print(f"Logged operation: {operation} on {table_name}")

    def view_logs(self):
        """View logged operations."""
        for log in self.logs:
            print(log)

    # ----- Core Operations -----
    def create_table(self, table_name, columns):
        self.tables[table_name] = {'columns': columns, 'rows': []}
        self.indexes[table_name] = {}
        self.log_operation('create_table', table_name)
        print(f"Table {table_name} created with columns: {columns}")

    def insert(self, table_name, values):
        self.check_permission('insert')
        if table_name not in self.tables:
            print("Table not found.")
            return
        converted_values = [str_to_int(value) if isinstance(value, str) else value for value in values]
        encrypted_values = [self.he.encrypt(value) for value in converted_values]
        name_field = values[0]
        proof, _ = self.zk_proof.generate_proof(name_field)
        self.tables[table_name]['rows'].append((encrypted_values, proof))
        for i, val in enumerate(values):
            col_name = self.tables[table_name]['columns'][i]
            if col_name not in self.indexes[table_name]:
                self.indexes[table_name][col_name] = {}
            self.indexes[table_name][col_name][val] = len(self.tables[table_name]['rows']) - 1
        self.log_operation('insert', table_name, data=values)
        print(f"Inserted: {values} into {table_name} (Encrypted)")

    def select(self, table_name, condition=None):
        self.check_permission('select')
        cached_result = self.get_cached_query(str(condition))
        if cached_result:
            print("Returning cached result.")
            return cached_result

        if table_name not in self.tables:
            print("Table not found.")
            return []

        selected_rows = []
        
        for row, proof in self.tables[table_name]['rows']:
            decrypted_row = [self.he.decrypt(value) for value in row]
            if condition:
                column_name, operator, value = condition
                column_index = self.tables[table_name]['columns'].index(column_name)
                row_value = decrypted_row[column_index]
                if self._evaluate_condition(row_value, operator, value):
                    selected_rows.append((decrypted_row, proof))

        self.cache_query(str(condition), selected_rows)
        self.log_operation('select', table_name, condition=condition)
        return selected_rows

    def update(self, table_name, condition, update_values):
        """Update rows based on the condition"""
        self.check_permission('update')
        self.begin_transaction()

        for row, proof in self.tables[table_name]['rows']:
            decrypted_row = [self.he.decrypt(value) for value in row]
            column_name, operator, value = condition
            column_index = self.tables[table_name]['columns'].index(column_name)
            row_value = decrypted_row[column_index]
            if self._evaluate_condition(row_value, operator, value):
                for update_col, new_value in update_values.items():
                    update_index = self.tables[table_name]['columns'].index(update_col)
                    encrypted_new_value = self.he.encrypt(new_value)
                    row[update_index] = encrypted_new_value
                self.log_operation('update', table_name, data=update_values)
                print(f"Row updated: {decrypted_row}")
        self.commit()

    def delete(self, table_name, condition):
        """Delete rows based on the condition"""
        self.check_permission('delete')
        self.begin_transaction()

        column_name, operator, value = condition
        column_index = self.tables[table_name]['columns'].index(column_name)

        self.tables[table_name]['rows'] = [
            (row, proof) for row, proof in self.tables[table_name]['rows']
            if not self._evaluate_condition(self.he.decrypt(row[column_index]), operator, value)
        ]

        self.log_operation('delete', table_name, condition=condition)
        print(f"Rows matching condition {condition} deleted from {table_name}")
        self.commit()

    def aggregate_sum(self, table_name, column_name):
        self.check_permission('select')
        cached_result = self.get_cached_query(f"SUM-{table_name}-{column_name}")
        if cached_result:
            print("Returning cached result.")
            return cached_result

        result = self._aggregate(table_name, column_name, 'SUM')
        self.cache_query(f"SUM-{table_name}-{column_name}", result)
        self.log_operation('aggregate_sum', table_name)
        return result

    def join(self, table1, table2, table1_column, table2_column, join_type="inner"):
        self.check_permission('select')
        cached_result = self.get_cached_query(f"JOIN-{table1}-{table2}-{join_type}")
        if cached_result:
            print("Returning cached result.")
            return cached_result

        if table1 not in self.tables or table2 not in self.tables:
            print("One of the tables not found.")
            return []
        table1_data = self.tables[table1]
        table2_data = self.tables[table2]
        col1_idx = table1_data['columns'].index(table1_column)
        col2_idx = table2_data['columns'].index(table2_column)
        joined_rows = []
        indexed_table1 = self.indexes[table1].get(table1_column, {})
        indexed_table2 = self.indexes[table2].get(table2_column, {})

        if join_type == "inner":
            common_keys = indexed_table1.keys() & indexed_table2.keys()
        elif join_type == "left":
            common_keys = indexed_table1.keys()
        elif join_type == "right":
            common_keys = indexed_table2.keys()
        elif join_type == "outer":
            common_keys = indexed_table1.keys() | indexed_table2.keys()

        for key in common_keys:
            row1, row2 = None, None
            proof1, proof2 = None, None

            if key in indexed_table1:
                row1, proof1 = table1_data['rows'][indexed_table1[key]]
                decrypted_row1 = [self.he.decrypt(val) for val in row1]
            else:
                decrypted_row1 = [None] * len(table1_data['columns'])

            if key in indexed_table2:
                row2, proof2 = table2_data['rows'][indexed_table2[key]]
                decrypted_row2 = [self.he.decrypt(val) for val in row2]
            else:
                decrypted_row2 = [None] * len(table2_data['columns'])

            decrypted_joined_row = decrypted_row1 + decrypted_row2
            proof, _ = self.zk_proof.generate_proof(decrypted_joined_row)
            joined_rows.append((decrypted_joined_row, proof))

            if self.zk_proof.verify(proof, None, decrypted_joined_row):
                print(f"Proof verified for joined row: {decrypted_joined_row}")
            else:
                print(f"Proof failed for joined row: {decrypted_joined_row}")

        self.cache_query(f"JOIN-{table1}-{table2}-{join_type}", joined_rows)
        self.log_operation('join', f"{table1}-{table2}")
        return joined_rows

    def _evaluate_condition(self, row_value, operator, value):
        if operator == '=':
            return row_value == value
        elif operator == '>':
            return row_value > value
        elif operator == '<':
            return row_value < value
        elif operator == '>=':
            return row_value >= value
        elif operator == '<=':
            return row_value <= value
        return False