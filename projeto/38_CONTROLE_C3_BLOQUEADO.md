# 38 — C3 bloqueado: controle publicado de Stewart (1992)

## Veredito — 17/09/2026

**O lote 37 não fecha. C3 foi executado primeiro e reprovou o controle publicado.**
Não foram integradas distribuições ao simulador nem iniciados os demais itens da
ordem 37. A ordem 32 não foi usada. Nominal, dinâmica, RNG e V_mod permanecem
inalterados; nenhuma nova onda de History Matching foi executada.

## Publicação e reconstrução do estado

Os documentos 27–37 e o histórico 18 v6 foram recuperados de
`Claude outputs/pareceres_27_a_37.zip`, preservando os arquivos do pacote, e
publicados em `203ecbd`; a exclusão de `Claude outputs/` foi publicada em
`d11d8ec`. O índice do checkout da autora foi preservado: nesta árvore ele
continha outros documentos, não os 27–37. O objeto `cedbfa3` não existe neste
clone e, portanto, não foi possível publicá-lo. O pacote não continha o briefing
nem os pareceres 23/25/26; a mensagem solicitada do commit não prova sua inclusão.

## Fonte, desenho e critério

Stewart (1992), *Modelling human error rates for human reliability analysis of a
structural design task*, DOI 10.1016/0951-8320(92)90097-5, páginas 174–175.
PDF local conferido por extração e visualmente, inclusive ampliação da Tabela 2.
SHA256: `0da3f1e0a4ab4514c47f9946d09996dba0c12debc71d1f2e63af65ff39ac911d`.

Protocolo anterior à execução: [PROTOCOLO_C3](../research/lote37/PROTOCOLO_C3.md).
Parâmetros literais: n=25, N=94, p=0,0163, CV=1,13, phi=0,845.
Pearson usa os grupos 0, 1, 2 e ≥3 erros, observados 68, 18, 5 e 3.
Aceitação exigida: mesma terceira casa decimal, sem ajustar alvo ou parâmetros.

## Frequências: publicado e recalculado

Valores abaixo gerados diretamente do CSV arquivado; “não” é reprovação na
terceira casa. Foram reprovadas 13 de 27 células.

| Distribuição | Erros | Publicado | Calculado | Passou |
|---|---:|---:|---:|---|
| binomial | 0 | 62.330 | 62.329642842 | sim |
| binomial | 1 | 25.820 | 25.820198697 | sim |
| binomial | 2 | 5.134 | 5.134116972 | sim |
| binomial | 3 | 0.652 | 0.652224748 | sim |
| binomial | 4 | 0.059 | 0.059440834 | sim |
| binomial | 5 | 0.004 | 0.004136749 | sim |
| binomial | 6 | 0.000 | 0.000228488 | sim |
| binomial | 7 | 0.000 | 0.000010276 | sim |
| binomial | 8 | 0.000 | 0.000000383 | sim |
| beta_binomial | 0 | 67.475 | 67.519233331 | não |
| beta_binomial | 1 | 18.334 | 18.312486372 | não |
| beta_binomial | 2 | 5.639 | 5.626435332 | não |
| beta_binomial | 3 | 1.765 | 1.759777280 | não |
| beta_binomial | 4 | 0.549 | 0.546319120 | não |
| beta_binomial | 5 | 0.167 | 0.166519122 | sim |
| beta_binomial | 6 | 0.050 | 0.049510963 | sim |
| beta_binomial | 7 | 0.014 | 0.014291928 | sim |
| beta_binomial | 8 | 0.000 | 0.003989000 | não |
| p_dependente | 0 | 66.416 | 66.457584286 | não |
| p_dependente | 1 | 19.719 | 19.700936717 | não |
| p_dependente | 2 | 5.690 | 5.675635606 | não |
| p_dependente | 3 | 1.593 | 1.586501208 | não |
| p_dependente | 4 | 0.432 | 0.429548501 | não |
| p_dependente | 5 | 0.113 | 0.112435353 | não |
| p_dependente | 6 | 0.029 | 0.028392239 | não |
| p_dependente | 7 | 0.007 | 0.006900658 | sim |
| p_dependente | 8 | 0.002 | 0.001610082 | sim |

