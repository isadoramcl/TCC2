# 80 — Custo e escopo de uma eventual reexecução do HM na v3

**Data:** 28/09/2026. **Estatuto:** análise prévia; nenhuma reexecução autorizada ou realizada nesta etapa. Apenas este relatório foi criado. Código, configurações e evidências arquivadas não foram alterados. Não foram usados git status, add, commit ou push.

## 1. Veredito e recomendação

**A inconsistência procede.** `src/modelo/04_gemeo_identico.py:98–110` amostra `k_heuristico` em [0,06; 0,16] e fixa a verdade em 0,135. `research/lote_noturno/cobertura.py:53` e `PROTOCOLO_D2_D3.md` repetem 0,135. Com `k_analitico=0,04` e a guarda atual, todos esses valores são inválidos. A validação anterior das 4.704 execuções não cobriu esses caminhos; portanto, não demonstrou ausência de violações em todo o projeto.

**Recomendo substituir a dimensão livre por `k_analitico` em [0,02; 0,08], mantendo cinco dimensões.** A intensidade comum de drenagem continua sendo uma premissa aberta e influencia trabalho analítico e heurístico. Mantê-la no espaço permite investigar essa incerteza. A justificativa não é conservar artificialmente cinco dimensões. Remover a dimensão e fixar ambas as drenagens em 0,04 também é coerente, mas responde uma pergunta condicional a essa escolha e omite sua incerteza.

Não recomendo reajustar a faixa de `k_heuristico`: isso o manteria indevidamente livre. Tampouco recomendo converter automaticamente a antiga verdade 0,135 em algum valor conveniente de `k_analitico`. O novo vetor verdadeiro precisa ser declarado antes da execução, junto do critério a acordar com a autora.

**Pré-condição técnica ainda não implementada:** a derivação está escrita em `config/parametros.yaml`, mas `carregar_parametros()` não sincroniza os dois coeficientes. Os simuladores leem ambos separadamente. Apenas renomear a dimensão deixaria `k_heuristico=0,04`: propostas com `k_analitico<0,04` violariam a guarda e propostas acima disso descumpririam a igualdade declarada. Cada proposta e cada vetor verdadeiro precisam materializar `k_heuristico=k_analitico`. `k_fuga=0,10` permanece separado. A varredura própria ainda declarada para o parâmetro derivado também precisa ser reconciliada futuramente.

## 2. Número de execuções

Contagem derivada do código, sem executar simuladores:

| Componente | Desenho atual | Execuções |
|---|---|---:|
| Alvo sintético do gêmeo | 2 instâncias × 10 sementes | 20 |
| HM, onda 1 | 400 propostas × 2 instâncias × 4 sementes | 3.200 |
| HM, onda 2 | 400 propostas × 2 instâncias × 4 sementes | 3.200 |
| **HM + gêmeo** | Um único pipeline, não dois experimentos completos | **6.420** |
| Cobertura repetida | 500 réplicas × (20 observações + 8 predições) | **14.000** |
| **Total, B=500** | Sem duplicar o custo do gêmeo | **20.420** |
| Alternativa B=1.000 | Cobertura 28.000 + HM/gêmeo 6.420 | **34.420** |

Fontes: constantes e modos `verdade`, `onda1`, `onda2` de `04_gemeo_identico.py`; laços `obs=10`, `sim=4`, duas instâncias e `range(500)` de `cobertura.py`. Junção, IC, identificabilidade e relatório não acrescentam simulações. A redução para quatro dimensões **não reduz essa contagem** se forem mantidas 400 propostas por onda.

Esses números orçam a transposição do desenho existente, não uma aprovação de seus critérios. O gêmeo histórico verifica a inclusão da verdade nas projeções marginais da caixa, o que não prova inclusão conjunta. Uma avaliação independente da resposta no vetor verdadeiro com 2×4 sementes acrescentaria **8 execuções** ao orçamento, se incluída no futuro protocolo; a cobertura já faz avaliações independentes em cada réplica. Diagnósticos adicionais (`15`, `17`, `19`), suíte e validação global não estão incluídos nas 20.420 execuções. Não é possível dar seu total antes de fechar quais desenhos históricos serão reexecutados como v3.

