# Auditoria autônoma — 15/09/2026

## Escopo e estado de referência

[DEC] Primeira auditoria autônoma: reconstrução por documentação, inspeção de
código, inventário de tabelas e piloto do History Matching (HM). Não constitui
reexecução integral dos pipelines nem validação empírica do modelo.

O checkout estava em `main`, HEAD `8f27477`, com alterações da autora já
preparadas no índice. Não foram descartadas, incluídas em commit nem
sobrescritas. O DOCX também apresentou alteração adicional no diretório de
trabalho durante a sessão; ele não foi editado nesta investigação.
O diagnóstico se refere ao **conteúdo local**, identificado por SHA-256 no
[manifesto](../outputs/diagnosticos/hm_20260915/manifesto.json), e não somente ao HEAD.

As instruções atuais da autora estão em [07_AUTONOMIA.md](07_AUTONOMIA.md).
Elas prevalecem sobre as proibições antigas de commit/push, mas exigem revisão,
verificação e preservação de trabalho alheio antes de publicar.

## Arquitetura efetivamente encontrada

- **NASA:** `src/nasa/01..06` audita PROMISE e referências D′/D″, consolida
  módulos com origem rastreável, verifica a limpeza, ajusta modelos logísticos
  e estima risco por faixa. A complexidade é tratada como marcador ordinal;
  o registro informa ausência de efeito positivo após controle por tamanho.
  Essa inferência não foi recalculada nesta sessão.
- **PSPLIB:** `src/psplib/01..04` lê redes, durações e recursos, calcula CPM,
  folgas e índice Di, e transfere razões de risco por nível. NASA informa o
  gradiente RR; J60 fornece projetos sintéticos e restrições. Nenhuma das bases
  é dado observado de confiança ou de desempenho humano de equipes.
- **Configuração:** `parametros.yaml` declara premissas e parâmetros abertos;
  `parametros_derivados.yaml` sobrepõe equipe, horizonte e escala de pressão
  em `carregar_parametros`. Di é lido do CSV já processado; sua ponderação
  não é recalculada pelo simulador quando se altera o YAML.
- **Núcleo:** `simulador.py` mantém agentes com competência, bateria e confiança,
  tarefas com estados e precedências, recursos, pressão endógena e dívida de
  retrabalho. A cada período libera agentes, detecta dívida, atribui tarefas,
  aplica portas de decisão, drena/recupera bateria e registra trajetórias.
- **Inferência difusa:** `fuzzy.py` calcula multiplicadores cognitivo e de rede;
  a configuração atual usa produto e centroide, com reescala da produtividade.
- **Mecanismos relevantes:** confiança constante por cenário; aprendizagem
  permanente na assistência; filtro de apoiador mais competente; retrabalho
  contabilizado em TR sem realocação de agente; parada espera também a dívida.
  Portanto não se deve descrever o código como uma fila explícita de retrabalho.
- **Análise:** verificador, experimento pareado, gêmeo sintético/HM, ablações,
  fatorial e sensibilidades. `docs/gerar_entrega.js` produz a Entrega a partir
  de tabelas, figuras e trechos ainda literais. Não se editou a monografia.

A referência ao TCC I nesta auditoria usa a especificação e a conferência já
registrada em `06_B9_VERIFICACAO.md`. O PDF original foi localizado no diretório
TCC, mas não foi reauditado integralmente. Fontes bibliográficas tampouco foram
revalidadas nesta sessão; conclusões atribuídas a elas permanecem sob essa ressalva.

## Experimentos e evidências disponíveis

O [inventário](../outputs/diagnosticos/hm_20260915/inventario_tabelas.csv) registra
61 tabelas de nível superior, incluindo seus separadores. Tabelas de
entrega usam ponto e vírgula; ler todas como CSV separado por vírgula gera
falsos erros de parsing. Isso foi conferido antes de registrar um defeito.

