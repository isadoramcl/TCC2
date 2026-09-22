# 78 — Causa da falha efetiva na v2: teste discriminante

**Estado atual: fatorial concluído sob a exceção de 1 ULP autorizada. Os blocos de parada abaixo são históricos; ver “Resultado final” ao fim.**

## Pré-registro — escrito antes de qualquer execução deste experimento

Clone independente `~/TCC2_discriminante`; execução no Mac autorizada pela autora em substituição ao Windows. Nenhum ajuste de parâmetros, alteração dos dois YAML nominais ou operação de publicação Git.

**Desenho:** 20 pares sorteados sem reposição dos 643 com contraste positivo na v2 (universo recontado independentemente), mais o par nominal. Semente 20260922, `random.Random.sample` sobre pares ordenados por `ai,ci`; seleção integral em `amostra.csv`. Quatro instâncias e sementes 0–3 da grade original. Canto 00 = limiar/constante; 10 = logístico/constante; 01 = limiar/logística; 11 = logístico/logística. Todas as demais opções vêm de `config/mvp.yaml`; instrumentação de tarefas desativada como nas grades. Execuções repetidas de um mesmo perfil/braço são reutilizadas entre pares, sem tratá-las como replicações adicionais.

**Porta de validade:** reexecutar primeiro 00 e 11; comparar TODOS os campos arquivados por chave, usando `float.hex()` nos números e igualdade nos demais, com leitura `float_precision='round_trip'`. Qualquer divergência interrompe o teste antes de interpretar e antes dos cantos mistos. Sem tolerância numérica. Censura ou violações impedem conclusão mecanística irrestrita.

### Hipóteses e resultados que as confirmariam ou derrubariam

Seja Dgf = falha adaptativa − centralizada no canto gf; negativo favorece adaptativa. Chamaremos inversão v1→v2 apenas D00<0 e D11>0; pares já positivos em 00 não são novas inversões. Sinal pontual e IC serão apresentados separadamente. IC que contém zero implica incerteza; não prova ausência de efeito.

- **H1 (assistência melhora o centralizado):** sustenta-se por célula se abrir apenas assistência eleva D (D10−D00>0), reduz a falha centralizada e essa redução é maior que a adaptativa; N_req/N_success centralizados devem crescer. É suficiente para inversão se D00<0<D10. Derrubada como explicação dessa célula se D10 não aumenta D ou se o deslocamento vem só do adaptativo piorando, sem melhora centralizada. IC95 do efeito e mudanças por braço medem a força da evidência. Repetir efeito da assistência com fuga ligada (D11−D01).
- **H2 (fuga altera o denominador/seleção de tarefas):** requer que ligar fuga mude o denominador real da taxa e as tarefas executadas, e desloque D em direção positiva. O código lido antes da execução define o denominador como `len(tarefas)` da instância: se a contagem continuar fixa e todas as tarefas terminarem, H2 é derrubada **na forma proposta**, mesmo que a fuga tenha efeitos no numerador, no tempo ou na porta de execução. Registrar numerador, denominador, conjunto de IDs executados e concluídos nos quatro cantos. Não confundir adiamentos com novas tarefas.
- **H3 (só os dois juntos):** sustenta-se descritivamente quando D00<0, D10<=0, D01<=0 e D11>0. Cai como necessidade conjunta se algum canto isolado já inverte. Estimar interação J=D11−D10−D01+D00 com IC95: só IC inteiramente positivo sustenta sinergia positiva; cruzamento apenas no canto conjunto pode ser soma de efeitos, não interação demonstrada. Se IC incluir zero, interação permanece inconclusiva.

**Análise:** para cada par e canto, diferença pareada por (arquivo,semente); média das quatro sementes por instância; IC t de Student com 4 instâncias, 3 graus de liberdade. Mesma construção para efeitos fatoriais, interação e mudanças por braço. Não usar 16 sementes como N independente. IC95 individuais, sem correção de multiplicidade. Os 20 pares foram selecionados pelo desfecho na mesma grade: análise diagnóstica condicionada, não nova validação nem estimativa da prevalência de inversões. Não agregar pares como observações independentes.