## 3. Tempo de máquina — estimativa, não benchmark da v3

Há duas referências locais, de desenhos distintos:

- `04_gemeo_identico.py`, cabeçalho: **0,108 s por execução**. É uma referência histórica documentada; não foi medida novamente nesta etapa.
- `outputs/diagnosticos/20260922_discriminante_falha/fatorial_completo/execucao.log`: **960 execuções em aproximadamente 42 s**, com quatro processos (`research/fatorial_78.py`). É tempo de parede, arredondado no log, em outra região paramétrica. Seu equivalente linear é 0,175 s por execução por trabalhador, não uma medição de CPU.

| Orçamento | A 0,108 s/run, serial | A 0,175 s/run, serial equivalente |
|---|---:|---:|
| HM/gêmeo, 6.420 | 11,56 min | 18,73 min |
| Cobertura B=500, 14.000 | 25,20 min | 40,83 min |
| Total, 20.420 | **36,76 min** | **59,56 min** |
| Total com B=1.000, 34.420 | 61,96 min | 100,39 min |

Com quatro partes paralelas para as ondas e dois processos para a cobertura (como no desenho atual), a projeção ideal para B=500 é **aproximadamente 15,5–25,2 minutos de parede**. Para B=1.000, aproximadamente **28,1–45,6 minutos**. São dois cenários de extrapolação, **não limites garantidos nem IC**. Partidas de processos, leitura, escrita, diferenças de horizonte e a mudança de núcleo podem elevar o tempo. Tempo exato da v3: **NÃO VERIFICÁVEL sem benchmark autorizado**. O custo de implementação, revisão e aprovação do protocolo não está incluído. Não executei piloto para melhorar essa estimativa.

## 4. O orçamento não autoriza rodar os scripts atuais

1. **Núcleo errado para uma alegação sobre o nominal v3:** tanto `04` como a cobertura usam `Simulacao`, não `SimulacaoMVP` com as opções de `config/mvp.yaml`. Mesmo corrigindo o parâmetro, isso não vira automaticamente uma verificação do nominal v3. É necessário decidir e registrar a migração do núcleo e congelar suas dependências.
2. **Violações invisíveis nos resultados atuais:** `04.rodar()` não exporta nem testa `violacoes`; a cobertura grava conclusão, mas também omite violações. Um CSV preenchido não demonstra validade. Instrumentação e interrupção por violação são requisitos futuros.
3. **Evidência congelada:** `04` escreve em caminhos históricos fixos; `juntar` também move arquivos de partes. Não deve ser executado como está. Uma versão nova precisa de diretório exclusivo, identificação de versão, manifesto de parâmetros/código/sementes e recusa de sobrescrita.
4. **Cobertura antiga preservada:** a execução arquivada usa seu snapshot de `simulador.py` e parâmetros. Reproduzi-la com esse snapshot não herda a guarda da v3. Já uma nova chamada de `cobertura.main()` copia o código atual e injeta 0,135: é esse caminho que passa a ser inválido. Não se deve reclassificar retroativamente o arquivo antigo como violador.
5. **Contrato observacional:** os quatro observáveis históricos incluem `E_total`, dependente de convenção interna, e atraso contra CPM sem recursos. Servem a uma verificação interna sintética, não autorizam calibração externa. O HM agrega variância sobre execuções; a cobertura estima variância de médias por bloco das duas instâncias fixas. Essa diferença já existe e deve ser resolvida explicitamente no protocolo, não escondida ao trocar a dimensão. Nada aqui autoriza alterar V_mod ou escolher dados favoráveis.

## 5. Reconferência e não comparabilidade

