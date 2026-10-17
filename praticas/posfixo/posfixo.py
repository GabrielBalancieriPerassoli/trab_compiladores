import ply.lex as lex
import ply.yacc as yacc

# ---------- LÉXICO ----------
tokens = ('IDENT', 'MAIS', 'MENOS', 'ASTERISCO', 'DIV')

t_MAIS      = r'\+'
t_MENOS     = r'-'
t_ASTERISCO = r'\*'
t_DIV       = r'/'

def t_IDENT(t):
    r'a'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"ERRO léxico - símbolo ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------- SINTÁTICO ----------
def p_expr_mais(p):
    "expr : expr MAIS termo"
    p[0] = p[1] + p[3] + ' + '

def p_expr_menos(p):
    "expr : expr MENOS termo"
    p[0] = p[1] + p[3] + ' - '

def p_expr_termo(p):
    "expr : termo"
    p[0] = p[1]

def p_termo_vezes(p):
    "termo : termo ASTERISCO fator"
    p[0] = p[1] + p[3] + ' * '

def p_termo_div(p):
    "termo : termo DIV fator"
    p[0] = p[1] + p[3] + ' / '

def p_termo_fator(p):
    "termo : fator"
    p[0] = p[1]

def p_fator_ident(p):
    "fator : IDENT"
    p[0] = ' A '

def p_error(t):
    if t:
        print(f"ERRO de sintaxe perto de '{t.value}'")
    else:
        print("ERRO de sintaxe no EOF")

parser = yacc.yacc(start='expr')

# ---------- MAIN ----------
if __name__ == "__main__":
    while True:
        expressao = input('> ')
        if not expressao:
            break

        resultado = parser.parse(expressao, lexer=lexer)
        if resultado:
            print(resultado)
