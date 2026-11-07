from dataclasses import dataclass, field


# ---------- TABELA DE SÍMBOLOS ----------

@dataclass
class Simbolo:
    nome: str
    categoria: str
    tipo: str
    nivel: int
    endereco: int = None
    parametros: list = field(default_factory=list)


class TabelaSimbolos:

    def __init__(self):
        self.simbolos = []
        self.nivel = 0

    def instala(self, simbolo):
        self.simbolos.append(simbolo)

    def busca(self, nome):
        for simbolo in reversed(self.simbolos):
            if simbolo.nome == nome:
                return simbolo
        return None

    def existe_no_escopo(self, nome):
        for simbolo in self.simbolos:
            if simbolo.nome == nome and simbolo.nivel == self.nivel:
                return True
        return False

    def entra_funcao(self):
        self.nivel = 1

    def sai_funcao(self):
        self.simbolos = [s for s in self.simbolos if s.nivel != 1]
        self.nivel = 0