# Fontes

> **Catálogo único.** Consolida este arquivo e `research/SOURCES.md`, que passa a
> ser histórico. Toda fonte usada em qualquer afirmação do trabalho entra aqui.
> Última consolidação: 20/09/2026.


Cada entrada traz o link, o que a fonte **sustenta** e — quando aplicável — o
que ela **não** sustenta. A segunda coluna é a que evita erro: já
sobre-afirmamos duas fontes e comparamos grandezas de unidades diferentes.

Status: `✓` existência e conteúdo conferidos · `?` a conferir

---

## Calibração e qualidade dos dados

**✓ SHEPPERD, M.; SONG, Q.; SUN, Z.; MAIR, C.** Data quality: some comments on
the NASA software defect datasets. *IEEE TSE*, v. 39, n. 9, p. 1208-1215, 2013.
`https://doi.org/10.1109/TSE.2013.11`
→ Sustenta: os problemas de qualidade e proveniência das bases NASA MDP; o
algoritmo de limpeza D′/D″.
→ Não sustenta: que os arquivos D″ distribuídos sigam literalmente o
pseudocódigo. Nossa validação achou resíduo de 46 registros (0,26%) no
tratamento do rótulo — isso é achado nosso e está declarado como limitação.

**✓ SHEPPERD, M.** The cleaned NASA MDP data sets. Figshare, 2018.
`https://figshare.com/articles/dataset/MDP_data_sets_D_and_D_-_zipped_up/6071675`
→ Sustenta: D′ e D″ migradas, D″ recomendada.
→ Pendência: os arquivos que usamos vieram de espelho público e têm data
anterior ao artigo. **Confirmar contra a coleção oficial** antes da redação final.

**✓ NASA.** SWE-220 — Cyclomatic Complexity for Safety-Critical Software.
*NASA Software Engineering Handbook*. `https://swehb.nasa.gov`
→ Sustenta: o limiar de 15 e a exigência de revisão formal acima dele.
→ Não sustenta: as quatro faixas que usamos (≤10, 11-15, 16-20, >20). As faixas
da fonte são cinco e se sobrepõem nos extremos. A adaptação é `[DEC]` nossa.

**✓ NASA.** Cyclomatic complexity assessment. NASA/TM-20205011566, NESC-RP-20-01515, 2020.
`https://ntrs.nasa.gov/api/citations/20205011566/downloads/20205011566.pdf`
→ Sustenta: evidência acadêmica "mista" sobre complexidade ciclomática e adoção
típica de faixas na ordem de 10 a 20.

**✓ McCABE, T. J.** A complexity measure. *IEEE TSE*, v. SE-2, n. 4, p. 308-320, 1976.

## Estrutura de projeto (PSPLIB)

**✓ KOLISCH, R.; SPRECHER, A.; DREXL, A.** Characterization and generation of a
general class of resource-constrained project scheduling problems.
*Management Science*, v. 41, n. 10, p. 1693-1703, 1995.
`https://doi.org/10.1287/mnsc.41.10.1693`
→ Sustenta: NC, RF e RS como parâmetros do delineamento fatorial.

**✓ KOLISCH, R.; SPRECHER, A.** PSPLIB — a project scheduling problem library.
*EJOR*, v. 96, n. 1, p. 205-216, 1997.

**✓ KOLISCH, R.** Serial and parallel resource-constrained project scheduling
methods revisited. *EJOR*, v. 90, n. 2, p. 320-333, 1996.
→ Sustenta: o SGS serial com prioridade por menor folga, usado na derivação de
parâmetros.

**✓ BEIN, W. W.; KAMBUROWSKI, J.; STALLMANN, M. F. M.** Optimal reduction of
two-terminal directed acyclic graphs. *SIAM J. Comput.*, v. 21, n. 6, p. 1112-1129, 1992.

