# Briefing — as três lacunas em aberto do TCC2

**Para:** uma conversa dedicada a avaliar propostas externas (GPT ou outra fonte) para fechar G-01, G-02 e G-03.
**Data:** 17/09/2026 · **Origem:** revisão independente do TCC2 (pareceres 09–25 em `projeto/`)

---

## 0. Como usar este documento

Este é um pacote de contexto autossuficiente. Quem o ler deve conseguir avaliar uma
proposta de fonte sem reler a conversa que o gerou.

**Papéis:** Isadora é a autora do TCC. O Codex implementa. O interlocutor deste
documento atua como **revisor científico independente**: não aceita afirmação por ter
sido reportada, verifica na fonte primária, e classifica achados com evidência,
impacto, teste discriminante e confiança.

**Regra que vale para tudo:** se uma afirmação for para a monografia sem fonte
conferida, é problema jurídico e acadêmico. Toda fonte carrega estado:

| Estado | Significado |
|---|---|
| **TEXTO LIDO** | texto integral obtido e a afirmação conferida contra o que está escrito |
| **DADO RECALCULADO** | além do texto, os dados depositados foram reanalisados e reproduzem o publicado |
| **METADADOS CONFERIDOS** | autoria, ano, veículo e identificador conferidos; conteúdo não lido — serve para localizar, não para citar |
| **NÃO VERIFICADA** | chegou por indicação, resumo ou compilação secundária — **não citar** |

Nunca inventar referência. Nunca aceitar "o código executou" como "o modelo está correto".

---

## 1. Contexto mínimo do modelo

Simulador híbrido ABM + Dinâmica de Sistemas de equipes de engenharia, sobre
instâncias do PSPLIB J60. Agentes com competência, bateria cognitiva e confiança
executam tarefas sob pressão. Em cada oportunidade o agente passa por uma porta de
decisão:

- **Porta 1 (omissão/heurística):** atalho — menor duração, maior risco de erro.
- **Porta 2 (hiato de competência):** pede assistência a colega mais competente.
- **Porta 3 (analítica):** execução completa.

Seleção da porta: `p_heu = σ((E − τ_sat)/s)`, com `E = D·P/B` (demanda × pressão / bateria).
Risco: `p0 = clip(F_base(nível) + R_error·(1 − μ_cog), 0, 1)`, e em P1
`p_falha = 1 − (1−p0)(1 − ρ_omissão·q)` com `q = max(0, 2·p_heu − 1)`.

Falhas são reportadas com probabilidade `p_reporte`; as não reportadas viram dívida
latente, detectada com `p_deteccao`, e entram numa fila de reparo.

**Estado geral:** o simulador está verificado (identidade bit a bit com o legado,
40 testes, invariantes em execução, 22.208 execuções sem violação). O que falta é
ancoragem empírica. Nenhuma das 39 magnitudes do modelo está ancorada externamente.

---

## 2. G-01 — Comparador de retrabalho: a unidade bate, o domínio não

### O que o modelo produz

`retrabalho_sobre_plano = TR / E_plano` — esforço de retrabalho sobre a soma das
durações nominais planejadas. **Esforço sobre esforço, adimensional.**

Valores no nominal corrigido: **0,289** (arranjo centralizado), **0,235** (adaptativo).

### O que a literatura oferece

| Fonte | Mede | Valor | Estado |
|---|---|---|---|
| Boehm & Basili (2001), *Software Defect Reduction Top 10 List*, IEEE Computer 34(1) | **esforço** de software em retrabalho evitável | 40–50% | verificada; link em `04_FONTES` |
| Love (2026), JCEM | custo sobre **valor de contrato** | 0,38% (máx. 3,67%); 0,76% com pós-conclusão | verificada |
| Love & Li (2000), CME 18(4) | custo sobre valor contratual | 3,15% e 2,40% | verificada |
| Compilação CMAA (CII 10-1, Burati et al. 1992, Hwang et al. 2009, CII 153-11) | **custo** direto e total | mediana direta 4,03%; total 7,25–10,89% | secundária; primários **não lidos** |

### Por que continua aberto

Boehm & Basili é a **única referência na mesma unidade** do modelo. O problema não é
unidade — é domínio: desenvolvimento de software contra execução de projeto genérico.
As demais medem custo sobre valor de contrato, que é outro denominador.

### Erros já cometidos — não repetir

1. Comparar 0,289 com 4–11% sem notar que um é esforço e o outro é custo. **Foi feito
   e retratado.**
2. Afirmar que "não existe comparador na mesma unidade". **Falso** — Boehm & Basili
   existe e já estava catalogado. Retratado (R-06).
3. Usar Boehm & Basili como validação em vez de ordem de grandeza com empréstimo
   declarado. Isso reintroduz o problema, só desloca o domínio.

### O que fecharia a lacuna

Um estudo que reporte **horas de retrabalho contra horas planejadas**, na mesma
unidade de trabalho, em projeto de engenharia **não-software**. Alternativa aceitável:
conversão explícita e defensável de custo para esforço, com a hipótese de
proporcionalidade declarada e justificada.

