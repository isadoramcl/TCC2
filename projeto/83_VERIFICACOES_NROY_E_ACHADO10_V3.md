# 83 — Verificações V-1, V-2, V-3 e Achado 10 na v3

29/09/2026. Somente pós-processamento dos quatro CSVs de ondas já existentes; nenhuma simulação, alteração de código, parâmetro ou operação Git. “V2” abaixo designa a evidência HM legada solicitada na comparação, não uma execução do núcleo MVP v2: o runner histórico usava Simulacao; o novo usa SimulacaoMVP. Arquivos de origem e hashes no manifesto anexo.

## V-1 — desenho e número de pontos aceitos

| Versão | Onda | Propostas | NROY | Aceitação |
|---|---:|---:|---:|---:|
| v2 | 1 | 400 | 40 | 10.00% |
| v2 | 2 | 400 | 115 | 28.75% |
| v3 | 1 | 400 | 46 | 11.50% |
| v3 | 2 | 400 | 63 | 15.75% |

Ambas usaram duas ondas de 400 propostas: 800 propostas por versão. A tabela final usa somente a onda 2: **115 pontos no legado e 63 na v3**, razão 1,83, não uma ordem de grandeza. Não somar os pontos das ondas para o N da tabela. A menor amostra v3 pode tornar seus extremos mais instáveis; não explica automaticamente a diferença. A falta de comparabilidade científica já decorre de espaço, verdade, núcleo e estimador de variância diferentes, não de uma diferença de ordem de grandeza do N.

## V-2 — a mesma medida de caixa, não volume geométrico do conjunto

| Versão | Caixa onda 1 / a priori | Caixa onda 2 / a priori |
|---|---:|---:|
| v2 | 17.3611% | 14.7987% |
| v3 | 62.9438% | 37.6899% |

A fórmula em ambos é produto das cinco amplitudes marginais dos pontos aceitos dividido pelo produto das cinco amplitudes a priori. O 14,8% legado JÁ era caixa envolvente (`04_gemeo_identico.py`, cálculo vol_final/vol_prior), assim como o 37,6899% novo. A comparação não sofre troca de definição, mas continua sem interpretação causal entre versões diferentes.

O **volume do conjunto NROY contínuo não é recuperável exatamente destes CSVs** sem uma regra adicional de interpolação/classificação do espaço não avaliado. A proporção aceita na primeira onda (10% e 11,5%) é uma estimativa amostral de ocupação sob o critério e desenho de cada versão; não é medida geométrica exata. Os 28,75% e 15,75% da segunda onda se referem à caixa reduzida onde aquela onda amostrou, não ao a priori inteiro. Não rotular nenhuma dessas proporções como o volume da caixa.

## V-3 — bootstrap dos pontos NROY finais

Foram reamostradas LINHAS completas, com reposição e mesmo tamanho N de cada versão, preservando a dependência entre dimensões. B=2000, semente-base 20260929, fluxos separados por versão; intervalo percentil [2,5%;97,5%], quantil linear. Faixas a priori fixas. Valores abaixo em porcentagem de contração da largura marginal.

| Parâmetro | Legado: estimativa [intervalo] | V3: estimativa [intervalo] |
|---|---:|---:|
| F_ancora | 36.77% [36.77%; 40.29%] | 12.95% [12.95%; 34.95%] |
| f_retrabalho | 5.99% [5.99%; 14.80%] | 13.32% [13.32%; 24.76%] |
| tau_sat | 10.88% [10.88%; 14.95%] | 41.55% [41.55%; 47.29%] |
| k_heuristico | 5.79% [5.79%; 10.03%] | — |
| k_analitico | — | 4.79% [4.79%; 14.58%] |
| mu_minimo | 70.35% [70.35%; 73.11%] | 10.24% [10.24%; 20.65%] |

O intervalo de mu_minimo na v3, **[10,24%;20,65%]**, exclui os **70,35%** históricos e não se sobrepõe ao intervalo legado **[70,35%;73,11%]**. Para tau_sat, [41,55%;47,29%] também não se sobrepõe a [10,88%;14,95%]. Tau_sat passou de “não identificado” para **parcialmente identificado**, não plenamente identificado.

**Limitação determinante do bootstrap pedido:** qualquer reamostra contém apenas pontos já observados; seu mínimo nunca diminui e seu máximo nunca aumenta. Portanto sua largura nunca excede a observada e sua contração nunca fica abaixo da estimativa original. Os limites inferiores iguais à estimativa, em todas as linhas, são consequência matemática disso. Estes são intervalos condicionais de reamostragem, não intervalos confiáveis para toda a incerteza dos extremos do NROY verdadeiro. Além disso, pontos aceitos de um desenho LHS adaptativo não são uma amostra independente de uma população fixa.

A conclusão suportada é: **a diferença não desaparece ao reamostrar os pontos aceitos disponíveis**. Não se pode concluir “a causa é mecânica” só porque os intervalos se separam: o bootstrap não inclui regiões não visitadas, ruído na decisão de aceitação, variabilidade do alvo sintético nem a escolha de outra realização LHS. Núcleo, verdade, parametrização e variância também mudaram. Reciprocamente, sobreposição não provaria que toda a mudança é ruído. Os números de exposição cognitiva fornecidos pela autora (7,92%/3,59%; mínimos 0,637/0,680) não foram reconferidos nesta análise e não são usados como prova causal; constituem uma hipótese compatível com a direção, sem fechar a magnitude.

## Achado 10 — crista e produto corretos

Na nuvem NROY final, Spearman entre F_ancora e f_retrabalho passou de **-0.839762** (115 pontos) para **-0.584341** (63 pontos). A associação negativa **persiste, mas enfraqueceu na amostra observada**; não desapareceu. Isso descreve uma crista empírica no conjunto aceito, não demonstra não identificabilidade estrutural.

A contração da largura de **F_ancora × f_retrabalho** passou de **74.6619%** para **49.5015%**. Usou-se a mesma faixa teórica do produto [0,015;0,200], amplitude 0,185. Na v3 o produto observado vai de **0.032832736** a **0.126255022**; no legado, de **0.057179849** a **0.104055413**. A contração v3 do produto, **49,50%**, continua maior que a de F_ancora (**12,95%**) e f_retrabalho (**13,32%**), mas é inferior aos **74,66%** históricos (o antigo texto arredondava 74,7%). No legado os fatores contraíam 36,77% e 5,99%.

Não trocar F_ancora por probabilidade efetiva de falha nesta frase. Maior contração do produto não prova que ele seja suficiente para substituir os dois fatores; a crista não foi “recuperada” por ajuste algum.

## Arquivos da análise

`outputs/diagnosticos/20260929_verificacoes_hm_v3/`: `ondas.csv`, `bootstrap_resumo.csv`, `bootstrap_replicas.csv` (20.000 linhas: 2 versões × 2000 réplicas × 5 dimensões), `achado10.csv`, `manifesto.json`. Leitura de todos os CSVs com float_precision='round_trip'. Spearman foi também conferido como Pearson dos postos. O parecer 81 e os outputs antigos permanecem intactos; este documento é seu complemento.
