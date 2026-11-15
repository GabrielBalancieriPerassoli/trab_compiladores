from __future__ import annotations
import arvore_ast as ast
from tabela_simbolos import Simbolo
from visitador import Visitador


# ---------- GERADOR MEPA ----------

class GeradorMepa(Visitador):

    operadores = {
        '+': 'SOMA', '-': 'SUBT', '*': 'MULT', '/': 'DIVI',
        '<': 'CMME', '<=': 'CMEG', '>': 'CMMA', '>=': 'CMAG',
        '==': 'CMIG', '!=': 'CMDG', '&&': 'CONJ', '||': 'DISJ',
    }

    def __init__(self):
        self.codigo = []
        self.contador_rotulos = 0
        self.nivel_atual = 0
        self.funcao_atual = None

    def gerar(self, programa: ast.Programa) -> str:
        self.__init__()
        self.visita(programa)
        return '\n'.join(self.codigo)

    def gere(self, instrucao: str):
        self.codigo.append(instrucao)

    def novo_rotulo(self) -> str:
        rotulo = f'R{self.contador_rotulos:02d}'
        self.contador_rotulos += 1
        return rotulo

    def deslocamento(self, s: Simbolo) -> int:
        if s.nivel == 0:
            return s.endereco
        n = len(self.funcao_atual.parametros)
        if s.categoria == 'param':
            return s.endereco - (n + 4)
        return s.endereco - n

    def deslocamento_retorno(self) -> int:
        n = len(self.funcao_atual.parametros)
        return -(n + 5)

    # ---------- programa ----------

    def visita_Programa(self, no: ast.Programa):
        self.gere('INPP')
        if no.variaveis:
            self.gere(f'AMEM {len(no.variaveis)}')

        if no.funcoes:
            rotulo_principal = self.novo_rotulo()
            for funcao in no.funcoes:
                funcao.simbolo.rotulo_entrada = self.novo_rotulo()
                funcao.simbolo.rotulo_saida = self.novo_rotulo()

            self.gere(f'DSVS {rotulo_principal}')
            for funcao in no.funcoes:
                self.visita(funcao)
            self.gere(f'{rotulo_principal}: NADA')

        for comando in no.comandos:
            self.visita(comando)

        if no.variaveis:
            self.gere(f'DMEM {len(no.variaveis)}')
        self.gere('PARA')
        self.gere('FIM')

    # ---------- declarações ----------

    def visita_Func(self, no: ast.Func):
        s = no.simbolo
        nivel_anterior = self.nivel_atual
        funcao_anterior = self.funcao_atual
        self.nivel_atual = s.nivel + 1
        self.funcao_atual = s

        self.gere(f'{s.rotulo_entrada}: NADA')
        self.gere(f'ENPR {self.nivel_atual}')
        if no.variaveis:
            self.gere(f'AMEM {len(no.variaveis)}')

        for comando in no.comandos:
            self.visita(comando)

        self.gere(f'{s.rotulo_saida}: NADA')
        if no.variaveis:
            self.gere(f'DMEM {len(no.variaveis)}')
        self.gere(f'RTPR {len(s.parametros)}')

        self.nivel_atual = nivel_anterior
        self.funcao_atual = funcao_anterior

    # ---------- comandos ----------

    def visita_Atrib(self, no: ast.Atrib):
        s = no.variavel.simbolo
        self.visita(no.expressao)
        self.gere(f'ARMZ {s.nivel},{self.deslocamento(s)}')

    def visita_If(self, no: ast.If):
        rotulo_fim = self.novo_rotulo()
        self.visita(no.condicao)

        if no.senao:
            rotulo_senao = self.novo_rotulo()
            self.gere(f'DSVF {rotulo_senao}')
            for comando in no.entao:
                self.visita(comando)
            self.gere(f'DSVS {rotulo_fim}')
            self.gere(f'{rotulo_senao}: NADA')
            for comando in no.senao:
                self.visita(comando)
        else:
            self.gere(f'DSVF {rotulo_fim}')
            for comando in no.entao:
                self.visita(comando)

        self.gere(f'{rotulo_fim}: NADA')

    def visita_While(self, no: ast.While):
        rotulo_inicio = self.novo_rotulo()
        rotulo_fim = self.novo_rotulo()

        self.gere(f'{rotulo_inicio}: NADA')
        self.visita(no.condicao)
        self.gere(f'DSVF {rotulo_fim}')
        for comando in no.corpo:
            self.visita(comando)
        self.gere(f'DSVS {rotulo_inicio}')
        self.gere(f'{rotulo_fim}: NADA')

    def visita_Return(self, no: ast.Return):
        s = self.funcao_atual
        self.visita(no.expressao)
        self.gere(f'ARMZ {self.nivel_atual},{self.deslocamento_retorno()}')
        self.gere(f'DSVS {s.rotulo_saida}')

    def visita_Read(self, no: ast.Read):
        for variavel in no.leitura:
            s = variavel.simbolo
            self.gere('LEIT')
            self.gere(f'ARMZ {s.nivel},{self.deslocamento(s)}')

    def visita_Print(self, no: ast.Print):
        for expressao in no.escrita:
            self.visita(expressao)
            self.gere('IMPR')

    def visita_ChamadaCmd(self, no: ast.ChamadaCmd):
        self.visita(no.chamada)
        if no.chamada.simbolo.tipo != 'void':
            self.gere('DMEM 1')

    # ---------- expressões ----------

    def visita_Numero(self, no: ast.Numero):
        self.gere(f'CRCT {no.valor}')

    def visita_Booleano(self, no: ast.Booleano):
        self.gere(f'CRCT {1 if no.valor else 0}')

    def visita_Id(self, no: ast.Id):
        s = no.simbolo
        self.gere(f'CRVL {s.nivel},{self.deslocamento(s)}')

    def visita_Binaria(self, no: ast.Binaria):
        self.visita(no.esquerda)
        self.visita(no.direita)
        self.gere(self.operadores[no.operador])

    def visita_Unaria(self, no: ast.Unaria):
        self.visita(no.expressao)
        if no.operador == '-':
            self.gere('INVR')
        else:
            self.gere('NEGA')

    def visita_Chamada(self, no: ast.Chamada):
        s = no.simbolo
        if s.tipo != 'void':
            self.gere('AMEM 1')
        for argumento in no.argumentos:
            self.visita(argumento)
        self.gere(f'CHPR {s.rotulo_entrada},{self.nivel_atual}')