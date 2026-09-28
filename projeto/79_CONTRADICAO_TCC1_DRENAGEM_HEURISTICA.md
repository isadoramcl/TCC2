# 79 — Contradição reportada no TCC1: drenagem heurística

**Estado atual: v3 adotada. Interrupções abaixo são histórico; critérios reconciliados e resultados finais ao fim.**

**Data:** 28/09/2026. **Estado: INTERROMPIDO no controle prévio de identidade. Não adotado como v3.**

## 1. Escopo e preservação

Trabalho no clone separado `~/TCC2_discriminante`, HEAD `48f567c`. A solicitação integral e os critérios escritos pela autora estão preservados em `outputs/diagnosticos/20260928_drenagem_heuristica/controle_previo/solicitacao_autora.txt`. Não foram alterados `config/parametros.yaml`, os módulos do modelo, os YAML nominais ou README. Não houve `git status`, `git add`, `git commit` ou `git push`. Nenhum diretório de outputs foi apagado, renomeado ou sobrescrito.

## 2. Fonte e causalidade: o que foi conferido

Leitura direta do PDF local `docs/snapshots/TCC_I_referencia_2026-09-15.pdf`:

- Página 26, narrativa de §4.1: a entrega imediata por satisficing reduz a cobrança percebida e proporciona alívio temporário da pressão local; o retrabalho oculto aumenta a pressão futura, reduzindo depois a bateria.
- Página 32, §4.4.3, Porta 1, linha 3: “Drena B(t) em taxa heurística acelerada”. Na página 33, Porta 3 usa taxa analítica sustentável.

Os dois trechos citados na solicitação estão presentes. A proposta da autora resolve a tensão interpretativa a favor da economia de esforço. Ressalva de leitura: pressão e bateria são estados distintos; os dois trechos, isoladamente, não constituem uma impossibilidade algébrica. A escolha de igualar coeficientes é uma decisão de formulação cuja justificativa completa envolve também as fontes de satisficing. Simon, Payne/Bettman/Luce e Kim não foram reavaliados nesta etapa interrompida.

No código, `pressao(t)` usa o tempo e a fração de tarefas concluídas para medir desvio contra o CPM; mais conclusões no mesmo instante podem diminuir a pressão, ou mantê-la nos limites do clip. `fator_omissao` reduz a duração antes do arredondamento. O caminho erro → dívida/reparo → ocupação/atraso → pressão permanece no código independentemente da comparação entre coeficientes de drenagem; isso é observação da estrutura, não demonstração experimental de todas as trajetórias do laço.

Derivação proposta pela autora: fixar k_heuristico=k_analitico=0,04; a economia viria do tempo reduzido por fator_omissao=0,75, sem novo parâmetro. **Limite a verificar no teste futuro:** no simulador as durações são discretas (`ceil` e mínimo de um período), a drenagem depende do esforço e a bateria tem piso zero. Logo 25% é a aproximação nominal sob estado/intensidade iguais, não uma economia estritamente garantida em toda tarefa. Nenhum teste foi ajustado para esconder esses casos de borda.

## 3. Teste prévio da inversão da checagem

Antes de modificar produção, foram criadas classes experimentais **em memória**, copiando o código atual e invertendo somente os predicados solicitados:

- Legado: `k_he <= k_an` → `k_he > k_an`.
- MVP: `kh <= ka` → `kh > ka`.
- Mensagem atualizada para a regra proposta; dependência do MVP ligada à cópia experimental do legado.

Executado o nominal histórico completo com k_heuristico reposto em 0,10, nos dois códigos: **384 pares / 768 simulações**, todas concluídas. A comparação usa os **49 campos numéricos efetivamente presentes no CSV**, incluindo `semente` e `violacoes`, por `float.hex()`, com leitura `float_precision='round_trip'`. Nenhuma exceção nova ou tolerância foi aplicada.

### Antes/depois local: a inversão é inerte para a dinâmica, não para o diagnóstico

**Único campo modificado pela inversão: `violacoes`, de 0 para 1 em 384/384 pares.** Todos os outros 48 campos numéricos são idênticos entre o código atual e a cópia com a checagem invertida. Com 0,10 > 0,04, o parâmetro histórico necessariamente infringe a nova regra. Portanto, exigir simultaneamente a checagem invertida e identidade dos 49 campos com o arquivo histórico é incompatível: o próprio campo de validação integra o controle.

Não foi omitido esse campo, ignorada a nova violação ou criada uma exceção silenciosa de execução histórica.

### Comparação com o CSV histórico: diferenças anteriores à alteração

