import hashlib
import os

class ZKProof:
    def __init__(self):
        self.salt = os.urandom(16)

    def _hash(self, x):
        return hashlib.sha256(str(x).encode('utf-8') + self.salt).hexdigest()

    def generate_proof(self, data, condition=None):
        self.v = self._hash(data)
        condition_proof = self._hash(condition) if condition else None
        return self.v, condition_proof

    def verify(self, proof, condition_proof, data, condition=None):
        return self._hash(data) == proof and (not condition or self._hash(condition) == condition_proof)
