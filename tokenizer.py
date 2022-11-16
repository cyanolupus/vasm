import re
from typing import Iterator
from tokendef import *

class Tokenizer:
    pattern: re.Pattern
    skip = r"([\s]*(;.*\n)?)*"
    opecode = r"add|sub|mul|div|cmp|abs|adc|sbc|shl|shr|ash|rol|ror|and|or|not|xor|mov|setl|seth|load|store|jmpa|jmp|nop|hlt"
    register = r"r1?[0-9]"
    immdval = r"\$-?0?x?b?[0-9a-f]+"
    labelset = r"[a-zA-Z_][a-zA-Z0-9_]*:"
    labelget = r":[a-zA-Z_][a-zA-Z0-9_]*"
    regexp = r"{}(({})|({})|({})|({})|({}))".format(skip, opecode, register, immdval, labelget, labelset)

    def __init__(self):
        self.pattern = re.compile(self.regexp)

    def tokenize(self, input: str) -> Iterator[Token]:
        i = 0
        while result := self.pattern.match(input, i):
            match result.groups()[-5:]:
                case (opc, None, None, None, None): yield Opecode(opc)
                case (None, reg, None, None, None): yield Register(int(reg[1:]))
                case (None, None, imm, None, None): yield Immdval(int(imm[1:], 0))
                case (None, None, None, lbl, None): yield LabelGet(lbl[1:])
                case (None, None, None, None, lbl): yield LabelSet(lbl[:-1])
            i = result.end()
        yield End()