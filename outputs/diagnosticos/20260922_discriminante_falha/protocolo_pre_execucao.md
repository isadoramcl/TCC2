# 78 — Causa da falha efetiva na v2: teste discriminante

## Pré-registro — escrito antes de qualquer execução deste experimento

Clone independente `~/TCC2_discriminante`; execução no Mac autorizada pela autora em substituição ao Windows. Nenhum ajuste de parâmetros, alteração dos dois YAML nominais ou operação de publicação Git.

**Desenho:** 20 pares sorteados sem reposição dos 643 com contraste positivo na v2 (universo recontado independentemente), mais o par nominal. Semente 20260922, `random.Random.sample` sobre pares ordenados por `ai,ci`; seleção integral em `amostra.csv`. Quatro instâncias e sementes 0–3 da grade original. Canto 00 = limiar/constante; 10 = logístico/constante; 01 = limiar/logística; 11 = logístico/logística. Todas as demais opções vêm de `config/mvp.yaml`; instrumentação de tarefas desativada como nas grades. Execuções repetidas de um mesmo perfil/braço são reutilizadas entre pares, sem tratá-las como replicações adicionais.

**Porta de validade:** reexecutar primeiro 00 e 11; comparar TODOS os campos arquivados por chave, usando `float.hex()` nos números e igualdade nos demais, com leitura `float_precision='round_trip'`. Qualquer divergência interrompe o teste antes de interpretar e antes dos cantos mistos. Sem tolerância numérica. Censura ou violações impedem conclusão mecanística irrestrita.

### Hipóteses e resultados que as confirmariam ou derrubariam

Seja Dgf = falha adaptativa − centralizada no canto gf; negativo favorece adaptativa. Chamaremos inversão v1→v2 apenas D00<0 e D11>0; pares já positivos em 00 não são novas inversões. Sinal pontual e IC serão apresentados separadamente. IC que contém zero implica incerteza; não prova ausência de efeito.

- **H1 (assistência melhora o centralizado):** sustenta-se por célula se abrir apenas assistência eleva D (D10−D00>0), reduz a falha centralizada e essa redução é maior que a adaptativa; N_req/N_success centralizados devem crescer. É suficiente para inversão se D00<0<D10. Derrubada como explicação dessa célula se D10 não aumenta D ou se o deslocamento vem só do adaptativo piorando, sem melhora centralizada. IC95 do efeito e mudanças por braço medem a força da evidência. Repetir efeito da assistência com fuga ligada (D11−D01).
- **H2 (fuga altera o denominador/seleção de tarefas):** requer que ligar fuga mude o denominador real da taxa e as tarefas executadas, e desloque D em direção positiva. O código lido antes da execução define o denominador como `len(tarefas)` da instância: se a contagem continuar fixa e todas as tarefas terminarem, H2 é derrubada **na forma proposta**, mesmo que a fuga tenha efeitos no numerador, no tempo ou na porta de execução. Registrar numerador, denominador, conjunto de IDs executados e concluídos nos quatro cantos. Não confundir adiamentos com novas tarefas.
- **H3 (só os dois juntos):** sustenta-se descritivamente quando D00<0, D10<=0, D01<=0 e D11>0. Cai como necessidade conjunta se algum canto isolado já inverte. Estimar interação J=D11−D10−D01+D00 com IC95: só IC inteiramente positivo sustenta sinergia positiva; cruzamento apenas no canto conjunto pode ser soma de efeitos, não interação demonstrada. Se IC incluir zero, interação permanece inconclusiva.

**Análise:** para cada par e canto, diferença pareada por (arquivo,semente); média das quatro sementes por instância; IC t de Student com 4 instâncias, 3 graus de liberdade. Mesma construção para efeitos fatoriais, interação e mudanças por braço. Não usar 16 sementes como N independente. IC95 individuais, sem correção de multiplicidade. Os 20 pares foram selecionados pelo desfecho na mesma grade: análise diagnóstica condicionada, não nova validação nem estimativa da prevalência de inversões. Não agregar pares como observações independentes.

**Leituras:** taxa de falha=(n_com_erro+n_reportadas)/n_tarefas; número executado = tarefas com início registrado, com confirmação por p1_omissao+p3_analitica. Fração P1 = omissões/(omissões+analíticas); fração de fuga = fugas/(fugas+omissões+analíticas), excluindo tentativas P2; publicar também fugas/(fugas+omissões). Pedidos N_req, sucessos N_success, insucessos N_fail, bloqueios prévios N_blocked. Bateria média = média temporal dos estados médios dos agentes registrados ao fim de cada período, com igual peso por execução/instância, não um pool que sobrepese execuções longas. Confiança final = média dos agentes ao término.

**Limite de atribuição:** assistência e fuga usam um mesmo fluxo auxiliar; mudar um canto muda o consumo subsequente desse fluxo, e decisões afetam o fluxo principal por realimentação. Sementes comuns garantem replicação, não alinhamento de sorteios por evento. O fatorial identifica o efeito da troca de opções na implementação, não isola mediação por cada evento.

**Ambiente:** NumPy/pandas alinhados ao requirements; SciPy 1.18.1 para IC, pois scipy==1.15.3 exige numpy<2.5 e o requirements fixa numpy==2.5.2. Não foi alterado o requirements. Versões exatas e hashes em manifesto_pre_execucao.json.

## Resultados

PENDENTES — pré-registro preservado em `protocolo_pre_execucao.md` e por hash.
