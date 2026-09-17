# Resposta à revisão científica — ciclo de 15/09/2026

Parecer respondido: [09_REVISAO_INDEPENDENTE](09_REVISAO_INDEPENDENTE_2026-09-15.md).
A revisão foi tratada como fonte de hipóteses. Esta resposta substitui a ordem
de trabalho da auditoria anterior, sem apagar evidência histórica.

## Resumo das decisões

- Confirmada a informação separada sobre frequência de falhas. Refutada a
  afirmação de que o conjunto de saídas só observa o produto dos parâmetros.
- Confirmados confiança constante e dois canais diretos, mas o segundo é o
  multiplicador **de rede**, não o cognitivo. Não foi adotada confiança dinâmica.
- Confirmada sensibilidade à variância, mas não a explicação exclusiva de piso
  de ruído, nem a equivalência entre reduzir ambas as variâncias e aumentar só
  réplicas simuladas. Cobertura e desenho observacional continuam prioritários.
- Corrigida a rastreabilidade por referências imutáveis e snapshots documentais.
  Nada foi descartado, sobrescrito ou integrado na `main` da autora.

## Desenho e reprodutibilidade

Os [planos iniciais](../research/PLANO_REVISAO.md) foram escritos antes das
simulações. A [continuação na fronteira](../research/PLANO_FRONTEIRA.md) foi
planejada após o piloto inicial não informar sobre aceitação. Foram realizadas
2112 execuções novas: produto, ruído, cobertura, confiança, vértices e fronteira.
Todos os pilotos registraram término completo, ausência de dívida pendente e
nenhuma violação detectada. Esse resultado é restrito às amostras testadas.

Os dados individuais e cálculos estão em
`outputs/diagnosticos/revisao_20260915/`. Comandos, ambiente e recuperação de
fontes estão em [REPRODUCAO](../research/REPRODUCAO.md). Os resultados numéricos
abaixo foram lidos dos CSVs na elaboração deste documento.

## Classificação crítica por crítica

### CRITICAL-1 — PARTIALLY ACCEPTED

**Aceito:** o argumento de produto suficiente é falso para as saídas usadas.
Correlações e R² do parecer foram reproduzidos por `16_reanalise_revisao.py`.
São análises descritivas dentro do desenho, não prova formal de identificabilidade.

**Experimento discriminante:** manter produto constante e variar F_ancora e
f_retrabalho, com demais parâmetros no vetor verdadeiro, instâncias e sementes
pareadas. O contraste de taxa de omissão entre extremos foi 0.063281,
IC95 [0.050088; 0.076474]. Para retrabalho/plano o intervalo
inclui zero. Assim, algumas saídas distinguem fatores mesmo quando outras
permanecem próximas. Evidências: `produto/bruto.csv`, `analise/produto_contrastes.csv`.

**Não aceito como conclusão:** a correlação sozinha provar identificabilidade
estrutural global ou unicidade dos cinco parâmetros. O piloto falsifica uma
invariância particular, não demonstra ausência de outras equivalências.

**Impacto/ação:** retirada do relatório automático a afirmação de que apenas o
produto é observável e a recomendação automática de colapsar os dois parâmetros.
Mantidas as tabelas históricas, a crista empírica e todos os cálculos.

### CRITICAL-2 — PARTIALLY ACCEPTED

**Reprodução:** o NROY legado contém 40 pontos. Dividir
V_sim por oito, mantendo V_obs e médias, deixa 13; dividir ambas deixa quatro,
reproduzindo a tabela do parecer. Isso é sensibilidade algébrica do denominador,
não resultado de novas réplicas. Evidência: `reanalise/sensibilidade_denominador.csv`.

**Pilotos reais:** os pontos equiespaçados do desenho não eram NROY; todos
continuaram rejeitados. Não se inferiram larguras a partir deles. Na continuação,
quatro pontos antes aceitos e quatro próximos do corte foram reavaliados com
mais sementes, mantendo as instâncias. Os quatro aceitos deixaram de sê-lo no
piloto ampliado. A conta com médias fixas não reproduziu os valores reais de I.
Evidências: `ruido/bruto.csv`, `fronteira/bruto.csv`, `fronteira/comparacao.csv`.

