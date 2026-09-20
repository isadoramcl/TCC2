# B2 — desligamento do canal direto e limites de robustez

> Leitura atual: [bloqueio de três vias e censura](B2_DEADLOCK_TRES_VIAS_E_CENSURA.md).
> Portão fechado sozinho não implica incompletude; nominal completo em ambos os braços.


> Leitura causal atualizada por [T-B2.3](TB23_PORTAO_E_INCOMPLETUDE.md):
> abrir só o portão completa 36/36; a rede sozinha completa 0/36.
> A-13 participa de bloqueio de três vias, restrito a s=0,01 e tau_sat=1/1,4
> na centralizada; assistência ou heurística liberam saídas independentes.


> Atualização: resultados iniciais publicados em `d54283b`. A classificação da
> incompletude e os contrastes das células afetadas são reavaliados em
> [T-B2.1/T-B2.2](TB2_HORIZONTE_E_SELECAO.md). As tabelas abaixo preservam o
> diagnóstico inicial; não usar valores censurados como desfechos finais.

18/09/2026. Continuação autorizada da ordem 37 após validação discriminante C3
e conclusão B1/T4. [Protocolo anterior](../research/lote41/PROTOCOLO_B2.md).

## Implementação e controles

`OpcoesMVP.canal_erro_direto`: `ativo` por padrão; `desligado` aplica R_error=0.
P_heu não mudou. A ausência de evidência de campo para o canal direto não prova
efeito nulo; a alternativa testa a dependência estrutural do resultado.
Nominal histórico preservado. Identidade bit a bit após a implementação passou;
modo desligado reproduz o modelo ativo com R_error configurado em zero.
Instrumentação por tarefa foi desativada apenas no runner B2 para limitar memória;
um controle verifica igualdade de resultados e RNG com/sem armazenamento.

1.344 execuções: nominal 16×12×2 cenários×2 canais=768; grade 4×4×2×2×9=576.
Grade usa exatamente os valores YAML preexistentes tau_sat=[0,7;1;1,4] e
s_transicao=[0,01;0,25;0,6]. Nenhuma busca de melhor parâmetro. O nominal ativo
reproduz T2 arquivado, diferença máxima 2,8421709430404014e-14 (serialização).

## Nominal: cinco indicadores em ambos os cenários

Valores média [IC95]; 16 médias por instância com 12 sementes internas.
IC t pontuais. A−C usa diferenças pareadas por instância/semente.

| Canal | Indicador | Centralizada | Adaptativa | Contraste A−C |
|---|---|---|---|---|
| ativo | atraso_relativo | 3.060802 [2.752985; 3.368620] | 2.037381 [1.773492; 2.301271] | -1.023421 [-1.113870; -0.932973] |
| ativo | taxa_omissao | 0.312500 [0.294370; 0.330630] | 0.084288 [0.076504; 0.092072] | -0.228212 [-0.242839; -0.213584] |
| ativo | divida_latente_sobre_plano | 0.103272 [0.093760; 0.112784] | 0.025458 [0.022972; 0.027943] | -0.077815 [-0.086201; -0.069428] |
| ativo | taxa_falha_efetiva | 0.361979 [0.339808; 0.384150] | 0.318924 [0.296469; 0.341378] | -0.043056 [-0.056843; -0.029268] |
| ativo | fracao_porta1 | 0.636979 [0.582431; 0.691528] | 0.520486 [0.458634; 0.582339] | -0.116493 [-0.136605; -0.096381] |
| desligado | atraso_relativo | 3.041374 [2.717604; 3.365144] | 2.010786 [1.751568; 2.270005] | -1.030588 [-1.126777; -0.934398] |
| desligado | taxa_omissao | 0.287413 [0.270622; 0.304204] | 0.076823 [0.069350; 0.084296] | -0.210590 [-0.223511; -0.197670] |
| desligado | divida_latente_sobre_plano | 0.098311 [0.090099; 0.106523] | 0.024303 [0.021418; 0.027189] | -0.074007 [-0.080703; -0.067311] |
| desligado | taxa_falha_efetiva | 0.334549 [0.314340; 0.354757] | 0.293490 [0.272736; 0.314243] | -0.041059 [-0.053419; -0.028699] |
| desligado | fracao_porta1 | 0.636198 [0.579808; 0.692587] | 0.519097 [0.458566; 0.579628] | -0.117101 [-0.137805; -0.096396] |

