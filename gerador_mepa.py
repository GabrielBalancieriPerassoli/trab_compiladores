from arvore_ast import *


# ---------- GERADOR MEPA ----------

class GeradorMepa:

    operadores = {
        '+': 'SOMA', '-': 'SUBT', '*': 'MULT', '/': 'DIVI',
        '<': 'CMME', '<=': 'CMEG', '>': 'CMMA', '>=': 'CMAG',
        '==': 'CMIG', '!=': 'CMDG', '&&': 'CONJ', '||': 'DISJ',
    }

    # variante CHPR p,k: endereço de retorno, k e D[k] salvo ficam entre os parâmetros e as locais
    tamanho_controle = 3

    def __init__(self):
        self.codigo = []
        self.contador_rotulos = 0
        self.nivel = 0
        self.rotulos_funcoes = {}
        self.num_parametros = 0
        self.rotulo_fim_funcao = None

    # ---------- saída ----------

    def novo_rotulo(self):
        self.contador_rotulos += 1
        return f'L{self.contador_rotulos}'

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
        if simbolo.nivel == 0:
            return 0, simbolo.endereco
        if simbolo.categoria == 'param':
            return 1, simbolo.endereco - (self.num_parametros + self.tamanho_controle)
        return 1, simbolo.endereco - self.num_parametros

    def endereco_resultado(self):
        return 1, -(self.num_parametros + self.tamanho_controle + 1)

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

        if no.funcoes:
            rotulo_principal = self.novo_rotulo()
            for funcao in no.funcoes:
                self.rotulos_funcoes[funcao.nome] = self.novo_rotulo()
            self.emite('DSVS', rotulo_principal)
            for funcao in no.funcoes:
                self.visita(funcao)
            self.emite('NADA', rotulo=rotulo_principal)

        for comando in no.comandos:
            self.visita(comando)
        if no.variaveis:
            self.emite('DMEM', len(no.variaveis))
        self.emite('PARA')

    # ---------- funções ----------

    def visita_Func(self, no):
        self.nivel = 1
        self.num_parametros = len(no.parametros)
        self.rotulo_fim_funcao = self.novo_rotulo()

        self.emite('ENPR', 1, rotulo=self.rotulos_funcoes[no.nome])
        if no.variaveis:
            self.emite('AMEM', len(no.variaveis))
        for comando in no.comandos:
            self.visita(comando)
        self.emite('NADA', rotulo=self.rotulo_fim_funcao)
        if no.variaveis:
            self.emite('DMEM', len(no.variaveis))
        self.emite('RTPR', 1, self.num_parametros)

        self.nivel = 0
        self.num_parametros = 0
        self.rotulo_fim_funcao = None

    def visita_Return(self, no):
        self.visita(no.expressao)
        self.emite('ARMZ', *self.endereco_resultado())
        self.emite('DSVS', self.rotulo_fim_funcao)

    def chama(self, no):
        if no.simbolo.tipo != 'void':
            self.emite('AMEM', 1)
        for argumento in no.argumentos:
            self.visita(argumento)
        self.emite('CHPR', self.rotulos_funcoes[no.nome], self.nivel)

    # ---------- comandos ----------

    def visita_ChamadaCmd(self, no):
        self.chama(no.chamada)
        if no.chamada.simbolo.tipo != 'void':
            self.emite('DMEM', 1)

    def visita_Atrib(self, no):
        self.visita(no.expressao)
        self.emite('ARMZ', *self.endereco(no.variavel.simbolo))

    def visita_If(self, no):
        rotulo_senao = self.novo_rotulo()
        rotulo_fim = self.novo_rotulo()

        self.visita(no.condicao)
        self.emite('DSVF', rotulo_senao)
        for comando in no.entao:
            self.visita(comando)
        self.emite('DSVS', rotulo_fim)
        self.emite('NADA', rotulo=rotulo_senao)
        for comando in no.senao:
            self.visita(comando)
        self.emite('NADA', rotulo=rotulo_fim)

    def visita_While(self, no):
        rotulo_inicio = self.novo_rotulo()
        rotulo_fim = self.novo_rotulo()

        self.emite('NADA', rotulo=rotulo_inicio)
        self.visita(no.condicao)
        self.emite('DSVF', rotulo_fim)
        for comando in no.corpo:
            self.visita(comando)
        self.emite('DSVS', rotulo_inicio)
        self.emite('NADA', rotulo=rotulo_fim)

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

    def visita_Chamada(self, no):
        self.chama(no)

    # ---------- ponto de entrada ----------

    def gerar(self, arvore):
        self.codigo = []
        self.contador_rotulos = 0
        self.rotulos_funcoes = {}
        self.visita(arvore)
        return '\n'.join(self.codigo)
