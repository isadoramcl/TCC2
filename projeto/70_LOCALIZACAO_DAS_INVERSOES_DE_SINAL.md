# T-GOV.2 — localização das inversões e leitura da multiplicidade

Nenhuma simulação nova. Base: T-GOV.1, 81 perfis, quatro instâncias e quatro
sementes; contrastes adaptativa−centralizada. Sinal oposto ao contraste médio
nominal negativo: IC95 inteiramente positivo. A taxa de falha efetiva nominal
já tinha IC cruzando zero; seu sinal de referência é apenas o da média.
Todos os resultados abaixo são completos, sem censura.

## Denominadores: 3/1.215, não 3/6.561

| metrica | N_total | IC_oposto_total | N_ordenacao_historica | IC_oposto_ordenado | vetores_distintos | perfis_A | perfis_C |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atraso_relativo | 6561 | 1602 | 1215 | 3 | 3 | 1 | 3 |
| divida_latente_sobre_plano | 6561 | 1628 | 1215 | 1 | 1 | 1 | 1 |
| fracao_porta1 | 6561 | 1701 | 1215 | 11 | 6 | 8 | 7 |
| taxa_falha_efetiva | 6561 | 379 | 1215 | 4 | 4 | 4 | 2 |
| taxa_omissao | 6561 | 2226 | 1215 | 3 | 3 | 3 | 2 |

Os três casos de atraso pertencem à região com ordenação histórica das quatro
premissas: 1.215 pares não idênticos. Na malha total há 1.602 ICs positivos
para atraso, incluindo os 1.599 em regiões que invertem ao menos uma premissa.
Os 81 perfis idênticos têm diferença exatamente zero. Misturar o numerador de
uma sub-região com o denominador total produz a comparação “55x menos”.

Sob n hipóteses todas nulas e ICs marginais com cobertura e caudas corretas,
a expectativa de exclusões numa direção seria 0,025*n: 164,025 para 6.561
ou 30,375 para 1.215. Linearidade da esperança não exige independência, mas
uma interpretação binomial das contagens exigiria hipóteses adicionais.
Aqui as hipóteses não são todas nulas, há fortes efeitos negativos, perfis
idênticos degenerados e reutilização das mesmas trajetórias. Essas contas
não estimam quantas das inversões observadas são falsas e não decidem entre
multiplicidade e mecanismo. Os ICs são pontuais, sem controle familiar.

## Todos os 22 contrastes da região de ordenação histórica

Tuplas explicitam os quatro parâmetros em cada braço. Nada foi filtrado por
magnitude além do critério solicitado de IC95 inteiramente oposto.

| metrica | perfil_adaptativa | perfil_centralizada | A (tau, limiar, reporte, detecção) | C (tau, limiar, reporte, detecção) | media | ic95_inf | ic95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atraso_relativo | 71 | 41 | 0.8, 0.425, 0.75, 0.12 | 0.525, 0.425, 0.45, 0.12 | 0.023259 | 0.009276 | 0.037241 |
| atraso_relativo | 71 | 68 | 0.8, 0.425, 0.75, 0.12 | 0.8, 0.425, 0.45, 0.12 | 0.066676 | 0.005723 | 0.12763 |
| atraso_relativo | 71 | 74 | 0.8, 0.425, 0.75, 0.12 | 0.8, 0.6, 0.15, 0.12 | 0.072946 | 0.019845 | 0.126047 |
| divida_latente_sobre_plano | 60 | 78 | 0.8, 0.25, 0.75, 0.03 | 0.8, 0.6, 0.75, 0.03 | 0.002526 | 0.000942 | 0.00411 |
| fracao_porta1 | 5 | 2 | 0.25, 0.25, 0.45, 0.12 | 0.25, 0.25, 0.15, 0.12 | 0.019792 | 0.008469 | 0.031115 |
| fracao_porta1 | 5 | 11 | 0.25, 0.25, 0.45, 0.12 | 0.25, 0.425, 0.15, 0.12 | 0.019792 | 0.008469 | 0.031115 |
| fracao_porta1 | 5 | 20 | 0.25, 0.25, 0.45, 0.12 | 0.25, 0.6, 0.15, 0.12 | 0.019792 | 0.008469 | 0.031115 |
| fracao_porta1 | 14 | 11 | 0.25, 0.425, 0.45, 0.12 | 0.25, 0.425, 0.15, 0.12 | 0.019792 | 0.008469 | 0.031115 |
| fracao_porta1 | 14 | 20 | 0.25, 0.425, 0.45, 0.12 | 0.25, 0.6, 0.15, 0.12 | 0.019792 | 0.008469 | 0.031115 |
| fracao_porta1 | 23 | 20 | 0.25, 0.6, 0.45, 0.12 | 0.25, 0.6, 0.15, 0.12 | 0.019792 | 0.008469 | 0.031115 |
| fracao_porta1 | 30 | 27 | 0.525, 0.25, 0.45, 0.03 | 0.525, 0.25, 0.15, 0.03 | 0.022917 | 0.010221 | 0.035612 |
| fracao_porta1 | 35 | 38 | 0.525, 0.25, 0.75, 0.12 | 0.525, 0.425, 0.15, 0.12 | 0.022917 | 0.000927 | 0.044906 |
| fracao_porta1 | 37 | 36 | 0.525, 0.425, 0.15, 0.075 | 0.525, 0.425, 0.15, 0.03 | 0.017708 | 0.005158 | 0.030259 |
| fracao_porta1 | 39 | 36 | 0.525, 0.425, 0.45, 0.03 | 0.525, 0.425, 0.15, 0.03 | 0.021875 | 0.004438 | 0.039312 |
| fracao_porta1 | 76 | 72 | 0.8, 0.6, 0.45, 0.075 | 0.8, 0.6, 0.15, 0.03 | 0.023958 | 0.004915 | 0.043002 |
| taxa_falha_efetiva | 54 | 36 | 0.8, 0.25, 0.15, 0.03 | 0.525, 0.425, 0.15, 0.03 | 0.029167 | 0.003205 | 0.055129 |
| taxa_falha_efetiva | 59 | 40 | 0.8, 0.25, 0.45, 0.12 | 0.525, 0.425, 0.45, 0.075 | 0.010417 | 0.006589 | 0.014245 |
| taxa_falha_efetiva | 63 | 36 | 0.8, 0.425, 0.15, 0.03 | 0.525, 0.425, 0.15, 0.03 | 0.030208 | 0.004602 | 0.055815 |
| taxa_falha_efetiva | 68 | 40 | 0.8, 0.425, 0.45, 0.12 | 0.525, 0.425, 0.45, 0.075 | 0.013542 | 0.000991 | 0.026092 |
| taxa_omissao | 54 | 36 | 0.8, 0.25, 0.15, 0.03 | 0.525, 0.425, 0.15, 0.03 | 0.029167 | 0.002099 | 0.056234 |
| taxa_omissao | 63 | 36 | 0.8, 0.425, 0.15, 0.03 | 0.525, 0.425, 0.15, 0.03 | 0.032292 | 0.003455 | 0.061128 |
| taxa_omissao | 67 | 66 | 0.8, 0.425, 0.45, 0.075 | 0.8, 0.425, 0.45, 0.03 | 0.014583 | 0.001888 | 0.027279 |

