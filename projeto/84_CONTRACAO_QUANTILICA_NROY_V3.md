# 84 — Contração por larguras quantílicas do NROY (V-4)

29/09/2026. Pós-processamento dos CSVs existentes; nenhum código do projeto alterado, nenhuma nova simulação ou operação Git. Este parecer complementa 81 e 83. “V2 histórica” designa o HM legado disponível na fase v2, executado pelo núcleo Simulacao, e não uma nova validação do MVP v2.

## Retirada do teste anterior

O bootstrap de max−min do V-3/parecer 83 fica **retirado como teste discriminante de incerteza das contrações**. Os arquivos antigos permanecem como registro, sem apagar evidência. A própria restrição dos extremos impede que uma reamostra tenha largura superior à observada. Os valores pontuais max−min continuam apresentados apenas como descrição comparativa.

## Definição e desenho do V-4

Para p inferior e superior, C=1−(q_superior(NROY)−q_inferior(NROY))/(q_superior(prior)−q_inferior(prior)).

A priori é a distribuição **uniforme contínua declarada em cada faixa [a,b]**: q_p=a+p(b−a). Assim, a largura 5–95% do prior é 0,90(b−a), e a interquartil é 0,50(b−a). Não se usou a largura completa no denominador nem os quantis empíricos da amostra de propostas. Por exemplo, mu_minimo tem faixa [0,40;0,70], largura 5–95% 0,27 e IQR 0,15 nas duas versões.

Amostras: 115 pontos aceitos na onda 2 histórica, 63 na v3. B=2000 réplicas por versão, linhas completas com reposição e N original, mantendo associações entre dimensões. Mesmos índices de reamostragem nas duas larguras. Semente-base 20260929, SeedSequence([20260929,4,índice_da_versão]). Quantis NumPy com interpolação linear; intervalos percentis 2,5–97,5%. Sem truncar contrações negativas.

## Estimativas e intervalos percentis (porcentagem)

| Versão | Parâmetro | Max−min | q95−q05 [intervalo] | IQR [intervalo] |
|---|---|---:|---:|---:|
| v2 | F_ancora | 36.77% | 37.18% [34.19%; 42.88%] | 35.19% [25.01%; 46.59%] |
| v2 | f_retrabalho | 5.99% | 17.53% [7.83%; 24.62%] | 29.45% [13.66%; 43.64%] |
| v2 | tau_sat | 10.88% | 9.14% [6.84%; 15.53%] | 7.10% [-11.29%; 23.74%] |
| v2 | k_heuristico | 5.79% | 5.35% [1.45%; 11.51%] | 7.47% [-7.10%; 25.62%] |
| v2 | mu_minimo | 70.35% | 72.51% [70.93%; 75.71%] | 70.33% [66.12%; 75.53%] |
| v3 | F_ancora | 12.95% | 34.11% [16.59%; 46.34%] | 37.43% [27.75%; 51.98%] |
| v3 | f_retrabalho | 13.32% | 17.82% [7.47%; 32.45%] | 22.45% [8.38%; 48.32%] |
| v3 | tau_sat | 41.55% | 42.55% [37.75%; 49.41%] | 52.68% [27.04%; 66.26%] |
| v3 | k_analitico | 4.79% | 9.23% [0.33%; 17.38%] | -3.29% [-20.52%; 27.61%] |
| v3 | mu_minimo | 10.24% | 14.40% [7.03%; 26.42%] | 31.41% [8.42%; 48.05%] |

## Resultado para mu_minimo

Com q95−q05, a contração cai de **72,51% [70,93%;75,71%]** para **14,40% [7,03%;26,42%]**. Com IQR, cai de **70,33% [66,12%;75,53%]** para **31,41% [8,42%;48,05%]**. Os intervalos não se sobrepõem em nenhuma medida. A diferença pontual é aproximadamente −58,11 pontos percentuais na largura 5–95% e −38,92 pontos na IQR.

**A perda de concentração marginal de mu_minimo na nuvem v3 persiste e não depende exclusivamente dos dois pontos extremos.** A concordância das duas estatísticas reforça essa constatação descritiva. Sua magnitude, porém, depende da largura escolhida: a estimativa v3 muda de 14,40% para 31,41%. Não transportar silenciosamente os rótulos de identificabilidade do critério max−min para outro estimador. Os dados não autorizam declarar que mu_minimo se tornou estruturalmente não identificável.

Tau_sat também muda de concentração nas duas estatísticas: 9,14% para 42,55% (5–95%) e 7,10% para 52,68% (IQR). Outros resultados são sensíveis ao estimador: F_ancora na v3 passa de 12,95% por extremos para 34,11% por 5–95% e 37,43% por IQR. Isso recomenda apresentar as medidas, em vez de eleger um único rótulo como propriedade intrínseca do modelo.

Contração negativa é permitida: por exemplo IQR de k_analitico v3 = **−3,29%**. Significa que a largura interquartil observada excede a IQR do prior uniforme, não que os pontos estejam fora da faixa a priori. Não foi corrigida ou cortada em zero.

## O que o resultado não demonstra

A hipótese de menor exposição da v3 ao fundo da escala cognitiva é **compatível com a direção** e a persistência da queda sob larguras robustas. Os números de exposição fornecidos pela autora não foram recalculados aqui e não constituem uma explicação causal demonstrada por esta análise. Ela tampouco separa alteração da drenagem, núcleo, verdade sintética, dimensão livre e estimador de variância usados no HM.

O bootstrap quantílico evita a degenerescência exata de max−min, mas permanece condicionado aos pontos aceitos disponíveis. Não inclui outra realização do LHS, erro na classificação NROY, variação da pseudo-observação ou regiões não amostradas; q05 e q95 com N=63 ainda dependem de poucos pontos de cauda. Por isso, intervalos separados sustentam a diferença descritiva nesta análise, não uma decomposição de mecanismos. Se a diferença desaparecesse sob um estimador, isso tampouco tornaria automaticamente a tabela histórica uma descrição válida da v3.

## Ressalva independente sobre volume e denominadores

Os 14,7987% históricos e 37,6899% da v3 são ambos volumes de CAIXAS ENVOLVENTES, divididos pelo volume do respectivo a priori. Mas **a dimensão k_heuristico [0,06;0,16] foi substituída por k_analitico [0,02;0,08]**. O produto das amplitudes a priori mudou de **0,0021 para 0,00126**, além de mudar o significado físico da coordenada. Portanto, “fração do a priori” tem denominadores diferentes e mede espaços científicos diferentes. A mudança de 14,8% para 37,69% não deve ser apresentada como aumento comparável do volume NROY do mesmo problema, independentemente do resultado do V-4. Para mu_minimo isoladamente, ao contrário, a faixa [0,40;0,70] e seus denominadores quantílicos foram mantidos.

## Evidências e preservação

`outputs/diagnosticos/20260929_larguras_quantilicas_hm/`: `contracoes_lado_a_lado.csv`, `bootstrap_replicas.csv` (40000 linhas: 2 versões × 2000 réplicas × 5 parâmetros × 2 larguras), `manifesto.json`. Leituras dos CSVs com float_precision='round_trip'; hashes das duas fontes conferidos antes/depois. Nenhum resultado anterior sobrescrito. O bootstrap do V-3 permanece arquivado, mas não sustenta a interpretação atual.
