import numpy as np

from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

num_iters = 10
sender_basis = np.empty(num_iters, dtype='<U1')
sender_bits = np.empty(num_iters, dtype='<i4')
receiver_basis = np.empty(num_iters, dtype='<U1')
receiver_bits = np.empty(num_iters, dtype='<i4')

simulator = QasmSimulator()
for i in range(num_iters):
    qreg_q = QuantumRegister(1, 'q')
    creg_r_bit = ClassicalRegister(1, 'r_bit')
    creg_s_bit = ClassicalRegister(1, 's_bit')
    creg_r_bas = ClassicalRegister(1, 'r_bas')
    creg_s_bas = ClassicalRegister(1, 's_bas')
    circuit = QuantumCircuit(qreg_q, creg_r_bit, creg_s_bit, creg_r_bas, creg_s_bas)

    circuit.h(qreg_q[0])
    circuit.measure(qreg_q[0], creg_s_bas[0])
    circuit.h(qreg_q[0])
    circuit.measure(qreg_q[0], creg_r_bas[0])
    circuit.barrier(qreg_q[0])
    circuit.h(qreg_q[0])
    circuit.measure(qreg_q[0], creg_s_bit[0])
    circuit.h(qreg_q[0]).c_if(creg_s_bas, 1)
    circuit.barrier(qreg_q[0])
    circuit.h(qreg_q[0]).c_if(creg_r_bas, 1)
    circuit.measure(qreg_q[0], creg_r_bit[0])

    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts_arr = np.array(list(result.get_counts().keys())[0].split(), dtype='<i4')
    
    sender_basis[i] = '+' if counts_arr[0] == 0 else 'X'
    sender_bits[i] = counts_arr[2]
    receiver_basis[i] = '+' if counts_arr[1] == 0 else 'X'
    receiver_bits[i] = counts_arr[3]

rke = (sender_basis == receiver_basis).mean()
key = sender_bits[np.where((sender_basis == receiver_basis) == True)[0]]
rkey = receiver_bits[np.where((sender_basis == receiver_basis) == True)[0]]

print("S Basis\t", sender_basis)
print("S Bits\t", sender_bits)
print("R Basis\t", receiver_basis)
print("R Bits\t", receiver_bits)
print("Basis match rate\t", rke)
print("S Key\t", key)
print("R Key\t", rkey)

    # compile the circuit down to low-level QASM instructions
    # supported by the backend (not needed for simple circuits)
    #compiled_circuit = transpile(circuit, simulator)

    # Execute the circuit on the qasm simulator
    #job = simulator.run(compiled_circuit, shots=1)

    # Grab results from the job
    #result = job.result()
    #for key in result.get_counts().keys():
    #    receiverBits.append(int(key))