**✓ DE REYCK, B.; HERROELEN, W.** On the use of the complexity index as a
measure of complexity in activity networks. *EJOR*, v. 91, n. 2, p. 347-366, 1996.
→ Sustenta: caracterização de complexidade **da rede inteira**.
→ **Não sustenta** um índice de dificuldade por atividade. A formulação
preliminar atribuía a eles nosso índice `Di` — atribuição imprópria, corrigida.
A referência foi realocada para caracterização de rede.

## Modelo híbrido e agentes

**✓ CROWDER, R. M.; ROBINSON, M. A.; HUGHES, H. P. N. et al.** The development
of an agent-based modeling framework for simulating engineering team work.
*IEEE Trans. SMC-A*, v. 42, n. 6, p. 1425-1439, 2012.
→ Sustenta: a fórmula ΔC = [15 + 3(C_k − C)]/100.
→ **Atenção:** especifica também que ΔC ∈ [0; 0,3], que a competência após ajuda
não ultrapassa a dificuldade da subtarefa, e que **ao terminar a subtarefa a
competência volta ao valor inicial**. Nosso código faz o ganho ser permanente.
Usamos a fórmula deles dentro de uma dinâmica diferente — item C6.

**✓ LIU, S.; TRIANTIS, K. P.; SARANGI, S.** Representing qualitative variables
and their interactions with fuzzy logic in system dynamics modeling.
*Systems Research and Behavioral Science*, v. 28, p. 245-263, 2011.
→ Sustenta: acoplar lógica difusa a modelos de dinâmica de sistemas.
→ **Não sustenta** o verbo "validado". Eles **propõem e ilustram** um método.

**✓ VAN BROEKHOVEN, E.; DE BAETS, B.** Only smooth rule bases can generate
monotone Mamdani-Assilian models under center-of-gravity defuzzification.
*IEEE Trans. Fuzzy Systems*, v. 17, n. 5, p. 1157-1174, 2009.
`https://doi.org/10.1109/TFUZZ.2009.2023328`
→ Sustenta: a Tabela IX e as cinco configurações com monotonicidade garantida;
para duas entradas, apenas t-norma **produto** com base monótona e suave.
→ **Não sustenta** a nossa partição uniforme específica (núcleos 0 / 0,5 / 1).
O artigo exige que exista **uma** partição difusa, não aquela. Classificar como
`[DEC]`, não `[LIT]` — item D6.

**✓ MACAL, C. M.; NORTH, M. J.** Tutorial on agent-based modelling and
simulation. *Journal of Simulation*, v. 4, n. 3, p. 151-162, 2010.

**✓ STERMAN, J. D.** *Business dynamics*. Boston: Irwin/McGraw-Hill, 2000.

**✓ RODRIGUES, A. G.** The application of system dynamics to project management
(SYDPIM). Tese — University of Strathclyde, 2000.

