from src.homomorphic_encryption import HomomorphicEncryption
from src.zero_knowledge_proof import ZKProof
from src.utils import str_to_int, int_to_str

class ZKDatabase:
    def __init__(self):
        self.he = HomomorphicEncryption(lwe_dimension=512)
        self.zk_proof = ZKProof()
        self.tables = {}
        self.indexes = {}

    def create_table(self, table_name, columns):
        self.tables[table_name] = {'columns': columns, 'rows': []}
        self.indexes[table_name] = {}
        print(f"Table {table_name} created with columns: {columns}")

    def insert(self, table_name, values):
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
        print(f"Inserted: {values} into {table_name} (Encrypted)")

    def select(self, table_name, condition=None):
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
                if (
                    (operator == '=' and row_value == value) or
                    (operator == '>' and row_value > value) or
                    (operator == '<' and row_value < value) or
                    (operator == '>=' and row_value >= value) or
                    (operator == '<=' and row_value <= value)
                ):
                    selected_rows.append((decrypted_row, proof))
        return selected_rows

    def aggregate_sum(self, table_name, column_name):
        return self._aggregate(table_name, column_name, 'SUM')

    def _aggregate(self, table_name, column_name, agg_type):
        if table_name not in self.tables:
            print("Table not found.")
            return None, None
        column_index = self.tables[table_name]['columns'].index(column_name)
        aggregate_value = None
        for row_data in self.tables[table_name]['rows']:
            row, _proof = row_data
            row_value = row[column_index]
            if aggregate_value is None:
                aggregate_value = row_value
            else:
                if agg_type == 'SUM':
                    aggregate_value = self.he.add(aggregate_value, row_value)
        decrypted_value = self.he.decrypt(aggregate_value)
        proof, _ = self.zk_proof.generate_proof(decrypted_value)
        return decrypted_value, proof

    def verify_aggregate(self, result, proof):
        if self.zk_proof.verify(proof, None, result):
            print(f"Proof verified for aggregate result: {result}")
        else:
            print(f"Proof failed for aggregate result: {result}")

    def join(self, table1, table2, table1_column, table2_column, join_type="inner"):
        if table1 not in self.tables or table2 not in self.tables:
            print("One of the tables not found.")
            return []
        table1_data = self.tables[table1]
        table2_data = self.tables[table2]
        col1_idx = table1_data['columns'].index(table1_column)
        col2_idx = table2_data['columns'].index(table2_column]
        joined_rows = []
        indexed_table1 = self.indexes[table1].get(table1_column, {})
        indexed_table2 = self.indexes[table2].get(table2_column, {})
        if join_type == "inner":
            for key in indexed_table1.keys() & indexed_table2.keys():
                row1, proof1 = table1_data['rows'][indexed_table1[key]]
                row2, proof2 = table2_data['rows'][indexed_table2[key]]
                decrypted_row1 = [self.he.decrypt(val) for val in row1]
                decrypted_row2 = [self.he.decrypt(val) for val in row2]
                decrypted_joined_row = decrypted_row1 + decrypted_row2