**Leituras:** taxa de falha=(n_com_erro+n_reportadas)/n_tarefas; número executado = tarefas com início registrado, com confirmação por p1_omissao+p3_analitica. Fração P1 = omissões/(omissões+analíticas); fração de fuga = fugas/(fugas+omissões+analíticas), excluindo tentativas P2; publicar também fugas/(fugas+omissões). Pedidos N_req, sucessos N_success, insucessos N_fail, bloqueios prévios N_blocked. Bateria média = média temporal dos estados médios dos agentes registrados ao fim de cada período, com igual peso por execução/instância, não um pool que sobrepese execuções longas. Confiança final = média dos agentes ao término.

**Limite de atribuição:** assistência e fuga usam um mesmo fluxo auxiliar; mudar um canto muda o consumo subsequente desse fluxo, e decisões afetam o fluxo principal por realimentação. Sementes comuns garantem replicação, não alinhamento de sorteios por evento. O fatorial identifica o efeito da troca de opções na implementação, não isola mediação por cada evento.

**Ambiente:** NumPy/pandas alinhados ao requirements; SciPy 1.18.1 para IC, pois scipy==1.15.3 exige numpy<2.5 e o requirements fixa numpy==2.5.2. Não foi alterado o requirements. Versões exatas e hashes em manifesto_pre_execucao.json.

## Resultado da primeira execução — INTERROMPIDO no controle obrigatório

**Veredito: identidade v1 DIVERGENTE; H1, H2 e H3 NÃO TESTADAS.** Não há conclusão causal autorizada para a monografia a partir deste lote.

O protocolo acima foi salvo em 2026-09-22T13:54:36.064114+00:00 antes da execução e permanece integral em `protocolo_pre_execucao.md`, SHA-256 `31e70529d7e4f7d07a6992566efe89f1f82c01a0442f8fcb1a6ece536ef3b8c3`. HEAD do clone: `8d10b4db8ace1ed9db9e49725daf6e542ef1fc0f`.

### Amostra e controle

A recontagem independente, com diferenças pareadas e médias por instância, confirmou **643 pares positivos entre 1.215 ordenados**. Foram registrados 20 pares sorteados mais o nominal (A=62, C=18), sem substituir nenhum par após observar o controle. Lista e todos os parâmetros em `amostra.csv`.

O canto 00 (`limiar` + `constante`) divergiu na **quarta execução comparada**. Foram comparados 53 campos por execução, 212 comparações: 211 iguais e uma divergente. Nas quatro linhas comparadas, a taxa de falha efetiva e os demais desfechos arquivados coincidem; isso não satisfaz o requisito de identidade integral nem autoriza extrapolar para o restante da grade.

| Chave/campo | Referência v1 | Reexecução |
|---|---|---|
| Perfil / arranjo | 2 / adaptativa | 2 / adaptativa |
| Instância / semente | j6010_1.sm / 3 | j6010_1.sm / 3 |
| competencia_minima_inicial | 0.24332019624229823 | 0.24332019624229825 |
| float.hex() | `0x1.f251dbea89292p-3` | `0x1.f251dbea89293p-3` |

**Diferença = +2,7755575615628914 × 10⁻¹⁷ (1 ULP).** Leitura dos CSV com `float_precision='round_trip'`. Não foi aplicada tolerância, alterado alvo, ajustado parâmetro ou substituído ambiente para fazer o controle passar. A causa dessa diferença não foi determinada neste lote; seria incorreto atribuí-la desde já ao CSV, ao sistema operacional ou a uma biblioteca.

| Etapa | Estatuto |
|---|---|
| Controle 00 contra SAT_GOV v1 | DIVERGENTE; interrompido na 4ª linha |
| Controle 11 contra governança v2 | NÃO EXECUTADO |
| Cantos mistos 10 e 01 | NÃO EXECUTADOS |
| Decomposição e IC95 do fatorial | NÃO CALCULADOS |
| H1 / H2 / H3 | NÃO TESTADAS empiricamente pelo fatorial |

O executor usa quatro processos e pode ter iniciado tarefas adicionais antes da detecção; elas não foram utilizadas nem interpretadas. O processo terminou com código 2; somente as quatro linhas comparadas foram persistidas. Nenhuma análise dos cantos mistos foi iniciada.

### Evidência reproduzível

Comandos executados no clone novo:

```bash
.venv/bin/python research/discriminante_falha.py preparar
.venv/bin/python -u research/discriminante_falha.py controles > outputs/diagnosticos/20260922_discriminante_falha/execucao_controles.log 2>&1
```

