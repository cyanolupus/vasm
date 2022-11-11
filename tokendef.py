from dataclasses import dataclass

class Token: pass

@dataclass
class Opecode(Token): name: str

@dataclass
class Register(Token): value: int

@dataclass
class Immdval(Token): value: int

@dataclass
class LabelSet(Token): name: str

@dataclass
class LabelGet(Token): name: str

@dataclass
class Nextline(Token): pass

@dataclass
class End(Token): pass