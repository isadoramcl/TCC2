# Teste discriminante de TL e resposta ao parecer 20 — 17/09/2026

## Conclusão

**O sinal de E_total depende da convenção de TL. Não sustenta uma conclusão de governança.**
O nominal permanece `unitario`; `crowder_eq3` é alternativa declarada. Não se escolheu
uma convenção por produzir sinal favorável. V_obs/V_mod não foi iniciado.

## 1. MAJOR-7 — teste discriminante

768 execuções: 16 instâncias × 12 sementes × 2 cenários × 2 convenções.
Todas as demais opções, instâncias e sementes foram mantidas. IC95 t sobre
16 diferenças médias por instância; sementes são réplicas internas pareadas.
E_total é média das razões por execução, não razão das médias TW/TL/TU/TR.

| Convenção | Centralizada | Adaptativa | Diferença A−C | IC95 da diferença |
|---|---:|---:|---:|---|
| unitario | 0.706713 | 0.655868 | -0.050845 | [-0.059773; -0.041916] |
| crowder_eq3 | 0.706713 | 0.758686 | 0.051973 | [0.043253; 0.060693] |

A mudança pareada de contraste é 0.102818, IC95 [0.089531; 0.116105].
Nos 384 pares, estados dos agentes/tarefas, RNG, trajetórias, eventos,
TW/TU/TR e demais resultados físicos coincidiram bit a bit. TL e duas razões
que o usam no denominador mudaram: E_total e retrabalho_sobre_esforco_realizado.
Assim, a inversão anterior é sensível à convenção contábil, sem mudança no
comportamento simulado. As conclusões anteriores sobre E_total ficam restritas
à convenção declarada e não devem ser destacadas como efeito de governança.

### Componentes do nominal nas duas convenções

| Convenção | Cenário | TW | TL | TU | TR |
|---|---|---:|---:|---:|---:|
| crowder_eq3 | adaptativa | 433.015625 | 10.319579 | 49.520833 | 80.136632 |
| crowder_eq3 | centralizada | 564.645833 | 0.000000 | 140.781250 | 98.574592 |
| unitario | adaptativa | 433.015625 | 102.859375 | 49.520833 | 80.136632 |
| unitario | centralizada | 564.645833 | 0.000000 | 140.781250 | 98.574592 |

### O que foi implementado

- Opção `lei_tempo_aprendizado`: `unitario` (default) ou `crowder_eq3`.
- Unitário mantém +1 por sucesso e zero por pedido não atendido.
- Eq3 usa +0,5*dC_original por sucesso e +0,05 por insucesso enviado.
  dC_original é o incremento calculado na escala 0–5, antes do teto da Eq2;
  não se usa dC/5, que é o incremento normalizado da competência.
- Bloqueio pré-pedido não gera TL em nenhuma convenção.
- Trata-se de uma alternativa de contabilização: não altera duração reservada,
  recurso ou relógio. A unidade temporal externa da Eq3 ainda exige ponte de
  interpretação para o projeto; o teste não calibra essa unidade.
- O código de competência legado não foi corrigido, conforme solicitado.

## 2. Componentes em todos os degraus

Médias das mesmas 192 execuções por cenário em cada degrau do lote estrutural.
Fonte histórica preservada: correcao_estrutural_20260916/alternativas/bruto.csv.
Todos estes degraus usam TL unitário. Componentes completos são publicados abaixo
e em `componentes_escada.csv`; não foram inferidos a partir de médias de E_total.

