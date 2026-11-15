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
    rotulo_entrada: str = None
    rotulo_saida: str = None


class TabelaSimbolos:

    def __init__(self):
        self.escopos = [{}]
        self.nivel = 0

    def instala(self, simbolo):
        self.escopos[-1][simbolo.nome] = simbolo

    def busca(self, nome):
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        return None

    def existe_no_escopo(self, nome):
        return nome in self.escopos[-1]

    def entrar_escopo(self):
        self.escopos.append({})
        self.nivel += 1

    def sair_escopo(self):
        self.escopos.pop()
        self.nivel -= 1