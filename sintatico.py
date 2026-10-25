import ply.yacc as yacc
from lexico import AnalisadorLexico

# ---------- SINTÁTICO (reconhecedor) ----------

class AnalisadorSintatico:

    tokens = AnalisadorLexico.tokens

    start = 'programa'

    # da menor para a maior precedência
    precedence = (
        ('left', 'OR_LOGICO'),
        ('left', 'AND_LOGICO'),
        ('nonassoc', 'IGUAL', 'DIFERENTE'),
        ('nonassoc', 'MENOR', 'MENOR_IGUAL', 'MAIOR', 'MAIOR_IGUAL'),
        ('left', 'MAIS', 'MENOS'),
        ('left', 'ASTERISCO', 'DIV'),
        ('right', 'MENOS_UNARIO', 'NOT_LOGICO'),
    )

    def __init__(self):
        self.lexico = AnalisadorLexico()
        self.parser = yacc.yacc(module=self, debug=True, write_tables=False)
        self.erro = False

    # ---------- programa ----------

    def p_programa(self, p):
        'programa : PROGRAM ID ABRE_CHAVE declaracoes_variaveis declaracoes_funcoes comandos FECHA_CHAVE'
        pass

    # ---------- declarações de variáveis ----------

    def p_declaracoes_variaveis(self, p):
        '''declaracoes_variaveis : declaracoes_variaveis declaracao_variavel
                                 | vazio'''
        pass

    def p_declaracao_variavel(self, p):
        'declaracao_variavel : tipo ID PONTO_VIRGULA'
        pass

    def p_tipo(self, p):
        '''tipo : INT
                | BOOL'''
        pass

    # ---------- declarações de funções ----------

    def p_declaracoes_funcoes(self, p):
        '''declaracoes_funcoes : declaracoes_funcoes declaracao_funcao
                               | vazio'''
        pass

    def p_declaracao_funcao(self, p):
        'declaracao_funcao : FUN ID ABRE_PAREN parametros FECHA_PAREN SETA tipo_retorno ABRE_CHAVE declaracoes_variaveis comandos FECHA_CHAVE'
        pass

    def p_parametros(self, p):
        '''parametros : lista_parametros
                      | vazio'''
        pass

    def p_lista_parametros(self, p):
        '''lista_parametros : lista_parametros VIRGULA parametro
                            | parametro'''
        pass

    def p_parametro(self, p):
        'parametro : tipo ID'
        pass

    def p_tipo_retorno(self, p):
        '''tipo_retorno : INT
                        | BOOL
                        | VOID'''
        pass

    # ---------- comandos ----------

    def p_comandos(self, p):
        '''comandos : comandos comando
                    | vazio'''
        pass

    def p_comando(self, p):
        '''comando : atribuicao
                   | condicional
                   | repeticao
                   | retorno
                   | leitura
                   | escrita
                   | chamada_comando'''
        pass

    def p_atribuicao(self, p):
        'atribuicao : ID ATRIB expressao PONTO_VIRGULA'
        pass

    def p_condicional(self, p):
        '''condicional : IF ABRE_PAREN expressao FECHA_PAREN bloco
                       | IF ABRE_PAREN expressao FECHA_PAREN bloco ELSE bloco'''
        pass

    def p_repeticao(self, p):
        'repeticao : WHILE ABRE_PAREN expressao FECHA_PAREN bloco'
        pass

    def p_bloco(self, p):
        'bloco : ABRE_CHAVE comandos FECHA_CHAVE'
        pass

    def p_retorno(self, p):
        'retorno : RETURN expressao PONTO_VIRGULA'
        pass

    def p_leitura(self, p):
        'leitura : READ ABRE_PAREN lista_identificadores FECHA_PAREN PONTO_VIRGULA'
        pass

    def p_lista_identificadores(self, p):
        '''lista_identificadores : lista_identificadores VIRGULA ID
                                 | ID'''
        pass

    def p_escrita(self, p):
        'escrita : PRINT ABRE_PAREN lista_expressoes FECHA_PAREN PONTO_VIRGULA'
        pass

    def p_lista_expressoes(self, p):
        '''lista_expressoes : lista_expressoes VIRGULA expressao
                            | expressao'''
        pass

    def p_chamada_comando(self, p):
        'chamada_comando : chamada PONTO_VIRGULA'
        pass

    def p_chamada(self, p):
        'chamada : ID ABRE_PAREN argumentos FECHA_PAREN'
        pass

    def p_argumentos(self, p):
        '''argumentos : lista_expressoes
                      | vazio'''
        pass

    # ---------- expressões ----------

    def p_expressao_binaria(self, p):
        '''expressao : expressao OR_LOGICO expressao
                     | expressao AND_LOGICO expressao
                     | expressao IGUAL expressao
                     | expressao DIFERENTE expressao
                     | expressao MENOR expressao
                     | expressao MENOR_IGUAL expressao
                     | expressao MAIOR expressao
                     | expressao MAIOR_IGUAL expressao
                     | expressao MAIS expressao
                     | expressao MENOS expressao
                     | expressao ASTERISCO expressao
                     | expressao DIV expressao'''
        pass

    def p_expressao_menos_unario(self, p):
        'expressao : MENOS expressao %prec MENOS_UNARIO'
        pass

    def p_expressao_not(self, p):
        'expressao : NOT_LOGICO expressao'
        pass

    def p_expressao_numero(self, p):
        'expressao : NUM'
        pass

    def p_expressao_booleano(self, p):
        '''expressao : TRUE
                     | FALSE'''
        pass

    def p_expressao_identificador(self, p):
        'expressao : ID'
        pass

    def p_expressao_chamada(self, p):
        'expressao : chamada'
        pass

    def p_expressao_parenteses(self, p):
        'expressao : ABRE_PAREN expressao FECHA_PAREN'
        pass

    # ---------- auxiliares ----------

    def p_vazio(self, p):
        'vazio :'
        pass

    def p_error(self, p):
        self.erro = True
        if p is None:
            print("ERRO sintático - fim de arquivo inesperado")
        else:
            print(f"ERRO sintático - token inesperado '{p.value}' na linha {p.lineno}")

    def parse(self, data):
        self.erro = False
        self.lexico.input(data)
        self.parser.parse(lexer=self.lexico)
        return not self.erro
