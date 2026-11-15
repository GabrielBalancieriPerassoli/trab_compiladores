from __future__ import annotations
from dataclasses import dataclass, field, fields
from tabela_simbolos import Simbolo


# ---------- classes base ----------

@dataclass
class No:
    linha: int = field(kw_only=True)

@dataclass
class Cmd(No):
    pass

@dataclass
class Expr(No):
    tipo: str | None = field(default=None, kw_only=True)


# ---------- nós do Coda: declarações ----------

@dataclass
class Programa(No):
    nome: str
    variaveis: list[Vari]
    funcoes: list[Func]
    comandos: list[Cmd]

@dataclass
class Vari(No):
    tipo: str
    nome: str
    simbolo: Simbolo | None = None

@dataclass
class Param(No):
    tipo: str
    nome: str
    simbolo: Simbolo | None = None

@dataclass
class Func(No):
    nome: str
    retorno: str
    parametros: list[Param]
    variaveis: list[Vari]
    comandos: list[Cmd]
    simbolo: Simbolo | None = None


# ---------- nós do Coda: comandos ----------

@dataclass
class Atrib(Cmd):
    variavel: Id
    expressao: Expr

@dataclass
class If(Cmd):
    condicao: Expr
    entao: list[Cmd]
    senao: list[Cmd]

@dataclass
class While(Cmd):
    condicao: Expr
    corpo: list[Cmd]

@dataclass
class Return(Cmd):
    expressao: Expr

@dataclass
class Read(Cmd):
    leitura: list[Id]

@dataclass
class Print(Cmd):
    escrita: list[Expr]

@dataclass
class ChamadaCmd(Cmd):
    chamada: Chamada


# ---------- nós do Coda: expressões ----------

@dataclass
class Id(Expr):
    nome: str
    simbolo: Simbolo | None = None

@dataclass
class Chamada(Expr):
    nome: str
    argumentos: list[Expr]
    simbolo: Simbolo | None = None

@dataclass
class Binaria(Expr):
    operador: str
    esquerda: Expr
    direita: Expr

@dataclass
class Unaria(Expr):
    operador: str
    expressao: Expr

@dataclass
class Numero(Expr):
    valor: int

@dataclass
class Booleano(Expr):
    valor: bool


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