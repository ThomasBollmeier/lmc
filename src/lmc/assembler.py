import re


class Assembler(object):

    mnemonics = [
        "ADD",
        "SUB",
        "STA",
        "LDA",
        "BRA",
        "BRZ",
        "BRP",
        "INP",
        "OUT",
        "HLT",
        "COB",
        "DAT"
    ]

    def __init__(self):
        self._inst_labels = {}  # instruction labels
        self._data_labels = {}

    def assemble(self, assembly_lines):
        self._inst_labels = {}
        self._data_labels = {}
        self._first_pass(assembly_lines)

    def _first_pass(self, assembly_lines):
        cmd_cnt = 0
        data_cnt = 0
        for line in assembly_lines:
            if not line:
                continue
            line = re.sub("//.*", "", line)
            parts = [s.upper() for s in line.split()]
            if "DAT" not in parts:
                # command line
                print(parts)
                cmd_cnt += 1
            else:
                # data line
                data_cnt += 1
