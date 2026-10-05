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

## Engenharia de Sistemas e projetos complexos

> Entraram em 05/10/2026, para o capítulo 2 da monografia. **Nenhuma delas fornece
> valor, parâmetro ou magnitude.** São definição, enquadramento e lacuna declarada.

**✓ KOSSIAKOFF, A.; SEYMOUR, S. J.; FLANIGAN, D. A.; BIEMER, S. M.** *Systems
engineering: principles and practice.* 3. ed. Hoboken: John Wiley & Sons, 2020.
(Wiley Series in Systems Engineering and Management). ISBN 9781119516668. 663 p.
PDF em `Refs_tcc1/Livros`; também anexado ao Projeto.
→ **Conferido no PDF primário (05/10/2026):** folha de título e créditos, e §1.1,
páginas impressas 3, 4, 5 e 10. **Leitura declarada: o capítulo 1**, não a obra
inteira.
→ **⚠ Ordem dos autores divergente dentro do próprio livro.** A folha de título traz
Kossiakoff, Seymour, Flanigan e Biemer. O registro da Library of Congress, na mesma
página de créditos, traz Kossiakoff, Biemer, Seymour e Flanigan. **Usar a ordem da
folha de título.** Kossiakoff morreu em 2005 e aparece com † na folha.
→ **Sustenta a definição de Engenharia de Sistemas adotada.** §1.1, **p. 3**: *"The
function of systems engineering is to guide the engineering and development of complex
systems."* Os autores apresentam isso como escolha, não como consenso: *"There are many
ways in which to define systems engineering. We will use the following definition"*.
Citar como definição adotada, não como *a* definição.
→ **Sustenta o olhar sobre o sistema inteiro.** **p. 4**: *"Systems engineering is
focused on the system as a whole; it emphasizes its total operation. It looks at the
system from the outside, that is, at its interactions with other systems and the
environment, as well as from the inside."*
→ **Sustenta que o objeto deste trabalho é objeto da Engenharia de Sistemas.** **p. 5**:
*"Systems engineering is an inherent part of project management – the part that is
concerned with guiding the engineering effort itself – setting its objectives, guiding
its execution, evaluating its results, and prescribing necessary corrective actions to
keep it on course."* A última oração é a descrição, em livro de referência da área, do
que o arranjo adaptativo faz no simulador.
→ **Sustenta o critério de equilíbrio entre atributos.** **p. 10**: *"the systems
engineer seeks the best balance of the critical system attributes"*, e os ditos *"the
best is the enemy of the good enough"* e *"systems engineering is the art of the good
enough"*. **Não fundir com o satisficing de Simon** — Kossiakoff fala de escolha de
projeto pelo engenheiro; Simon, de decisão sob limitação cognitiva.
→ **Não sustenta:** nada quantitativo. Nenhuma taxa de erro, nenhum parâmetro, nenhum
modelo de equipe, nenhum dado.
→ **Usada em:** §1.1, §1.2 e §2.1 da monografia.

**✓ BKCASE EDITORIAL BOARD.** *The Guide to the Systems Engineering Body of Knowledge
(SEBoK)*, versão 2.14. Hoboken: The Trustees of the Stevens Institute of Technology,
2026. Liberada em 18 maio 2026. 1.705 p. PDF em `Refs_tcc1/Livros`.
→ **Conferido no PDF primário (05/10/2026):** folha de abertura, que registra
*"Released 18 May 2026"* e *"Version 2.14"*; e as páginas impressas 38 e 144–145.
**Leitura declarada: os artigos *Systems Engineering Overview* e *Systems of Systems
(SoS)***, não as 1.705 páginas.
→ **Nota sobre a forma de citar.** Obra coletiva, versionada, de origem em *wiki*. A
versão e a data de liberação **são parte da referência**, porque o conteúdo muda entre
versões.
→ **Sustenta a definição institucional de Engenharia de Sistemas.** *Systems Engineering
Overview*, **p. 38**: *"Systems engineering (SE) is a transdisciplinary approach and
means to enable the realization of successful systems."* E, na mesma página: *"An
engineered system is a technical or socio-technical system which is the subject of an SE
life cycle."* — a palavra **sócio-técnico** na definição é o que autoriza tratar a
equipe humana como parte do sistema, e não como ruído externo.
→ **Sustenta, com nome da área e em fonte institucional, o problema que este trabalho
compara.** *Systems of Systems (SoS)*, **p. 145**, primeiro dos sete *pain points*
catalogados pelo grupo de trabalho da INCOSE: *"SoS Authorities. In a SoS each
constituent system has its own local 'owner' with its stakeholders, users, business
processes and development approach. As a result, the type of organizational structure
assumed for most traditional systems engineering under a single authority responsible
for the entire system is absent from most SoS."*
→ **Sustenta que a alternativa ao controle centralizado é problema aberto, não solução
conhecida.** Mesma página, segundo *pain point*: *"Leadership. [...] This question of
leadership is experienced where a lack of structured control normally present in SE of
systems requires alternatives to provide coherence and direction, such as influence and
incentives."* A obra registra que faltam alternativas; **não** diz qual funciona.
→ **Sustenta que o processo precisa ser adaptado, não só aplicado.** **p. 144**:
*"systems engineering processes are in most cases implemented for engineering both the
constituent systems and the system of systems and need to be tailored to support the
characteristics of SoS."*
→ **Não sustenta:** nenhum valor, nenhum modelo, nenhuma recomendação de arranjo. É obra
de síntese: cataloga o estado do conhecimento, não produz resultado.
→ **Usada em:** §1.2 e §2.1.