Arquivos em `outputs/diagnosticos/20260922_discriminante_falha/`:

- `protocolo_pre_execucao.md`: critérios registrados antes das simulações.
- `manifesto_pre_execucao.json`: versões, HEAD, hashes, desenho e sementes.
- `amostra.csv`: 20 pares sorteados e referência nominal, com parâmetros.
- `bruto_controles.csv`: quatro linhas novas comparadas, incluindo decomposição bruta, bateria e conjuntos de tarefas.
- `identidade.json`: chave, todos os campos comparados, valores e hexadecimais da divergência.
- `execucao_controles.log`: registro da interrupção.
- `verificacao_final.json`: integridade dos arquivos protegidos e checksums dos artefatos.

**Integridade:** os dois YAML nominais, os parâmetros e todos os módulos de `src/modelo/` mantêm seus hashes originais. Nenhum `git add`, `git commit` ou `git push` foi executado. As pastas antigas não foram alteradas. O clone e o ambiente isolado foram criados em `~/TCC2_discriminante`.

### O que a monografia pode afirmar

Este lote confirma apenas a população usada no sorteio e documenta uma falha de identidade integral. **Não permite afirmar que assistência, fuga ou interação causam a perda de robustez.** A definição de denominador fixo foi identificada na inspeção do código e consta do pré-registro; não deve ser confundida com conclusão de um fatorial concluído. A próxima etapa é reconciliar a divergência de identidade e obter autorização para retomar o desenho, preservando estes resultados.


## Rechecagem integral autorizada — leitura textual e round_trip

**Estado atual: PARADO. Diferença restrita a `competencia_minima_inicial`; nenhum campo dinâmico divergente.** Esta seção atualiza a cobertura dos controles; a interrupção inicial e seus arquivos permanecem preservados. H1–H3 continuam sem interpretação.

### 1. Valor literal, sem pandas

Leitura com `csv.DictReader` da biblioteca padrão sobre o texto de `outputs/diagnosticos/SAT_GOV_20260919/bruto.csv`. Linha física 73: kind=GOV, perfil=2, instância=j6010_1.sm, semente=3, arranjo=adaptativa.

- Texto exato: **`0.24332019624229823`**.
- `float(texto).hex()`: **`0x1.f251dbea89292p-3`**.
- `pd.read_csv(..., float_precision='round_trip')`: **`0x1.f251dbea89292p-3`**.
- Reexecução: **`0.24332019624229825`**, hexadecimal **`0x1.f251dbea89293p-3`**.

A referência já era lida com `round_trip` no primeiro controle. A conferência nativa adicional confirma que **a conversão do texto nesta leitura não causou a divergência**. Não demonstra como o valor foi originalmente calculado ou serializado.

### 2. Todos os controles do desenho, sem parada na primeira diferença

Reexecutados os controles dos **21 pares pré-registrados**, com os mesmos quatro arquivos e quatro sementes. São 30 combinações distintas de perfil/arranjo, reutilizadas entre pares; 480 execuções por canto e **960 ao todo**. O escopo é a amostra solicitada, não uma nova reexecução da grade inteira de 81 perfis.

| Controle | Execuções | Campos por linha (além da chave) | Comparações | Execuções divergentes | Campo divergente |
|---|---:|---:|---:|---:|---|
| 00: limiar + constante, referência v1 | 480 | 53 | 25.440 | 120 | competencia_minima_inicial |
| 11: logístico + logística, referência v2 | 480 | 50 | 24.000 | 120 | competencia_minima_inicial |
| Total | **960** | — | **49.440** | **240** | único campo |

Todas as **240 diferenças** têm o mesmo tamanho: **+2,7755575615628914 × 10⁻¹⁷ = 1 ULP**, com os dois hexadecimais acima. Ocorrem exclusivamente na **semente 3**, em todos os 30 perfis/arranjos × quatro instâncias × dois cantos. A listagem integral das 240 chaves, linhas de origem, textos literais, valores, hexadecimais e deltas está em `rechecagem_round_trip/divergencias_todas.csv`.

**Zero divergências** em `makespan`, `TW`, `TL`, `TU`, `TR`, `taxa_falha_efetiva`, `p1_omissao` e `N_req`, e também zero nos demais campos arquivados, exceto o campo inicial indicado. Todas as 960 execuções terminaram, sem violações. As chaves são únicas. Para cada valor numérico de referência comparado, o parser `round_trip` foi também conferido contra `float()` aplicado ao token literal do CSV: nenhuma diferença entre leitores.

