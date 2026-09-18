# Ordem de serviço 37 — Lote final do MVP, com testes e critérios de aceitação

**Data:** 17/09/2026 · **Substitui e consolida a ordem 32** e os itens novos dos pareceres 35 e 36.
**Congelamento da simulação: 27/09/2026.** Este é o último lote.

---

## Regras que valem para todos os itens

1. **O nominal histórico não é substituído.** Tudo entra como alternativa preservada e varrida.
2. **Protocolo registrado antes de executar**, como em T1/T2/T3.
3. **Porta de segurança global:** depois de cada item, o teste de identidade bit a bit com as
   opções neutras tem de continuar passando — todos os campos por `float.hex()`, o estado do
   RNG e a guarda anti-delegação. **Se quebrar, o item volta; não se afrouxa o teste.**
4. **Se a saída esperada não aparecer, refazer** e reportar o que se observou. Não ajustar o
   critério para a saída passar. Em nenhum item o objetivo é "dar certo" — é medir.
5. **Nada de nova onda de History Matching.** O vetor `z` externo continua desabilitado.

---

# BLOCO A — Defeito estrutural

## A1 · Rota de fuga da Porta 1 nunca executa

**Diagnóstico.** `p1_fuga = 0,000000` e `n_adiamentos = 0,000000` nos dois arranjos, em 16
instâncias × 12 sementes. A condição é `omega > limite_aversao_perda`, com `omega = 0,50`
(premissa, igual nos dois cenários) e `limite_aversao_perda = 0,60`. **Os dois lados são
constantes lidas uma vez**, logo a comparação é uma constante de tempo de compilação: ou
nenhuma decisão heurística vira fuga, ou todas viram. Não há regime intermediário. E
`limite_aversao_perda` declara `varredura: [0,40; 0,60; 0,80]` no YAML mas **não está no
desenho de robustez executado**.

**Implementar.** Alternativa preservada `regra_fuga` com dois valores: `constante` (atual,
default, preserva bits) e `dependente_estado`. Na segunda, a fuga passa a depender da
sobrecarga, não de duas constantes — forma sugerida, a declarar como `[DEC]`:
`omega·q > limite`, com `q = max(0, 2·p_heu − 1)`. Incluir `limite_aversao_perda` no desenho
de robustez, ou declarar por que ficou fora.

**Testar.**
- Controle de identidade: com `regra_fuga='constante'`, bits idênticos ao nominal atual.
- Contrafactual local: mesma tarefa, mesmo estado, mesmos sorteios, com e sem a regra nova.
- Varredura de `limite` em pelo menos [0,10; 0,20; 0,30; 0,40] sob a regra dependente.

**Saída esperada.** Sob `dependente_estado`, `p1_fuga > 0` em alguma configuração **e**
variação contínua de `p1_fuga` com `limite`, não degrau. Os cinco indicadores reportados com
IC95 no nominal e na alternativa.

**Se não bater.** Se `p1_fuga` continuar 0 em toda a varredura, a condição ainda é
degenerada — refazer a formulação. Se for função degrau, reportar como tal: significa que a
fuga continua sendo interruptor, e isso muda o que a monografia pode dizer do mecanismo.

---

# BLOCO B — Leitura do mecanismo

## B1 · T4 — separar o portão de assistência do canal difuso

**Diagnóstico.** O bloco `confianca` do T2 move `tau_inicial` **e** `tau_min` juntos, e
`tau_inicial` alimenta dois caminhos: o portão de assistência e a entrada difusa
(`desconfianca = 1 − confianca` → `mu_rede`). O efeito significativo sobre
`taxa_falha_efetiva` (−0,0345, IC95 [−0,049 ; −0,021]) pode vir de qualquer um dos dois.

**Implementar.** Nada novo: `tau_portao` e `tau_rede` já existem como overrides independentes.

**Testar.** Quatro células — portão centralizado/adaptativo × rede centralizada/adaptativa —
com `p_reporte` e `p_deteccao` **igualados**. Mesmas instâncias e sementes do T2.

**Saída esperada.** Os cinco indicadores nas quatro células, com IC95, e a decomposição do
efeito de confiança em parcela do portão e parcela da rede.

