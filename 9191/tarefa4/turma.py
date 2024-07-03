# Autor: Carlos Pinto Machado
# email: 7791966@formacao.iefp.pt

import sys
from statistics import mean
from typing import List, Dict, Tuple, Iterator
from operator import attrgetter, itemgetter

from dataclasses import dataclass

DISCIPLINAS = ["Português", "Matemática", "Ciências"]


@dataclass
class Aluno:
    id: int
    notas: Dict[str, int]

    def nota(self, disciplina: str) -> int:
        return self.notas.get(disciplina)

    def notas_valores(self) -> List[int]:
        return self.notas.values()


@dataclass
class Turma:
    alunos: List[Aluno] = None
    disciplinas: List[str] = None

    def notas_de(self, disciplina: str) -> Iterator[int]:
        return (aluno.nota(disciplina) for aluno in self.alunos)

    def notas_de_com_id(self, disciplina: str) -> Iterator[Tuple[int, int]]:
        return ((aluno.id, aluno.nota(disciplina)) for aluno in self.alunos)

    def medias_por_disciplina(self) -> List[Tuple[str, float]]:
        return [
            (disciplina, mean(self.notas_de(disciplina)))
            for disciplina in self.disciplinas
        ]

    def medias_dos_alunos(self) -> List[Tuple[int, float]]:
        return [(aluno.id, mean(aluno.notas_valores())) for aluno in self.alunos]

    def melhor_nota_por_disciplina(self) -> List[Tuple[str, int, int]]:
        return [
            (disciplina, *max(self.notas_de_com_id(disciplina), key=itemgetter(1)))
            for disciplina in self.disciplinas
        ]
    def pior_nota_por_disciplina(self) -> List[Tuple[str, int, int]]:
        return [
            (disciplina, *min(self.notas_de_com_id(disciplina), key=itemgetter(1)))
            for disciplina in self.disciplinas
        ]


def ler_aluno(id: int, disciplinas: List[str]) -> Aluno:
    notas = {}
    print(f"Avaliação do Aluno {id}:")
    for disciplina in disciplinas:
        nota = 0
        try:
            nota = int(input(f"Nota em {disciplina}: "))
            if not (0 <= nota <= 20):
                raise ValueError("Nota não está entre 0 e 20")
        except ValueError as error:
            print("[LER_ALUNO]: ", error)
            sys.exit(1)
        notas[disciplina] = nota
    return Aluno(id=id, notas=notas)


def ler_alunos(n: int, disciplinas: List[str]) -> Turma:
    alunos = [ler_aluno(i, disciplinas) for i in range(1, n + 1)]
    return Turma(alunos=alunos, disciplinas=disciplinas)

def imprime_medias_por_disciplina(turma: Turma) -> None:
    print("Resultados: ")
    for disciplina, media in turma.medias_por_disciplina():
        print(f"Média das notas em {disciplina}: {media:.2f}")

def imprime_medias_por_aluno(turma: Turma) -> None:
    print("Média das notas por aluno: ")
    for id, media in turma.medias_dos_alunos():
        print(f"- Aluno {id}: {media:.2f}")

def imprime_melhor_notas_por_disciplina(turma: Turma) -> None:
    print("Melhor nota por disciplina: ")
    for disciplina, id, nota in turma.melhor_nota_por_disciplina():
        print(f"- {disciplina}: Aluno {id} ({nota})")

def imprime_pior_notas_por_disciplina(turma: Turma) -> None:
    print("Pior nota por disciplina: ")
    for disciplina, id, nota in turma.pior_nota_por_disciplina():
        print(f"- {disciplina}: Aluno {id} ({nota})")

def main():
    n = 0
    print("Bem-vindo ao Sistema de Registo de Avaliação de Alunos\n")

    try:
        n = int(input("Por favor, insira o número de alunos que deseja avaliar: "))
        if n < 1:
            raise ValueError("Não é um número inteiro positivo")
    except ValueError as error:
        print("[NUMERO_DE_ALUNOS_INVALIDO]: ", error)
        sys.exit(1)

    turma = ler_alunos(n, DISCIPLINAS)
    print("")
    imprime_medias_por_disciplina(turma)
    print("")
    imprime_medias_por_aluno(turma)
    print("")
    imprime_melhor_notas_por_disciplina(turma)
    print("")
    imprime_pior_notas_por_disciplina(turma)


if __name__ == "__main__":
    main()
