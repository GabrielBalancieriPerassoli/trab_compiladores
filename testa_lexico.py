import sys
from lexico import lexer

caminho = sys.argv[1]
with open(caminho, encoding='utf-8') as arquivo:
    data = arquivo.read()

lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)