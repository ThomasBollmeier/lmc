from lmc.inout import Stdin, Stdout


class LMC(object):
    """
    The Little Man Computer
    """

    MEM_SIZE = 100

    def __init__(self):
        self._pc = 0  # program counter
        self._acc = 0  # accumulator
        self._negative = False

        self._reset_memory()

        self._in = Stdin()
        self._out = Stdout()

    def _reset_memory(self):
        self._mem = []
        for _ in range(self.MEM_SIZE):
            self._mem.append(0)

    def add(self, address):
        self._acc += self._mem[address]
        self._negative = False

    def sub(self, address):
        value = self._mem[address]
        if self._acc >= value:
            self._acc -= value
            self._negative = False
        else:
            self._negative = True

    def store(self, address):
        self._mem[address] = self._acc

    def load(self, address):
        self._acc = self._mem[address]
        self._negative = False

    def branch(self, address):
        self._pc = self._mem[address]

    def branch_if_zero(self, address):
        if self._acc == 0 and not self._negative:
            self._pc = self._mem[address]

    def branch_if_positive(self, address):
        if self._acc >= 0 and not self._negative:
            self._pc = self._mem[address]

    def inp(self):
        self._acc = self._in.next_value()
        self._negative = False

    def out(self):
        self._out.write(self._acc)

