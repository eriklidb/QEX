from bb84 import BB84Scheme
from e91 import E91Scheme
from b92 import B92Scheme
from core import QKDResults

if __name__ == "__main__":
    bb84 = BB84Scheme()
    e91 = E91Scheme()
    b92 = B92Scheme()
    bb84_res = bb84.run(1000000)
    e91_res = e91.run(1000000)
    b92_res = b92.run(1000000)
    print("\n")
    print("BB84 RKE:\t", bb84_res.raw_key_efficiency(), "\n")
    print("E91 RKE:\t", e91_res.raw_key_efficiency(), "\n")
    print("B92 RKE:\t", b92_res.raw_key_efficiency(), "\n")
