from __future__ import annotations
import sys
from sintatico import AnalisadorSintatico
from semantico import AnalisadorSemantico
from mepa import GeradorMepa


# ---------- COMPILADOR CODA ----------

def compilar(fonte: str) -> str | None:
    parser = AnalisadorSintatico()
    arvore = parser.parse(fonte)
    if arvore is None:
        print("Programa rejeitado (erro léxico ou sintático)")
        return None

    semantico = AnalisadorSemantico()
    if not semantico.analisar(arvore):
        for linha, mensagem in sorted(semantico.erros):
            print(f"ERRO semântico - {mensagem} na linha {linha}")
        print("Programa rejeitado")
        return None

    gerador = GeradorMepa()
    return gerador.gerar(arvore)


def main():
    if len(sys.argv) < 2:
        print("Uso: python coda.py <programa> [saida.mepa]")
        sys.exit(1)

    caminho_fonte = sys.argv[1]
    try:
        with open(caminho_fonte, encoding='utf-8') as arquivo:
            fonte = arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_fonte}")
        sys.exit(1)

    codigo = compilar(fonte)
    if codigo is None:
        sys.exit(1)

    if len(sys.argv) > 2:
        caminho_saida = sys.argv[2]
        with open(caminho_saida, 'w', encoding='utf-8') as saida:
            saida.write(codigo + '\n')
        print(f"Código MEPA gravado em {caminho_saida}")
    else:
        print(codigo)


if __name__ == '__main__':
    main()