| Degrau | Cenário | TW | TL | TU | TR |
|---|---|---:|---:|---:|---:|
| legado | adaptativa | 547.192708 | 10.489583 | 5.942708 | 52.508906 |
| legado | centralizada | 696.796875 | 0.000000 | 126.265625 | 68.865320 |
| controle_motor | adaptativa | 547.192708 | 10.489583 | 5.942708 | 52.508906 |
| controle_motor | centralizada | 696.796875 | 0.000000 | 126.265625 | 68.865320 |
| C4_tempo_apenas | adaptativa | 492.562500 | 10.776042 | 5.911458 | 49.057465 |
| C4_tempo_apenas | centralizada | 554.473958 | 0.000000 | 143.572917 | 64.020102 |
| C4_completo | adaptativa | 492.296875 | 10.781250 | 5.859375 | 64.604340 |
| C4_completo | centralizada | 554.796875 | 0.000000 | 144.536458 | 95.911015 |
| C4_C1 | adaptativa | 500.921875 | 10.854167 | 6.817708 | 68.763273 |
| C4_C1 | centralizada | 564.645833 | 0.000000 | 140.781250 | 98.574592 |
| C4_C1_comunicacao | adaptativa | 490.755208 | 41.718750 | 17.869792 | 73.164864 |
| C4_C1_comunicacao | centralizada | 564.645833 | 0.000000 | 140.781250 | 98.574592 |
| C4_C1_Crowder | adaptativa | 452.630208 | 43.473958 | 18.437500 | 68.656729 |
| C4_C1_Crowder | centralizada | 564.645833 | 0.000000 | 140.781250 | 98.574592 |
| C4_C1_Crowder_C6 | adaptativa | 433.015625 | 102.859375 | 49.520833 | 80.136632 |
| C4_C1_Crowder_C6 | centralizada | 564.645833 | 0.000000 | 140.781250 | 98.574592 |
| MVP_corrigido | adaptativa | 433.015625 | 102.859375 | 49.520833 | 80.136632 |
| MVP_corrigido | centralizada | 564.645833 | 0.000000 | 140.781250 | 98.574592 |
| MVP_corrigido_Di_yaml | adaptativa | 433.104167 | 102.614583 | 49.500000 | 80.260312 |
| MVP_corrigido_Di_yaml | centralizada | 564.651042 | 0.000000 | 140.781250 | 98.607515 |

## 3. MINOR-8 — confusão de atribuição na escada

`C4_C1_comunicacao` altera conjuntamente protocolo, escala do incremento e teto
de competência. O contraste com `C4_C1` não identifica o efeito isolado do protocolo.
Essa limitação também afeta interpretações causais da evolução de TL nessa passagem.

No legado, Cp=0,8/Cr=0,4 produz (15+3*0,4)/100=0,162, somado diretamente
à competência normalizada, com teto 0,98. No caminho Crowder, a conversão
para 0–5 produz dC_original=0,21 e incremento normalizado 0,042, com teto Dr.
A implementação fora de escala foi mantida deliberadamente para identidade exata.
O termo constante domina o incremento legado, reduzindo o peso relativo da
competência do colega. Precisão de leitura: a dependência não desaparece
algebricamente — antes dos tetos, a derivada em relação a Cp é 0,03 nos dois
caminhos. A diferença está no intercepto (0,15 versus 0,03), peso relativo e teto.
Não se recodificou o legado para resolver essa limitação de atribuição.

## 4. Controles, registro e continuidade

40 testes passaram; revisão independente recalculou os intervalos e componentes,
sem bloqueio para integração. Manifestos históricos referem-se às fontes de
seus commits, não às versões posteriores em HEAD.

- Controle nominal contra código fixado 1fd22ff: 32 casos, opção omitida e
  explícita, resultados/estados/eventos/registros/RNG comparados por bits.
- Controle legado neutro e cinco horizontes de fronteira continuam ativos.
- Zero incompletas e violações nas 768 execuções; nominal unitário reproduz
  os números publicados do lote anterior (tolerância de leitura CSV 1e-12).
- O runner reconstrói TL Eq3 a partir dos eventos e verifica igualdade exata.
- Parecer20 preservado byte a byte e publicado em revisao-auditoria, commit9ef0f47.
- Resultados antigos não foram sobrescritos. A leitura do relatório19 é corrigida
  por esta resposta. Nenhuma preferência entre leis é inferida dos sinais.
- Próxima etapa: discutir unidades/observáveis e V_obs/V_mod; nenhuma onda HM
  ou ajuste de parâmetros foi iniciado neste trabalho.

## Reprodução

```sh
python3 -m unittest discover -s research -p 'test_*.py' -v
python3 src/modelo/25_teste_tempo_aprendizado.py --saida /tmp/tcc2-teste-tl-novo --workers 4
```

Diretório de saída deve ser novo. Dados e manifestos:
`outputs/diagnosticos/teste_TL_20260917/`.
