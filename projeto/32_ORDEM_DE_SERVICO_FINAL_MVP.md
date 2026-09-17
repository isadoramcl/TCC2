# Ordem de serviço 32 — Último lote do MVP antes do congelamento

**Data:** 17/09/2026 · **Origem:** pareceres 23 a 31 e a bancada de fatores humanos
**Congelamento da simulação: 27/09/2026.** Depois desta data, nenhum experimento novo.
Este é o último lote.

---

## Regra que vale para todos os itens

O **nominal histórico não é substituído**. Tudo entra como alternativa preservada e
varrida, com protocolo registrado antes de executar, como já foi feito em T1/T2/T3.
Qualquer item que altere dinâmica precisa de controle ANTES/DEPOIS e não pode quebrar
o teste de identidade bit a bit com as opções neutras.

---

## Prioridade 1 — Defeito estrutural

### P1.1 · Rota de fuga da Porta 1 nunca executa (achado A-14, parecer 29)

`p1_fuga = 0,000000` e `n_adiamentos = 0,000000` nos dois arranjos, em todas as 16
instâncias × 12 sementes. A condição é `omega > limite_aversao_perda`, com `omega = 0,50`
(premissa, igual nos dois cenários) e `limite_aversao_perda = 0,60`. Os dois lados são
**constantes lidas uma vez**, então a comparação é uma constante: ou nenhuma decisão
heurística vira fuga, ou **todas** viram. Não existe regime intermediário. E
`limite_aversao_perda` declara `varredura: [0,40; 0,60; 0,80]` no YAML mas **não está no
desenho de robustez executado**, então essa varredura nunca rodou.

**Não** corrigir promovendo a fuga ao nominal e rerrodando tudo — isso desestabiliza o
capítulo de resultados a 10 dias do congelamento.

**Fazer:** implementar como **alternativa preservada**, com a fuga dependente de estado em
vez de duas constantes. Forma coerente com o resto do modelo, a ser declarada como `[DEC]`:
`omega·(E − τ_sat) > limite` ou `omega·q > limite`, com `q = max(0, 2·p_heu − 1)` — assim a
fuga ocorre nas situações de sobrecarga, que é o que o modelo conceitual descrevia, e ganha
regime intermediário. Reportar os cinco indicadores no nominal e na alternativa, com IC95.

Incluir `limite_aversao_perda` no desenho de robustez, ou declarar explicitamente que ficou
de fora e por quê.

**Se não der tempo de implementar:** declarar no texto que o mecanismo está no código mas
nunca é exercitado na configuração nominal, e removê-lo da descrição do comportamento do
modelo. Isso é aceitável; o que não é aceitável é descrevê-lo como parte do comportamento.

---

## Prioridade 2 — Fechar a leitura do mecanismo

### P2.1 · T4 — separar portão de canal difuso (parecer 27, §7)

O bloco `confianca` do T2 move `tau_inicial` **e** `tau_min` juntos, e `tau_inicial`
alimenta dois caminhos: o portão de assistência e a entrada difusa
(`desconfianca = 1 − confianca` → `mu_rede`). Então o efeito significativo sobre
`taxa_falha_efetiva` pode vir da assistência **ou** do canal difuso, e o T2 não separa.

Importa porque `p0` depende de `mu_cog`, não de `mu_rede`. Se o efeito passar pelo canal
difuso, a leitura correta não é "assistência reduz defeito", e sim "confiança reduz
duração, e duração reduz degradação cognitiva".

**Fazer:** quatro células — `tau_portao` centralizado/adaptativo × `tau_rede`
centralizado/adaptativo — com `p_reporte` e `p_deteccao` igualados. Os dois overrides já
existem. Reportar `atraso_relativo`, `taxa_omissao`, `divida_latente_sobre_plano`,
`taxa_falha_efetiva` e `fracao_porta1`, com IC95.

### P2.2 · Cenário com efeito de P sobre o erro igual a zero

