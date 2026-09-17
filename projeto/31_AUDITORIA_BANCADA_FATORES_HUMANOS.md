# Parecer 31 — Auditoria da bancada de fatores humanos

**Data:** 17/09/2026 · **Revisor:** Claude
**Objeto:** `bancada-fatores-humanos` (relatório, scripts e `resultados/`), produzida em conversa paralela
**Método:** recomputação independente a partir dos CSV publicados e leitura do código

---

## 1. Veredito

Trabalho de qualidade alta. A disciplina é a certa: cada fonte traz a linha do que **não**
sustenta, há uma seção inteira de "o que NÃO fazer com isso", nada foi inserido no
simulador, e os detalhes que **teriam** quebrado cada ponte estão listados — inclusive
dois que efetivamente ocorreram e foram corrigidos.

Recomputei o que era recomputável. Confere, com duas ressalvas de documentação (§3) e
uma objeção conceitual que muda o peso do principal achado (§4).

## 2. Verificação independente

| Afirmação | Recomputado por mim | Veredito |
|---|---|---|
| corr(taxa INC, não-marcações avaliadas/jogo) = −0,77 | **−0,7681** | confere |
| corr(INC/jogo, não-marcações avaliadas/jogo) = −0,17 | **−0,1733** | confere |
| Dupla falta sob break point: −1,06 p.p. | recalculei dos agregados: 0,2771 → 0,2665 = **−1,06 p.p.** | confere |
| Curva de dificuldade plana do 2º ao 15º golpe | 10,3% / 9,1% / 10,2% / 9,7% / … / 9,1% | confere |
| 87,1% dos erros são omissões | bate com `omission_share_of_errors = 0,871` | confere |

A verificação do parser de tênis contra os agregados oficiais do projeto (62,55% × 62,21%;
10,34% × 10,34%) é o tipo de controle que quase ninguém faz e que dá credibilidade ao resto.

### O achado da NBA sobrevive ao meu escrutínio

A taxa de omissão cai 74,7% (0,2055 → 0,0519) enquanto o **numerador por jogo** cai só
62,4% (1,655 → 0,622) e o **denominador por jogo** sobe de 8,05 para 19,27 e volta a 11,97.
A taxa acompanha o denominador (r = −0,77); o numerador não (r = −0,17). A conclusão —
**quem decide o denominador é quem audita, não quem executa** — está sustentada.

Isso é o análogo externo direto de `p_reporte` e `p_deteccao`, e corrobora empiricamente
o que a decomposição T2 do parecer 24 já tinha mostrado por dentro do modelo: 97,5% do
contraste de `taxa_omissao` é a premissa de reporte. **Duas evidências independentes, uma
interna e uma de campo, apontando para a mesma coisa.** É material forte de discussão.

## 3. Duas ressalvas de documentação — corrigir antes de virar apêndice

### 3.1 `taxa_reversao_pct` não é o que o rótulo sugere

O relatório diz *"Taxa de reversão: 1,06% dos commits"* e, na frase seguinte, *"De 579
reversões, 496 alvos foram identificados"*. O leitor calcula 579/67.313 = **0,86%** e não
chega a 1,06%. Pelo recorte 2015+, 574/45.859 = **1,25%**. Nenhum dos dois é 1,058%.

O código explica: linha 79, `taxa_reversao_pct = 100 * base.reverted.mean()`. A grandeza é
a **proporção de commits que FORAM revertidos** (alvos), não a proporção de commits **que
são reversões**. E `base` é a amostra de regressão, cujo tamanho não é publicado — a taxa
implica um denominador de ≈ 46,9 mil, que não aparece em tabela nenhuma.

Não invalida nada (todos os efeitos do T3 são nulos de qualquer modo). Mas um número de
apêndice que não se reproduz das tabelas publicadas é exatamente o que um avaliador cutuca.
**Correção:** renomear para "proporção de commits revertidos" e publicar o tamanho de `base`.

### 3.2 A tabela de tênis mistura denominadores sem avisar

Em `t2_tenis_medias_breakpoint.csv`, `double_fault` é sobre **todos os pontos** (0,1035 e
0,1020, diferença de −0,15 p.p.). Na tabela do relatório, o efeito é **dado 2º saque**
(−1,06 p.p.). Os dois estão certos e eu reconciliei os dois — mas quem comparar as tabelas
vai achar que há erro de fator 7. **Correção:** rotular a coluna do CSV como
`double_fault_por_ponto` e dizer na tabela que o efeito é condicionado ao 2º saque.

## 4. A objeção que muda o peso do principal achado: Reichelt & Lyneis e o G-01

O relatório trata Reichelt & Lyneis (1999) como o comparador de retrabalho **em esforço**
que faltava ao G-01 — 48% das horas de projeto (30–65%) e 24% das horas de execução
(13–40%), sobre horas totais, em aeroespacial, construção naval e civil. E converte o
indicador do modelo para o denominador deles: `TR/(E_plano+TR)` = **19–22%**, dentro da
faixa de execução.

**Unidade certa, domínio certo.** É melhor que Boehm & Basili, que é software.

