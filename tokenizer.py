import re
from typing import Iterator
from tokendef import *

class Tokenizer:
    pattern: re.Pattern
    skip = r"([\s]*(;.*\n)?)*"
    opecode = r"add|sub|mul|div|cmp|abs|adc|sbc|shl|shr|ash|rol|ror|and|or|not|xor|mov|setl|seth|load|store|nop|hlt|jmp|jz|je|jnz|jne|ja|jnbe|jb|jnae|jc|jcc|jr"
    register = r"r1?[0-9]"
    val0b = r"\$-?0b[01]+"
    val0x = r"\$-?0x[0-9a-f]+"
    val10 = r"\$-?[0-9]+"
    labelset = r"[a-zA-Z_][a-zA-Z0-9_]*:"
    labelget = r":[a-zA-Z_][a-zA-Z0-9_]*"
    regexp = r"{}(({})|({})|({})|({})|({})|({})|({}))".format(skip, opecode, register, val0b, val0x, val10, labelget, labelset)

    def __init__(self):
        self.pattern = re.compile(self.regexp)

    def tokenize(self, input: str) -> Iterator[Token]:
        i = 0
        while result := self.pattern.match(input, i):
            match result.groups()[-7:]:
                case (opc, None, None, None, None, None, None): yield Opecode(opc)
                case (None, reg, None, None, None, None, None): yield Register(int(reg[1:]))
                case (None, None, imm0b, None, None, None, None): yield Immdval(int(imm0b[1:], 2))
                case (None, None, None, imm0x, None, None, None): yield Immdval(int(imm0x[1:], 16))
                case (None, None, None, None, imm10, None, None): yield Immdval(int(imm10[1:]))
                case (None, None, None, None, None, lbl, None): yield LabelGet(lbl[1:])
                case (None, None, None, None, None, None, lbl): yield LabelSet(lbl[:-1])
            i = result.end()
        yield End()