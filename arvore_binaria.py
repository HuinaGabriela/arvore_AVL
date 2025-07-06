
# Árvore balanceada
# Esta implementação mantém a árvore sempre "equilibrada" para garantir buscas,
# inserções e remoções rápidas (O(log n)). A cada operação, a AVL verifica se
# a árvore está desbalanceada e, se necessário, faz rotações para reequilibrar.

import matplotlib.pyplot as plt
import networkx as nx
import timeit
import random

# Criar a classe do nó (Node)
class Node:
    def __init__(self, valor):
        self.valor = valor        # Valor do nó
        self.esquerda = None      # Filho à esquerda
        self.direita = None       # Filho à direita
        self.altura = 1           # alteração para o cálculo de balanceamento AVL


# Criar a classe da Árvore Binária
class Arvore_AVL:
    
    def __init__(self):
        self.raiz = None  # Começa vazia

    def inserir(self, valor):
        self.raiz = self._inserir_recursivo(self.raiz, valor)

    # balanceamento AVL
    def _inserir_recursivo(self, no, valor):
        if no is None:
            return Node(valor)

        if valor < no.valor:
            no.esquerda = self._inserir_recursivo(no.esquerda, valor)
        else:
            no.direita = self._inserir_recursivo(no.direita, valor)

        # Atualiza altura
        no.altura = 1 + max(self._get_altura(no.esquerda), self._get_altura(no.direita))

        # Calcula o fator de balanceamento
        fb = self._get_fb(no)

        # Casos de desbalanceamento (rotações)

        # Caso esquerda-esquerda
        if fb > 1 and valor < no.esquerda.valor:
            return self._rotacao_direita(no)

        # Caso direita-direita
        if fb < -1 and valor > no.direita.valor:
            return self._rotacao_esquerda(no)

        # Caso esquerda-direita
        if fb > 1 and valor > no.esquerda.valor:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        # Caso direita-esquerda
        if fb < -1 and valor < no.direita.valor:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no
    # Obtem a altura de um nó específico. Cálcula o fator de balanceamento (FB) e atualiza corretamente a altura de cada nó após inserções e rotações.
    def _get_altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _get_fb(self, no):
        return self._get_altura(no.esquerda) - self._get_altura(no.direita)

    def _rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita
        # Roda
        x.direita = y
        y.esquerda = T2

        # Atualiza altura
        y.altura = 1 + max(self._get_altura(y.esquerda), self._get_altura(y.direita))
        x.altura = 1 + max(self._get_altura(x.esquerda), self._get_altura(x.direita))

        return x

    def _rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda

        # Roda
        y.esquerda = x
        x.direita = T2

        # Atualiza altura
        x.altura = 1 + max(self._get_altura(x.esquerda), self._get_altura(x.direita))
        y.altura = 1 + max(self._get_altura(y.esquerda), self._get_altura(y.direita))

        return y

# Percorrer a árvore
    def em_ordem(self):
        self._em_ordem_recursivo(self.raiz)

    def _em_ordem_recursivo(self, no):
        if no is not None:
            self._em_ordem_recursivo(no.esquerda)
            print(no.valor)
            self._em_ordem_recursivo(no.direita)

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, no, valor):
        if no is None:
            return False  # Não encontrou
        if valor == no.valor:
            return True   # Encontrou!
        elif valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)
        else:
            return self._buscar_recursivo(no.direita, valor)

