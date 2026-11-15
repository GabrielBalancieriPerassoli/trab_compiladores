import sys
from sintatico import AnalisadorSintatico
from semantico import AnalisadorSemantico

caminho = sys.argv[1]
with open(caminho, encoding='utf-8') as arquivo:
    data = arquivo.read()

parser = AnalisadorSintatico()
arvore = parser.parse(data)

if arvore is None:
    print("Programa rejeitado (erro léxico ou sintático)")
else:
    semantico = AnalisadorSemantico()
    if semantico.analisar(arvore):
        print("Programa aceito")
    else:
        for linha, mensagem in sorted(semantico.erros):
            print(f"ERRO semântico - {mensagem} na linha {linha}")
        print("Programa rejeitado")

    for simbolo in semantico.ts.escopos[0].values():
        print(simbolo)