| Família | Evidência preservada | Dimensão observada |
|---|---|---|
| Cenários | `modelo_03_experimento_bruto.csv` | 384 execuções, 16 instâncias, 12 sementes, 2 cenários |
| HM | `modelo_04_hm_onda1.csv`, `...onda2.csv` | 400 e 400 pontos; observação sintética separada |
| Ablação | `modelo_07_ablacao_bruto.csv` | 2880 linhas |
| Limiar de ajuda | `modelo_09_sensibilidade_tau_min.csv` | 2112 linhas |
| Fatorial | `modelo_10_fatorial_celulas.csv` | 3072 linhas |
| Pressão | `modelo_11_tendencia_piloto.csv`, `...confirmatorio.csv` | 800 e 2000 linhas |
| Porta de assistência | `modelo_12_porta2_bruto.csv` | 768 linhas |
| Inferência por instância | `modelo_14_experimento_por_instancia.csv` | 7 métricas, reanálise dos cenários |

Essas dimensões são inventário de artefatos, não contagem de novas execuções
nem garantia de independência estatística entre observações.

## Verificações e reconciliação do backlog antigo

**Presentes no código atual, sem nova execução integral nesta sessão:**

- A1: o script NASA de modelos agora grava a tabela de sobrevivência usada na figura.
- A2: `figura_10()` é chamada por `main()`, e a chamada de entrada ocorre após a definição.
- A4: scipy, matplotlib e PyYAML constam em `requirements.txt`; ambiente limpo
  ainda não foi validado. O ambiente usado no piloto tem versões diferentes
  das fixadas, registradas no manifesto.
- A6: padrões dos cenários foram ajustados ao artefato publicado.
- A7: a remoção do CSV órfão está preparada no índice da autora.
- A8: a docstring já retira a acusação de defeito de sinal no TCC I.
- B2: o verificador já contém teste em múltiplas instâncias e cenários.
- B7/B9: reanálise por instância, ablação e fatorial já têm código e tabelas.
  Não repetir como se ainda não tivessem sido feitos.

**Resultados de verificação salvos, não certificação nova:**
`modelo_02_verificacoes.csv` distingue invariantes, testes fracos e testes
contingentes à amostra. O crescimento de defeitos gerados sob pressão no
cenário adaptativo aparece como **NAO CONFIRMADA**; preservar esse resultado.
Os logs de pressão atribuem a diferença à dose endógena e ao canal de risco,
mas isso não transforma ausência de confirmação em prova de ausência de efeito.

## Backlog técnico-científico priorizado

Prioridade considera validade, dependência entre tarefas e risco de intervenção.
A ordem abaixo é de trabalho; não significa que o HM tenha mais consequência
conceitual que a representação do retrabalho.

