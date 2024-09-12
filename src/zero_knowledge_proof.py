import hashlib
import os

class ZKProof:
    def __init__(self):
        self.salt = os.urandom(16)

    def _hash(self, x):
        return hashlib.sha256(str(x).encode('utf-8') + self.salt).hexdigest()

    def generate_proof(self, data):
        return self._hash(data)

    def verify(self, proof, data):
        return self._hash(data) == proof