### 3. Decisão segundo o critério da autora

Aplica-se o segundo caso: **sobra diferença somente na competência mínima inicial, sem diferença dinâmica. Parar e reportar.** Não executar os cantos mistos, não afrouxar identidade e não interpretar mecanismos. Arredondamento entre plataformas é uma hipótese ainda não testada; não há evidência suficiente para atribuir especificamente a Mac versus Windows.

Comando executado:

```bash
.venv/bin/python -u research/conferencia_round_trip_78.py > outputs/diagnosticos/20260922_discriminante_falha/rechecagem_round_trip.log 2>&1
```

Saídas novas, preservando a tentativa original:

- `rechecagem_round_trip/valor_literal.json` — token textual e linha de origem.
- `rechecagem_round_trip/bruto.csv` — 960 execuções novas.
- `rechecagem_round_trip/divergencias_todas.csv` — todas as 240 diferenças.
- `rechecagem_round_trip/resumo.json` — contagens, campos e integridade dos arquivos protegidos.
- `rechecagem_round_trip/verificacao_entrega.json` — hashes desta entrega e do relatório atualizado.
- `rechecagem_round_trip.log` — execução completa, sem parada antecipada; código de saída 0 indica conclusão da conferência, não aprovação da identidade.

Código do modelo e configurações nominais continuam idênticos aos hashes pré-registrados. Nenhuma publicação Git foi realizada.


## Retomada autorizada — exceção de plataforma registrada antes dos cantos mistos

A autora informou ter verificado em Linux x86, Python 3.10 e NumPy 2.2.6, as oito combinações de instância/arranjo da semente 3: `competencia_minima_inicial` reproduziu `0x1.f251dbea89292p-3`, idêntico ao arquivo. A causa foi identificada pela autora como arredondamento de plataforma no `rng.normal` inicial. **Proveniência:** verificação externa comunicada pela autora nesta sessão; não executamos Linux nem recebemos seu log bruto. A conferência local independente demonstra que o parser não explica a diferença e que não há diferença nos campos dinâmicos arquivados das 960 execuções controladas. Isso não prova identidade de todos os estados internos ou de outras configurações.

**Ambiente desta execução:** Python 3.12.14 (Clang 22.1.3), NumPy 2.5.2, macOS ARM64. Valor local: `0x1.f251dbea89293p-3`; diferença positiva de 1 ULP.

**Novo critério, autorizado pela autora:** todos os campos devem continuar idênticos por `float.hex()` (textos/bools por igualdade), com exceção exclusiva de `competencia_minima_inicial`, que admite distância de até 1 ULP. Qualquer outra diferença interrompe a análise. Não aplicamos tolerância global nem alteramos referências, sorteios ou parâmetros.

Revalidação integral concluída antes de executar os cantos mistos: **960/960 controles aprovados pelo critério atualizado**, 49.440 comparações de campos, 240 exceções de exatamente 1 ULP apenas na competência mínima inicial, zero diferenças não permitidas. Evidência: `fatorial_completo/controle_criterio_atualizado.json`. O critério original e as duas interrupções permanecem preservados como histórico; o estado atual é retomado sob a autorização acima. A amostra, a semente e os testes de H1–H3 permanecem os do pré-registro.


## Resultado final — fatorial concluído sob o critério atualizado

**Resumo:** os controles passaram com a única exceção de plataforma autorizada; **1.920/1.920 execuções completas**, zero violações. Foram reaproveitados os 960 controles integralmente reexecutados e rodadas 960 execuções novas nos cantos mistos. Nenhum parâmetro foi ajustado e nenhuma configuração nominal foi alterada.

### 1. Vereditos H1–H3