Vem da bancada de fatores humanos: **nenhuma base de campo com efeito fixo sustentou
"mais pressão → mais erro"**. O tênis deu o sinal oposto (−0,59 p.p. em erro não forçado
sob break point); NBA e Go deram nulo. A ressalva correta é que "pressão" cobre construtos
diferentes — importância do que está em jogo produz cautela, custo de oportunidade do tempo
produz aceleração — mas a objeção vai aparecer na defesa.

**Fazer:** rodar o nominal num cenário em que o efeito de `P` sobre a probabilidade de erro
é anulado, mantendo tudo o mais. Verificar se as conclusões centralizado × adaptativo
sobrevivem. Se sobreviverem, o capítulo fica muito mais forte; se não sobreviverem, é
melhor saber agora. Varrer também `s_transicao` e `tau_sat` em torno do nominal.

---

## Prioridade 3 — Readout e diagnóstico da calibração

Nenhum destes altera dinâmica.

### P3.1 · Novo readout de retrabalho

Acrescentar `retrabalho_sobre_esforco_total = TR / (E_plano + TR)` como campo derivado,
sem alterar RNG, decisões ou estados — mesmo tratamento dado a `taxa_falha_efetiva` no T3.
Propagar aos runners e aos resumos. Controle ANTES/DEPOIS obrigatório.

Motivo: põe o indicador na mesma escala de Reichelt & Lyneis (1999), que reportam retrabalho
sobre **horas totais**. Os valores atuais convertem para 19,0% (adaptativa) e 22,4%
(centralizada).

### P3.2 · Teste de cobertura do History Matching

O gêmeo sintético atual usa **uma única** pseudo-observação, o que não mede taxa de falsa
exclusão. Uma realização com `I = 3,594` não demonstra que o instrumento está desregulado,
porque o próprio `z` sintético é aleatório mesmo quando gerado no vetor verdadeiro.

**Fazer:** redesenhar como cobertura repetida. B = 500 (1.000 se couber). Em cada réplica:
gerar `z_b` novo no vetor verdadeiro pelo desenho declarado; reestimar a resposta do
verdadeiro com sementes independentes; calcular os quatro `I_j` e `I_max,b`; registrar se
`I_max,b > 3`.

Reportar a **taxa empírica de falsa exclusão** e o **percentil 95 de `I_max`** sob o vetor
verdadeiro.

**Proibido:** ajustar `V_mod` até o gabarito passar; escolher pseudo-observação favorável.

Se o percentil 95 exceder 3, reportá-lo como corte conjunto empiricamente justificado para
um desenho de **quatro** observáveis, registrando que o corte 3 vem de uma regra marginal e
que o máximo de quatro `I_j` não tem o mesmo erro de um único.

### P3.3 · Declarar o estimando do `V_obs` sintético

Hoje `V_obs` é `d[o].var(ddof=1)/n` sobre execuções do **próprio simulador**. Isso só é
válido se estiver declarado qual experimento o `z` sintético imita.

**Fazer:** escrever o estimando explicitamente (por exemplo: média esperada do observável
nas instâncias fixas, sobre a aleatoriedade dos agentes), e fazer geração e estimação
respeitarem a mesma unidade amostral. Renomear o gêmeo idêntico para **verificação interna
do procedimento** — ele não informa o `V_obs` externo, e o texto não pode sugerir que
informa.

---

## Prioridade 4 — Pendências de análise e instrumentação

### P4.1 · Recalcular o gradiente sobre linhas de código (D-06)

O gradiente publicado está no eixo de complexidade ciclomática, que **não sobrevive ao
controle de tamanho**: razão de chances 0,944, p = 0,166, negativa. O eixo de linhas de
código dá gradiente mais acentuado (até 5,37 contra 2,99) e mais preciso (z = 34,3 contra
25,6). O script existe. **Não é conferência — os números mudam.**

