# Correção estrutural do MVP — 16/09/2026

## Estado

Etapas 1–7 concluídas: 21.408 execuções de comparação/robustez/canais/B9 e
32 de instrumentação (21.440 no total), sem incompletas ou violações. O relatório 11,
B1/B3/B7/B9 e o lote `mvp_20260915` continuam congelados como pré-correção.

## Alterações isoladas

1. **Compatibilidade:** o próprio laço MVP neutro reproduz o legado nos campos
   publicados, trajetórias, estados de agentes/tarefas, dívida e RNG. O teste
   impede delegação ao executar legado. Trinta e dois pares nominais e cinco
   horizontes de fronteira; corrigido teto automático que vazava para modo fixo.
2. **C4:** preservado p0; omissão reduz duração e recebe excesso dependente de
   q=max(0,2*p_heu−1), p_fail=1−(1−p0)(1−rho*q). A fonte humana de rho é
   transporte de construto declarado, não calibração de tarefas de engenharia.
   O fator temporal continua decisão aberta, varrida; não foi derivado do estudo
   cujo prazo era imposto pelo experimentador.
3. **Contrafactual:** mesma tarefa/estado/sorteios, forçando P1 e P3; o caso com
   sobrecarga detecta menor duração e maior risco. Fator1/rho0 não detecta efeito.
   Médias observadas por porta não foram usadas como teste causal.
4. **Crowder:** Eq. (4), p. 1431 do PDF local, com competência original em 0–5:
   dC=clip((15+3*(5*Cp−5*Cr))/100,0,0.30); incremento de C normalizada=dC/5;
   tau normalizada aumenta tau*dC no sucesso ou cai 0,01 no insucesso.
   Respondente recebe a atualização. Bloqueio pré-pedido não altera tau.
   N_req=N_success+N_fail; N_blocked separado. Mesma lei nos dois cenários.
5. **C6 e canais:** competência reinicia na conclusão ou troca de subtarefa;
   confiança não reinicia. Overrides de portão/rede são condições iniciais e
   evoluem separadamente pelos mesmos eventos; as diagonais devem reproduzir
   o nominal. O documento 18 contém “reset da confiança”; prevalecem instrução
   da autora e fonte primária, ambas indicando competência.
6. **Instrumentação:** uma linha por oportunidade elegível, inclusive P2/fuga;
   registra estados, seleção, riscos e duração, sem novos sorteios. Não equivale
   a replay completo, pois sorteios de reporte/detecção não são exportados.

[DEC] Foi mantido destinatário único por tentativa (melhor elegível disponível;
se todos ocupados, pedido ao melhor elegível e insucesso registrado), em vez do
broadcast integral de Crowder. TL mantém uma unidade por sucesso; não se alega
transplante da Eq. (3). Protocolo, lei e reset têm alternativas separadas no lote.

## Como interpretar os resultados

- `taxa_omissao` é a proporção histórica de tarefas com falha não reportada;
  não é frequência P1 nem probabilidade total de falha. A frequência P1 vem dos
  registros por oportunidade.
- `E_total=TW/(TW+TL+TU+TR)` é uma razão contábil do modelo. A redução de TW
  por atalho pode reduzir essa razão, mesmo com menor duração de projeto.
  Não é medida empiricamente calibrada de produtividade.
- N, no fatorial, é o canal fuzzy da confiança em **mu_rede**, distinto do
  portão G. Não é uma intervenção direta em mu_cog (fadiga/pressão).
- Os intervalos usam instâncias como unidades; sementes são réplicas internas.
  A robustez tem quatro instâncias por célula, portanto precisão limitada.
- Família discreta declarada não representa todo o espaço contínuo plausível.
  Não há ranking, busca de melhor política ou função objetivo.

## Evidências e continuidade

- [Sequência e decisões](../research/PLANO_CORRECAO_ESTRUTURAL.md).
- [Hashes congelados](../research/CONGELAMENTO_PRE_CORRECAO.json).
- Saídas novas: `outputs/diagnosticos/correcao_estrutural_20260916/`.
- Após o MVP: V_obs/V_mod e implausibilidade perfilada, junto das fragilidades
  de unidade, agregação, Di/gradiente e validação externa da seleção P1. Sem
  novas ondas HM enquanto o alvo observacional não estiver resolvido.

## Resultados nominais já reexecutados

Diferença = adaptativa − centralizada; 16 instâncias, 12 sementes por cenário.

| Métrica | Centralizada | Adaptativa | Diferença | IC95 da diferença |
|---|---:|---:|---:|---|
| atraso_relativo | 3.060802 | 2.037381 | -1.023421 | [-1.113870; -0.932973] |
| E_total | 0.706713 | 0.655868 | -0.050845 | [-0.059773; -0.041916] |
| taxa_omissao | 0.312500 | 0.084288 | -0.228212 | [-0.242839; -0.213584] |
| retrabalho_sobre_plano | 0.289204 | 0.234953 | -0.054251 | [-0.065545; -0.042957] |
| divida_latente_sobre_plano | 0.103272 | 0.025458 | -0.077815 | [-0.086201; -0.069428] |

**E_total inverteu o sinal nominal**: legado +0,104631; corrigido −0,050845.
Não há preservação de todas as conclusões de governança. O detalhamento
incremental mostra aumento do aprendizado após normalização/protocolo e
reset C6; TL adaptativo passa de 10,854 (C4+C1) a 102,859 (com reset).
Ao mesmo tempo TW cai de 500,922 para 433,016. Esses componentes explicam
a mudança na razão contábil, sem autorizá-la como ganho/perda de produtividade empírica.

