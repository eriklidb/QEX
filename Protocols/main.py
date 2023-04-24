from bb84 import BB84Scheme
from e91 import E91Scheme
from b92 import B92Scheme
import matplotlib.pyplot as plt 
import numpy as np

if __name__ == "__main__":
    num_shots = 256 # Number of bits of an AES-key (type of symmetric key alg) (belived to be quantum resistant).
    num_sessions = 1000
    schemes = [BB84Scheme(False), E91Scheme(False), B92Scheme(False)]
    rke_vecs = np.array([[scheme.run(num_shots).rke() for _ in range(num_sessions)] for scheme in schemes])
    rke_means = rke_vecs.mean(axis=1)
    rke_stds = rke_vecs.std(axis=1)

    schemes_title = [str(scheme) for scheme in schemes]
    schemes_color = ['tab:red', 'tab:green', 'tab:blue']

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.bar(schemes_title, rke_means, label=schemes_title, color=schemes_color)
    ax1.set_ylabel('Mean')
    ax1.set_title('Mean of RKE per scheme')
    ax1.legend(title='QKD scheme')

    ax2.bar(schemes_title, rke_stds, label=schemes_title, color=schemes_color)
    ax2.set_ylabel('Standard deviation')
    ax2.set_title('Standard deviation of RKE per scheme')
    ax2.legend(title='QKD scheme')

    plt.show()

    """"
    fig, ax = plt.subplots()
    ax.bar(schemes_title, [scheme.rke() for scheme in schemes_res], label=schemes_title, color=schemes_color)
    ax.set_ylabel('RKE')
    ax.set_title('QKD scheme')
    ax.legend(title='Raw Key Efficiencies')
    plt.show()

    print("BB84 RKE:\t", bb84_res.rke(), "\n")
    print("E91 RKE:\t", e91_res.rke(), "\n")
    print("B92 RKE:\t", b92_res.rke(), "\n")

    print("BB84 QBER:\t", bb84_res.qber(), "\n")
    print("E91 QBER:\t", e91_res.qber(), "\n")
    print("B92 QBER:\t", b92_res.qber(), "\n")

    bb84_e = BB84Scheme(True)
    e91_e = E91Scheme(True)
    b92_e = B92Scheme(True)
    bb84_e_res = bb84_e.run(num_shots)
    e91_e_res = e91_e.run(num_shots)
    b92_e_res = b92_e.run(num_shots)

    print("BB84 (w/ eve) RKE:\t", bb84_e_res.rke(), "\n")
    print("BB84 (w/ eve) QBER:\t", bb84_e_res.qber(), "\n")
    print("E91 (w/ eve) RKE:\t", e91_e_res.rke(), "\n")
    print("E91 (w/ eve) QBER:\t", e91_e_res.qber(), "\n")
    print("B92 (w/ eve) RKE:\t", b92_e_res.rke(), "\n")
    print("B92 (w/ eve) RKE:\t", b92_e_res.rke(), "\n")
    print("B92 (w/ eve) QBER:\t", b92_e_res.qber(), "\n")
    """