| Ordem / item | Evidência atual | Próxima ação e critério de encerramento |
|---|---|---|
| 1 — B5, desenho HM | RNG reinicializado no `main` de `04_gemeo_identico.py`; dependência confirmada nos CSVs | Diagnóstico realizado abaixo. Integrar gerador por onda e guarda contra desenho repetido; preservar legado. Só reavaliar as conclusões após desenho completo independente. |
| 2 — A10/B6, integridade da calibração | Horizonte derivado do μ nominal; `rodar()` não exporta `concluiu`, dívida pendente nem violações | Instrumentar alternativa e testar extremos da faixa antes de nova rodada HM. Distinguir término de tarefas de término completo. Conferir I no vetor verdadeiro; marginais contendo a verdade não demonstram pertinência conjunta. |
| 3 — C1/B4, retrabalho e conservação | Detecção soma TR e retira dívida, sem tarefa residual; especificação §2 promete retorno à fila | Quantificar esforço, tempo e disponibilidade; avaliar fila de retrabalho em alternativa preservada. Corrigir divergência por decisão científica, não por harmonização cosmética. |
| 4 — C2, definição de prazo | `executar()` exige dívida vazia para parar, além das tarefas terminais | Instrumentar último término e fim da dívida; comparar ambas as medidas com pares idênticos antes de escolher a principal. Percentuais antigos de cauda ainda não reproduzidos aqui. |
| 5 — C3/Porta 2, confiança | Confiança só inicializada, comparação estrita com limiar; sensibilidade salva mostra dois regimes | Formalizar filtro de competência e explicitar domínio de validade. Dinâmica de confiança apenas como hipótese experimental justificada; não suavizar só para obter efeito esperado. |
| 6 — B8/B10, generalização | Seleção espaçada de instâncias em `03`; RR e âncora influenciam risco | Planejar amostra que cubra células e piloto pareado da âncora/gradiente, incluindo RR uniforme; expandir somente após pergunta e instrumentação definidas. |
| 7 — Inferência NASA | `smf.logit(...).fit(...)` sem covariância por agrupamento | Reavaliar precisão considerando projetos e pequeno número de grupos. Não afirmar antecipadamente que todo erro-padrão necessariamente aumentará. |
| 8 — A11, parâmetros declarados sem efeito | CSV de órfãos; pesos iguais implementados no script Di | Conferir consumo por caminho completo, separar configuração futura da efetiva e testar propagação antes de sensibilidades pelo YAML. |
| 9 — B11, métricas redundantes | `n_com_erro` coincide numericamente com número de tarefas vezes `taxa_omissao`; ambas seguem na tabela de reanálise | Definir uma como verificação de manipulação; investigar diferenças de p antes de reutilizar inferência das duas como evidências distintas. |
| 10 — C4/C5/C6 | Duração efetiva não distingue diretamente as portas; fuga condicionada a Ω; competência acumulada | Diagnósticos separados de tempo, ativação de fuga e reset de aprendizagem. Não atribuir efeitos a mecanismos inativos. |
| 11 — documentação e proveniência | README dizia simulador pendente (corrigido nesta publicação); registro §17.5 afirma convergência; especificação descreve fila ausente, agora sinalizados com nota de atualização | Atualizar a partir desta auditoria; retirar afirmações não sustentadas ao revisar a entrega. Auditar fontes e hashes externos em tarefa própria. |

**Precisão sobre o empate:** o YAML nominal centralizado usa `tau_inicial`
e `tau_min` distintos. A coincidência citada nos registros envolve níveis
cruzados entre cenários e pontos da varredura/fatorial; não descrever o cenário
centralizado nominal como se já tivesse igualdade entre os dois parâmetros.

## Primeiro ciclo: diagnóstico B5

### Problema, hipótese e teste discriminante

[HIPOTESE] Recriar o RNG com a mesma semente repete o hipercubo latino nas
coordenadas normalizadas de cada caixa. Normalizar ambas as ondas deve revelar
igualdade, mesmo quando os vetores em unidades físicas são diferentes.

O teste da exigência de desenhos diferentes **falhou no legado**, como deveria.
Um controle usando nova semente, com os mesmos limites e tamanho de desenho,
deve deixar de repetir as coordenadas, manter estratificação e reproduzir-se.
A tolerância numérica do detector está explícita no script e não é critério de
significância estatística.

### Alternativa experimental e comparação

[DEC] Script novo e isolado: `src/modelo/15_diagnostico_hm.py`. Reutiliza o LHS,
o simulador e a fórmula de implausibilidade existentes. Não altera parâmetros
nominais nem escreve nas ondas publicadas. Se a pasta de saída já existe,
interrompe em vez de sobrescrever.

Desenhos de sementes 20260905 e
20260915; índices fixados antes da simulação:
`[0, 57, 114, 171, 228, 285, 342, 399]`. Instâncias `['j6010_1.sm', 'j6032_1.sm']`, sementes do simulador
`[0, 1, 2, 3]`. Cada desenho usa a mesma caixa da onda legada.
O subconjunto dos pontos não é, por si, um LHS completo.

| Medida | Legado | Alternativa |
|---|---|---|
| Erro máximo contra coordenadas normalizadas da primeira onda | 1.22125e-15 | 0.985827 |
| Pontos do piloto | 8 | 8 |
| Pontos não descartados pelo corte preservado | 2 | 3 |

A amostra legada reproduziu as médias e variâncias publicadas com erro máximo
2.22045e-16. As 128 execuções concluíram
as tarefas, zeraram a lista de dívida e não registraram violações.
Todos os hashes de entrada conferidos permaneceram iguais.

### Conclusão e tentativa de refutação