**Se não bater.** Se as duas diagonais não reproduzirem o nominal correspondente, há erro de
implementação dos overrides — refazer antes de interpretar.

**Interpretação a registrar.** `p0` depende de `mu_cog`, não de `mu_rede`. Se o efeito passar
pela rede, a leitura correta não é "assistência reduz defeito", e sim "confiança reduz
duração, e duração reduz degradação cognitiva". Escrever qual dos dois foi.

## B2 · Cenário com o canal de erro direto desligado

**Diagnóstico.** O modelo tem **dois canais** da pressão para o erro:
`p_heu = σ((E − τ_sat)/s)`, que é **seleção de estratégia** e tem apoio empírico
(Rieskamp & Hoffrage 2008); e `R_error·(1 − μ_cog)`, que é **erro direto** e **não tem apoio
de campo**. Três tentativas de campo deram nulo ou sinal oposto, cada uma com descasamento de
construto. **Isso é ausência de evidência, não demonstração de efeito nulo** — a distinção
importa e tem de estar no texto.

**Implementar.** Alternativa `canal_erro_direto` com valores `ativo` (default) e `desligado`
(`R_error = 0`). Não alterar `p_heu`.

**Testar.** Nominal nas duas configurações, mesmas instâncias e sementes. Varrer também
`s_transicao` e `tau_sat` em torno do nominal, nas duas.

**Saída esperada.** Os cinco indicadores com IC95 nas duas configurações, e a resposta
explícita: **as conclusões centralizado × adaptativo sobrevivem com o canal desligado?**

**Se não bater.** Se não sobreviverem, **reportar assim mesmo**. Esse é um resultado, e é
melhor sabê-lo agora. Não procurar configuração em que sobrevivam.

---

# BLOCO C — Ancoragem empírica (novo, dos textos integrais)

## C1 · Ancorar `F_ancora` em Stewart & Melchers (1988)

**Base.** Tabela 1, p. 290: cálculo de 1, 2, 3, 4, 5 e 8 passos dá 0,0128 / 0,0256 / 0,0384 /
0,0512 / 0,0640 / 0,1024 — **linear exato em k**. Consulta a tabela: 0,0126.

**Implementar.** Reparametrizar: `F_ancora = k × 0,0128`, com `k` = número de microtarefas
elementares por atividade, derivado do nível de dificuldade por uma decomposição **declarada
sintética** e varrida (é o único ponto onde a autorização do orientador se aplica).

**Testar.**
- Controle exato: para k = 1, 2, 3, 4, 5, 8 a função deve devolver exatamente 0,0128, 0,0256,
  0,0384, 0,0512, 0,0640 e 0,1024, comparados por `float.hex()` ou tolerância de 1e-12.
- Mapa reverso publicado: para cada valor da varredura atual de `F_ancora`, reportar o `k`
  implícito.

**Saída esperada.** Tabela com os seis pontos batendo exato, e a tabela reversa mostrando
`k ≈ 3,9` para 0,05 e `k ≈ 7,8` para 0,10.

**Rótulo obrigatório.** `F_ancora` de **0,15 a 0,25 exige k acima de 8**, que é o maior valor
publicado. Esses valores entram como **cenário de sensibilidade**, nunca como valor ancorado.
A decomposição sintética deve **preferencialmente cair em k ≤ 8**.

**Se não bater.** Se algum dos seis pontos não reproduzir exato, o mapeamento está errado —
refazer antes de rodar qualquer lote.

## C2 · Heterogeneidade de taxa de erro entre agentes (CV = 1,13)

**Base.** Stewart 1992, p. 174: beta-binomial com μ = 0,0163, σ² = 0,00034, **V = σ/μ = 1,13**,
α = 0,7546, β = 45,4563. O autor declara que V pode ser assumido constante para qualquer taxa
média.

**Implementar.** Alternativa `heterogeneidade_erro` com valores `nenhuma` (default, preserva
bits) e `beta_cv113`. Na segunda, cada agente recebe uma taxa basal sorteada de Beta com média
igual ao `F_base` configurado e coeficiente de variação 1,13. Dado μ e CV:

```
σ = 1,13 · μ
t = μ(1 − μ)/σ² − 1
α = μ · t        β = (1 − μ) · t
```

