# T1/T2/T3 — arranjo, portão e premissas de reporte

**V_obs/V_mod continua pausado. Nominal histórico preservado.**

## Desenho e verificações

[DEC] Protocolo registrado em `research/PLANO_T1_T2_T3.md` antes de executar.
2176 execuções: 1408 em T1, 768 em T2; todas completas, sem violações.
T1: 88 células, 4 instâncias e
4 sementes por célula. T2: 16 instâncias,
12 sementes; referência compartilhada e três intervenções.
IC95 t sobre médias por instância, sementes internas pareadas; intervalos pontuais.
O piloto foi executado em pasta separada e não compõe esses números.
Os pares comuns (p_reporte, p_deteccao), lidos do desenho, são
[(0.15, 0.03), (0.75, 0.12)].

T2 altera blocos: **confiança significa tau_inicial E tau_min**. Não é efeito
isolado de tau_inicial. Na referência ambos estão no nível centralizado; a célula
confiança troca os dois, a célula reporte troca p_reporte e p_deteccao, e ambos
reproduz o nominal adaptativo. Os demais parâmetros são idênticos.

Mesmas instâncias/sementes e mesma sequência pseudoaleatória inicial em todos
os contrastes. O consumo sequencial pode desalinhá-la entre eventos após as
trajetórias divergirem. Não se alega identidade de sorteio por tarefa/evento.
O estimando é o contraste entre regimes simulados, não um contrafactual local de
uma mesma tarefa. Nenhum resultado abaixo constitui calibração externa.

## T1 — portão binário, resposta global não reduzida a degrau puro

Na igualdade tau=tau_min e abaixo dela, pedidos ficam bloqueados. Logo acima,
a comunicação se ativa. Essa é a descontinuidade do predicado estrito. Porém os
cinco desfechos variam também dentro de cada lado, inclusive quando N_req é zero.
**A hipótese de um degrau puro não descreve a resposta observada.** A arquitetura
combina um portão binário e um canal fuzzy variável; não se pode concluir que o
aparato difuso não contribui ao contraste.

Em estado local fixo (bateria e pressão fixadas no arquivo), mu_rede varia de
0.775000 a 1.000000 com tau, sem alterar mu_cog.
O CSV local separa a resposta fuzzy de seleção, disponibilidade e aprendizado.
A trajetória completa é discreta, com ceil, sorteios, filas e confiança dinâmica;
malha finita não prova continuidade matemática. O indicador `degrau_puro=False`
é descritivo, não teste de significância (usa igualdade numérica exata).

Curvas dos cinco indicadores com IC95: [figura](../outputs/diagnosticos/arranjo_20260917/T1_curvas.png).
Dados completos: `T1_curvas_IC95.csv`, `T1_forma.csv` e
`T1_canal_fuzzy_estado_fixo.csv`. Não se impõe monotonicidade aos resultados.

### Contraste local tau_min+epsilon menos igualdade

| tau_min | p_reporte | Indicador | Diferença local | IC95 |
|---|---|---|---|---|
| 0.25 | 0.15 | atraso_relativo | -0.258810 | [-0.539247; 0.021626] |
| 0.25 | 0.15 | taxa_omissao | -0.032292 | [-0.091932; 0.027348] |
| 0.25 | 0.15 | divida_latente_sobre_plano | -0.011639 | [-0.036664; 0.013385] |
| 0.25 | 0.15 | taxa_falha_efetiva | -0.030208 | [-0.086042; 0.025625] |
| 0.25 | 0.15 | fracao_porta1 | -0.098958 | [-0.251054; 0.053137] |
| 0.25 | 0.15 | N_req | 109.687500 | [44.330721; 175.044279] |
| 0.25 | 0.75 | atraso_relativo | -0.269547 | [-0.358573; -0.180520] |
| 0.25 | 0.75 | taxa_omissao | -0.000000 | [-0.058555; 0.058555] |
| 0.25 | 0.75 | divida_latente_sobre_plano | -0.003855 | [-0.018190; 0.010480] |
| 0.25 | 0.75 | taxa_falha_efetiva | -0.031250 | [-0.128767; 0.066267] |
| 0.25 | 0.75 | fracao_porta1 | -0.087500 | [-0.167245; -0.007755] |
| 0.25 | 0.75 | N_req | 86.812500 | [40.754703; 132.870297] |
| 0.6 | 0.15 | atraso_relativo | 0.294843 | [0.029508; 0.560179] |
| 0.6 | 0.15 | taxa_omissao | 0.010417 | [-0.014094; 0.034927] |
| 0.6 | 0.15 | divida_latente_sobre_plano | -0.001896 | [-0.017522; 0.013731] |
| 0.6 | 0.15 | taxa_falha_efetiva | 0.007292 | [-0.001051; 0.015634] |
| 0.6 | 0.15 | fracao_porta1 | -0.075000 | [-0.121882; -0.028118] |
| 0.6 | 0.15 | N_req | 105.875000 | [22.170196; 189.579804] |
| 0.6 | 0.75 | atraso_relativo | -0.175022 | [-0.248316; -0.101728] |
| 0.6 | 0.75 | taxa_omissao | 0.006250 | [-0.015740; 0.028240] |
| 0.6 | 0.75 | divida_latente_sobre_plano | -0.005072 | [-0.013759; 0.003615] |
| 0.6 | 0.75 | taxa_falha_efetiva | 0.002083 | [-0.043370; 0.047537] |
| 0.6 | 0.75 | fracao_porta1 | -0.064583 | [-0.111932; -0.017235] |
| 0.6 | 0.75 | N_req | 103.937500 | [25.035870; 182.839130] |

