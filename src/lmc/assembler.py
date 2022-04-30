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

    def run(self, assembly_lines, lmc):
        instructions, mem_values = self.assemble(assembly_lines)
        lmc.clear_memory()
        lmc.load_program(instructions)
        for address, value in mem_values:
            lmc.set_data(address, value)
        lmc.run()

    def assemble(self, assembly_lines):
        instructions = []
        data = []
        labels = {}
        variables = {}
        for line in assembly_lines:
            if not line:
                continue
            line = re.sub("//.*", "", line)
            parts = [s.upper() for s in line.split()]
            parse_result = self._parse(parts)
            if parse_result["instruction"] != "DAT":
                instructions.append(parse_result)
            else:
                data.append(parse_result)
        for i, instruction in enumerate(instructions):
            name = instruction["label"]
            if name:
                labels[name] = i
        num_instructions = len(instructions)
        for i, d in enumerate(data):
            name = d["label"]
            if name:
                variables[name] = num_instructions + i
        instructions = self._calc_instruction_codes(instructions, labels, variables)
        memory_values = self._calc_memory_init(data, num_instructions)
        return instructions, memory_values

    @staticmethod
    def _calc_memory_init(data, program_size):
        ret = []
        for i, d in enumerate(data):
            address = program_size + i
            value = int(d["data"]) if d["data"] else 0
            ret.append((address, value))
        return ret

    def _calc_instruction_codes(self, instructions, labels, variables):
        ret = []
        for inst in instructions:
            d = inst["data"]
            if not d:
                address = None
            elif d in labels:
                address = int(labels[d])
            elif d in variables:
                address = int(variables[d])
            else:
                address = int(d)
            ret.append(self._calc_instruction_code(inst["instruction"], address))
        return ret

    @staticmethod
    def _calc_instruction_code(mnemonic, address):
        opcodes = {
            "ADD": 1,
            "SUB": 2,
            "STA": 3,
            "LDA": 5,
            "BRA": 6,
            "BRZ": 7,
            "BRP": 8,
            "INP": 901,
            "OUT": 902,
            "HLT": 0,
            "COB": 0
        }
        if mnemonic not in opcodes:
            raise Exception("Illegal instruction")
        ret = opcodes[mnemonic]
        if address is not None:
            ret = ret * 100 + address
        return ret

    def _parse(self, parts):
        for mnemonic in self.mnemonics:
            try:
                idx = parts.index(mnemonic)
                label = parts[0] if idx == 1 else ""
                data = parts[idx + 1] if idx < len(parts) - 1 else ""
                return {
                    "instruction": mnemonic,
                    "data": data,
                    "label": label
                }
            except ValueError:
                pass
        raise Exception("Illegal instruction")