**Testar.**
- **Controle positivo, e é o teste decisivo:** para μ = 0,0163, a fórmula deve devolver
  **α ≈ 0,7546 e β ≈ 45,46**, reproduzindo os valores publicados por Stewart. Tolerância de
  arredondamento da terceira casa.
- Controle de identidade com `nenhuma`.
- Verificar média e CV empíricos da amostra de agentes.

**Saída esperada.** α e β reproduzindo os publicados; média e CV empíricos convergindo para
μ e 1,13; os cinco indicadores com IC95 nas duas configurações.

**Armadilha a tratar explicitamente.** A Beta com CV = 1,13 **só existe para μ ≤ 0,4392**,
porque σ = 1,13μ precisa satisfazer σ² ≤ μ(1−μ). Com `F_ancora` alto e o multiplicador de
risco da camada NASA, `F_base` **pode ultrapassar esse limite**. O código tem de detectar e
**falhar com mensagem explícita**, não silenciosamente reduzir o CV. Registrar em quais
células isso ocorre.

**Se não bater.** Se α e β não reproduzirem os publicados, a parametrização está errada.
Não seguir adiante.

## C3 · Sensibilidade à não independência entre erros

**Base.** Stewart 1992, Tabela 2, p. 175: a binomial (independência) é **rejeitada**
(χ² = 10,174 contra crítico 5,991, 2 g.l.). Beta-binomial χ² = 0,162 e binomial p-dependente
χ² = 0,583, ambas com 1 g.l. e crítico 3,841. A p-dependente usa `p_x = φ · p_av · x` com
**φ = 0,845**.

**Implementar.** Alternativa `dependencia_erro` com `nenhuma` (default) e `p_dependente`.

**Testar — o melhor controle deste lote.** A Tabela 2 de Stewart é um conjunto de validação
completo. Com n = 25 microtarefas e 94 respondentes, implementar as três distribuições e
conferir que reproduzem as frequências esperadas publicadas:

| Nº de erros | Observado | Binomial | Beta-binomial | p-dependente |
|---:|---:|---:|---:|---:|
| 0 | 68 | 62,330 | 67,475 | 66,416 |
| 1 | 18 | 25,820 | 18,334 | 19,719 |
| 2 | 5 | 5,134 | 5,639 | 5,690 |
| 3 | 2 | 0,652 | 1,765 | 1,593 |
| 4 | 1 | 0,059 | 0,549 | 0,432 |
| 5 | 0 | 0,004 | 0,167 | 0,113 |
| 6 | 0 | 0,000 | 0,050 | 0,029 |
| 7 | 0 | 0,000 | 0,014 | 0,007 |
| 8 | 0 | 0,000 | 0,000 | 0,002 |
| **χ²** | | **10,174** | **0,162** | **0,583** |

Parâmetros: binomial `p = 0,0163`; beta-binomial `μ = 0,0163`, `V = 1,13`; p-dependente
`p_av = 0,0163`, `φ = 0,845`.

**Saída esperada.** As frequências esperadas reproduzidas na terceira casa decimal e os três
χ² batendo. **Se isso passar, a implementação das distribuições está correta** e pode ser
usada com confiança no simulador.

**Magnitude a reportar — com a ressalva.** O texto de Stewart resume aumentos de
*"aproximadamente 20–30% e 50%"* na probabilidade de falha. O recálculo direto da Tabela 3
(p. 177) dá **+27,0% e +43,7%** para a beta-binomial e **+94,2% e +110,7%** para a
p-dependente, nos dois procedimentos publicados. **Reportar as duas coisas e deixar explícito
que o recálculo é nosso** — não corrigir o autor em silêncio. E o escopo é daquela análise de
confiabilidade específica, não lei geral.

**Se não bater.** Se as frequências não reproduzirem, a implementação está errada. Este teste
não admite tolerância frouxa: os valores são publicados.

## C4 · Faixa de sensibilidade de `p_heu` a partir de Rieskamp

**Base.** Rieskamp & Hoffrage 2008, Estudo 2, p. 266–267: 7 de 36 (19,4%) classificados com
estratégia não compensatória sob baixa pressão, 16 de 36 (44,4%) sob alta. McNemar p = 0,02.

