# Estado do trabalho — 06/09/2026

Este documento é deliberadamente pessimista. Ele registra o que está **de pé**,
o que está **quebrado** e o que está **afirmado sem sustentação**. Um estado
otimista seria inútil: o valor está em saber onde não pisar.

## O pipeline

Dezoito scripts, executáveis em sequência, cada um com verificações próprias.

```
src/nasa/      01 auditar → 02 consolidar → 03 validar D'' → 04 modelos
               logísticos → 05 faixas F_base → 06 figuras
src/psplib/    01 auditar J60 → 02 índice Di → 03 transferência ordinal → 04 figuras
src/modelo/    01 derivar parâmetros → simulador.py + fuzzy.py →
               02 verificar → 03 experimento → 04 gêmeo idêntico →
               05 figuras → 06 exportar parâmetros
docs/          gerar_entrega.js  (gera a Entrega 1 a partir dos CSVs)
```

Bases: NASA MDP (17.377 módulos, 12 projetos, versão D″ de Shepperd et al.) e
PSPLIB J60 (480 instâncias, 28.800 tarefas).

## Verificado por auditoria independente

Um revisor externo reimplementou com código próprio e reproduziu:

- toda a camada de dados: F_base por faixa, Wilson, Cochran-Armitage,
  leave-one-project-out, razões de risco e bootstrap, CPM/folga/Di, grade
  NC/RF/RS, SGS (480/480 com razão mínima exatamente 1,0000), validação D″ e
  modelos logísticos;
- todas as tabelas regeradas do zero saem idênticas às publicadas;
- ausência de vazamento entre os braços do experimento pareado;
- o defeito da métrica de retrabalho (`S_UR_final` nulo em 384/384);
- a correção da t-norma difusa (max-min viola com derivada 0,259; produto zera);
- a crista de equifinalidade `F_âncora × f_retrabalho`.

**Isto é a espinha dorsal do trabalho e ela está de pé.** O que segue são
problemas de encanamento e de interpretação, não de substância.

## Quebrado — confirmado, ainda não corrigido

| o quê | evidência |
|---|---|
| `src/nasa/06_figuras.py:191` lê `04_sobrevivencia_ao_controle_de_tamanho.csv`, que **nenhum script gera** | clone limpo quebra o pipeline; a fig3 publicada usa números de uma execução antiga (OR 0,946 / LR 1,73 / p 0,188 contra os atuais 0,944 / 1,92 / 0,166) |
| `figura_10()` está definida **depois** do `if __name__ == "__main__"` | nunca é chamada; a fig10 não se regenera |
| anotações da fig8 são literais e estão vencidas | dizem 30% / 118,2 vs 6,3 / +8,1%; o correto é +44,8% / 126,3 vs 5,9 / +10,4% |
| `requirements.txt` sem scipy, matplotlib e pyyaml | ambiente limpo não roda o modelo |
| onda 2 do History Matching usa **o mesmo RNG** da onda 1 | é reescalonamento afim exato: não avaliou nenhum ponto novo |
| verificação 8 usa Spearman sobre 5 médias | scipy devolve p assintótico 1e-24; o menor p bilateral exato com n=5 é 2/120 = 0,0167 |
| verificação 4 foi trocada por "relógios não negativos" | passa por construção; a original comparava Σ(TW+TL+TU+TR) com o tempo de agente alocado, que hoje dá 891,9 contra 1.426,1 |
| verificações 1, 5, 6, 7, 9 rodam só em `j6010_1` | uma instância, um cenário |
| verificação 9a não restringe nada | passa para todo `F_âncora` de 0,05 a 0,25 |
| 5 parâmetros declarados no YAML nunca são lidos | `defuzzificacao`, `inferencia`, `pesos_Di`, `politica_atribuicao`, `replicacoes`. `pesos_Di` é o pior: o script do Di usa 1/3 fixo no código |
| `retrabalho.p_deteccao: 0.05` é config morta | o simulador lê o `p_deteccao` do cenário |
| `psplib_04_carga_paralela.csv` é órfão | nenhum script o gera |

## Afirmado sem sustentação — precisa cair ou ser provado

Isto é mais grave que bug, porque está escrito como conclusão.

