# MVP — implementação, robustez e resultados

> **PRÉ-CORREÇÃO ESTRUTURAL — congelado em 16/09/2026.** Números históricos preservados; não constituem resultado do MVP corrigido nem alimentam conclusão final sem reexecução. Ver `research/CONGELAMENTO_PRE_CORRECAO.json` e `research/PLANO_CORRECAO_ESTRUTURAL.md`.

**Estado: software e passada declarada de robustez concluídos.** Duas leis de
confiança permanecem candidatas; a escolha aguarda orientação da autora.
Calibração e fragilidades são a próxima etapa, juntas. Nenhuma nova onda HM,
troca de método ou busca por melhor política foi feita.

## 1. Entregas e proteção

| pedido | entrega |
|---|---|
| Preservar/reconciliar e rebasear | Três arquivos vivos copiados com SHA-256 em `research/preservacao_rodada2`; conteúdo reconciliado sobre main `dc8721f` |
| Instrumentação | Cabeçalho corrigido, prioridades e estrutura atualizadas, verificador de DOCX falha em ausência/divergência |
| C4 | Duração da omissão reduzida, fator explícito e família {0,50; 0,75; 1} |
| C1 | Fila real de reparos, agente e recurso ocupados, conservação gerado=pago+pendente |
| C3 | Constante + média de eventos + saldo de eventos; nenhuma lei eleita |
| A11 | Quatro esquemas YAML efetivamente propagados a Di e quartis; controle 1/3 histórico preservado |
| A10/B6 | Mesmo estado/RNG até término absorvente; limite de segurança censurado; teste de extensão e horizonte inicial dobrado |
| Porta 2 | Família finita de quatro regras, incluindo as três ablações existentes |
| Governança | Contrastes em 36 células (9 pontos × 4 pesos), além de complementos declarados |
| B9 e fatorial | Repetição B9 e 2⁵ com portão e rede separados; tabelas completas ANTES/CONTROLE/DEPOIS |

O checkout da autora não foi alterado: os três hashes vivos e o hash do DOCX
continuam iguais aos preservados. Main permanece `dc8721f`; esta publicação
fica na branch `codex/resposta-revisao-cientifica`, sem merge em main.

## 2. Verificação

- 19 testes automatizados passaram, incluindo censura, conservação, capacidade, confiança e hash.
- Clone limpo de dd29e29: os 19 testes passaram, 90 evidências históricas foram recuperadas e nove tabelas consolidadas foram regeneradas sem qualquer diferença numérica.
- Revisão independente do núcleo, desenho e consolidação concluída; correções de TW em censura e dívida zero foram reproduzidas por testes antes do conserto.
- 17.920 execuções novas: 3.072 alternativas, 1.408 robustez, 12.288 canais e 1.152 B9.
- Todas terminaram sem trabalho/dívida pendentes e sem violações.
- As 384 linhas do experimento legado foram reproduzidas sem diferença numérica.
- As 3.072 diagonais G=N reproduzem o fatorial antigo; diferença máxima de ponto flutuante 1,42×10⁻¹⁴.
- Dobrar o horizonte inicial produziu saídas substantivas idênticas nos 32 pares de execuções correspondentes.

## 3. Antes/depois do contraste principal

Diferença = adaptativa − centralizada. Mesmas 16 instâncias e 12 sementes.
MVP nesta tabela = C4+C1, τ constante; leis candidatas são braços separados.

| métrica | ANTES legado | DEPOIS C4+C1 | IC 95% do contraste depois |
|---|---:|---:|---|
| atraso_relativo | -1.135399 | -1.154039 | [-1.295486; -1.012592] |
| taxa_omissao | -0.153299 | -0.165538 | [-0.175840; -0.155236] |
| divida_latente_sobre_plano | -0.053983 | -0.056758 | [-0.061317; -0.052200] |
| retrabalho_sobre_plano | -0.048631 | -0.045743 | [-0.055162; -0.036325] |
| E_total | 0.104631 | 0.131083 | [0.116536; 0.145630] |

A reserva de ambos os participantes da ajuda é uma correção separada de C4.
O controle do motor mede essa diferença: atraso adaptativo 1,999133 no legado,
2,023489 no controle, 1,728878 com C4 e 1,882540 ao acrescentar C1. Portanto,
não se atribui toda mudança ao fator de omissão. O controle de horizonte
automático coincide com o controle fixo neste desenho.

O reparo disputa capacidade e acrescenta custo tardio; isso implementa o
mecanismo faltante de soluções sintomáticas. Não é prova de que um arquétipo
se manifeste com qualquer parâmetro nem de que a omissão sempre seja vantajosa.

## 4. Robustez do resultado principal

Família definida antes de simular: oito vértices de F_ancora∈{0,05;0,25},
f_retrabalho∈{0,30;0,80}, μ_min∈{0,40;0,70}, mais centro, cruzados com quatro
pesos Di do YAML. Quatro instâncias e quatro sementes por cenário em cada célula.

