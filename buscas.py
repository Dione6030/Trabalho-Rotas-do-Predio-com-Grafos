import heapq
from collections import deque
from grafo import carregar_grafo, arestas
from caminhos import calcular_custo, reconstruir_caminho, mostrar_rota

#BFS

def bfs(grafo, origem, destino):
    anterior = {origem: None}       # de onde cheguei (a origem não tem anterior); também marca quem já foi descoberto
    fila = deque([origem])          # fila FIFO: explora por níveis, primeiro quem está a menos arestas da origem
    while fila:
        v = fila.popleft()          # tira o nó mais antigo da fila
        if v == destino:            # chegou no destino: pode parar
            break
        for w, _peso in grafo[v]:   # olha os vizinhos de v (o peso é ignorado: BFS conta arestas, não metros)
            if w not in anterior:   # só entra se ainda não foi descoberto
                anterior[w] = v     # guarda que cheguei em w vindo de v
                fila.append(w)      # w entra no fim da fila
    caminho = reconstruir_caminho(anterior, destino)   # volta do destino até a origem seguindo 'anterior'
    return caminho, calcular_custo(grafo, caminho), len(anterior)   # ["LABTEC", "PATIO1", ..., "BAN_MSC"], 47, 22 (descobertos)


def main():
    grafo = carregar_grafo("arestas.txt")
    origem, destino = "LABTEC", "BAN_MSC"

    if origem not in grafo or destino not in grafo:   # evita KeyError se o nome do ponto estiver errado
        print("Origem ou destino não existe no grafo.")
        return

    caminho, _, visitados = bfs(grafo, origem, destino)   # '_' = custo, não usado aqui (mostrar_rota recalcula)

    if caminho:                     # lista vazia = não existe rota
        print("\n=== BFS ===")
        mostrar_rota(grafo, caminho)
        print(f"Visitados: {visitados}")
    else:
        print(f"Não existe rota de {origem} até {destino}.")


if __name__ == "__main__":
    main()

#DFS

def dfs(grafo, origem, destino):
    anterior = {origem: None}       # de onde cheguei; também funciona como "já visitei"
    _visitar(grafo, origem, destino, anterior)   # preenche 'anterior' por recursão (não precisa do retorno True/False)
    caminho = reconstruir_caminho(anterior, destino)
    return caminho, calcular_custo(grafo, caminho), len(anterior)   # ["LABTEC", "PATIO1", ..., "BAN_MSC"], 47, 12


def _visitar(grafo, no, destino, anterior):
    if no == destino:               # caso base: achou o destino
        return True                 # True sobe pela pilha de chamadas avisando "pare de explorar"

    for vizinho, _peso in grafo[no]:        # tenta cada vizinho, um de cada vez, indo fundo antes de voltar
        if vizinho not in anterior:         # ignora quem já foi visitado (evita ciclos)
            anterior[vizinho] = no          # guarda que cheguei em vizinho vindo de no
            if _visitar(grafo, vizinho, destino, anterior):   # desce um nível; se achou lá embaixo...
                return True                 # ...repassa o True para cima e encerra a busca

    return False                    # becos sem saída: nenhum vizinho levou ao destino, então volta (backtracking)


if __name__ == "__main__":
    origem, destino = "LABTEC", "BAN_MSC"

    caminho, _, visitados = dfs(arestas, origem, destino)

    if caminho:
        print("\n=== DFS ===")
        mostrar_rota(arestas, caminho)
        print(f"Visitados: {visitados}")
    else:
        print(f"Não há caminho de {origem} até {destino}.")

#Gulosa

def heuristica_por_saltos(grafo, destino):
    """h(no) = nº mínimo de arestas entre 'no' e o destino."""
    saltos = {destino: 0}           # distância em arestas até o destino (o próprio destino está a 0)
    fila = deque([destino])         # BFS rodando "ao contrário": parte do destino e espalha para o resto do grafo
    while fila:
        atual = fila.popleft()
        for vizinho, _peso in grafo[atual]:
            if vizinho not in saltos:                   # primeira vez que chega = menor nº de saltos
                saltos[vizinho] = saltos[atual] + 1     # um salto a mais que o nó de onde veio
                fila.append(vizinho)
    return lambda no: saltos.get(no, float("inf"))      # nó que não alcança o destino vale infinito


