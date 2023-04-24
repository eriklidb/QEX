from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator

import core


class BB84Scheme(core.QKDScheme):
    def __init__(self, eavesdropper: bool):
        simulator = QasmSimulator()
        qreg_q = QuantumRegister(1, 'q')

        if eavesdropper:
            creg_e_bit = ClassicalRegister(1, 'e_bit')
            creg_e_bas = ClassicalRegister(1, 'e_bas')
        creg_r_bit = ClassicalRegister(1, 'r_bit')
        creg_s_bit = ClassicalRegister(1, 's_bit')
        creg_r_bas = ClassicalRegister(1, 'r_bas')
        creg_s_bas = ClassicalRegister(1, 's_bas')

        if eavesdropper:
            circuit = QuantumCircuit(qreg_q, creg_e_bit, creg_e_bas, creg_r_bit, creg_s_bit, creg_r_bas, creg_s_bas)
        else:
            circuit = QuantumCircuit(qreg_q, creg_r_bit, creg_s_bit, creg_r_bas, creg_s_bas)

        # RNG for basis
        if eavesdropper:
            circuit.h(qreg_q[0])
            circuit.measure(qreg_q[0], creg_e_bas[0])
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_s_bas[0])
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_r_bas[0])
        circuit.barrier(qreg_q[0])

        # Sender
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_s_bit[0])
        circuit.h(qreg_q[0]).c_if(creg_s_bas, 1)
        circuit.barrier(qreg_q[0])

        # Eavesdropper
        if eavesdropper:
            circuit.h(qreg_q[0]).c_if(creg_e_bas, 1)
            circuit.measure(qreg_q[0], creg_e_bit[0])
            circuit.h(qreg_q[0]).c_if(creg_e_bas, 1)

        # Receiver
        circuit.h(qreg_q[0]).c_if(creg_r_bas, 1)
        circuit.measure(qreg_q[0], creg_r_bit[0])

        self._circuit = transpile(circuit, simulator)
        self._eavesdropper = eavesdropper

    def _get_circuit(self):
        return self._circuit

    def _interpret_bits(self, bits_str: str) -> core.QKDBits:
        bit_sent = bits_str[2] == '1'
        bit_recv = bits_str[3] == '1'
        basis_sent = bits_str[0]
        basis_recv = bits_str[1]
        if self._eavesdropper:
            basis_eavesdropped = bits_str[4] == '1'
            bit_eavesdropped = bits_str[5] == '1'
        certain = basis_sent == basis_recv
        bits = core.QKDBits()
        bits.bit_sent = bit_sent
        bits.bit_recv = bit_recv
        bits.certain = certain
        if self._eavesdropper:
            bits.bit_eavesdropped = bit_eavesdropped
        return bits

    def __str__(self):
        return "BB84"