| métrica | menor contraste entre células | maior contraste | IC inteiramente abaixo de zero |
|---|---:|---:|---:|
| atraso_relativo | -1.364084 | -0.581860 | 36/36 |
| taxa_omissao | -0.370833 | -0.060417 | 36/36 |
| divida_latente_sobre_plano | -0.178358 | -0.013267 | 36/36 |
| retrabalho_sobre_plano | -0.074027 | 0.002446 | 7/36 |
| E_total | 0.003189 | 0.200902 | 0/36 |

**Conclusão sustentada neste domínio:** o contraste de atraso, omissões e
exposição à dívida oculta manteve a direção nas 36 células. Isso não se estende
automaticamente ao retrabalho pago: seu contraste muda de sinal em parte do
desenho. E_total é um índice contábil, não eficiência; também possui mais
heterogeneidade entre instâncias. Nenhum caso foi removido para reforçar a conclusão.

Os complementos de Porta 2, confiança e fator de omissão foram comparados no
centro. Eles não cobrem todas as interações entre leis, pesos e vértices.
Quatro instâncias dão intervalos pouco precisos; os IC são pontuais, sem
garantia simultânea. Interior contínuo, outros fatores e validação externa
permanecem fora da passada pequena declarada. Não há ranking ou política eleita.

## 5. Atribuição de B9 e canais

G move o portão de ajuda; N move a entrada de confiança do multiplicador de
rede. O multiplicador cognitivo direto recebe fadiga/pressão, e não τ.
Logo “canal cognitivo” na revisão anterior não é o nome correto de N.
Os grupos abaixo somam todos os termos com G sem N, com N sem G, com ambos
ou sem ambos. Incluem interações com B/C/D; são uma partição algébrica do
contraste nestes níveis, não percentuais universais de causalidade.

| modelo / atraso | G sem N | N sem G | G e N | outros |
|---|---:|---:|---:|---:|
| legado | 24.76% | 32.44% | 2.66% | 40.14% |
| mvp | 11.08% | 22.95% | 7.06% | 58.91% |

No MVP sem assistência, TL é zero nos dois cenários, mas o contraste de
atraso continua −0,944721 (81,86% do nominal). O contraste de TU inverte
para +17,239583. Esses são efeitos de intervenções distintas, não uma única
“fração da assistência”. No fatorial, parcelas podem ultrapassar 100% ou ter
sinais opostos, pois há compensação entre termos.

As tabelas detalhadas mapeiam cada coluna numérica de B9 e do fatorial
publicado. O fatorial antigo continua comparável pela restrição G=N; o 2⁵
completo tem 31 termos, documentados separadamente.

## 6. Ressalva de valores-p e interpretação da rodada 2

O ambiente efetivo usa SciPy 1.11.4; requirements.txt geral fixa 1.15.3.
Alguns valores-p mudam mesmo ao reexecutar o código antigo sobre o CSV antigo.
Confirmou-se seleção automática diferente entre procedimento exato e aproximado
em um exemplo; empates/zeros e arredondamento também importam. As tabelas
incluem CONTROLE_mesmo_ambiente e delta_vs_controle. Não atribuir esses deltas
ao novo modelo, nem usar redução de p como evidência de melhoria.

O piloto anterior refutou a suficiência universal do produto F×f. Não provar
diferença nos outros observáveis não demonstra suficiência exata nesses canais.
O vetor verdadeiro foi excluído em K=64 contra z publicada; média finita não
prova exclusão permanente. As oito escolhas de fronteira não estimam volume
ou largura global do NROY. Essas ressalvas permanecem junto dos resultados.

## 7. Próxima etapa autorizada após o MVP

1. Tratar V_obs/V_mod e adequação do alvo observacional, sem escolher valores para passar no teste.
2. Implementar e avaliar implausibilidade perfilada como diagnóstico dentro de HM; distinguir limitações práticas e estruturais com evidência.
3. Tratar conjuntamente as fragilidades: inferência/empates, retrabalho, dependência dos pesos e das leis, generalização além da família discreta.
4. Aguardar orientação para eleger uma lei de τ(t). Manter ambas executáveis.
5. Retomar novas ondas apenas depois de resolver V_obs/V_mod; preservar History Matching.

## Artefatos e reprodução

- [Comandos, ambiente e ressalvas](../research/REPRODUCAO.md)
- [Decisões do modelo](../docs/registro_de_decisoes.md#18-mvp-alternativas-preservadas-e-decisões-explícitas--16092026)
- [Resumo das verificações](../outputs/diagnosticos/mvp_20260915/consolidado/verificacoes.csv)
- [Antes/depois do experimento](../outputs/diagnosticos/mvp_20260915/consolidado/antes_depois_numeros_experimento.csv)
- [Antes/depois de B9 e fatorial](../outputs/diagnosticos/mvp_20260915/consolidado/antes_depois_numeros_B9_fatorial.csv)
- [Contrastes de robustez](../outputs/diagnosticos/mvp_20260915/robustez/resumo.csv)
- [Grupos dos canais](../outputs/diagnosticos/mvp_20260915/consolidado/atribuicao_grupos_canais.csv)
- [Hashes das evidências](../outputs/diagnosticos/mvp_20260915/consolidado/hashes_evidencias.csv)
