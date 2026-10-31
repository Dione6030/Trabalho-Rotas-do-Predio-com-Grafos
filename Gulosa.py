import heapq
from collections import deque

from planta import arestas
from caminhos import reconstruir_caminho, mostrar_rota


def heuristica_por_saltos(grafo, destino):
    """h(no) = nº mínimo de arestas entre 'no' e o destino."""
    saltos = {destino: 0}
    fila = deque([destino])
    while fila:
        atual = fila.popleft()
        for vizinho, _peso in grafo[atual]:
            if vizinho not in saltos:
                saltos[vizinho] = saltos[atual] + 1
                fila.append(vizinho)
    return lambda no: saltos.get(no, float("inf"))


def heuristica_manhattan(coordenadas, destino):
    """h(no) = distância de Manhattan até o destino, usando (x, y) de cada nó."""
    xd, yd = coordenadas[destino]

    def h(no):
        x, y = coordenadas[no]
        return abs(x - xd) + abs(y - yd)

    return h


def gulosa(grafo, origem, destino, h):
    anterior = {origem: None}
    fronteira = [(h(origem), origem)]

    while fronteira:
        _, atual = heapq.heappop(fronteira)
        if atual == destino:
            return anterior
        for vizinho, _peso in grafo[atual]:
            if vizinho not in anterior:
                anterior[vizinho] = atual
                heapq.heappush(fronteira, (h(vizinho), vizinho))

    return anterior


if __name__ == "__main__":
    origem, destino = "LABTEC", "BAN_MSC"

    h = heuristica_por_saltos(arestas, destino)
    anterior = gulosa(arestas, origem, destino, h)
    caminho = reconstruir_caminho(anterior, destino)

    if caminho:
        mostrar_rota(arestas, caminho)
    else:
        print(f"Sem caminho de {origem} até {destino}")