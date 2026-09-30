# Revisão independente — rodada 2

**Objeto:** trabalho do Codex em resposta ao parecer `09_REVISAO_INDEPENDENTE_2026-09-15.md`,
worktree `codex/resposta-revisao-cientifica` em `/private/tmp/tcc2-publicacao-auditoria`,
**ainda não commitado**. 11 arquivos, +666 −24.
**Revisor:** Claude · **Autor/implementador:** Codex · **Data:** 15/09/2026

Esta rodada tem um resultado incômodo para mim: duas das minhas críticas se
confirmaram, uma se confirmou pelo mecanismo mas **com o remédio errado**, e o
experimento que eu mesmo pedi produziu um achado que derruba a minha própria
prescrição. Está tudo abaixo, inclusive as retratações.

---

## 1. O que verifiquei nesta rodada

Li os seis pilotos, a análise, os testes e o diff do `04_gemeo_identico.py`;
recalculei por conta própria a decomposição de variância e a distribuição do
observável crítico a partir do `produto/bruto.csv`; e conferi os hashes dos
snapshots.

| verificação | resultado |
|---|---|
| Snapshot do DOCX oficial | `d5a658f1…` — **idêntico byte a byte** ao arquivo vivo no checkout da autora |
| Snapshot do TCC I | `f2017d03…` — confere com o declarado em `SOURCES.md` |
| `EVIDENCE_INDEX.csv` | 90 arquivos com SHA-256 e commit de origem |
| Diff do `04_gemeo_identico.py` | **puramente interpretativo**: `CORTE = 3.0` intacto, nenhuma fórmula alterada |
| Controles diagonais do piloto de confiança | `{"0.25": true, "0.8": true}` — as células que devem reproduzir o simulador nominal reproduzem |
| Execuções dos pilotos | 1.600 execuções, 0 tarefas incompletas, 0 dívida pendente, 0 violações |

**Qualidade de processo.** O plano foi registrado **antes** de rodar
(`PLANO_REVISAO.md`), e contém a frase que mais importa nesta rodada: *"Nenhum
piloto aceita a predição quantitativa do revisor como critério de sucesso."*
Isso é o oposto de buscar confirmação, e foi cumprido — o resultado contraria a
minha predição em um ponto central. O `test_revisao.py` verifica as duas coisas
certas: que o relatório **deixou** de imprimir as frases insustentadas e que a
tabela numérica **não mudou** — provando que a alteração foi de interpretação, não
de número. E testa o estimador pareado contra dados sintéticos de resposta
conhecida. É o melhor trabalho metodológico do projeto até aqui.

---

## 2. Adjudicação dos achados da rodada 1

### CRITICAL-1 — **CONFIRMADO experimentalmente**

Piloto pareado, produto `F × f` fixo em 0,0756, `F` ∈ {0,12; 0,18; 0,24},
32 sementes, 2 instâncias. Contraste `F=0,24` − `F=0,12`:

| observável | contraste | IC 95% | inclui zero? |
|---|---|---|---|
| **taxa_omissao** | **+0,0633** | **[0,0501; 0,0765]** | **não** |
| atraso_relativo | +0,0150 | [−0,0032; 0,0332] | sim |
| retrabalho_sobre_plano | −0,0080 | [−0,0217; 0,0058] | sim |
| E_total | +0,0010 | [−0,0058; 0,0079] | sim |

Com o produto constante, a taxa de omissão muda 0,063 — da ordem da amplitude do
próprio observável. O `[ACHADO 10]` está refutado por experimento, não por
correlação. A retirada foi feita corretamente: o texto saiu, o corte ficou, a
tabela é a mesma.

A verdade refinada é melhor do que a minha formulação e do que a anterior: **o
produto é suficiente para o canal de esforço e retrabalho, e não é suficiente
para o canal de omissão.** É isso que deve ir para a monografia.

### CRITICAL-3 — **CONFIRMADO e quantificado**

Decomposição 2×2 entre portão de confiança e entrada de rede, 12 sementes,
4 instâncias, com as células diagonais controladas contra o nominal:

| observável | portão | rede | interação | total |
|---|---|---|---|---|
| **TL** | **+10,60** [9,16; 12,05] | **0,00** [0,00; 0,00] | +0,44 | +11,04 |
| **TW** | −27,27 [−45,5; −9,0] | **−110,23** [−118,1; −102,3] | +0,23 | −137,27 |
| TU | −119,73 | +14,29 | −15,21 | −120,65 |
| **atraso_relativo** | **−0,3085** [−0,551; −0,066] | **−0,3180** [−0,530; −0,106] | +0,013 | −0,6133 |
| **E_total** | **+0,1168** | **−0,0420** | +0,0262 | +0,1009 |
| taxa_omissao | −0,0042 (inclui 0) | −0,0049 (inclui 0) | +0,0014 | −0,0076 |

