import sys
from sintatico import AnalisadorSintatico
from semantico import AnalisadorSemantico
from mepa import GeradorMepa

caminho = sys.argv[1]
with open(caminho, encoding='utf-8') as arquivo:
    data = arquivo.read()

parser = AnalisadorSintatico()
arvore = parser.parse(data)

if arvore is None:
    print("Programa rejeitado (erro léxico ou sintático)")
    sys.exit(1)

semantico = AnalisadorSemantico()
if not semantico.analisar(arvore):
    for linha, mensagem in sorted(semantico.erros):
        print(f"ERRO semântico - {mensagem} na linha {linha}")
    print("Programa rejeitado")
    sys.exit(1)

gerador = GeradorMepa()
codigo = gerador.gerar(arvore)

if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', encoding='utf-8') as saida:
        saida.write(codigo + '\n')
else:
    print(codigo)