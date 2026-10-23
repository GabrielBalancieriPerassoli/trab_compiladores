import ply.lex as lex

# ---------- LÉXICO ----------

class AnalisadorLexico:

    reservadas = {
        'program': 'PROGRAM',
        'fun': 'FUN',
        'int': 'INT',
        'bool': 'BOOL',
        'void': 'VOID',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'return': 'RETURN',
        'read': 'READ',
        'print': 'PRINT',
        'true': 'TRUE',
        'false': 'FALSE'
    }

    tokens = (
        'ABRE_PAREN', 'FECHA_PAREN',
        'PONTO_VIRGULA', 'ABRE_CHAVE',
        'FECHA_CHAVE', 'VIRGULA',
        'ATRIB', 'SETA',
        'IGUAL', 'DIFERENTE',
        'MENOR', 'MENOR_IGUAL',
        'MAIOR', 'MAIOR_IGUAL',
        'MAIS', 'MENOS',
        'ASTERISCO', 'DIV',
        'AND_LOGICO', 'OR_LOGICO',
        'NOT_LOGICO', 'ID',
        'NUM'
    ) + tuple(reservadas.values())

    t_ABRE_PAREN     = r'\('
    t_FECHA_PAREN    = r'\)'
    t_PONTO_VIRGULA  = r';'
    t_ABRE_CHAVE     = r'\{'
    t_FECHA_CHAVE    = r'\}'
    t_VIRGULA        = r','
    t_ATRIB          = r'='
    t_SETA           = r'->'
    t_IGUAL          = r'=='
    t_DIFERENTE      = r'!='
    t_MENOR          = r'<'
    t_MENOR_IGUAL    = r'<='
    t_MAIOR          = r'>'
    t_MAIOR_IGUAL    = r'>='
    t_MAIS           = r'\+'
    t_MENOS          = r'-'
    t_ASTERISCO      = r'\*'
    t_DIV            = r'/'
    t_AND_LOGICO     = r'&&'
    t_OR_LOGICO      = r'\|\|'
    t_NOT_LOGICO     = r'!'

    t_ignore = ' \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_ID(self, t):
        r'[A-Za-z][A-Za-z0-9_]*'
        t.type = self.reservadas.get(t.value, 'ID')
        return t

    def t_NUM(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_NOVALINHA(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMENTARIO(self, t):
        r'//[^\n]*'
        pass

    def t_error(self, t):
        print(f"ERRO léxico - símbolo ilegal '{t.value[0]}' na linha {t.lineno}")
        t.lexer.skip(1)

    def input(self, data):
        self.lexer.lineno = 1
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()