**✓ ZHU, J.; MOSTAFAVI, A.** Towards a new paradigm for management of complex
engineering projects: a system-of-systems framework. In: *2014 IEEE International
Systems Conference Proceedings* (8th Annual IEEE Systems Conference — SysCon). IEEE,
2014. p. 213–219. DOI: 10.1109/SysCon.2014.6819260. PDF em `Refs_tcc1/Artigos Centrais`;
também anexado ao Projeto.
→ **Conferido no PDF primário (05/10/2026), p. 1 e 6 da paginação do PDF.** O PDF não
traz volume nem páginas: só a linha *"978-1-4799-2086-0/14/$31.00 ©2014 IEEE"*.
Conferência, páginas e DOI conferidos no registro Crossref em 05/10/2026.
→ **Opõe, na literatura, os dois arranjos que o simulador compara.** Resumo, **p. 1**:
*"The traditional project management paradigm is mainly based on centralized planning and
control. The centralized planning and control are rooted in a reductionism perspective in
which engineering projects are identified as monolithic systems while, in reality, complex
engineering projects are systems-of-systems."*
→ **Sustenta que a crítica ao controle centralizado é posição estabelecida, e nomeia o
CPM entre as ferramentas dessa tradição.** **p. 1**: *"Traditional project management
frameworks are based on centralized planning and control in which the tools and techniques
(e.g., work breakdown structure and critical path method) are rooted in a reductionism
perspective"*. **Registrar que este trabalho usa o CPM**, para a componente de criticidade
do `D_i` — não é contradição, mas precisa ser dito: aqui o CPM mede folga da tarefa, não
governa a equipe.
→ **Sustenta a nomenclatura PM 1.0 / PM 2.0** para a oposição entre planejamento
centralizado descendente e abordagem ascendente, **p. 1**.
→ **Não sustenta nada de empírico, e os autores dizem isso.** Resumo, **p. 1**: o
*framework* *"can be tested by researchers from different engineering fields to advance the
body of knowledge"*. Conclusão, **p. 6**: *"The use of the proposed framework will
facilitate the creation of tools and techniques"* — promessa, não resultado. **Nunca citar
como evidência de que governança descentralizada funcione melhor.**
→ **Usada em:** §1.1, §1.2 e §2.1.

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

**✓ XU, X.; ZOU, P. X. W.** System dynamics analytical modeling approach for construction
project management research: a critical review and future directions. *Frontiers of
Engineering Management*, v. 8, n. 1, p. 17–31, 2021. DOI: 10.1007/s42524-019-0091-7.
PDF em `Refs_tcc1/Métricas de Interação Humana`.
→ **Conferido no PDF primário (05/10/2026), p. 1, 11 e 12 da paginação do PDF.**
→ **⚠ Armadilha de citação, conferida.** O PDF traz *"© Higher Education Press 2020"* e
está paginado 1–15: é a versão *online-first*, de 11/03/2020. O fascículo de registro é
**v. 8, n. 1 (mar. 2021), p. 17–31**, conferido nos metadados do editor em 05/10/2026.
**Citar "2020, p. 1–15" estaria errado.**
→ **Sustenta que a Dinâmica de Sistemas é abordagem estabelecida em gestão de projetos de
construção.** Revisão de **105 artigos publicados entre 1994 e 2018**.
→ **Sustenta que a aplicação frequentemente é malfeita, e nomeia onde.** Resumo: *"many
studies have failed to apply SD accurately"*; e *"When applying SD method to model
construction system, the following aspects must be carefully considered: Model boundary,
model development, model test, and model simulation."* É justificativa, vinda de dentro da
área, para o capítulo de verificação.
→ **Sustenta o híbrido e o fator humano como direções reconhecidas da área.** **p. 11**:
*"three future research directions of SD in construction project management are proposed
(Fig. 8), namely, hybrid modeling, uncertainty analysis, and human factor analysis."*
→ **Não sustenta:** o domínio é **obra civil**, não projeto de engenharia em geral. A
revisão não avalia modelos híbridos ABM + DS em particular, não valida nenhum modelo e não
fornece parâmetro, magnitude ou faixa.
→ **Usada em:** §2.2 e §6.1.