| Campo | Execuções com diferença no código atual | Maior diferença absoluta | Maior distância |
|---|---:|---:|---:|
| competencia_maxima_inicial | 96 | 1,1102230246251565e-16 | 1 ULP |
| competencia_minima_inicial | 64 | 5,551115123125783e-17 | 1 ULP |
| competencia_maxima_final | 96 | 1,1102230246251565e-16 | 1 ULP |
| confianca_media_final | 4 | 1,1102230246251565e-16 | 2 ULP |

São **160 execuções distintas** com pelo menos uma diferença pré-existente; as contagens por campo se sobrepõem. As mesmas diferenças aparecem na cópia com checagem invertida, acrescidas das 384 diferenças em `violacoes`. Makespan, TW, TL, TU, TR, taxa de falha, contagens de portas e pedidos, e os cinco indicadores publicados não diferem nesse controle histórico. Isso não autoriza chamar os 49 campos de idênticos.

A confiança final difere em quatro execuções centralizadas:

| Instância | Semente | Referência hex | Reexecução hex | ULP |
|---|---:|---|---|---:|
| j6019_1.sm | 6 | 0x1.8941ff61e9095p-2 | 0x1.8941ff61e9094p-2 | 1 |
| j6021_1.sm | 6 | 0x1.6a0f2b93af957p-2 | 0x1.6a0f2b93af955p-2 | 2 |
| j6032_1.sm | 5 | 0x1.1b794f6cd0fa1p-1 | 0x1.1b794f6cd0fa0p-1 | 1 |
| j6038_1.sm | 6 | 0x1.16847a5223038p-1 | 0x1.16847a5223037p-1 | 1 |

Ambiente: Python 3.12.14, NumPy 2.5.2, macOS ARM64. O parecer 78 tinha autorização específica de até 1 ULP **apenas na competência mínima inicial naquele teste**. Ela não cobre competências máximas ou confiança final deste conjunto. A origem dessas novas diferenças não foi comprovada; não foi presumida como plataforma nem considerada nula por conveniência.

## 4. Critério de adoção e ponto de parada

A solicitação integral preservada é o protocolo de referência: zero violações e conclusão; identidade histórica; teste contrafactual de custo por período e por tarefa; quatro contrastes negativos com IC95 dentro e fora da amostra; adoção teórica independente de melhora dos resultados; tabelas v2/v3; validação completa; só depois, k_fuga separado.

**O controle histórico literal falhou. Conforme a ordem de parar diante de divergências, as etapas seguintes não foram executadas.** Não foram simulados os candidatos com k_heuristico=0,04, não foram confrontados os números de referência da candidata, não foi promovida v3, não foi separado k_fuga. O teste novo de custo ainda não foi implementado: seu desenho deve explicitar as condições de estado pareado e arredondamento, sem afirmar uma redução estrita universal que tarefas de um período não podem satisfazer.

Para retomar sem alterar o alvo silenciosamente, é necessário reconciliar:

1. Se a identidade dinâmica deve excluir **explicitamente** `violacoes`, mantendo e reportando a violação esperada na configuração histórica, ou se outra política histórica de validação é desejada.
2. As diferenças pré-existentes em competências e confiança final: confirmação da causa e decisão sobre critério de identidade, ou ambiente que reproduza integralmente o arquivo.

Não foi adotada nenhuma dessas alternativas por conta própria. A mudança proposta permanece pendente; os números não foram ajustados.

## 5. Evidência reproduzível

```bash
.venv/bin/python -u research/controle_previo_79.py
```

Saídas em `outputs/diagnosticos/20260928_drenagem_heuristica/controle_previo/`:

- `manifesto.json`: 49 campos, versões e hashes das configurações e módulos antes do experimento.
- `bruto.csv`: 768 execuções, variantes anterior e checagem invertida.
- `divergencias_referencia.csv`: cada diferença frente ao arquivo, com chave, valor, hexadecimal e delta.
- `divergencias_antes_depois.csv`: as 384 mudanças no diagnóstico de violações.
- `resumo.json` e `execucao.log`: contagens e conclusão do experimento.
- `solicitacao_autora.txt`: protocolo recebido, sem alteração.
- `hashes_entrega.json`: integridade da entrega.

Os hashes dos arquivos do modelo e configurações foram conferidos ao final e permanecem iguais aos anteriores. O código de diagnóstico não grava nos arquivos de produção.


## Reconciliação autorizada — antes da etapa 1

A autora corrigiu o item 1: identidade em **48 campos, excluindo violacoes**. Guarda testada separadamente: k_h=0,10 produz exatamente uma violação; k_h=0,04 produz zero. O conflito anterior era erro da especificação recebida, não achado científico sobre o modelo.

