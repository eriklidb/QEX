import numpy as np

from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

num_iters = 10
sender_basis = np.empty(num_iters, dtype='<i4')
receiver_basis = np.empty(num_iters, dtype='<i4')
receiver_certain = np.empty(num_iters, dtype='<i4')

eavesdropper = False

if eavesdropper:
    eavesdropper_basis = np.empty(num_iters, dtype='<U1')
    eavesdropper_bits = np.empty(num_iters, dtype='<i4')

simulator = QasmSimulator()
for i in range(num_iters):

    qreg_q = QuantumRegister(1, 'q')
    creg_s_bas = ClassicalRegister(1, 's_bas')
    creg_r_bas = ClassicalRegister(1, 'r_bas')
    creg_r_certain = ClassicalRegister(1, 'r_certain')
    circuit = QuantumCircuit(qreg_q, creg_s_bas, creg_r_bas, creg_r_certain)

    circuit.h(qreg_q[0])
    circuit.measure(qreg_q[0], creg_r_bas[0])
    circuit.h(qreg_q[0])
    circuit.measure(qreg_q[0], creg_s_bas[0])
    circuit.barrier(qreg_q[0])
    circuit.reset(qreg_q[0])
    circuit.h(qreg_q[0]).c_if(creg_s_bas, 1)
    circuit.barrier(qreg_q[0])
    circuit.h(qreg_q[0]).c_if(creg_r_bas, 0)
    circuit.measure(qreg_q[0], creg_r_certain[0])

    circuit.draw()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts_arr = np.array(list(result.get_counts().keys())[0].split(), dtype='<i4')
    
    sender_basis[i] = 0 if counts_arr[2] == 0 else 1 # TODO: Rename to bits
    receiver_basis[i] = 0 if counts_arr[1] == 0 else 1
    receiver_certain[i] = counts_arr[0]

rke = receiver_certain.mean()
key = sender_basis[np.where(receiver_certain)[0]]
rkey = receiver_basis[np.where(receiver_certain)[0]]
if eavesdropper:
    ekey = eavesdropper_bits[np.where(receiver_certain)[0]]


print("S Basis\t", sender_basis)
print("R Basis\t", receiver_basis)
print("R Certain\t", receiver_certain)
if eavesdropper:
    print("E Basis\t", eavesdropper_basis)
    print("E Bits\t", eavesdropper_bits)
print("Raw key efficiency\t", rke)
print("S Key\t", key)
print("R Key\t", rkey)
if eavesdropper:
    print("E Key\t", ekey)

    # compile the circuit down to low-level QASM instructions
    # supported by the backend (not needed for simple circuits)
    #compiled_circuit = transpile(circuit, simulator)

    # Execute the circuit on the qasm simulator
    #job = simulator.run(compiled_circuit, shots=1)

    # Grab results from the job
    #result = job.result()
    #for key in result.get_counts().keys():
    #    receiverBits.append(int(key))

