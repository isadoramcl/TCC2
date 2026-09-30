# 85 — Sensibilidade ao eixo de F_base e aos pesos de Di

## Pré-registro

2026-09-29T13:42:41.162852+00:00

Nominal v3 final preservado. Primeiro: 384 execuções por eixo no nominal, comparar média e limites de IC95 às referências fornecidas e eixo complexidade à etapa3 oficial, tolerância 0,0005; parar se exceder. Tamanho usa exatamente as razões declaradas 1/1,9018/2,8368/5,3670, derivadas arredondadas da frequência bruta LOC_TOTAL. Complexidade usa o YAML nominal, não arredondamento alternativo.

A: após controle, dois eixos nos conjuntos fora48 e aleatorio24, com as chaves (arquivo,semente) da etapa3. B: três alternativas de pesos do YAML no nominal16 e fora48. Referência pesos iguais é o Di arquivado que alimenta o nominal, sem recalculá-lo artificialmente pelos pesos arredondados do YAML. Alternativas usam a função recalcular_di existente no runner20, no universo completo das tarefas; recálculo de Di, quartis globais e nível antes da instanciação do simulador. Não altera dados originais.

IC95: contraste pareado adaptativa−centralizada por (arquivo,semente), médias das sementes por instância, t sobre instâncias. Sem descarte de variantes. Todas as execuções devem concluir e ter zero violações. Nenhum parâmetro será ajustado por resultado.

## Critério da autora (transcrição)

Vale para os dois itens.

1. Zero violações em todas as execuções; todas concluem.
2. INSENSIBILIDADE, a afirmação que se quer testar: os cinco contrastes mantêm
   SINAL NEGATIVO com IC 95% EXCLUINDO ZERO em todas as variantes e em todos os
   conjuntos. Se isso valer, a conclusão do trabalho não depende da escolha e
   ambos os itens fecham como decisão de escopo declarada.
3. Se algum contraste MUDAR DE SINAL ou passar a incluir zero em alguma
   variante, isso é resultado e entra como tal — identificando exatamente qual
   indicador, qual variante e qual conjunto. Não é motivo para descartar a
   variante nem para procurar outra ponderação que recupere o resultado.
4. A taxa de falha efetiva já está declarada como não robusta à varredura de
   governança. Se ela for a única a falhar aqui, isso é consistente com o que já
   se sabe e deve ser dito assim, sem virar achado novo.
5. Reportar tudo em tabela única, variante por variante, conjunto por conjunto.

## Estado

Pré-registro escrito antes de executar. Resultados pendentes. Código de produção e nominal não serão modificados; orquestração temporária será copiada como texto na saída para rastreabilidade.


## Resultado final — 29/09/2026

**Item A: critério de insensibilidade atendido. Item B: critério de insensibilidade atendido.** Todas as 8.832 execuções concluíram, com zero violações; todos os 60 contrastes da tabela única são negativos, com IC95 excluindo zero. Ambos os itens podem fechar como **decisão de escopo declarada dentro das alternativas e conjuntos testados**. A configuração nominal v3 permanece intacta.

### Controle nominal e reconciliação transparente

As médias e os dois limites de IC dos cinco indicadores do eixo complexidade reproduziram **exatamente** a etapa3 oficial, resíduo 0. O critério solicitado de tolerância 0,0005 contra essa referência foi atendido. O eixo tamanho reproduziu os números fornecidos pela autora com diferença máxima de **0,000045371429**.

Há uma discrepância com a tabela recebida: o limite inferior do IC de atraso no eixo complexidade foi **−1,047255946**, enquanto a tabela fornecia **−1,0481**; diferença **0,000844054**. Os demais números ficaram dentro da tolerância. Não foi alterado o resultado para fazê-lo coincidir, nem foi atribuída a causa ao arredondamento como fato demonstrado.

O primeiro verificador aplicou uma condição adicional, mais ampla que a solicitada contra a etapa3: exigir a mesma tolerância para cada número arredondado da tabela recebida. Ele parou por esse limite de IC. A falha ficou preservada em controle_veredito.json; a reconciliação foi registrada em [85A](85A_RECONCILIACAO_DO_CONTROLE.md) **antes da extensão**. Prosseguiu-se pela condição explicitamente solicitada contra o nominal oficial, que passou. controle_diferencas.csv conserva todos os valores e controle_criterio_autora.json identifica a decisão. Isso não altera o critério de insensibilidade nem omite a diferença observada.

### Execuções e desenho efetivo

