# Compilador Coda

Trabalho da disciplina de Compiladores da UEM, com a Profa. Valéria Feltrim.

Dupla: Gabriel Balancieri Perassoli e Felipe Matheus.

Compilador da linguagem Coda feito em Python com o PLY 3.11. O programa passa pela análise léxica, pela análise sintática (que monta a AST) e pela análise semântica, e no final é gerado o código para a MEPA.

## Requisitos

- Python 3.10 ou mais novo.
- O PLY já está na pasta `ply/`, então não precisa instalar nada.

## Como compilar

```
python coda.py programa.txt
```

O código MEPA sai na tela. Para gravar num arquivo, passe o nome do arquivo de saída:

```
python coda.py programa.txt programa.mepa
```

Se o programa tiver erro léxico, sintático ou semântico, o compilador mostra as mensagens com a linha de cada erro e não gera código.

A mensagem `Generating LALR tables` é do próprio PLY e aparece toda vez. Ela vai para a saída de erro, então não entra no arquivo `.mepa`.

## Como executar o código MEPA

Com o interpretador da MEPA descompactado numa pasta `mepa`:

```
python mepa/mepa_pt.py --progfile programa.mepa
```

Se o programa tiver `read`, o interpretador fica esperando os valores no terminal.

Exemplo com o fatorial recursivo dos testes:

```
python coda.py testes/mepa/fatorial.txt fatorial.mepa
python mepa/mepa_pt.py --progfile fatorial.mepa
```

Digitando `5`, a saída é `120`.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `coda.py` | programa principal: lê o arquivo, roda as análises e gera o MEPA |
| `lexico.py` | análise léxica |
| `sintatico.py` | análise sintática com o PLY, monta a AST |
| `arvore_ast.py` | classes dos nós da AST e a função que imprime a árvore |
| `visitador.py` | classe base dos visitadores (usada pelo semântico e pelo gerador) |
| `tabela_simbolos.py` | tabela de símbolos |
| `semantico.py` | análise semântica |
| `mepa.py` | gerador de código MEPA |
| `testa_lexico.py` | roda só o léxico e lista os tokens |
| `testa_sintatico.py` | roda o léxico e o sintático e imprime a AST |
| `testa_semantico.py` | roda até o semântico e mostra os erros e a tabela de símbolos |
| `testes/` | programas de teste, separados por fase |
| `ply/` | biblioteca PLY 3.11 |

## Testando cada fase

```
python testa_lexico.py testes/lexico/numeros.txt
python testa_sintatico.py testes/sintatico/valido.txt
python testa_semantico.py testes/semantico/retorno.txt
python coda.py testes/mepa/controle.txt
```

Na pasta `testes/sintatico`, os arquivos que começam com `erro_` devem ser rejeitados. Na pasta `testes/semantico`, cada arquivo tem erros de um tipo, menos o `declaracoes_ok.txt`, que é aceito. Os programas de `testes/mepa` foram rodados no interpretador da MEPA.

## Decisões de implementação

- A tabela de símbolos é uma pilha de escopos: o escopo global (nível 0) e um escopo para cada função (nível 1). A busca vai do topo para a base, então uma variável local esconde uma global com o mesmo nome.
- A análise semântica não para no primeiro erro: os erros são guardados e mostrados no final, em ordem de linha. Se tiver erro léxico ou sintático, a análise semântica não roda. Com qualquer erro, nenhum código MEPA é gerado.
- A chamada de função usa `CHPR p,k`. Os argumentos são empilhados na ordem da declaração: o primeiro parâmetro fica em `-(n+4)` e o último em `-5`, o valor de retorno fica em `-(n+5)` e as variáveis locais começam em `0`.
- O `&&` e o `||` calculam os dois lados e depois aplicam `CONJ` ou `DISJ`.
