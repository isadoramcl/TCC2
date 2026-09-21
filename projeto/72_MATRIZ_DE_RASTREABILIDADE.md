# 72 — Matriz de rastreabilidade das fontes

**Data:** 20/09/2026
> **HISTÓRICO — não usar como catálogo.** O catálogo canônico é
> `projeto/04_FONTES.md`. Esta matriz marcou como "não obtidas" cinco fontes que
> o catálogo já tinha conferido (retratação R-22) e confundiu homônimos de Ball e
> White. Mantida só como registro do erro.

---

## Como ler

**Estado de verificação:**

| | |
|---|---|
| **LIDO** | texto integral aberto neste trabalho; trechos citados conferidos na página |
| **PARCIAL** | metadados e resumo conferidos na origem; texto integral **não** aberto |
| **REPRODUZIDO** | fonte de dados ou algoritmo, verificado por reprodução do resultado publicado |
| **NÃO OBTIDO** | citado em documento interno, nunca obtido — **não pode ser citado na monografia** |

A coluna **não sustenta** não é formalidade. Existe porque a maior parte das
retratações deste trabalho veio de atribuir a uma fonte algo adjacente ao que
ela diz.

---

## 1. Âncoras do modelo de erro

### Stewart, M. G.; Melchers, R. E. (1988) — **LIDO**

*Checking models in structural design.* Journal of Structural Engineering.
**⚠ Completar volume, número e páginas antes de citar.**

| | |
|---|---|
| **Sustenta** | Tabela 1, p. 290: taxa de erro por microtarefa de projetistas civis profissionais. `p(k) = k × 0,0128` exato para k = 1, 2, 3, 4, 5 e 8. Consulta a tabela: 0,0126. Fig. 1, p. 287: nó de omissão antes do nó de comissão |
| **Usada em** | Ancoragem de `F_ancora` (controle C1); estrutura da Porta 1 |
| **Não sustenta** | Valores de `F_ancora` acima de 0,10 — exigem k > 8, o maior publicado. As taxas de omissão de 0,40 a 0,80 são de **um** fator de redução específico e não transportam como "taxa de atalho". A hipótese (v) do artigo, sobre ausência de pressão temporal, é **declaração de escopo**, não resultado |

### Stewart, M. G. (1992) — **LIDO**

