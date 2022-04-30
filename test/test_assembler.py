from unittest import TestCase
from lmc.assembler import Assembler
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


class TestAssembler(TestCase):

    def test_run(self):
        assembler = Assembler()
        in_ = TestIn([6, 7])
        out = TestOut()
        lmc = LMC(in_=in_, out=out)

        assembler.run(self._read_assembly("data/mult.lmc"), lmc)

        self.assertEqual([42], out.out)

    def test_assemble(self):
        assembler = Assembler()
        assembler.assemble(self._read_assembly("data/mult.lmc"))

    @staticmethod
    def _read_assembly(path):
        f = open(path)
        ret = f.readlines()
        f.close()
        return ret