### Pista não explorada

Rodrigues (2000), tese sobre SYDPIM (aplicação de dinâmica de sistemas à gestão de
projetos), já catalogada em `04_FONTES`. A literatura de dinâmica de sistemas aplicada
a projeto trabalha **nativamente em esforço**, não em custo. Ninguém olhou ainda com
essa pergunta na mão. Também: relatórios do CII com dados de **homem-hora**, que são
diferentes dos relatórios de custo que a compilação CMAA usa.

### Critério de aceitação de uma proposta

A fonte precisa declarar: numerador (o que conta como retrabalho), denominador (contra
o quê), unidade amostral independente, fronteira do sistema (o que está dentro do
projeto), e o domínio. Se qualquer um estiver ausente, a fonte não fecha a lacuna —
no máximo a ilustra.

---

## 3. G-02 — A ponte de agregação do HEART

### O que o modelo precisa

`F_ancora` fixa o **nível absoluto** de `P(tarefa produz defeito)` por atividade do
J60. A camada NASA fornece só o gradiente ordinal entre faixas de complexidade, nunca
o nível. Hoje `F_ancora` é `aberto`, varrido em [0,05; 0,10; 0,15; 0,20; 0,25].

### O que o HEART oferece

HEART (*Human Error Assessment and Reduction Technique*) estrutura a estimativa como
confiabilidade nominal por **tipo genérico de tarefa**, multiplicada por condições
produtoras de erro com multiplicadores tabelados. A correspondência estrutural com o
simulador é quase termo a termo:

| HEART | simulador |
|---|---|
| confiabilidade nominal por tipo genérico | `F_base(nível)` |
| condições produtoras de erro, multiplicativas | `μ_cognitivo`, pressão, fadiga |
| probabilidade de falha da tarefa | `p_falha` |

Multiplicadores conferidos em documento de aplicação: falta de tempo ×11,
desconhecimento de situação infrequente ×17, sobrecarga de capacidade de canal ×6.
Probabilidades calculadas nos exemplos: 0,16, 0,09 e 0,02.

### Por que continua aberto — o problema central

**A probabilidade do HEART é por passo elementar. Uma atividade do J60 agrega muitos
passos.** Sem uma regra de composição, o número do HEART não pode ser lido como
`F_ancora`.

E a composição não é detalhe: com `p = 0,02` por passo e `k = 50` passos,
`1 − 0,98⁵⁰ = 0,64`. A escolha de `k` domina completamente o resultado. Uma regra de
composição sem justificativa para `k` apenas transfere a arbitrariedade de um
parâmetro para outro.

### Estado de verificação — importante

A **estrutura** do HEART e alguns multiplicadores foram conferidos em documento de
aplicação. A **tabela de tipos genéricos de tarefa com valores nominais NÃO foi
verificada na fonte primária.** Obter antes de qualquer citação. Fontes a procurar:
Williams, J. C. (origem, 1986) e consolidações posteriores (Williams & Bell,
2017/2023, em *Safety and Reliability*); validação em Kirwan, B. et al. (1997),
*Applied Ergonomics*. Todas **NÃO VERIFICADAS**.

### O que fecharia a lacuna

Uma das duas:

1. Uma regra de composição justificada — por exemplo `1 − Π(1 − p_k)` sobre `k` passos —
   **com `k` estimado a partir de decomposição de tarefa documentada**, não arbitrado.
2. Uma fonte de confiabilidade humana que já reporte no **nível de pacote de trabalho**,
   dispensando a composição.

A segunda é muito preferível. A primeira só vale se `k` vier de algum lugar defensável.

### Outra objeção já levantada, e válida

Além do nível de agregação, há descasamento de denominador (custo × esforço), de
numerador (o que conta como "retrabalho" difere entre fontes) e descasamento interno:
com `F_ancora = 0,18` e `f_retrabalho = 0,42` o produto é 0,0756, mas o observável do
modelo dava 0,196 — cerca de 2,6× o produto. Registrado no §9 do parecer 12.

---

## 4. G-03 — P(heurístico | pressão, dificuldade): a validação dos 64%

### O que o modelo produz

`p_heu = σ((E − τ_sat)/s)` com `E = D·P/B`. A forma funcional é **escolhida**, não medida.

Frequências medidas no modelo corrigido, e os denominadores importam:

| Cenário | P1 / oportunidades | P1 / tarefas executadas |
|---|---:|---:|
| Centralizada | 0,2354 | 0,6740 |
| Adaptativa | 0,1911 | 0,5792 |

A cifra de "64%" que circulava só faz sentido contra **tarefas executadas**. Oportunidades
incluem P2 e fuga, que não chegam a executar.

### O que já foi descartado — não repropor

