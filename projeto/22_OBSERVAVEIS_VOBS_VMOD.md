# Observáveis e início da especificação de V_obs/V_mod — 17/09/2026

> **V_obs/V_mod PAUSADO por instrução da autora.** T1/T2/T3 devem ser concluídos antes de qualquer retomada. Este arquivo registra um contrato, não autorização para novas ondas.

## 1. Decisão de interpretação

[DEC] Retirada a conclusão de governança baseada em `E_total`, inclusive a inversão
de seu contraste. É uma grandeza diagnóstica interna que soma, no denominador,
TW em períodos de trabalho, TL em eventos de ajuda (unitário) ou incrementos
contábeis da Eq. 3, TU em períodos bloqueados e TR em esforço. Não foi estabelecida
uma conversão comum dessas unidades. Toda nova apresentação do diagnóstico deve
mostrar as duas convenções de `lei_tempo_aprendizado`; nenhuma é eleita pelo sinal.
Os números históricos permanecem nos artefatos originais, sem uso conclusivo.

Os contrastes de governança **dentro da família simulada declarada** foram descritos por
menor `atraso_relativo`, menor fração de falhas não reportadas e menor pico de dívida
latente. Não é conclusão empírica sobre projetos externos. A interpretação agora deve
considerar o [bloqueio de premissas de T2](24_TESTES_ARRANJO_T1_T2_T3.md): esses
contrastes não isolam um efeito de governança independente das premissas de reporte.

## 2. Verificação reproduzível da independência de TL

Tabela gerada por `research/verificar_independencia_tl.py` a partir dos CSV
publicados, sem novos experimentos ou mudanças de parâmetros:

| Indicador | Pares TL idênticos | Contrastes negativos | IC95 inteiramente negativo |
|---|---:|---:|---:|
| retrabalho_sobre_esforco_realizado | TR / (TW+TL+TU+TR), denominador de unidades distintas | Mesma contabilidade interna de E_total; mudou entre convenções TL; ainda aparece como DIAGNOSTICO em 05_figuras_modelo.py | **Excluída**, pelo mesmo motivo de E_total |
| atraso_relativo | 384/384 | 129/129 | 128/129 |
| taxa_omissao | 384/384 | 129/129 | 129/129 |
| divida_latente_sobre_plano | 384/384 | 129/129 | 129/129 |


[DEC] A coluna de pares refere-se ao nominal nas duas convenções; a robustez
refere-se ao lote histórico de configurações, que não foi reexecutado nesta etapa.
Não confundir sinal da estimativa com intervalo inteiramente negativo.
O runner original já comparou estados, trajetórias e RNG por bits; esta verificação
reconfere explicitamente os três resultados a partir dos CSV. Adulterar cada
indicador em uma réplica foi detectado pelo verificador (controles negativos).

A inspeção de `simulador_mvp.py::contabilizar_tempo_aprendizado` confirma que a
alternativa modifica apenas o acumulador TL, sem alterar relógio, capacidade,
sorteios ou decisões. Em `simulador.py::_resultado`:

- `atraso_relativo = makespan / makespan_cpm` (derivado pelos runners);
- `taxa_omissao = n_com_erro / número_de_tarefas`;
- `divida_latente_sobre_plano = max_t S_UR(t) / E_plano`.

Nenhuma fórmula usa TL; os numeradores e denominadores não são afetados pela
convenção. A invariância estrutural vale para essa alternativa implementada;
a verificação empírica cobre os pares declarados, não uma nova varredura inteira.

Reprodução: `python3 research/verificar_independencia_tl.py`.
Evidência, escopo e hashes dos dados: `outputs/diagnosticos/observaveis_20260917/`.

## 3. Contrato de medição antes de V_obs

[DEC] O vetor externo z ainda **não está habilitado**. O vetor de quatro grandezas
em `04_gemeo_identico.py::OBSERVAVEIS` pertence ao teste sintético histórico, não
é um vetor aprovado para calibração real. Seu código e resultados são preservados;
a caracterização antiga como grandezas diretamente registradas em projetos foi
retirada do comentário. Nenhuma nova onda de History Matching foi executada.

