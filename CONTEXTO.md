# Contexto do projeto - Compilador Coda

Compiladores (UEM) - Profa. Valéria
Dupla: Gabriel Balancieri e Felipe Matheus

Compilador da linguagem Coda em Python + PLY 3.11: análise léxica, sintática (gerando AST), semântica com tabela de símbolos e geração de código MEPA. Entrega pelo Classroom até 23h59 de 29/11/2026. A apresentação vale **nota individual**: a professora pede para explicar trechos do código, as estruturas de dados, as regras de cada análise, a AST e a MEPA gerada. Os dois precisam saber explicar todas as partes.

Este arquivo reúne o contexto do trabalho e as instruções de como conduzi-lo. Divisão de tarefas e cronograma estão no `PLANEJAMENTO.md`.

---

## 1. Instruções

Leia isto antes de responder qualquer pergunta sobre o trabalho.

**Como funciona a ajuda neste trabalho.** A nota é individual e vem de uma apresentação oral, e a especificação penaliza partes do trabalho produzidas por IA generativa. Por isso, qualquer ajuda serve para entender, tirar dúvidas, depurar e revisar. O código do compilador é escrito pela dupla.

**O que você faz**
- Explica conceitos de compiladores e o funcionamento do PLY 3.11 e da MEPA.
- Mostra exemplos curtos (até ~12 linhas) em linguagens de brinquedo diferentes do Coda (calculadora, posfixo, exemplo do Robô). Não use palavras-chave do Coda nos exemplos.
- Revisa o nosso código (protocolo abaixo).
- Ajuda a depurar: pede para rodar algo, lê o traceback ou o `parser.out` junto com a gente.
- Sugere casos de teste e pode escrever programas Coda pequenos **como entrada de teste**.
- Transforma pontos ambíguos da especificação em perguntas para a professora.
- Sempre que possível, confere o comportamento rodando código, não de cabeça.

**O que você não faz**
- Não escreve as partes do compilador do Coda: regras léxicas, produções da gramática (inclusive a conversão EBNF para BNF do Coda), classes da AST, métodos de visita, tabela de símbolos, gerador de MEPA. Pseudocódigo que vira código linha a linha também conta.
- Teste: se a resposta pode ser colada no trabalho com poucas mudanças, passou do ponto.
- Não sugere nomes de arquivos, classes ou variáveis além dos que já estão neste arquivo: nomes são escolha da dupla.
- Não usa o PDF da especificação como fonte de regras. Use o resumo da seção 4, que tem só o texto visível. Caso omisso vai para a professora.

**Escada de dicas** (subir um degrau por vez, só se continuarmos travados depois de tentar):
1. uma pergunta que aponta a direção;
2. o conceito por trás e onde estudar (slide, lista, manual do PLY);
3. um exemplo análogo numa linguagem de brinquedo;
4. o algoritmo descrito em palavras ou num diagrama, sem código.

Se pedirmos o código pronto, responda com gentileza e firmeza em duas frases, lembre o motivo acima e ofereça o próximo degrau. Exceção: quando a resposta já estiver pronta no material da disciplina (slides, listas, exemplos da aula), aponte onde está e explique.

**Protocolo de revisão de código**
1. Leia tudo antes de comentar.
2. Diga em uma frase o que está bom.
3. Aponte no máximo três problemas, por prioridade: onde (arquivo, função), o que acontece (de preferência uma entrada que reproduz), por quê (o conceito) e uma dica. A correção é descrita em palavras; quem digita somos nós.
4. Termine com uma pergunta de defesa sobre o próprio código ("por que essa regra é função e aquela é string?"), para treinar a apresentação.

**Estilo das respostas:** português do Brasil, passo a passo, uma etapa por vez, com exemplos visuais (entrada e saída esperada). Peça para mostrarmos a saída antes de avançar.

---

## 2. Como rodar

Sempre a partir da raiz do repositório (`trabalho_coda>` no terminal):

```
python testa_lexico.py testes\lexico\borda.txt
```

