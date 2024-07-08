"""gestor_produto.py: Sistema de Gestão de Produtos
"""

import csv
from dataclasses import dataclass, astuple
from typing import List, Any, Dict, Callable, Iterator
from operator import attrgetter
from statistics import mean


@dataclass(frozen=True, order=True)
class Preco:
    """Representação de uma Preço"""

    id: int
    produto_id: int
    valor: float


@dataclass(frozen=True, order=True)
class Produto:
    """Representação de um Produto"""

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


def ler_produtos(filename: str = "produtos.csv") -> List[Produto]:
    """Lê produtos de um ficheiro"""
    return [
        Produto(int(produto_id), nome) for produto_id, nome in ler_lista_tipo(filename)
    ]


def ler_precos(filename: str = "precos.csv") -> List[Preco]:
    """Lê preços de um ficheiro"""
    return [
        Preco(int(preco_id), int(produto_id), float(valor))
        for preco_id, produto_id, valor in ler_lista_tipo(filename)
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


def escrever_produtos(elementos: List[Produto], filename: str = "produtos.csv"):
    """Escreve um csv com produtos"""
    return escrever_lista_tipo(filename, elementos, astuple, ("id", "nome"))


def escrever_precos(elementos: List[Preco], filename: str = "precos.csv"):
    """Escreve um csv com avaliacões"""
    return escrever_lista_tipo(
        filename, elementos, astuple, ("id", "produto_id", "valor")
    )


@dataclass
class GestorStock:
    """Representação de produtos e preços e interoperabilidade entre ambos"""

    produtos: List[Produto]
    precos: List[Preco]

    def adicionar_produto(self, nome):
        """Adiciona um produto ao gestor"""
        if nome in map(attrgetter("nome"), self.produtos):
            raise UserWarning("Produto já existe?")
        produto_id = 1 + max(map(attrgetter("id"), self.produtos), default=0)
        produto = Produto(produto_id, nome)
        self.produtos.append(produto)
        return produto

    def adicionar_preco(self, produto_id, valor):
        """Adiciona uma preço ao gestor"""
        preco_id = max(map(attrgetter("id"), self.precos), default=0) + 1
        preco = Preco(preco_id, produto_id, valor)
        self.precos.append(preco)
        return preco

    def produto_chamado(self, nome):
        """Retorna um produto de um dado nome, assumindo que seja como um id único"""
        return next(
            (produto for produto in self.produtos if produto.nome == nome), None
        )

    def precos_de_produto(self, produto: Produto):
        """Retorna um iterador para preços de um produto"""
        return [preco for preco in self.precos if preco.produto_id == produto.id]

    def salvar(
        self,
        ficheiro_produtos: str = "produtos.csv",
        ficheiro_precos: str = "precos.csv",
    ):
        """Salva Stock para csvs"""
        escrever_produtos(self.produtos, ficheiro_produtos)
        escrever_precos(self.precos, ficheiro_precos)


def ver_produto(gestor: GestorStock, produto: Produto):
    """Visualiza um único produto de um gestor"""
    print(f"Nome: {produto.nome}")
    print(f"Id: {produto.id}")
    precos = gestor.precos_de_produto(produto)
    if len(precos) > 0:
        print("Preços:")
        for preco in precos:
            print(f" - id: {preco.id}")
            print(f" - valor: {preco.valor: g}")


def ver_produtos(gestor: GestorStock):
    """Comando para ver todos os produtos do gestor"""
    print("Lista de produtos:\n")
    for produto in gestor.produtos:
        ver_produto(gestor, produto)
        print("")


def adicionar_produto(gestor: GestorStock):
    """Comando para adicionar um produto do gestor"""
    nome = input("Insira o nome do produto: ").strip().lower()
    try:
        produto = gestor.adicionar_produto(nome)
        print(f"Criado Produto {produto.id}: {produto.nome}")
    except UserWarning as error:
        print(error)


def adicionar_preco(gestor: GestorStock):
    """Comando para adicionar uma preço do gestor"""
    nome = input("Insira o nome do produto: ").strip()
    produto = gestor.produto_chamado(nome)
    if produto is None:
        print("Produto não existe")
    else:
        try:
            valor = float(input("Preço: "))
            if valor < 0:
                raise ValueError("Preço não pode ser negativo")
            gestor.adicionar_preco(produto.id, valor)
        except ValueError as error:
            print(error)


def media_de_produto(gestor: GestorStock):
    """Comando para calcular média de preços de um produto"""
    nome = input("Nome de produto: ")
    produto = gestor.produto_chamado(nome)
    if produto is None:
        print("Produto inexistente!")
    else:
        precos = gestor.precos_de_produto(produto)
        media = mean(map(attrgetter('valor'), precos)) if len(precos) > 0 else 0
        print(f"Média de preços de {nome}: {media: .2f}")


def listar_commandos(_):
    """Comando para listar os comandos"""
    print("Lista de comandos:")
    for cmd, _ in COMANDOS.items():
        print(f"- {cmd}")


COMANDOS: Dict[str, Callable] = {
    "adicionar produto": adicionar_produto,
    "adicionar preço a um produto": adicionar_preco,
    "ver produtos": ver_produtos,
    "calcular média de preços de um produto": media_de_produto,
    "ajuda": listar_commandos,
    "sair": None,
}


def main():
    """Função de entrada"""
    parar = False
    produtos = ler_produtos()
    precos = ler_precos()
    gestor = GestorStock(produtos, precos)

    while not parar:
        cmd = input("Comando: ").strip().lower()
        print("")
        if cmd not in COMANDOS:
            print("################")
            print("Comando Inválido")
            print("################\n")
            listar_commandos(None)
        elif cmd == "sair":
            parar = True
        else:
            COMANDOS.get(cmd)(gestor)
        print("")
    gestor.salvar()


if __name__ == "__main__":
    main()
