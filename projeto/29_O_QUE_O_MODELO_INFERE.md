# Parecer 29 — O que o modelo já infere: certo, errado e faltando

**Data:** 17/09/2026 · **Revisor:** Claude
**Base:** `outputs/diagnosticos/correcao_estrutural_20260916/correcao/nominal_corrigido.csv`
(16 instâncias × 12 sementes, 60 tarefas por instância), tabelas T1/T2 do parecer 24,
e `config/parametros.yaml`. Todos os números abaixo foram recomputados.

---

## 1. Achado novo · A-14 · CRÍTICO — A Porta 1 tem três saídas e uma nunca executa

`p1_fuga = 0,000000` e `n_adiamentos = 0,000000` **nos dois arranjos**, em todas as
16 instâncias × 12 sementes.

A condição é `if heu and omega > limite_aversao_perda`. No YAML:

- `omega = 0,50` — `premissa`, declarada IGUAL nos dois cenários como controle experimental;
- `limite_aversao_perda = 0,60` — `aberto`.

`0,50 > 0,60` é **falso**. A rota de fuga (adiamento por aversão à perda do gestor) é
código morto no nominal.

**Pior que o portão de confiança.** Ali, pelo menos, a comparação envolvia uma variável
de estado que poderia mudar. Aqui os dois lados são **constantes lidas uma vez**. Logo
`omega > limite` é uma constante de tempo de compilação, e o comportamento é
estritamente binário:

- `limite ≥ 0,50` → **nenhuma** decisão heurística vira fuga (regime atual);
- `limite < 0,50` → **toda** decisão heurística vira fuga, e nenhuma tarefa é jamais
  executada pela Porta 1.

**Não existe regime intermediário.** O parâmetro declara `varredura: [0,40; 0,60; 0,80]`,
mas `limite_aversao_perda` **não está no desenho de robustez executado** (que varre
`F_ancora`, `f_retrabalho`, `mu_minimo`, políticas de Porta 2, leis de confiança e
fatores de omissão). Então essa varredura nunca rodou.

**Consequência:** um mecanismo herdado do TCC I — o gestor que adia sob aversão à perda —
está no código, consome uma linha do registro de decisão, e **nunca foi exercitado**.
A monografia não pode descrevê-lo como parte do comportamento do modelo.

**Saída, e é barata:** tornar a fuga dependente do estado, não de duas constantes. A
forma natural, coerente com o resto do modelo, é comparar a aversão à perda com a
**magnitude da sobrecarga**, por exemplo `omega·(E − τ_sat) > limite` ou `omega·q > limite`
com `q = max(0, 2·p_heu − 1)`. Aí a fuga passa a acontecer nas situações extremas, que
é o que o TCC I descrevia, e ganha regime intermediário. Alternativamente: declarar o
mecanismo como não implementado e removê-lo do texto.

---

## 2. O que o modelo infere hoje — e está correto

Números: média por execução. Diferenças com IC95 vêm do T2 (parecer 24).

| # | Inferência | Evidência | Estado |
|---|---|---|---|
| I-1 | O arranjo de confiança reduz o prazo **independentemente** da premissa de reporte | ambos − reporte = −0,4326, IC95 [−0,491; −0,374] | **sólida** |
| I-2 | Reduz a taxa de falha **efetiva**, igualado o reporte | −0,0345, IC95 [−0,049; −0,021] | **sólida** |
| I-3 | Reduz o uso da rota heurística | −0,1190, IC95 [−0,139; −0,099] | **sólida** |
| I-4 | Assistência tem custo: em limiar alto com reporte baixo, abrir o portão **aumenta** o atraso | +0,2948, IC95 [0,0295; 0,5602] | **sólida, e não óbvia** |
| I-5 | O retrabalho por falha é menor sob menor sobrecarga | 4,188 contra 4,539 por falha (−7,7%), via `f_corrup·(E − τ_sat)` | **coerente com o mecanismo** |
| I-6 | O pico de dívida oculta é 4,05× maior no arranjo centralizado | `S_UR_maximo` 8,67 contra 35,15 | descritiva |
| I-7 | ~24% das tarefas estão acima do agente mais competente e são estruturalmente irresolvíveis por assistência | 14,54 de 60 tarefas; `hiato_sem_colega_capaz` ≈ 10,3 nos dois arranjos | **estrutural, deve ser declarada** |
| I-8 | O arranjo adaptativo **não** reduz a intensidade de retrabalho — reduz o trabalho total | TR/TW = 0,185 (adapt.) contra 0,175 (centr.) | **importante e contraintuitiva** |