**✓ BALDWIN, W. C.; SAUSER, B.; CLOUTIER, R.** Simulation approaches for system of
systems: events-based versus agent based modeling. *Procedia Computer Science*, v. 44,
p. 363–372, 2015. DOI: 10.1016/j.procs.2015.03.032. Apresentado na *2015 Conference on
Systems Engineering Research*. Acesso aberto (CC BY-NC-ND). PDF em `Refs_tcc1/Artigos
Centrais`; também anexado ao Projeto.
→ **Conferido no PDF primário (05/10/2026), p. 363 e 371.** Volume e páginas constam do
PDF e foram confirmados no Crossref.
→ **Sustenta a escolha de agentes por comparação empírica, não por preferência.** Resumo,
**p. 363**: *"We review different modeling techniques and use two converse techniques, i.e.
agent-based and event-based modeling, to run a simulation of hypothetical systems
collaborating into a SoS. The results of the empirical comparison indicate an agent-based
modeling approach would achieve a characterization model better with validation achieved
through an event-based approach."*
→ **Sustenta a lacuna que justifica construir um simulador.** Conclusão, **p. 371**: *"Few
simulations were found in the literature where the basis for the model is the SoS behavior
or the actions of the component systems. Furthermore no simulations were found where the
SoS characteristics are directly modeled in order to produce the simulation. Therefore
there appears to be a gap in the literature for modeling and simulating the behavior of
SoS."*
→ **Não sustenta:** os sistemas simulados são **hipotéticos**, declaradamente. Sem equipe,
sem projeto de engenharia, sem dado de campo. E a comparação é agentes × eventos discretos,
**não** agentes × dinâmica de sistemas — não é respaldo do híbrido.
→ **Usada em:** §2.3.

**✓ SILVA, R. de A.; BRAGA, R. T. V.** Simulating systems-of-systems with agent-based
modeling: a systematic literature review. *IEEE Systems Journal*, v. 14, n. 3,
p. 3609–3617, set. 2020. DOI: 10.1109/JSYST.2020.2980896. PDF em `Refs_tcc1/Artigos
Centrais`; também anexado ao Projeto.
→ **Conferido no PDF primário (05/10/2026), p. 1, 3 e 8 da paginação provisória.**
→ **⚠ Armadilha de citação.** O PDF é a versão aceita, com o aviso impresso em todas as
páginas: *"This article has been accepted for inclusion in a future issue of this journal.
Content is final as presented, with the exception of pagination."* **Não tem volume, número
nem páginas finais.** Os dados acima vêm do registro Crossref, conferido em 05/10/2026.
Citar a paginação do PDF (1–9) estaria errado.
→ **Sustenta as razões técnicas de usar agentes para sistemas de sistemas.** **p. 1**, entre
as cinco razões: *"ABM provides the necessary dynamics for investigating emergent
behaviors"* e *"ABM follows the same principle of an SoS (i.e., guided by objectives,
autonomicity, and adaptability)"*.
→ **Sustenta a tipologia de arranjos de controle, e dá nome de literatura ao contraste deste
trabalho.** **p. 1**: dirigido, com *"a coordinator agent that controls (with authority) all
the constituent systems"*; reconhecido; colaborativo, com *"a decentralized control (i.e.,
there is no coordinator agent)"*; e virtual. **Os dois arranjos comparados aqui são os
extremos dessa tipologia.**
→ **Sustenta a lacuna em ferramentas.** Conclusão, **p. 8**: *"we also need to enhance the
current SoS simulation tools. The simulators identified do not encompass a large number of
frameworks, approaches, or models, therefore, being risky to perform SoS simulations that
need to have all this joint"*; e, entre as recomendações, *"simulating agent-based models by
considering the existing types of SoS"*.
→ **Não sustenta:** nenhum valor, nenhuma magnitude. É revisão: não simula, não mede, não
valida. Domínio: sistemas de sistemas em geral, não equipes humanas.
→ **Usada em:** §1.2 e §2.3.

**✓ SOYEZ, J.-B.; MORVAN, G.; MERZOUKI, R.; DUPONT, D.** Multilevel agent-based modeling of
system of systems. *IEEE Systems Journal*, v. 11, n. 4, p. 2084–2095, dez. 2017.
DOI: 10.1109/JSYST.2015.2429679. PDF em `Refs_tcc1/Artigos Centrais`; também anexado ao
Projeto.
→ **Conferido no PDF primário (05/10/2026), p. 1 e 10 da paginação provisória.**
→ **⚠ Mesma armadilha, e pior.** O PDF é a versão aceita, com o mesmo aviso de paginação
provisória, e o campo de título dos metadados traz só o nome de arquivo
(`jsyst-soyez-2429679-x.pdf`). Volume, número, páginas e **ano** (2017, não 2015, que é o
ano do DOI) vêm do Crossref, conferido em 05/10/2026. **Citar 2015 estaria errado.**
→ **Sustenta o tratamento multinível como problema formal reconhecido** — o que a
arquitetura híbrida enfrenta: agentes no nível do indivíduo, estoques e fluxos no da equipe.
Resumo, **p. 1**: *"Multilevel aspects are modeled with the Influence Reaction Model for
Multilevel Simulation (IRM4MLS) agent-based meta-model."*
→ **Sustenta que reorganização por mudança de objetivo ou de capacidade é elemento previsto
nesse tipo de modelo.** Resumo, **p. 1**: *"They consider reorganization of SoSs caused by
changes of goals or subsystem capacity."*
→ **Não sustenta o arranjo adaptativo — e isto precisa estar escrito.** Conclusão, **p. 10**:
*"We proposed a generic multilevel multiagent formalism to represent a SoS managed by a
central authority."* **O formalismo pressupõe autoridade central**, que é um dos dois
arranjos, não os dois. **Não citar Soyez como respaldo da descentralização.**
→ **Não sustenta:** nada de empírico sobre equipes. É formalismo, ilustrado por estudo de
caso de veículos autônomos em terminal portuário (projeto europeu InTraDE).
→ **Usada em:** §2.3.

