# Resposta numérica T-B2.3 e D1

> Leitura atual: [bloqueio de três vias e censura](52_DEADLOCK_DE_TRES_VIAS_E_CENSURA.md).
> Portão fechado sozinho não implica incompletude; nominal completo em ambos os braços.


Primeiro ponto sem incompletas: **tau_inicial=0,600001**. Igualdade em 0,60
continua com 36/36 incompletas. O limiar observado coincide com a desigualdade
estrita do portão (`tau > tau_min=0,60`), não com o número particular 0,25.
Malha finita não estima um limiar contínuo independente, mas inclui o ponto de
igualdade e seu vizinho superior. No controle só portão, 36/36 concluem;
no só rede, 0/36. Nenhuma seleção de novo tau nominal.

| tau_inicial | Incompletas/36 | Hiato sem confiança médio | N_req médio |
|---:|---:|---:|---:|
| 0.250000 | 36/36 | 106925.777778 | 0.000000 |
| 0.590000 | 36/36 | 106919.333333 | 0.000000 |
| 0.600000 | 36/36 | 106919.333333 | 0.000000 |
| 0.600001 | 0/36 | 14.361111 | 329.416667 |
| 0.610000 | 0/36 | 14.250000 | 329.416667 |
| 0.650000 | 0/36 | 3.583333 | 325.277778 |
| 0.800000 | 0/36 | 0.083333 | 325.833333 |
| 1.000000 | 0/36 | 0.083333 | 338.583333 |

Hiato e N_req são médias de contagens acumuladas por execução, não totais da
grade. Exposição temporal muda; proporção por oportunidade está no resumo
original. População: 36 casos selecionados por incompletude histórica.
Formulação publicável: **nesta amostra e configuração, a centralizada trava
com confiança inicial menor ou igual ao limiar de assistência, e a abertura
inicial do portão remove o bloqueio nos níveis testados**. Não generalizar para
todos os tau_sat/s_transicao ou instâncias a partir dessas 36.

## D1 — nominal nos dois arranjos

Adaptativa: **0.186604625**, esperado aproximado 0,190.

Centralizada: **0.221795485**, esperado aproximado 0,224.

384 execuções completas (192 por braço, 16 instâncias ×12 sementes). Média das
razões por execução TR/(E_plano+TR), não razão das médias. Nenhum parâmetro
ajustado para aproximar o esperado. ANTES/DEPOIS dos campos antigos, estados e
RNG: resíduo zero em 64 controles. Brutos: noturno_D1/nominal_384.csv.
