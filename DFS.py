from planta import arestas
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
    origem, destino = "LABTEC", "LAB203"

    anterior = dfs(arestas, origem, destino)
    caminho = reconstruir_caminho(anterior, destino)

    if caminho:
        mostrar_rota(arestas, caminho)
    else:
        print(f"Não há caminho de {origem} até {destino}.")