**✓ MAZZETTO, S.** Interdisciplinary perspectives on agent-based modeling in the
architecture, engineering, and construction industry: a comprehensive review. *Buildings*,
v. 14, n. 11, art. 3480, 2024. DOI: 10.3390/buildings14113480. Acesso aberto. PDF em
`Refs_tcc1/Artigos Centrais`; também anexado ao Projeto.
→ **Conferido no PDF primário (05/10/2026), p. 1;** volume, número e artigo confirmados no
Crossref. Revisão de **178 documentos publicados entre 1970 e 2024**.
→ **Sustenta que a Modelagem Baseada em Agentes está estabelecida no setor de arquitetura,
engenharia e construção.** Serve para situar o método, e só.
→ **⚠ NÃO sustenta o número que o próprio resumo anuncia.** O resumo, **p. 1**, afirma:
*"ABM is shown to reduce project delays by up to 15% through enhanced resource
allocation"*. **Procurado "15%" nas 42 páginas: aparece uma vez, no resumo, e em nenhum
outro lugar do artigo.** Não há estudo, tabela, agregação ou citação que sustente a cifra
dentro do texto. **Não citar os 15%.** Registrado porque é cifra atraente, fácil de repetir
e indefensável na banca.
→ **Não sustenta:** nenhum parâmetro, nenhuma magnitude, nenhuma validação. Revisão
narrativa, e o tom do resumo é promocional — *"transformative impact"*, *"indispensable
role"*, *"revolutionizing"*. Usar com parcimônia, apenas para situar o método.
→ **Usada em:** §2.3, uma frase de contextualização.

## Variáveis qualitativas em modelos de simulação

> Entraram em 05/10/2026, para §2.4 da monografia. São a formulação do problema que a
> lógica difusa deste trabalho enfrenta — **não** respaldo do método adotado.

**✓ COYLE, R. G.** Qualitative modelling in system dynamics, or what are the wise limits of
quantification? *Keynote address.* In: *Proceedings of the 17th International Conference of
the System Dynamics Society*, Wellington, Nova Zelândia, 20–23 jul. 1999. Manuscrito
paginado 1–22. Disponível em:
`https://proceedings.systemdynamics.org/1999/PAPERS/KEYNOTE1.PDF`. PDF em
`Refs_tcc1/Métricas de Interação Humana`.
→ **Conferido no PDF primário (05/10/2026), páginas 2, 11 e 12 do manuscrito.** A paginação
é do próprio manuscrito, não de revista — declarar isso ao citar página.
→ **Conferência, ordinal e datas conferidos na página dos anais oficiais (05/10/2026):**
*"The 17th International Conference of The System Dynamics Society [...] July 20 - 23, 1999
--- Wellington, New Zealand"*, realizada em conjunto com a 5ª Australian & New Zealand
Systems Conference.
→ **Confirmação independente da natureza do documento:** McLucas (2003), na própria lista de
referências, registra *"Coyle, R.G. 1999. Qualitative modelling in system dynamics or what
are the wise limits to quantification? Keynote address: Conference of the System Dynamics
Society, Wellington, New Zealand."*
→ **Sustenta que quantificar variável mal medida é problema reconhecido dentro da própria
Dinâmica de Sistemas, e não ressalva inventada aqui.** Resumo, **p. 2**: *"The paper briefly
reviews that debate and then discusses some of the problems involved in quantification.
Those problems are exemplified by an analysis of a particular model which turns out to bear
little relation to the real problem it purported to analyse."*
→ **Sustenta, nominalmente, três decisões de formulação deste trabalho como questões abertas
da disciplina.** Agenda de pesquisa, **p. 11–12**: *"Attempting to establish principles for
deducing the shape and values of non-linearities."*; *"Developing a technique for handling
multiple non-linear effects on a given variable, so as to avoid double-counting."*; e
*"Defining a procedure for establishing the forms of relationships involving multipliers,
that is whether the factors are multiplicative, additive, minimising or whatever."*
→ A terceira é literalmente o caso de `E = D·P/B`, que é multiplicativo, e da escolha da
t-norma do sistema difuso (mínimo ou produto). **Coyle registra em 1999 que não existe
procedimento estabelecido para decidir isso.** Com essa fonte, a varredura de t-norma deixa
de ser detalhe de implementação e passa a ser resposta a uma lacuna declarada da área.
→ **Sustenta o critério de risco adotado.** **p. 12**: *"how can we guard against models
which risk becoming plausible nonsense?"*
→ **Não sustenta:** nenhum valor, nenhuma forma funcional, nenhuma recomendação. É
*keynote*: sem dado, sem amostra, sem teste. E Coyle argumenta **a favor** de modelos
qualitativos — ele descreve o risco da quantificação, não a endossa.
→ **⚠ Não confundir** com **COYLE, R. G.** Qualitative and quantitative modelling in system
dynamics: some research questions. *System Dynamics Review*, v. 16, n. 3, 2000 — texto
distinto, com outro título, citado por McLucas. **Não citar o keynote como se fosse o artigo
da revista**, e não atribuir ao keynote páginas de fascículo.
→ **Usada em:** §2.4.

