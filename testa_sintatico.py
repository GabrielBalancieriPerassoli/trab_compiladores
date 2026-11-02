import sys
from sintatico import AnalisadorSintatico
from arvore_ast import print_ast

caminho = sys.argv[1]
with open(caminho, encoding='utf-8') as arquivo:
    data = arquivo.read()

parser = AnalisadorSintatico()
arvore = parser.parse(data)

if arvore is not None:
    print("Programa aceito")
    print_ast(arvore)
else:
    print("Programa rejeitado")