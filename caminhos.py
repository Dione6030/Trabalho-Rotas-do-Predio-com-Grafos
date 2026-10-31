def reconstruir_caminho(anterior, destino):
    if destino not in anterior:
        return []
    caminho = []
    no = destino
    while no is not None:
        caminho.append(no)
        no = anterior[no]
    caminho.reverse()
    return caminho


def peso_da_aresta(grafo, a, b):
    for vizinho, peso in grafo[a]:
        if vizinho == b:
            return peso


def listar_trechos(grafo, caminho):
    return [(a, b, peso_da_aresta(grafo, a, b)) for a, b in zip(caminho, caminho[1:])]


def calcular_custo(grafo, caminho):
    return sum(peso for _a, _b, peso in listar_trechos(grafo, caminho))


def mostrar_rota(grafo, caminho):
    acumulado = 0
    print(f"Trajeto de {caminho[0]} até {caminho[-1]}:\n")
    for i, (a, b, peso) in enumerate(listar_trechos(grafo, caminho), start=1):
        acumulado += peso
        print(f"  {i}. {a} -> {b}: {peso} m (acumulado: {acumulado} m)")
    print(f"\nCaminho: {' -> '.join(caminho)}")
    print(f"Custo total: {calcular_custo(grafo, caminho)} m")