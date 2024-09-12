import random

secret_key = [random.randint(0, (1 << 32) - 1) for _ in range(512)]

class HomomorphicEncryption:
    def __init__(self, lwe_dimension):
        self.lwe_dimension = lwe_dimension

    def encrypt(self, plaintext):
        delta = (1 << (32 - 1))  # Scaling factor
        encoded_plaintext = delta * plaintext
        noise = random.randint(0, delta >> 1)
        mask = [random.randint(0, (1 << 32) - 1) for _ in range(self.lwe_dimension)]
        body = sum([mask[i] * secret_key[i] for i in range(self.lwe_dimension)]) + encoded_plaintext + noise
        return (mask, body)

    def add(self, ct1, ct2):
        mask_sum = [(ct1[0][i] + ct2[0][i]) for i in range(self.lwe_dimension)]
        body_sum = ct1[1] + ct2[1]
        return (mask_sum, body_sum)

    def decrypt(self, ciphertext):
        delta = (1 << (32 - 1))
        mask, body = ciphertext
        recovered_plaintext = body - sum([mask[i] * secret_key[i] for i in range(self.lwe_dimension)])
        return round(recovered_plaintext / delta)
