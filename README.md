# Rotas do Prédio com Grafos

API em FastAPI que calcula rotas entre as portas do prédio do UniSenac Gonçalves, modelado como um grafo não direcionado e ponderado (arquivo `arestas.txt`). Algoritmos disponíveis: BFS, DFS, Busca Gulosa e Dijkstra.

## Integrantes

- Ítalo Valente
- Dione Pinheiro

## Unidade do peso

O peso de cada aresta é a distância entre duas portas em **metros (m)**.
O custo de uma rota é a soma dos pesos das arestas percorridas.

## Como rodar

Pré-requisito: Python 3 instalado.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn api:app --reload
```

No Mac/Linux, ative o venv com `source .venv/bin/activate`.

Execute o `uvicorn` dentro da pasta do projeto, o arquivo `arestas.txt` é lido pelo caminho relativo. Depois acesse a documentação interativa em http://127.0.0.1:8000/docs

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/portas` | Todas as portas do grafo |
| GET | `/vizinhos/{porta}` | Vizinhos de uma porta e o peso de cada aresta |
| GET | `/rota?origem=&destino=&algoritmo=` | Caminho, custo e visitados (`bfs`, `dfs`, `gulosa` ou `dijkstra`) |
| GET | `/comparar?origem=&destino=` | Roda os quatro algoritmos e indica o de menor custo |

Exemplo:

```
http://127.0.0.1:8000/rota?origem=LABTEC&destino=BAN_MSC&algoritmo=dijkstra
```

## Par de portas em que BFS e Dijkstra discordam

**LABTEC → BAN_MSC**

| Algoritmo | Caminho | Arestas | Custo | Visitados |
|-----------|---------|---------|-------|-----------|
| BFS | LABTEC → PATIO1 → CANTINA1 → CANTINA2 → PATIO2 → BAN_MSC | 5 | **47 m** | 22 |
| Dijkstra | LABTEC → LAB201 → LAB202 → LAB203 → BAN_FEM → PATIO2 → BAN_MSC | 6 | **33 m** | 12 |

**Por que discordam?**

O BFS explora o grafo por camadas e trata todas as arestas como se tivessem o mesmo custo. Por isso ele garante o caminho com **menos arestas** e não o **mais curto em metros**. Aqui, o trajeto pela cantina tem só 5 arestas, mas passa por trechos longos (LABTEC → PATIO1 = 13 m, CANTINA1 → CANTINA2 = 12 m e CANTINA2 → PATIO2 = 12 m), somando 47 m.

O Dijkstra leva os pesos em conta. O trajeto pelos laboratórios tem uma aresta a mais (6), mas cada trecho é curto (3 + 4 + 11 + 10 + 2 + 3 = 33 m), então o custo total é 14 m menor. O Dijkstra também precisou visitar menos nós (12 contra 22), porque encontrou o destino sem explorar as ramificações longas do grafo.

Conclusão: O BFS minimiza o número de arestas, e o Dijkstra minimiza a soma dos pesos, quando as arestas possuem pesos diferentes, os dois podem escolher caminhos distintos.