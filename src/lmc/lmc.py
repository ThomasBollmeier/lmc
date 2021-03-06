from lmc.inout import Stdin, Stdout


class LMC(object):
    """
    The Little Man Computer
    """

    MEM_SIZE = 100

    def __init__(self, in_=Stdin(), out=Stdout()):

        self._mem = [None for _ in range(self.MEM_SIZE)]

        self._pc = 0  # program counter
        self._acc = 0  # accumulator
        self._negative = False  # negative acc flag
        self._prog_size = 0

        self._in = in_
        self._out = out

        self._done = False

    def set_input(self, in_):
        self._in = in_

    def set_output(self, out):
        self._out = out

    def clear_memory(self):
        self._mem = [None for _ in range(self.MEM_SIZE)]

    def load_program(self, instructions):
        self._prog_size = len(instructions)
        for idx, instruction in enumerate(instructions):
            self._mem[idx] = instruction
        self._pc = 0
        self._acc = 0
        self._negative = False

    def get_free_data_address(self):
        address = self._prog_size
        mem_size = len(self._mem)
        while address < mem_size:
            if self._mem[address] is None:
                return address
            address += 1
        return None

    def set_data(self, address, value):
        self._mem[address] = value

    def run(self):
        self._done = False
        while not self._done:
            instruction = self._fetch()
            if instruction is None:
                break
            opcode, address = self._decode(instruction)
            self._execute(opcode, address)

    def _fetch(self):
        ret = self._mem[self._pc]
        self._pc += 1
        return ret

    @staticmethod
    def _decode(instruction):
        if instruction == 0:
            return 0, 0
        instruction_str = str(instruction)
        opcode = int(instruction_str[0])
        address = int(instruction_str[1:])
        return opcode, address

    def _execute(self, opcode, address):
        if opcode == 1:
            self.add(address)
        elif opcode == 2:
            self.sub(address)
        elif opcode == 3:
            self.store(address)
        elif opcode == 5:
            self.load(address)
        elif opcode == 6:
            self.branch(address)
        elif opcode == 7:
            self.branch_if_zero(address)
        elif opcode == 8:
            self.branch_if_positive(address)
        elif opcode == 9:
            if address == 1:
                self.inp()
            elif address == 2:
                self.out()
            else:
                raise Exception("Illegal opcode")
        elif opcode == 0:
            if address == 0:
                self.halt()
            else:
                raise Exception("Illegal opcode")
        else:
            raise Exception("Illegal opcode")

    def add(self, address):
        self._acc += self._mem[address]
        self._negative = self._acc < 0

    def sub(self, address):
        self._acc -= self._mem[address]
        self._negative = self._acc < 0

    def store(self, address):
        self._mem[address] = self._acc

    def load(self, address):
        self._acc = self._mem[address]
        self._negative = self._acc < 0

    def branch(self, address):
        self._pc = address

    def branch_if_zero(self, address):
        if self._acc == 0 and not self._negative:
            self._pc = address

    def branch_if_positive(self, address):
        if self._acc >= 0 and not self._negative:
            self._pc = address

    def inp(self):
        self._acc = self._in.read_value()
        self._negative = self._acc < 0

    def out(self):
        self._out.write(self._acc)

    def halt(self):
        self._done = True