**✓ McLUCAS, A. C.** Incorporating soft variables into system dynamics models: a suggested
method and basis for ongoing research. In: *Proceedings of the 21st International Conference
of the System Dynamics Society*, Nova York, 20–24 jul. 2003. 12 p. Disponível em:
`https://proceedings.systemdynamics.org/2003/proceed/PAPERS/214.pdf`. PDF em
`Refs_tcc1/Métricas de Interação Humana`.
→ **Conferido no PDF primário (05/10/2026), p. 1 e notas de fim.** Título e autoria
confirmados no arquivo dos anais oficiais (`2003/proceed/PAPERS/214.pdf`).
→ **Ordinal, cidade e datas conferidos na página dos anais oficiais (05/10/2026):** *"21st
System Dynamics Conference [...] July 20 - 24, 2003 --- The Roosevelt Hotel --- New York
City"*.
→ **⚠ Os metadados internos do PDF estão errados.** O campo *Title* do arquivo diz *"Towards
A Robust Methodology For Handling Social 'Variables' In SD Modelling"*, que **não é o título
deste trabalho** — é de outro texto do mesmo autor. O correto está na folha de abertura. Quem
extrair metadado automaticamente pega o título errado.
→ **Sustenta que incorporar variável "soft" de forma confiável é fraqueza reconhecida da
prática de Dinâmica de Sistemas.** Resumo, **p. 1**: *"This paper identifies a weakness in
system dynamics modelling practice, that is, in reliably incorporating soft variables into
system dynamics models."*
→ **Sustenta a exigência de hipótese testada em vez de chute — justificativa metodológica da
varredura de premissas e do History Matching.** **p. 1**: *"We must avoid making guesses
about the influences that soft variables might have. Rather, we must create and repeatedly
test dynamic hypotheses about soft variables."*
→ **Sustenta a crítica à expressão pseudoalgébrica e a exigência de consistência
dimensional.** Nota de fim **iii**: *"in econometric modelling there is an implicit
assumption that statistical correlation among a group of variables is seen as causality. In
effect this is what modellers are doing when they produce the type of pseudo-algebraic
expressions described in our opening example. With statistical correlation it is easy to
ignore demands for dimensional consistency."*
→ **Não sustenta o método deste trabalho.** McLucas propõe combinar *systems thinking*,
análise de causalidade e análise de decisão multicritério (*conjoint analysis*); aqui se usa
lógica difusa. São soluções **diferentes** para o mesmo problema. Citar na formulação do
problema, nunca como respaldo do método adotado.
→ **Usada em:** §2.4.

**✓ PLUCHINOTTA, I.; ZHOU, K.; ZIMMERMANN, N.** Dealing with soft variables and data
scarcity: lessons learnt from quantification in a participatory system dynamics modelling
process. *System Dynamics Review*, v. 40, n. 4, e1770, 2024. DOI: 10.1002/sdr.1770. Acesso
aberto (CC BY). PDF em `Refs_tcc1/Métricas de Interação Humana`.
→ **Conferido no PDF primário (05/10/2026), p. 1 e 3.** DOI e fascículo lidos no próprio
arquivo.
→ **Sustenta que quantificar o intangível sob escassez de dado é problema aberto e
reconhecido na revista da própria área.** Resumo, **p. 1**: *"Although this explorative
nature is one of the key advantages, it also represents a challenge for quantifying the
intangible, i.e. more qualitative aspects of an SD model, especially when it is not possible
to apply conventional analytical methods due to data scarcity. Procedures to obtain and
analyse information using participatory approaches are limited."*
→ **Sustenta que a prática aceita é declarar o procedimento de quantificação**, e não ter
dado para tudo: a contribuição anunciada é um *quantification framework* em função da
disponibilidade de dado e do grau de envolvimento de interessados. É o que legitima o esquema
de rótulos `[LIT]`, `[CALIB]`, `[DEC]` e `[ABERTO]`.
→ **Não sustenta:** nenhum valor. E o contexto é **modelagem participativa com
interessados**, que não é o caso aqui — não houve elicitação com participantes. Citar como
enquadramento do problema, não como método seguido.
→ **Usada em:** §2.4; e §8.3–8.4, como literatura que trata escassez de dado como condição
normal da área, não como defeito deste trabalho.

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