*Modelling human error rates for human reliability analysis of a structural
design task.* Reliability Engineering & System Safety.
DOI [10.1016/0951-8320(92)90097-5](https://doi.org/10.1016/0951-8320(92)90097-5).
**⚠ Completar volume e páginas.** Páginas consultadas: 173–177.

| | |
|---|---|
| **Sustenta** | Tabela 1, p. 173: 94 respondentes, 38 erros, 2 327 microtarefas, `p_av = 0,0163`. Tabela 2, p. 175: binomial rejeitada (χ² = 10,174, crítico 5,991); beta-binomial χ² = 0,162; p-dependente χ² = 0,583. `CV = 1,13`, `α = 0,7546`, `β = 45,4563`, `φ = 0,845` |
| **Usada em** | Heterogeneidade entre agentes (C2); sensibilidade à não independência (C3) |
| **Não sustenta** | **Nada sobre pressão temporal** — a manipulação falhou e o autor fundiu as amostras (p. 173). A Tabela 3 dá +27% a +44% (beta-binomial) e +94% a +111% (p-dependente), não os "20–30% e 50%" do texto corrido |
| **Achado próprio** | **A-16.** A Tabela 2 não é internamente reprodutível na precisão impressa: nenhum par (α, β) satisfaz simultaneamente os três conjuntos publicados. Discrepância de 0,012% |

### Crowder, R. M.; Robinson, M. A.; Hughes, H. P. N.; Sim, Y.-W. (2012) — **PARCIAL**

*The Development of an Agent-Based Modeling Framework for Simulating Engineering
Team Work.* IEEE Transactions on Systems, Man, and Cybernetics — Part A.
**⚠ Completar volume, número, páginas e DOI.** PDF no diretório do projeto.

| | |
|---|---|
| **Sustenta** | Equação de incremento de competência `ΔC = [15 + 3(C_k − C)]/100`; lei de atualização de confiança |
| **Usada em** | Porta 2, transferência lateral de conhecimento; dinâmica de `τ` |
| **Não sustenta** | Os escalares 15 e 3 como valores absolutos — o próprio TCC I instrui submetê-los a sensibilidade. Feito: variação de 3× move o contraste em menos de 5% |

---

## 2. Seleção de estratégia sob pressão

### Rieskamp, J.; Hoffrage, U. (2008) — **PARCIAL**

*Inferences under time pressure: How opportunity costs affect strategy
selection.* Acta Psychologica **127**(2), 258–276.
DOI [10.1016/j.actpsy.2007.05.004](https://doi.org/10.1016/j.actpsy.2007.05.004).

| | |
|---|---|
| **Sustenta** | **Construto, não valor.** Sob alta pressão de tempo as inferências são melhor previstas por LEX; sob baixa pressão, por modelo linear ponderado. Resumo conferido na origem |
| **Usada em** | Justificativa da transição estocástica para modo heurístico |
| **Não sustenta** | **Os números 7/36 e 16/36 não foram conferidos no texto integral.** Mesmo confirmados, não transportam: Rieskamp conta *participante classificado*, o modelo conta *execução de tarefa* — denominadores distintos. O Estudo 1 do mesmo artigo **não** achou o efeito |
| **⚠ Ação** | Abrir o texto integral antes de citar qualquer número, ou citar só o construto |

### Payne, J. W.; Bettman, J. R.; Luce, M. F. (1996) — **NÃO OBTIDO**

| | |
|---|---|
| **Situação** | Citado como evidência de deslocamento de estratégia sob pressão. O deslocamento aponta na direção certa mas **não é significativo** |
| **⚠ Ação** | Obter ou remover |

---

## 3. Omissão e adiamento

### Ball, J. et al. — **NÃO OBTIDO** · White, P. et al. — **NÃO OBTIDO** · Lee, S. et al. — **NÃO OBTIDO**

| | |
|---|---|
| **Situação** | Citados em pareceres internos como base do construto *care left undone*, que reenquadra a rota de fuga como adiamento por falta de tempo. **Nenhum foi obtido.** Ano, veículo e páginas desconhecidos |
| **⚠ Ação** | **Obter os três ou remover toda afirmação que se apoia neles.** Como a rota de fuga é inalcançável no ponto de operação, removê-los custa pouco ao texto |

---

## 4. Degradação de qualidade e segurança psicológica

### Reichelt, K.; Lyneis, J. (1999) — **NÃO OBTIDO**

| | |
|---|---|
| **Situação** | Citado pelos multiplicadores médios de degradação de qualidade: 0,95 por pressão de cronograma, 0,97 por fadiga de hora extra, Tabelas 1–2 |
| **Usada em** | Verificação da faixa de `mu_minimo` (E3) |
| **Ressalva obrigatória** | São saídas de modelo de Dinâmica de Sistemas calibrado, da **mesma linhagem** deste trabalho — consistência com a literatura de modelagem, não medição independente |
| **⚠ Ação** | Obter e conferir as duas tabelas, ou declarar a verificação como não realizada |

### Edmondson, A. C. (1999) — **NÃO OBTIDO**

| | |
|---|---|
| **Situação** | Citado como base do construto de segurança psicológica, que `p_reporte` encarna. Marcado NÃO VERIFICADA há semanas |
| **⚠ Ação** | É a referência canônica da área e fácil de obter. Obter |

---

## 5. Fontes de dados — verificadas por reprodução

### Shepperd, M.; Song, Q.; Sun, Z.; Mair, C. (2013) — **REPRODUZIDO**

*Data quality: Some comments on the NASA software defect datasets.*
IEEE Transactions on Software Engineering. **⚠ Completar volume, número, páginas.**

| | |
|---|---|
| **Sustenta** | Algoritmo de limpeza que separa D' de D''. **Reproduzido em 12 de 12 bases.** Resíduo de 46 registros (0,26%) restrito a qual rótulo foi mantido em pares conflitantes |
| **Achado próprio** | Naquele resíduo os arquivos distribuídos **não seguem literalmente o pseudocódigo publicado**, que manda remover ambos os membros do par |

### Kolisch, R.; Sprecher, A.; Drexl, A. (1995) — **REPRODUZIDO**

*Characterization and generation of a general class of resource-constrained
project scheduling problems.* Management Science. **⚠ Completar volume, páginas.**

| | |
|---|---|
| **Sustenta** | Definições de NC, RF e RS. Recalculadas a partir dos arquivos, recuperam o fatorial 3 × 4 × 4 = 48 células com 10 instâncias — valida leitura e formulações simultaneamente |

### Boehm, B.; Basili, V. (2001) — **LIDO**

*Software Defect Reduction Top 10 List.* IEEE Computer.
**⚠ Completar volume, número, páginas.**

| | |
|---|---|
| **Sustenta** | Faixa de esforço de retrabalho. **É a única referência na mesma unidade da saída do modelo** |

---

## 6. Base conceitual herdada do TCC I

| fonte | estado | papel | ação |
|---|---|---|---|
| **Kim, D. H. (1994)** | PARCIAL, PDF no projeto | Arquétipos de Soluções Sintomáticas e Erosão de Metas — base dos dois laços causais | completar referência |
| **Sterman, J. (2000)** | NÃO OBTIDO | Dinâmica de Sistemas, estoques e fluxos | canônica, obter |
| **Rodrigues, A. (2000)** | NÃO OBTIDO | Retrabalho oculto em projetos | obter ou remover |
| **Simon, H. (1957)** | NÃO OBTIDO | *Satisficing* | canônica, obter |
| **Liu; Triantis; Sarangi (2011)** | NÃO OBTIDO | Lógica difusa em DS | obter; o TCC I já a cita |
| **Macal & North (2010)** | NÃO OBTIDO | Fundamentos de ABM | obter |

> Estas seis vêm da bibliografia do TCC I. Se já constam lá com referência
> completa, **copie de lá** — é o caminho mais rápido e mantém consistência
> entre as duas monografias.

---

## 7. Precedente direto

### Pessoa, R. W. S. et al. — **LIDO**, mas **preprint**

*A Hybrid Agent-Based and System Dynamics Framework for Modelling Project
Execution and Technology Maturity in Early-Stage R&D.*
**Sem volume, páginas ou DOI. O rodapé diz "Preprint submitted to Elsevier".**

| | |
|---|---|
| **Sustenta** | O precedente mais próximo. Agentes homogêneos por hipótese declarada; pressão atua sobre produtividade; retrabalho com probabilidade fixa; validação por julgamento de especialista; admite que a parametrização pode superestimar a produtividade |
| **Usada em** | Capítulo de posicionamento — o delta está no parecer 43 |
| **⚠ Ação** | Confirmar estado de publicação e ano. Se continuar preprint, **declarar como tal na citação** |

---

## 8. Metodologia de calibração

| fonte | estado | papel |
|---|---|---|
| **Raue et al.** | NÃO OBTIDO | identificabilidade estrutural × prática |
| **Grimm et al. (2005)** | NÃO OBTIDO | modelagem orientada a padrões |
| **Pukelsheim (1994)** | PARCIAL | regra três sigma — em `research/SOURCES.md`, marcada PARTIALLY SUPPORTED |
| **De Baets (2009)**, **Love (2000)** | não avaliadas nesta rodada | ver `research/SOURCES.md` |

---

## 9. O que fazer, em ordem

**Bloqueante — não pode ir para a monografia como está:**

1. **Obter ou remover:** Ball, White, Lee, Payne/Bettman/Luce, Reichelt & Lyneis,
   Edmondson, Rodrigues. Sete fontes citadas e nunca abertas.
2. **Copiar do TCC I:** Kim, Sterman, Simon, Liu/Triantis/Sarangi, Macal & North.
   Cinco, e a referência completa já existe lá.
3. **Completar dados bibliográficos:** Stewart & Melchers, Stewart, Crowder,
   Shepperd, Kolisch, Boehm & Basili — volume, número, páginas.
4. **Rieskamp:** abrir o texto integral ou citar só o construto, nunca os números.
5. **Pessoa et al.:** confirmar publicação; se preprint, declarar.

**Depois disso:**

6. Apagar `projeto/04_FONTES.md` e `research/SOURCES.md`, ou marcá-los como
   histórico no topo. Dois catálogos parciais é pior que nenhum.

---

## 10. Nota sobre este documento

O que está marcado **LIDO** foi conferido na página durante este trabalho e os
trechos citados estão reproduzidos nos pareceres 35, 36 e 41. O que está
**PARCIAL** teve metadados e resumo conferidos na origem, e o texto integral
não foi aberto. O que está **NÃO OBTIDO** nunca foi aberto por ninguém neste
trabalho — essas entradas existem para serem resolvidas, não para serem citadas.

Nenhum dado bibliográfico foi preenchido por inferência. Onde aparece
**⚠ Completar**, é porque o dado não foi verificado, e escrever um número
plausível ali seria exatamente o risco que este documento existe para eliminar.
