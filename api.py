from fastapi import FastAPI, HTTPException
from grafo import carregar_grafo
from buscas import bfs, dfs, gulosa, dijkstra    # importar não executa os testes dos blocos __main__ de buscas.py

app = FastAPI(title="API de Rotas do UniSenac")   # o título aparece na documentação automática (/docs)
grafo = carregar_grafo("arestas.txt")             # lê o arquivo uma vez, quando a API sobe (não a cada requisição)

ALGORITMOS = {                  # nome que vem na URL -> função que roda a busca
    "bfs": bfs,                 # todas têm a mesma assinatura (grafo, origem, destino) e o mesmo retorno (caminho, custo, visitados)
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}

def validar_pontos(origem: str, destino: str):
    origem, destino = origem.upper(), destino.upper()   # aceita "labtec" ou "LabTec": os nomes no grafo são todos maiúsculos
    if origem not in grafo or destino not in grafo:     # o grafo é um dict, então 'in' confere se o ponto existe
        raise HTTPException(404, "Origem ou destino não existe no grafo.")   # 404 = não encontrado
    return origem, destino                              # devolve os nomes já normalizados

def executar(algoritmo: str, origem: str, destino: str):
    caminho, custo, visitados = ALGORITMOS[algoritmo](grafo, origem, destino)   # busca a função no dict e chama (sem if/elif)
    return {"caminho": caminho, "custo": custo, "visitados": visitados}         # {"caminho": ["LABTEC", "LAB201", ..., "BAN_MSC"], "custo": 33, "visitados": 12}

@app.get("/portas")             # GET /portas
def portas():
    return list(grafo.keys())   # lista com o nome de todos os pontos do grafo

@app.get("/vizinhos/{porta}")   # GET /vizinhos/LABTEC  ({porta} vem no caminho da URL)
def vizinhos(porta: str):
    porta = porta.upper()
    if porta not in grafo:
        raise HTTPException(404, "Porta não encontrada")
    return [{"porta": p, "peso": w}
        for p, w in grafo[porta]]       # [{"porta": "PATIO1", "peso": 13}, {"porta": "LAB201", "peso": 3}]

@app.get("/rota")               # GET /rota?origem=LABTEC&destino=BAN_MSC&algoritmo=dijkstra  (parâmetros vêm depois do "?")
def rota(origem: str, destino: str, algoritmo: str):
    origem, destino = validar_pontos(origem, destino)
    algoritmo = algoritmo.lower()           # aceita "Dijkstra" ou "DIJKSTRA"
 
    if algoritmo not in ALGORITMOS:         # 400 = pedido inválido (erro de quem chamou a API)
        raise HTTPException(400, "Opção inválida. Use 'bfs', 'dfs', 'gulosa' ou 'dijkstra'."
        )
    resultado = executar(algoritmo, origem, destino)
    if not resultado["caminho"]:            # lista vazia = a busca terminou sem alcançar o destino
        raise HTTPException(404, f"Não existe rota de {origem} até {destino}.")
    return resultado                        # {"caminho": [...], "custo": 33, "visitados": 12}

@app.get("/comparar")           # GET /comparar?origem=LABTEC&destino=BAN_MSC
def comparar(origem: str, destino: str):
    origem, destino = validar_pontos(origem, destino)
 
    resultados = {nome: executar(nome, origem, destino) for nome in ALGORITMOS}   # roda os 4 algoritmos: {"bfs": {...}, "dfs": {...}, ...}
 
    if not resultados["bfs"]["caminho"]:    # se o BFS não achou, nenhum outro acha: basta olhar um
        raise HTTPException(404, f"Não existe rota de {origem} até {destino}.")
 
    menor_custo = min(resultados, key=lambda nome: resultados[nome]["custo"])   # nome do algoritmo de menor custo (em empate, o primeiro do dict)
    return {
        "origem": origem,
        "destino": destino,
        "resultados": resultados,           # o resultado completo de cada algoritmo
        "menor_custo": menor_custo,         # "dijkstra"
    }