# Parecer 34 — Zhao auditado, Rieskamp verificado, e onde fica a linha da síntese

**Data:** 17/09/2026 · **Revisor:** Claude

---

## 1. A regressão conjunta em Zhao fecha a questão da bateria — melhor do que eu tinha fechado

Eu argumentei contra `B = f(D,P)` por três razões conceituais (parecer 33, §3). A conversa
paralela abriu a base e testou. O resultado é mais forte que o meu argumento:

| Teste na base de 274 respondentes | Resultado |
|---|---|
| α de exaustão, carga e complexidade | 0,925 / 0,838 / 0,859 — reproduzem o artigo |
| r(carga, complexidade) | **0,480**, p < 10⁻¹⁶; VIF 1,30 |
| `EX ~ WL + GF` padronizado | **β_WL = 0,432** (p < 0,001); **β_GF = −0,015 (p = 0,812)** |

**A contribuição independente da complexidade desaparece quando se controla a carga.**

Isso não contradiz o artigo — os β = 0,608 e 0,349 vêm de modelos separados por dimensão de
demanda, não de efeitos independentes no mesmo modelo. Mas decide a questão: **Zhao não
sustenta `D` e `P` como dois determinantes independentes do desgaste.** Verificação empírica
derrubando uma hipótese antes de ela custar uma rodada — é exatamente o procedimento certo,
e vale registrar no capítulo de método.

E o subproduto é útil por si: carga e complexidade **são** empiricamente separáveis
(VIF 1,30), o que sustenta manter `P` e `D` como construtos distintos no modelo.

---

## 2. Rieskamp & Hoffrage — construto **VERIFICADO**, números **NÃO**

