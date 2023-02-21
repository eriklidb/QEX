import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

numIters = 5 
debug = False
senderBasis = []
senderBits = []
receiverBasis = []
receiverBits = []

for i in range(numIters):
    # Use Aer's qasm_simulator
    simulator = QasmSimulator()

    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(1, 1)

    senderBits.append(0)
    senderUseX = np.random.choice([False, True])
    if senderUseX:
        circuit.x(0)
        senderBits[i] = 1

    senderUseH = np.random.choice([False, True])
    if senderUseH:
        circuit.h(0)
        senderBasis.append('X')
    else:
        senderBasis.append('Z')

    receiverUseH = np.random.choice([False, True])
    if receiverUseH:
        circuit.h(0)
        receiverBasis.append('X')
    else:
        receiverBasis.append('Z')
    circuit.measure([0], [0])

    # compile the circuit down to low-level QASM instructions
    # supported by the backend (not needed for simple circuits)
    compiled_circuit = transpile(circuit, simulator)

    # Execute the circuit on the qasm simulator
    job = simulator.run(compiled_circuit, shots=1)

    # Grab results from the job
    result = job.result()
    for key in result.get_counts().keys():
        receiverBits.append(int(key))

    # Returns counts
    if debug:
        print("Sender use X = ", senderUseX)
        print("Sender use H = ", senderUseH)
        print("Receiver use H = ", receiverUseH)
        #print("Sender classical bits = ", senderBit)
        print("Receiver classical bits = ", result.get_counts())

print(senderBasis)
print(senderBits)
print(receiverBasis)
print(receiverBits)