**I-8 merece atenção.** Medido contra o trabalho efetivamente realizado, o arranjo
adaptativo retrabalha um pouco **mais**, não menos. O ganho vem de fazer menos trabalho
total (TW 433 contra 565) e esperar menos (TU 49,5 contra 140,8). A leitura correta não
é "o arranjo adaptativo produz menos defeito por unidade de trabalho" — é "produz menos
trabalho e menos espera, para a mesma entrega".

## 3. O que está vindo incorreto, ou degenerado

| # | Problema | Evidência | Gravidade |
|---|---|---|---|
| E-1 | **Rota de fuga da Porta 1 nunca executa** | `p1_fuga = 0` nos dois arranjos; `0,50 > 0,60` constante | **crítica** |
| E-2 | **Portão de confiança degenerado** nos dois sentidos | `N_req = 0` centralizada; `hiato_colega_capaz_sem_confianca` = 130,6 de 140,8 | **crítica** (A-13) |
| E-3 | **A confiança satura**: é catraca de mão única | 0,25 → 0,25 (congelada) e 0,80 → 0,9364 (perto do teto 1) | **alta** — ver §4 |
| E-4 | `taxa_omissao`, `divida_latente` e `S_PV` são dominados pela premissa de reporte | 97,5%, 95,5%; `S_PV/E_plano` ≈ 1 − `taxa_omissao` (0,907 e 0,664) | **alta** — não são desfechos independentes |
| E-5 | `retrabalho_sobre_esforco_realizado` contaminado por TL | TL = 0 num braço e 102,9 no outro; denominadores não comparáveis | média — já excluído de z |
| E-6 | `S_UR_final` é estruturalmente nulo | 1e-15 e 1e-17; o laço só termina com dívida vazia | baixa — já conhecido; usar o pico |
| E-7 | Sem acúmulo permanente de competência | `competencia_maxima_final` = `competencia_maxima_inicial` | baixa — é fiel a Crowder, mas deve ser declarado |

### §4 — Por que E-3 importa mais do que parece

A lei de confiança é `τ ← τ(1+ΔC)` no sucesso e `τ − 0,01` no insucesso. No braço
adaptativo houve 102,9 sucessos contra 39,1 insucessos por execução. Com ΔC ≈ 0,21, o
crescimento é multiplicativo e o decremento é aditivo e pequeno. Resultado: τ sobe de
0,80 para 0,9364, perto do teto 1,0.

**Isso é uma catraca, não uma dinâmica.** Num modelo de Dinâmica de Sistemas, um estoque
que só sobe até saturar não tem laço de balanceamento — não há realimentação negativa
capaz de derrubá-lo. O "estoque de confiança" do modelo, portanto, **não produz
comportamento dinâmico interessante**: ele decide no primeiro instante (pelo valor
inicial) e depois satura.

Isso está fiel à Eq. (4) de Crowder, que é assimétrica por construção. Mas precisa ser
dito no texto: **a confiança, neste modelo, é praticamente uma condição inicial, não
uma variável de estado com dinâmica própria.** É uma limitação estrutural herdada da
fonte, e declará-la é mais forte do que deixar a banca descobrir.

## 4. O que está faltando

| # | Falta | Por quê |
|---|---|---|
| F-1 | Separar portão de canal difuso (T4) | `tau_inicial` alimenta os dois; o efeito sobre falha efetiva pode vir do canal difuso, não da assistência |
| F-2 | Exercitar a rota de fuga (E-1) | mecanismo do TCC I nunca testado |
| F-3 | Mapeamento explícito contra as proposições do TCC I | **preciso da lista de proposições do TCC I para fazer isto** — não está nos arquivos do repositório |
| F-4 | Ancoragem externa de qualquer magnitude | zero de 39 parâmetros ancorados |
| F-5 | Sensibilidade dos estoques | `S_UR_maximo` e `S_PV` nunca tiveram varredura própria |

**Sobre F-3:** você perguntou o que o TCC I afirmava e o que o modelo hoje infere. Para
responder afirmação por afirmação eu preciso da lista de proposições do TCC I. Ela não
está no repositório nem nos arquivos do Projeto. Se você me mandar a seção de hipóteses
ou proposições da monografia do TCC I, eu monto a tabela de correspondência — cada
proposição contra o que o modelo hoje sustenta, refuta ou não testa. **Esse é
provavelmente o capítulo de resultados mais forte que o trabalho pode ter**, porque
mostra um modelo conceitual sendo confrontado com sua própria implementação.

## 5. Estado: pronto, pronto-com-erro, pendente

### Pronto