| Conjunto | Instâncias | Sementes por instância e braço | Variantes | Execuções |
|---|---:|---:|---:|---:|
| Nominal | 16 | 12 | 5 | 1.920 |
| Fora da amostra | 48 | 12 | 5 | 5.760 |
| Teste aleatório | 24 | 12 | 2 eixos | 1.152 |
| **Total** | | | | **8.832** |

As chaves (arquivo,semente) são as mesmas da etapa3 arquivada, conferidas individualmente. Ambos os arranjos são simulados em cada chave. As variantes A alteram somente risco.razoes_de_risco; B altera os pesos e seus derivados Di/nível/F_base a montante. Não se cruzaram eixo tamanho e pesos alternativos: são duas sensibilidades separadas, como solicitado.

Razões complexidade: **1; 1,935; 2,367; 2,985**. Razões tamanho: **1; 1,9018; 2,8368; 5,3670**. As razões obtidas diretamente das frequências LOC_TOTAL arquivadas são 1; 1,901830808; 2,836805556; 5,366950758, confirmando as quatro casas fornecidas. Mantiveram-se a transferência ordinal e os demais parâmetros; não foram criadas medidas LOC para tarefas J60.

### Tabela única — adaptativa menos centralizada

Cada célula contém média [IC95]. Pareamento por arquivo/semente, média das sementes por instância, intervalo t entre instâncias. N=16,48,24 conforme conjunto. As proporções são frações (por exemplo −0,02 corresponde a −2 pontos percentuais). Valores completos nos CSVs, arredondamento aqui a seis casas.

| Variante | Conjunto | Atraso relativo | Omissão | Dívida latente/plano | Falha efetiva | Fração Porta 1 |
|---|---|---:|---:|---:|---:|---:|
| Complexidade / pesos iguais (referência) | nominal | -0.910045 [-1.047256; -0.772834] | -0.174306 [-0.189571; -0.159040] | -0.054653 [-0.060665; -0.048642] | -0.019358 [-0.030336; -0.008379] | -0.053385 [-0.067347; -0.039424] |
| Complexidade / pesos iguais (referência) | fora48 | -0.938070 [-1.017488; -0.858652] | -0.178906 [-0.188151; -0.169662] | -0.056657 [-0.060429; -0.052885] | -0.019213 [-0.026047; -0.012379] | -0.044705 [-0.051015; -0.038394] |
| Complexidade / pesos iguais (referência) | aleatorio24 | -0.952782 [-1.073080; -0.832483] | -0.174595 [-0.185622; -0.163568] | -0.054236 [-0.058862; -0.049610] | -0.017593 [-0.026851; -0.008335] | -0.055324 [-0.066086; -0.044562] |
| Tamanho / pesos iguais | nominal | -0.922445 [-1.036663; -0.808228] | -0.216927 [-0.232745; -0.201109] | -0.065578 [-0.071398; -0.059757] | -0.022135 [-0.035491; -0.008780] | -0.042361 [-0.054465; -0.030257] |
| Tamanho / pesos iguais | fora48 | -0.959900 [-1.051118; -0.868682] | -0.219589 [-0.230106; -0.209072] | -0.069439 [-0.073889; -0.064990] | -0.013860 [-0.021029; -0.006691] | -0.036053 [-0.043204; -0.028903] |
| Tamanho / pesos iguais | aleatorio24 | -1.028079 [-1.149586; -0.906572] | -0.214062 [-0.229841; -0.198284] | -0.066807 [-0.073453; -0.060162] | -0.022106 [-0.031947; -0.012266] | -0.054051 [-0.065260; -0.042842] |
| Complexidade / criticidade reduzida | nominal | -0.919564 [-1.028838; -0.810290] | -0.179427 [-0.193273; -0.165581] | -0.053366 [-0.058702; -0.048030] | -0.020573 [-0.032695; -0.008450] | -0.055990 [-0.062591; -0.049388] |
| Complexidade / criticidade reduzida | fora48 | -1.008085 [-1.105228; -0.910942] | -0.177720 [-0.186455; -0.168985] | -0.055339 [-0.059132; -0.051547] | -0.020978 [-0.029504; -0.012452] | -0.051505 [-0.059040; -0.043969] |
| Complexidade / duração dominante | nominal | -0.829950 [-0.926084; -0.733816] | -0.177865 [-0.189474; -0.166255] | -0.058728 [-0.064379; -0.053077] | -0.014149 [-0.023137; -0.005161] | -0.030208 [-0.040437; -0.019980] |
| Complexidade / duração dominante | fora48 | -0.918441 [-1.004589; -0.832293] | -0.172541 [-0.181249; -0.163832] | -0.056961 [-0.060725; -0.053196] | -0.007639 [-0.013478; -0.001799] | -0.026939 [-0.032837; -0.021040] |
| Complexidade / recursos dominantes | nominal | -0.895342 [-1.024041; -0.766643] | -0.176910 [-0.193314; -0.160505] | -0.048605 [-0.054374; -0.042836] | -0.028733 [-0.035562; -0.021903] | -0.052604 [-0.067217; -0.037991] |
| Complexidade / recursos dominantes | fora48 | -1.033483 [-1.109266; -0.957701] | -0.174682 [-0.184764; -0.164599] | -0.050883 [-0.055006; -0.046759] | -0.022714 [-0.029455; -0.015974] | -0.059578 [-0.067776; -0.051379] |