Antes de cada commit, rodar todos os testes da pasta `testes\` e conferir se nada mudou (regressão).

---

## 3. Estrutura atual

```
trabalho_coda/
├── CONTEXTO.md            este arquivo
├── PLANEJAMENTO.md        divisão de tarefas e cronograma
├── README.md
├── .gitignore             ignora parsetab.py, parser.out e __pycache__
├── ply/                   PLY 3.11 (pacote do material da disciplina)
├── lexico.py              léxico completo (classe AnalisadorLexico)
├── testa_lexico.py        roda o léxico num arquivo e imprime os tokens
├── testes/
│   └── lexico/            simbolos, linhas, comentarios, identificadores, numeros, borda
└── praticas/posfixo/      práticas do posfixo feitas em aula
```

Próximos arquivos (nome escolhido por quem for escrever): o parser, as classes da AST e a impressora, a análise semântica e o gerador de MEPA. Cada fase ganha sua pasta em `testes\`.

**Material de referência da disciplina:** slides (em especial "3. Análise Léxica", "4. Análise Sintática" e os de LR), Lista 3 (questões 13 a 15 sobre o léxico), práticas do posfixo e o exemplo do Robô (`robo_lexer.py`, `robo_parser.py`, `robo_ast.py`, `robo_ast_utils.py`), que é o modelo de estrutura em classes.

---

## 4. Especificação do Coda (resumo do texto visível)

### Léxico
- Case-sensitive.
- 13 palavras reservadas: `program fun int bool void if else while return read print true false`.
- 21 símbolos: `( ) ; { } , -> = == != < <= > >= + - * / && || !`.
- Identificador: letra seguida de letras, dígitos ou `_`. Palavra reservada não pode ser identificador.
- Número: um ou mais dígitos decimais. O sinal não faz parte do número (`-42` são dois tokens; o menos unário é tratado na sintaxe).
- Comentário de linha começando em `//`.
- Espaços, tabulações e quebras de linha são ignorados, mas as quebras são contadas para indicar a linha dos erros.
- Caractere ou sequência inválida: mensagem de erro com pelo menos a linha.

### Tipos e organização
- `int`, `bool` e `void` (só como retorno de função). Sem tipos definidos pelo programador.
- Funções só no escopo global (sem aninhamento), introduzidas por `fun`, com tipo de retorno.
- No programa: declarações de variáveis, depois funções, depois comandos. Na função: declarações de variáveis, depois comandos.
- Declaração de variável sem valor inicial.

### Gramática (EBNF do Apêndice I)

```
<programa>             ::= 'program' <identificador> '{' <declaracoes-variaveis> <declaracoes-funcoes> <comandos> '}'
<declaracoes-funcoes>  ::= { <declaracao-funcao> }
<declaracao-funcao>    ::= 'fun' <identificador> '(' [ <lista-parametros> ] ')' '->' <tipo-retorno>
                           '{' <declaracoes-variaveis> <comandos> '}'
<lista-parametros>     ::= <parametro> { ',' <parametro> }
<parametro>            ::= <tipo> <identificador>
<declaracoes-variaveis>::= { <declaracao-variavel> }
<declaracao-variavel>  ::= <tipo> <identificador> ';'
<tipo>                 ::= 'int' | 'bool'
<tipo-retorno>         ::= 'int' | 'bool' | 'void'
<comandos>             ::= { <comando> }
<comando>              ::= <atribuicao> | <condicional> | <repeticao> | <retorno>
                         | <leitura> | <escrita> | <chamada-comando>
<atribuicao>           ::= <identificador> '=' <expressao> ';'
<condicional>          ::= 'if' '(' <expressao> ')' <bloco> [ 'else' <bloco> ]
<repeticao>            ::= 'while' '(' <expressao> ')' <bloco>
<bloco>                ::= '{' <comandos> '}'
<retorno>              ::= 'return' <expressao> ';'
<leitura>              ::= 'read' '(' <lista-identificadores> ')' ';'
<lista-identificadores>::= <identificador> { ',' <identificador> }
<escrita>              ::= 'print' '(' <lista-expressoes> ')' ';'
<lista-expressoes>     ::= <expressao> { ',' <expressao> }
<chamada-comando>      ::= <chamada> ';'
<chamada>              ::= <identificador> '(' [ <lista-expressoes> ] ')'
<expressao>            ::= <expressao> <operador-binario> <expressao> | <operador-unario> <expressao>
                         | <numero> | <booleano> | <identificador> | <chamada> | '(' <expressao> ')'
<operador-binario>     ::= '+' | '-' | '*' | '/' | '<' | '<=' | '>' | '>=' | '==' | '!=' | '&&' | '||'
<operador-unario>      ::= '-' | '!'
```

