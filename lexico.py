import ply.lex as lex

# ---------- LÉXICO ----------
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
    'NOT_LOGICO'
)

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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"ERRO léxico - símbolo ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()