## Estresse agudo e função executiva — apoio conceitual a `mu_cog`

> Entraram em 28/09/2026, depois do fechamento do modelo. São apoio conceitual ao
> construto de degradação cognitiva e origem de uma limitação declarada. **Nenhum
> parâmetro foi calibrado por causa delas.**

**✓ ARNSTEN, A. F. T.** Stress signalling pathways that impair prefrontal cortex
structure and function. *Nature Reviews Neuroscience*, v. 10, n. 6, p. 410–422, 2009.
DOI: 10.1038/nrn2648. Acesso aberto: `https://pmc.ncbi.nlm.nih.gov/articles/PMC2907136/`.
PDF em `Refs_tcc2`.
→ **Conferido no PDF primário (29/09/2026), páginas 410, 411 e 412.**
→ **Sustenta a sensibilidade do raciocínio à pressão.** Resumo, **p. 410**: *"Even quite
mild acute uncontrollable stress can cause a rapid and dramatic loss of prefrontal
cognitive abilities, and more prolonged stress exposure causes architectural changes in
prefrontal dendrites."*
→ **Sustenta a seletividade — e é isto que ancora a Porta 1.** Seção *Acute stress impairs
PFC function*, **p. 410**: *"the types of tasks that were impaired by stress were those
that required PFC operations, whereas engrained habits that rely on basal ganglia circuits
were spared or enhanced."* Não é perda uniforme de capacidade: é troca de deliberação por
automatismo.
→ **Sustenta o mecanismo da troca.** **Box 1, p. 411**: *"attention regulation switches
from thoughtful 'top-down' control by the PFC that is based on what is most relevant to the
task at hand to 'bottom-up' control by the sensory cortices"*; *"The amygdala also biases us
towards habitual motor responding rather than flexible, spatial navigation"*; e *"during
stress, orchestration of the brain's response patterns switches from slow, thoughtful PFC
regulation to the reflexive and rapid emotional responses of the amygdala"*. Síntese na
**p. 412**: *"acute uncontrollable stress impairs PFC-mediated cognitive functions in humans
and animals and switches the control of behaviour and emotion to more primitive brain
circuits."*
→ **Não sustenta:** nenhum valor. É neurobiologia, boa parte em roedores e primatas, sem
tarefa de engenharia e sem taxa de erro. Não vira `mu_minimo` nem `F_ancora`.
→ **Usada em:** fundamentação do construto de `mu_cog` e da Porta 1.

**✓ DOROC, K.; YADAV, N.; MURAWSKI, C.** Acute stress impairs decision-making at varying
levels of decision complexity. *Communications Psychology*, v. 3, art. 179, 2025.
DOI: 10.1038/s44271-025-00355-x. Acesso aberto. PDF em `Refs_tcc2`.
→ **Conferido no PDF primário (29/09/2026), p. 1.**
→ **Desenho, do resumo:** *"a within-participants laboratory experiment in which university
students (n = 42) made objective decisions of varying complexity (computational hardness)
under both acutely stressful and control conditions."* Estresse induzido pelo Trier Social
Stress Test.
→ **Sustenta o elo pressão → qualidade da decisão, em tarefa com gabarito objetivo.**
Resumo: *"We find that higher cortisol levels, induced via the Trier Social Stress Test,
leads to lower decision quality and a higher incidence of experienced time pressure."* E a
conclusão: *"Our results demonstrate that acute stress impairs the capacity to decide
correctly, and highlights the importance of computational hardness and time pressure as
potential moderators of this effect."*
→ **Sustenta a pressão de tempo como moderador — declarado post-hoc pelos autores.** Resumo:
*"Post-hoc, we find that the most substantial deficits in decision quality occurred when
acute stress was accompanied by time pressure, with gaze-tracking analyses offering
tentative evidence that changes in attention allocation may be one mechanism for this
effect."* Isso favorece a arquitetura deste trabalho, em que a variável operante é
`E = D·P/B` — mas a etiqueta *post-hoc* é obrigatória ao citar.
→ **Não sustenta:** nenhuma magnitude. 42 estudantes, laboratório, efeitos de poucos pontos
percentuais de acurácia. E a coincidência de a tarefa ser combinatória, como o PSPLIB, é
coincidência de família de problema — **não** validação do simulador.
→ **⚠ Nota de integridade:** uma versão anterior desta entrada citava *"acute stress alone
has a surprisingly limited effect on decision-making"* como sendo dos autores. **Essa frase
não existe no artigo** — veio de extração automática e foi removida em 29/09 após leitura do
PDF. Registrado para que não volte.
→ **Usada em:** sustentação empírica do elo pressão → qualidade da decisão.

