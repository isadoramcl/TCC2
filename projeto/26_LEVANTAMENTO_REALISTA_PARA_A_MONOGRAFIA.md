# Parecer 26 — Levantamento realista: o que está pronto, o que falta, e o que fazer com o que não vai ficar pronto

**Data:** 17/09/2026 · **Revisor:** Claude
**Escopo:** estado do MVP e do que a monografia precisa ter

---

## 1. O MVP está fechado?

**Como software, sim.** Como argumento científico, não — e a diferença é o que importa agora.

| Dimensão | Estado | Evidência |
|---|---|---|
| Implementação (C4 tempo + qualidade, C1 fila, Crowder, reset C6, horizonte, políticas Porta 2) | **Pronto** | `simulador_mvp.py`, commit `ddc7c94` |
| Controle de identidade bit a bit com o legado | **Pronto, forte** | compara todos os campos por `float.hex()`, o estado do RNG, e impede delegação ao laço legado |
| Suíte de testes | **Pronto** | 40 testes, com controles negativos no verificador |
| Invariantes em execução | **Pronto** | conservação de retrabalho, precedência, recursos; zero violações em 22.208 execuções |
| Congelamento e rastreabilidade | **Pronto** | resultados pré-correção preservados, 72 hashes íntegros |
| Legado intacto | **Pronto** | `simulador.py` e `main` não foram alterados destrutivamente |
| **Conclusões que o modelo sustenta** | **Aberto — é o gargalo** | parecer 23 |

Fechar o MVP não era o objetivo final: era pré-condição para produzir números
confiáveis. Isso foi alcançado. O que não foi alcançado é saber o que os números
significam.

## 2. Problemas já encontrados — situação de cada um

| # | Achado | Estado | Consequência se ficar assim |
|---|---|---|---|
| A-01 | `F_ancora × f_retrabalho` não separáveis pelos agregados | **aberto** | limitação declarada; não impede a defesa |
| A-02 | NROY esvazia em K=64; I(verdadeiro) → 3,594 | **aberto** | calibração inviável — vira limitação declarada |
| A-03 | Metade de qualidade da Porta 1 ausente | **resolvido** | — |
| A-04 | Teste do gêmeo idêntico inválido (RNG re-semeado) | **resolvido e retratado** | — |
| A-05 / A-13 | Porta de confiança degenerada; contraste majoritariamente premissa | **aberto — CRÍTICO** | **a conclusão de governança não se defende sem isto** |
| A-06 | `atraso_relativo` domina a implausibilidade sem informar | **resolvido por exclusão** (não admitido em z) | — |
| A-07 | Bloqueio contado como recusa | **resolvido** | — |
| A-08 | Sem controle de identidade bit a bit | **resolvido** | — |
| A-11 | Inversão de `E_total` era artefato da convenção de TL | **resolvido — achado retirado** | — |
| A-12 | Escala da fórmula de competência no braço legado | **declarado, preservado de propósito** | nota de leitura |
| D-03 | `f_atalho` sem fonte | **aberto** | parâmetro de sensibilidade declarado — aceitável |
| D-13 | Precedente ABM+SD com ciclos de retrabalho não citado | **aberto — ALTO RISCO** | pergunta de banca sem resposta |
| G-01 | Retrabalho: unidade bate, domínio não | **aberto** | limitação declarada |
| G-02 | Ponte de agregação do HEART | **aberto** | limitação declarada |
| G-03 | P(heurístico) sem validação externa | **aberto** | limitação declarada |
| D-06 | Gradiente sobre linhas de código não recalculado | **aberto** | gradiente publicado está em eixo contestado |

## 3. O que a monografia precisa ter, e o que já existe

| Componente | Temos? | Observação |
|---|---|---|
| Modelo documentado e reproduzível | **Sim, forte** | especificação, parâmetros declarados, hashes, testes |
| Capítulo de verificação e validação | **Sim, muito forte** | é o ponto alto do trabalho — auditoria adversarial documentada, achados retratados, controles negativos |
| Limitações declaradas | **Sim, forte** | 22 é um contrato observacional sério |
| Resultados que sustentam as afirmações | **Parcial — é o que falta** | parecer 23 cortou a base da conclusão de governança |
| Posicionamento contra o estado da arte | **Não** | D-13 |
| Calibração | **Não, e não vai haver** | precisa virar contribuição declarada, não lacuna |
| Pacote de reprodutibilidade | **Sim** | testes, congelamento, manifestos |

**Leitura:** o software não é o risco. O risco é o capítulo de resultados dizer uma
coisa que os números não sustentam, e o capítulo de introdução não dizer o que este
trabalho faz que o precedente já não fazia.

## 4. O que falta, por que falta, e a saída realista

Ordenado por risco × custo, não por ordem lógica.

### P1 — Decomposição premissa × mecanismo (T1/T2/T3 do parecer 23)

- **Por que falta:** ninguém tinha olhado os contadores por arranjo até ontem.
- **Por que é crítico:** `p_reporte` responde por 93,4% do contraste de `taxa_omissao`
  e 87,4% do de dívida latente. Sem a decomposição, o capítulo de resultados afirma
  como achado o que é premissa.
- **Saída:** T2 (três células: só τ difere / só reporte-detecção difere / ambos) é o
  mínimo. T1 e T3 são desejáveis.
- **Custo:** baixo — a maquinaria existe (`tau_portao`, `tau_rede`).
- **Se não der tempo:** T2 sozinho basta. Sem T2, a conclusão de governança tem de
  sair do texto.