**Implementar.** Nada no modelo. É **análise**, não parâmetro.

**Testar.** Varrer `tau_sat` e `s_transicao` e reportar a razão entre a fração via Porta 1 no
extremo superior e no extremo inferior da faixa de `P` do modelo.

**Saída esperada.** A razão observada no modelo, comparada à razão de **2,3×** (ou +25 p.p.)
de Rieskamp, **declarando o descasamento de unidade**: Rieskamp conta participante
classificado, o modelo conta execução de tarefa. São denominadores diferentes.

**PROIBIDO.** Ajustar `tau_sat` ou `s_transicao` para o modelo bater em 19,4% → 44,4%. Isso
seria calibrar contra alvo de outra unidade. A comparação é **descritiva** e entra como faixa
de sensibilidade declarada.

**Contexto a registrar.** O Estudo 1 do mesmo artigo **não** achou o efeito (χ²(1) = 0,10,
p = 0,75), porque ali ambas as condições tinham custo de oportunidade. O contraste do Estudo 2
é pressão contra **ausência** de pressão, e o `P` do modelo nunca desce abaixo de 0,30.

---

# BLOCO D — Readout e diagnóstico da calibração

## D1 · Novo readout de retrabalho

**Implementar.** `retrabalho_sobre_esforco_total = TR / (E_plano + TR)` como campo derivado,
sem alterar RNG, decisões ou estados — mesmo tratamento do `taxa_falha_efetiva` no T3.
Propagar aos runners e resumos.

**Testar.** Controle ANTES/DEPOIS em todos os campos preexistentes.

**Saída esperada.** Campos anteriores inalterados (resíduo máximo da ordem de 1e-14), e o
campo novo dando aproximadamente **0,190** (adaptativa) e **0,224** (centralizada) no nominal.

**Se não bater.** Se algum campo preexistente mudar, houve efeito colateral — refazer.

## D2 · Teste de cobertura do History Matching

**Diagnóstico.** O gêmeo sintético atual usa **uma única** pseudo-observação. Uma realização
com `I = 3,594` **não** demonstra que o instrumento está desregulado, porque o próprio `z`
sintético é aleatório mesmo gerado no vetor verdadeiro. Os 0/20, 3/20, 2/20 e 4/20 já
existentes são poucos demais.

**Implementar.** Cobertura repetida, B = 500 (1.000 se couber no tempo). Em cada réplica:
gerar `z_b` novo no vetor verdadeiro pelo desenho declarado; reestimar a resposta do verdadeiro
com sementes independentes; calcular os quatro `I_j` e `I_max,b`; registrar `I_max,b > 3`.

**Saída esperada.** A **taxa empírica de falsa exclusão** com intervalo de confiança binomial,
e o **percentil 95 de `I_max`** sob o vetor verdadeiro.

**Como interpretar — os dois resultados são úteis.** Taxa em torno de 5% significa que o
episódio de 3,594 foi realização rara e o instrumento está razoavelmente calibrado. Taxa alta
significa que o corte 3 é agressivo demais para um desenho de **quatro** observáveis — e aí o
percentil 95 vira corte conjunto empiricamente justificado, registrando que o corte 3 vem de
uma regra marginal.

**PROIBIDO.** Ajustar `V_mod` até o gabarito passar. Escolher pseudo-observação favorável.

**Se a taxa for muito alta (acima de ~30%).** Não tratar como resultado — pode haver erro no
desenho. Reportar e parar antes de usar o HM.

## D3 · Declarar o estimando do `V_obs` sintético

**Diagnóstico.** Hoje `V_obs` é `d[o].var(ddof=1)/n` sobre execuções do **próprio simulador**.
Isso só é válido se estiver declarado qual experimento o `z` sintético imita.

**Implementar.** Escrever o estimando explicitamente (por exemplo: média esperada do observável
nas instâncias fixas, sobre a aleatoriedade dos agentes) e fazer geração e estimação
respeitarem a mesma unidade amostral. **Renomear o gêmeo idêntico para "verificação interna do
procedimento"** — ele não informa o `V_obs` externo, e o texto não pode sugerir que informa.