**✓ SAPOLSKY, R. M.** Stress and the brain: individual variability and the inverted-U.
*Nature Neuroscience*, v. 18, n. 10, p. 1344–1346, out. 2015. DOI: 10.1038/nn.4109.
PMID 26404708. PDF em `Refs_tcc2`.
→ **Conferido no PDF primário (28/09/2026), páginas 1344–1346.** É um **Commentary**, não
artigo de pesquisa: não traz dado novo. Citar como perspectiva de autoridade, não como
evidência.
→ **Sustenta a forma da curva, e ela inclui um platô.** p. 1346: *"the effects of stress in
the brain form a nonlinear 'inverted-U' dose–response curve as a function of stressor
severity: the transition from the complete absence of stress to mild stress causes an
increase in endpoint X, the transition from mild-to-moderate stress causes endpoint X to
plateau and the transition from moderate to more severe stress decreases endpoint X."*
→ **Sustenta que a posição do pico é questão em aberto.** p. 1346: *"For any particular
stressor, setting and context, where along the axis of stressor severity is the peak of an
individual's inverted-U?"* Ele lista isso entre as perguntas que deveriam ocupar o campo.
→ **Não sustenta posicionar o pico na escala de `P`.** A Figura 1, p. 1345, é rotulada
*"Conceptualization"* e tem no eixo horizontal concentração de corticosterona de 0 a 50
μg/dl, faixa benéfica em 10–20, *"the species-specific glucocorticoid of rats and mice"*.
Não há tradução para pressão de cronograma.
→ **Usada em:** enquadramento da faixa `P ∈ [0,30; 1,00]` como escopo declarado, e
justificativa de não modelar o ramo ascendente.

### Não usar — Peter Levine / ônibus espacial

A alegação de que Peter Levine teria trabalhado com a NASA no programa do ônibus espacial
aparece na biografia do site do próprio instituto dele, não em estudo, artigo ou relatório
da NASA. Procurado em 28/09/2026: não há publicação correspondente. **Não é fonte citável.**

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

**✓ PROBST, T. M.; ESTRADA, A. X.** Accident under-reporting among employees: testing the
moderating influence of psychological safety climate and supervisor enforcement of safety
practices. *Accident Analysis and Prevention*, v. 42, n. 5, p. 1438–1444, 2010.
DOI: 10.1016/j.aap.2009.06.027. PDF em `Refs_tcc2`.
→ **Conferido no PDF primário (28/09/2026), páginas 1438, 1441 e 1442.** 425 empregados de
5 setores de risco acima da média.
→ **Sustenta o construto de `p_reporte` na etapa causal certa** — acidente vivido pelo
trabalhador → reportado ou não à organização, que é a decisão do agente no modelo. Resumo,
p. 1438: *"There was an average of 2.48 unreported accidents for every accident reported to
the organization."*
→ **Sustenta a dependência do clima.** §3.2, p. 1441: *"when the organizational safety
climate was perceived to be positive, there was relatively little discrepancy between the
number of reported and unreported accidents. However, when the climate was perceived to be
poor, the ratio of accident under-reporting significantly increased to more than 3
unreported accidents for every 1 reported."* F(1, 361) = 8,94, p < 0,005, η² = 0,02.
→ **Sustenta o mecanismo, não só a associação.** §3.3.1 e Tabela 3, p. 1442: 54% dos
empregados vivenciaram e deixaram de reportar um acidente no ano anterior; entre os motivos,
37,5% marcaram *"I did not want to be the one to break the company's accident-free record"*;
e 64% relataram ao menos uma consequência negativa por ter reportado, incluindo ser culpado
pelo incidente (23,9%). É o construto de Edmondson medido em comportamento, não em escala
de atitude.
→ **Não sustenta os valores 0,75 e 0,15.** Pela Figura 1, p. 1442, a probabilidade de
reportar fica em torno de 0,24 sob clima ruim e 0,40 sob clima positivo — razão de 1,7,
contra a razão de 5 dos cenários do modelo. **O contraste declarado é mais extremo que o
observado**, e leitura de figura é aproximada. Os oito parâmetros de governança permanecem
premissas de cenário, varridas.
→ **Não confundir** com Probst, Brubaker & Barsotti (2008), *Journal of Applied Psychology*,
93(5), 1147–1154, cujo índice mede **empresa → OSHA**, e não trabalhador → empresa.
Descartada para `p_reporte` por essa razão.
→ **Usada em:** sustentação do construto de `p_reporte` e da sua dependência do clima.