Recalculei os seguintes valores por código de leitura próprio, usando `pd.read_csv(..., float_precision='round_trip')`, sem chamar os runners:

| Evidência histórica | Valor reproduzido |
|---|---:|
| Onda 2: propostas com I≤3 | 115/400 = 28,75% |
| Volume da caixa envolvente NROY / volume a priori | 0,1479872143905411 = **14,8%** |
| Contração marginal mu_minimo | 70,3457% |
| Contração marginal F_ancora | 36,7725% |
| Contração marginal tau_sat | 10,8815% |
| Contração marginal f_retrabalho | 5,9928% |
| Contração marginal k_heuristico | 5,7891% |
| Cobertura: I_max>3 | 31/500 = **6,2%** |
| Wilson 95% | **[4,4019%; 8,6660%]** |
| Clopper–Pearson 95%, método usado no parecer 59 | [4,2511%; 8,6853%] |
| Percentil 95 de I_max | 3,1168746531864384 |

Fontes: `outputs/tables/modelo_04_hm_onda2.csv` e `outputs/diagnosticos/noturno_D2_execucao/replicas.csv`. Para a caixa, multipliquei as cinco amplitudes marginais dos pontos aceitos divididas pelas amplitudes a priori (0,20; 0,50; 0,70; 0,10; 0,30). Portanto, **14,8% não é uma estimativa direta do volume do conjunto conjunto NROY**, e difere dos 28,75% de propostas aceitas na segunda onda. Os intervalos Wilson e exato têm nomes diferentes; ambos estão corretos para seus métodos.

Uma nova execução em quatro dimensões ou com `k_analitico` livre responde a outro espaço científico. Volume relativo, contrações e classificações não podem ser apresentados como melhora/piora frente ao espaço antigo. Isso continua verdadeiro caso se decida não reexecutar: os números antigos não passam a caracterizar a v3. Permanecem evidência histórica do procedimento legado disponível nas fases v1/v2, não validação retroativa dos respectivos nominais MVP.

**Ressalva sobre a cobertura:** seus 6,2% são calculados num vetor verdadeiro fixo; a cobertura não amostra o a priori de cinco dimensões. Alterar apenas a dimensão de uma busca, preservando exatamente a distribuição dos observáveis no ponto verdadeiro, não mudaria sua cobertura. Aqui a mudança de dinâmica, parametrização/verdade e eventual desenho impede transportar os 6,2% à v3. Uma comparação futura precisa declarar essas diferenças; não atribuir eventual melhoria somente à retirada de uma dimensão.

**Nota a acompanhar a linha histórica de identificabilidade:** “Na v3, k_heuristico deixa de ser estimando independente por derivação: k_heuristico=k_analitico. A contração histórica de 5,8% permanece registrada para o espaço legado; a retirada da linha da análise v3 decorre da formulação, não de falta de dados nem de uma nova conclusão de não identificabilidade.” A tabela histórica não foi editada.

## 6. Levantamento dos pipelines e limite da validação anterior

Nenhum pipeline foi executado nesta etapa, conforme a restrição expressa. O inventário abaixo é estático: existência e dependências não equivalem a aprovação. Para o futuro critério “todos”, é necessário classificar cada entrada em execução nominal v3, replay histórico ou análise sem dinâmica. Testes deliberadamente inválidos devem verificar a rejeição; não podem ser contados como violações do nominal.

