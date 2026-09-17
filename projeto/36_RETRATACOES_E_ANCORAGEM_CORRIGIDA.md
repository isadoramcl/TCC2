# Parecer 36 — Retratações R-11 a R-13 e a ancoragem corrigida

**Data:** 17/09/2026 · **Revisor:** Claude
**Origem:** crítica em conversa paralela ao parecer 35, após segunda leitura dos primários

---

## 1. Aceito as três correções. Duas vão mais longe.

### R-11 · A extrapolação linear até k = 20

**O que eu escrevi:** que a faixa `F_ancora = [0,05 ; 0,25]` corresponde a atividades de
4 a 20 passos elementares, como se fosse mapeamento estabelecido.

**Por que está errado:** a Tabela 1 (p. 290) publica k = 1, 2, 3, 4, 5 e **8**. O maior valor
observado é 8, que dá 0,1024. Tudo acima disso é extrapolação.

**O recorte correto:**

| `F_ancora` varrido | k implícito | Estado |
|---:|---:|---|
| 0,05 | 3,9 | **dentro da faixa observada** |
| 0,10 | 7,8 | **dentro da faixa observada** (limite) |
| 0,15 | 11,7 | extrapolação |
| 0,20 | 15,6 | extrapolação |
| 0,25 | 19,5 | extrapolação |

**Dois dos cinco valores varridos estão ancorados. Três são extrapolação** e têm de ser
rotulados como cenário de sensibilidade.

**E há uma razão mecanicista contra a extrapolação que a crítica não levantou.** A
linearidade `p ≈ kp₁` é a aproximação de primeira ordem da composição **por independência**,
`1 − (1−p₁)^k`. E o artigo-irmão, Stewart (1992), **rejeita a independência** entre erros
(χ² = 10,174 contra crítico 5,991). Ou seja: além de não haver dado acima de k = 8, o
mecanismo que justificaria a linearidade está refutado pelo próprio autor, em outro artigo.
Isso torna a extrapolação **mais** frágil, não menos.

**Ressalva adicional de amostra:** o `p_av = 0,0163` de Stewart (1992) vem de um conjunto que
**descartou deliberadamente** as tarefas de cálculo de quatro e cinco passos, para igualar
dificuldade (p. 173). Então 0,0163 e 0,0128 vêm de conjuntos relacionados, não idênticos.
Não misture os dois numa mesma conta sem dizer isso.

### R-12 · Stewart (1992) não é evidência de efeito nulo da pressão

**O que eu escrevi:** que era "o quinto achado independente sem efeito de pressão sobre erro".

**Por que está errado, e é o erro mais sério dos três:** a manipulação **falhou**. Metade dos
respondentes foi instruída a completar no menor tempo possível, e os tempos de resposta não
diferiram — o próprio autor conclui que *"the instructions were not sufficiently explicit"* e
funde as duas amostras (p. 173). Uma manipulação que falha **não produz informação** sobre o
efeito. Concluir "nulo" a partir dela é tratar ausência de evidência como evidência de
ausência.

**E eu estendi o erro:** contei também Stewart & Melchers (1988) como quarto achado. Mas a
hipótese (v) daquele artigo — *"No microtask completion time constraints (i.e. no time
pressure)"*, p. 289 — é **declaração de escopo do modelo**, não resultado. Não é evidência
de nada sobre pressão.

**A contagem honesta**, portanto, não é cinco:

> Nenhum estudo de campo com manipulação limpa de pressão temporal demonstrou efeito direto
> de pressão sobre erro no sentido do modelo. Três tentativas deram nulo ou sinal oposto
> (tênis com sinal invertido, NBA e Go nulos), cada uma com seu próprio descasamento de
> construto. Stewart (1992) não testa a questão porque a manipulação não funcionou.

Mais fraco que o que eu escrevi, e é o que se sustenta.

**A recomendação sobrevive à retratação.** Rodar o cenário com `R_error·(1−μ_cog) = 0`
continua certo — não porque a literatura prove efeito nulo, mas porque **não há evidência de
campo sustentando o canal**, e o trabalho precisa mostrar se depende dele.

### R-13 · A omissão de Stewart sustenta a Porta 1, não a rota de fuga

**O que eu escrevi:** que as taxas de omissão de 0,40 a 0,80 justificam corrigir a rota de fuga.

**Por que está errado:** em Stewart & Melchers, omissão é **pular uma microtarefa dentro da
macrotarefa**; o algoritmo segue para a próxima e o projeto é concluído, com um componente
faltando. Não é abandonar a atividade.

O mapeamento correto separa as duas fontes:

| Construto externo | O que é | Porta do modelo |
|---|---|---|
| Omissão de Stewart & Melchers | microtarefa pulada; a atividade **é concluída**, pior | **Porta 1 (omissão)** |
| *Care left undone* de Ball e White | a tarefa necessária **não é realizada** por falta de tempo | **rota de fuga (adiamento)** |

Eu havia mapeado corretamente Ball e White para a fuga (parecer 33, §5) e depois **misturei**
Stewart no mesmo balde. São portas diferentes.

**A boa notícia é que isso melhora o quadro:** a estrutura de Stewart — nó de omissão
primeiro, comissão depois — é a estrutura da **Porta 1**, que é o mecanismo principal do
modelo e não o ramo morto.