### Veredito por item

**A — Eixo de F_base:** 30/30 contrastes negativos e IC95 inteiramente negativos, em complexidade e tamanho nos três conjuntos. A direção e o critério de exclusão de zero sobrevivem à troca de eixo. As magnitudes mudam; não se afirma igualdade dos resultados nem validação causal da complexidade controlada por tamanho. O eixo nominal permanece como escolha de escopo testada, sem necessidade de escolher outro para sustentar os cinco sinais nos desenhos avaliados.

**B — Pesos de Di:** 40/40 contrastes negativos e IC95 inteiramente negativos, incluindo referência e três alternativas, nos conjuntos nominal e fora da amostra. Dez contrastes de referência também entram em A; por isso a tabela única contém 60, não 70. O resultado é insensível às ponderações declaradas quanto ao critério solicitado, embora os efeitos tenham magnitudes diferentes. Não se afirma robustez a qualquer vetor de pesos.

Nenhum indicador mudou de sinal ou passou a incluir zero. A falha efetiva também sobreviveu aqui; isso **não retrata** sua não robustez na varredura de governança, que é outro desenho. Não houve escolha posterior de variante, descarte de execução ou busca de pesos favoráveis.

### Recálculo a montante — verificado, não apenas declarado

O Di nominal arquivado corresponde aos terços exatos: desvio máximo de 3,33×10⁻¹⁶ frente à média dos três componentes. Recalculá-lo com 0,3333/0,3333/0,3334 daria diferença de até 6,67×10⁻⁵. Por isso, a referência preservou o Di que de fato alimenta o nominal oficial, em vez de criar uma quarta mudança não solicitada.

Para as três alternativas, usou-se a função existente recalcular_di, com soma ponderada dos componentes normalizados. Os quartis foram recalculados **no universo completo de 28.800 tarefas**, antes de selecionar as instâncias experimentais; cada tarefa recebeu o novo nível e o correspondente F_base=0,10×razão_do_nível. Esses dados, e não apenas o YAML, foram passados à construção do simulador.

| Alternativa | Pesos duração/recursos/criticidade | Tarefas com nível alterado (universo completo) |
|---|---|---:|
| criticidade reduzida | 0,40 / 0,40 / 0,20 | 5.797 |
| duração dominante | 0,60 / 0,20 / 0,20 | 10.043 |
| recursos dominantes | 0,20 / 0,60 / 0,20 | 12.022 |

Os arquivos tarefas_*.csv preservam Di e nível nominais e alternativos, além do F_base aplicado. Uma análise independente recompôs a soma ponderada, os cortes, a atribuição de níveis e o F_base de todas as tarefas; também conferiu as chaves de cada execução. Diferença máxima entre os 60 contrastes/limites recalculados e o runner: **2,22×10⁻¹⁶**.

### Preservação e evidências

Diretório: `outputs/diagnosticos/20260929_eixo_fbase_pesos_di/`.

- controle_nominal.csv e extensao.csv: todas as execuções, sem sobrescrever as evidências antigas.
- tabela_unica.csv e tabela_unica_recalculada.csv: todos os 60 contrastes, resultado original e auditoria independente.
- auditoria_independente.json e validade_final.json: contagens, conclusão e violações.
- auditoria_recalculo_di.json e tarefas_*.csv: alteração efetiva a montante.
- snapshot/ e hashes_entradas.json: código, parâmetros e dados que alimentaram o lote; nominal e código de produção preservados.
- Orquestração e análise executadas foram preservadas como textos; não se editaram scripts do modelo.

Os **826 arquivos de outputs anteriores** conferem com seus hashes de partida. Leituras de CSV com float_precision='round_trip'. Não foram executados git status/add/commit/push. A sensibilidade encerra os dois itens no escopo acima; não é calibração nem fundamento para alterar o nominal.
