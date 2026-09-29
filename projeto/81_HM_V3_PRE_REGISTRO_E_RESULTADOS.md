# 81 — HM e cobertura interna da v3

## Pré-registro (antes de qualquer execução deste experimento)

Data UTC: 2026-09-28T19:15:13.670298+00:00. Autorização: instrução da autora após o parecer 80. Resultados pendentes neste registro inicial.

[DEC] Espaço 5D: F_ancora [0,05;0,25], f_retrabalho [0,30;0,80], tau_sat [0,70;1,40], **k_analitico [0,02;0,08]**, mu_minimo [0,40;0,70]. Em toda proposta e na verdade, k_heuristico=k_analitico por atribuição do mesmo float; controle por float.hex(). k_fuga permanece 0,10.

[DEC] Verdade: F_ancora=0,180; f_retrabalho=0,420; tau_sat=0,850; **k_analitico=0,065**; mu_minimo=0,620. O coeficiente 0,065 ocupa 75% da faixa nova, mesma posição relativa de (0,135−0,06)/(0,16−0,06)=75% no desenho antigo. Não está no centro 0,05, não é extremo e foi escolhido sem executar o novo desenho. Nenhuma faixa será adaptada para melhorar identificabilidade.

Núcleo: SimulacaoMVP com opções de config/mvp.yaml (v3), parâmetros e derivados atuais; instrumentação por tarefa desligada apenas para reduzir armazenamento. Cenário adaptativa. Duas instâncias fixas selecionadas pelo mesmo espaçamento do runner 04; 4 sementes por proposta, 10 para o alvo. Duas ondas de 400 pontos LHS, semente de desenho 20260905 em cada onda, como no histórico; a segunda usa a caixa envolvente dos pontos com I_max<=3 da primeira. Se não houver pontos aceitos, registrar NROY vazio e não inventar faixa para a segunda onda. Os identificadores concretos das instâncias serão congelados no manifesto antes de simular.

Estimando interno: média esperada dos quatro observáveis sobre o conjunto fixo das duas instâncias, variando a aleatoriedade dos agentes. Cada bloco é a média das duas instâncias; V_obs e V_sim são variâncias amostrais dessas médias divididas pelo número de blocos (10 e 4). O HM antigo usava variância de execuções agrupadas: esta diferença também impede comparação direta. Vetor interno preservado: taxa_omissao (proporção de tarefas), atraso_relativo (makespan/CPM sem recursos, adimensional), retrabalho_sobre_plano (TR/esforço planejado) e E_total (razão contábil interna, dependente da convenção TL). E_total NÃO é observável para calibração externa; atraso não é crescimento do prazo contratual. O experimento verifica o procedimento internamente, não estima V_obs externo.

Cobertura: B=500, em cada réplica 10 blocos de observação e 4 de predição independentes; duas instâncias por bloco. Sementes 10000000+28*b+offset+2*bloco+i, offset 0 para observação e 20 para predição. I_j=abs(z_j-f_j)/sqrt(V_obs,j+V_sim,j); V_mod=0, sem ajuste. Denominador zero: I=0 se diferença zero, infinito caso contrário. Reportar I_max>3, IC95 Wilson, distância do nominal 5%, p95 de I_max e contagens de censura. Corte 3 é marginal, não garantia conjunta de 95%. Nenhuma escolha posterior de pseudo-observação.

Critério de validade (não de beleza da tabela): zero violações em TODAS as execuções; igualdade bit a bit dos coeficientes em TODA proposta; preservar todas as saídas, incluindo resultados desfavoráveis. Execução incompleta será explicitamente registrada e impedirá interpretação irrestrita. Identificabilidade é descritiva, sem passou/reprovou; reportar amplitudes e contrações sem otimizar faixas. Nenhuma mudança de V_mod para fazer o verdadeiro passar.

Comparação: resultados v3 ao lado dos históricos, sem interpretar diferenças de espaço a priori, dinâmica e estimador de variância como melhoria. A retirada de k_heuristico é POR DERIVAÇÃO, não por falta de dados. outputs/ antigos não serão sobrescritos. HM/gêmeo 6420 execuções, cobertura 14000, total previsto 20420. Avaliação adicional do vetor verdadeiro com quatro sementes independentes: +8 (20428), registrada aqui antes da execução para testar I conjunto, além das projeções marginais.

Plano: escrever teste de derivação com controle negativo; implementar runner versionado e saídas exclusivas; testar; congelar código/configuração/desenho; executar alvo, ondas e cobertura; auditar os CSVs com código de análise independente; completar inventário nominal-v3/histórico/não executado por arquivo; publicar resultados sem Git.


## Resultados finais — fechamento em 29/09/2026

**Execução válida nos critérios pré-registrados:** 34.428/34.428 completas, zero violações, derivação hexadecimal respeitada em todas as execuções. **A identificabilidade é descritiva: k_analitico não ficou identificado neste desenho.** Nenhuma faixa, parâmetro, pseudo-observação, corte ou V_mod foi alterado em resposta aos resultados.