**Tentativa de refutação:** no próprio vetor verdadeiro, com o conjunto ampliado,
o maior I contra a observação publicada foi 3.109290, determinado por
prazo. Portanto, maior rejeição não implica inferência melhor. Não substituir a
observação porque ela deixou de caber no critério.

**UNRESOLVED:** quanto da largura global vem de precisão Monte Carlo, observação,
geometria, escolhas do critério ou informação insuficiente. Rejeita-se a afirmação
categórica de que a causa exclusiva já esteja demonstrada. Nem aceitar nem
rejeitar a previsão numérica de contração global com base neste subconjunto.
A alegação de que não atingir aquela previsão fortaleceria automaticamente
não-identificabilidade estrutural também é rejeitada: há várias causas alternativas.

### CRITICAL-3 — PARTIALLY ACCEPTED

**Confirmado:** τ constante e homogêneo em cada cenário; portão sempre fechado
no centralizado e aberto no adaptativo, condicionado ainda à disponibilidade
e competência. TL nulo no centralizado é consequência direta desse portão.

**Correção factual:** `multiplicadores()` usa confiança na entrada de μ_rede.
μ_cognitivo recebe fadiga e pressão. Há efeitos indiretos por realimentação,
mas não se deve chamar o canal direto de cognitivo. A especificação §5.2 já
explicita confiança → rede; a afirmação de que isso não está documentado em
lugar nenhum é excessiva. Faltava analisar a implicação para as ablações.

**Piloto fatorial separado:** mantendo os demais parâmetros centralizados,
variaram-se somente confiança lida pelo portão e pela rede. Para atraso relativo,
os efeitos simples na referência foram -0.308509
(portão), -0.318049 (rede) e
0.013273 (interação). Para E_total, os efeitos
simples foram 0.116785 e -0.042017,
com interação 0.026175. Não são percentuais universais
de contribuição; são contrastes condicionais ao desenho e às instâncias.

As diagonais reproduziram o simulador nominal. O controle no mesmo estado
confirmou mudança apenas no multiplicador de rede. Fonte conceitual conferida
no TCC I: há τ(t) e regra de portão, mas não lei de atualização de τ naquele
pseudocódigo. Portanto, τ constante é uma simplificação com alcance limitado;
a necessidade de uma dinâmica específica não decorre apenas da notação.

**Impacto:** o fator A é alteração de parâmetro composta; não mede exclusivamente
assistência. A ablação que desliga somente assistência continua sendo teste
válido daquele mecanismo, condicionado ao restante do arranjo. O parecer vai
longe demais ao tratar todo contraste entre cenários como simples aritmética.
Não substituir dinamicamente a confiança nesta rodada.

### MAJOR-4 — PARTIALLY ACCEPTED

**Aceito:** a garantia marginal de Pukelsheim não fornece automaticamente
cobertura conjunta para o máximo com variâncias estimadas. **Rejeitado:** o
máximo ser, por si, um erro; é prática explícita no tutorial de Andrianakis.
Também não há motivo para exigir que todo observável informe F_ancora:
prazo é informativo sobre μ_minimo, outro parâmetro que se pretende calibrar.

Reproduzidos 205
pontos cujo máximo é prazo, e as contagens de aceitação por observável.
A regra conjunta preserva necessidade de ajuste simultâneo das saídas.
Não ponderar para produzir a contração desejada em um parâmetro.

**Cobertura empírica no vetor verdadeiro** (IC95 binomial exato):

| Observação | Variância | Exclusões | Fração | IC95 |
|---|---|---|---|---|
| publicada | legado | 2/20 | 10.0% | [1.2%; 31.7%] |
| publicada | pareada | 4/20 | 20.0% | [5.7%; 43.7%] |
| renovada | legado | 0/20 | 0.0% | [0.0%; 16.8%] |
| renovada | pareada | 3/20 | 15.0% | [3.2%; 37.9%] |

Na linha pareada contra a observação publicada, somente `V_sim` usa a estimativa
pareada; `V_obs` permanece o valor legado associado à observação fixa. Portanto,
essa linha é uma combinação híbrida, não uma reestimação pareada de ambas as
parcelas de variância.