[LIMITACAO] Epsilon = 10⁻⁶ é o menor passo declarado na malha. O salto de pedidos não
implica salto detectável em todos os desfechos: IC95 de omissão, dívida e falha
efetiva incluem zero nas células locais. No limiar alto com reporte baixo, abrir
o portão **aumenta** atraso neste desenho. Não escolher limiar pelo sinal favorável.
A incerteza com poucas instâncias e as interações impedem extrapolação universal.

### Alternativa de reposicionamento proposta, sem eleger cenário

[DEC] Para investigar comunicação ativa nos dois braços, usar limiar comum e
confianças iniciais a pequenas distâncias positivas dele: uma família com margens
+0,01 e +0,05, repetida separadamente para cada limiar nominal. Repetir cada par
nos dois níveis comuns de reporte/detecção. Ambos os braços começam com pedidos
elegíveis; Crowder poderá alterar essa condição ao longo da execução. Os rótulos
passam a significar confiança próxima ao limiar, não os arranjos históricos.
Não aplicar a mudança ao YAML nominal. Esta é proposta experimental a priori,
não a seleção do ponto de melhor desempenho; não foi executada nesta entrega.

## T2 — bloqueio de premissas

Diferença = intervenção − referência centralizada. Razões são médias das razões
por execução. A fração P1 usa tarefas executadas, não oportunidades ou esforço.

| Bloco alterado | Indicador | Referência | Intervenção | Diferença | IC95 |
|---|---|---|---|---|---|
| confianca | atraso_relativo | 3.060802 | 2.741961 | -0.318842 | [-0.380422; -0.257261] |
| reporte | atraso_relativo | 3.060802 | 2.469996 | -0.590807 | [-0.685519; -0.496094] |
| ambos | atraso_relativo | 3.060802 | 2.037381 | -1.023421 | [-1.113870; -0.932973] |
| confianca | taxa_omissao | 0.312500 | 0.271181 | -0.041319 | [-0.054601; -0.028038] |
| reporte | taxa_omissao | 0.312500 | 0.090104 | -0.222396 | [-0.235935; -0.208857] |
| ambos | taxa_omissao | 0.312500 | 0.084288 | -0.228212 | [-0.242839; -0.213584] |
| confianca | divida_latente_sobre_plano | 0.103272 | 0.087967 | -0.015305 | [-0.019987; -0.010623] |
| reporte | divida_latente_sobre_plano | 0.103272 | 0.028985 | -0.074287 | [-0.082580; -0.065995] |
| ambos | divida_latente_sobre_plano | 0.103272 | 0.025458 | -0.077815 | [-0.086201; -0.069428] |
| confianca | taxa_falha_efetiva | 0.361979 | 0.310937 | -0.051042 | [-0.066909; -0.035174] |
| reporte | taxa_falha_efetiva | 0.361979 | 0.353472 | -0.008507 | [-0.022926; 0.005912] |
| ambos | taxa_falha_efetiva | 0.361979 | 0.318924 | -0.043056 | [-0.056843; -0.029268] |
| confianca | fracao_porta1 | 0.636979 | 0.502344 | -0.134635 | [-0.158280; -0.110990] |
| reporte | fracao_porta1 | 0.636979 | 0.639497 | 0.002517 | [-0.005978; 0.011013] |
| ambos | fracao_porta1 | 0.636979 | 0.520486 | -0.116493 | [-0.136605; -0.096381] |