O `rede = 0,00` exato em TL, com IC degenerado, é um controle estrutural perfeito:
o tempo de ajuda depende **só** do portão, como tem que ser.

Fora de TL, a atribuição da B9 não se sustenta:

- **`atraso_relativo`: metade do contraste vem do canal cognitivo**, não da
  assistência. Os dois termos são estatisticamente indistinguíveis entre si.
- **`TW`: 80% vem do canal de rede.**
- **`E_total`: os dois canais têm sinais opostos** e se cancelam parcialmente.

Portanto a frase de `06_B9_VERIFICACAO.md` §1.3 — "ao neutralizar a assistência,
o contraste de ociosidade desaparece" — vale para `TL` e **só** para `TL`. Toda
atribuição de 91% a 99,8% do contraste de tempo e ocupação a "τ_inicial =
assistência" precisa ser reescrita: o fator A move dois mecanismos.

### MAJOR-4 — **CONFIRMADO empiricamente**

Cobertura em 20 blocos independentes, contra a observação publicada:

| estimador de variância | exclusões do vetor verdadeiro | taxa | IC 95% exato |
|---|---|---|---|
| legado | 2/20 | 10% | [1,2%; 31,7%] |
| pareado | 4/20 | 20% | [5,7%; 43,7%] |

Contra observações renovadas a cada bloco: 0/20 (legado) e 3/20 (pareado).
Os intervalos são largos com n = 20 e o Codex os reporta — correto. O corte não
foi mexido para produzir cobertura, e o rótulo no relatório passou de
"(Pukelsheim, 1994)" para "(convencao legada; sem garantia conjunta de 95%)".
É a resposta certa: declarar, não recalibrar.

### MAJOR-5 — **parcialmente refutado, e o Codex está certo**

`SOURCES.md` observa que "taxas de aceitação de ondas com domínios distintos
precisam considerar seus denominadores; taxas condicionais não medem diretamente
a mesma região". Isso invalida a minha comparação entre 10% (sobre a caixa a
priori) e 28,7% (sobre o casco do NROY da onda 1): são taxas condicionais a
domínios diferentes, e o aumento é **esperado** ao concentrar a amostra numa
região plausível. Retiro essa parte do argumento.

**O que sobrevive**, porque é afirmação sobre um domínio só: amostrando dentro do
casco da onda 1, apenas 28,7% é NROY. O casco superestima o conjunto em cerca de
3,5×, e larguras marginais de casco continuam sendo estatística insensível.

### MAJOR-1 e MAJOR-2 — **resolvidos na forma**

`EVIDENCE_INDEX.csv` + `recuperar_evidencias.py` recuperam a evidência histórica
por commit e SHA-256, sem merge e sem tocar no checkout — solução melhor que a
que eu sugeri, porque não força concluir o merge pendente. E o snapshot do DOCX
oficial está no Git com hash conferido, idêntico ao arquivo vivo.

Ressalva que permanece: um snapshot é uma foto. Se a autora editar o DOCX de
novo, o snapshot envelhece em silêncio. Ou o `gerar_entrega.js` volta a produzir
esse conteúdo, ou o snapshot precisa de uma verificação de hash que **falhe**
quando o arquivo vivo divergir.

---

## 3. Minhas retratações

**Retrato a predição quantitativa do CRITICAL-2.** Eu previ que, com K = 64, as
larguras marginais contrairiam (`F_ancora` 34% → 60%, `f_retrabalho` 3% → 42%).
Isso não pode acontecer, porque o NROY não se estreita: ele **esvazia**.

Piloto de fronteira, 4 pontos que eram NROY no legado e 4 rejeitados próximos ao
corte:

| ponto | K=8 real | K=64 aproximado (minha conta) | K=64 real | veredito |
|---|---|---|---|---|
| 1 | 2,34 ✓ | 4,21 | **6,16** | rejeitado |
| 159 | 1,64 ✓ | 3,46 | **6,01** | rejeitado |
| 274 | 2,46 ✓ | 4,10 | **3,62** | rejeitado |
| 379 | 1,91 ✓ | 3,69 | **5,55** | rejeitado |

**4 de 4 pontos do NROY legado caem fora com K = 64.** A aproximação que eu usei
— dividir `V_sim` por 8 mantendo as médias — foi **conservadora**: o I real é
maior que o aproximado em três dos quatro pontos, porque as médias também se
deslocam. A direção do meu diagnóstico estava certa; o número, não; e a conclusão
que eu tirei dele ("os parâmetros ficariam melhor identificados") está errada.

**Retiro também a comparação de taxas de aceitação entre ondas** (MAJOR-5,
acima), e aceito a ressalva de `SOURCES.md` de que os K = 30/100/200 de McCulloch
et al. foram escolhidos por diagnóstico e não constituem mínimo universal. Eu os
usei como referência externa; são indício, não requisito.