| Hipótese | Veredito | Evidência discriminante |
|---|---|---|
| H1: assistência melhora o centralizado e desloca o contraste | **Sustentação parcial, não explicação única** | Assistência isolada reduz a falha centralizada em 15/20 pares; o padrão completo pré-registrado (melhora centralizada maior que a adaptativa, mais pedidos e sucessos) ocorre em 9/20, dos quais 7 são novas inversões. Assistência isolada eleva o contraste em 12/20 e o reduz em 8/20. |
| H2: fuga altera o denominador / conjunto executado | **Derrubada na forma proposta** | Todas as 1.920 execuções executam e concluem as mesmas 60 tarefas; denominador=60 em todos os cantos. Os conjuntos de IDs coincidem nas 480 chaves perfil/arranjo/instância/semente. A fuga pode alterar o numerador, mas não por mudar esse denominador ou excluir tarefas. |
| H3: só os dois juntos produzem a inversão | **Padrão presente em parte das células; sinergia não demonstrada** | Em 6 das 14 novas inversões da amostra, apenas o canto conjunto fica positivo. Nas outras 8, ao menos uma mudança isolada já inverte. Todos os 20 IC95 da interação incluem zero; também inclui zero o do par nominal. |

**Precisão:** estes são padrões de médias pareadas, não 20 provas independentes. Na assistência isolada, apenas um IC95 do deslocamento do contraste é inteiramente positivo (par 34/51: +2,917 p.p. [0,156; 5,677]); há também um inteiramente negativo (68/66: −1,875 p.p. [−3,453; −0,297]). Os demais incluem zero. A assistência é um fator causal manipulado no fatorial, mas os contadores associados não demonstram sozinhos toda a cadeia de mediação.

### 2. Onde o sinal inverte

Dos 20 pares sorteados por serem positivos na v2, **6 já eram positivos na v1**; portanto, apenas **14 são novas inversões**. Entre essas 14:

- 3 invertem com assistência isolada;
- 6 invertem com fuga isolada;
- 1 pertence aos dois grupos acima;
- 6 só ficam positivos com as duas mudanças juntas.

Em **19/20** pares o contraste aumenta de 00 para 11; no par 68/66 ele diminui e continua positivo. Na passagem completa v1→v2, o braço centralizado melhora em **20/20** pares. O adaptativo piora em **12/20**; nos outros oito também melhora. Isso impede atribuir toda a mudança apenas a melhora centralizada ou apenas a piora adaptativa. A decomposição por par abaixo mostra ambas.

Nos 14 pares que realmente invertem, oito já invertem em algum canto isolado: logo H3 não é necessária em geral. Nos seis restantes, cruzar zero apenas em 11 não prova sinergia; efeitos aditivos podem produzir o mesmo padrão. Não foi ajustado o desenho para estreitar os intervalos.

### 3. Contrastes completos com IC95

Valores em **pontos percentuais** de falha efetiva, adaptativa − centralizada. IC95 t sobre quatro médias de instância, com quatro sementes pareadas em cada uma. 00=limiar/constante; 10=logístico/constante; 01=limiar/logística; 11=logístico/logística. Sinais pontuais não equivalem a IC excluindo zero.

