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
    from planta import arestas

    origem, destino = "LABTEC", "BAN_MSC"
    caminho, custo, expandidas = dijkstra(arestas, origem, destino)

    if caminho:
        mostrar_rota(arestas, caminho)
        print(f"Nós finalizados: {expandidas}")
    else:
        print(f"Não existe rota entre {origem} e {destino}.")