**Saída esperada.** Documento curto com o estimando declarado, e o código coerente com ele.

---

# BLOCO E — Pendências de análise e instrumentação

## E1 · Recalcular o gradiente sobre linhas de código

**Diagnóstico.** O gradiente publicado está no eixo de complexidade ciclomática, que **não
sobrevive ao controle de tamanho**: razão de chances 0,944, p = 0,166, negativa. O eixo de
linhas de código dá gradiente mais acentuado (até 5,37 contra 2,99) e mais preciso (z = 34,3
contra 25,6).

**Saída esperada.** Gradiente recalculado e republicado. **Não é conferência — os números
mudam.** Declarar qual versão dos dados NASA foi usada (Shepperd et al. publicam versões
limpas; ver `04_FONTES`).

## E2 · Instrumentar a saturação da confiança

**Diagnóstico.** `confianca_media_final` = 0,9364 no adaptativo (de 0,80, teto 1,0) e 0,2500
no centralizado (congelada, porque nunca há evento). A lei cresce multiplicativamente no
sucesso e decresce 0,01 no insucesso, com 102,9 sucessos contra 39,1 insucessos por execução —
é catraca de mão única, sem laço de balanceamento.

**Saída esperada.** Trajetória de confiança exportada e o **período em que a média cruza 0,95**,
para a monografia poder declarar com número que a confiança é, na prática, condição inicial e
não variável de estado com dinâmica própria.

## E3 · Testar a faixa de `mu_minimo` contra referência externa

**Base.** Reichelt & Lyneis (1999), Tabelas 1–2: degradação média de qualidade de **0,95** por
pressão de cronograma e **0,97** por fadiga de hora extra.

**Saída esperada.** Distribuição de `mu_cog` e `mu_rede` observada no nominal, e verificação de
compatibilidade com médias dessa ordem.

**Ressalva obrigatória no texto.** São saídas de modelo de Dinâmica de Sistemas calibrado, **da
mesma linhagem deste trabalho** — é consistência com a literatura de modelagem, não medição
independente.

---

# BLOCO F — Arrumação do repositório

- `Claude outputs/` no `.gitignore`. Hoje há cópias duplicadas de `18_HISTORICO...docx`,
  `20_AUDITORIA...md` e `BRIEFING_TRES_LACUNAS.md` na raiz, fora de `projeto/`, e não estão
  ignoradas. O lugar canônico é `projeto/`.
- Commitar os pareceres 23 e 25 a 37.
- Resolver os dois arquivos numerados 07 (`07_AUTONOMIA.md` versionado e
  `07_BRIEFING_ORIENTADOR.md` sem versionar).
- Correções documentais da bancada de fatores humanos, se ela virar apêndice: `taxa_reversao_pct`
  está mal rotulada (é proporção de commits **que foram revertidos**, não que **são** reversões;
  publicar o tamanho de `base`), e a tabela de tênis mistura denominadores (dupla falta por
  ponto no CSV, por 2º saque no relatório).

---

# Ordem sugerida

1. **D1 e D3** — baratos, não alteram dinâmica, abrem caminho.
2. **C1, C2, C3** — a ancoragem. **C3 primeiro**, porque a Tabela 2 valida as distribuições
   antes de elas entrarem no simulador.
3. **A1 e B1** — podem rodar no mesmo lote.
4. **B2** — cenário com o canal de erro direto desligado.
5. **D2** — o mais pesado; roda enquanto os outros são analisados.
6. **C4, E1, E2, E3**.
7. **F**.

---

# Critério de encerramento do lote

O lote está fechado quando:

- o teste de identidade bit a bit passa com as opções neutras, depois de todas as alterações;
- os controles publicados reproduzem: seis pontos de C1, α e β de C2, e as frequências e χ² da
  Tabela 2 em C3;
- os cinco indicadores estão reportados com IC95 em cada alternativa;
- toda alternativa nova aparece no desenho de robustez ou tem declarado por que não aparece;
- nenhum resultado foi escolhido por ser favorável.

**Se qualquer controle publicado falhar, o lote não fecha.** Reportar o que se observou, o que
se esperava, e o que foi tentado — antes de prosseguir.