A EBNF deve ser convertida para BNF para o PLY, preferindo recursão à esquerda. A gramática de expressões é ambígua; a ambiguidade se resolve com a precedência do PLY.

### Precedência (da menor para a maior)
1. `||` esquerda
2. `&&` esquerda
3. `==` `!=` não associativos
4. `<` `<=` `>` `>=` não associativos
5. `+` `-` esquerda
6. `*` `/` esquerda
7. `-` unário e `!` direita

Operadores não associativos não podem ser encadeados no mesmo nível.

### Semântica
- Tabela de símbolos com categoria, tipo, escopo, nível léxico e o que mais as fases seguintes precisarem.
- Programa = escopo global, nível 0. Cada função = escopo local, nível 1. Blocos de `if`, `else` e `while` não criam escopo. Escopo léxico; locais podem ocultar globais.
- Redeclaração no mesmo escopo: erro, e a declaração anterior permanece.
- Chamada: o identificador deve ser função declarada e visível; mesmo número de argumentos e parâmetros; tipos iguais na mesma ordem. Recursão direta permitida. Parâmetros por valor.
- Função `void` não produz valor: chamada só como comando. Funções `int`/`bool` podem ser usadas em expressões ou como comando (valor descartado).
- Funções `int`/`bool` precisam de pelo menos um `return <expressão>` do tipo declarado (sem análise de caminhos). Funções `void` não têm `return`.
- Atribuição: o alvo é variável declarada e visível; a expressão tem o mesmo tipo.
- Condição de `if` e `while`: tipo `bool`.
- `read`: cada argumento é variável visível, `int` ou `bool`. `print`: cada argumento é expressão `int` ou `bool`.
- Expressões: `+ - * /` e `-` unário: `int` → `int`; `< <= > >=`: `int` → `bool`; `== !=`: operandos do mesmo tipo (`int` ou `bool`) → `bool`; `&& ||` e `!`: `bool` → `bool`. Número é `int`; `true`/`false` são `bool`; variável tem o tipo declarado; chamada tem o tipo de retorno da função.

### Entrega
- AST explícita: semântica e geração de código são travessias da AST, não ações do parser.
- Execução pela linha de comando, recebendo o arquivo-fonte como argumento; MEPA na saída padrão ou em arquivo.

---

## 5. Padrões do código

**Geral**
- Nomes, comentários e mensagens em português.
- Cada fase é uma classe, no modelo do exemplo do Robô: o PLY é montado no `__init__` com `module=self`.
- O parser pega os tokens direto da classe do léxico: `tokens = AnalisadorLexico.tokens`.
- Passar o lexer explicitamente para o parser (`parse(..., lexer=...)`).
- Nada de verificação semântica nas ações do parser: elas só montam a AST.
- Nunca gerar MEPA se houve qualquer erro (léxico, sintático ou semântico).

**Mensagens de erro** (formato atual do léxico, manter o padrão nas outras fases):
```
ERRO léxico - símbolo ilegal '$' na linha 3
```
Sugestão para as próximas: `ERRO sintático - ... na linha N`, `ERRO semântico - ... na linha N`.

**Tokens do léxico** (o parser usa exatamente estes nomes)

| Símbolo | Token | Símbolo | Token |
|---|---|---|---|
| `(` | ABRE_PAREN | `<=` | MENOR_IGUAL |
| `)` | FECHA_PAREN | `>` | MAIOR |
| `;` | PONTO_VIRGULA | `>=` | MAIOR_IGUAL |
| `{` | ABRE_CHAVE | `+` | MAIS |
| `}` | FECHA_CHAVE | `-` | MENOS |
| `,` | VIRGULA | `*` | ASTERISCO |
| `=` | ATRIB | `/` | DIV |
| `->` | SETA | `&&` | AND_LOGICO |
| `==` | IGUAL | `\|\|` | OR_LOGICO |
| `!=` | DIFERENTE | `!` | NOT_LOGICO |
| `<` | MENOR | | |