**No nominal, os cinco contrastes negativos sobrevivem com o canal direto
desligado, todos com IC95 abaixo de zero.** Isso não remove a contribuição das
premissas de reporte à omissão e à dívida, nem autoriza tratar atraso relativo
a CPM como crescimento de prazo externo. E_total continua excluído da conclusão.

## Grade: execuções incompletas não são resultados finais

**36/576 execuções da grade ficaram incompletas; 24 não executaram tarefa alguma.**
Todas pertencem ao braço centralizado, nos dois estados do canal direto. Nenhuma
violação contábil foi registrada. Não houve censura nas 768 execuções nominais.

| Canal | tau_sat | s_transicao | Cenário | Completas/execuções | Sem tarefas |
|---|---:|---:|---|---:|---:|
| ativo | 1.0 | 0.01 | centralizada | 9/16 | 4 |
| ativo | 1.4 | 0.01 | centralizada | 5/16 | 8 |
| desligado | 1.0 | 0.01 | centralizada | 9/16 | 4 |
| desligado | 1.4 | 0.01 | centralizada | 5/16 | 8 |

Os CSV brutos preservam essas execuções. Taxa de omissão/falha zero em uma
execução sem tarefas não significa desempenho superior. O prazo igual a 256×CPM
é horizonte atingido, não prazo final. Fração P1 com denominador zero é NaN,
nunca zero. As tabelas gerais carregam contagens explícitas de censura e de
frações indefinidas; suas médias em células censuradas descrevem apenas os
valores até o limite, e não sustentam inferência sobre desfechos finais.

Para leitura sem esse problema, a tabela `grade_completa_contrastes_IC95.csv`
seleciona **células inteiras sem censura**, preservando todas as sementes e
instâncias de cada célula. Não elimina seletivamente execuções desfavoráveis
nem representa a grade completa. Há sete células completas por canal.

### Contraste A−C nas células completas (inclui resultados não significativos)