**Mas as taxas continuam intransportáveis.** PRFO = 0,80 é a taxa de omitir **aquele** fator
de redução específico — um passo que projetistas sabidamente pulam porque omiti-lo é
conservador. Não é "80% das tarefas são feitas por atalho". O que transporta é a **estrutura**
e a **ordem de grandeza relativa** entre omissão e comissão, não o valor.

**E o defeito A-14 permanece de pé por conta própria:** a rota de fuga nunca executa porque
`0,50 > 0,60` é falso por construção. Isso é defeito independentemente de fonte externa.

---

## 2. O qualificador dos 20–50% — e uma divergência que achei na Tabela 3

A crítica está certa: a frase correta é *"na HRA estrutural analisada por Stewart,
incorporar heterogeneidade ou dependência elevou a probabilidade de falha em cerca de
20–50% em relação à hipótese independente"*, não uma lei geral.

**Mas a Tabela 3 (p. 177) não sustenta bem nem essa versão.** Os valores publicados:

| Procedimento | Binomial | Beta-binomial | p-dependente |
|---|---:|---:|---:|
| 'Design code' | 4,14 × 10⁻⁵ | 5,95 × 10⁻⁵ | 8,04 × 10⁻⁵ |
| 'Safe load tables' | 3,26 × 10⁻⁵ | 4,14 × 10⁻⁵ | 6,87 × 10⁻⁵ |

Razões que eu calculei:

| | Beta-binomial | p-dependente |
|---|---:|---:|
| 'Design code' | **+43,7%** | **+94,2%** |
| 'Safe load tables' | **+27,0%** | **+110,7%** |

O texto diz "approximately 20–30% and 50%". A tabela dá **+27% a +44%** para a beta-binomial
e **+94% a +111%** para a p-dependente. O texto atribui as re-análises a um conjunto mais
amplo de tarefas que o da Tabela 3, o que pode explicar a diferença — mas **cite a tabela,
não a frase**, e diga qual procedimento.

---

## 3. A ancoragem corrigida, para entrar no texto

> A probabilidade basal de erro por atividade é ancorada em Stewart & Melchers (1988,
> Tabela 1, p. 290), que mede taxas de erro de engenheiros civis profissionais em
> microtarefas de projeto estrutural. As taxas publicadas para cálculos de 1, 2, 3, 4, 5 e 8
> passos guardam relação linear exata com o número de passos, `p(k) = k × 0,0128`, cobrindo
> a faixa `[0,0128 ; 0,1024]`. Dois dos cinco valores varridos de `F_ancora` (0,05 e 0,10)
> caem nessa faixa observada e correspondem a atividades de aproximadamente 4 e 8 passos
> elementares. Os valores de 0,15 a 0,25 exigem extrapolação além do maior número de passos
> publicado e são tratados como **cenário de sensibilidade**, não como valor ancorado. A
> extrapolação é conservadora em rótulo e não em mecanismo: a linearidade é a aproximação de
> primeira ordem da composição por independência, hipótese que Stewart (1992, Tabela 2,
> p. 175) rejeita para estes mesmos dados.

---

## 4. O que muda na lista de itens novos do parecer 35

| Item | Situação após esta revisão |
|---|---|
| **N1** — ancorar `F_ancora` | **Mantido, com o recorte de R-11**: ancorado só em 0,05 e 0,10; o resto é sensibilidade declarada |
| **N2** — heterogeneidade entre agentes, CV = 1,13 | **Mantido integralmente.** É o achado mais limpo dos três textos |
| **N3** — sensibilidade à independência, φ = 0,845 | **Mantido**, com o qualificador de que o efeito de 20–50% é daquela HRA, e citando a Tabela 3 |
| **N4** — rota de fuga | **Reformulado.** Continua prioridade máxima pelo defeito A-14, mas a justificativa externa vem de Ball e White, não de Stewart. As taxas de Stewart vão para a **Porta 1** |
| **N5** — cenário com `R_error·(1−μ_cog) = 0` | **Mantido**, com justificativa corrigida: ausência de evidência de campo, não demonstração de efeito nulo |

**Item novo:**

### N6 · A ponte J60 → k continua aberta, e é aqui que a síntese entra

Eu disse no parecer 35 que a autorização de síntese "não é mais necessária para o G-02".
**Errado, pela mesma razão do R-11.** O que fechou foi o segundo elo — `k passos → p_erro`,
com regra publicada dentro de k = 1…8. O primeiro elo — **`nível de atividade J60 → k`** —
continua sem fonte, porque ninguém publica quantos passos elementares tem uma atividade
abstrata do PSPLIB.

É exatamente ali que a permissão do orientador serve, e com uma restrição a mais que vem
desta revisão: **a decomposição sintética deve preferencialmente cair dentro de k ≤ 8**, onde
há dado. Acima disso, cenário de sensibilidade rotulado.

---

## 5. Créditos à crítica

As três correções estão certas e duas delas eu não teria achado sozinho relendo o meu próprio
parecer. Em particular a de Stewart e a pressão — confundir manipulação falha com efeito nulo
é erro de inferência, não de leitura, e é o tipo que passa despercebido justamente porque a
conclusão *parecia* reforçar o que as outras fontes já diziam.

Registro também o padrão: esta é a segunda vez que uma verificação minha exagerou na direção
de uma conclusão que eu já esperava — a primeira foi o "46% está fora de qualquer leitura
razoável" (R-02). Vale como aviso para o resto do trabalho.
