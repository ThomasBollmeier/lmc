from unittest import TestCase
from lmc.lmc import LMC


class TestIn(object):

    def __init__(self, numbers):
        self._numbers = numbers
        self._curr = 0

    def read_value(self):
        ret = self._numbers[self._curr]
        self._curr += 1
        return ret


class TestOut(object):

    def __init__(self):
        self.out = []

    def write(self, value):
        self.out.append(value)


class TestLMC(TestCase):

    def setUp(self):
        self.lmc = LMC()

    def test_load_program(self):
        instructions = [
            550,
            151,
            252,
            902,
            0
        ]
        self.lmc.load_program(instructions)
        address = self.lmc.get_free_data_address()
        self.assertEqual(5, address)

    def test_run_program(self):

        self.lmc.set_data(50, 40)
        self.lmc.set_data(51, 3)
        self.lmc.set_data(52, 1)

        instructions = [
            550,
            151,
            252,
            902,
            0
        ]
        self.lmc.load_program(instructions)

        out = TestOut()
        self.lmc.set_output(out)

        self.lmc.run()

        self.assertEqual([42], out.out)

    def test_get_free_data_address(self):
        address = self.lmc.get_free_data_address()
        self.assertEqual(0, address)
        self.lmc.set_data(address, 42)
        address = self.lmc.get_free_data_address()
        self.assertEqual(1, address)

    def test_set_data(self):
        self.lmc.set_data(0, 42)
        self.assertEqual(42, self.lmc._mem[0])

    def test_add(self):
        self.lmc.set_data(50, 41)
        self.lmc.set_data(51, 1)
        self.lmc.load(50)
        self.lmc.add(51)
        self.assertEqual(42, self.lmc._acc)

    def test_sub(self):
        self.lmc.set_data(50, 43)
        self.lmc.set_data(51, 1)
        self.lmc.load(50)
        self.lmc.sub(51)
        self.assertEqual(42, self.lmc._acc)

    def test_load_and_store(self):
        self.lmc.set_data(50, 42)
        self.lmc.load(50)
        self.lmc.store(51)
        self.assertEqual(42, self.lmc._acc)
        self.assertEqual(42, self.lmc._mem[51])

    def test_branch(self):
        self.lmc.set_data(50, 5)
        self.lmc.branch(50)
        self.assertEqual(5, self.lmc._pc)

    def test_branch_if_zero(self):
        self.lmc._acc = 4
        jump_addr = 5
        self.lmc.set_data(50, jump_addr)
        self.lmc.branch_if_zero(50)
        self.assertEqual(0, self.lmc._pc)

        self.lmc._acc = 0
        self.lmc.branch_if_zero(50)
        self.assertEqual(jump_addr, self.lmc._pc)

    def test_branch_if_positive(self):
        self.lmc._acc = -4
        self.lmc._negative = True
        jump_addr = 5
        self.lmc.set_data(50, jump_addr)
        self.lmc.branch_if_positive(50)
        self.assertEqual(0, self.lmc._pc)

        self.lmc._acc = 4
        self.lmc._negative = False
        self.lmc.branch_if_positive(50)
        self.assertEqual(jump_addr, self.lmc._pc)

    def test_inp(self):
        self.lmc.set_input(TestIn([42]))
        self.lmc.inp()
        self.assertEqual(42, self.lmc._acc)

    def test_out(self):
        out = TestOut()
        self.lmc.set_output(out)
        self.lmc._acc = 42
        self.lmc.out()
        self.assertEqual([42], out.out)