Não há host x86 conectado nem docker/podman nesta sessão; aplicada a alternativa Mac autorizada. A autora informou repetição em Linux x86, Python 3.10 / NumPy 2.2.6: 384 execuções e 49 campos idênticos ao arquivo. Evidência externa comunicada pela autora, não execução Linux realizada aqui. A causa informada é arredondamento de rng.normal no macOS ARM, propagado à confiança por Crowder. Ambiente local: Python 3.12.14 / NumPy 2.5.2. Critério local: float.hex em todos os 48 campos, exceto competencia_* e confianca_media_final, que admitem até 2 ULP; nenhuma tolerância para outros campos. Não corrigir o gerador para imitar plataforma.

Risco residual: perto de empates, diferenças de poucos ULP podem mudar max(apoio,key=competencia) e, então, a trajetória. Não ocorreu nos indicadores das 384 execuções controladas. A logística torna extremamente improvável uma troca de decisão pelo deslocamento mínimo da probabilidade, mas não oferece garantia matemática de impossibilidade; outras comparações rígidas de competência também exigem cuidado fora da amostra testada. A conclusão empírica é restrita ao controle observado.

Antes de alterar produção: quatro testes novos executados, com 11 falhas esperadas em subcasos de custo/guarda e nenhum erro de execução; log preservado. Snapshot v2 em etapa1/snapshot_v2, além dos arquivos históricos config/parametros_v2.yaml e config/mvp_v2.yaml. O teste mede drenagem real num estado pareado e declara o caso unitário sem economia estrita por arredondamento. As etapas 2 e 3 permanecem condicionadas aos controles e à reprodução das referências da etapa 1.


## Encerramento da etapa 2 e pré-registro da etapa 3

Etapa 1 reproduziu os dez contrastes/IC95 nas quatro casas reportadas. Etapa 2: 4.704/4.704 completas, zero violações; nominal 384, fora48 1.152, aleatório24 576 e governança 2.592. Suíte reconciliada: 106 testes aprovados. Os cinco contrastes dos três conjuntos de validação têm IC95 negativo. Governança: falha efetiva negativa em 504/1.215 pares, contra 564 na v2; resultado não universal nem otimizado.

Etapa 3 iniciada somente após esse fechamento: k_fuga=0,10 congelado, kh=ka=0,04 mantidos. Modificar apenas a drenagem de adiamento em ambos os laços, sem mudar o custo da execução heurística. Configurações históricas sem k_fuga continuam usando kh, permitindo reproduzir etapas anteriores. Teste real de um adiamento falhou antes em ambos os laços (0,008 medido versus 0,020 esperado) e será repetido após a alteração. Repetir o conjunto completo, apresentar etapa2/etapa3 separadas e registrar qualquer mudança de sinal, sem eleger resultado conveniente.


## Resultado final — v3 adotada; três etapas concluídas separadamente

**Execução local em macOS ARM; sem Git de escrita.** A identidade segue o critério reconciliado e a exceção de plataforma autorizada, não a regra original retratada. A mudança foi adotada por coerência da formulação; nenhum parâmetro foi escolhido por melhorar resultado.

### Controles e testes

- **1a:** 384 execuções × 48 campos numéricos; zero diferenças não permitidas. As 260 diferenças de plataforma estão em 160 execuções e se limitam a competencia_* / confianca_media_final, até 2 ULP. Controle repetido após a etapa 3 com o mesmo resultado. Evidência Linux exata foi informada pela autora, sem nova execução x86 nesta sessão.
- **1b:** guarda dispara exatamente uma vez nas 384 execuções históricas com kh=0,10; não dispara nas candidatas com kh=0,04. Teste unitário adicional cobre legado/MVP e ambos os arranjos.
- **Custo real de bateria:** mesma tarefa/estado/pressão/eficiência, sem erro ou fuga. Durações analíticas 4/8/12 contra heurísticas 3/6/9: intensidade igual e custo total 25% menor. Exemplo de oito períodos: 0,064 → 0,048. Controle negativo kh=0,10 reprova a economia. Duração de um período dá custo igual por arredondamento, explicitamente testado; não alegar economia estrita universal.
- **Etapa 1:** todas as dez médias e os vinte limites dos IC95 reproduziram as quatro casas publicadas pela autora. 768/768 concluídas, zero violações.
- **Etapa 2:** 4.704/4.704 concluídas, zero violações; suíte 106 testes aprovada. Inclui as 768 já verificadas na etapa 1, sem duplicá-las como amostras novas.
- **Etapa 3:** novo lote completo de 4.704/4.704 concluídas, zero violações; suíte final **107 testes aprovada**. Teste de fuga falhou antes e passou depois nos dois laços: kh=0,04 e E=0,2, custo do adiamento 0,008 → 0,020; variar kh mantendo k_fuga fixo não altera essa drenagem.

