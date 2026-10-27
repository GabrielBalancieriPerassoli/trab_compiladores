from __future__ import annotations
from dataclasses import dataclass, field, fields


# ---------- classes base ----------

@dataclass
class No:
    linha: int = field(kw_only=True)

@dataclass
class Cmd(No):
    pass

@dataclass
class Expr(No):
    pass


# ---------- nós do Coda ----------

@dataclass
class Atrib(Cmd):
    variavel: Id
    expressao: Expr

@dataclass  
class Id(No):
    nome: str

@dataclass
class Param(No):
    tipo: str
    nome: str

@dataclass
class Vari(No):
    tipo: str
    nome: str

@dataclass
class Func(No):             
    nome: str
    retorno: str
    parametros: list[Cmd]
    variaveis: list[Param]
    comandos: list[Vari]


# ---------- impressora ----------

def print_ast(no, nivel=0):
    indent = '    ' * nivel

    if isinstance(no, list):
        for item in no:
            print_ast(item, nivel)
        return

    if not isinstance(no, No):
        print(f'{indent}{no!r}')
        return

    print(f'{indent}{type(no).__name__} (linha={no.linha})')

    for campo in fields(no):
        if campo.name == 'linha':
            continue

        valor = getattr(no, campo.name)

        if isinstance(valor, (No, list)):
            print(f'{indent}    {campo.name}:')
            print_ast(valor, nivel + 2)
        else:
            print(f'{indent}    {campo.name}: {valor!r}')