| Par | Perfis A/C | D00 [IC95] | D10 [IC95] | D01 [IC95] | D11 [IC95] | Padrão pontual |
| --- | --- | --- | --- | --- | --- | --- |
| amostra_01 | 56/65 | +0.104 [-0.227; +0.436] | -0.417 [-5.466; +4.633] | +0.208 [-0.455; +0.871] | +1.562 [-4.547; +7.672] | já positivo em 00 |
| amostra_02 | 17/9 | +0.729 [-5.111; +6.569] | -0.313 [-3.296; +2.671] | -1.562 [-3.033; -0.092] | +0.937 [-3.473; +5.348] | já positivo em 00 |
| amostra_03 | 62/68 | -1.562 [-6.623; +3.498] | -0.729 [-2.555; +1.097] | +1.667 [-5.159; +8.493] | +1.667 [-7.112; +10.446] | fuga isolada |
| amostra_04 | 2/18 | -0.417 [-3.013; +2.180] | -2.083 [-4.564; +0.397] | +0.938 [-3.473; +5.348] | +1.146 [-4.567; +6.859] | fuga isolada |
| amostra_05 | 62/73 | -1.562 [-6.262; +3.137] | -3.542 [-9.385; +2.301] | +1.562 [-3.260; +6.385] | +1.875 [-2.194; +5.944] | fuga isolada |
| amostra_06 | 11/18 | -0.417 [-3.013; +2.180] | +1.146 [-3.554; +5.846] | +0.938 [-3.473; +5.348] | +0.938 [-8.429; +10.304] | assistência e fuga isoladas |
| amostra_07 | 68/66 | +1.562 [-1.834; +4.959] | -0.313 [-4.449; +3.824] | -0.104 [-6.874; +6.665] | +0.625 [-11.364; +12.614] | já positivo em 00 |
| amostra_08 | 64/9 | -3.646 [-7.526; +0.234] | -0.625 [-8.664; +7.414] | -3.646 [-9.203; +1.911] | +1.250 [-5.109; +7.609] | só conjunto |
| amostra_09 | 7/9 | +0.417 [-2.964; +3.797] | +1.562 [-4.099; +7.224] | -1.146 [-3.926; +1.634] | +2.917 [-7.594; +13.428] | já positivo em 00 |
| amostra_10 | 8/19 | +0.521 [-4.903; +5.944] | -0.625 [-6.973; +5.723] | -1.771 [-5.689; +2.147] | +1.875 [-6.761; +10.511] | já positivo em 00 |
| amostra_11 | 79/49 | -1.563 [-7.884; +4.759] | -2.292 [-9.880; +5.297] | +1.875 [-2.734; +6.484] | +1.979 [-5.024; +8.983] | fuga isolada |
| amostra_12 | 61/55 | -0.521 [-4.762; +3.720] | +1.667 [-9.919; +13.252] | -0.208 [-4.055; +3.639] | +1.458 [+0.602; +2.314] | assistência isolada |
| amostra_13 | 60/3 | -5.208 [-10.415; -0.002] | -3.021 [-7.993; +1.952] | -4.062 [-13.159; +5.034] | +0.313 [-1.667; +2.292] | só conjunto |
| amostra_14 | 8/14 | +0.208 [-3.932; +4.349] | +3.750 [-4.861; +12.361] | -2.083 [-7.074; +2.908] | +1.354 [-2.411; +5.119] | já positivo em 00 |
| amostra_15 | 62/77 | -1.250 [-8.692; +6.192] | -0.729 [-8.335; +6.876] | +1.042 [-6.719; +8.802] | +1.771 [-7.658; +11.200] | fuga isolada |
| amostra_16 | 78/51 | -0.625 [-7.568; +6.318] | -1.042 [-6.935; +4.851] | -2.708 [-6.360; +0.943] | +0.729 [-4.667; +6.126] | só conjunto |
| amostra_17 | 34/51 | -1.458 [-5.305; +2.389] | +1.458 [-3.151; +6.068] | -1.042 [-4.889; +2.805] | +3.125 [+1.745; +4.505] | assistência isolada |
| amostra_18 | 31/19 | -4.583 [-11.826; +2.659] | -3.646 [-16.540; +9.249] | -4.375 [-12.116; +3.366] | +1.146 [-6.574; +8.866] | só conjunto |
| amostra_19 | 67/10 | -3.542 [-11.433; +4.350] | -1.875 [-6.484; +2.734] | -4.271 [-14.773; +6.231] | +0.521 [-5.492; +6.534] | só conjunto |
| amostra_20 | 64/19 | -3.854 [-8.198; +0.489] | -2.917 [-12.448; +6.615] | -3.854 [-12.522; +4.814] | +0.312 [-5.869; +6.494] | só conjunto |
| nominal | 62/18 | -4.792 [-11.411; +1.827] | -2.396 [-6.773; +1.981] | -2.604 [-3.239; -1.969] | +0.104 [-5.531; +5.740] | só conjunto |

Apenas dois dos 20 contrastes selecionados têm IC95 de 11 inteiramente positivo: 61/55 e 34/51. **Não chamar os demais de inversões estatisticamente estabelecidas:** são inversões do sinal da estimativa, com incerteza. A seleção foi feita usando os mesmos dados/sementes, e os perfis são compartilhados entre pares; os resultados não estimam a prevalência de mecanismos na população dos 643 pares nem em novas instâncias.

### 4. Qual braço muda — passagem 00→11

Mudanças em pontos percentuais. Negativo significa que a taxa de falha do braço caiu. IC95 completos das mudanças de cada braço e dos efeitos isolados estão em `efeitos_IC95.csv`; a tabela abaixo é a decomposição pontual, não um teste de significância adicional.