# Remover um nó da árvore
    def remover(self, valor):
        self.raiz = self._remover_recursivo(self.raiz, valor)

    def _remover_recursivo(self, no, valor):
        if no is None:
            return no

        if valor < no.valor:
            no.esquerda = self._remover_recursivo(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover_recursivo(no.direita, valor)
        else:
            # Encontrou o nó a remover
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda

            menor_valor = self._encontrar_minimo(no.direita)
            no.valor = menor_valor
            no.direita = self._remover_recursivo(no.direita, menor_valor)

        # Aqui entra o rebalanceamento após a remoção
        no.altura = 1 + max(self._get_altura(no.esquerda), self._get_altura(no.direita))
        fb = self._get_fb(no)

        # Casos de rotação
        if fb > 1 and self._get_fb(no.esquerda) >= 0:
            return self._rotacao_direita(no)

        if fb > 1 and self._get_fb(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        if fb < -1 and self._get_fb(no.direita) <= 0:
            return self._rotacao_esquerda(no)

        if fb < -1 and self._get_fb(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def _encontrar_minimo(self, no):
        while no.esquerda is not None:
            no = no.esquerda
        return no.valor

# Visualizar a árvore (de forma simples)
    def imprimir(self):
        self._imprimir_recursivo(self.raiz, 0)

    def _imprimir_recursivo(self, no, nivel):
        if no is not None:
            self._imprimir_recursivo(no.direita, nivel + 1)
            print('    ' * nivel + str(no.valor))
            self._imprimir_recursivo(no.esquerda, nivel + 1)

# calcular a altura da árvore inteira
    def altura(self):
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, no):
        if no is None:
            return 0
        altura_esquerda = self._altura_recursiva(no.esquerda)
        altura_direita = self._altura_recursiva(no.direita)
        return 1 + max(altura_esquerda, altura_direita)
    
    def exportar_grafico(self, titulo="Árvore AVL"):
        G = nx.DiGraph()
        pos = {}
        self._adicionar_nos_grafico(self.raiz, G, pos)

        plt.figure(figsize=(10, 5))
        nx.draw(
            G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=1000,
            font_size=10,
            arrows=True,
            arrowstyle='-|>',
            arrowsize=20
        )
        plt.title(titulo)
        plt.show()

    def _adicionar_nos_grafico(self, no, G, pos, x=0, y=0, dx=1.0):
        if no is None:
            return
        G.add_node(no.valor)
        pos[no.valor] = (x, y)
        if no.esquerda:
            G.add_edge(no.valor, no.esquerda.valor)
            self._adicionar_nos_grafico(no.esquerda, G, pos, x - dx, y - 1, dx / 2)
        if no.direita:
            G.add_edge(no.valor, no.direita.valor)
            self._adicionar_nos_grafico(no.direita, G, pos, x + dx, y - 1, dx / 2)

# Teste
def testar_arvore(valores, remover_valor=None, buscar_valores=[]):
    print("\n--- TESTE COM VALORES:", valores, "---")
    
    arvore = Arvore_AVL()

    for v in valores:
        arvore.inserir(v)

    print("\nValores em ordem (em_ordem):")
    arvore.em_ordem()

    for val in buscar_valores:
        encontrado = arvore.buscar(val)
        print(f"\nBuscar {val}: {'Encontrado' if encontrado else 'Não encontrado'}")

    if remover_valor is not None:
        print(f"\nRemovendo o valor {remover_valor} da árvore...")
        arvore.remover(remover_valor)
        print("Após remoção (em_ordem):")
        arvore.em_ordem()

    print("\nÁrvore visualizada:")
    arvore.imprimir()

    print("\nAltura da árvore:", arvore.altura())

    # Gerar gráfico
    arvore.exportar_grafico("arvore_teste")
    print("-" * 40)

def medir_desempenho(valores, remover_valores=[]):
    arvore = Arvore_AVL()

    print("\n--- MEDINDO DESEMPENHO ---")

    # Medir tempo de inserção
    tempo_insercao = timeit.timeit(
        stmt=lambda: [arvore.inserir(v) for v in valores],
        number=1
    )
    print(f"Tempo de inserção de {len(valores)} valores: {tempo_insercao:.6f} segundos")

    # Medir tempo de remoção
    tempo_remocao = timeit.timeit(
        stmt=lambda: [arvore.remover(v) for v in remover_valores],
        number=1
    )
    print(f"Tempo de remoção de {len(remover_valores)} valores: {tempo_remocao:.6f} segundos")

    print(f"Altura final da árvore: {arvore.altura()}")
    print("-" * 40)



testar_arvore(
    valores=[10, 5, 15, 2, 7, 20],
    remover_valor=5,
    buscar_valores=[7, 100]
)

# # Teste com dados em ordem (desbalanceado em árvore binária simples, balanceado em AVL)
# testar_arvore(
#     valores=[1, 2, 3, 4, 5, 6, 7],
#     remover_valor=3,
#     buscar_valores=[4]
# )

# # Teste com valores aleatórios
# testar_arvore(
#     valores=[50, 30, 70, 20, 40, 60, 80],
#     remover_valor=70,
#     buscar_valores=[80, 100]
# )

# Medir desempenho com muitos elementos
valores_teste = random.sample(range(1, 10001), 1000)  # 1000 valores únicos aleatórios de 1 a 10000
valores_remover = random.sample(valores_teste, 200)   # Remove 200 deles
medir_desempenho(valores_teste, remover_valores=valores_remover)
