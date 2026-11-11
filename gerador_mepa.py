from arvore_ast import *


# ---------- GERADOR MEPA ----------

class GeradorMepa:

    operadores = {
        '+': 'SOMA', '-': 'SUBT', '*': 'MULT', '/': 'DIVI',
        '<': 'CMME', '<=': 'CMEG', '>': 'CMMA', '>=': 'CMAG',
        '==': 'CMIG', '!=': 'CMDG', '&&': 'CONJ', '||': 'DISJ',
    }

    def __init__(self):
        self.codigo = []

    # ---------- saída ----------

    def emite(self, instrucao, *argumentos, rotulo=None):
        texto = instrucao
        if argumentos:
            texto += ' ' + ','.join(str(a) for a in argumentos)
        if rotulo is not None:
            self.codigo.append(f'{rotulo}: {texto}')
        else:
            self.codigo.append(f'    {texto}')

    # ---------- endereços ----------

    def endereco(self, simbolo):
        return simbolo.nivel, simbolo.endereco

    # ---------- visitador ----------

    def visita(self, no):
        nome_metodo = f'visita_{type(no).__name__}'
        visitor = getattr(self, nome_metodo, self.visita_padrao)
        return visitor(no)

    def visita_padrao(self, no):
        raise NotImplementedError(f"Geração não implementada: {type(no).__name__}")

    # ---------- programa ----------

    def visita_Programa(self, no):
        self.emite('INPP')
        if no.variaveis:
            self.emite('AMEM', len(no.variaveis))
        for comando in no.comandos:
            self.visita(comando)
        if no.variaveis:
            self.emite('DMEM', len(no.variaveis))
        self.emite('PARA')

    # ---------- comandos ----------

    def visita_Atrib(self, no):
        self.visita(no.expressao)
        self.emite('ARMZ', *self.endereco(no.variavel.simbolo))

    def visita_Read(self, no):
        for variavel in no.leitura:
            self.emite('LEIT')
            self.emite('ARMZ', *self.endereco(variavel.simbolo))

    def visita_Print(self, no):
        for expressao in no.escrita:
            self.visita(expressao)
            self.emite('IMPR')

    # ---------- expressões ----------

    def visita_Numero(self, no):
        self.emite('CRCT', no.valor)

    def visita_Booleano(self, no):
        self.emite('CRCT', 1 if no.valor else 0)

    def visita_Id(self, no):
        self.emite('CRVL', *self.endereco(no.simbolo))

    def visita_Binaria(self, no):
        self.visita(no.esquerda)
        self.visita(no.direita)
        self.emite(self.operadores[no.operador])

    def visita_Unaria(self, no):
        self.visita(no.expressao)
        self.emite('INVR' if no.operador == '-' else 'NEGA')

    # ---------- ponto de entrada ----------

    def gerar(self, arvore):
        self.codigo = []
        self.visita(arvore)
        return '\n'.join(self.codigo)