- `ID`: identificador, o valor é o texto (`'x_1'`).
- `NUM`: número, o valor já vem como `int` (`42`).
- Palavras reservadas: o token é a palavra em maiúsculas: `PROGRAM FUN INT BOOL VOID IF ELSE WHILE RETURN READ PRINT TRUE FALSE`.
- `TRUE` e `FALSE` são dois tokens separados, e o valor deles é o texto (`'true'`/`'false'`), não `bool` do Python.
- Comentários `//` e quebras de linha não viram token. `-42` são dois tokens (`MENOS` e `NUM`).

**Coisas do PLY que já deram problema (não repetir)**
- Regra escrita como função é testada antes das regras string, na ordem do arquivo. Regras string são ordenadas pelo tamanho da regex.
- `t_error` e `t_ignore` são nomes especiais: não podem ser renomeados.
- No léxico, nenhuma variável que não seja regra pode começar com `t_` (quebra o `lex.lex()`). No parser, evitar `p_` em qualquer coisa que não seja regra (gera aviso).
- Todo tipo devolvido por uma regra precisa estar na tupla `tokens`.
- Dentro da classe, toda regra recebe `self` (`def t_ID(self, t)`, `def p_x(self, p)`).
- Na docstring das regras do parser, precisa de espaço antes e depois do `:`.
- O `robo_parser.py` está incompleto e tem erros de digitação (`p.lineono`, `p.lineo`, `ast.Int`, `p[0] = p[3]`). Usar como modelo de estrutura, não copiar.

---

## 6. Como fazer cada fase

### Fase 2 - Parser (reconhecedor)

1. Converter a EBNF da seção 4 para BNF **no papel**: repetições `{ }` viram listas com recursão à esquerda; opcionais `[ ]` viram uma produção vazia ou duas versões da produção-mãe.
2. Escrever as regras no PLY **sem ações**, só para reconhecer. Definir o símbolo inicial com `start`.
3. Expressões: uma produção por operador (com o token do operador escrito na produção), a tabela `precedence` com os 7 níveis da especificação e o menos unário com `%prec` (o `-` unário e o binário são o mesmo token).
4. `p_error` com a linha do token, tratando o caso `None` (fim de arquivo inesperado), e um flag de erro.
5. Construir com `debug=True` e `write_tables=False`, e ler o `parser.out`.

**Pronto quando:** o `parser.out` não tem nenhum conflito; programas válidos são aceitos; `a < b < c` e `a == b != c` são rejeitados.

**Armadilhas:**
- agrupar os operadores num não-terminal (`e : e op e`) desliga a precedência;
- um operador esquecido na `precedence` é resolvido errado em silêncio;
- um nome fictício na `precedence` que nunca aparece num `%prec` dá erro fatal;
- `p_empty` como primeira regra vira o símbolo inicial;
- um opcional em volta de uma lista que já pode ser vazia gera conflito reduce/reduce;
- com `debug=False` ou com `parsetab.py` em cache, os conflitos não aparecem;
- conflito em `ELSE` significa conversão errada: no Coda os blocos têm chaves, então não existe "else pendente".

**Perguntas prováveis:** como vocês converteram `{ }` e `[ ]`; por que recursão à esquerda; como o PLY usa a `precedence`; o que o `nonassoc` faz; por que `if/else` não gera conflito; por que atribuição e chamada, que começam com identificador, não conflitam.

### Fase 3 - AST

1. Desenhar os nós **no papel**: para cada construção, o que a semântica e a MEPA vão precisar (vira campo) e o que é só pontuação (`;`, parênteses, chaves e `->` somem). Repetições viram listas do Python; opcionais ausentes viram `None` ou `[]`. Todo nó guarda a **linha**.
2. Escrever as classes (modelo `robo_ast.py`: dataclasses, classe base com `linha`, classes intermediárias para comando e expressão) e a impressora (modelo `robo_ast_utils.py`).
3. Testar montando árvores à mão, sem o parser.
4. Integração com o parser: as ações fazem `p[0] = ...`. Parênteses devolvem o nó de dentro. A linha vem de um token da própria produção (o operador, a palavra-chave ou o identificador) com `p.lineno(n)`. A chamada usada como comando e como expressão precisa ser distinguível, porque a semântica trata as duas de forma diferente.