| Canal | tau_sat | s_transicao | Indicador | Média [IC95] |
|---|---:|---:|---|---|
| ativo | 0.7 | 0.01 | atraso_relativo | -1.416290 [-2.324837; -0.507743] |
| ativo | 0.7 | 0.01 | taxa_omissao | -0.305208 [-0.346569; -0.263848] |
| ativo | 0.7 | 0.01 | divida_latente_sobre_plano | -0.097336 [-0.139977; -0.054695] |
| ativo | 0.7 | 0.01 | taxa_falha_efetiva | -0.106250 [-0.198834; -0.013666] |
| ativo | 0.7 | 0.01 | fracao_porta1 | -0.312500 [-0.527749; -0.097251] |
| ativo | 0.7 | 0.25 | atraso_relativo | -1.247446 [-1.965293; -0.529600] |
| ativo | 0.7 | 0.25 | taxa_omissao | -0.220833 [-0.298719; -0.142947] |
| ativo | 0.7 | 0.25 | divida_latente_sobre_plano | -0.072189 [-0.103877; -0.040500] |
| ativo | 0.7 | 0.25 | taxa_falha_efetiva | -0.053125 [-0.165299; +0.059049] |
| ativo | 0.7 | 0.25 | fracao_porta1 | -0.114583 [-0.206692; -0.022475] |
| ativo | 0.7 | 0.6 | atraso_relativo | -1.135001 [-1.377880; -0.892121] |
| ativo | 0.7 | 0.6 | taxa_omissao | -0.205208 [-0.279705; -0.130712] |
| ativo | 0.7 | 0.6 | divida_latente_sobre_plano | -0.063592 [-0.099185; -0.027998] |
| ativo | 0.7 | 0.6 | taxa_falha_efetiva | -0.046875 [-0.132019; +0.038269] |
| ativo | 0.7 | 0.6 | fracao_porta1 | -0.040625 [-0.099523; +0.018273] |
| ativo | 1.0 | 0.25 | atraso_relativo | -1.050750 [-1.891816; -0.209684] |
| ativo | 1.0 | 0.25 | taxa_omissao | -0.207292 [-0.244552; -0.170031] |
| ativo | 1.0 | 0.25 | divida_latente_sobre_plano | -0.067985 [-0.089434; -0.046536] |
| ativo | 1.0 | 0.25 | taxa_falha_efetiva | -0.047917 [-0.114107; +0.018274] |
| ativo | 1.0 | 0.25 | fracao_porta1 | -0.108333 [-0.117710; -0.098957] |
| ativo | 1.0 | 0.6 | atraso_relativo | -1.106533 [-1.421340; -0.791725] |
| ativo | 1.0 | 0.6 | taxa_omissao | -0.184375 [-0.290646; -0.078104] |
| ativo | 1.0 | 0.6 | divida_latente_sobre_plano | -0.059817 [-0.087612; -0.032022] |
| ativo | 1.0 | 0.6 | taxa_falha_efetiva | -0.045833 [-0.127754; +0.036087] |
| ativo | 1.0 | 0.6 | fracao_porta1 | -0.056250 [-0.143623; +0.031123] |
| ativo | 1.4 | 0.25 | atraso_relativo | -1.198250 [-1.636998; -0.759502] |
| ativo | 1.4 | 0.25 | taxa_omissao | -0.229167 [-0.307802; -0.150532] |
| ativo | 1.4 | 0.25 | divida_latente_sobre_plano | -0.076137 [-0.112490; -0.039785] |
| ativo | 1.4 | 0.25 | taxa_falha_efetiva | -0.082292 [-0.148010; -0.016573] |
| ativo | 1.4 | 0.25 | fracao_porta1 | -0.229167 [-0.312153; -0.146180] |
| ativo | 1.4 | 0.6 | atraso_relativo | -0.953338 [-1.360596; -0.546081] |
| ativo | 1.4 | 0.6 | taxa_omissao | -0.186458 [-0.210287; -0.162630] |
| ativo | 1.4 | 0.6 | divida_latente_sobre_plano | -0.066995 [-0.097277; -0.036714] |
| ativo | 1.4 | 0.6 | taxa_falha_efetiva | -0.016667 [-0.116779; +0.083446] |
| ativo | 1.4 | 0.6 | fracao_porta1 | -0.058333 [-0.154260; +0.037593] |
| desligado | 0.7 | 0.01 | atraso_relativo | -1.265622 [-1.947982; -0.583263] |
| desligado | 0.7 | 0.01 | taxa_omissao | -0.266667 [-0.335781; -0.197552] |
| desligado | 0.7 | 0.01 | divida_latente_sobre_plano | -0.098714 [-0.141159; -0.056268] |
| desligado | 0.7 | 0.01 | taxa_falha_efetiva | -0.095833 [-0.250567; +0.058900] |
| desligado | 0.7 | 0.01 | fracao_porta1 | -0.316667 [-0.547168; -0.086166] |
| desligado | 0.7 | 0.25 | atraso_relativo | -1.148710 [-1.625213; -0.672207] |
| desligado | 0.7 | 0.25 | taxa_omissao | -0.192708 [-0.251855; -0.133562] |
| desligado | 0.7 | 0.25 | divida_latente_sobre_plano | -0.063404 [-0.097040; -0.029769] |
| desligado | 0.7 | 0.25 | taxa_falha_efetiva | -0.030208 [-0.117056; +0.056639] |
| desligado | 0.7 | 0.25 | fracao_porta1 | -0.114583 [-0.216509; -0.012658] |
| desligado | 0.7 | 0.6 | atraso_relativo | -1.052429 [-1.354144; -0.750714] |
| desligado | 0.7 | 0.6 | taxa_omissao | -0.194792 [-0.254677; -0.134906] |
| desligado | 0.7 | 0.6 | divida_latente_sobre_plano | -0.056312 [-0.086673; -0.025951] |
| desligado | 0.7 | 0.6 | taxa_falha_efetiva | -0.051042 [-0.151647; +0.049563] |
| desligado | 0.7 | 0.6 | fracao_porta1 | -0.046875 [-0.108687; +0.014937] |
| desligado | 1.0 | 0.25 | atraso_relativo | -1.213323 [-1.895401; -0.531246] |
| desligado | 1.0 | 0.25 | taxa_omissao | -0.222917 [-0.286395; -0.159438] |
| desligado | 1.0 | 0.25 | divida_latente_sobre_plano | -0.075711 [-0.120523; -0.030899] |
| desligado | 1.0 | 0.25 | taxa_falha_efetiva | -0.043750 [-0.124136; +0.036636] |
| desligado | 1.0 | 0.25 | fracao_porta1 | -0.110417 [-0.149641; -0.071192] |
| desligado | 1.0 | 0.6 | atraso_relativo | -1.027619 [-1.511138; -0.544100] |
| desligado | 1.0 | 0.6 | taxa_omissao | -0.182292 [-0.303264; -0.061319] |
| desligado | 1.0 | 0.6 | divida_latente_sobre_plano | -0.062710 [-0.101352; -0.024068] |
| desligado | 1.0 | 0.6 | taxa_falha_efetiva | -0.048958 [-0.152577; +0.054660] |
| desligado | 1.0 | 0.6 | fracao_porta1 | -0.066667 [-0.166044; +0.032711] |
| desligado | 1.4 | 0.25 | atraso_relativo | -0.890419 [-1.240990; -0.539847] |
| desligado | 1.4 | 0.25 | taxa_omissao | -0.193750 [-0.238880; -0.148620] |
| desligado | 1.4 | 0.25 | divida_latente_sobre_plano | -0.072001 [-0.093449; -0.050552] |
| desligado | 1.4 | 0.25 | taxa_falha_efetiva | -0.048958 [-0.065534; -0.032383] |
| desligado | 1.4 | 0.25 | fracao_porta1 | -0.230208 [-0.341333; -0.119084] |
| desligado | 1.4 | 0.6 | atraso_relativo | -0.925787 [-1.026749; -0.824826] |
| desligado | 1.4 | 0.6 | taxa_omissao | -0.160417 [-0.188284; -0.132549] |
| desligado | 1.4 | 0.6 | divida_latente_sobre_plano | -0.053123 [-0.076692; -0.029553] |
| desligado | 1.4 | 0.6 | taxa_falha_efetiva | -0.014583 [-0.083166; +0.053999] |
| desligado | 1.4 | 0.6 | fracao_porta1 | -0.064583 [-0.159974; +0.030807] |