Observação publicada fixa mede desempenho condicional àquela realização;
observação renovada testa o procedimento sintético conjuntamente. Os blocos
são independentes entre si; as instâncias dentro de cada bloco permanecem fixas
com sementes pareadas. Os intervalos são largos e não certificam cobertura
nominal. A forma alternativa de variância não foi promovida por produzir mais
ou menos rejeição. Evidência: `analise/cobertura_blocos.csv` e `...resumo.csv`.

### MAJOR-5 — PARTIALLY ACCEPTED

**Aceito:** caixa envolvente é resumo insuficiente para declarar convergência.
A fração condicional muda de 0.100 para
0.287, mas os domínios amostrados são distintos.
A segunda caixa de amostragem ocupa 0.173611
do volume original. Logo “quase triplicou” não compara o mesmo denominador.

**Rejeitado:** interpretar a fração rejeitada como volume exato da caixa, ou o
Jaccard de índices como sobreposição física. O Jaccard de índices foi reproduzido,
mas há zero vetores físicos exatamente comuns entre os conjuntos aceitos.
`ponto` é índice do desenho, não identidade persistente do parâmetro entre ondas.
A causa exclusiva proposta para estabilidade das larguras permanece aberta.
Evidência: `reanalise/caixas.csv`, `reanalise/jaccard.csv`.

### MAJOR-3 — PARTIALLY ACCEPTED

**Aceito:** a variância legada não explicita o estimando e mistura diferenças
entre instâncias com dispersão estocástica; a mesma semente também introduz
pareamento. **Rejeitado como regra geral:** que sempre seja obrigatório adicionar
instâncias para reduzir ruído da média de um conjunto fixo.

Para f(x) = média das esperanças das duas instâncias fixas, diferenças entre suas
esperanças não são incerteza Monte Carlo. A alternativa estima variância das
médias por semente / número de sementes, preservando covariância induzida pelo
pareamento. Para inferir uma população de projetos, a variabilidade entre projetos
passa a importar; isso é outro alvo e exige outra amostragem e observação.

Teste sintético: offsets determinísticos entre instâncias resultam em variância
Monte Carlo zero na alternativa, positiva no estimador legado. Outro controle
verifica a covariância de sementes. **UNRESOLVED:** reproduzir os percentuais
específicos de decomposição do parecer sem sua fórmula; uma ANOVA explícita por
célula produziu valores diferentes, preservados em
`reanalise/decomposicao_variancia_legada.csv`. Não se usou essa discrepância para
negar a necessidade de rever a agregação.

### MAJOR-1 — ACCEPTED, com correção de um exemplo

A branch anterior não incluía todas as evidências históricas descritas.
A ressalva “estado local” não bastava para facilitar auditoria externa.
Porém `outputs/tables/modelo_04_hm_onda2.csv` já existia; o uso de apelido no
texto não prova ausência do arquivo.

**Ação:** índice de 90 arquivos com hashes e commits de origem, e
recuperador testado. A base histórica pode ser obtida sem merge da autora nem
cópia indiscriminada de outputs na branch nova. O parecer e os documentos
insubstituíveis estão versionados nesta branch. Consulte
[EVIDENCE_INDEX](../research/EVIDENCE_INDEX.csv) e [REPRODUCAO](../research/REPRODUCAO.md).

### MAJOR-2 — PARTIALLY ACCEPTED

**Aceito:** a versão oficial local não tinha snapshot no Git consultado.
**Correção factual:** o tamanho e hash atuais diferem do tamanho relatado pelo
revisor; a cópia preservada tem o hash documentado em SOURCES.
**Rejeitado:** desautorizar a designação do arquivo oficial por ser supostamente
apenas autoatestada. A autora forneceu essa instrução diretamente nesta conversa.

**Ação:** snapshot byte a byte versionado, sem editar original ou sobrescrever
`docs/entrega1_...docx` da branch. O snapshot do TCC I preserva a fonte conceitual
usada. **UNRESOLVED:** equivalência entre gerador e DOCX oficial; o snapshot
resolve preservação, não geração automática fiel.

### MAJOR-6 — PARTIALLY ACCEPTED

