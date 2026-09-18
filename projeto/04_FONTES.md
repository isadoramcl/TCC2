# Fontes

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

**? PESSOA et al.** Framework ABM+SD para execução de projetos de P&D com ciclos
de retrabalho. → É o precedente mais próximo do que foi construído e **ainda não
é citado em lugar nenhum**. O PDF está na pasta de referências. Incluir.

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

## Referências do TCC1 a conferir

Estão na monografia e ainda não foram auditadas uma a uma:

- **? MAHAMID** — o ano da citação diverge do PDF (`mahamid2020.pdf`).
- **? RATH, T.** — entrada quebrada em duas linhas.
- **? RESTREPO-TAMAYO et al. (2024)** — sem volume e páginas.

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
