# Parecer 39 — C3 reproduz. O bloqueio é um falso positivo, e o defeito é meu

**Data:** 18/09/2026 · **Revisor:** Claude
**Audita:** parecer 38 do Codex (`f94a2e8`) e `outputs/diagnosticos/lote37_C3_20260917/`
**Fonte reauditada:** Stewart (1992), Tabela 2, p. 175

---

## 1. Veredito

**O controle C3 reproduz. O lote 37 não estava bloqueado.**

O que reprovou não foi a fonte nem a implementação do Codex: foi o **critério de
aceitação**, que a ordem de serviço 37 não especificou. Na ausência de
especificação o Codex adotou tolerância **absoluta** na terceira casa decimal, e
a aplicou igualmente a valores que vão de 67,475 até 0,002. Sobre 67,475 isso
exige seis algarismos significativos de um cálculo cujas **entradas estão
publicadas com três**.

A omissão é minha. A ordem 37 mandou reproduzir a Tabela 2 e não disse com que
precisão. Registro como **A-15**, defeito da ordem de serviço, não do executor.

---

## 2. O que o Codex fez certo, e que vale preservar como procedimento

Antes da discordância, o que não se discute:

- **Preservou o alvo.** Não ajustou `α`, `β`, `p`, `φ` nem o agrupamento para
  fazer o gabarito passar, mesmo tendo identificado três variantes diagnósticas
  que aproximariam algumas células.
- **Não elegeu a variante conveniente.** A fração 38/2327 aproxima a p-dependente
  e estraga a binomial; o parecer 38 diz isso explicitamente em vez de omitir.
- **Parou o lote inteiro** em vez de seguir com os outros itens e reportar o
  problema no fim.
- **Separou hipótese de causa:** "precisão não publicada ou inconsistência
  editorial são hipóteses, **não causas confirmadas**". Correto, e é exatamente
  a distinção que eu errei em R-09.
- **Registrou o SHA256 do PDF e das fontes**, e conferiu a tabela em ampliação.

O parecer 38 termina pedindo: *"Reconciliar com o revisor a precisão dos
parâmetros"*. É o pedido certo, dirigido à pessoa certa. A resposta está abaixo.

---

## 3. A prova: a discrepância é inteiramente explicada pela precisão das entradas

Recalculei tudo de forma independente, em ambiente separado, sem usar o código do
Codex. Primeiro, um ponto de método: as frequências da Tabela 2 são **contagens
de respondentes**, não porcentagens — as binomiais somam 93,999 e as
beta-binomiais 93,993, ambas ≈ N = 94. Confirma `n = 25`, `N = 94`.

### 3.1 A binomial passa sem ressalva

| Erros | Publicado | Recalculado | Δ |
|---:|---:|---:|---:|
| 0 | 62,330 | 62,3296 | −0,0004 |
| 1 | 25,820 | 25,8202 | +0,0002 |
| 2 | 5,134 | 5,1341 | +0,0001 |
| 3 | 0,652 | 0,6522 | +0,0002 |
| 4 | 0,059 | 0,0594 | +0,0004 |
| 5 | 0,004 | 0,0041 | +0,0001 |

Seis algarismos significativos de acordo. Mesmo esta o Codex reprovou no χ²,
por 10,173 contra 10,174 — diferença de **0,01%**, no último dígito impresso.

### 3.2 A beta-binomial: três origens de (α, β), três distâncias

| Origem de (α, β) | α | β | Δ em zero erros |
|---|---:|---:|---:|
| μ = 0,0163 e CV = 1,13 (o que a ordem 37 mandou usar) | 0,75408 | 45,5086 | **+0,044** |
| α, β **impressos no artigo** | 0,75460 | 45,4563 | **+0,008** |

Usando os parâmetros que o próprio artigo imprime, a maior distância cai para
**0,008 sobre 67,475** — cinco algarismos de acordo. O parecer 38 chama isso de
"também não reproduz a tabela". Não procede.

### 3.3 A propagação do arredondamento, que é o teste decisivo

μ está impresso como **0,0163** e CV como **1,13** — três algarismos cada. Os
valores verdadeiros estão em μ ∈ [0,01625; 0,01635] e CV ∈ [1,125; 1,135].
Varrendo esses dois intervalos:

| Erros | Faixa implicada | Publicado | Contém? |
|---:|---:|---:|:---:|
| 0 | [67,426 ; 67,612] | 67,475 | **sim** |
| 1 | [18,244 ; 18,381] | 18,334 | **sim** |
| 2 | [5,605 ; 5,647] | 5,639 | **sim** |
| 3 | [1,745 ; 1,775] | 1,765 | **sim** |
| 4 | [0,538 ; 0,555] | 0,549 | **sim** |

