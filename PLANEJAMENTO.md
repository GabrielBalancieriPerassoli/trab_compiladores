# Planejamento do trabalho - Compilador Coda

Dupla: Gabriel Balancieri e Felipe Matheus
Entrega: Classroom, até 23h59 de 29/11/2026 (meta interna: 28/11)

Padrões de código, tokens e decisões estão no `CONTEXTO.md`.

---

## Como a dupla trabalha

- Cada um escreve o próprio código. Commits pequenos, mensagem em português dizendo o que mudou.
- IA usada como tutor: tirar dúvidas, explicar erros, revisar. Quem escreve o código e precisa saber explicar cada linha somos nós.
- Trabalho em paralelo com uma branch por parte (`parser`, `ast`...). Ao terminar, abre Pull Request no GitHub e **o outro revisa antes do merge**. A revisão é também o estudo da parte do outro para a apresentação.
- `git pull` antes de começar a mexer, `git push` ao terminar.
- Antes de cada encontro com a professora, um explica para o outro a parte que não escreveu.

---

## Divisão e cronograma

| Fase | Período | Responsável | Pronto quando |
|---|---|---|---|
| 0. Preparação | 16 a 18/10 | Gabriel | concluída |
| 1. Léxico | 19 a 25/10 | Gabriel | concluída em 19/10 (classe em 23/10) |
| 2. Parser reconhecedor | 26/10 a 01/11 | Felipe | `parser.out` sem conflitos, aceita programas válidos, rejeita `a < b < c` e `a == b != c` |
| 3. AST (em paralelo) | 26/10 a 08/11 | Gabriel | classes dos nós + impressora; árvore de 3 programas sem `;`, parênteses ou chaves |
| 2+3. Integração | até 08/11 | os dois juntos | parser montando a AST nas ações |
| 4. Semântica | 09 a 16/11 | a definir | todos os testes de erro semântico com a mensagem e a linha certas |
| 5. MEPA | 17 a 24/11 | a definir | fatorial recursivo rodando no interpretador da professora |
| 6. Fechamento | 25 a 28/11 | os dois | regressão completa, ensaio da apresentação, entrega |

Prova 1: data a confirmar (reservar a semana para estudo).

---

## Combinado entre parser e AST

1. O Felipe começa com o parser só reconhecendo: regras sem ações, até o `parser.out` ficar sem conflitos.
2. Enquanto isso, o Gabriel define as classes dos nós e a impressora, testando com árvores montadas à mão.
3. Quando os dois estiverem prontos, as ações `p[0] = ...` são escritas juntos, numa sessão em dupla.
