class Instruction:
    opc: str
    immf: bool
    rd: int
    rs: int
    imm: int

    def __init__(self, opecode: str, rd: int, rs: int, imm: int):
        self.opc = opecode
        oprtype = self.calc_oprtype(opecode)
        if not oprtype[0][0] and rs != None:
            raise Exception(f"Opecode({opecode}) does not take source register")
        if not oprtype[0][1] and imm != None and not oprtype[1]:
            raise Exception(f"Opecode({opecode}) does not take immidiate value")
        if not oprtype[1] and imm != None and rs != None:
            raise Exception(f"Opecode({opecode}) does not take 3 operands")

        if rd == None:
            self.rd = 0
        else:
            self.rd = rd
        if rs == None:
            self.rs = 0
        else:
            self.rs = rs
        if imm == None:
            self.immf = False
            self.imm = 0
        else:
            if imm > 0xffff:
                raise Exception(f"Immediate value({imm}) is too large < 2^16")
            self.immf = True
            self.imm = imm

    def get_bitcode(self) -> str:
        return f"0b{self.calc_opecode(self.opc):07b}{self.immf:01b}{self.rd:04b}{self.rs:04b}{self.imm & 0xffff:016b}"
    
    def get_hexcode(self) -> str:
        return f"{int(self.get_bitcode(), 2):08x}"

    def __str__(self) -> str:
        return self.get_hexcode()

    @staticmethod
    def calc_opecode(opecode) -> int:
        match opecode:
            case "add":
                return 0b000_0000
            case "sub":
                return 0b000_0001
            case "mul":
                return 0b000_0010
            case "div":
                return 0b000_0011
            case "cmp":
                return 0b000_0100
            case "abs":
                return 0b000_0101
            case "adc":
                return 0b000_0110
            case "sbc":
                return 0b000_0111
            case "shl":
                return 0b000_1000
            case "shr":
                return 0b000_1001
            case "ash":
                return 0b000_1010
            case "rol":
                return 0b000_1100
            case "ror":
                return 0b000_1101
            case "and":
                return 0b001_0000
            case "or":
                return 0b001_0001
            case "not":
                return 0b001_0010
            case "xor":
                return 0b001_0011
            case "setl":
                return 0b001_0110
            case "seth":
                return 0b001_0111
            case "load":
                return 0b001_1000
            case "store":
                return 0b001_1001
            case "jmp":
                return 0b001_1100
            case "jmpa":
                return 0b001_1101
            case "nop":
                return 0b001_1110
            case "hlt":
                return 0b001_1111

    @staticmethod
    def calc_oprtype(opecode: str) -> tuple[tuple[bool, bool], bool]:
        match opecode:
            case "add" | "sub" | "mul" | "div" | "cmp" | "abs" | "adc" | "sbc" | "shl" | "shr" | "ash" | "rol" | "ror" | "jmp":
                return (True, True), False
            case "and" | "or" | "not" | "xor":
                return (True, False), False
            case "setl" | "seth":
                return (False, True), False
            case "load" | "store":
                return (True, False), True
            case "jmpa":
                return (True, True), False
            case "nop" | "hlt":
                return (False, False), False