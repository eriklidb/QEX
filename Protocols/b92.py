from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator

import core


class B92Scheme(core.QKDScheme):
    def __init__(self, eavesdropper: bool):
        simulator = QasmSimulator()
        qreg_q = QuantumRegister(1, 'q')
        
        if eavesdropper:
            creg_e_bit = ClassicalRegister(1, 'e_bit')
            creg_e_certain = ClassicalRegister(1, 'e_certain')
        creg_s_bit = ClassicalRegister(1, 's_bit')
        creg_r_bit = ClassicalRegister(1, 'r_bit')
        creg_r_certain = ClassicalRegister(1, 'r_certain')
        
        if eavesdropper:
            circuit = QuantumCircuit(qreg_q, creg_e_bit, creg_e_certain, creg_s_bit, creg_r_bit, creg_r_certain)
        else:
            circuit = QuantumCircuit(qreg_q, creg_s_bit, creg_r_bit, creg_r_certain)

        # RNG for basis
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_r_bit[0])
        circuit.h(qreg_q[0])
        circuit.measure(qreg_q[0], creg_s_bit[0])
        circuit.barrier(qreg_q[0])

        # Sender
        circuit.reset(qreg_q[0])
        circuit.h(qreg_q[0]).c_if(creg_s_bit, 1)
        circuit.barrier(qreg_q[0])

        # Eavesdropper
        if eavesdropper:
            circuit.h(qreg_q[0]).c_if(creg_e_bit, 0)
            circuit.measure(qreg_q[0], creg_e_certain[0])
            circuit.reset(qreg_q[0])
            circuit.h(qreg_q[0]).c_if(creg_e_bit, 1)


        # Receiver
        circuit.h(qreg_q[0]).c_if(creg_r_bit, 0)
        circuit.measure(qreg_q[0], creg_r_certain[0])

        self._circuit = transpile(circuit, simulator)
        self._eavesdropper = eavesdropper

    def _get_circuit(self):
        return self._circuit

    def _interpret_bits(self, bits_str: str) -> core.QKDBits:
        bit_sent = bits_str[2] == '1'
        bit_recv = bits_str[1] == '1'
        certain = bits_str[0] == '1'
        if self._eavesdropper:
            bit_eavesdropped = bits_str[4] == '1'
        bits = core.QKDBits()
        bits.bit_sent = bit_sent
        bits.bit_recv = bit_recv
        bits.certain = certain
        if self._eavesdropper:
            bits.bit_eavesdropped = bit_eavesdropped
        return bits

