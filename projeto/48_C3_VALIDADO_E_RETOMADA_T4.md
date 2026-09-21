# Resposta à especificação 41 — C3 validado e retomada B1/T4

18/09/2026. A especificação completa foi fornecida diretamente pela autora na
conversa; não se presume que o arquivo 41 esteja commitado. Parecer 43 excluído.
Posteriormente publicado em `d54283b`, a pedido da autora. Árvore de trabalho
movida para `TCC2/.worktrees/integracao-main-tl`; não depende mais de `/tmp`.

## 1. Veredito C3

**A implementação está validada; a fonte é internamente inconsistente na quarta
casa significativa.** Não se afirma reprodução exata nem se mantém o bloqueio
pelos critérios retratados dos pareceres 39/40. As saídas históricas permanecem
intactas. O critério vigente é o teste discriminante especificado pela autora.

Parâmetros operacionais fixos: **alpha=0,7546, beta=45,4563**, n=25, N=94.
Não reproduzem as frequências impressas na precisão de aproximadamente 0,012%
da maior célula. Os inversos diagnósticos não entraram como parâmetros.
Base de comparação pré-declarada: k=0..4; frequências são contagens, não percentuais.

## 2. Resíduos da candidata, célula a célula

| k | Publicado | Calculado | Razão | Resíduo (%) |
|---|---:|---:|---:|---:|
| 0 | 67.475 | 67.483116433 | 1.000120288 | +0.012028800 |
| 1 | 18.334 | 18.329064340 | 0.999730792 | -0.026920804 |
| 2 | 5.639 | 5.637495972 | 0.999733281 | -0.026671897 |
| 3 | 1.765 | 1.764935557 | 0.999963489 | -0.003651149 |
| 4 | 0.549 | 0.548427293 | 0.998956819 | -0.104318145 |

As diferenças sucessivas de razões incluem sinais negativos e positivos:
portanto não há tendência monotônica nas cinco células. Esse controle descritivo
não prova independência estatística dos resíduos. A amplitude é publicada abaixo.

## 3. Bateria de controles negativos

| Implementação | Maior desvio (%) | Amplitude (%) | Vezes o desvio candidato |
|---|---:|---:|---:|
| candidata | 0.104318145 | 0.116346946 | 1.000 |
| N1_sem_menos_um | 2.250601271 | 2.739783391 | 21.574 |
| N2_n24 | 9.992419179 | 11.091017188 | 95.788 |
| N3_binomial | 89.172889941 | 130.005216203 | 854.817 |
| N4_troca_alpha_beta | 100.000000000 | 0.000000000 | 958.606 |
| N5_sigma_CV_mu_quadrado | 89.155746650 | 129.972694653 | 854.652 |

N1 omite −1; N2 usa n=24; N3 usa binomial; N4 troca alpha/beta; N5 usa
literalmente sigma=CV*mu². **Todos os cinco** excedem 1% e dez vezes o desvio
candidato. N5 deu 89,155747%, não os ~99,93% orientativos. Não foi alterado para
bater nessa orientação. A bateria estabelece discriminação para esses erros,
não para toda implementação errada possível.

Resíduos de **cada controle em cada célula** estão em
[residuos.csv](../outputs/diagnosticos/lote41_C3_20260918/residuos.csv).
As quatro condições C-1..C-4 constam aprovadas no
[veredito](../outputs/diagnosticos/lote41_C3_20260918/veredito.json).

## 4. A-16 reproduzido

Busca de 73×73=5.329 pontos da caixa impressa de alpha/beta. Todos satisfazem
os arredondamentos mu→0,0163 e CV→1,13; nenhum E0 arredonda a 67,475.
E0∈[67,481624506;67,484608392]. Alpha*=0,754875715 e beta*=45,435977462,
com o outro parâmetro fixo. Discrepância operacional de E0=0,012028800%.
[Busca integral](../outputs/diagnosticos/lote41_C3_20260918/busca_A16_5329.csv)
e registro em [04_FONTES](04_FONTES.md). A exceção de oito erros permanece
conhecida; não foi apagada nem incluída na seleção de cinco células autorizada.

## 5. Verificações

- Três testes discriminantes: bateria, A-16 e comparação independente da
  candidata SciPy com a implementação original por log-gamma — aprovados.
- Identidade bit a bit após C3: três testes aprovados (campos, RNG, estados e
  guarda anti-delegação), incluindo nominal histórico.
- O comando `research/lote37/validar_c3.py` usa `parecer41` por padrão;
  `--regra historica` e `--regra parecer39` preservam os critérios anteriores
  para auditoria, não como critério vigente.

