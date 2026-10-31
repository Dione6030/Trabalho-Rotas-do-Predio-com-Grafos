from collections import deque
from planta import carregar_grafo
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