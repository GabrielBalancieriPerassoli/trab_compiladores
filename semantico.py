from arvore_ast import *
from tabela_simbolos import *


# ---------- SEMÂNTICO ----------

class AnalisadorSemantico:

    def __init__(self):
        self.erros = []
        self.ts = TabelaSimbolos()
        self.proximo_endereco = 0
        self.funcao_atual = None
        self.achou_return = False

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

    def visita_ChamadaCmd(self, no):
        self.confere_chamada(no.chamada)

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

    def visita_Func(self, no):
        if self.ts.existe_no_escopo(no.nome):
            self.erro(no.linha, f"função '{no.nome}' já declarada")
            return

        tipos_parametros = [p.tipo for p in no.parametros]

        simbolo = Simbolo(nome=no.nome, categoria='fun', tipo=no.retorno,
                          nivel=0, parametros=tipos_parametros)
        no.simbolo = simbolo
        self.ts.instala(simbolo)

        self.ts.entra_funcao()
        self.proximo_endereco = 0
        self.funcao_atual = simbolo  
        self.achou_return = False

        for parametro in no.parametros:
            self.visita(parametro)
        for variavel in no.variaveis:
            self.visita(variavel)
        for comando in no.comandos:
            self.visita(comando)

        if no.retorno != 'void' and not self.achou_return:      # NOVO: faltou o return?
            self.erro(no.linha, f"função '{no.nome}' precisa de return")
        self.funcao_atual = None                                 # NOVO: "saí da função"

        self.ts.sai_funcao()

    def visita_Param(self, no):
        if self.ts.existe_no_escopo(no.nome):
            self.erro(no.linha, f"parâmetro '{no.nome}' já declarado")
            return

        simbolo = Simbolo(nome=no.nome, categoria='param', tipo=no.tipo,
                          nivel=self.ts.nivel, endereco=self.proximo_endereco)
        self.proximo_endereco += 1

        no.simbolo = simbolo
        self.ts.instala(simbolo)

    def visita_Return(self, no):
        tipo = self.visita(no.expressao)

        if self.funcao_atual is None:
            self.erro(no.linha, "return fora de função")
            return

        if self.funcao_atual.tipo == 'void':
            self.erro(no.linha, f"função void '{self.funcao_atual.nome}' não pode ter return")
            return

        self.achou_return = True
        if tipo != 'erro' and tipo != self.funcao_atual.tipo:
            self.erro(no.linha, f"return de {tipo} em função {self.funcao_atual.tipo}")

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

        if simbolo.categoria == 'fun':
            self.erro(no.linha, f"'{no.nome}' é uma função, não uma variável")
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

    def visita_Chamada(self, no):
        tipo = self.confere_chamada(no)
        if tipo == 'void':
            self.erro(no.linha, f"função void '{no.nome}' usada em expressão")
            return 'erro'
        return tipo

    # ---------- chamadas ----------
    def confere_chamada(self, no):
        tipos_args = [self.visita(arg) for arg in no.argumentos]

        simbolo = self.ts.busca(no.nome)
        if simbolo is None:
            self.erro(no.linha, f"função '{no.nome}' não declarada")
            return 'erro'

        if simbolo.categoria != 'fun':
            self.erro(no.linha, f"'{no.nome}' não é uma função")
            return 'erro'

        no.simbolo = simbolo

        if len(tipos_args) != len(simbolo.parametros):
            self.erro(no.linha, f"função '{no.nome}' espera {len(simbolo.parametros)} argumento(s)")
            return simbolo.tipo

        for i in range(len(tipos_args)):
            if tipos_args[i] != 'erro' and tipos_args[i] != simbolo.parametros[i]:
                self.erro(no.linha, f"argumento {i + 1} de '{no.nome}' deve ser {simbolo.parametros[i]}")

        return simbolo.tipo

    # ---------- ponto de entrada ----------

    def analisar(self, arvore):
        self.visita(arvore)
        return self.erros