```sh
python3 research/lote37/validar_c3.py --regra parecer41 --saida /tmp/c3-41-nova
python3 -m unittest discover -s research -p test_c3_discriminante.py -v
python3 -m unittest discover -s research -p test_compatibilidade.py -v
```

As pastas de saída devem ser novas. Não foi ajustado nenhum parâmetro ao gabarito.

## 6. B1/T4 — desenho e controle das diagonais

Executadas **1.536 simulações**: quatro células × dois níveis comuns de reporte
× 16 instâncias × 12 sementes. CC/AC/CA/AA indicam portão/rede nos níveis
centralizado (C) ou adaptativo (A). Portão inclui tau inicial e tau_min, como T2;
rede muda apenas tau inicial. Reporte e detecção são iguais dentro de cada
quadro. Crowder continua dinâmico, mesma lei em todos os braços.

**768 diagonais verificadas bit a bit** contra execuções sem overrides: resultados,
agentes, tarefas, eventos, registros, dívida e RNG. Diagonais também reproduzem
as quatro células T2 arquivadas, diferença máxima de serialização
2,8421709430404014e-14. Nenhuma censura ou violação. Identidade neutra após B1:
três testes aprovados; testes de isolamento dos overrides aprovados.

IC95 t calculados sobre 16 médias de instância (12 sementes internas pareadas),
pontuais, não simultâneos. As sementes comuns não garantem sorteios alinhados
por evento depois de as trajetórias divergirem.

### Reporte/detecção comuns: nível centralizada

| Indicador | CC | AC | CA | AA |
|---|---|---|---|---|
| atraso_relativo | 3.060802 [2.752985; 3.368620] | 2.967879 [2.638366; 3.297392] | 2.848410 [2.519324; 3.177496] | 2.741961 [2.422897; 3.061025] |
| taxa_omissao | 0.312500 [0.294370; 0.330630] | 0.278299 [0.257130; 0.299467] | 0.285156 [0.264179; 0.306134] | 0.271181 [0.252556; 0.289805] |
| divida_latente_sobre_plano | 0.103272 [0.093760; 0.112784] | 0.092145 [0.084258; 0.100033] | 0.097249 [0.088450; 0.106049] | 0.087967 [0.079164; 0.096771] |
| taxa_falha_efetiva | 0.361979 [0.339808; 0.384150] | 0.323437 [0.300467; 0.346408] | 0.332552 [0.309159; 0.355945] | 0.310937 [0.290718; 0.331157] |
| fracao_porta1 | 0.636979 [0.582431; 0.691528] | 0.550868 [0.494368; 0.607368] | 0.575347 [0.515699; 0.634995] | 0.502344 [0.442458; 0.562229] |

| Indicador | Portão AC−CC | Rede CA−CC | Interação AA−AC−CA+CC | Total AA−CC |
|---|---|---|---|---|
| atraso_relativo | -0.092924 [-0.219962; +0.034114] | -0.212392 [-0.318448; -0.106336] | -0.013526 [-0.187514; +0.160462] | -0.318842 [-0.380422; -0.257261] |
| taxa_omissao | -0.034201 [-0.049621; -0.018781] | -0.027344 [-0.039617; -0.015070] | +0.020226 [+0.002429; +0.038023] | -0.041319 [-0.054601; -0.028038] |
| divida_latente_sobre_plano | -0.011127 [-0.017075; -0.005179] | -0.006023 [-0.010532; -0.001514] | +0.001845 [-0.004214; +0.007905] | -0.015305 [-0.019987; -0.010623] |
| taxa_falha_efetiva | -0.038542 [-0.056198; -0.020886] | -0.029427 [-0.042528; -0.016326] | +0.016927 [-0.001667; +0.035521] | -0.051042 [-0.066909; -0.035174] |
| fracao_porta1 | -0.086111 [-0.103943; -0.068279] | -0.061632 [-0.078187; -0.045077] | +0.013108 [-0.005623; +0.031838] | -0.134635 [-0.158280; -0.110990] |

### Reporte/detecção comuns: nível adaptativa

