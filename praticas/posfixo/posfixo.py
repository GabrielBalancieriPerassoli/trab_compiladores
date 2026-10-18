import ply.lex as lex
import ply.yacc as yacc

# ---------- LÉXICO ----------
tokens = ('IDENT', 'MAIS', 'MENOS', 'ASTERISCO', 'DIV', 'AND', 'OR')

t_MAIS      = r'\+'
t_MENOS     = r'-'
t_ASTERISCO = r'\*'
t_DIV       = r'/'

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_IDENT(t):
    r'a|b'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"ERRO léxico - símbolo ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------- SINTÁTICO ----------
def p_or_op(p):
    "or_op : or_op OR and_op"
    p[0] = p[1] + p[3] + " or "

def p_or_desce(p):
    "or_op : and_op"
    p[0] = p[1]

def p_and_op(p):
    "and_op : and_op AND expr"
    p[0] = p[1] + p[3] + " and "

def p_and_desce(p):
    "and_op : expr"
    p[0] = p[1]

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
    p_aux = p[1].upper()
    p[0] = "" + p_aux + " "

def p_error(t):
    if t:
        print(f"ERRO de sintaxe perto de '{t.value}'")
    else:
        print("ERRO de sintaxe no EOF")

parser = yacc.yacc(start='or_op')

# ---------- MAIN ----------
if __name__ == "__main__":
    while True:
        expressao = input('> ')
        if not expressao:
            break

        resultado = parser.parse(expressao, lexer=lexer)
        if resultado:
            print(resultado)
