from fastapi import FastAPI, HTTPException
from grafo import carregar_grafo

app = FastAPI()
grafo = carregar_grafo("arestas.txt")

@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    if porta not in grafo:
        raise HTTPException(404, "Porta não encontrada")
    return [{"porta": p, "peso": w}
        for p, w in grafo[porta]]