### Revisão durante a execução e cobertura principal

A revisão independente detectou que a cobertura herdada usa sementes diferentes entre instâncias, enquanto o HM pareia a semente nas duas. Essa diferença de covariância impede atribuir a primeira taxa ao HM exato. O pré-registro complementar [81A](81A_COBERTURA_PAREADA_PRE_REGISTRO.md) foi escrito antes de rodar a cobertura pareada e antes de consultar a taxa inicial. Ela foi definida como **principal por correspondência de desenho**, não por apresentar uma taxa conveniente. As duas séries de 500 réplicas estão preservadas, sem seleção de réplicas. O complemento acrescentou 14.000 execuções ao orçamento original; não foram feitas novas ondas de HM.

### Controles e custo observado

| Etapa | Execuções | Completas | Violações |
|---|---:|---:|---:|
| Alvo sintético | 20 | 20 | 0 |
| Predição independente no verdadeiro | 8 | 8 | 0 |
| Onda 1 | 3.200 | 3.200 | 0 |
| Onda 2 | 3.200 | 3.200 | 0 |
| Cobertura com instâncias independentes | 14.000 | 14.000 | 0 |
| Cobertura pareada principal | 14.000 | 14.000 | 0 |
| **Total científico** | **34.428** | **34.428** | **0** |

- Teste de derivação sobre 400 propostas de teste, extremos e verdade; controle negativo de 1 ULP rejeitado. Na execução e na auditoria, verificação de TODOS os coeficientes, incluindo as 800 propostas reais e todas as repetições no verdadeiro.
- Auditoria independente lê os brutos com round_trip, recompõe médias por bloco, V_obs/V_sim e I; verifica propostas versus execução por float.hex, faixas e 400 estratos LHS por dimensão/onda, duas instâncias distintas por bloco, verdade completa, sementes e pareamento. Não importa funções estatísticas do runner.
- Resíduo máximo da recomputação: 2e-14 (arredondamento de agregação). Não há divergência na classificação das réplicas ou no conjunto aceito.
- Suíte completa: **112 testes aprovados**, incluindo os cinco novos testes. Log `outputs/diagnosticos/20260928_hm_v3/testes_suite.log`. O total científico acima não inclui execuções internas de testes.
- Primeiro lote: 536.46 s; complemento: 402.45 s; soma observada 15.65 min de parede, ambos com quatro trabalhadores (inclui overhead dos respectivos runners; não inclui tempo de programação/revisão). Não é medição de CPU nem benchmark universal.

### Cobertura: todas as versões ao lado, sem comparação causal

| Versão/desenho | Exclusões / B | Taxa | IC95 Wilson | p95 de I_max |
|---|---:|---:|---:|---:|
| Legado, instâncias independentes | 31/500 | 6.20% | [4.40%; 8.67%] | 3.116875 |
| V3, instâncias independentes (diagnóstico) | 37/mu_minimo | 7.40% | [5.42%; 10.03%] | 3.299083 |
| **V3, pareada (principal)** | 33/500 | 6.60% | [4.74%; 9.12%] | 3.144957 |

A cobertura principal tem falsa exclusão **6,6%, ou 1,6 ponto percentual acima da referência de 5%**. O IC95 [4,74%; 9,12%] inclui 5%; não demonstra igualdade exata com 5%, nem uma garantia de cobertura de 95%. A cobertura empírica correspondente é 93,4%. A série independente resulta em 7,4% e seu intervalo exclui 5%; também permanece publicada.

O percentil 95 pareado, **3,144957**, excede 3. Ele é uma referência empírica de corte conjunto para ESTE desenho interno de quatro observáveis; 3 é a regra marginal. Não substituí o corte pré-registrado, não recalculei NROY com outro corte e não ajustei V_mod. O JSON da análise também conserva testes binomiais bilaterais como diagnóstico pós-processamento; a conclusão pré-especificada usa taxa e Wilson, não seleção por p-valor.

### Gêmeo individual: exclusão explícita do verdadeiro

As sementes 100–109 geraram o alvo; 200–203 estimaram independentemente a resposta no verdadeiro. Os quatro índices foram:

| Observável | I_j |
|---|---:|
| taxa_omissao | 0.253004703 |
| atraso_relativo | 0.444807331 |
| retrabalho_sobre_plano | 5.017714980 |
| E_total | 0.427555712 |

**I_max=5,017715: o verdadeiro foi excluído nessa realização**, por retrabalho_sobre_plano. Não se procurou outra observação nem outra semente para fazê-lo passar. A verdade está dentro das cinco projeções marginais da caixa NROY final, mas isso não implica aceitação conjunta. A frequência de falsa exclusão é medida pelas 500 réplicas, não por esse único gêmeo. Este resultado não invalida as execuções nem autoriza chamar o procedimento de calibrado externamente.