### P2 — Reescrever a conclusão de governança como mecanismo de transmissão

- **Por que falta:** decorre de P1.
- **Saída:** trocar "o arranjo adaptativo tem melhor desempenho" por "dado um
  diferencial declarado de premissas de reporte e confiança, a degradação cognitiva,
  as portas de decisão e a fila de retrabalho transmitem esse diferencial com
  amplificação de 1,50× em prazo, 1,14× na taxa de falha efetiva e 1,22× na seleção
  da Porta 1". Menor, verdadeiro, e é pergunta de mecanismo — que é o que o
  simulador investiga.
- **Custo:** escrita, não código. Horas.

### P3 — Citar o precedente e escrever o delta (D-13)

- **Por que falta:** foi anotado em `04_FONTES` como pendência e nunca executado.
- **Por que é alto risco:** existe trabalho publicado com arcabouço ABM+SD para
  execução de projetos com ciclos de retrabalho. O PDF está nos arquivos do Projeto.
  Um TCC que constrói exatamente isso sem citar quem já fez recebe a pergunta na
  defesa, e ela não tem resposta improvisável.
- **Saída:** ler, citar, e escrever meia página dizendo o que este trabalho acrescenta
  — degradação cognitiva por porta de decisão, arranjos contrastados, ancoragem
  externa tentada e documentada — e o que herda.
- **Custo:** uma leitura e meia página. **Melhor relação risco/esforço de toda a lista.**

### P4 — Transformar a ausência de calibração em contribuição declarada

- **Por que falta:** o NROY esvazia (A-02), o vetor z não está habilitado (22), e
  nenhuma das cinco grandezas candidatas passou no contrato de unidade e fronteira.
- **Por que isso é bom, se apresentado certo:** um trabalho que constrói um
  simulador, submete-o a auditoria adversarial, e **demonstra com precisão por que
  ele ainda não é calibrável, nomeando cada obstrução**, é contribuição metodológica
  legítima. O parecer 22 já é esse artefato.
- **Saída:** um capítulo curto — "por que este modelo não é calibrável hoje" — com a
  tabela de admissibilidade do 22, as três obstruções (G-01, G-02, G-03) e o critério
  que uma fonte teria de satisfazer. Mais a rota alternativa de adequação: modelagem
  orientada a padrões (Grimm et al. 2005, já em `04_FONTES`), com os padrões nomeados
  e o critério de sucesso escrito.
- **Custo:** escrita, com material já existente. **Não tente calibrar. Não vai dar.**

### P5 — Recalcular o gradiente sobre linhas de código (D-06)

- **Por que falta:** adiado para depois do MVP; o MVP acabou.
- **Por que importa:** o gradiente publicado está em eixo de complexidade ciclomática,
  que não sobrevive ao controle de tamanho (razão de chances 0,944, p = 0,166,
  negativa). O eixo de linhas de código dá gradiente mais acentuado (até 5,37 contra
  2,99) e mais preciso (z = 34,3 contra 25,6).
- **Saída:** recomputar e republicar. Não é conferência — os números mudam.
- **Custo:** baixo, script existe.
- **Se não der tempo:** declarar que o gradiente está em eixo confundido por tamanho
  e que o recálculo é trabalho futuro. É honesto, mas enfraquece a camada NASA.

### P6 — Consolidar fontes e histórico

- **Saída:** migrar para `04_FONTES.md` as fontes novas que estão só no Word 18, no
  formato dele (com a linha do que a fonte **não** sustenta). Verificar Edmondson
  (1999) antes de qualquer uso.
- **Custo:** baixo, mas é o que protege contra citação sem fonte.

### Não fazer — declarar como limitação

- **G-01 / G-02 / G-03.** Cada um exige dado externo que não existe em forma
  compatível. Tentar fechá-los agora consome o prazo e não fecha.
- **Novas ondas de History Matching.** Sem z habilitado, é calibrar contra o próprio
  modelo.
- **`f_atalho`.** Fica como parâmetro de sensibilidade declarado, varrido. Está certo assim.
- **Corrigir a escala do braço legado (A-12).** A preservação é deliberada e sustenta
  o controle de identidade. Só declarar na leitura da tabela incremental.

## 5. Sequência sugerida

1. **T2** (decomposição premissa × mecanismo) — dispara agora, é o único bloqueio real.
2. **Enquanto roda:** ler o precedente e escrever o delta (P3). Não depende de nada.
3. **Com T2 na mão:** reescrever a conclusão de governança (P2).
4. **P5** se houver folga; **P4** e **P6** são escrita e podem ir em paralelo.

## 6. O balanço honesto

O trabalho está em melhor forma do que a lista de achados sugere. O que existe hoje
— um simulador verificado, com controle de identidade bit a bit, invariantes em
execução, resultados congelados, e um histórico de auditoria em que quatro afirmações
foram retiradas porque não sobreviveram ao teste — é mais rigor do que a maioria dos
TCCs de simulação apresenta.

O que não existe é ancoragem empírica, e ela não vai existir no prazo. A decisão
estratégica é aceitar isso de frente: a contribuição não é "calibramos um modelo de
equipes de engenharia", é **"construímos um simulador, submetemos a auditoria
adversarial, e mapeamos exatamente o que impede sua calibração"**. A segunda é
verdadeira, defensável e sustentada por documentação que já existe. A primeira não é.

O maior risco isolado neste momento não é técnico: é o capítulo de resultados
afirmar governança sem a decomposição do parecer 23, e a introdução não posicionar o
trabalho contra o precedente. Os dois são baratos e os dois são resolvíveis esta semana.