**✓ PESSOA, R. W. S. et al.** An Agent-Based Modeling Dynamic Hybrid Model for
Project Management in Research and Development. *Industrial & Engineering
Chemistry Research*, 2026. [DOI e fonte primária](https://pubs.acs.org/doi/10.1021/acs.iecr.5c04351).
Conferido em 18/09/2026 por texto indexado da editora: não conclusão persistiu
com 600 semanas, associada à alocação/dependências e disponibilidade de agentes.
É precedente de limitação estrutural; não demonstra mecanismo idêntico neste
TCC, nem propriedade necessária de todo modelo ABM+SD. Ver diagnóstico T-B2.

## Calibração de modelos e identificabilidade

**✓ ANDRIANAKIS, I.; VERNON, I. R.; McCREESH, N. et al.** Bayesian history
matching of complex infectious disease models using emulation.
*PLoS Comput. Biol.*, v. 11, n. 1, e1003968, 2015.
`https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003968`
→ Sustenta: History Matching, implausibilidade, conjunto NROY.

**✓ McCULLOCH, J.; GE, J.; WARD, J. A. et al.** Calibrating agent-based models
using uncertainty quantification methods. *JASSS*, v. 25, n. 2, art. 1, 2022.
`https://www.jasss.org/25/2/1.html`
→ Sustenta: o teste do gêmeo idêntico.
→ **Reforça a nossa limitação:** os autores enfatizam que modelos reais sempre
têm discrepância e que ignorá-la prende os parâmetros ao modelo em vez de
representar grandezas fisicamente significativas.

**✓ PUKELSHEIM, F.** The three sigma rule. *The American Statistician*, v. 48,
n. 2, p. 88-91, 1994. `https://doi.org/10.1080/00031305.1994.10476030`
→ Sustenta: o corte de implausibilidade em 3.
→ **Precisão exigida:** a desigualdade vale para distribuições com **densidade**
unimodal, não para "qualquer distribuição unimodal". Corrigir o texto — item E7.

## Retrabalho (validação externa)

**✓ BOEHM, B.; BASILI, V. R.** Software defect reduction top 10 list.
*Computer*, v. 34, n. 1, p. 135-137, 2001.
`https://www.cs.umd.edu/~basili/publications/journals/J81.pdf`
→ Sustenta: 40% a 50% do **esforço** em retrabalho evitável. É a única referência
na **mesma unidade** da saída do modelo.

**✓ LOVE, P. E. D. et al.** Quantifying the costs of field rework in
construction. *JCEM*, v. 152, n. 1, 2026.
`https://ascelibrary.org/doi/10.1061/JCEMD4.COENG-17026`
→ 0,38% do valor de contrato (máx. 3,67%); 0,76% incluindo pós-conclusão.
→ **Unidade diferente:** custo sobre valor de contrato, não esforço. Já erramos
comparando as duas. Retida apenas como piso de ordem de grandeza, com a
diferença declarada.

**✓ LOVE, P. E. D.; LI, H.** Quantifying the causes and costs of rework in
construction. *Construction Management and Economics*, v. 18, n. 4, p. 479-490, 2000.
→ 3,15% e 2,40% do valor contratual. Mesma ressalva de unidade.

---

## Fatores humanos e erro — âncoras do modelo de erro

**✓ STEWART, M. G.; MELCHERS, R. E.** Simulation of human error in a design
loading task. *Structural Safety*, v. 5, p. 285–297, 1988. Elsevier Science
Publishers. Recebido 10/11/1987, aceito 10/09/1988. PDF em
`Refs/…` e conferido. Páginas consultadas: 287 e 290.
→ **Sustenta:** Tabela 1, p. 290 — taxa de erro por microtarefa de projetistas
civis profissionais, `p(k) = k × 0,0128` exato para k = 1, 2, 3, 4, 5 e 8;
consulta a tabela 0,0126. Fig. 1, p. 287 — nó de omissão antes do de comissão.
→ **Não sustenta:** valores de `F_ancora` acima de 0,10, que exigem k > 8, o
maior publicado. As taxas de omissão de 0,40 a 0,80 são de **um** fator de
redução específico e não transportam como "taxa de atalho". A hipótese (v) do
artigo, sobre ausência de pressão temporal, é declaração de escopo, não resultado.
→ **Usada em:** ancoragem de `F_ancora` (controle C1); estrutura da Porta 1.

**✓ STEWART, M. G.** Modelling human error rates for human reliability analysis
of a structural design task. *Reliability Engineering and System Safety*, v. 36,
p. 171–180, 1992. DOI: 10.1016/0951-8320(92)90097-5. Texto integral lido;
páginas consultadas 173–177.
→ **Sustenta:** Tabela 1, p. 173 — 94 respondentes, 38 erros, 2 327 microtarefas,
`p_av = 0,0163`. Tabela 2, p. 175 — binomial rejeitada (χ² = 10,174 contra
crítico 5,991); beta-binomial χ² = 0,162; p-dependente χ² = 0,583. `CV = 1,13`,
`α = 0,7546`, `β = 45,4563`, `φ = 0,845`.
→ **Não sustenta:** **nada sobre pressão temporal.** A manipulação falhou — os
tempos de resposta não diferiram e o autor fundiu as amostras (p. 173). A
Tabela 3 dá +27% a +44% (beta-binomial) e +94% a +111% (p-dependente), não os
"20–30% e 50%" do texto corrido.
→ **Achado próprio (A-16):** a Tabela 2 não é internamente reprodutível na
precisão impressa. Ver seção específica no fim deste arquivo.
→ **Usada em:** heterogeneidade entre agentes (C2); não independência (C3).

## Seleção de estratégia sob pressão

**✓ RIESKAMP, J.; HOFFRAGE, U.** Inferences under time pressure: how opportunity
costs affect strategy selection. *Acta Psychologica*, v. 127, p. 258–276, 2008.
DOI: 10.1016/j.actpsy.2007.05.004. Texto integral lido; contagens conferidas
contra o Estudo 2, p. 266–267.
→ **Sustenta:** o construto. Sob alta pressão de tempo as inferências são melhor
previstas por LEX; sob baixa pressão, por modelo linear ponderado.
→ **Conferido (20/09/2026):** 7/36 (19,4%) e 16/36 (44,4%) **reconstroem-se** do
trecho publicado — 11 dos 29 participantes compensatórios sob baixa pressão
migram para não compensatório sob alta, e 2 dos 7 não compensatórios migram no
sentido inverso; McNemar p = 0,02.
→ **Não sustenta:** o valor não transporta. Rieskamp conta *participante
classificado*, o modelo conta *execução de tarefa* — denominadores diferentes.
O **Estudo 1 do mesmo artigo não achou o efeito** (χ² = 0,10; p = 0,75), e o
contraste do Estudo 2 é pressão × **ausência** de pressão, condição que a faixa
de `P` do modelo (0,30 a 1,00) nunca produz. Se citar, cite como mudança
relativa (2,3×), com a ressalva.
→ **Usada em:** justificativa da transição estocástica para modo heurístico (C4).

**✓ PAYNE, J. W.; BETTMAN, J. R.; LUCE, M. F.** When time is money: decision
behavior under opportunity-cost time pressure. *Organizational Behavior and
Human Decision Processes*, v. 66, n. 2, p. 131–152, maio 1996.
→ **Não sustenta:** o deslocamento de estratégia sob pressão aponta na direção
do modelo mas **não é significativo**. Citar com essa ressalva.

## Omissão, adiamento e segurança psicológica

**✓ BALL, J. E.; MURRELLS, T.; RAFFERTY, A. M.; MORROW, E.; GRIFFITHS, P.**
'Care left undone' during nursing shifts: associations with workload and
perceived quality of care. *BMJ Quality & Safety*, v. 23, n. 2, p. 116–125,
2014. DOI: 10.1136/bmjqs-2012-001767. Acesso aberto:
`https://eprints.soton.ac.uk/355664`.
→ **Conferido no resumo (21/09/2026):** *"Most nurses (86%) reported that one or
more care activity had been left undone due to lack of time on their last
shift."*
→ **Sustenta:** omissão de tarefa necessária por falta de tempo, associada à
carga — o construto da **rota de fuga (adiamento)**.
→ **Não sustenta:** o valor. 86% é proporção de **enfermeiros que omitiram ao
menos uma atividade no último turno**, não taxa de omissão por tarefa, e o
domínio é enfermagem hospitalar.
→ **Não confundir** com Ball, Maskill & Ormerod (1998), homônimo sem uso aqui.

**✓ WHITE, E. M.; AIKEN, L. H.; McHUGH, M. D.** Registered nurse burnout, job
dissatisfaction, and missed care in nursing homes. *Journal of the American
Geriatrics Society*, v. 67, n. 10, p. 2065–2070, 2019. DOI: 10.1111/jgs.16051.
PDF em `Refs_tcc2` (versão de publicação antecipada, paginada 1–7; as páginas
finais 2065–2070 vêm da página institucional da Penn Nursing).
→ **Conferido no texto (21/09/2026):** *"Controlling for RN and nursing home
characteristics, RNs with burnout were five times more likely to leave
necessary care undone (odds ratio [OR] = 4.97; 95% confidence interval [CI] =
2.56-9.66) than RNs without burnout."* Amostra: 687 enfermeiros em 540
instituições; *burnout* medido pela subescala de **exaustão emocional** do
Maslach Burnout Inventory; 72% omitiram ao menos uma tarefa no último turno.
→ **Sustenta:** o elo `exaustão → omissão` — e a medida de exaustão é a mesma
família de instrumento usada em Zhao (MBI), o que torna a cadeia coerente.
→ **Não sustenta:** o valor. Razão de chances entre enfermeiros com e sem
exaustão alta, desenho transversal, domínio distante. Não vira parâmetro.

**✓ EDMONDSON, A.** Psychological safety and learning behavior in work teams.
*Administrative Science Quarterly*, v. 44, n. 2, p. 350–383, 1999.
DOI: 10.2307/2666999. Texto integral aberto, hospedado pelo MIT.
→ **Conferido (21/09/2026):** definição na **p. 354** — *"Team psychological
safety is defined as a shared belief that the team is safe for interpersonal
risk taking."* Sobre erro, também p. 354: *"Team members may be unwilling to
bring up errors that could help the team make subsequent changes because they
are concerned about being seen as incompetent."* Confiabilidade da escala
α = 0,82 (Tabela 2, p. 363).
→ **Sustenta:** o construto de `p_reporte` — a relutância em trazer o erro à
tona por medo de parecer incompetente é exatamente o que o parâmetro representa.
→ **Não sustenta:** nenhum valor de `p_reporte`. É crença compartilhada em nível
de equipe, medida por escala de atitude — não probabilidade de reporte por
evento.
→ **Leitura feita por extração automática do PDF.** Conferir as duas citações na
p. 354 com os olhos antes de colocá-las na monografia.

## Carga, complexidade e desgaste

**✓ ZHAO, C.; QI, J.; CHEN, Y.** Job demands, job resources, and burnout among
metro site management personnel in China: a cross-sectional study based on the
JD-R model. *Frontiers in Psychology*, v. 17, 2026. Publicado em 22/07/2026.
DOI: 10.3389/fpsyg.2026.1856402 · PubMed 42564107 · PMC13441851.
Autores: Chunxiao Zhao, Jinghua Qi e Yuxiang Chen (China University of Mining
and Technology).
Conferido no texto integral em 17/09/2026 (parecer 33, §2). Dados declarados em
`10.5281/zenodo.21153010` — citar este DOI, que é o que consta no artigo.
→ **Sustenta:** a direção `carga, complexidade → exaustão`, em gestão de obras —
domínio certo. 274 respostas válidas; carga β = 0,608, complexidade β = 0,349,
em modelos separados.
→ **Não sustenta:** `D` e `P` como determinantes independentes do desgaste. Na
regressão conjunta executada sobre a base aberta, β_WL = 0,432 e β_GF = −0,015
(n.s.) — a complexidade perde efeito próprio quando se controla a carga.
Desenho transversal: não informa a dinâmica da bateria `B`.

## Degradação de qualidade

**✓ REICHELT, K.; LYNEIS, J.** The dynamics of project performance: benchmarking
the drivers of cost and schedule overrun. *European Management Journal*, v. 17,
n. 2, p. 135–150, 1999. PDF em `Refs_tcc2`.
→ **Conferido nas tabelas (21/09/2026), p. 149.** Efeito médio sobre a
**qualidade** do trabalho:

| fator | Tabela 1 — projeto (design) | Tabela 2 — execução (build) |
|---|---:|---:|
| pressão de cronograma | 0,95 | 0,96 |
| fadiga de hora extra | 0,97 | 0,98 |

→ **Correção:** os documentos internos citavam "0,95 e 0,97, Tabelas 1–2". Esses
dois números são **só da Tabela 1**; na Tabela 2 são 0,96 e 0,98. Citar a
tabela certa.
→ **Detalhe que importa para o modelo:** a pressão de cronograma **reduz a
qualidade mas aumenta a produtividade** (1,04 no projeto, 1,03 na execução) —
é o trade-off que a Porta 1 representa.
→ **Ressalva obrigatória:** são médias de efeito extraídas de modelos de
Dinâmica de Sistemas calibrados pela Pugh-Roberts em dez projetos (nove
esforços de projeto), **mesma linhagem** deste trabalho — consistência com a
literatura de modelagem, não medição independente.
→ **Usada em:** verificação da faixa de `mu_minimo` (E3).

## Base conceitual herdada do TCC I

**✓ KIM, D. H.** *Systems thinking tools: a user's reference guide.* Waltham:
Pegasus Communications, 1994. 60 p. (The Toolbox Reprint Series).
ISBN 1-883823-02-1. Exemplar consultado: reimpressão de 2000, pasta de
referências do TCC I.
→ **Sustenta:** os dois arquétipos, na tabela *Systems Archetypes at a Glance* —
"Drifting Goals" na **p. 20** e "Shifting the Burden/Addiction" na **p. 21**.
→ **⚠ Correção para a monografia:** o TCC I cita *Kim, D. H. Systems archetypes
I: diagnosing systemic issues and designing high-leverage interventions*, que é
**outro volume** da mesma série. O PDF que existe é o *Systems thinking tools*.
Citar o que foi lido.
→ **⚠ Nome:** o TCC I chama o segundo arquétipo de **Soluções Sintomáticas**;
Kim o chama **Shifting the Burden**. Declarar a equivalência uma vez.
→ **Não sustenta:** nenhum valor de parâmetro. Ancora a **forma** dos laços.

**✓ SIMON, H. A.** *Models of man: social and rational.* New York: John Wiley and
Sons, 1957. Referência completa já consta no TCC I.
→ **Sustenta:** o conceito de *satisficing*, base da Porta 1.
→ **Atenção:** o livro não está na pasta de referências. É citação canônica de
conceito, não de valor — aceitável, mas não atribuir a ele nenhuma afirmação
além da definição.

**✓ MAHAMID, I.** Impact of rework on material waste in building construction
projects. *International Journal of Construction Management*, v. 22, n. 8,
p. 1500–1507, 2022.
DOI: 10.1080/15623599.2020.1728607.
→ **Divergência resolvida:** publicado online em 19/02/2020, fascículo impresso
v. 22, n. 8, p. 1500–1507, 2022 (Taylor & Francis). O TCC I cita 2022, correto,
mas **sem as páginas** — acrescentar p. 1500–1507 na monografia.

**✓ RATH, T.** Effort-based strategy selection in multi-attribute decision
making: when bounded rationality predicts optimal behavior. Kanpur: Indian
Institute of Technology, 1 dez. 2025. Preprint, 17 p.
→ **Atenção:** preprint sem veículo, DOI nem arXiv no PDF. Citar como preprint,
como o TCC I já faz, e não apoiar afirmação central só nele.

**✓ RESTREPO-TAMAYO, L. M.; GASCA-HURTADO, G. P.; VALENCIA-CALVO, J.**
Characterizing social and human factors in software development team
productivity: a system dynamics approach. *IEEE Access*, v. 12, p. 59739–59755,
2024. DOI: 10.1109/ACCESS.2024.3388505.
→ **Correção para a monografia:** o TCC I omite volume, páginas e DOI.

## Retiradas do catálogo em 21/09/2026

Sem uso em nenhuma decisão, parâmetro, código ou documento do modelo:

- **Lee et al. (2020)** e **Jarratt et al. (2011)** — vinham de uma matriz
  proposta em conversa paralela (parecer 33), sem título registrado, e nunca
  foram ligadas a nenhum elo do modelo.
- **Ball, Maskill & Ormerod (1998)** e **White, Braund, Howes et al. (2018)** —
  homônimos obtidos por engano ao procurar Ball (2014) e White (2019).

## Regra ao acrescentar fonte

Nada entra aqui sem: (1) link que abre; (2) o trecho que sustenta a afirmação;
(3) uma linha dizendo o que a fonte **não** sustenta. A terceira é a que evita
que a citação seja esticada depois.

## Plano B metodológico — D-12

**✓ GRIMM, V. et al.** Pattern-oriented modeling of agent-based complex systems:
lessons from ecology. *Science*, 310(5750), 987–991, 2005.
[Registro e resumo primário USGS](https://www.usgs.gov/publications/pattern-oriented-modeling-agent-based-complex-systems-lessons-ecology),
[DOI](https://doi.org/10.1126/science.1116681). Conferido em 17/09/2026.
→ Sustenta: modelagem orientada a padrões como estratégia para desenhar, testar
e analisar modelos de agentes e sua organização interna.
→ Não sustenta: os padrões específicos de engenharia, limiares de aceitação ou
a validação empírica deste simulador. O plano B do parecer 22 é [DEC].
Nota de proveniência: a referência D-12 mencionada pela autora não constava na
versão de 04_FONTES disponível em origin/main ddc7c94; esta entrada registra a
fonte primária conferida, sem inventar um registro anterior.


### Stewart (1992) — discrepância conhecida da Tabela 2, oito erros

Parecer 39: parâmetros canônicos alpha=0,7546 e beta=45,4563. A frequência
beta-binomial para oito erros é **0,004018884** respondente em N=94; o PDF
imprime **0,000**. Com mu/CV literais a conta anterior era 0,003989000.
Discrepância conhecida, dispensada de bloqueio explicitamente pelo parecer 39.
Truncamento editorial é hipótese, não causa demonstrada; uma linha ≥8 também
não explicaria massa menor que a de exatamente oito erros.
A aplicação da regra de precisão aos parâmetros canônicos está no
[relatório 40](40_RECONCILIACAO_C3_REGRA39.md); outras células continuam abertas.


### A-16 — Stewart (1992), inconsistência interna quantificada

18/09/2026. Regra corrigida fornecida integralmente pela autora nesta sessão;
substitui o parecer 39. A implementação é validada como teste discriminante,
e a fonte é internamente inconsistente na quarta casa significativa. Não se
alega reprodução das frequências à precisão impressa.

Busca reproduzida em **5.329 pontos (73×73)** da caixa de arredondamento
alpha∈[0,75455;0,75465], beta∈[45,45625;45,45635]. Todos os pontos satisfazem
mu arredondado a 0,0163 e CV a 1,13; **nenhum** produz E0 que arredonde a 67,475.
Faixa E0=[67,481624506;67,484608392]. Inversos diagnósticos:
alpha*=0,754875715 com beta fixo (arredonda a 0,7549), e beta*=45,435977462
com alpha fixo. Não são usados como parâmetros operacionais.

**Operacional: alpha=0,7546; beta=45,4563**, os impressos. E0=67,483116433,
discrepância de **0,0120288%** na maior célula. Célula de oito erros continua
registrada como discrepância conhecida. A aprovação discriminante usa apenas
k=0..4, especificados previamente pela autora.

Maior resíduo candidato 0,104318%, amplitude 0,116347%; cinco negativos dão
2,250601%, 9,992419%, 89,172890%, 100% e 89,155747%, todos acima de 1% e
mais de dez vezes o candidato. N5 segue literalmente sigma=CV*mu²; o resultado
não coincide com os 99,93% orientativos, e não foi ajustado.
Evidências: [bateria, resíduos e busca completa](../outputs/diagnosticos/lote41_C3_20260918/).