def heuristica_manhattan(coordenadas, destino):
    """h(no) = distância de Manhattan até o destino, usando (x, y) de cada nó."""
    xd, yd = coordenadas[destino]   # posição do destino no mapa

    def h(no):
        x, y = coordenadas[no]      # posição do nó que está sendo avaliado
        return abs(x - xd) + abs(y - yd)    # distância "em quarteirões": só horizontal + vertical

    return h


def gulosa(grafo, origem, destino, h=None):
    if h is None:                   # se ninguém passou heurística, usa a de saltos
        h = heuristica_por_saltos(grafo, destino)

    anterior = {origem: None}       # de onde cheguei; também marca quem já foi descoberto
    fronteira = [(h(origem), origem)]   # heap ordenado só por h: sai primeiro quem "parece" mais perto do destino

    while fronteira:
        _, atual = heapq.heappop(fronteira)     # pega o nó com menor h (o peso das arestas não entra na decisão)
        if atual == destino:
            break
        for vizinho, _peso in grafo[atual]:
            if vizinho not in anterior:         # a primeira descoberta fica e nunca é corrigida (por isso pode não ser o menor custo)
                anterior[vizinho] = atual
                heapq.heappush(fronteira, (h(vizinho), vizinho))   # entra no heap com prioridade = h(vizinho)

    caminho = reconstruir_caminho(anterior, destino)
    return caminho, calcular_custo(grafo, caminho), len(anterior)   # ["LABTEC", "PATIO1", ..., "BAN_MSC"], 47, 11


if __name__ == "__main__":
    origem, destino = "LABTEC", "BAN_MSC"

    h = heuristica_por_saltos(arestas, destino)     # monta a heurística uma vez para este destino
    caminho, _, visitados = gulosa(arestas, origem, destino, h)

    if caminho:
        print("\n=== Busca Gulosa ===")
        mostrar_rota(arestas, caminho)
        print(f"Visitados: {visitados}")
    else:
        print(f"Sem caminho de {origem} até {destino}")

#Dijkstra

def relaxar_vizinhos(grafo, atual, distancia, anterior, fila):
    for vizinho, peso in grafo[atual]:
        nova_distancia = distancia[atual] + peso    # custo de chegar em vizinho passando por 'atual'
        if nova_distancia < distancia[vizinho]:     # achou um caminho melhor que o conhecido até agora?
            distancia[vizinho] = nova_distancia     # atualiza a menor distância conhecida
            anterior[vizinho] = atual               # e lembra que o melhor jeito de chegar é por 'atual'
            heapq.heappush(fila, (nova_distancia, vizinho))   # entra no heap com a nova prioridade


def dijkstra(grafo, origem, destino):
    distancia = {p: float("inf") for p in grafo}    # menor distância conhecida até cada ponto (infinito = ainda não alcançado)
    distancia[origem] = 0                           # chegar na origem custa 0
    anterior = {origem: None}                       # de onde cheguei
    fila = [(0, origem)]                            # heap de (distância, nó): sempre sai o mais barato
    finalizadas = set()                             # nós com distância definitiva (não melhora mais)

    while fila:
        _d, atual = heapq.heappop(fila)             # pega o nó de menor distância
        if atual in finalizadas:                    # entrada velha do heap (o nó já foi fechado por um caminho melhor)
            continue
        finalizadas.add(atual)                      # distância de 'atual' agora é definitiva
        if atual == destino:                        # destino finalizado = menor caminho garantido
            break
        relaxar_vizinhos(grafo, atual, distancia, anterior, fila)   # tenta melhorar a distância dos vizinhos

    caminho = reconstruir_caminho(anterior, destino)
    return caminho, distancia[destino], len(finalizadas)   # ["LABTEC", "LAB201", ..., "BAN_MSC"], 33, 12

if __name__ == "__main__":

    origem, destino = "LABTEC", "BAN_MSC"
    caminho, _, expandidas = dijkstra(arestas, origem, destino)

    if caminho:
        print("\n=== Dijkstra ===")
        mostrar_rota(arestas, caminho)
        print(f"Nós finalizados: {expandidas}")
    else:
        print(f"Não existe rota entre {origem} e {destino}.")