## Qui-quadrado

Os três controles falham na terceira casa.

| Distribuição | Publicado | Calculado |
|---|---:|---:|
| binomial | 10.174 | 10.173016538 |
| beta_binomial | 0.162 | 0.161081738 |
| p_dependente | 0.583 | 0.584350304 |

## Investigação: discrepância confirmada, causa ainda aberta

- A fórmula de momentos com mu=0,0163 e CV=1,13 produz alpha=0,7540813924
  e beta=45,5085807201, diferentes dos impressos 0,7546 e 45,4563.
  Usar o par impresso como diagnóstico também não reproduz a tabela:
  frequência de zero erros 67,483116433, contra 67,475.
- Na p-dependente, a frequência de zero erros é diretamente
  `94*(1-0.845*0.0163)**25 = 66.457584286`, contra 66,416.
  Essa discrepância independe da implementação da recorrência.
- O PDF imprime 0,000 para oito erros na beta-binomial, confirmado em ampliação;
  os parâmetros literais produzem 0,003989000 (arredonda para 0,004).
  O alvo foi preservado.
- As alternativas diagnósticas usam apenas valores já impressos na fonte:
  alpha/beta, momentos de contagem e a fração 38/2327. Esta última aproxima a
  frequência zero p-dependente (66,414836730), mas altera a binomial para
  62,282077171, incompatível com 62,330. Nenhuma alternativa foi eleita ou
  ajustada para fazer o gabarito passar.

Precisão não publicada ou inconsistência editorial são hipóteses, **não causas
confirmadas**. Os dados demonstram incompatibilidade entre parâmetros literais
e o conjunto de alvos na precisão exigida. Não demonstram que toda diferença
seja apenas arredondamento. As fórmulas e o agrupamento também foram conferidos
em revisão independente, com recálculo concordante de binomial e p-dependente.

## Verificações e reprodução

- Quatro testes de algoritmo passaram: comparação binomial/beta-binomial com
  SciPy, enumeração de sequências para a recorrência, redução ao caso binomial,
  fórmula direta para zero erros e rejeição de Beta inviável. O teste do
  comparador confirma que ele detecta a discrepância; não valida a tabela.
- Os três testes existentes de compatibilidade passaram após C3, incluindo
  identidade bit a bit com opções neutras e o nominal de referência.
- O controle científico `validar_c3.py` terminou com **código 1**, conforme exigido.
  Testes de algoritmo aprovados não substituem esse controle reprovado.

A partir da raiz do repositório:

```sh
python3 -m unittest discover -s research -p test_stewart_c3.py -v
python3 -m unittest discover -s research -p test_compatibilidade.py -v
python3 research/lote37/validar_c3.py --saida /tmp/tcc-c3-nova-execucao
```

A pasta de saída deve ser nova; o runner preserva resultados antes de retornar
falha. Requer numpy, pandas, scipy (testes) e o PDF no caminho registrado no
manifesto. [Saídas completas](../outputs/diagnosticos/lote37_C3_20260917/)
contêm frequências, chi², variantes diagnósticas e hashes das fontes.

## Próximo passo e itens pendentes

Reconciliar com o revisor a precisão dos parâmetros e a consistência da Tabela 2
antes de retomar C3. Não mudar o critério de aceitação silenciosamente nem
inferir parâmetros por ajuste ao gabarito. O bloqueio impede integração C3 e a
continuação dos blocos A/B/C/D/E/F. E-1, T4, readout de retrabalho, estimando e
cobertura repetida permanecem pendentes; não são declarados resolvidos.
Não calibrar tau_sat/s_transicao contra Rieskamp nem alterar V_mod.