---

## 4. Achado novo desta rodada — **CRITICAL-4**

### O vetor verdadeiro é excluído permanentemente, e o termo que manda é `V_obs`

O Codex mediu a implausibilidade no próprio vetor verdadeiro com K = 64:

| observável | média no verdadeiro | observação publicada | I |
|---|---|---|---|
| taxa_omissao | 0,09323 | 0,10333 | 1,219 |
| **atraso_relativo** | **1,62423** | **1,57674** | **3,109** |
| retrabalho_sobre_plano | 0,19589 | 0,19725 | 0,145 |
| E_total | 0,85911 | 0,85960 | 0,109 |

**I = 3,109 > 3: o teste do gêmeo idêntico reprova o vetor que gerou os dados.**

Fui além e decompus o denominador. Com K = 64, `V_obs` já responde por 74% a 86%
dele:

| observável | V_obs (z, 20 exec) | V_sim (K=64) | fração de V_obs |
|---|---|---|---|
| taxa_omissao | 5,06e-05 | 1,82e-05 | 73,6% |
| atraso_relativo | 1,75e-04 | 5,86e-05 | 74,9% |
| retrabalho_sobre_plano | 7,51e-05 | 1,26e-05 | 85,6% |
| E_total | 1,47e-05 | 5,00e-06 | 74,6% |

E, no limite K → ∞, com `V_sim` → 0, a implausibilidade do verdadeiro **não vai a
zero**: converge para o escore da própria observação.

```
I(verdadeiro)  ->  |z − μ| / sqrt(V_obs)
atraso_relativo:  0,04748 / sqrt(1,746e-04)  =  3,594
```

**Nenhuma quantidade de réplicas de simulação resgata o vetor verdadeiro.**

Descartei as explicações fáceis. Recalculei a distribuição de `atraso_relativo`
nas 64 execuções do vetor verdadeiro: desvio-padrão 0,0613, assimetria +0,01,
componente entre instâncias ≈ 7% da variância total. Não é cauda pesada, não é
bimodalidade, não é efeito de instância. É uma observação sintética publicada que
está a ~3,6 erros-padrão da média do vetor que a gerou.

Isso reinterpreta tudo:

1. **O cabeçalho do `04_gemeo_identico.py` está errado na direção.** Ele afirma
   que `V_mod = 0` torna o teste "OTIMISTA por construção". Com uma única
   observação `z` fixa, o efeito é o inverso conforme K cresce: o teste vira
   **sistematicamente pessimista**, porque o denominador para de encolher e o
   desvio da observação vira um viés permanente.
2. **O veredito "APROVADO" do gêmeo idêntico é artefato do K = 8.** Ele passa
   porque o denominador é grande, não porque o procedimento identifique algo.
3. **A pergunta central do projeto tem aqui um exemplo puro.** O resultado
   "APROVADO" não emerge do fenômeno modelado: emerge do tamanho da amostra de
   réplicas e de um sorteio particular da observação sintética.

O braço "renovada" da cobertura sustenta a leitura: quando `z` é resorteada a
cada bloco, o estimador legado exclui **0 de 20**. Contra a `z` publicada,
exclui 2 de 20. A `z` publicada é atípica.

**Causa:** demonstrada para o mecanismo; a razão de a `z` publicada ser atípica
(azar de sorteio com 10 sementes de observação, ou `V_obs` subestimado pelo
tratamento iid de 2 instâncias × 10 sementes) ainda é hipótese.
**Confiança:** alta.

---

## 5. Onde discordo ou peço cuidado

**5.1 O trabalho está em `/private/tmp`, sem commit.** 666 linhas e seis pilotos
existem num diretório temporário do macOS, que o sistema limpa periodicamente, e
numa worktree cujos arquivos não estão em nenhum commit. Do meu lado a worktree
aparece como `prunable`. É o mesmo risco do DOCX que a própria rodada acabou de
resolver — desta vez com o trabalho que resolve o risco. Commitar em
`codex/resposta-revisao-cientifica` é a primeira coisa a fazer.

**5.2 Os dois resultados precisam ser publicados juntos.** "O produto não é
suficiente, logo os fatores são separáveis" (CRITICAL-1) e "com medição precisa
o NROY esvazia e o verdadeiro é excluído" (CRITICAL-4) apontam em direções
opostas para o leitor apressado. Separados, o primeiro sugere que a
identificabilidade melhorou. Juntos, dizem a coisa certa: **o canal de
identificação existe, e o instrumento de aceitação atual não consegue usá-lo.**