[ACHADO] Confirmada a repetição do desenho normalizado. A semente distinta
elimina essa dependência determinística na alternativa. **Não é correto dizer
que a onda antiga não avaliou vetores novos:** a caixa mudou e os vetores físicos
mudaram. A falha é usar um desenho dependente como evidência de refinamento
independente.

[LIMITACAO] O piloto não estima convergência, não demonstra vantagem preditiva
da alternativa e não encerra B5. Diferença na contagem de pontos aceitos não é
medida de qualidade. A nova semente é escolha computacional explícita, não
calibração para aumentar aceitação. Não houve seleção de semente por resultado.

[LIMITACAO] Mesmo larguras semelhantes com outro desenho não provam
não-identificabilidade estrutural: o resultado depende também de observáveis,
variâncias, corte e domínio. O argumento de que só o produto é observável exige
revisão: o código acrescenta um termo cognitivo a `F_base`, e a taxa de omissão
é um observável separado do custo de correção. Uma crista empírica não equivale
a prova de invariância estrutural de toda a distribuição das saídas.

[LIMITACAO] Manter a agregação legada de variâncias isolou o efeito do desenho;
não validou essa agregação entre instâncias. Não observar truncamento neste
piloto tampouco exclui truncamento no restante do espaço.

### Reprodução e verificação final

```sh
python3 src/modelo/15_diagnostico_hm.py --saida /tmp/tcc2_hm_reproducao
```

Use uma pasta ainda inexistente. Consulte `manifesto.json`, `desenho.csv`,
`piloto_bruto.csv`, `piloto_resumo.csv` e `verificacoes.json` no diretório gerado.
As tabelas `comparacao.csv` e `inventario_tabelas.csv` anexas são resumos da
sessão; os dados e controles essenciais são produzidos pelo script.

**Próximo problema:** A10/B6 — testar término completo nos extremos do espaço
antes de investir em ondas independentes completas. Depois, corrigir a geração
por onda no pipeline e o texto de conclusão incondicional. O modelo nominal
permanece preservado enquanto essas hipóteses são investigadas.

**Publicação:** autorizada pela autora para README e divergências. Publicação
em branch de documentação, a partir de `origin/main`, sem concluir o merge
existente no checkout principal. Esta auditoria descreve o estado local, que
inclui código e tabelas ainda pendentes de integração. A publicação do registro
não representa resolução de B5 nem incorporação dessas alterações alheias.


## Documento oficial e retificação após conferência direta

[DEC] Por instrução explícita da autora, o documento oficial de análise
preliminar é a cópia local de `docs/entrega1_metodologia_resultados_iniciais.docx`.
O gerador e a versão remota não a substituem como referência de conteúdo.
Não regenerar sobre ela antes de comparar e preservar ajustes locais.

O texto do DOCX foi extraído de `word/document.xml` e conferido nesta sessão.
SHA-256 na leitura: `d5a658f1cdf03d99e6bdc0b5d03cb4aaa9420853ec7ebc2bb3f55e85a728c57d`.
A cópia local já apresenta o limite de identificabilidade como possibilidade,
sem descartar redução adicional por outro delineamento. Também declara
explicitamente que TR não ocupa agente nem disputa capacidade.

Assim, as divergências identificadas estão no relatório incondicional de HM,
no registro histórico e na especificação; não se deve atribuir aquelas
conclusões categóricas ao documento oficial local. Nenhuma edição do DOCX foi
realizada por este diagnóstico.

O checkout principal está em merge de `113c638` para `main`, com conflitos já
resolvidos e alterações preparadas. Esse estado foi confirmado antes da
publicação e será preservado. A cópia isolada de publicação é
`/private/tmp/tcc2-publicacao-auditoria`.


### Verificação sobre a base de publicação

O piloto também foi executado em checkout isolado de `origin/main` anterior à
publicação, sem o merge local. Os arquivos de desenho, resultados individuais,
resumos e verificações saíram **idênticos byte a byte** aos do estado local.
Os hashes de ambas as bases permanecem registrados; isso confirma reprodução
deste piloto, sem certificar igualdade entre todas as versões do simulador.
Ver `outputs/diagnosticos/hm_20260915/verificacao_publicacao.json`.
