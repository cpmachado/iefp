# Autor: Carlos Pinto Machado
# email: 7791966@formacao.iefp.pt


# funções de operações
def soma(a: float, b: float) -> float:
    return a + b


def subtracao(a: float, b: float) -> float:
    return a - b


def multiplicacao(a: float, b: float) -> float:
    return a * b


def divisao(a: float, b: float) -> float:
    return a / b


OPERACOES = {
    "1": {"nome": "Soma", "func": soma},
    "2": {"nome": "Subtração", "func": subtracao},
    "3": {"nome": "Multiplicação", "func": multiplicacao},
    "4": {"nome": "Divisão", "func": divisao},
    "5": {"nome": "Sair"},
}

OPERACAO_SAIDA = "5"


# Input/Output
def imprime_menu():
    print("#############")
    print("#Calculadora#")
    print("#############")
    print("\n".join([f"{k}. {v.get('nome')}" for (k, v) in OPERACOES.items()]))


def main():
    continua = True
    while continua:
        imprime_menu()
        op = input("Escolha uma operação: ")

        if op == OPERACAO_SAIDA:
            continua = False
        elif op not in OPERACOES:
            print("Operação inválida")
        else:
            f = OPERACOES.get(op).get("func")
            a = float(input("Insira um número: "))
            b = float(input("Insira outro número: "))

            try:
                print(f"Resultado: {f(a, b)}")
            except ZeroDivisionError:
                print("Não pode dividir por 0")


if __name__ == "__main__":
    main()