A primeira suíte pós-mudança teve 60 falhas em seis métodos de teste: identidade C2, identidade 1fd22ff, escalares Crowder, dois controles de portões e runner TL. As três primeiras famílias diferiam só na guarda; agora verificam explicitamente as listas de violações antigas/novas e continuam comparando todos os demais campos/estados/RNG. Os controles de portões passaram a repor kh histórico para comparar saídas históricas. No auditor de TL, sum() do Python recente divergia do acúmulo sequencial +=; a verificação agora reproduz a ordem temporal, sem mudar a dinâmica ou TL. Logs da falha e da aprovação foram preservados.

### Resultados lado a lado

Contraste adaptativa − centralizada; IC95 t sobre médias de sementes por instância. Etapa 2 muda apenas kh e a guarda; etapa 3 muda apenas a drenagem da fuga para k_fuga=0,10. Não atribuir a etapa 1 os números da etapa 3.

| Conjunto | Indicador | v2 | v3 etapa 1/2 | v3 final (etapa 3) |
| --- | --- | --- | --- | --- |
| nominal | Atraso relativo | -0.9429 [-1.0864; -0.7994] | -0.8682 [-0.9866; -0.7497] | -0.9100 [-1.0473; -0.7728] |
| nominal | Omissão | -0.2016 [-0.2137; -0.1894] | -0.1759 [-0.1940; -0.1577] | -0.1743 [-0.1896; -0.1590] |
| nominal | Dívida latente | -0.0694 [-0.0761; -0.0628] | -0.0552 [-0.0615; -0.0489] | -0.0547 [-0.0607; -0.0486] |
| nominal | Falha efetiva | -0.0229 [-0.0347; -0.0111] | -0.0217 [-0.0342; -0.0092] | -0.0194 [-0.0303; -0.0084] |
| nominal | Fração P1 | -0.0511 [-0.0697; -0.0326] | -0.0523 [-0.0669; -0.0376] | -0.0534 [-0.0673; -0.0394] |
| fora48 | Atraso relativo | -0.9860 [-1.0731; -0.8988] | -0.9317 [-1.0084; -0.8549] | -0.9381 [-1.0175; -0.8587] |
| fora48 | Omissão | -0.2074 [-0.2163; -0.1985] | -0.1778 [-0.1865; -0.1691] | -0.1789 [-0.1882; -0.1697] |
| fora48 | Dívida latente | -0.0727 [-0.0778; -0.0676] | -0.0570 [-0.0612; -0.0529] | -0.0567 [-0.0604; -0.0529] |
| fora48 | Falha efetiva | -0.0213 [-0.0276; -0.0149] | -0.0190 [-0.0258; -0.0122] | -0.0192 [-0.0260; -0.0124] |
| fora48 | Fração P1 | -0.0499 [-0.0587; -0.0410] | -0.0446 [-0.0514; -0.0378] | -0.0447 [-0.0510; -0.0384] |
| aleatorio24 | Atraso relativo | -1.0330 [-1.1607; -0.9052] | -0.9256 [-1.0380; -0.8131] | -0.9528 [-1.0731; -0.8325] |
| aleatorio24 | Omissão | -0.1999 [-0.2121; -0.1878] | -0.1731 [-0.1838; -0.1623] | -0.1746 [-0.1856; -0.1636] |
| aleatorio24 | Dívida latente | -0.0664 [-0.0738; -0.0590] | -0.0539 [-0.0587; -0.0491] | -0.0542 [-0.0589; -0.0496] |
| aleatorio24 | Falha efetiva | -0.0231 [-0.0313; -0.0148] | -0.0164 [-0.0254; -0.0073] | -0.0176 [-0.0269; -0.0083] |
| aleatorio24 | Fração P1 | -0.0609 [-0.0754; -0.0464] | -0.0560 [-0.0662; -0.0457] | -0.0553 [-0.0661; -0.0446] |

Os deltas com IC95 pareado estão em `etapa3/mudancas_pareadas.csv`: v2→etapa2 isola a correção inicial, etapa2→etapa3 isola o desacoplamento da fuga. Não são IC de diferenças calculados por subtração dos limites marginais.

### Governança: sinal e magnitude

81 perfis, quatro instâncias × quatro sementes × dois rótulos = 2.592 execuções por versão. Perfis iguais sob rótulos distintos foram conferidos idênticos. 1.215 pares ordenados não idênticos; negativos favorecem adaptativa. Contagem não equivale a significância, e pares compartilham perfis.

