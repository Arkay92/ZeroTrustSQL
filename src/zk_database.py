from src.homomorphic_encryption import HomomorphicEncryption
from src.zero_knowledge_proof import ZKProof

class ZKDatabase:
    def __init__(self):
        self.he = HomomorphicEncryption(lwe_dimension=512)
        self.zk_proof = ZKProof()
        self.tables = {}

    def create_table(self, table_name, columns):
        self.tables[table_name] = {'columns': columns, 'rows': []}
        print(f"Table {table_name} created with columns: {columns}")

    def insert(self, table_name, values):
        if table_name not in self.tables:
            print("Table not found.")
            return
        encrypted_values = [self.he.encrypt(value) for value in values]
        self.tables[table_name]['rows'].append(encrypted_values)
        print(f"Inserted: {values} into {table_name} (Encrypted)")

    def select(self, table_name, condition=None):
        if table_name not in self.tables:
            print("Table not found.")
            return []
        
        selected_rows = []
        for row in self.tables[table_name]['rows']:
            decrypted_row = [self.he.decrypt(value) for value in row]
            if condition:
                column_name, operator, value = condition
                column_index = self.tables[table_name]['columns'].index(column_name)
                row_value = decrypted_row[column_index]

                if operator == "=" and row_value == value:
                    selected_rows.append(decrypted_row)
                elif operator == ">" and row_value > value:
                    selected_rows.append(decrypted_row)
                elif operator == "<" and row_value < value:
                    selected_rows.append(decrypted_row)
        
        return selected_rows

    def aggregate_sum(self, table_name, column_name):
        column_index = self.tables[table_name]['columns'].index(column_name)
        aggregate_value = None

        for row in self.tables[table_name]['rows']:
            row_value = row[column_index]
            if aggregate_value is None:
                aggregate_value = row_value
            else:
                aggregate_value = self.he.add(aggregate_value, row_value)

        return self.he.decrypt(aggregate_value)

    def verify_select(self, result, condition=None):
        proof = self.zk_proof.generate_proof(result)
        print(f"Generated Proof: {proof}")
        
        if self.zk_proof.verify(proof, result):
            print("Proof Verified")
        else:
            print("Proof Verification Failed")

    def verify_sum(self, result):
        proof = self.zk_proof.generate_proof(result)
        print(f"Generated Proof: {proof}")
        
        if self.zk_proof.verify(proof, result):
            print("Sum Proof Verified")
        else:
            print("Sum Proof Verification Failed")
