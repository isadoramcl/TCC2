# 40 — Aplicação da regra do parecer 39: incompatibilidade remanescente

18/09/2026. Base atualizada por `git pull origin main`: `f726861`.
O pull trouxe o parecer 39, o briefing 07 e os pareceres 23/25/26.

## Resultado

**C3 permanece sem aprovação pela seção 5 do parecer 39. B1 não foi iniciado.**
A regra antiga não foi reaplicada como critério vigente. Alpha=0,7546 e
beta=45,4563 são agora canônicos. A saída anterior de 17/09 foi preservada,
e BB8 foi registrada como exceção conhecida, conforme autorização explícita.

A seção 5 exige propagação da precisão dos parâmetros impressos e elege os
parâmetros derivados impressos como origem canônica. Isso implica:

- alpha ∈ [0,75455; 0,75465]; beta ∈ [45,45625; 45,45635];
- p ∈ [0,01625; 0,01635]; phi ∈ [0,8445; 0,8455].

Como solicitado, mu=0,0163 e CV=1,13 reconstroem alpha=0,7540813924,
com diferença relativa de aproximadamente 0,069% frente a 0,7546. Essa
compatibilidade aproximada do construto não define a incerteza dos parâmetros
canônicos impressos.

O intervalo mais amplo de mu/CV mostrado no §3.3 do parecer 39 **não é o
intervalo dos alpha/beta canônicos**. Escolher este intervalo mais amplo para
aceitar a tabela mudaria a origem da incerteza prescrita na seção 5.

## Contraexemplo decisivo, independente de caudas ou chi²

Para zero erros na beta-binomial:

`E0 = 94 * produto((beta+i)/(alpha+beta+i), i=0..24)`.

Cada fator diminui com alpha e aumenta com beta. Logo os extremos exatos no
retângulo impresso são obtidos nos dois cantos opostos; não é estimativa de
Monte Carlo nem resultado de otimização.

- Central canônico: **67,483116433**.
- Intervalo propagado: **[67,481624506; 67,484608392]**.
- Publicado: **67,475**; fora do intervalo.
- Mesmo tratando o publicado como arredondado em [67,4745;67,4755], os
  intervalos continuam disjuntos.

Portanto o bloqueio remanescente não depende de exigir precisão infinita da
saída impressa, nem da exceção BB8. A diferença de 0,008 não é aceita apenas
por ser pequena: é necessário um intervalo de entrada que a explique, conforme
a própria regra nova.

## Outras células BB e chi²

| Célula | Publicado | Canônico | Limite inferior | Limite superior | Compatível com arredondamento da saída? |
|---|---:|---:|---:|---:|---|
| 0 erros | 67.475 | 67.483116433 | 67.481624506 | 67.484608392 | não |
| 1 erros | 18.334 | 18.329064340 | 18.328241861 | 18.329886775 | não |
| 2 erros | 5.639 | 5.637495972 | 5.637078241 | 5.637913703 | não |
| 3 erros | 1.765 | 1.764935557 | 1.764771436 | 1.765099684 | sim |
| 4 erros | 0.549 | 0.548427293 | 0.548368580 | 0.548486010 | não |
| 5 erros | 0.167 | 0.167313461 | 0.167293662 | 0.167333262 | sim |
| 6 erros | 0.050 | 0.049791980 | 0.049785617 | 0.049798344 | sim |
| 7 erros | 0.014 | 0.014385993 | 0.014384037 | 0.014387950 | sim |
| 8 erros | 0.000 | 0.004018884 | 0.004018309 | 0.004019460 | não |
| χ² | 0.162 | 0.161243389 | 0.161005565 | 0.161481462 | não |

As células 0, 1, 2 e 4 e o chi² continuam incompatíveis mesmo considerando a
precisão da saída. BB8 é exceção conhecida e não causa o bloqueio. A inclusão
literal também reprova algumas células pequenas que simplesmente arredondam
para o valor publicado (inclusive zeros binomiais); essas reprovações formais
estão explicitadas no CSV, mas **não são a justificativa científica do bloqueio**.
A coluna adicional compara os intervalos propagados com os intervalos de
arredondamento das saídas. Não é uma tolerância uniforme de seis dígitos sobre
o cálculo: cada entrada continua com sua própria precisão propagada.

## Método e verificações

Protocolo anterior: [PROTOCOLO_C3_39](../research/lote37/PROTOCOLO_C3_39.md).
Binomial e BB: sinais das derivadas logarítmicas certificados no retângulo,
seguidos de avaliação dos extremos. P-dependente: recorrência com envoltórias
conservadoras não negativas. Chi²: propagação conservadora dos quatro grupos
0,1,2,≥3. Envoltórias conservadoras não garantem que todos os alvos possam ser
atingidos conjuntamente por um único vetor. A exclusão de E0, porém, é exata.

Seis testes de algoritmo/limites passaram, incluindo cálculo independente de
E0 pela fórmula de produto, comparação com SciPy e inclusão de pontos interiores.
Os três testes de compatibilidade passaram após a alteração, incluindo identidade
bit a bit. O runner científico retorna código 1, `BLOQUEADO_REGRA_39`.
Não houve mudança no simulador, nos parâmetros do nominal, no RNG ou em V_mod.

## Artefatos preservados e reprodução

- [Saída histórica](../outputs/diagnosticos/lote37_C3_20260917/): intacta.
- [Primeira execução da regra 39](../outputs/diagnosticos/lote37_C3_regra39_20260918/): preservada.
- [Saída com diagnóstico adicional de arredondamento](../outputs/diagnosticos/lote37_C3_regra39_20260918_final/): mesma conta, acrescenta coluna diagnóstica.

```sh
python3 research/lote37/validar_c3.py --regra parecer39 --saida /tmp/c3-39-nova
python3 -m unittest discover -s research -p 'test_stewart_c3*.py' -v
python3 -m unittest discover -s research -p test_compatibilidade.py -v
```

A pasta deve ser nova. `--regra historica` conserva a reprodução do critério
antigo; o default é `parecer39`. Os manifests registram hashes do código e das
instruções. Nenhuma saída foi escolhida por favorecer aprovação.

## Reconciliação necessária

O revisor precisa esclarecer qual origem de incerteza governa a aceitação BB:
alpha/beta impressos (regra textual da seção 5) ou mu/CV (intervalos da demonstração
§3.3). Sob a primeira, C3 não passa; não foi substituída pela segunda sem registro
ou autorização. Não afirmar que os parâmetros foram ajustados ou que a causa
editorial está provada. Depois dessa reconciliação, a retomada solicitada é B1.
Os dois PROIBIDOS e a identidade bit a bit permanecem válidos.
