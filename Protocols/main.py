from bb84 import BB84Scheme
from core import QKDResults

if __name__ == "__main__":
    scheme = BB84Scheme()
    results = scheme.run(1000000)
    print("RKE:", results.raw_key_efficiency())
