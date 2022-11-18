from instruction import Instruction
from tokenizer import Tokenizer
from tokendef import *

class Parser:
    label_dict: dict[str:int]

    def __init__(self):
        self.label_dict = {}

    def parse(self, code) -> list[Instruction]:
        address = 0
        instructions = []
        opecode = None
        rd = None
        rs = None
        imm = None

        for token in Tokenizer().tokenize(code):
            match token:
                case Opecode(name):
                    address += 1
                case LabelSet(name):
                    self.label_dict[name] = address
                case _: pass
        for token in Tokenizer().tokenize(code):
            match token:
                case Opecode(name):
                    if opecode != None:
                        instructions.append(Instruction(opecode, rd, rs, imm))
                    opecode = name
                    rd = None
                    rs = None
                    imm = None
                case Register(value):
                    if rd == None:
                        rd = value
                    elif rs == None:
                        rs = value
                    else:
                        raise Exception("Too many registers")
                case Immdval(value):
                    if imm == None:
                        imm = value
                    else:
                        raise Exception("Too many immediate values")
                case LabelGet(name):
                    if imm == None:
                        if name in self.label_dict:
                            imm = self.label_dict[name]
                        else:
                            raise Exception(f"Label not found: {name}")
                    else:
                        raise Exception("Label cannot be used with immediate value")
                case End():
                    instructions.append(Instruction(opecode, rd, rs, imm))
                case LabelSet(name):
                    pass
                case _: raise Exception("Invalid operand")
        return instructions

    @staticmethod
    def parse_imm(imm: str) -> str:
        try:
            imm = imm.replace("#", "")
            return int(imm, 0)
        except ValueError:
            raise Exception("Invalid immediate value")

    @staticmethod
    def parse_reg(reg: str) -> str:
        try:
            reg = reg.replace("r", "")
            return int(reg, 0)
        except ValueError:
            raise Exception("Invalid register")