| Grandeza candidata | Unidade e denominador | Fronteira do sistema e regra de contagem | Admissibilidade em z externo |
|---|---|---|---|
| E_total | Mistura trabalho, eventos/incrementos TL, bloqueio e esforço | Contabilidade interna acumulada até o término; quociente de acumuladores | **Excluída**: depende da convenção interna de TL e não tem ponte comum de unidades |
| atraso_relativo | Razão de períodos simulados; makespan / makespan_sem_recursos | Projeto simulado até término absorvente, incluindo reparos/dívida; base é limite inferior CPM de precedências sem restrições de recursos | **Não admitida atualmente**: não equivale a crescimento de prazo sobre cronograma aprovado; não usar percentuais de atraso da literatura como z |
| taxa_omissao | Tarefas com falha não reportada / tarefas modeladas | Rótulo histórico concluida_com_erro, mesmo após reparação; cada tarefa contada uma vez, não cada tentativa; não é frequência P1 nem taxa total de defeitos | Candidata condicionada à mesma unidade tarefa/entrega e auditoria de falhas não reportadas; registros só de defeitos reportados não identificam esse alvo |
| retrabalho_sobre_plano | Esforço TR / soma das durações nominais E_plano | Retrabalho acumulado até encerramento; esforço debitado pelo modelo, distinto da duração inteira reservada ao reparo; não custo monetário | Candidata condicionada à equivalência entre esforço simulado e esforço externo, escopo de retrabalho e base planejada comparáveis |
| divida_latente_sobre_plano | Pico do estoque de esforço oculto / E_plano | Máximo da trajetória S_UR amostrada ao fim dos períodos, não estoque final nem total de defeitos | Diagnóstico interno por ora: exige observação longitudinal independente do estoque oculto e mesma frequência de amostragem |

[ABERTO] Mesmo uma razão adimensional pode comparar coisas diferentes. Para atraso,
substituir CPM por prazo contratado mudaria o observável: requer uma nova definição,
fonte de baseline, unidade temporal, tratamento de calendário/recursos e fronteira
de entrega/reparos. Deve entrar como alternativa explícita e preservada; não se
rebatiza o quociente atual como crescimento de prazo. Invariância a TL é necessária
neste diagnóstico, mas não suficiente para validade observacional.

### Estatística de extremo e horizonte endógeno

[LIMITACAO] `divida_latente_sobre_plano` usa um pico. Para uma sequência de
observações ampliada por inclusão de amostras, o máximo é não decrescente e sua
esperança pode aumentar com o número de oportunidades de amostragem, mesmo sem
mudança de mecanismo. No modelo, o horizonte depende da própria dinâmica.
Comparações externas exigem igualar também o número de amostras (e a janela,
cadência, fronteira e mecanismo de observação), não apenas o intervalo entre elas.
Essa propriedade não prova que diferenças de pico entre processos distintos sejam
somente viés de duração. Quantificar essa parcela exige desenho com janela/número
de amostras comparáveis, sem cortar silenciosamente as trajetórias históricas.

## 4. V_obs, V_sim e V_mod — especificação inicial, sem valores arbitrários

[DEC] Para cada coordenada que vier a ser admitida, registrar antes de estimar:
fonte e população; unidade amostral independente; janela de observação; numerador
e denominador; baseline; fronteira de encerramento; faltantes/censura; mecanismo de
reporte/detecção; conversões e evidência de que medição externa e modelo coincidem.
Observável dependente de convenção interna fica fora de z. Não mascarar a
incompatibilidade de unidades ou fronteiras aumentando V_obs ou V_mod.

- **V_obs:** incerteza do estimador externo na escala do observável (unidade ao
  quadrado), incluindo amostragem e medição identificáveis. Para média de projetos,
  a unidade independente é projeto; tarefas e sementes não aumentam artificialmente
  esse n. Distinguir dispersão entre projetos de incerteza da média. Para razões,
  preservar a dependência entre numerador e denominador e o estimando escolhido
  (média das razões versus razão dos totais). Registrar covariâncias se houver
  dados conjuntos, sem assumir independência silenciosamente.
- **V_sim:** erro Monte Carlo da estimativa simulada para o mesmo estimando;
  separar variação entre instâncias e réplicas dentro da instância. Não reutilizar
  automaticamente var/n do lote sintético como incerteza observacional externa.
