import sys
from sintatico import AnalisadorSintatico

caminho = sys.argv[1]
with open(caminho, encoding='utf-8') as arquivo:
    data = arquivo.read()

parser = AnalisadorSintatico()
if parser.parse(data):
    print("Programa aceito")
else:
    print("Programa rejeitado")