A conclusão nominal não é uma garantia uniforme: na grade completa de parâmetros
não se demonstrou robustez de desfechos finais por causa da censura. Nas células
completas, intervalos baseados em apenas quatro instâncias são pouco precisos;
IC que inclui zero é inconclusivo, não prova ausência de efeito.

## Causa investigada: seleção bloqueia tarefas executáveis

Caso reproduzido: `j6021_1.sm`, seed=0, centralizada, tau_sat=1, s=0,01.
A regra escolhe a maior dificuldade dentre as tarefas prontas **antes** de testar
competência. Escolhe tarefa 3, Di=0,689416916, mas a competência máxima é
0,626850718. As tarefas 2 e 4 (Di=0,343328875 e 0,440339881) também estão
prontas e cabem na competência, porém não são selecionadas.

Ajuda bloqueada por 0,25 > 0,60 falso. Mesmo na pressão máxima P=1 e bateria=1,
a chance heurística para a tarefa escolhida é 3,24749e-14 por tentativa.
Enquanto ninguém trabalha a bateria não cai; o mecanismo repete o mesmo
impasse. Um limite superior por união para haver ao menos uma P1 em
6×256×76 tentativas é aproximadamente 3,79e-9. Observado: zero tarefas em
19.456 períodos, N_req=0 e N_blocked=97.280. O zero no relatório não era acaso
numérico de arredondamento: o denominador era de fato zero.

Isso identifica uma interação da regra de seleção com o portão fechado e a
transição quase determinística. Não prova que priorizar tarefas compatíveis
resolveria todos os impasses futuros; esse contrafactual ainda precisa ser
experimentado como alternativa preservada. **Nenhuma mudança nessa política
foi feita para fazer a grade passar.** Evidência está em
[diagnostico_sem_tarefas.json](../outputs/diagnosticos/lote41_B2_censura_20260918/diagnostico_sem_tarefas.json).

## Correção do runner e rastreabilidade

A primeira tentativa falhou por divisão por zero e tinha apenas manifesto salvo;
foi preservada em `lote41_B2_20260918`, com registro da falha. A reexecução em
`lote41_B2_censura_20260918` grava cada linha imediatamente e preserva NaN e
censura. A correção é observacional; não consome RNG e não muda a dinâmica.
Teste de regressão impede converter ausência de tarefas em fração zero.

[Saídas completas](../outputs/diagnosticos/lote41_B2_censura_20260918/).

```sh
python3 research/lote41/b2.py --saida /tmp/b2-nova
```

## Continuidade

C3 validado e B1 concluído. B2 executado e documentado, com robustez limitada
por censura estrutural. **O lote 37 não está fechado.** Prioridade seguinte:
testar alternativa preservada para seleção de tarefa e repetir as células
censuradas antes de sustentar robustez na grade. A1 e os demais itens ainda não
executados permanecem pendentes; não são declarados resolvidos.
Não ajustar s_transicao/tau_sat para evitar o resultado nem contra Rieskamp.
Nenhuma nova onda HM, nenhum ajuste de V_mod, resultados desta etapa publicados em `d54283b`.