| Família | Caminhos | Situação e justificativa para não executar agora |
|---|---|---|
| HM/gêmeo | `src/modelo/04_gemeo_identico.py` | Incompatibilidade confirmada; aguarda escolha e protocolo. |
| Cobertura | `research/lote_noturno/cobertura.py`, `PROTOCOLO_D2_D3.md`, `test_cobertura.py` | Nova execução incompatível; snapshot antigo é replay histórico. |
| Diagnósticos derivados de HM | `src/modelo/15`, `17`, `19` | Importam parâmetros/verdade do 04: também afetados. 16 e 18 reanalisam seus outputs; não geram validação nova. |
| Modelo legado | `src/modelo/02`, `03`, `07` a `12`, `14` | Verificações, cenários, ablações e sensibilidades; não cobertos pela validação das 4.704. Requerem decisão de versão e inspeção de overrides. |
| MVP e correções | `src/modelo/20`, `21`, `23`, `25`, `26` | Entradas experimentais próprias; execução nominal não cobre todas as opções. Não executadas porque o escopo atual é relatório. |
| Lotes científicos anteriores | `research/lote37`, `lote41`, `lote_noturno`, `tb2` | Incluem controles estatísticos sem ABM, testes estruturais e runners históricos v1. Preservar evidência; não convertê-los silenciosamente em nominal v3. |
| Validação de portões e governança | `research/validacao` e subpasta `portoes_suaves` | Desenhos históricos v1/v2, além dos grupos reaproveitados na 79. Identificar versão por entrada antes de alegar cobertura v3. |
| Auditorias 78 e 79 | scripts de discriminante/fatorial, controle prévio, drenagem e validação | 79 cobre nominal, amostras e governança, não todo o inventário. 78 é replay de controles históricos. |
| NASA, PSPLIB e preparação | `src/nasa`, `src/psplib`, `src/modelo/01`, `06` | Preparação/análise de dados, sem execução de agentes; guarda de drenagem não se aplica. Reexecutar não responderia à inconsistência. |
| Figuras, exportações, relatórios | `src/modelo/05`, `13`, `16`, `18`, `22`, `24`; auxiliares de relatório em research | Consomem evidências; não demonstram zero violações se a entrada omite o campo. Não sobrescrever saídas antigas. |
| Suíte e auxiliares | arquivos `test_*.py`, verificadores documentais e de TL | Parte contém casos inválidos intencionais e controles legados. Aprovação anterior da suíte não prova validade do HM; nova execução depende do escopo acordado. |

A busca textual de 0,135 localizou as definições ativas no 04, na cobertura e no protocolo. Dependências indiretas via `hm.VERDADE`, `hm.PARAMETROS` e `hm.aplicar` em 15/17/19 também entram no alcance; buscar apenas o literal não basta.

## 7. Critério pendente, a acordar antes de executar

Este relatório **não fixa o critério final nem autoriza execução**. Para a decisão conjunta: confirmar 5D ou 4D, núcleo alvo, vetor verdadeiro, observáveis/unidade amostral, desenho de cobertura, e política por pipeline histórico. Manter os dois requisitos já determinados: nenhum pipeline executado como nominal v3 registra violação; resultados novos ficam ao lado dos antigos, identificados por versão e com não comparabilidade escrita. O teste da derivação deve cobrir propostas abaixo e acima de 0,04, não só o nominal onde igualdade acidental esconderia o problema.

**Conclusão:** corrigir conceitualmente para a intensidade comum livre é a opção mais defensável; custo-base de 20.420 execuções, projeção de aproximadamente 15,5–25,2 minutos paralelos sob referências históricas, ainda sem benchmark da v3. A execução aguarda decisão da autora.

## Anexo — arquivos Python inventariados (sem execução)

Lista por diretório, incluindo módulos e análises sem bloco main, para não confundir ausência desse bloco com ausência de um pipeline. A classificação funcional e a aprovação individual permanecem tarefas futuras; este anexo é o alcance inicial da inspeção.

