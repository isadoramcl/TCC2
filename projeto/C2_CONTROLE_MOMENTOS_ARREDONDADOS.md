# C2 — controle de precisão incompatível com entradas arredondadas

**Item interrompido antes de introduzir heterogeneidade no simulador.**
A política do lote manda registrar observado versus esperado quando um controle
publicado reprova; não ajustar parâmetros ou tolerância para fazê-lo passar.

## Resultado literal da fórmula prescrita

| Parâmetro | Calculado com mu=0,0163; CV=1,13 | Impresso | Diferença |
|---|---:|---:|---:|
| alpha | 0,754081392435 | 0,7546 | −0,000518607565 |
| beta | 45,508580720130 | 45,4563 | +0,052280720130 |

Não coincidem na terceira casa, critério da ordem37. O lote noturno usava
"aproximadamente", sem definir um critério substituto; não inventar tolerância
após observar o resultado. A fórmula não foi modificada.

A biblioteca SciPy confirma que os parâmetros calculados têm exatamente os
momentos solicitados. Já os parâmetros impressos implicam
mu=0,016329480707 e CV=1,129581318086: estes **arredondam** para0,0163 e1,13.
Logo não é nova prova de inconsistência da fonte: entradas arredondadas não
permitem recuperar parâmetros com mais precisão. A-16 tratava a consistência
com as frequências da tabela; não confundir os dois achados. Os parâmetros
operacionais de C3 (0,7546;45,4563) permanecem intocados.

## Domínio, sem sorteios nem ajuste de CV

A Beta própria requer **0<mu<0,439193640476086**, desigualdade estrita.
No extremo a concentração t=0, fora da Beta não degenerada. O helper rejeita
limites/NaN com mensagem explícita; não reduz CV. Camada NASA histórica:

| F_ancora | Nível | F_base inválido |
|---:|---|---:|
| 0.15 | muito_alta | 0.447750 |
| 0.20 | alta | 0.473400 |
| 0.20 | muito_alta | 0.597000 |
| 0.25 | media | 0.483750 |
| 0.25 | alta | 0.591750 |
| 0.25 | muito_alta | 0.746250 |

A grade completa de admissibilidade está em `dominio_celulas.csv`.
Não houve sorteio de agentes, verificação empírica de momentos, implantação de
`heterogeneidade_erro` ou contraste dinâmico: dependem de resolver a porta de
controle primeiro. Esses passos permanecem pendentes, não aprovados por omissão.

## Verificação e próximo passo

`c2_precontrole.py` encerrou com código1 e publicou os resíduos, sem absorvê-los
num veredito verbal. Três testes da fórmula/domínio/momentos impressos passaram;
eles verificam a matemática, **não fazem passar o controle publicado reprovado**.
Identidade neutra permanece passando. Não usar "todos os testes passaram" para
esconder esta reprovação científica.

É necessário reconciliar o critério C2: comparar momentos na precisão publicada
ou explicitar outro contrato numérico antes de liberar a alternativa. Não houve
redefinição unilateral do alvo. Saídas em `outputs/diagnosticos/C2_20260919/`.
