from arvore_ast import *

conta = Atrib(
    variavel=Id(nome='x', linha=1),
    expressao=Binaria(
        operador='-',
        esquerda=Id(nome='a', linha=1),
        direita=Binaria(operador='*', esquerda=Numero(valor=2, linha=1),
                        direita=Id(nome='b', linha=1), linha=1),
        linha=1,
    ),
    linha=1,
)
print_ast(conta)