O bloco reporte/detecção altera fortemente a fração de falhas não reportadas e
seu estoque oculto. Isso não demonstra redução equivalente de defeitos gerados:
seu IC95 de taxa de falha efetiva inclui zero. “Inclui zero” significa inconclusivo,
não ausência de efeito. A confiança isolada reduz a taxa efetiva neste desenho.
A redução do nominal combina mecanismos e premissas; não é evidência de um efeito
único de governança independente das escolhas de reporte e limiar.

### Interação e efeito condicionado

Não somar contribuições como percentuais causais. A interação é
(ambos − referência) − (confiança − referência) − (reporte − referência).
Interação positiva nos desfechos reduzidos expressa subaditividade das reduções,
não um prejuízo provocado pela confiança.

| Indicador | Interação | IC95 |
|---|---|---|
| atraso_relativo | -0.113773 | [-0.193343; -0.034202] |
| taxa_omissao | 0.035503 | [0.019939; 0.051068] |
| divida_latente_sobre_plano | 0.011778 | [0.006727; 0.016828] |
| taxa_falha_efetiva | 0.016493 | [-0.002239; 0.035225] |
| fracao_porta1 | 0.015625 | [0.002788; 0.028462] |

Confiança adicional depois de igualar o bloco reporte ao adaptativo:

| Indicador | Ambos − reporte | IC95 |
|---|---|---|
| atraso_relativo | -0.432614 | [-0.491390; -0.373839] |
| taxa_omissao | -0.005816 | [-0.013603; 0.001971] |
| divida_latente_sobre_plano | -0.003527 | [-0.006063; -0.000992] |
| taxa_falha_efetiva | -0.034549 | [-0.048575; -0.020522] |
| fracao_porta1 | -0.119010 | [-0.138697; -0.099324] |

## Conferência do braço sem comunicação

No nominal centralizado: hiato_encontrado médio=140.781250;
hiato_colega_capaz_sem_confianca=130.562500;
N_req=0.000000, p2_ajuda=0.000000, TL=0.000000.
A porta não se abre e Crowder não recebe eventos nesse braço. Isso explica por
que os degraus de comunicação/lei/reset anteriores só alteraram o adaptativo.
Não significa que todos os mecanismos fuzzy estejam inertes no centralizado.

A razão das probabilidades de não reporte é
3.400000; a razão observada de omissão é
3.707518. A comparação logarítmica da
premissa com o contraste é descritiva; não identifica uma parcela causal porque
reporte/detecção também afetam filas, duração, pressão e futuros sorteios.
T2 mede esses regimes explicitamente, incluindo suas interações.

## T3 — taxa de falha efetiva de primeira classe

`Resultado.taxa_falha_efetiva = (n_com_erro+n_reportadas)/n_tarefas`.
O campo é derivado sem alterar RNG, decisões ou estados. Foi propagado aos
runners que exportam execuções, inclusive por asdict, e aos resumos de desfechos.
Os artefatos anteriores não foram sobrescritos. Consumidores de CSV histórico
podem derivá-lo em memória quando os dois contadores e o denominador existem;
onde faltam contadores, não inventar uma baseline.

Neste lote completo a soma confere com todas as falhas instrumentadas por tarefa.
Nos runs censurados, ocultos entram no contador após conclusão e reportados entram
durante a execução: a fórmula não deve ser interpretada como taxa final de todas
as tentativas. Publicar sempre concluiu/censura. Reparos não reincidem no modelo;
essa taxa conta falhas da execução original, não tentativas de reparo.

Controles exatos existentes preservam campos anteriores, estados e RNG. A tabela
`controle_nominal.csv` registra ANTES/DEPOIS sem mudança substantiva; o maior
resíduo de leitura CSV foi 2.84e-14.

## Correções documentais e continuidade

Parecer 22: retrabalho_sobre_esforco_realizado excluído do vetor z pela dependência
de TL; pico de dívida exige controlar número de amostras e horizonte endógeno.
Plano B orientado a padrões registrado antes de avaliá-los, com padrões candidatos,
critério de sucesso conjunto e exigência de fonte externa. Não converter controles
internos tautológicos em validação externa. Nenhuma retomada de V_obs/V_mod ou HM.

Próxima questão: discutir a alternativa próxima ao limiar e obter evidência externa
para premissas de reporte/detecção. Resultados desta entrega não substituem o
nominal histórico. O parecer 23 citado não estava disponível no remoto consultado;
a instrução textual da autora foi integralmente usada como referência operacional.

Reprodução: `python3 src/modelo/26_testes_arranjo.py --saida /tmp/arranjo-novo --workers 4`,
seguida da geração deste relatório por `research/gerar_relatorio_arranjo.py`
(a geração lê o lote publicado). O diretório do experimento deve ser novo.