O controle C4 de tempo apenas versus C4 completo isola o risco: TR centralizado
passa de 64,020 para 95,911; adaptativo, de 49,057 para 64,604. O custo
de qualidade entrou sem forçar toda omissão a falhar e sem escolher rho pelo resultado.

## Robustez já reexecutada

129 configurações, 4.128 execuções, nenhuma censurada e nenhuma violação.
Atraso, falhas não reportadas e dívida latente tiveram contraste negativo em
129/129 configurações. TR teve 126 contrastes negativos e 3 positivos; E_total,
124 negativos e 5 positivos. Os intervalos das células de sinal positivo
em TR/E_total incluem zero; n=4 instâncias exige cautela. Nenhuma célula foi
selecionada para substituir o nominal. Esses resultados cobrem a família declarada.

## Seleção da Porta 1 e amplificação de rho

A amostra declarada de 32 execuções produziu 5.659 oportunidades e 1.920
execuções de tarefas. São denominadores diferentes:

| Cenário | P1/oportunidades | P1/tarefas executadas | E[q] nas oportunidades | E[q condicionado a P1] |
|---|---:|---:|---:|---:|
| Centralizada | 0,2354 | 0,6740 | 0,1652 | 0,6963 |
| Adaptativa | 0,1911 | 0,5792 | 0,1131 | 0,5852 |

A comparação com os 64% anteriores só faz sentido com o denominador
correspondente de tarefas executadas. A frequência menor por oportunidade
não representa correção/validação da logística. A seleção por p_heu eleva q
na amostra de P1 e amplifica a sensibilidade ao excesso rho*q. Não foi alterado
p_heu para produzir uma frequência-alvo. A validação externa continua aberta.

As tabelas condicionais por faixas declaradas de Di, P e B estão em
`instrumentacao/selecao_condicional.csv`; registros individuais em
`instrumentacao/tarefas.csv.gz`. São descrições internas, com dependência
entre oportunidades; não foram tratados como ensaios humanos independentes.

## B9 e atribuição dos canais — reexecutados

Sem assistência, TL é zero nos dois cenários, mas permanecem 86,91% do contraste
nominal de atraso e 98,14% do contraste de falhas não reportadas. Logo, essa
ablação não sustenta atribuir todo o contraste à assistência. Com Crowder,
eliminar comunicação também elimina as atualizações de confiança associadas;
a ablação não é uma intervenção isolada no limiar do portão.

O fatorial G,N,B,C,D de condições iniciais separa portão e canal fuzzy da
confiança. Agregando termos e suas interações com B/C/D:

| Grupo de termos | Parcela do contraste de atraso | % assinado |
|---|---:|---:|
| Inclui G, sem N | −0,260384 | 25,44% |
| Inclui N, sem G | −0,298666 | 29,18% |
| Inclui G e N | +0,126435 | −12,35% |
| Sem G nem N | −0,590807 | 57,73% |

As parcelas somam o contraste −1,023421. Percentuais são contribuições
algébricas assinadas na referência centralizada, não importâncias independentes.
Em E_total, os grupos G sem N e N sem G contribuem −0,021555 e −0,047562;
as interações G/N contribuem +0,014194 e os demais termos +0,004079.
Não se atribui a inversão a um único coeficiente de confiança.

## Verificação final e arquivos de comparação

- 34 testes passaram, incluindo compatibilidade, contrafactual negativo, eventos
  Crowder, reset no horizonte final, canais e instrumentação sem alterar RNG.
- 21.408 execuções principais: zero incompletas, zero violações e nenhum reparo
  ou dívida pendente ao término; 32 execuções instrumentadas também completas.
- 384 diagonais corrigidas coincidem com o nominal; 3.072 diagonais legadas
  reproduzem o histórico. Diferenças máximas verificadas: zero.
- Horizonte duplicado idêntico em 32 pares para cada rho (96 pares ao todo).
- 72 hashes históricos intactos. DOCX oficial vivo e snapshot conferidos pelo
  verificador que falha diante de ausência ou divergência.
- Suplemento reproduzido em pasta externa, com CSV e verificações idênticos.
- Valores-p históricos são acompanhados de controle no mesmo ambiente:
  SciPy 1.11.4 usa aproximação normal em alguns casos com zeros. Não atribuir
  diferenças de implementação estatística ao modelo.

Arquivos sob `outputs/diagnosticos/correcao_estrutural_20260916/`:

- `correcao/antes_depois_incremental.csv`: efeito de cada etapa nas mesmas chaves.
- `correcao/antes_depois_MVP_pre_correcao.csv`: MVP efd81b7 versus corrigido.
- `consolidado/antes_depois_numeros_experimento.csv`: números publicados,
  controle no mesmo ambiente e resultados novos.
- `consolidado/antes_depois_numeros_B9_fatorial.csv`: correspondência numérica
  B9/fatorial; quatro fatores históricos são a restrição diagonal G=N.
- `consolidado/atribuicao_grupos_canais.csv`: portão, rede e interações separados.
- `correcao/sinais_robustez.csv`, `correcao/denominadores_selecao.csv` e
  `correcao/verificacoes.json`: sinais, denominadores e controles adicionais.

Próxima questão prioritária: especificar V_obs/V_mod e a ponte entre
observação externa e grandeza simulada antes de qualquer nova onda de HM.
As fragilidades de unidade/nível de agregação, Di/gradiente, fator temporal,
P1 externa, protocolo de comunicação e reparos sem reincidência permanecem
explícitas. Fechamento de software e robustez interna não equivalem a validação
empírica nem a calibração do modelo.