### P4.2 · Instrumentar a saturação da confiança

`confianca_media_final` é 0,9364 no arranjo adaptativo (partindo de 0,80, teto 1,0) e
0,2500 no centralizado (congelada, porque nunca há evento). A lei de Crowder cresce
multiplicativamente no sucesso e decresce 0,01 no insucesso, com 102,9 sucessos contra
39,1 insucessos por execução — é catraca de mão única, sem laço de balanceamento.

**Fazer:** exportar a trajetória de confiança e o **período em que a média cruza 0,95**,
para que a monografia possa declarar com número que a confiança é, na prática, condição
inicial e não variável de estado com dinâmica própria. É limitação estrutural herdada da
fonte; declará-la é mais forte que deixar a banca descobrir.

### P4.3 · Testar a faixa de `mu_minimo` contra referência externa

Reichelt & Lyneis (1999) reportam degradação média de qualidade de **0,95** por pressão de
cronograma e **0,97** por fadiga de hora extra. São multiplicadores de degradação — a mesma
grandeza de `mu_cog` e `mu_rede`.

**Fazer:** reportar a distribuição de `mu_cog` e `mu_rede` observada no nominal e verificar
se é compatível com médias dessa ordem. Se for, é um segundo parâmetro ganhando
interpretação externa. **Ressalva obrigatória no texto:** são saídas de modelo de Dinâmica
de Sistemas calibrado, da mesma linhagem deste trabalho — consistência com a literatura de
modelagem, não medição independente.

---

## Prioridade 5 — Arrumação do repositório

- Acrescentar `Claude outputs/` ao `.gitignore`. Hoje há cópias duplicadas de
  `18_HISTORICO_DECISOES_E_FONTES.docx`, `20_AUDITORIA_CORRECAO_1fd22ff.md` e
  `BRIEFING_TRES_LACUNAS.md` na raiz, fora de `projeto/`, e não estão ignoradas. O lugar
  canônico é `projeto/`.
- Os pareceres 23 e 25 a 31 do revisor estão em `projeto/` e precisam ser commitados.
- Conferir se há dois arquivos numerados 07 (`07_AUTONOMIA.md` versionado e
  `07_BRIEFING_ORIENTADOR.md` sem versionar). Resolver a numeração antes do pacote final.

---

## Correções documentais que vêm da bancada de fatores humanos

Se a bancada entrar como apêndice exploratório — e a recomendação é que entre:

- **`taxa_reversao_pct` do T3 (Go) está mal rotulada.** O código calcula
  `100 * base.reverted.mean()`, que é a proporção de commits **que foram revertidos**
  (alvos), não a proporção de commits **que são reversões**. O relatório diz "1,06% dos
  commits" e o leitor calcula 579/67.313 = 0,86%, ou 574/45.859 = 1,25% no recorte 2015+.
  Nenhum bate. Renomear e publicar o tamanho de `base`.
- **A tabela de tênis mistura denominadores.** No CSV, `double_fault` é sobre todos os
  pontos; na tabela do relatório, o efeito de −1,06 p.p. é condicionado ao 2º saque. Os dois
  estão certos, mas quem comparar acha erro de fator 7. Rotular a coluna e declarar o
  condicionamento.

---

## Ordem sugerida de execução

1. P3.1 e P3.3 (baratos, não alteram dinâmica) — abrem caminho para P3.2.
2. P1.1 (alternativa preservada) e P2.1 (T4) — podem rodar no mesmo lote.
3. P2.2 (cenário com efeito de P nulo).
4. P3.2 (cobertura do HM) — o mais pesado; roda enquanto os outros são analisados.
5. P4.1, P4.2, P4.3.
6. P5 e as correções documentais.

**V_obs/V_mod externo continua pausado.** Nenhuma nova onda de History Matching. O vetor `z`
não está habilitado, e o P3.2 é verificação interna do procedimento, não calibração.
