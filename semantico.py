from arvore_ast import *
from tabela_simbolos import *


# ---------- SEMÂNTICO ----------

class AnalisadorSemantico:

    def __init__(self):
        self.erros = []
        self.ts = TabelaSimbolos()
        self.proximo_endereco = 0

    # ---------- mensagens de erro ----------

    def erro(self, linha, mensagem):
        self.erros.append(f"ERRO semântico - {mensagem} na linha {linha}")

    # ---------- visitador (igual ao slide 13) ----------

    def visita(self, no):
        if no is None:
            return
        nome_metodo = f'visita_{type(no).__name__}'
        visitor = getattr(self, nome_metodo, self.visita_padrao)
        return visitor(no)

    def visita_padrao(self, no):
        raise NotImplementedError(f"Visita não implementada: {type(no).__name__}")

    # ---------- programa ----------

    def visita_Programa(self, no):
        for declaracao in no.variaveis:
            self.visita(declaracao)
        for funcao in no.funcoes:
            self.visita(funcao)
        for comando in no.comandos:
            self.visita(comando)

    # ---------- declarações ----------

    def visita_Vari(self, no):
        if self.ts.existe_no_escopo(no.nome):
            self.erro(no.linha, f"variável '{no.nome}' já declarada")
            return

        simbolo = Simbolo(nome=no.nome, categoria='var', tipo=no.tipo,
                          nivel=self.ts.nivel, endereco=self.proximo_endereco)
        self.proximo_endereco += 1

        no.simbolo = simbolo
        self.ts.instala(simbolo)

    # ---------- comandos ----------

    def visita_Atrib(self, no):
        tipo_expr = self.visita(no.expressao)
        tipo_var = self.visita(no.variavel)

        if tipo_expr != 'erro' and tipo_var != 'erro' and tipo_expr != tipo_var:
            self.erro(no.linha, f"atribuição de {tipo_expr} a variável {tipo_var}")

    def visita_If(self, no):
        tipo = self.visita(no.condicao)
        if tipo != 'erro' and tipo != 'bool':
            self.erro(no.linha, "condição do if deve ser bool")

        for comando in no.entao:
            self.visita(comando)
        for comando in no.senao:
            self.visita(comando)

    def visita_While(self, no):
        tipo = self.visita(no.condicao)
        if tipo != 'erro' and tipo != 'bool':
            self.erro(no.linha, "condição do while deve ser bool")

        for comando in no.corpo:
            self.visita(comando)

    def visita_Read(self, no):
        for variavel in no.leitura:
            self.visita(variavel)

    def visita_Print(self, no):
        for expressao in no.escrita:
            self.visita(expressao)

    # ---------- expressões ----------

    def visita_Numero(self, no):
        return 'int'

    def visita_Id(self, no):
        simbolo = self.ts.busca(no.nome)
        if simbolo is None:
            self.erro(no.linha, f"variável '{no.nome}' não declarada")
            return 'erro'
        no.simbolo = simbolo
        return simbolo.tipo

    def visita_Binaria(self, no):
        esq = self.visita(no.esquerda)
        dir = self.visita(no.direita)

        if esq == 'erro' or dir == 'erro':
            return 'erro'

        if no.operador in ('+', '-', '*', '/'):
            if esq == 'int' and dir == 'int':
                return 'int'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos int")
            return 'erro'

        if no.operador in ('<', '<=', '>', '>='):
            if esq == 'int' and dir == 'int':
                return 'bool'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos int")
            return 'erro'

        if no.operador in ('==', '!='):
            if esq == dir:
                return 'bool'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos do mesmo tipo")
            return 'erro'

        if no.operador in ('&&', "||"):
            if esq == 'bool' and dir == 'bool':
                return 'bool'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos bool")
            return 'erro'

    def visita_Unaria(self, no):
        tipo = self.visita(no.expressao)

        if tipo == 'erro':
            return 'erro'

        if no.operador == '-':
            if tipo == 'int':
                return 'int'
            self.erro(no.linha, "operador '-' exige operando int")
            return 'erro'

        if no.operador == '!':
            if tipo == 'bool':
                return 'bool'
            self.erro(no.linha, "operador '!' exige operando bool")
            return 'erro'

    def visita_Booleano(self, no):
        return 'bool'

    # ---------- ponto de entrada ----------

    def analisar(self, arvore):
        self.visita(arvore)
        return self.erros