A correção sobre os cenários nominais permanece válida. Deve ficar explícito
que o empate cruzado explica por que trocar apenas tau_min não abre o portão
naquela célula e por que a desigualdade estrita cria a descontinuidade.
O acesso à evidência de B9 foi restabelecido por commit no índice.
O efeito nulo do parâmetro naquele fatorial não demonstra irrelevância geral.

### RNG/B5 — ACCEPTED; prioridade revista

A repetição normalizada continua confirmada pelo diagnóstico reproduzível
publicado anteriormente. Não deve ser usada para validar refinamento independente.
Corrigir a semente é necessário, mas não basta para interpretar as larguras.
A prioridade de novas ondas completas fica abaixo de estimando, observação e
cobertura. Não é necessário esperar todos esses estudos para reconhecer o defeito.

## Conclusões anteriores que mudaram

| Conclusão anterior | Nova evidência | Nova conclusão |
|---|---|---|
| Só o produto é observado; colapsar os fatores | Contraste pareado com produto constante altera omissão | Não descartar o canal separado de frequência; identificabilidade global ainda aberta |
| Larguras estáveis provam limite estrutural e dispensam outra onda | Desenho dependente, caixas condicionais e sensibilidade real à precisão | Convergência e causa estrutural não demonstradas |
| τ_inicial age só por assistência | Intervenções isoladas no portão e na rede produzem efeitos | A é parâmetro composto; interpretar por mecanismos separados |
| Nova onda independente é a próxima investigação mais informativa | Mais réplicas rejeitam inclusive o vetor verdadeiro contra z publicado | Priorizar alvo observacional e critério de incerteza antes da onda completa |

O DOCX oficial já continha ressalvas e não foi reescrito. A correção do relatório
não regenera resultados históricos. Os limiares descritivos de largura continuam
rotulados como convenções legadas, sem inferência estrutural.

## Alterações implementadas e verificação

- Scripts experimentais separados; nenhuma nova lei de confiança, risco ou
  retrabalho incorporada ao simulador nominal.
- Relatório HM requalificado: removidas afirmações falsas e garantia conjunta
  indevida; mantida a tabela numérica idêntica em teste de regressão.
- Teste do relatório falhou antes da correção pela conclusão categórica antiga
  e passou após a mudança. Controles sintéticos verificam o estimador alternativo.
- Vértices da caixa testados, sem truncamento nesta amostra. Isso não certifica
  todo o espaço, todas as sementes ou outras instâncias.
- Fontes primárias consultadas e limites registrados em [SOURCES](../research/SOURCES.md).
- Revisão do diff, nova reprodução e preservação do checkout original fazem
  parte do gate de publicação. Os hashes protegidos e MERGE_HEAD são verificados.

## Backlog após este ciclo — continuar daqui

1. **Alvo observacional e cobertura:** separar média condicional, saída de um
   projeto e população de projetos; avaliar z publicado em amostras independentes
   e a estabilidade de V_obs/V_sim. Não escolher pesos ou corte pelo NROY menor.
2. **Avaliação da alternativa de variância:** comparação em mais blocos
   independentes previamente definidos; precisão do estimador e cobertura fora
   da amostra usada no piloto. Ainda não promovida ao pipeline nominal.
3. **Informação por parâmetro:** desenho local de sensibilidade e perfis sobre
   observáveis separados; comparar custo/benefício antes de busca ou otimização.
   O produto não deve substituir prematuramente os fatores.
4. **Ondas independentes:** corrigir RNG e guardas; relatar domínio amostrado,
   aceitação, resolução e incerteza sem usar somente casco. Sem rodada completa
   enquanto critérios anteriores permanecerem mal definidos.
5. **Confiança:** ampliar os contrastes de canais se necessário; a formulação
   dinâmica é alternativa futura, não correção presumida. Manter distinção entre
   parâmetro, mecanismo e consequência endógena.
6. **Retrabalho/prazo, generalização e inferência NASA:** continuam importantes;
   atacar em ciclos separados, com referência preservada e perguntas definidas.
7. **Documento oficial vs gerador:** preservar snapshot; medir diferenças antes
   de qualquer regeneração e recuperar rastreabilidade editorial.

Não há evidência neste ciclo que justifique introduzir IA, emulador ou algoritmo
de otimização específico. A limitação atual é definir e testar a inferência.