**"As ondas convergiram; o limite é estrutural."** Não se sustenta: a onda 2 era
cópia afim da onda 1. É claro que as larguras não mudaram. A afirmação só volta
a valer se, com desenho independente, elas continuarem estáveis.

**"O experimento isola um mecanismo."** Os dois cenários diferem em **quatro**
parâmetros ao mesmo tempo (`tau_inicial`, `tau_min`, `p_reporte`,
`p_deteccao`). Nenhum efeito pode ser atribuído a um mecanismo sem ablação.

**Taxa de omissão como evidência independente.** A razão observada entre os
braços é 0,2936; a razão mecânica prevista só por `p_reporte` é
(1−0,75)/(1−0,15) = 0,2941. Ou seja, **99,8% da diferença é o parâmetro
reaparecendo na saída**. É *manipulation check*, não achado. Pior: `n_com_erro`
e `taxa_omissao` são a mesma grandeza dividida por 60 — a mesma evidência
aparece duas vezes na tabela.

**Atraso relativo de −36,2%.** O braço centralizado passa 39,1 períodos (16,2%
do makespan) **sem nenhuma tarefa ativa**, só esperando a dívida oculta aflorar,
porque o laço só encerra quando a dívida zera. Medido até a última tarefa
concluída, o atraso é −22,2%. As duas medidas são legítimas, mas só a favorável
está publicada.

**Estatística dos "192 pares".** São 16 instâncias × 12 sementes: as sementes
não são projetos independentes. Refeito com a instância como unidade: 16 de 16
favorecem o adaptativo, p = 3,05e-05 (o mínimo possível para n=16) e os *d*
sobem para 3,07 a 7,82. **A correção fortalece o resultado** — mas os p da
ordem de 1e-33 que estão publicados não são interpretáveis.

**Seleção das instâncias.** `todas[::30][:16]` cobre 16 das 48 células do
fatorial, todas com sufixo `_1`, em passo irregular e não documentado.

**Competência de Crowder.** O código faz a competência subir permanentemente.
Crowder et al. especificam que ela **volta ao valor inicial** a cada subtarefa.
Usamos a fórmula deles dentro de uma dinâmica diferente, sem declarar.

**"Conforme especificado na fase conceitual"**, dito sobre a estrutura do sistema
difuso. O TCC1 não definiu entradas, termos nem regras — a própria especificação
registra isso.

**"Procedimento validado"** para Liu, Triantis e Sarangi. Eles propõem e ilustram.

**Procedência de F_base.** A tabela classifica F_base como calibrado. O que é
calibrado empiricamente é o **RR por faixa**; F_base contém `F_âncora`, que é
aberto. E a partição difusa uniforme (núcleos 0 / 0,5 / 1) está como `[LIT]`:
Van Broekhoven exige *uma* partição, não *aquela* — é `[DEC]`.

## Corrigido nesta rodada

- Matriz de cenários agora é montada de `parametros_cenarios.csv`, que vem do
  YAML. Os valores fabricados saíram.
- Sete referências cruzadas de equação consertadas, e a causa eliminada: o
  gerador resolve por identificador simbólico e **falha a geração** se uma
  citação não resolver.
- Legendas de figura no formato ABNT (identificação acima com travessão, fonte
  abaixo).
- Removida a afirmação falsa de que `p_deteccao` era idêntico entre os cenários,
  e acrescentado o parágrafo declarando que quatro parâmetros variam juntos.
- `src/modelo/06_exportar_parametros.py`: exporta cenários e procedência, e
  detecta parâmetros órfãos e nomes ambíguos entre seções.

## Pendências de decisão da autora

Não são bugs. Mudam o que o modelo afirma, e ela precisa decidir:

1. Retrabalho deve ocupar agente e recurso? (Hoje `TR` é somado sem consumir
   tempo — diverge da especificação e do TCC1.)
2. A simulação encerra na última tarefa ou continua até a dívida zerar?
3. `τ(t)` deve evoluir? (Hoje é constante, e por isso o braço centralizado
   **nunca** concede ajuda: `TL = 0,00`.)
4. A omissão deve custar tempo reduzido, como o TCC1 prevê? (Aqui provavelmente
   quem está errado é o código: sem isso o arquétipo de Soluções Sintomáticas
   não existe no modelo.)
5. O ramo de fuga da Porta 2 é código morto (0 adiamentos em 384 execuções).
   Ativar ou declarar desligado?