**5.3 `research/` está fora do layout documentado.** A seção de estrutura do
README lista `data/`, `src/`, `outputs/`, `docs/`, `projeto/`. Um sexto diretório
de primeira classe precisa entrar lá, ou a documentação recomeça a divergir do
repositório — que é exatamente o defeito que a auditoria anterior corrigiu.

**5.4 Concordo com a recusa a calcular largura de conjunto vazio** e com o
desenho do `PLANO_FRONTEIRA.md`. Uma ressalva: oito pontos escolhidos pela
aceitação anterior não estimam volume nem largura, e o próprio plano diz isso.
Manter essa frase no relatório final.

---

## 6. Backlog revisado

| # | item | classe | critério de encerramento |
|---|---|---|---|
| 1 | Commitar a worktree | risco de perda | Nada científico em diretório temporário |
| 2 | **`V_obs` e `V_mod`: a observação, não a réplica, é o termo que manda** | CRITICAL-4 | Decidir e justificar como a incerteza da observação entra em I. Sem isso, nenhuma onda nova é interpretável |
| 3 | Reescrever a atribuição da B9 e do fatorial 2⁴ separando portão e canal cognitivo | CRITICAL-3 | Nenhuma frase atribui a "assistência" efeito que a decomposição mostra ser de rede |
| 4 | Publicar CRITICAL-1 e CRITICAL-4 na mesma seção | redação | O leitor não pode sair com a impressão de que a identificabilidade melhorou |
| 5 | Só então: B5, desenho independente por onda | confirmado | Depois de 2 |
| 6 | `research/` no layout do README | MINOR | Estrutura documentada = estrutura real |
| 7 | Verificação de hash que falhe quando o DOCX vivo divergir do snapshot | MAJOR-2 residual | Snapshot que envelhece em silêncio não protege |
| 8 | A10/B6 nos vértices: **resultado negativo, preservar** | encerrado nesta forma | 128 execuções, 0 incompletas, 0 dívida, 0 violações |

---

## 7. Questões que voltam ao Codex

1. **Discriminar por que a `z` publicada é atípica.** Rodar o vetor verdadeiro
   com as sementes de observação 100–109 e confirmar que reproduz `z` exatamente
   (descarta deriva de código). Depois estimar a distribuição da própria `z` com,
   digamos, 200 sementes de observação, e verificar se o desvio de 0,0475 em
   `atraso_relativo` está dentro de ~2 desvios de uma `V_obs` bem estimada. Se
   estiver, a `z` foi azar de sorteio; se não estiver, `V_obs` está subestimada.
2. **Cobertura conjunta com `z` resorteada.** Repetir a cobertura com `z` nova a
   cada bloco **e** K alto, que é a combinação ainda não testada. A taxa de
   exclusão do verdadeiro nesse desenho é o número que diz se o corte 3 serve.
3. **Qual `V_mod` tornaria o teste honesto?** Não escolher o valor que faz passar.
   Medir qual magnitude de `V_mod` seria necessária para que o verdadeiro
   sobrevivesse com K = 64 e declarar se essa magnitude é defensável — se não
   for, a conclusão é que o desenho do gêmeo precisa mudar, não o parâmetro.
4. **Reexecutar a B9 e o fatorial com os dois canais separados**, produzindo a
   tabela ANTES/DEPOIS de cada percentual publicado que mudar.
5. **Verificar a unimodalidade dos resíduos** nos quatro observáveis, já que a
   desigualdade de Vysochanskii–Petunin exige densidade unimodal. Eu verifiquei
   `atraso_relativo` e `taxa_omissao` no vetor verdadeiro e não encontrei
   patologia; falta o resto do espaço.

---

## 8. Memória científica

**Confirmado nesta rodada:** CRITICAL-1 (por experimento pareado);
CRITICAL-3 (por decomposição 2×2 com controle estrutural); MAJOR-4 (cobertura
empírica 10–20%); o mecanismo do CRITICAL-2 (4/4 pontos do NROY caem com K=64).

**Refutado nesta rodada:** a minha predição quantitativa de contração de larguras
(CRITICAL-2); a minha comparação de taxas de aceitação entre ondas (MAJOR-5).

**Novo:** CRITICAL-4 — `V_obs` domina o denominador e o vetor verdadeiro é
excluído no limite; o veredito "APROVADO" é artefato do K pequeno.

**Resolvido:** MAJOR-1 (índice de evidências por hash e commit) e MAJOR-2
(snapshot versionado, hash conferido).

**Preservado como resultado negativo:** nenhum truncamento nos 32 vértices da
caixa; os 8 pontos equiespaçados da onda 1 rejeitados com K=4 e K=32.

**Em aberto:** por que a `z` publicada é atípica; qual `V_mod` seria defensável;
unimodalidade fora dos pontos verificados; se o canal cognitivo e o portão
interagem em outros arranjos além do centralizado.