- **src/modelo**: `01_derivar_parametros.py`, `02_verificar_simulador.py`, `03_experimento_cenarios.py`, `04_gemeo_identico.py`, `05_figuras_modelo.py`, `06_exportar_parametros.py`, `07_ablacao_governanca.py`, `08_verificar_ablacao.py`, `09_sensibilidade_tau_min.py`, `10_decomposicao_fatorial.py`, `11_tendencia_pressao.py`, `12_porta2_operacionalizacao.py`, `13_exportar_tabelas_entrega.py`, `14_experimento_por_instancia.py`, `15_diagnostico_hm.py`, `16_reanalise_revisao.py`, `17_pilotos_revisao.py`, `18_analisar_pilotos_revisao.py`, `19_piloto_fronteira.py`, `20_experimento_mvp.py`, `21_canais_mvp.py`, `22_consolidar_mvp.py`, `23_instrumentacao_correcao.py`, `24_analisar_correcao.py`, `25_teste_tempo_aprendizado.py`, `26_testes_arranjo.py`, `ancoragem_stewart.py`, `fuzzy.py`, `heterogeneidade_erro.py`, `simulador.py`, `simulador_mvp.py`.

- **src/nasa**: `01_auditar_raw.py`, `02_consolidar_dpp.py`, `03_validar_dpp.py`, `04_modelos_logisticos.py`, `05_faixas_complexidade.py`, `06_figuras.py`.

- **src/psplib**: `01_auditar_j60.py`, `02_indice_dificuldade.py`, `03_transferencia_ordinal.py`, `04_figuras.py`.

- **research/arrumacao**: `renomear.py`.

- **research**: `conferencia_round_trip_78.py`, `controle_previo_79.py`, `discriminante_falha.py`, `etapa1_drenagem_79.py`, `fatorial_78.py`, `gerar_relatorio_arranjo.py`, `recuperar_evidencias.py`, `relatar_fatorial_78.py`, `relatorio_drenagem_79.py`, `test_a1.py`, `test_ancoragem_mvp.py`, `test_arranjo.py`, `test_b2_censura.py`, `test_c2_formula.py`, `test_c2_identidade_anterior.py`, `test_c2_integracao.py`, `test_c3_discriminante.py`, `test_canais_mvp.py`, `test_canal_erro_direto.py`, `test_causal_porta.py`, `test_compatibilidade.py`, `test_crowder.py`, `test_documento_oficial.py`, `test_drenagem_v3.py`, `test_escalares_crowder.py`, `test_experimento_mvp.py`, `test_fuga_desacoplada.py`, `test_instrumentacao.py`, `test_mvp.py`, `test_portoes_suaves.py`, `test_qualidade_porta1.py`, `test_revisao.py`, `test_rotulagem_b2.py`, `test_runner_tl.py`, `test_stewart_ancora.py`, `test_stewart_c3.py`, `test_stewart_c3_39.py`, `test_t4_canais.py`, `test_taxa_falha.py`, `test_tb23_configuracao.py`, `test_tb2_pares.py`, `test_tempo_aprendizado.py`, `validacao_drenagem_79.py`, `verificar_documento_oficial.py`, `verificar_exports_arranjo.py`, `verificar_independencia_tl.py`.

- **research/lote37**: `distribuicoes.py`, `validar_c3.py`, `validar_c3_39.py`.

- **research/lote41**: `b2.py`, `c3.py`, `rotulagem.py`, `t4.py`.

- **research/lote_noturno**: `a1.py`, `a1_relatorio.py`, `analisar_nominal.py`, `analisar_tb23.py`, `c1.py`, `c2_fechamento.py`, `c2_precontrole.py`, `cobertura.py`, `crowder1.py`, `crowder1_relatorio.py`, `gov2.py`, `nasa_offline.py`, `nominal.py`, `readout.py`, `sat_gov.py`, `sat_gov_relatorio.py`, `test_cobertura.py`.

- **research/tb2**: `diagnostico.py`, `relatorio.py`, `rotas_rotulos.py`, `varredura_confianca.py`.

- **research/validacao**: `analise.py`, `c4_dinamico.py`, `fora_da_amostra.py`, `gov_v2.py`, `nominal_v2.py`, `parte2.py`, `teste_aleatorio.py`.

- **research/validacao/portoes_suaves**: `analise_portoes.py`, `estresse.py`, `teste_portoes.py`, `varredura_s.py`.
