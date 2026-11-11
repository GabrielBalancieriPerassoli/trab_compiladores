import sys
from sintatico import AnalisadorSintatico
from semantico import AnalisadorSemantico
from gerador_mepa import GeradorMepa

caminho = sys.argv[1]
with open(caminho, encoding='utf-8') as arquivo:
    data = arquivo.read()

parser = AnalisadorSintatico()
arvore = parser.parse(data)

if arvore is None:
    print("Programa rejeitado (erro léxico ou sintático)")
    sys.exit(1)

semantico = AnalisadorSemantico()
erros = semantico.analisar(arvore)
if erros:
    for mensagem in erros:
        print(mensagem)
    print("Programa rejeitado")
    sys.exit(1)

gerador = GeradorMepa()
print(gerador.gerar(arvore))