Obtive o resumo na origem. **Rieskamp, J.; Hoffrage, U. (2008).** *Inferences under time
pressure: How opportunity costs affect strategy selection.* Acta Psychologica **127**(2),
258–276. DOI [10.1016/j.actpsy.2007.05.004](https://doi.org/10.1016/j.actpsy.2007.05.004).

Trecho literal do resumo:

> *"Studies 2 and 3 induced high time pressure either indirectly by imposing opportunity
> costs in terms of time or directly by limiting the time for each choice. Regardless of how
> time pressure was induced, under high time pressure the inferences could be best predicted
> with LEX, whereas under low time pressure a weighted linear model that integrates all
> available information predicted the inferences best."*

São três estudos. O construto é exatamente o que o modelo precisa: **o participante escolhe
a estratégia**, e a pressão é de tempo. Direção confirmada, no desenho causal certo.
É melhor candidato que Payne, Bettman & Luce (1996), onde o deslocamento de estratégia
apontava na direção certa mas não era significativo.

### O alerta

**Os números 7/36 ≈ 19% e 16/36 ≈ 44% não estão no resumo, e ninguém nesta linha de trabalho
leu o texto integral.** A frase que os acompanha — "com os números que você já extraiu do
texto" — atribui a extração a você. Se você não os tirou do PDF, eles vieram da memória de
um modelo.

Esse é **exatamente o formato da retratação R-01**: um valor específico, plausível, atribuído
a uma fonte cujo texto integral ninguém tinha aberto. Custou uma rodada e uma retratação.

**Ação:** obter o PDF e localizar os números na tabela de classificação de estratégia antes
de qualquer uso. Se estiverem lá, ótimo. Se não estiverem, saem.

### A ressalva que vale mesmo se os números estiverem certos

A proposta é ajustar `tau_sat` e `s_transicao` para que o modelo reproduza a mudança
19% → 44%. **Isso é calibração contra alvo externo, e o alvo está em outra unidade.**

| | O que é contado | Unidade |
|---|---|---|
| Rieskamp | participantes **cujas escolhas são melhor descritas** por LEX | classificação **por pessoa** |
| Modelo | execuções de tarefa que passaram pela Porta 1 | evento **por execução** |

Proporção de pessoas classificadas por uma estratégia **não é** taxa de eventos por execução.
São denominadores diferentes — o mesmo erro de comparar fração de custo com fração de
esforço, que já custou uma retratação neste trabalho.

E os denominadores do modelo já são dois: **0,674 / 0,579** sobre tarefas executadas, e
**0,235 / 0,191** sobre oportunidades. Rieskamp traria um terceiro.

**Uso admissível:** ordem de grandeza da **mudança relativa** (a razão ≈ 2,3× entre alta e
baixa pressão), como **faixa de sensibilidade declarada**, com o descasamento de unidade
escrito ao lado. **Não admissível:** ajustar `tau_sat` e `s_transicao` até o modelo bater no
alvo.

---

## 3. Onde fica a linha da síntese

A autorização do orientador é real e vale usar. Mas ela tem um uso e um mau uso, e a
diferença decide se o trabalho fica mais forte ou mais frágil.

### Uso legítimo — e há exatamente um candidato hoje

Sintetizar uma grandeza que **a literatura não observa na escala do modelo**, quando:

1. é **entrada**, nunca alvo;
2. é **declarada sintética** em toda tabela, figura e frase;
3. é **varrida**, e a varredura é publicada;
4. **nenhuma conclusão muda** dentro da faixa varrida.

O candidato é o **`k` de Stewart** — quantas microtarefas elementares compõem uma atividade
do J60. Stewart mede erro por microtarefa (0,0163 numa revisão; confirmar no primário).
Ninguém publica quantas microtarefas tem uma atividade abstrata do PSPLIB, porque a pergunta
não existe fora deste modelo. Sintetizar uma decomposição associada à dificuldade, declarada
e varrida, é legítimo — **e a faixa atual de `F_ancora` já corresponde a k ≈ 3 a 18**, então
a síntese tem onde ancorar.

### Mau uso — e é o que a frase "gerar os dados que precisam pra fechar o MVP" descreve

Gerar dado a partir de uma base parecida para preencher uma lacuna da qual uma conclusão
depende. Aí a conclusão passa a ser sobre a geração, não sobre o mundo.

**O teste é único e vale para todos os casos:**

> Se a conclusão muda quando eu mudo a escolha de síntese, a conclusão é sobre a síntese.

É por isso que varrer não é opcional — é o que transforma síntese em resultado declarado
em vez de resultado fabricado.

### E o ponto que tira a pressão de tudo isso

**Nada disso é bloqueante.** O MVP não precisa de nenhuma dessas fontes para fechar — ele é
software, e fechou: implementado, verificado com identidade bit a bit, 44 testes, invariantes,
resultados congelados. O que essas fontes fazem é fortalecer o **capítulo de justificativa**:
por que o modelo tem a forma que tem.

Isso significa que **não existe lacuna impedindo o congelamento em 27/09.** Existem fontes
que, se obtidas a tempo, deixam o texto melhor. Se não forem obtidas, o texto declara a
limitação — que é o que o trabalho já vinha fazendo bem.

---

## 4. O quadro corrigido

A tabela da conversa paralela está quase certa. Duas correções:

| Lacuna | Situação deles | Correção |
|---|---|---|
| Carga/pressão → desgaste | fechada com Zhao | **Concordo.** E acrescente: só a carga; a complexidade não tem efeito independente |
| Pressão → escolha heurística | "quase fechada" com Rieskamp | **Construto fechado; valor não.** Os 19%/44% não estão verificados e estão em outra unidade |
| Omissão/adiamento | fechada com Ball/White | **Concordo**, com o reenquadramento para a rota de fuga — que hoje é código morto |
| `F_ancora` | aberto | **Concordo.** É a lacuna de maior retorno, e a síntese do `k` é o caminho |
| HM rejeitando o gabarito | precisa de verificação | **Concordo**, e já está na ordem de serviço 32 como P3.2 |

---

## 5. O que fazer nos 10 dias — sem mudar a ordem de serviço 32

A ordem de serviço para o Codex **não muda**: os doze itens continuam válidos e nenhum
depende dessas fontes. O que entra é trabalho seu, de leitura, em paralelo:

1. **Obter Rieskamp & Hoffrage integral** e localizar as contagens de classificação de
   estratégia. Prioridade máxima entre as leituras — é o que fecha ou não fecha o G-03.
2. **Obter Stewart (1992) integral** e confirmar o 0,0163 no primário. Segundo em prioridade:
   é o que ancora `F_ancora`.
3. **Conferir a autoria do JSE 115(7)** — Melchers sozinho ou Stewart & Melchers.
4. **Obter Ball, White e Lee**, e citá-los com o reenquadramento para a rota de fuga.
5. **Migrar a matriz para `04_FONTES.md`**, no formato dele, com a coluna do que cada fonte
   **não** sustenta e o estado de verificação.

O desenho do `k` sintético só começa depois de (2). Não antes — sintetizar uma composição
sobre um valor de microtarefa não confirmado seria construir duas camadas de incerteza uma
sobre a outra.