**✓ MONTGOMERY, A.; CHALILI, V.; LAINIDI, O.; MOURATIDIS, C.; MALIOUSIS, I.;
PAITARIDOU, K. et al.** Psychological safety and patient safety: a systematic and narrative
review. *PLOS One*, v. 20, n. 4, e0322215, 2025. DOI: 10.1371/journal.pone.0322215.
Acesso aberto. PDF em `Refs_tcc2`.
→ **Conferido no PDF primário (29/09/2026), páginas 9 e 10.** Nove estudos quantitativos,
N = 17.926, 88,4% enfermeiros.
→ **Sustenta que o elo entre segurança psicológica e reporte de erro é CONTESTADO.**
Discussão, p. 9: *"Overall, there is relatively little hard data to link PS and patient
safety outcomes. Only nine studies fit the criteria [...] This is stark contrast to
literature that purports a clear link between the two phenomena."* Conclusões, p. 10:
*"Ultimately, we are left with a paradox regarding PS in healthcare teams. Reporting patient
safety problems in a team can be both an indication of high and low levels of PS."*
→ **Sustenta o confundimento que o modelo resolve — e a revisão o diz por conta própria.**
p. 9, sobre Halbesleben et al.: *"looking at only one indicator (e.g., frequency) may not
represent the whole picture of safety, whereby a low frequency of injuries may actually be
an indication of low reporting rather than an indication that the organization scores high
on safety."* A literatura mede **erros reportados**, que é `erros cometidos × probabilidade
de reportar`, e não consegue separar os dois. **O modelo separa por construção:**
`p_reporte` é condicional ao erro ter ocorrido, e o erro é gerado por outro mecanismo. O
simulador enxerga o erro oculto, que é o que o pesquisador de campo não enxerga.
→ **Sustenta o mecanismo do duplo vínculo.** p. 9: *"when employees adhere to a norm that
says, 'hide errors,' they know they are violating another norm that says, 'reveal errors'.
The employees are thus in a double bind."* E p. 10, citando Kaldjian et al.: *"a gap exists
between the intention to report and the actual act of reporting medical errors, due to
severe repercussions."*
→ **Não sustenta:** nenhum valor, e **não sustenta a direção que o modelo assume**. Entra
como ressalva e como argumento, não como apoio. Os autores registram a própria cautela,
p. 9: *"Absence of evidence is not evidence of absence."*
→ **Usada em:** discussão — a separação entre frequência de erro e propensão a reportar é
contribuição do modelo, não premissa dele.

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

**✓ KELLER, A. C.; MEIER, L. L.** It's a new day — is it? Testing accumulation and
sensitisation effects of workload on fatigue in daily diary studies. *Work & Stress*,
v. 38, n. 3, p. 231–247, 2024. DOI: 10.1080/02678373.2023.2251124. Acesso aberto (CC BY);
publicado online em 28/08/2023. PDF em `Refs_tcc2`.
→ **Conferido no PDF primário (28/09/2026), páginas 231, 240, 241 e 243.** Quatro estudos
de diário, média de 166 participantes e 1.406 observações por estudo, 10 dias úteis.
→ **Sustenta o mecanismo da bateria na escala que o modelo resolve.** Tabela 4, p. 240: o
coeficiente de carga sobre fadiga **dentro do dia** é 0,18 / 0,08 / 0,15 / 0,24 nos quatro
estudos, todos p < 0,05. Resumo, p. 231: *"workload had positive concurrent effects on
fatigue [...] workload had positive effects on fatigue within one day."*
→ **Não sustenta a persistência entre dias.** Mesma tabela: o acúmulo dos dias anteriores dá
0,01 / −0,01 / −0,01 / 0,04, nenhum significativo.
→ **Nem sustenta o contrário — ressalva dos próprios autores.** p. 243: *"All four studies
ran for ten working days only, and it is possible that the accumulation and sensitisation
effects of workload require more time."* E p. 241: *"Previous research has reported the
effects of stressors on next-day strain (e.g. Zhang et al., 2016), whereas others have
failed to find such effects (e.g. Demerouti & Cropanzano, 2017)."*
→ **Atenção ao verbo.** Os autores escrevem *insufficient support*, não *no effect*.
Escrever "a literatura mostra que a fadiga não acumula" seria sobre-afirmar.
→ **Usada em:** apoio ao elo carga → fadiga dentro do período; e limitação declarada quanto
à persistência entre períodos, acompanhada do teste E-BAT.

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


## Avaliada e não incorporada em 05/10/2026

- **Hu, Y.; Wu, L.; Li, N.; Zhao, T.** Multi-agent decision-making in construction
  engineering and management: a systematic review. *Sustainability*, v. 16, n. 16,
  art. 7132, 2024. DOI: 10.3390/su16167132. PDF em `Refs_tcc1/Artigos Centrais`; anexada
  ao Projeto.
  **Lida no PDF primário em 05/10/2026 (p. 1 e 6) e descartada por leitura, não por
  esquecimento.** O "multi-agent" do título significa **múltiplas partes interessadas
  humanas**, não agentes computacionais: *"Construction engineering and management (CEM)
  involves multiple stakeholders, complex interest relationships, and conflicts"*. A
  expressão *agent-based modeling* aparece no artigo apenas como item de um agrupamento de
  palavras-chave num mapa bibliométrico, **p. 6**. **Citá-la em §2.3 como apoio ao método
  seria erro de leitura** — erro fácil, porque o título convida a ele. Não acrescenta ao que
  Silva & Braga, Baldwin, Xu & Zou e Zhu & Mostafavi já sustentam. Registrada aqui para que
  não volte por engano.

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
