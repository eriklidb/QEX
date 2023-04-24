from bb84 import BB84Scheme
from e91 import E91Scheme
from b92 import B92Scheme
import matplotlib.pyplot as plt 

if __name__ == "__main__":
    num_shots = 1e6

    bb84 = BB84Scheme(False)
    e91 = E91Scheme(False)
    b92 = B92Scheme(False)
    bb84_res = bb84.run(num_shots)
    e91_res = e91.run(num_shots)
    b92_res = b92.run(num_shots)

    schemes_res = [bb84_res, e91_res, b92_res]

    print("\n")
    for scheme_res in schemes_res:
        print(scheme_res._title, "RKE:\t", scheme_res.rke(), "\n")

    schemes_title = [scheme._title for scheme in schemes_res]
    schemes_color = ['tab:red', 'tab:green', 'tab:blue']

    fig, ax = plt.subplots()

    ax.bar(schemes_title, [scheme.rke() for scheme in schemes_res], label=schemes_title, color=schemes_color)
    ax.set_ylabel('RKE')
    ax.set_title('QKD scheme')
    ax.legend(title='Raw Key Efficiencies')

    plt.show()


    """
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
