"""gestor_plantel.py: Sistema de Gestão do plantel
"""

import sys
from dataclasses import dataclass, astuple
from enum import StrEnum
from statistics import mean
from typing import List, Any, Dict, Tuple, Callable, Iterator
from operator import attrgetter


class Metrica(StrEnum):
    """Enumerado para as metricas"""

    GOLOS = "golos"
    ASSISTENCIAS = "assistencias"
    DEFESAS = "defesas"
    MINUTOS_JOGADOS = "minutos_jogados"


@dataclass
class Recomendacao:
    """Representação para Recomendações"""

    metrica: Metrica
    melhor: Callable[Any, str]
    pior: Callable[Any, str]


@dataclass(frozen=True, order=True)
class Jogador:
    """Representação para Jogador"""

    id: int
    nome: str


@dataclass(frozen=True, order=True)
class Medida:
    """Representação para Medida"""

    metrica: Metrica
    valor: int
    treino_id: int
    jogador_id: int


@dataclass
class EstatisticaPlantel:
    """Representação para Estatísticas do Plantel"""

    metrica: Metrica
    media: float
    melhor: Tuple[int, str]
    pior: Tuple[int, str]


@dataclass
class Plantel:
    """Representação para Plantel"""

    jogadores: List[Jogador]
    medidas: List[Medida]

    def adicionar_jogador(self, jogador: Jogador):
        """Adiciona um Jogador"""
        self.jogadores.append(jogador)

    def adicionar_medida(self, medida: Medida):
        """Adiciona uma medida"""
        self.medidas.append(medida)

    def jogador_por_id(self, jogador_id: int) -> Jogador:
        """Retorna o jogador com um dado id"""
        return next(jogador for jogador in self.jogadores if jogador.id == jogador_id)

    def medidas_de_metrica(self, metrica: Metrica) -> Iterator[Medida]:
        """Retorna um iterador para todas as medidas de uma dada metrica"""
        return (medida for medida in self.medidas if medida.metrica == metrica)

    def max_de_metrica(self, metrica: Metrica) -> Medida:
        """Retorna a medida com o valor máximo numa dada metrica"""
        return max(
            self.medidas_de_metrica(metrica),
            key=attrgetter("valor"),
        )

    def min_de_metrica(self, metrica: Metrica) -> Medida:
        """Retorna a medida com o valor mínimo numa dada metrica"""
        return min(
            self.medidas_de_metrica(metrica),
            key=attrgetter("valor"),
        )

    def estatisticas_plantel(self) -> List[EstatisticaPlantel]:
        """Retorna uma lista com as estatísticas associadas ao plantel"""

        def obter_tuplo_valor_nome(medida: Medida):
            valor = medida.valor
            nome = self.jogador_por_id(medida.jogador_id).nome
            return (valor, nome)

        return [
            EstatisticaPlantel(
                metrica=metrica,
                media=mean(medida.valor for medida in self.medidas_de_metrica(metrica)),
                melhor=obter_tuplo_valor_nome(self.max_de_metrica(metrica)),
                pior=obter_tuplo_valor_nome(self.min_de_metrica(metrica)),
            )
            for metrica in Metrica
        ]


# Predicados
def positivop(n: int):
    """Predicado para verificar que n é positivo"""
    return n > 0


def nao_negativop(n: int):
    """Predicado para verificar que n é não negativo"""
    return n >= 0


PROMPTS_METRICAS: Dict[Metrica, str] = {
    Metrica.GOLOS: "Golo(s)",
    Metrica.ASSISTENCIAS: "Assistências",
    Metrica.DEFESAS: "Defesas",
    Metrica.MINUTOS_JOGADOS: "Minutos jogados",
}