| Par (A/C) | Δ centralizada | Δ adaptativa | Δ contraste A−C |
| --- | --- | --- | --- |
| amostra_01 (56/65) | -0.625 | +0.833 | +1.458 |
| amostra_02 (17/9) | -4.167 | -3.958 | +0.208 |
| amostra_03 (62/68) | -1.458 | +1.771 | +3.229 |
| amostra_04 (2/18) | -3.125 | -1.562 | +1.562 |
| amostra_05 (62/73) | -1.667 | +1.771 | +3.437 |
| amostra_06 (11/18) | -3.125 | -1.771 | +1.354 |
| amostra_07 (68/66) | -0.521 | -1.458 | -0.938 |
| amostra_08 (64/9) | -4.167 | +0.729 | +4.896 |
| amostra_09 (7/9) | -4.167 | -1.667 | +2.500 |
| amostra_10 (8/19) | -3.437 | -2.083 | +1.354 |
| amostra_11 (79/49) | -2.500 | +1.042 | +3.542 |
| amostra_12 (61/55) | -0.312 | +1.667 | +1.979 |
| amostra_13 (60/3) | -4.583 | +0.938 | +5.521 |
| amostra_14 (8/14) | -3.229 | -2.083 | +1.146 |
| amostra_15 (62/77) | -1.250 | +1.771 | +3.021 |
| amostra_16 (78/51) | -2.812 | -1.458 | +1.354 |
| amostra_17 (34/51) | -2.812 | +1.771 | +4.583 |
| amostra_18 (31/19) | -3.437 | +2.292 | +5.729 |
| amostra_19 (67/10) | -3.646 | +0.417 | +4.062 |
| amostra_20 (64/19) | -3.437 | +0.729 | +4.167 |
| nominal (62/18) | -3.125 | +1.771 | +4.896 |

### 5. Referência nominal: quatro instâncias × quatro sementes

**Esta é a referência nominal dentro da grade de governança, não o experimento nominal completo de 16 instâncias × 12 sementes.** Não se deve substituir a conclusão daquele experimento por este pequeno subconjunto. Aqui D11=+0,104 p.p., IC95 [−5,531; +5,740], compatível com os dois sinais; a identidade com o bruto v2 foi confirmada.

- Centralizada: falha **30,729% → 27,604%** (−3,125 p.p.).
- Adaptativa: falha **25,938% → 27,708%** (+1,771 p.p.).
- Contraste: **−4,792 → +0,104 p.p.**, mudança +4,896 p.p., IC95 [+0,867; +8,924]. Um IC da mudança excluindo zero não faz o IC do contraste final excluir zero.
- Assistência isolada: centralizada −1,979 p.p., adaptativa +0,417 p.p.; desloca D em +2,396 p.p., IC95 [−2,015; +6,806].
- Fuga isolada: centralizada −0,833 p.p., adaptativa +1,354 p.p.; desloca D em +2,188 p.p., IC95 [−3,970; +8,345].
- Interação: **+0,313 p.p.**, IC95 [−7,078; +7,703]. Os dois efeitos isolados explicam aritmeticamente +4,583 dos +4,896 p.p. da mudança; o resto é a interação estimada, muito imprecisa. Não há demonstração de sinergia.

Leituras médias por execução para o par nominal:

| Canto | Braço | Falha (%) | N_req | N_success | N_fail | N_blocked |
| --- | --- | --- | --- | --- | --- | --- |
| 00 | adaptativa | 25.938 | 140.938 | 102.125 | 38.812 | 0.062 |
| 00 | centralizada | 30.729 | 0.000 | 0.000 | 0.000 | 118.562 |
| 01 | adaptativa | 27.292 | 144.812 | 107.875 | 36.938 | 0.000 |
| 01 | centralizada | 29.896 | 0.000 | 0.000 | 0.000 | 131.000 |
| 10 | adaptativa | 26.354 | 121.875 | 86.000 | 35.875 | 1.688 |
| 10 | centralizada | 28.750 | 73.750 | 39.062 | 34.688 | 33.562 |
| 11 | adaptativa | 27.708 | 148.438 | 108.188 | 40.250 | 2.438 |
| 11 | centralizada | 27.604 | 90.312 | 52.875 | 37.438 | 35.625 |