**Pronto quando:** a árvore impressa de três programas de teste não tem `;`, parênteses nem chaves, e `-a * b`, `!a && b || c` e `a - -b` aparecem agrupados como `(-a)*b`, `((!a) && b) || c` e `a - (-b)`.

**Armadilhas:** esquecer o `p[0]` deixa `None` na árvore; `p.lineno(n)` de um não-terminal devolve 0; verificação semântica dentro do parser (não pode).

**Perguntas prováveis:** o que entra e o que fica fora da AST e por quê; como a linha chega ao nó; por que separar parser e semântica; como a precedência aparece no formato da árvore.

### Fase 4 - Semântica

1. Tabela de símbolos com nível (0 global, 1 função), categoria, tipo e deslocamento. Escolher a organização e saber justificar.
2. Travessia da AST (um método de visita por tipo de nó; o método genérico deve **acusar** nó não tratado, não ignorar).
3. Função: verificar redeclaração, montar a assinatura completa e instalar a função **antes** do corpo (por causa da recursão); depois abrir o nível 1, instalar parâmetros e locais e visitar o corpo.
4. Tipo "erro" para expressões que falharam, para um erro não virar uma cascata de mensagens. Mensagens com linha.
5. O que a MEPA vai precisar (nível, deslocamento, número de locais e de parâmetros) tem que sobreviver à saída do escopo da função.

**Pronto quando:** cada caso abaixo dá exatamente o resultado esperado, com um erro por caso:
- local com o nome de um global: aceito; parâmetro e local com o mesmo nome: erro; global e função com o mesmo nome: erro;
- recursão direta: aceita;
- função `void` dentro de expressão, `1 == true`, `while (n)` com `n` `int`, número errado de argumentos: um erro cada;
- função `int` sem `return`: erro; `return` em função `void`: erro.

**Perguntas prováveis:** como a busca trata o sombreamento; quando a função entra na tabela; como detectar chamada `void` dentro de expressão; o que acontece com `1 == true`; por que calcular os deslocamentos já aqui.

### Fase 5 - MEPA

1. Esqueleto do programa, globais, atribuição e expressões (pós-ordem, como no posfixo).
2. `print` e `read`.
3. `if`/`else` e `while` com rótulos únicos (contador, reservando os rótulos antes de gerar os filhos).
4. Funções: chamada como expressão e como comando, parâmetros, locais, `return`, recursão.

Antes do passo 4, confirmar no material da professora a variante de chamada (`CHPR p` ou `CHPR p,k`), porque ela muda o deslocamento dos parâmetros e do resultado. Deixar esse cálculo numa função só, e a formatação do texto MEPA num ponto só.

**Pronto quando:** fatorial recursivo, um laço com uma chamada de função usada como comando e um `return` dentro de `while` dão a saída certa no interpretador da professora, e a pilha não cresce.

**Armadilhas:** esquecer o `AMEM 1` antes dos argumentos de uma função `int`/`bool`; não descartar (`DMEM 1`) o resultado de uma chamada usada como comando; empilhar o operando direito primeiro (inverte `-`, `/` e as comparações); `return` sem salto para o fim da função.

**Perguntas prováveis:** o que é o par (k, n); por que os parâmetros têm deslocamento negativo; por que `AMEM 1` antes dos argumentos; desenhe a pilha durante `f(3)`; como um `return` dentro de `while` sai da função; como vocês garantem rótulos únicos.

### Fase 6 - Fechamento

Rodar todos os testes de novo; revisar mensagens de erro e a execução pela linha de comando; ensaiar a apresentação, cada um explicando as partes que o outro escreveu; entregar no Classroom em 28/11.

---

## 7. Registro de decisões

A coluna "Por quê" é preenchida pela dupla, com as nossas palavras (a professora pode perguntar).

| Decisão | Alternativas | Por quê |
|---|---|---|
| `1abc` vira `NUM(1)` + `ID(abc)`, sem erro léxico (confirmar com a professora) | acusar "identificador malformado" já no léxico | |
| `true` e `false` como dois tokens (`TRUE`, `FALSE`) | um token só para os dois | |
| Léxico (e as próximas fases) organizados como classe | funções soltas no módulo | |
| Código na raiz do repositório | pasta `src/` | |
| Palavras reservadas por dicionário consultado no `t_ID` | uma regra por palavra | |
