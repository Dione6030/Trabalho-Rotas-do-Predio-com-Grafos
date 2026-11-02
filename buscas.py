#BFS
from collections import deque
from grafo import carregar_grafo
from caminhos import reconstruir_caminho, mostrar_rota


def bfs(grafo, origem, destino):
    anterior = {origem: None}
    fila = deque([origem])
    while fila:
        v = fila.popleft()
        if v == destino:
            break
        for w, _peso in grafo[v]:
            if w not in anterior:
                anterior[w] = v
                fila.append(w)
    return anterior


def main():
    grafo = carregar_grafo("arestas.txt")
    origem, destino = "LABTEC", "BAN_MSC"

    if origem not in grafo or destino not in grafo:
        print("Origem ou destino não existe no grafo.")
        return

    caminho = reconstruir_caminho(bfs(grafo, origem, destino), destino)

    if caminho:
        mostrar_rota(grafo, caminho)
    else:
        print(f"Não existe rota de {origem} até {destino}.")


if __name__ == "__main__":
    main()

#DFS
from grafo import arestas
from caminhos import reconstruir_caminho, mostrar_rota


def dfs(grafo, origem, destino):
    anterior = {origem: None}
    _visitar(grafo, origem, destino, anterior)
    return anterior


def _visitar(grafo, no, destino, anterior):
    if no == destino:
        return True

    for vizinho, _peso in grafo[no]:
        if vizinho not in anterior:
            anterior[vizinho] = no
            if _visitar(grafo, vizinho, destino, anterior):
                return True

    return False


if __name__ == "__main__":
    origem, destino = "LABTEC", "BAN_MSC"

    anterior = dfs(arestas, origem, destino)
    caminho = reconstruir_caminho(anterior, destino)

    if caminho:
        mostrar_rota(arestas, caminho)
    else:
        print(f"Não há caminho de {origem} até {destino}.")

#Gulosa
import heapq
from collections import deque
from grafo import arestas
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

#Dijkstra
import heapq
from caminhos import mostrar_rota, reconstruir_caminho


def relaxar_vizinhos(grafo, atual, distancia, anterior, fila):
    for vizinho, peso in grafo[atual]:
        nova_distancia = distancia[atual] + peso
        if nova_distancia < distancia[vizinho]:
            distancia[vizinho] = nova_distancia
            anterior[vizinho] = atual
            heapq.heappush(fila, (nova_distancia, vizinho))


def dijkstra(grafo, origem, destino):
    distancia = {p: float("inf") for p in grafo}
    distancia[origem] = 0
    anterior = {origem: None}
    fila = [(0, origem)]
    finalizadas = set()

    while fila:
        _d, atual = heapq.heappop(fila)
        if atual in finalizadas:
            continue
        finalizadas.add(atual)
        if atual == destino:
            break
        relaxar_vizinhos(grafo, atual, distancia, anterior, fila)

    caminho = reconstruir_caminho(anterior, destino)
    return caminho, distancia[destino], len(finalizadas)


if __name__ == "__main__":
    from grafo import arestas

    origem, destino = "LABTEC", "BAN_MSC"
    caminho, custo, expandidas = dijkstra(arestas, origem, destino)

    if caminho:
        mostrar_rota(arestas, caminho)
        print(f"Nós finalizados: {expandidas}")
    else:
        print(f"Não existe rota entre {origem} e {destino}.")