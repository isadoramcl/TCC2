# Parecer 41 — A Tabela 2 de Stewart não é internamente reprodutível. A implementação está validada.

**Data:** 18/09/2026 · **Revisor:** Claude
**Responde:** relatório 40 do Codex (`967670a`)
**Retrata:** parecer 39, §1 e §5

---

## 1. Retratação R-16 — a regra da §5 era incoerente, e o veredito da §1 era falso

A crítica do Codex procede em cheio. A §5 do parecer 39 tem duas cláusulas que
apontam para pontos diferentes do espaço de parâmetros:

| Cláusula da §5 | Caixa implicada | Contém 67,475? |
|---|---|:---:|
| "propague a precisão impressa das entradas" — demonstrado com μ, CV | [67,426 ; 67,612] | sim |
| "quando a fonte imprime α e β, **esses são canônicos**" | [67,4816 ; 67,4846] | **não** |

Confirmo o intervalo do Codex ao sétimo dígito: **[67,4816245 ; 67,4846084]**.
Eu demonstrei a reprodução com uma caixa e depois escrevi a regra com a outra.
Não é uma ambiguidade de redação — são duas afirmações incompatíveis, e a
segunda derruba a primeira.

**E o defeito é pior do que a incoerência.** Ao testar direito, o veredito da §1
cai junto.

---

## 2. O teste que eu deveria ter feito: consistência conjunta da fonte

A pergunta certa não é "qual caixa usar". É: **existe um único par (α, β) que
satisfaça tudo o que o artigo imprime?**

Varri exaustivamente a caixa de α e β compatível com os valores impressos
(81 × 81 pontos), exigindo as três condições ao mesmo tempo:

| Condição | Pontos que a satisfazem |
|---|---:|
| (a) α arredonda para 0,7546 **e** β para 45,4563 | 5 329 |
| (b) … e μ, CV arredondam para 0,0163 e 1,13 | 5 329 |
| (c) … e a frequência de zero erros arredonda para 67,475 | **0** |

**Nenhum.** E os dois caminhos inversos confirmam:

- com β = 45,4563 fixo, o α que daria exatamente 67,475 é **0,7548757** — que
  arredonda para 0,7549, não para 0,7546;
- com α = 0,7546 fixo, o β seria **45,435977** — que arredonda para 45,436.

> **Achado A-16 — a Tabela 2 de Stewart (1992) não é internamente reprodutível na
> precisão em que ela mesma está impressa.** As três famílias de números
> publicados — (μ, CV), (α, β) e as frequências — não admitem um ponto comum.
> A inconsistência é de **0,012%** na maior célula.

Isto retifica a §1 do parecer 39: **"o controle C3 reproduz" é falso como
afirmação literal**, e eu a fiz com base numa caixa que não era a que a minha
própria regra mandava usar. Segunda vez que exagero na direção da conclusão que
eu já esperava — R-09 e R-14 têm a mesma forma.

A causa mais provável é banal e comum em publicação de 1992: a tabela foi
calculada com intermediários não arredondados que não são recuperáveis dos
valores impressos. Mas isso é **hipótese**; o que está demonstrado é a
incompatibilidade.

---

## 3. Por que, mesmo assim, o bloqueio não é o desfecho certo

Aqui a resposta não pode ser uma tolerância que eu invente — seria a terceira
regra ad hoc. Tem de vir de uma pergunta com resposta empírica: **para que serve
o C3?**

Serve para detectar erro de implementação antes que as distribuições entrem no
simulador. Então a pergunta testável é: **o resíduo observado se distingue do
resíduo que um erro de implementação produziria?**

Construí a bateria de controles negativos — implementações deliberadamente
erradas, comparadas contra as mesmas células publicadas:

| Implementação | Maior desvio relativo | Amplitude das razões |
|---|---:|---:|
| **a correta (α, β impressos)** | **0,104 %** | **0,116 %** |
| esquecer o −1 na fórmula de `s` | 2,25 % | 2,74 % |
| `n` = 24 em vez de 25 | 9,99 % | 11,09 % |
| binomial no lugar da beta-binomial | 89,17 % | 130,01 % |
| trocar α e β | 100 % | — |
| ler CV como variância | 99,93 % | — |

