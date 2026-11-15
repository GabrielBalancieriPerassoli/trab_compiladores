from __future__ import annotations
import arvore_ast as ast
from tabela_simbolos import Simbolo, TabelaSimbolos
from visitador import Visitador


# ---------- SEMÂNTICO ----------

class AnalisadorSemantico(Visitador):

    def __init__(self):
        self.ts = TabelaSimbolos()
        self.erros = []
        self.proximo_endereco = 0
        self.funcao_atual = None
        self.achou_return = False

    def erro(self, linha: int, mensagem: str):
        self.erros.append((linha, mensagem))

    def analisar(self, programa: ast.Programa) -> bool:
        self.__init__()
        self.visita(programa)
        return len(self.erros) == 0

    # ---------- programa ----------

    def visita_Programa(self, no: ast.Programa):
        for declaracao in no.variaveis:
            self.visita(declaracao)
        for funcao in no.funcoes:
            self.visita(funcao)
        for comando in no.comandos:
            self.visita(comando)

    # ---------- declarações ----------

    def visita_Vari(self, no: ast.Vari):
        if self.ts.existe_no_escopo(no.nome):
            self.erro(no.linha, f"variável '{no.nome}' já declarada")
            return

        simbolo = Simbolo(nome=no.nome, categoria='var', tipo=no.tipo,
                          nivel=self.ts.nivel, endereco=self.proximo_endereco)
        self.proximo_endereco += 1

        no.simbolo = simbolo
        self.ts.instala(simbolo)

    def visita_Param(self, no: ast.Param):
        if self.ts.existe_no_escopo(no.nome):
            self.erro(no.linha, f"parâmetro '{no.nome}' já declarado")
            return

        simbolo = Simbolo(nome=no.nome, categoria='param', tipo=no.tipo,
                          nivel=self.ts.nivel, endereco=self.proximo_endereco)
        self.proximo_endereco += 1

        no.simbolo = simbolo
        self.ts.instala(simbolo)

    def visita_Func(self, no: ast.Func):
        if self.ts.existe_no_escopo(no.nome):
            self.erro(no.linha, f"função '{no.nome}' já declarada")
            return

        tipos_parametros = [p.tipo for p in no.parametros]

        simbolo = Simbolo(nome=no.nome, categoria='fun', tipo=no.retorno,
                          nivel=0, parametros=tipos_parametros)
        no.simbolo = simbolo
        self.ts.instala(simbolo)

        self.ts.entrar_escopo()
        self.proximo_endereco = 0
        self.funcao_atual = simbolo
        self.achou_return = False

        for parametro in no.parametros:
            self.visita(parametro)
        for variavel in no.variaveis:
            self.visita(variavel)
        for comando in no.comandos:
            self.visita(comando)

        if no.retorno != 'void' and not self.achou_return:
            self.erro(no.linha, f"função '{no.nome}' precisa de return")
        self.funcao_atual = None

        self.ts.sair_escopo()

    # ---------- comandos ----------

    def visita_Atrib(self, no: ast.Atrib):
        tipo_expr = self.visita(no.expressao)
        tipo_var = self.visita(no.variavel)

        if tipo_expr != 'erro' and tipo_var != 'erro' and tipo_expr != tipo_var:
            self.erro(no.linha, f"atribuição de {tipo_expr} a variável {tipo_var}")

    def visita_If(self, no: ast.If):
        tipo = self.visita(no.condicao)
        if tipo != 'erro' and tipo != 'bool':
            self.erro(no.linha, "condição do if deve ser bool")

        for comando in no.entao:
            self.visita(comando)
        for comando in no.senao:
            self.visita(comando)

    def visita_While(self, no: ast.While):
        tipo = self.visita(no.condicao)
        if tipo != 'erro' and tipo != 'bool':
            self.erro(no.linha, "condição do while deve ser bool")

        for comando in no.corpo:
            self.visita(comando)

    def visita_Return(self, no: ast.Return):
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

    def visita_Read(self, no: ast.Read):
        for variavel in no.leitura:
            self.visita(variavel)

    def visita_Print(self, no: ast.Print):
        for expressao in no.escrita:
            self.visita(expressao)

    def visita_ChamadaCmd(self, no: ast.ChamadaCmd):
        self.confere_chamada(no.chamada)

    # ---------- expressões (retornam o tipo: 'int', 'bool' ou 'erro') ----------

    def visita_Numero(self, no: ast.Numero) -> str:
        return 'int'

    def visita_Booleano(self, no: ast.Booleano) -> str:
        return 'bool'

    def visita_Id(self, no: ast.Id) -> str:
        simbolo = self.ts.busca(no.nome)
        if simbolo is None:
            self.erro(no.linha, f"variável '{no.nome}' não declarada")
            return 'erro'

        if simbolo.categoria == 'fun':
            self.erro(no.linha, f"'{no.nome}' é uma função, não uma variável")
            return 'erro'

        no.simbolo = simbolo
        return simbolo.tipo

    def visita_Binaria(self, no: ast.Binaria) -> str:
        esq = self.visita(no.esquerda)
        dire = self.visita(no.direita)

        if esq == 'erro' or dire == 'erro':
            return 'erro'

        if no.operador in ('+', '-', '*', '/'):
            if esq == 'int' and dire == 'int':
                return 'int'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos int")
            return 'erro'

        if no.operador in ('<', '<=', '>', '>='):
            if esq == 'int' and dire == 'int':
                return 'bool'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos int")
            return 'erro'

        if no.operador in ('==', '!='):
            if esq == dire:
                return 'bool'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos do mesmo tipo")
            return 'erro'

        if no.operador in ('&&', '||'):
            if esq == 'bool' and dire == 'bool':
                return 'bool'
            self.erro(no.linha, f"operador '{no.operador}' exige operandos bool")
            return 'erro'

    def visita_Unaria(self, no: ast.Unaria) -> str:
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

    def visita_Chamada(self, no: ast.Chamada) -> str:
        tipo = self.confere_chamada(no)
        if tipo == 'void':
            self.erro(no.linha, f"função void '{no.nome}' usada em expressão")
            return 'erro'
        return tipo

    # ---------- chamadas ----------

    def confere_chamada(self, no: ast.Chamada) -> str:
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