E o relatório já declara as duas fragilidades certas: os números são saídas de modelos de
Dinâmica de Sistemas calibrados, alguns *"in preparation for litigation"*; e a amostra é de
clientes de consultoria, projetos pioneiros, com estouro médio de orçamento de 86%.

**Falta declarar a terceira, que é a mais séria.** Reichelt e Lyneis pertencem à mesma
linhagem de modelagem de projeto por Dinâmica de Sistemas em que este TCC se inscreve — a
mesma de Rodrigues e do SYDPIM, já catalogado em `04_FONTES`. Então comparar o retrabalho
deste modelo com os 48%/24% deles **não é comparar modelo com mundo: é comparar modelo com
modelo**, de famílias aparentadas.

Isso não elimina o uso. Reposiciona:

- **Não é** ancoragem empírica, e não fecha o G-01 no sentido forte.
- **É** uma verificação de consistência com a literatura estabelecida de modelagem de
  projeto — "o retrabalho que este simulador produz está na ordem de grandeza que os
  modelos calibrados da área produzem". Isso vale, e é escrevível.

A frase que entra na monografia tem de dizer as três coisas: mesma unidade, mesmo domínio,
**e** saída de modelo calibrado da mesma família — não medição independente.

### 4.1 Um achado secundário que talvez valha mais que o principal

O relatório registra, como "bônus", que Reichelt & Lyneis reportam degradação média de
qualidade de **0,95 por pressão de cronograma** e **0,97 por fadiga de hora extra**, com
qualidade média de projeto de 0,33.

Esses são **multiplicadores de degradação** — exatamente a grandeza do `μ_cognitivo` e do
`μ_rede` deste modelo, cujo piso `mu_minimo` é hoje parâmetro `aberto` e varrido. Vale
testar se a faixa varrida é compatível com 0,95 e 0,97 como valores médios. Se for, é um
**segundo parâmetro ganhando interpretação externa**, junto com o `F_ancora` do Stewart.

Com a mesma ressalva do §4: saída de modelo calibrado, não medição.

## 5. O desafio ao construto P — e a peça que faltava

O achado mais desconfortável da bancada: **nenhuma base de campo com efeito fixo sustentou
"mais pressão → mais erro"**. O tênis deu o sinal **oposto** (−0,59 p.p. em erro não
forçado e −1,06 p.p. em dupla falta sob break point); NBA e Go deram nulo.

O relatório resolve corretamente: *"pressão não é um construto só"*. No tênis a pressão é
**importância do ponto**, não escassez de tempo. O `P` do modelo é pressão de prazo e carga.

**A peça que completa isso está no parecer 30**, e nenhuma das duas análises tinha as duas
metades. Payne, Bettman & Luce (1996, OBHDP 66(2):131–152) manipulam pressão por **custo de
oportunidade do tempo** — o sujeito escolhe quanto tempo gastar — e encontram aceleração
forte: aquisições de informação caem de 24,6 para 15,4 (p < 0,0001).

Juntando:

| Tipo de pressão | Efeito observado | Fonte |
|---|---|---|
| Importância do que está em jogo | **mais cautela**, menos erro | tênis (bancada) |
| Custo de oportunidade do tempo | **aceleração**, menos processamento | Payne, Bettman & Luce (1996) |
| Prazo de release "macio" | nulo | Go (bancada) |
| Escopo de auditoria | não é pressão — fabrica a métrica | NBA (bancada) |

As duas linhas não se contradizem: elas mostram que o rótulo "pressão" cobre construtos com
sinais opostos. **O modelo precisa dizer qual deles o seu `P` representa** — e a resposta
honesta é pressão de prazo e carga, que é o construto do meio, para o qual só há suporte
de aceleração, não de erro.

## 6. Recomendações

1. **Rodar o cenário de sensibilidade com efeito de P sobre o erro igual a zero** (item 2
   dos próximos passos da bancada). É o teste certo, é barato, e responde à objeção antes
   que ela seja feita. Se as conclusões centralizado × adaptativo sobreviverem, o capítulo
   fica muito mais forte; se não sobreviverem, é melhor saber agora.
2. **Corrigir as duas ressalvas de documentação** (§3) antes de a bancada virar apêndice.
3. **Registrar Reichelt & Lyneis (1999) em `04_FONTES`** com a linha do que não sustenta
   incluindo a objeção do §4: saída de modelo calibrado da mesma linhagem.
4. **Testar a faixa de `mu_minimo`** contra os multiplicadores 0,95 e 0,97 (§4.1).
5. **Sim, isto entra como apêndice exploratório** da monografia. Uma seção que testa pontes
   com dados reais e conclui que três das quatro não se sustentam é evidência de rigor, não
   de fracasso. E o achado da NBA sobre o denominador da auditoria é bom demais para ficar
   em nota interna — corrobora de fora o que a decomposição T2 mostrou por dentro.
6. **Lichess continua sendo a base certa para o G-03** e vale a tentativa na máquina da
   autora: o jogador escolhe quanto tempo gasta, a pressão é tempo de relógio, a dificuldade
   é medida por motor e o erro é objetivo. É a única das quatro em que todos os construtos
   se alinham ao modelo.
