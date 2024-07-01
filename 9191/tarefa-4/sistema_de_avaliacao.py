# Autor: Carlos Pinto Machado
# email: 7791966@formacao.iefp.pt

import sys
from statistics import mean
from typing import Self, List, Dict

from dataclasses import dataclass

DISCIPLINAS = ["Português", "Matemática", "Ciências"]


@dataclass
class Aluno:
    id: int
    notas: Dict[str, int]

    def media(self) -> float:
        return mean(self.notas.values())

    @staticmethod
    def ler_aluno(id: int, disciplinas: List[str] = DISCIPLINAS) -> Self:
        notas = {}
        print(f"\nAvaliação do Aluno {id}:")
        for disciplina in disciplinas:
            try:
                nota = int(input(f"- Nota em {disciplina}: "))
                if nota < 0:
                    raise ValueError("Nota < 0")
                notas[disciplina] = nota
            except ValueError as error:
                print(f"Nota Inválida: {error}")
                sys.exit(1)
        return Aluno(id, notas)


@dataclass
class Turma:
    nome: str
    alunos: List[Aluno]

    def imprimir_medias_por_disciplina(self):
        medias = [
            (disciplina, mean(aluno.notas.get(disciplina) for aluno in self.alunos))
            for disciplina in DISCIPLINAS
        ]
        print("\nResultados: ")
        for disciplina, media in medias:
            print(f"Média das notas em {disciplina}: {media:.2f}")

    def imprimir_medias_por_aluno(self):
        print("\nMédia das notas por aluno: ")
        for aluno in self.alunos:
            print(f"Aluno {aluno.id}: {aluno.media(): .2f}")

    def imprimir_melhor_nota_por_disciplina(self):
        print("\nMelhor nota por disciplina: ")
        notas = [
            (
                disciplina,
                max(self.alunos, key=(lambda aluno: aluno.notas.get(disciplina))),
            )
            for disciplina in DISCIPLINAS
        ]
        for disciplina, aluno in notas:
            id = aluno.id
            nota = aluno.notas.get(disciplina)
            print(f"- {disciplina}: Aluno {aluno.id} ({nota})")

    def imprimir_pior_nota_por_disciplina(self):
        print("\nPior nota por disciplina: ")
        notas = [
            (
                disciplina,
                min(self.alunos, key=(lambda aluno: aluno.notas.get(disciplina))),
            )
            for disciplina in DISCIPLINAS
        ]
        for disciplina, aluno in notas:
            id = aluno.id
            nota = aluno.notas.get(disciplina)
            print(f"- {disciplina}: Aluno {aluno.id} ({nota})")

    @staticmethod
    def ler_alunos(n: int) -> Self:
        nome = "X"
        alunos = [Aluno.ler_aluno(i) for i in range(1, n + 1)]
        return Turma(nome, alunos)


def is_natural(n: int) -> bool:
    return type(n) is int and n >= 1


def main():
    n = 0
    print("Bem-vindo ao Sistema de Registo de Avaliação de Alunos\n")

    try:
        n = int(input("Por favor, insira o número de alunos que deseja avaliar: "))
        if not is_natural(n):
            raise ValueError("Não é um número inteiro positivo")
    except ValueError as error:
        print("[NUMERO_DE_ALUNOS_INVALIDO]: ", error)
        sys.exit(1)

    turma = Turma.ler_alunos(n)
    turma.imprimir_medias_por_disciplina()
    turma.imprimir_medias_por_aluno()
    turma.imprimir_melhor_nota_por_disciplina()
    turma.imprimir_pior_nota_por_disciplina()


if __name__ == "__main__":
    main()
