from fastapi import FastAPI, HTTPException
from grafo import carregar_grafo
from buscas import bfs, dfs, gulosa, dijkstra

app = FastAPI(title="API de Rotas do UniSenac")
grafo = carregar_grafo("arestas.txt")

ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}

def validar_pontos(origem: str, destino: str):
    origem, destino = origem.upper(), destino.upper()
    if origem not in grafo or destino not in grafo:
        raise HTTPException(404, "Origem ou destino não existe no grafo.")
    return origem, destino

def executar(algoritmo: str, origem: str, destino: str):
    caminho, custo, visitados = ALGORITMOS[algoritmo](grafo, origem, destino)
    return {"caminho": caminho, "custo": custo, "visitados": visitados}

@app.get("/portas")
def portas():
    return list(grafo.keys())

@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    if porta not in grafo:
        raise HTTPException(404, "Porta não encontrada")
    return [{"porta": p, "peso": w}
        for p, w in grafo[porta]]

@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str):
    origem, destino = validar_pontos(origem, destino)
    algoritmo = algoritmo.lower()
 
    if algoritmo not in ALGORITMOS:
        raise HTTPException(400, "Opção inválida. Use 'bfs', 'dfs', 'gulosa' ou 'dijkstra'."
        )
    resultado = executar(algoritmo, origem, destino)
    if not resultado["caminho"]:
        raise HTTPException(404, f"Não existe rota de {origem} até {destino}.")
    return resultado

@app.get("/comparar")
def comparar(origem: str, destino: str):
    origem, destino = validar_pontos(origem, destino)
 
    resultados = {nome: executar(nome, origem, destino) for nome in ALGORITMOS}
 
    if not resultados["bfs"]["caminho"]:
        raise HTTPException(404, f"Não existe rota de {origem} até {destino}.")
 
    menor_custo = min(resultados, key=lambda nome: resultados[nome]["custo"])
    return {
        "origem": origem,
        "destino": destino,
        "resultados": resultados,
        "menor_custo": menor_custo,
    }