1. **Estudo de leitura sob restrição de tempo (Nature Human Behaviour / OSF q2dm6).**
   Serve para `ρ_omissão` (custo de acurácia sob prazo), e dele derivei
   ε(30 s) = 0,268 IC95 [0,197; 0,339], n = 32, com os dados recalculados.
   **NÃO serve para G-03:** o orçamento de tempo era fixado pelo experimentador
   (30/60/90 s), então a velocidade é resposta a prazo imposto, não escolha de
   estratégia. A direção causal é inversa à do modelo, onde o agente escolhe o atalho
   e o prazo é consequência. Um valor de `f_atalho ≈ 0,87` derivado dali foi
   **retratado** por esse motivo (R-01).
2. **Meta-análise de auditoria em publicação de baixa confiabilidade editorial.**
   Descartada. Substituto sugerido para o mesmo construto: Soobaroyen (2006),
   *International Journal of Auditing* — **NÃO VERIFICADA**.
3. **Szalma, Hancock & Quinn (2008)**, meta-análise de pressão de tempo (125 estudos,
   827 tamanhos de efeito, anais da HFES). **TEXTO LIDO.** Sustenta o **construto** —
   pressão de tempo acelera e prejudica acurácia, com variabilidade substancial entre
   estudos. **Não serve como fonte de valor**: é anais de congresso e não reporta
   proporção de seleção de estratégia.

### O que fecharia a lacuna

Estudo empírico que reporte a **proporção de decisões tomadas por atalho heurístico**
em função de pressão de prazo e de dificuldade de tarefa, em contexto profissional,
com o agente **escolhendo** a estratégia — não com o prazo imposto de fora.

### Pistas não exploradas

A literatura natural é a de **seleção adaptativa de estratégia** e do compromisso
esforço-acurácia. Duas linhas, ambas **NÃO VERIFICADAS**, a obter e conferir:

- Payne, Bettman & Johnson — trabalho canônico sobre o tomador de decisão adaptativo
  e a troca entre esforço e acurácia, incluindo deslocamento de estratégia sob pressão
  de tempo. É a literatura que mais diretamente mede o que o modelo assume.
- Literatura de heurísticas rápidas e frugais (Gigerenzer e colaboradores), que reporta
  uso de estratégia em função de custo de informação.

Qualquer uma delas, se reportar **proporções de uso de estratégia sob pressão**, é
candidata direta. Se reportar apenas acurácia, serve para `ρ_omissão` e não para G-03.

---

## 5. Contrato de admissibilidade — aplicável às três

Do parecer 22, e vale para qualquer fonte proposta. Antes de usar um número,
registrar: fonte e população; unidade amostral independente; janela de observação;
numerador e denominador; linha de base; fronteira de encerramento; tratamento de
faltantes e censura; mecanismo de reporte e detecção; conversões aplicadas; e
evidência de que a medição externa e a grandeza do modelo coincidem.

Três regras que já custaram retratações:

1. **Uma razão adimensional pode comparar coisas diferentes.** Esforço/esforço e
   custo/valor-de-contrato são ambos adimensionais e não são comparáveis.
2. **Não mascarar incompatibilidade de unidade ou fronteira aumentando a variância.**
   Se as grandezas não são a mesma coisa, inflar `V_obs` ou `V_mod` esconde o erro em
   vez de tratá-lo.
3. **Empréstimo de domínio é aceitável se declarado; não é aceitável se apresentado
   como validação.**

---

## 6. Como avaliar uma proposta que chegar

Para cada fonte sugerida, responder em ordem:

1. A referência existe? Autores, ano, veículo, identificador — conferir na origem.
2. O texto integral foi obtido? Se não, o estado é **METADADOS**, e não se cita valor.
3. O que ela mede, exatamente — numerador, denominador, unidade, fronteira?
4. Isso é a mesma grandeza que o modelo produz, ou exige uma ponte? Se exige, qual, e
   ela é defensável ou só transfere a arbitrariedade?
5. Qual o domínio, e o empréstimo está declarado?
6. **O que a fonte NÃO sustenta** — essa linha é obrigatória e é o que impede que a
   citação seja esticada depois.

Uma proposta que não sobrevive aos seis pontos não fecha a lacuna. Pode, ainda assim,
ser útil como suporte de construto — desde que registrada assim, e não como fonte de valor.

---

## 7. Onde está o resto

Repositório TCC2, ramo `main`:

- `projeto/04_FONTES.md` — catálogo canônico de fontes, com a linha do que cada uma **não** sustenta.
- `docs/registro_de_decisoes.md` — decisões do pipeline, com marcas `[LITERATURA]` / `[DECISÃO]` / `[ACHADO]` / `[ABERTO]`.
- `projeto/18_HISTORICO_DECISOES_E_FONTES.docx` — histórico da revisão: decisões, achados, retratações, gargalos.
- `projeto/12_ANCORAGEM_EXTERNA_F_ANCORA.md` — G-01 e G-02 em detalhe, incluindo o §9 sobre unidades e fronteira.
- `projeto/17_RHO_OMISSAO_DADOS_HUMANOS.md` — derivação de `ρ_omissão`.
- `projeto/22_OBSERVAVEIS_VOBS_VMOD.md` — contrato observacional.
- `projeto/25_LEVANTAMENTO_REALISTA_PARA_A_MONOGRAFIA.md` — o que fazer com o que não vai fechar no prazo.
