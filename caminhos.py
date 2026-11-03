def reconstruir_caminho(anterior, destino):
    if destino not in anterior:     # destino nunca foi alcançado pela busca: não existe rota
        return []
    caminho = []                    # vai sair na ordem inversa (destino -> origem)
    no = destino
    while no is not None:           # só a origem tem anterior None, então o loop para quando chega nela
        caminho.append(no)
        no = anterior[no]           # anda um passo para trás: de onde cheguei neste nó
    caminho.reverse()               # inverte para ficar origem -> destino
    return caminho                  # ["LABTEC", "LAB201", "LAB202"]


def peso_da_aresta(grafo, a, b):
    for vizinho, peso in grafo[a]:  # procura b entre os vizinhos de a
        if vizinho == b:
            return peso             # peso (em metros) da aresta a-b
                                    # se b não for vizinho de a, a função termina sem return e devolve None


def listar_trechos(grafo, caminho):
    # zip(caminho, caminho[1:]) forma pares de nós consecutivos: (1º, 2º), (2º, 3º), ...
    return [(a, b, peso_da_aresta(grafo, a, b)) for a, b in zip(caminho, caminho[1:])]   # [("LABTEC", "LAB201", 3), ("LAB201", "LAB202", 4)]


def calcular_custo(grafo, caminho):
    return sum(peso for _a, _b, peso in listar_trechos(grafo, caminho))   # soma só os pesos dos trechos (_a e _b não são usados); caminho vazio dá 0


def mostrar_rota(grafo, caminho):    # espera um caminho com pelo menos 1 nó (quem chama já confere se não está vazio)
    acumulado = 0                    # soma dos metros percorridos até o trecho atual
    print(f"Trajeto de {caminho[0]} até {caminho[-1]}:\n")    # primeiro e último nó do caminho
    for i, (a, b, peso) in enumerate(listar_trechos(grafo, caminho), start=1):   # start=1: numera os trechos a partir de 1
        acumulado += peso
        print(f"  {i}. {a} -> {b}: {peso} m (acumulado: {acumulado} m)")
    print(f"\nCaminho: {' -> '.join(caminho)}")                # LABTEC -> LAB201 -> LAB202
    print(f"Custo total: {calcular_custo(grafo, caminho)} m")  # tem que bater com o último acumulado