| Indicador | v2: negativos | etapa 2: negativos | etapa 3: negativos |
| --- | --- | --- | --- |
| Atraso relativo | 1128/1215 (92.84%) | 1115/1215 (91.77%) | 1114/1215 (91.69%) |
| Omissão | 926/1215 (76.21%) | 940/1215 (77.37%) | 950/1215 (78.19%) |
| Dívida latente | 1101/1215 (90.62%) | 1124/1215 (92.51%) | 1103/1215 (90.78%) |
| Falha efetiva | 564/1215 (46.42%) | 504/1215 (41.48%) | 531/1215 (43.70%) |
| Fração P1 | 802/1215 (66.01%) | 806/1215 (66.34%) | 806/1215 (66.34%) |

Em cada etapa, `GOV_contrastes.csv` traz cada par com média/IC95; `GOV_sinais.csv` separa sinais de IC excluindo zero. `GOV_antes_depois.csv` lista mudanças frente à v2 e `etapa3/GOV_etapa2_etapa3.csv` lista mudanças específicas do desacoplamento. Não há alegação de sinal estável em toda a grade.

### Decisão e limites

A v3 final usa kh=ka=0,04 e k_fuga=0,10. v2 preservada por `config/mvp_v2.yaml` + `config/parametros_v2.yaml`; v1 conserva `config/mvp_v1.yaml` e usa os parâmetros históricos ao reproduzir a evidência. A restauração histórica aciona a guarda atual por desenho; não esconder essa violação nem confundi-la com diferença de dinâmica. Código/configurações executados nas etapas 1/2 estão em snapshots separados. O fallback de k_fuga para kh em configurações antigas preserva o acoplamento anterior.

A derivação do custo pressupõe mesmo E, eficiência e ausência de saturação de bateria; o teste registra exatamente esse contrafactual. Nas trajetórias livres, duração discreta, realimentações e bateria no piso impedem extrapolar “25% em toda tarefa”. A varredura declarada de kh [0,02;0,04] permanece como sensibilidade, sem procura de valor ótimo.

A evidência empírica favorece o adaptativo nos pontos nominais/validações apresentados, mas a vantagem não é universal na grade de governança. Falha efetiva continua exigindo essa ressalva. Nenhuma onda de History Matching, ajuste de V_mod ou calibração foi realizada.

### Reprodutibilidade e arquivos

Scripts: `research/test_drenagem_v3.py`, `test_fuga_desacoplada.py`, `etapa1_drenagem_79.py`, `validacao_drenagem_79.py`, `relatorio_drenagem_79.py`. Todos os CSV arquivados foram lidos com round_trip. Nova execução completa em diretório livre:

```bash
python research/validacao_drenagem_79.py rodar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3
python research/validacao_drenagem_79.py analisar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3
python -m unittest discover -s research -p "test_*.py" -v
```

Saídas deste lote: `outputs/diagnosticos/20260928_drenagem_heuristica/`, separadas em controle_previo, etapa1, etapa2 e etapa3. Não foram renomeadas nem apagadas saídas anteriores. A geração recusa sobrescrever bruto_novo.csv existente.

Conferência independente de agregação (csv/statistics) das 30 estimativas atuais das etapas 2/3: resíduo máximo de médias/IC95 **2.22e-16**. Este limite é verificação numérica das contas, não tolerância aplicada à identidade do simulador.

Os 15 contrastes finais dos três conjuntos mantêm IC95 inteiramente negativo.

### Inversões estritas de sinal na governança

Contagens abaixo excluem passagens pelo zero. Pares e IC completos nos CSV; não são contagens de inversões significativas.

| Transição | Métrica | Negativo → positivo | Positivo → negativo |
|---|---|---:|---:|
| v2→etapa2 | atraso_relativo | 69 | 56 |
| v2→etapa2 | divida_latente_sobre_plano | 60 | 83 |
| v2→etapa2 | fracao_porta1 | 133 | 136 |
| v2→etapa2 | taxa_falha_efetiva | 302 | 241 |
| v2→etapa2 | taxa_omissao | 112 | 127 |
| etapa2→etapa3 | atraso_relativo | 24 | 23 |
| etapa2→etapa3 | divida_latente_sobre_plano | 51 | 30 |
| etapa2→etapa3 | fracao_porta1 | 49 | 50 |
| etapa2→etapa3 | taxa_falha_efetiva | 68 | 93 |
| etapa2→etapa3 | taxa_omissao | 35 | 44 |