| Indicador | CC | AC | CA | AA |
|---|---|---|---|---|
| atraso_relativo | 2.469996 [2.156931; 2.783061] | 2.209612 [1.904265; 2.514960] | 2.171330 [1.891204; 2.451457] | 2.037381 [1.773492; 2.301271] |
| taxa_omissao | 0.090104 [0.079878; 0.100330] | 0.085503 [0.078662; 0.092345] | 0.088542 [0.079210; 0.097874] | 0.084288 [0.076504; 0.092072] |
| divida_latente_sobre_plano | 0.028985 [0.026041; 0.031929] | 0.025907 [0.023772; 0.028042] | 0.027220 [0.024176; 0.030264] | 0.025458 [0.022972; 0.027943] |
| taxa_falha_efetiva | 0.353472 [0.326955; 0.379989] | 0.331076 [0.309014; 0.353139] | 0.333160 [0.309354; 0.356965] | 0.318924 [0.296469; 0.341378] |
| fracao_porta1 | 0.639497 [0.581268; 0.697725] | 0.567014 [0.506338; 0.627690] | 0.595920 [0.538944; 0.652896] | 0.520486 [0.458634; 0.582339] |

| Indicador | Portão AC−CC | Rede CA−CC | Interação AA−AC−CA+CC | Total AA−CC |
|---|---|---|---|---|
| atraso_relativo | -0.260384 [-0.301455; -0.219312] | -0.298666 [-0.339278; -0.258053] | +0.126435 [+0.089135; +0.163735] | -0.432614 [-0.491390; -0.373839] |
| taxa_omissao | -0.004601 [-0.011599; +0.002398] | -0.001562 [-0.008329; +0.005204] | +0.000347 [-0.008115; +0.008809] | -0.005816 [-0.013603; +0.001971] |
| divida_latente_sobre_plano | -0.003078 [-0.005290; -0.000866] | -0.001765 [-0.004401; +0.000872] | +0.001316 [-0.000923; +0.003554] | -0.003527 [-0.006063; -0.000992] |
| taxa_falha_efetiva | -0.022396 [-0.034723; -0.010068] | -0.020313 [-0.031313; -0.009312] | +0.008160 [-0.005665; +0.021984] | -0.034549 [-0.048575; -0.020522] |
| fracao_porta1 | -0.072483 [-0.089705; -0.055261] | -0.043576 [-0.054297; -0.032855] | -0.002951 [-0.019363; +0.013460] | -0.119010 [-0.138697; -0.099324] |

## 7. Leitura dos mecanismos

**Os dois canais contribuem à redução da taxa de falha efetiva.** No reporte
adaptativo: portão −0,022396 [−0,034723;−0,010068]; rede
−0,020313 [−0,031313;−0,009312]; interação +0,008160
[−0,005665;+0,021984]. O total −0,034549 reproduz T2. Não somar os dois
componentes sem a interação nem repartir essa interação arbitrariamente.

No contraste de rede CA−CC o portão centralizado fica fechado (nenhum pedido),
logo o benefício não exige assistência. O código mantém p0 dependente de mu_cog,
não de mu_rede. O canal de rede atua pela duração e pela evolução de pressão e
bateria: no reporte adaptativo, CA−CC reduz duração efetiva média em 1,538108
períodos e eleva mu_cog médio em 0,031145. A leitura é **confiança reduz duração
e, por esse caminho indireto, reduz degradação cognitiva**, e não “assistência
reduz defeito” para esse contraste. Essas médias corroboram a leitura do código;
não constituem identificação separada de todos os mediadores e realimentações.

O contraste de portão também reduz falhas e uso de P1. Abrir o portão gera
eventos de comunicação que atualizam ambos os estados de confiança pela lei
Crowder existente; portanto a intervenção no portão inclui as consequências
dinâmicas da assistência sobre a rede. T4 separa as duas intervenções iniciais,
não congela todos os mediadores posteriores. Com reporte baixo, o IC do efeito
do portão no atraso inclui zero; não há evidência de redução desse desfecho
nessa condição isolada. A rede reduz atraso nos dois níveis de reporte.

[E_total permanece diagnóstico interno, fora das conclusões de governança.]
T4 não altera o nominal nem resolve por si só a validade externa dos construtos.

## 8. Artefatos e continuidade

[Saídas T4 completas](../outputs/diagnosticos/lote41_T4_20260918/) incluem células,
decomposição, contrastes por instância, bruto, manifesto e controles de diagonais.
[Protocolo](../research/lote41/PROTOCOLO.md) anterior à execução.

```sh
python3 research/lote41/t4.py --saida /tmp/t4-nova
```

C3 validado pelo critério vigente; B1 concluído. Isso não declara o lote 37
inteiro fechado. B2 foi executado na sequência: ver [resultados e limite de robustez](47_B2_ROBUSTEZ_DO_CANAL_DIRETO.md).
A grade revelou censura estrutural; os itens restantes continuam pendentes. Nenhuma calibração contra Rieskamp,
nenhuma nova onda HM e nenhum ajuste de V_mod.