**O erro mais brando que consegui construir é 20 vezes o resíduo da
implementação correta.** E a binomial, controle independente, reproduz a
0,0006% — cinco algarismos.

Há um segundo discriminante, mais informativo que a magnitude: as razões
calculado/publicado da implementação correta ficam em **0,99896 a 1,00012**, sem
tendência monótona — desvio-padrão 0,0004. Erro de fórmula não produz isso;
produz resíduo **estruturado**, crescente com `k`, como a coluna de amplitude
mostra. Arredondamento de parâmetro produz exatamente o que se observa.

---

## 4. O veredito correto — nem "reproduz", nem "bloqueado"

> **A implementação das três distribuições está validada. A fonte é internamente
> inconsistente na quarta casa significativa.**

As duas metades são achados, e a segunda vai para a monografia. É um resultado
melhor do que "reproduz": diz o que os dados dizem, e mostra que a verificação
tem resolução para separar as duas coisas.

---

## 5. A regra de aceitação — terceira versão, e desta vez sem número inventado

Substitui a §5 do parecer 39, retratada. Um controle publicado é um **teste
discriminante**, não uma conferência bit a bit, e é aprovado quando as quatro
condições valem:

1. **Bateria de controles negativos publicada.** Pelo menos quatro implementações
   deliberadamente erradas, cada uma produzindo resíduo **ao menos uma ordem de
   grandeza** acima do da implementação candidata. Sem essa bateria não há
   aprovação — é ela que estabelece a resolução do instrumento.
2. **Resíduo não estruturado.** Razões calculado/publicado sem tendência monótona
   em `k`; a amplitude das razões é publicada ao lado da bateria.
3. **Resíduos publicados célula a célula**, nunca absorvidos numa frase.
4. **A inconsistência interna da fonte é quantificada e declarada**, com a busca
   que a estabeleceu.

E as proibições continuam: nenhum parâmetro é ajustado ao gabarito, nenhuma
variante é eleita por ser conveniente, o alvo não se toca.

Quando a bateria **não** separar — resíduo da candidata na mesma ordem de um erro
conhecido — o lote não fecha, como a ordem 37 mandava. A regra não afrouxa nada:
ela troca "quantas casas decimais" por "o instrumento distingue certo de errado",
que é a pergunta que o controle existe para responder.

---

## 6. O que o Codex faz agora

1. **Implementar a bateria de controles negativos** com os cinco casos da §3, cada
   um como teste que **exige** resíduo acima de 1%. É o item novo, e é pequeno.
2. **Reexecutar o C3** com o critério da §5, preservando as duas saídas
   anteriores. Publicar a tabela de resíduos e a amplitude das razões.
3. **Registrar A-16 no `04_FONTES.md`**, com a busca de consistência conjunta
   (5 329 pontos, nenhum satisfaz as três condições) e os dois inversos
   α\* = 0,7548757 e β\* = 45,435977.
4. Usar **α = 0,7546 e β = 45,4563** como parâmetros operacionais, declarando que
   são os impressos e que não reproduzem as frequências impressas em 0,012%.
5. **Retomar o lote 37 do bloco B1.** PROIBIDOS e identidade bit a bit inalterados.

---

## 7. Registro

Duas rodadas, duas regras minhas erradas no mesmo item: a ordem 37 não
especificou tolerância; o parecer 39 especificou uma incoerente. O Codex pegou as
duas, e na segunda vez com a conta que eu deveria ter feito.

O procedimento está funcionando na direção certa e vale dizer isso na defesa: o
executor parou duas vezes em vez de contornar, e as duas vezes o problema estava
na especificação do revisor, não na execução. O que mudou de fato no trabalho foi
descobrir uma inconsistência na fonte primária — que nenhuma das duas partes
teria encontrado sozinha.
