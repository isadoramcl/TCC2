# E1 — recálculo offline do gradiente por linhas de código

Script `src/nasa/05_faixas_complexidade.py` realmente reexecutado, com novas
saídas em `outputs/diagnosticos/noturno_E1/`. Dados: versão NASA D'' (Dpp) de
Shepperd arquivada em `data/raw/nasa_dpp_reference/` e base consolidada local;
SHA256 da base, dos 13 ARFF e do script publicados no manifesto. Não é a versão
PROMISE bruta. N=17.377 módulos, 3.040 defeituosos (17,4944%).

LOC foi dividido em quartis da própria base: cortes 10, 20 e 41 linhas. Isso é
uma decisão desta análise, não limite normativo externo. Mantida a alternativa
histórica por complexidade; nenhum parâmetro do simulador foi sobrescrito.

| Nível | Complexidade, frequência | LOC, frequência | Complexidade, ajustada por projeto | LOC, ajustada por projeto |
|---|---:|---:|---:|---:|
| baixa | 0,14700 | 0,06336 | 0,14876 | 0,07267 |
| média | 0,28452 | 0,12050 | 0,27293 | 0,12197 |
| alta | 0,34791 | 0,17974 | 0,33102 | 0,17419 |
| muito alta | 0,43881 | 0,34005 | 0,39422 | 0,30833 |

O gradiente por LOC tem números diferentes do de complexidade. Ambos são
monotônicos nesta base; contagens recompõem N e a taxa global. Sensibilidade de
cortes e leave-one-project-out foram reexecutados e arquivados, não copiados.
O script já contemplava ambos os eixos; a publicação atual registra a reexecução
independente sem sugerir que LOC foi implementado pela primeira vez.

Tamanho de módulo não é dificuldade cognitiva de tarefa de projeto nem prova
causal de risco individual. A alternativa não elimina transporte de construto.
Todos os controles do script passaram; três testes de identidade também.
