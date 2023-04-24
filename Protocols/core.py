from qiskit.providers.aer import QasmSimulator
import numpy as np

import abc

class QKDBits():
    bit_sent: bool
    bit_recv: bool
    certain: bool   # IF bases agree
    error: bool     # IF bits do not agree
    bit_eavesdropped: bool | None

    def __init__(self):
        self.bit_eavesdropped = None

    def __hash__(self):
        return hash((self.bit_sent, self.bit_recv, self.certain, self.bit_eavesdropped))

    def __eq__(self, other):
        return (self.bit_sent, self.bit_recv, self.certain, self.bit_eavesdropped) == (self.bit_sent, self.bit_recv, self.certain, self.bit_eavesdropped)

    def __str__(self):
        partial = f"Bits(S:{'01'[self.bit_sent]}, R:{'01'[self.bit_recv]}, C:{self.certain}"
        if self.bit_eavesdropped is not None:
            partial += f", E:{self.bit_eavesdropped}"
        partial += ")"
        return partial

    def __repr__(self):
        return self.__str__()

    def _calc_error(self):
        self.error = self.bit_sent != self.bit_recv


class QKDResults():
    _total_count: int
    _bit_counts: dict[QKDBits, int]
    _certainty_count: int | None
    _bit_error_count: int | None
    _rke: float

    def __init__(self, bit_counts: dict[QKDBits, int]):
        self._bit_counts = bit_counts
        self._total_count = sum([count for count in self._bit_counts.values()])
        self._rke = None
        self._certainty_count = None
        self._bit_error_count = None

    def raw_key_efficiency(self):
        self._calc_certainty_count()
        print("[dgb] certainty_count", self._certainty_count)
        print("[dgb] total_count", self._total_count)
        return self._certainty_count / self._total_count

    def rke(self):
        if self._rke == None:
            self._rke = self.raw_key_efficiency()
        return self._rke

    def quantum_bit_error_rate(self):
        self._calc_certainty_count()
        if self._bit_error_count is None:
            self._bit_error_count = sum([count for (bits, count) in self._bit_counts.items() if bits.certain and bits.error])
        print("[dgb] bit_error_count", self._bit_error_count)
        print("[dgb] certainty_count", self._certainty_count)
        if self._certainty_count > 0:
            return self._bit_error_count / self._certainty_count
        else:
            return 0

    def qber(self):
        return self.quantum_bit_error_rate()

    def _calc_certainty_count(self):
        if self._certainty_count is None:
            self._certainty_count = sum([count for (bits, count) in self._bit_counts.items() if bits.certain])

class QKDScheme(abc.ABC):
    def _get_circuit(self):
        pass
    def _interpret_bits(self, bits_str: str) -> QKDBits:
        pass
    def __str__(self):
        pass
    def run(self, shots: int) -> QKDResults:
        simulator = QasmSimulator()
        bit_counts = dict()
        circ = self._get_circuit()
        job = simulator.run(circ, shots=shots)
        result = job.result().get_counts()
        print("[dbg] result", result)
        for bits_str, bits_count in result.items():
            bits_str = bits_str.replace(" ", "")
            bits = self._interpret_bits(bits_str)
            bits._calc_error()
            if bits not in bit_counts:
                bit_counts[bits] = 0
            bit_counts[bits] += bits_count
        return QKDResults(bit_counts)
        