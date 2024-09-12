# ZeroTrustSQL: Secure SQL Operations with Homomorphic Encryption and Zero-Knowledge Proofs

## Overview

**ZeroTrustSQL** is a privacy-preserving database solution that enables SQL-like operations on encrypted data using **Homomorphic Encryption (HE)** and **Zero-Knowledge Proofs (ZKProofs)**. This project demonstrates how to create, store, query, and verify data securely, without ever exposing plaintext values, ensuring data privacy even during computations.

### Key Features:
- **Homomorphic Encryption**: Perform computations on encrypted data, including addition, without revealing sensitive information.
- **Zero-Knowledge Proofs**: Verify the correctness of query results (like `SELECT`, `SUM`, and `JOIN`) without exposing underlying data.
- **SQL-like Operations**: Supports SQL operations such as `SELECT`, `SUM`, and `JOIN`, operating entirely on encrypted values.
- **Proof Verification**: Easily verify results to ensure data integrity with cryptographic proofs.

## Project Structure

```plaintext
ZeroTrustSQL/
│
├── src/
│   ├── __init__.py                 # Initializes the src package
│   ├── homomorphic_encryption.py   # Contains homomorphic encryption logic
│   ├── zero_knowledge_proof.py     # Manages ZKProof generation and verification logic
│   ├── zk_database.py              # SQL-like encrypted database operations
│   ├── utils.py                    # Helper functions like string-to-integer conversions
│   └── main.py                     # Demonstrates usage of the database system
│
├── tests/
│   ├── __init__.py                 # Initializes the tests package
│   └── test_zk_database.py         # Unit tests for database functionality
│
├── setup.py                        # Packaging configuration
├── requirements.txt                # Python package dependencies
└── README.md                       # Project documentation
```

## Getting Started
### Prerequisites
#### Python 3.6+
Install the required libraries by running the following command:
```
pip install -r requirements.txt
```
### Running the Example
The main.py file contains an example usage of the database system, demonstrating how to create tables, insert data, run queries, and verify results. To run the example:
```
python src/main.py
```

Example Operations:
- Create Tables: Create tables for users and orders, defining the columns.
- Insert Encrypted Data: Insert data that will be encrypted.
- Select Query: Query the encrypted data with conditions (e.g., select users with a balance greater than or equal to 100).
- Aggregate SUM: Compute the sum of an encrypted column (e.g., user balances).
- JOIN Tables: Perform JOINs between users and orders based on user IDs.
- Proof Verification: Verify the results using Zero-Knowledge Proofs.

## Testing
To run the unit tests and ensure everything works correctly:
```
python -m unittest discover -s tests
```

Tests include:

- Table creation and data insertion
- Querying with SELECT and JOIN
- SUM aggregation
- Zero-Knowledge proof verification

## Dependencies
- lightphe: For homomorphic encryption operations.
- pycryptodome: For cryptographic operations (e.g., hashing, random number generation).
- unittest: Python's built-in testing framework (used in test_zk_database.py).

## Installation
Clone this repository:
```
git clone https://github.com/Arkay92/ZeroTrustSQL.git
cd ZeroTrustSQL
```

### Install the dependencies:
```
pip install -r requirements.txt
```

### Run the main example:
```
python src/main.py
```

## How It Works
Homomorphic Encryption allows computations on encrypted data without revealing the plaintext. In this project, it’s used for securely calculating sums (aggregate_sum), adding encrypted values, and querying.
Zero-Knowledge Proofs verify the correctness of operations like SUM or JOIN without revealing sensitive data. The ZKProof class is responsible for generating cryptographic proofs and validating results.

Example Code Usage:
```
from src.zk_database import ZKDatabase
```

### Initialize the database
```
db = ZKDatabase()
```

### Create tables
```
db.create_table("users", ["user_id", "name", "age", "balance"])
db.create_table("orders", ["order_id", "user_id", "amount"])
```

### Insert encrypted data
```
db.insert("users", [1, "Alice", 30, 100])
db.insert("orders", [101, 1, 50])
```

### Query and verify results
```
results = db.select("users", condition=("balance", ">=", 100))
db.verify_select(results, condition=("balance", ">=", 100))
```

### Calculate SUM and verify
```
total_sum, sum_proof = db.aggregate_sum("users", "balance")
db.verify_aggregate(total_sum, sum_proof)
```

## Contributing
Feel free to open an issue or submit a pull request if you would like to contribute to this project. Feedback and suggestions are always welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any questions or feedback, please contact total.trance.network@gmail.com.