### HM e identificabilidade

| Grandeza | Espaço legado 5D | V3 5D |
|---|---:|---:|
| Propostas aceitas na onda 2 | 115/400 (28,75%) | 63/400 (15,75%) |
| Volume da caixa envolvente / volume a priori | 14,7987% | 37,6899% |

Na v3, a onda 1 aceitou 46/400 (11,5%) e a caixa ocupou 62,9438% do a priori. Os percentuais de caixa **não** são estimativas diretas do volume do conjunto NROY conjunto e não demonstram convergência das ondas. O mesmo desenho normalizado LHS foi preservado nas duas ondas, limitação herdada e declarada.

| Parâmetro | Contração histórica | Contração v3 (onda 2) | Leitura descritiva v3 |
|---|---:|---:|---|
| risco.F_ancora | 36.77% | 12.95% | não identificado |
| retrabalho.f_retrabalho | 5.99% | 13.32% | não identificado |
| agentes.tau_sat | 10.88% | 41.55% | parcialmente identificado |
| fuzzy.mu_minimo | 70.35% | 10.24% | não identificado |
| agentes.k_heuristico | 5.79% | — | **Retirado por derivação**, não por falta de dados |
| agentes.k_analitico | — | 4.79% | **Não identificado por contração marginal** |

Os rótulos usam a convenção descritiva histórica: contração <25% não identificado; de 25% a <50%, parcialmente; ≥50%, identificado. Não são um teste de identificabilidade estrutural nem critério passou/reprovou. Os limites completos de cada projeção, por onda, estão em `auditoria/identificabilidade_lado_a_lado.csv`. Para k_analitico, a projeção final é aproximadamente [0,021421; 0,078548], permanecendo próxima de toda a faixa [0,02; 0,08].

**Não comparabilidade:** mudaram o significado de uma dimensão, o vetor verdadeiro, o núcleo (legado → MVP v3), a dinâmica e o estimador da variância do HM; a cobertura principal também explicita o pareamento. Portanto, diferenças de contração, volume ou exclusão não podem ser atribuídas apenas à substituição de kh nem apresentadas como melhora/piora do método. Os resultados antigos continuam válidos para seu desenho histórico. Nada foi apagado ou renomeado para parecer resultado v3.

### Proveniência e limites de preservação

O primeiro runner capturou hashes e snapshots de código/configuração/pré-registro, verificou-os ao final e reconferiu **699 arquivos de outputs anteriores sem mudança**. O complemento verificou o mesmo código/configuração e leu os dados PSPLIB de cópias congeladas; seus hashes coincidem com o manifesto anterior do parecer 78.

Limitação descoberta em revisão: o primeiro lote não capturou os hashes dos CSVs de entrada na partida. A cópia posterior e a igualdade com o manifesto 78 não provam retrospectivamente ausência de alteração transitória durante o primeiro lote. Não foi observada alteração; o limite é declarado, não tratado como verificação que não ocorreu. Imports de código são vivos, com hashes antes/depois e snapshots preservados, não isolamento completo do ambiente. Versões de Python/NumPy/plataforma estão no desenho JSON.

### Inventário e continuidade

[82 — Inventário de pipelines v3](82_INVENTARIO_PIPELINES_V3.md) lista 133 arquivos, cada um com estatuto, evidência ou motivo de não execução. As 4.704 execuções da 79 foram reconferidas por grupo; não foram confundidas com todos os entrypoints do projeto. Casos históricos incompatíveis com a configuração viva ficam explicitamente marcados. O runner v3 é `research/hm_v3.py`; o 04 legado e a cobertura D2 permanecem históricos e não devem ser usados como entradas v3.

Não houve mudança do nominal, dos simuladores, nem git status/add/commit/push. A próxima decisão científica não é escolher uma faixa mais estreita para k_analitico: é interpretar a informação limitada destes observáveis internos e, separadamente, fechar o contrato observacional de eventual calibração externa.

### Comandos executados e arquivos de entrega

```bash
python -m unittest discover -s research -p test_hm_v3.py -v
python research/hm_v3.py --saida outputs/diagnosticos/20260928_hm_v3 --workers 4
python -m unittest discover -s research -p test_cobertura_pareada_v3.py -v
python research/cobertura_pareada_v3.py outputs/diagnosticos/20260928_hm_v3
python -m unittest discover -s research -p 'test_*.py' -v
python research/analisar_hm_v3.py outputs/diagnosticos/20260928_hm_v3
python research/inventariar_pipelines_v3.py
```

Usou-se `.venv/bin/python` no clone TCC2_discriminante. Comandos científicos recusam destinos existentes: para reprodução, selecionar outro diretório e preservar estes resultados. A análise gera `auditoria/` novo, sem tocar nos brutos. Pré-registros originais estão também nos snapshots anteriores à execução; este parecer recebeu os resultados apenas depois do término.