- **V_mod:** discrepância entre modelo e sistema observado após compatibilizar a
  medição. Declarar mecanismos omitidos, escala e evidência independente que possam
  informar sua magnitude; manter separada de V_sim e V_obs. Não fixar zero por
  conveniência nem ajustar para manter parâmetros desejados no NROY.

[ABERTO] Valores e forma de dependência ainda não especificados: não há nesta etapa
base observacional compatibilizada que autorize atribuí-los. A soma das parcelas
no denominador da implausibilidade requer hipóteses de independência declaradas;
se não forem defensáveis, tratar a dependência explicitamente antes de executar HM.
History Matching permanece o método; perfil de implausibilidade vem depois do
contrato observacional, sem escolher parâmetros para obter sinal esperado.

## 5. Próxima questão e preservação

Próxima tarefa: auditar as fontes externas já presentes no projeto contra o contrato
acima, começando por esforço de retrabalho e falhas não reportadas. Para cada fonte,
registrar inclusão/exclusão e o estimando realmente observado. Só então propor z,
V_obs e a evidência para V_mod. Se nenhuma fonte satisfizer o contrato, declarar
insuficiência dos dados, sem preencher o vetor com proxies internos.

Os relatórios 11, 19 e 21 tiveram a leitura corrigida a pedido da autora; números
brutos e manifestos históricos permanecem intactos. Hashes de documentos nesses
manifestos referem-se aos commits históricos, não ao texto revisado atual.

## 6. Plano B metodológico — D-12, antes de avaliar padrões

[DEC] Se nenhuma fonte satisfizer o contrato observacional, a rota será **modelagem
orientada a padrões**, conforme a estratégia geral de
[Grimm et al. (2005)](https://www.usgs.gov/publications/pattern-oriented-modeling-agent-based-complex-systems-lessons-ecology).
O artigo oferece uma estratégia de desenho e avaliação de modelos baseados em
agentes; não fornece padrões ou faixas quantitativas para este projeto. Os
padrões abaixo são candidatos deste trabalho, não conclusões já confirmadas.
Não se substitui History Matching por um algoritmo alternativo nem se produz
calibração numérica sem observáveis compatíveis.

| Padrão candidato a reproduzir | Medição e contraste que discriminam mecanismos | Critério de sucesso proposto antes da avaliação |
|---|---|---|
| Compromisso entre tempo de execução e falha sob pressão | Mesma unidade tarefa e estratos de dificuldade; duração e falhas efetivas, não falhas ocultas; evidência humana de pressão temporal deve ter transporte de construto declarado | Reproduzir conjuntamente a direção tempo–erro observada em dados independentes, com IC95 do contraste na direção registrada; usar faixa quantitativa somente se unidades e fronteiras forem compatíveis |
| Descoberta tardia de defeitos e concentração posterior de retrabalho | Séries de eventos de descoberta e esforço de reparo; defasagem e distribuição temporal, com janela/número de amostras fixados | Reproduzir a ordenação temporal e a faixa de defasagem extraída de uma fonte independente antes da execução; não contar a própria regra de detecção/reparo do código como validação |
| Assistência limitada pela disponibilidade e pela competência relativa | Pedidos enviados, atendidos e não atendidos separados de bloqueios; carga dos respondentes e ganhos do solicitante | Reproduzir a direção da relação entre carga/disponibilidade e atendimento e a relação entre hiato de competência e aprendizado, ambas aferidas externamente; discriminar nominal de alternativas sem restrição de disponibilidade ou sem filtro de competência |

[DEC] Sucesso global exige que uma mesma configuração preservada reproduza
simultaneamente os padrões externos admitidos, em instâncias/sementes reservadas
para avaliação, sem escolher uma configuração diferente para cada padrão. Antes
de avaliar, registrar fonte, estimando, sinal/faixa, nível de agregação, incerteza,
janelas e casos de exclusão. Critérios e tolerâncias não serão relaxados após ver
os resultados. Ausência de evidência externa para um padrão impede marcá-lo como
validado; padrão contradito ou teste inconclusivo será reportado como tal.

Controles de identidade, conservação, contrafactuais de porta e invariância a TL
continuam necessários, mas são verificações internas, não padrões externos.
Não exigir vantagem de um arranjo como critério de sucesso: isso imporia a conclusão.
A seleção definitiva das fontes/padrões aguarda T1/T2 e o encerramento da pausa.
