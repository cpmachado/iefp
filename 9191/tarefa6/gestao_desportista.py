"""gestor_desportista.py: Sistema de Gestão de Desportistas
"""

import csv
from dataclasses import dataclass, astuple
from typing import List, Any, Dict, Callable, Iterator
from operator import attrgetter


@dataclass(frozen=True, order=True)
class Avaliacao:
    """Representação de uma Avaliação"""

    id: int
    desportista_id: int
    valor: float


@dataclass(frozen=True, order=True)
class Desportista:
    """Representação de um Desportista"""

    id: int
    nome: str


def ler_lista_tipo(filename: str) -> List[Any]:
    """Lê as linhas de um csv e retorna"""
    try:
        with open(filename, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            # skip do cabeçalho
            next(reader, None)
            return list(reader)
    except FileNotFoundError:
        return []


def ler_desportistas(filename: str = "desportistas.csv") -> List[Desportista]:
    """Lê desportistas de um ficheiro"""
    return [
        Desportista(int(desportista_id), nome)
        for desportista_id, nome in ler_lista_tipo(filename)
    ]


def ler_avaliacoes(filename: str = "avaliacoes.csv") -> List[Avaliacao]:
    """Lê avaliações de um ficheiro"""
    return [
        Avaliacao(int(avaliacao_id), int(desportista_id), float(valor))
        for avaliacao_id, desportista_id, valor in ler_lista_tipo(filename)
    ]


def escrever_lista_tipo(
    filename: str, elementos: List[Any], t: Callable, header: Iterator[Any] = None
):
    """Escreve um csv"""
    with open(filename, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # escrever cabeçalho
        if header:
            writer.writerow(header)
        writer.writerows(map(t, elementos))


def escrever_desportistas(
    elementos: List[Desportista], filename: str = "desportistas.csv"
):
    """Escreve um csv com desportistas"""
    return escrever_lista_tipo(filename, elementos, astuple, ("id", "nome"))


def escrever_avaliacoes(elementos: List[Avaliacao], filename: str = "avaliacoes.csv"):
    """Escreve um csv com avaliacões"""
    return escrever_lista_tipo(
        filename, elementos, astuple, ("id", "desportista_id", "valor")
    )


@dataclass
class GrupoDesportivo:
    """Representação de desportistas e avaliações e interoperabilidade entre ambos"""

    desportistas: List[Desportista]
    avaliacoes: List[Avaliacao]

    def adicionar_desportista(self, nome):
        """Adiciona um desportista ao grupo"""
        if nome in map(attrgetter("nome"), self.desportistas):
            raise UserWarning("Desportista já existe?")
        desportista_id = max(map(attrgetter("id"), self.desportistas)) + 1
        desportista = Desportista(desportista_id, nome)
        self.desportistas.append(desportista)
        return desportista

    def adicionar_avaliacao(self, desportista_id, valor):
        """Adiciona uma avaliação ao grupo"""
        avaliacao_id = max(map(attrgetter("id"), self.avaliacoes)) + 1
        avaliacao = Avaliacao(avaliacao_id, desportista_id, valor)
        self.avaliacoes.append(avaliacao)
        return avaliacao

    def desportista_chamado(self, nome):
        """Retorna um desportista de um dado nome, assumindo que seja como um id único"""
        return next(
            desportista for desportista in self.desportistas if desportista.nome == nome
        )

    def avaliacoes_de_desportista(self, desportista: Desportista):
        """Retorna um iterador para avaliações de um desportista"""
        return (
            avaliacao
            for avaliacao in self.avaliacoes
            if avaliacao.desportista_id == desportista.id
        )

    def salvar(
        self,
        ficheiro_desportistas: str = "desportistas.csv",
        ficheiro_avaliacoes: str = "avaliacoes.csv",
    ):
        """Salve Grupo para csvs"""
        escrever_desportistas(self.desportistas, ficheiro_desportistas)
        escrever_avaliacoes(self.avaliacoes, ficheiro_avaliacoes)


def visualizar_desportista(grupo: GrupoDesportivo, desportista: Desportista):
    """Visualiza um único desportista de um grupo"""
    print(f"Nome: {desportista.nome}")
    print(f"Id: {desportista.id}")
    print("Avaliacões:")
    for avaliacao in grupo.avaliacoes_de_desportista(desportista):
        print(f" - id: {avaliacao.id}")
        print(f" - valor: {avaliacao.valor: g}")


def visualizar_desportistas(grupo: GrupoDesportivo):
    """Comando para visualizar todos os desportistas do grupo"""
    print("Visualizar:\n")
    for desportista in grupo.desportistas:
        visualizar_desportista(grupo, desportista)
        print("")


def adicionar_desportista(grupo: GrupoDesportivo):
    """Comando para adicionar um desportista do grupo"""
    nome = input("Insira o nome do desportista: ").strip()
    try:
        desportista = grupo.adicionar_desportista(nome)
        print(f"Criado Desportista {desportista.id}: {desportista.nome}")
    except UserWarning as error:
        print(error)


def adicionar_avaliacao(grupo: GrupoDesportivo):
    """Comando para adicionar uma avaliação do grupo"""
    nome = input("Insira o nome do desportista: ").strip()
    desportista = grupo.desportista_chamado(nome)
    if desportista is None:
        print("Desportista não existe")
    else:
        try:
            valor = float(input("Valor: "))
            grupo.adicionar_avaliacao(desportista.id, valor)
        except ValueError as error:
            print(error)


def listar_commandos(_):
    """Comando para listar os comandos"""
    print("Lista de comandos:")
    for cmd, _ in COMANDOS.items():
        print(f"- {cmd}")


COMANDOS: Dict[str, Callable] = {
    "adicionar_desportista": adicionar_desportista,
    "adicionar_avaliacao": adicionar_avaliacao,
    "visualizar": visualizar_desportistas,
    "ajuda": listar_commandos,
    "sair": None,
}


def main():
    """Função de entrada"""
    parar = False
    desportistas = ler_desportistas()
    avaliacoes = ler_avaliacoes()
    grupo = GrupoDesportivo(desportistas, avaliacoes)

    while not parar:
        cmd = input("Comando: ").strip()
        print("")
        if cmd not in COMANDOS:
            print("################")
            print("Comando Inválido")
            print("################\n")
            listar_commandos(None)
        elif cmd == "sair":
            parar = True
        else:
            COMANDOS.get(cmd)(grupo)
        print("")
    grupo.salvar()


if __name__ == "__main__":
    main()
