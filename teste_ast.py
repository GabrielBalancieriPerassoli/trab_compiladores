from arvore_ast import *
print(isinstance(If(condicao=Id(nome='ok', linha=1), entao=[], senao=[], linha=1), Cmd))