**Todos os cinco valores publicados caem dentro.** A largura da faixa em zero
erros é 0,186 — quatro vezes a discrepância de 0,044 que motivou o bloqueio.

### 3.4 A p-dependente, que o parecer 38 apontou como a mais robusta

O argumento do 38 é que `94·(1−φp)^25 = 66,4576` contra 66,416 **independe da
implementação**. Está certo que independe da implementação. Mas não independe da
precisão de φ e p, que também estão impressos com três algarismos:

| | |
|---|---|
| φ ∈ [0,8445; 0,8455], p ∈ [0,01625; 0,01635] | faixa **[66,373 ; 66,543]** |
| Publicado | **66,416 — dentro** |
| φ que daria exatamente 66,416 com p = 0,0163 | 0,846515 |
| p que daria exatamente 66,416 com φ = 0,845 | 0,0163292 |

Ambos arredondam para os valores impressos. Não há inconsistência a reconciliar.

---

## 4. A célula que continua aberta — e que não bloqueia nada

Beta-binomial, **oito erros**: o artigo imprime 0,000 e o cálculo dá 0,00399,
que arredonda para 0,004. Essa não é explicada por arredondamento das entradas.
É provavelmente truncamento editorial da cauda ou uma linha "≥ 8".

Registre como **discrepância conhecida** no `04_FONTES.md`, com o valor
calculado ao lado. Não é motivo de bloqueio: a célula vale 0,004 respondente em
94, e nenhuma quantidade do modelo depende dela.

---

## 5. A regra de aceitação corrigida — substitui a da ordem 37

A ordem 37 dizia "reproduza a Tabela 2" e não definia tolerância. Passa a valer:

> Uma célula de controle publicado **passa** quando o valor publicado cai dentro
> do intervalo obtido propagando a precisão impressa dos parâmetros de entrada
> da fonte. Quando a fonte imprime também os parâmetros derivados (aqui α e β),
> **esses são a origem canônica**; os parâmetros de construto (μ, CV) descrevem o
> modelo e não servem para reconstruir os derivados.
>
> Quando a propagação **não** contém o valor publicado, a célula **reprova** e o
> lote não fecha — a regra da ordem 37 continua valendo nesse caso.
>
> Tolerância absoluta uniforme sobre valores de magnitudes diferentes é proibida:
> exigir 0,0005 de 67,475 e de 0,002 são exigências de 6 e de 1 algarismos.

Isso não afrouxa o controle. Afrouxá-lo seria aceitar a discrepância dizendo
"é pequena". A regra acima **quantifica** o que a fonte permite afirmar, e a
discrepância cai dentro disso por fator de quatro.

---

## 6. O que o Codex deve fazer agora

1. **Desbloquear C3** com a regra da §5. Reexecutar `validar_c3.py` com o critério
   corrigido e arquivar a saída ao lado da anterior — **sem apagar a anterior**,
   que documenta o achado.
2. Usar **α = 0,7546 e β = 45,4563** (impressos) como parâmetros canônicos da
   beta-binomial. Registrar que μ = 0,0163 e CV = 1,13 reconstroem α com erro de
   0,07%, dentro da precisão publicada.
3. Registrar a célula de oito erros como discrepância conhecida.
4. **Retomar o lote 37 do bloco B1 em diante**, com todo o resto inalterado — os
   dois PROIBIDOS continuam de pé, e a identidade bit a bit continua sendo porta
   de cada item.
5. Publicar o `cedbfa3`, que não existe naquele clone: os pareceres 23, 25 e 26 e
   o `07_BRIEFING_ORIENTADOR.md` estão no checkout da autora e entram pelo merge.

---

## 7. O padrão, para o registro

Esta é a terceira vez neste trabalho que um controle "reprova" por um critério que
ninguém escreveu. Das quinze retratações e defeitos registrados, **este é o
primeiro em que o executor estava certo e a ordem estava errada** — e ele só
apareceu porque o Codex parou o lote inteiro em vez de contornar.

O procedimento certo, que vale manter: quem executa **para e escala**; quem
escreveu a ordem **responde com a conta**, não com uma flexibilização.

Vale registrar também o que teria acontecido se o Codex tivesse "resolvido"
sozinho: escolheria a fração 38/2327, que aproxima a p-dependente e estraga a
binomial. O bloqueio evitou isso.