| Canto | Braço | Fração P1 | Fração fuga | Executadas | Bateria média | Confiança final |
| --- | --- | --- | --- | --- | --- | --- |
| 00 | adaptativa | 0.4302 | 0.0000 | 60 | 0.7307 | 0.9210 |
| 00 | centralizada | 0.5385 | 0.0000 | 60 | 0.7010 | 0.2500 |
| 01 | adaptativa | 0.4042 | 0.1346 | 60 | 0.7226 | 0.9479 |
| 01 | centralizada | 0.5208 | 0.2067 | 60 | 0.6975 | 0.2500 |
| 10 | adaptativa | 0.4052 | 0.0000 | 60 | 0.7280 | 0.9247 |
| 10 | centralizada | 0.4635 | 0.0000 | 60 | 0.7418 | 0.5068 |
| 11 | adaptativa | 0.3979 | 0.0869 | 60 | 0.7435 | 0.9357 |
| 11 | centralizada | 0.4448 | 0.1618 | 60 | 0.7488 | 0.5697 |

**Todas as células, não apenas a referência:** `leituras_por_braco_medias.csv` contém as 168 combinações par×canto×braço, com todos os indicadores pedidos. `leituras_por_braco_IC95.csv` contém as mesmas leituras com IC95 para cada indicador. Incluem N_req, N_success, N_fail, N_blocked, p2_bloqueio, as duas definições explícitas de fração de fuga, tarefas executadas/concluídas, numerador/denominador, bateria média e confiança final. Definições e fronteiras estão no pré-registro.

### 6. O que a monografia pode afirmar

> No diagnóstico fatorial dos 20 pares amostrados que favoreciam o centralizado na v2, seis já o favoreciam na v1 e 14 apresentaram nova inversão do sinal estimado. A suavização da assistência contribui em parte das células, mas não explica sozinha todos os casos. A fuga também modifica o contraste mesmo com assistência por limiar, sem alterar o denominador ou o conjunto final de tarefas: todas as execuções completam as mesmas 60 tarefas. Em seis novas inversões o cruzamento ocorre somente com as duas mudanças juntas, porém os intervalos da interação incluem zero. O diagnóstico não sustenta uma causa única nem sinergia demonstrada, e seus sinais pontuais devem ser lidos com a incerteza de quatro instâncias e a seleção de células pelo resultado.

Retirar qualquer afirmação categórica de que a perda de robustez decorre **apenas** de abrir assistência no centralizado. Também não sustentar H2 como diluição do denominador, nem equiparar cruzamento conjunto a interação estatisticamente comprovada. Não se avaliou mediação por tarefa nem se alinhou RNG por evento; não atribuir o efeito remanescente da fuga a uma cadeia cognitiva específica sem outro teste.

### 7. Arquivos, comandos e verificação

Todos os arquivos novos ficam em `outputs/diagnosticos/20260922_discriminante_falha/fatorial_completo/`. As saídas antigas, o protocolo inicial e a primeira lista de diferenças permanecem intactos.

```bash
.venv/bin/python research/fatorial_78.py controle
.venv/bin/python research/fatorial_78.py executar
.venv/bin/python research/fatorial_78.py analisar
.venv/bin/python research/relatar_fatorial_78.py
```

- `controle_criterio_atualizado.json`: revalidação campo a campo e todas as exceções.
- `criterio_pre_cantos_mistos.md` e `manifesto_retomada.json`: emenda registrada antes da execução.
- `bruto_mistos.csv` / `bruto_completo.csv`: 960 novos resultados / 1.920 resultados dos quatro cantos.
- `contrastes_IC95.csv` e `diferencas_por_instancia.csv`: 84 contrastes e suas quatro médias pareadas.
- `efeitos_IC95.csv`: assistência, fuga, interação e mudanças por braço, 336 estimativas com IC95.
- `classificacao_hipoteses.csv`: classificação transparente das 21 células, sem eleger variante.
- `leituras_por_braco_medias.csv` / `leituras_por_braco_IC95.csv`: decomposição de todas as células, 168 linhas largas / 2.520 estimativas com IC95.
- `verificacoes.json`: integralidade, ausência de violações e igualdade dos conjuntos de tarefas.
- `verificacao_independente_analise.json`: segunda implementação das contas com `csv` e `statistics`, sem as agregações pandas da análise principal.

A segunda implementação conferiu **2940 linhas de estimativas/IC95**; maior diferença entre médias ou limites = **5.68e-14**, inferior a 1e-12 (checagem das tabelas, não tolerância dos controles de identidade). Os hashes de todos os arquivos protegidos permanecem iguais. Sem alterações do modelo, dos YAML nominais, das referências e sem `git add`, `commit` ou `push`.