[Lista integral de ICs opostos em toda a malha](../outputs/diagnosticos/GOV2_CROWDER1_20260919/GOV2_todas_inversoes_IC95.csv),
com os oito valores e a região de cada contraste.
[Sub-região ordenada e assinaturas das diferenças por execução](../outputs/diagnosticos/GOV2_CROWDER1_20260919/GOV2_inversoes_ordenacao_historica.csv).

## Onde se concentram e qual a leitura

- **Atraso (3): concentração clara em um perfil A**, o 71:
  tau=0,80, limiar=0,425, reporte=0,75, detecção=0,12. Os comparadores C
  também começam com assistência aberta e detecção=0,12, mas reporte menor.
  São 3/53 comparações ordenadas envolvendo A=71, contra 0/1.162 no restante.
  Esta região foi identificada após observar os dados, não pré-especificada.
  Não são três ocorrências espalhadas ou três réplicas independentes: as três
  reutilizam o mesmo braço A. Achado descritivo de região candidata; o padrão
  sozinho não confirma mecanismo nem exclui multiplicidade.
- **Omissão (3): dois casos compartilham C=36**, baixa detecção/reporte
  (0,03/0,15), e A com confiança 0,80 versus 0,525. O terceiro mantém
  confiança/limiar/reporte iguais e altera somente detecção 0,03→0,075.
  Há um agrupamento de dois e um caso separado, não uma região única.
- **Falha efetiva (4): dois pares de regiões**. Todos têm confiança A=0,80
  versus C=0,525 e reporte igual entre os braços. Os casos de reporte/detecção
  baixos coincidem com duas inversões de omissão; o outro par usa reporte=0,45,
  detecção A=0,12 versus C=0,075. Mudam limiares A=0,25/0,425. Concentração
  descritiva em maior confiança inicial, não prova causal dos escalares.
- **Dívida latente (1): caso isolado**, tau=0,80 e reporte=0,75 em ambos,
  detecção=0,03; só o limiar muda de C=0,60 para A=0,25. Uma célula não
  estabelece concentração regional: manter como inversão exploratória,
  compatível com flutuação/multiplicidade até confirmação independente.
- **Fração P1 (11): seis são o mesmo vetor de diferenças por execução**,
  com tau=0,25, assistência fechada nos dois braços, detecção=0,12 e
  reporte 0,15→0,45; limiares diferentes não mudam as trajetórias. Os cinco
  restantes são outros contrastes. Há redundância estrutural, não seis
  evidências independentes de uma região. Não atribuir esse agrupamento a Crowder.

**Veredicto:** as inversões de atraso e parte das demais estão concentradas,
e a leitura anterior de “sinal não estável” sem escala regional foi ampla demais.
Predomina o contraste negativo sob ordenação histórica, com exceções locais
exploratórias e dependentes. Não é justificável classificar todas como ruído,
nem elevá-las a regimes científicos confirmados só pela localização. Dívida
permanece um caso isolado; fracão P1 inclui duplicatas exatas. A nova varredura
Crowder caracteriza sensibilidade nominal, mas não reexecuta estes perfis e,
portanto, não poderá provar por si só a causa dessas inversões.