- Implementação do MVP (C4 tempo e qualidade, C1 fila, Crowder, reset C6, horizonte, políticas de Porta 2)
- Controle de identidade bit a bit com o legado, incluindo estado do RNG e guarda anti-delegação
- 44 testes, com controles negativos no verificador
- Invariantes em execução: conservação de retrabalho, precedência, recursos — zero violações
- Congelamento e rastreabilidade: 72 hashes, resultados pré-correção preservados
- T1, T2, T3 executados com protocolo registrado antes
- Contrato observacional (parecer 22)
- `taxa_falha_efetiva` como campo de primeira classe

### Pronto, mas com erro ou degenerescência

| Item | Situação |
|---|---|
| Porta 1 — rota de fuga | implementada, **nunca executa** (E-1) |
| Porta 2 — portão de confiança | implementado, **degenerado nos dois sentidos** (E-2) |
| Lei de confiança | fiel à fonte, mas **satura**; sem laço de balanceamento (E-3) |
| Braço legado da fórmula de competência | escala errada, **preservada de propósito** para o controle de identidade (A-12) |
| `retrabalho_sobre_esforco_realizado` | produzido e usado em figuras, mas contaminado por TL (E-5) |
| `limite_aversao_perda` | declara varredura, **não está no desenho de robustez executado** |

### Pendente

- T4 (separação portão × canal difuso)
- Correção ou remoção da rota de fuga
- Mapeamento contra as proposições do TCC I (depende de F-3)
- Recálculo do gradiente sobre linhas de código (D-06)
- Citação do precedente ABM+SD e escrita do delta (D-13)
- Consolidação de fontes em `04_FONTES.md`; verificar Edmondson (1999)

---

## 6. Os seis itens que eu havia posto de fora — reavaliados com 10 dias livres

O ponto de controle exige pouco (estado atual, cronograma, assinatura do orientador).
Então os 10 dias estão livres. Reavaliação honesta de cada um:

| Item | Dá para resolver até 27/09? | Por quê |
|---|---|---|
| **G-01** — comparador de retrabalho em esforço fora de software | **Não, mas dá para melhorar muito** | Não existe a cifra. **Mas** Rodrigues (2000, SYDPIM) e relatórios do CII com homem-hora nunca foram consultados com essa pergunta. Vale 1 dia de busca: se achar, fecha; se não achar, a busca documentada **é** a evidência de insuficiência, e isso vale no texto. |
| **G-02** — ponte de agregação do HEART | **Não** | Exige uma regra de composição com `k` (número de passos elementares por atividade) vindo de decomposição documentada. Não existe decomposição de tarefa no PSPLIB. Fechar isso é um trabalho em si. **Obter a tabela primária do HEART, porém, é obrigatório** — hoje ela está NÃO VERIFICADA e está sendo citada. Isso sim, em 1 dia. |
| **G-03** — validação de P(heurístico) | **Talvez, parcialmente** | Payne, Bettman & Johnson nunca foram consultados. Se reportarem proporções de seleção de estratégia sob pressão, fecha; se só reportarem acurácia, não. Vale 1 dia. É o de maior chance dos três. |
| **Calibração / novas ondas de HM** | **Não, e não se deve tentar** | O vetor z não está habilitado. Calibrar sem z é calibrar contra o próprio modelo. |
| **Reposicionamento próximo ao limiar** | **Sim, tecnicamente** | Mas com a ressalva de potência do parecer 27: margens de +0,01 e +0,05 dão contraste pequeno demais para 4 instâncias. Se for feito, incluir margens largas. **Prioridade abaixo de E-1 e T4.** |
| **D-06** — gradiente sobre linhas de código | **Sim** | Script existe, é recomputar e republicar. Meio dia. **Deveria entrar**, porque o gradiente publicado está num eixo que não sobrevive ao controle de tamanho. |

### O que eu faria com os 10 dias, em ordem

1. **E-1** — corrigir ou remover a rota de fuga. É um defeito estrutural num mecanismo
   central e é barato. (Codex)
2. **T4** — separar portão de canal difuso. Fecha a leitura do mecanismo principal. (Codex)
3. **D-06** — recalcular o gradiente sobre linhas de código. (Codex)
4. **Três buscas de fonte, um dia cada:** tabela primária do HEART; Rodrigues/CII em
   homem-hora; Payne, Bettman & Johnson. Mesmo as que falharem produzem a evidência
   documentada de insuficiência, que é material de capítulo. (Isadora)
5. **D-13** — ler o precedente e escrever o delta. (Isadora)
6. **Assinatura do orientador** — depende de terceiro, então começar cedo.

Nada disso é experimento novo depois de 27/09. Tudo cabe.