RECOMENDACAO_METRICAS: Dict[Metrica, Recomendacao] = {
    Metrica.GOLOS: Recomendacao(
        Metrica.GOLOS,
        (lambda nome: f"{nome} esteve bem em golos, merece reconhecimento."),
        (lambda nome: f"{nome} tem de melhorar a sua performance em golos."),
    ),
    Metrica.ASSISTENCIAS: Recomendacao(
        Metrica.ASSISTENCIAS,
        (lambda nome: f"{nome} esteve bem em assistências, merece reconhecimento."),
        (lambda nome: f"{nome} tem de melhorar a sua performance em assistências."),
    ),
    Metrica.DEFESAS: Recomendacao(
        Metrica.DEFESAS,
        (
            lambda nome: f"{nome} esteve excelente em defesas,"
            + " merecendo reconhecimento pela sua defesa/sólida no tempo em que jogou."
        ),
        (
            lambda nome: f"{nome} pode melhorar sua performance em defesa "
            + "deve contribuir mais para a equipa."
        ),
    ),
    Metrica.MINUTOS_JOGADOS: Recomendacao(
        Metrica.MINUTOS_JOGADOS,
        (
            lambda nome: f"{nome} esteve excelente em minutos jogados,"
            + "merecendo reconhecimento pela sua defesa/sólida no tempo em que jogou."
        ),
        (
            lambda nome: f"{nome} pode melhorar sua performance em minutos jogados "
            + "deve contribuir mais para a equipa."
        ),
    ),
}


def input_intp(p: Callable[int, bool], id_e_prompt: Tuple[str, str]) -> int:
    """input para inteiros que valida de acordo com um predicado p"""
    str_id, prompt = id_e_prompt
    n = int(input(f"{prompt}: "))
    if not p(n):
        raise ValueError(f"{str_id} não pode assumir valor {n}")
    return n


def ler_medidas(plantel: Plantel, jogador_id: int):
    """Lê medidas e adiciona ao plantel"""
    treino_id = input_intp(positivop, ("treino_id", "Treino"))
    for metrica in Metrica:
        prompt = PROMPTS_METRICAS.get(metrica)
        valor = input_intp(positivop, (metrica, prompt))
        plantel.adicionar_medida(Medida(metrica, valor, treino_id, jogador_id))


def adicionar_jogadores_plantel(plantel: Plantel = None) -> Plantel:
    """Lê jogadores e adiciona ao plantel"""
    n = input_intp(nao_negativop, ("Número de jogadores", "Número de Jogadores"))

    if plantel is None:
        plantel = Plantel([], [])

    base = len(plantel.jogadores) + 1

    for jogador_id in range(base, base + n):
        print(f"Jogador {jogador_id}:")
        nome = input("Nome: ")
        plantel.adiciona_jogador(Jogador(jogador_id, nome))
        ler_medidas(plantel, jogador_id)

    return plantel


def imprimir_estatisticas(estatisticas: List[EstatisticaPlantel]):
    """Imprime estatísticas"""
    for metrica, media, (melhor_valor, melhor_nome), (pior_valor, pior_nome) in map(
        astuple, estatisticas
    ):
        print(f"\nEstatísticas para {metrica}:")
        print(f"Média: {media: .2f}")
        print(f"Máximo: {melhor_valor} (melhor desempenho: {melhor_nome})")
        print(f"Mínimo: {pior_valor} (pior desempenho: {pior_nome})")


def imprimir_recomendacoes(estatisticas: List[EstatisticaPlantel]):
    """Imprime recomendações"""
    print("\nRecomendações:")
    for metrica, _, (_, melhor_nome), (_, pior_nome) in map(astuple, estatisticas):
        recomendacao = RECOMENDACAO_METRICAS.get(metrica)
        print(recomendacao.melhor(melhor_nome))
        print(recomendacao.pior(pior_nome))


def main():
    """Função de entrada"""
    plantel = None
    parar = False

    while not parar:
        try:
            plantel = adicionar_jogadores_plantel(plantel)
        except ValueError as error:
            print(error.args)
            sys.exit(1)
        estatisticas = plantel.estatisticas_plantel()
        imprimir_estatisticas(estatisticas)
        imprimir_recomendacoes(estatisticas)

        parar = input("\nParar(s/n)? ").strip().lower() == "s"


if __name__ == "__main__":
    main()
