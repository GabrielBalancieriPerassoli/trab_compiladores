import sys
from lexico import AnalisadorLexico

caminho = sys.argv[1]
with open(caminho, encoding='utf-8') as arquivo:
    data = arquivo.read()

lexer = AnalisadorLexico()
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)