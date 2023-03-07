from qiskit.providers.aer import QasmSimulator

import abc

class QKDBits():
    bit_sent: bool
    bit_recv: bool
    certain: bool

    def __hash__(self):
        return hash((self.bit_sent, self.bit_recv, self.certain))

    def __eq__(self, other):
        return (self.bit_sent, self.bit_recv, self.certain) == (self.bit_sent, self.bit_recv, self.certain)

    def __str__(self):
        return f"Bits(S:{'01'[self.bit_sent]}, R:{'01'[self.bit_recv]}, C:{self.certain})"

    def __repr__(self):
        return self.__str__()

class QKDResults():
    _total_count: int
    _bit_counts: dict[QKDBits, int]
    _certainty_count: int | None

    def __init__(self, bit_counts: dict[QKDBits, int]):
        self._bit_counts = bit_counts
        self._total_count = sum([count for (bits, count) in self._bit_counts.items()])
        self._rke = None
        self._certainty_count = None

    def raw_key_efficiency(self):
        if self._certainty_count is None:
            self._certainty_count = sum([count for (bits, count) in self._bit_counts.items() if bits.certain])
        print("[dgb] certainty_count", self._certainty_count)
        print("[dgb] total_count", self._total_count)
        return self._certainty_count / self._total_count

    def rke(self):
        return self.raw_key_efficiency()

class QKDScheme(abc.ABC):
    def _get_circuit(self):
        pass
    def _interpret_bits(self, bits_str: str) -> QKDBits:
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
            if bits not in bit_counts:
                bit_counts[bits] = 0
            bit_counts[bits] += bits_count
        return QKDResults(bit_counts)
