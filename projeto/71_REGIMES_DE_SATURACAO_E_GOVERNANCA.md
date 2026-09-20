# T-SAT.1 e T-GOV.1 — caracterização de regime, nominal preservado

## T-SAT.1 — 384 execuções nominais, 192 por braço

Fonte congelada: `outputs/diagnosticos/noturno_nominal/tarefas.csv` e `bruto.csv`.
79.327 oportunidades de decisão, das quais 13.334 selecionaram P1. Denominador
é decisão, não tarefa única; repetições por bloqueio integram a distribuição.
Tabela abaixo em frações (multiplicar por 100 para porcentagens):

| populacao | cenario | N | menor_001 | maior_099 | meio_01_09 |
| --- | --- | --- | --- | --- | --- |
| todas_decisoes | ambos | 79327 | 0.0 | 0.0919863350435539 | 0.1494951277623003 |
| todas_decisoes | adaptativa | 40777 | 0.0 | 0.0721239914657772 | 0.1460627314417441 |
| todas_decisoes | centralizada | 38550 | 0.0 | 0.1129961089494163 | 0.1531258106355382 |
| selecionou_p1 | ambos | 13334 | 0.0 | 0.5470226488675566 | 0.179466026698665 |
| selecionou_p1 | adaptativa | 5996 | 0.0 | 0.4904936624416277 | 0.1939626417611741 |
| selecionou_p1 | centralizada | 7338 | 0.0 | 0.5932134096484055 | 0.1676206050695012 |

[Histograma](../outputs/diagnosticos/SAT_GOV_20260919/SAT1_histograma.png),
[100 intervalos e contagens](../outputs/diagnosticos/SAT_GOV_20260919/SAT1_histograma.csv).
Último intervalo inclui 1; demais são fechados à esquerda e abertos à direita.

**A hipótese operacional não se confirma pelo limiar proposto de menos de 10%
no meio:** há 14,95% de todas as decisões e 17,95% das seleções P1 em [0,1;0,9].
Não há massa abaixo de 0,01. A distribuição é bimodal, mas a massa inferior
fica acima desse extremo; não descrevê-la como empilhada em 0 e 1.

A conclusão sobre q exige outra distinção: 92,33% das seleções P1 têm q<0,01
ou q>0,99 e apenas 5,07% estão em [0,1;0,9]. q é quase binário neste sentido,
pois a transformação q=max(0,2*p_heu−1) zera todo p_heu<=0,5. Isso sustenta
concentração de q a montante da fuga, mas não atribui causalmente o degrau do
A1 somente à saturação de p_heu. O comparador individual também é binário.
[Leitura suplementar de q](../outputs/diagnosticos/SAT_GOV_20260919/SAT1_q_suplementar.csv).

## T-SAT.2 — condicional não disparada

O gatilho pré-declarado de T-SAT.1 não foi atingido; não se executou a varredura
condicional. Além disso, há impedimento independente da saturação: no limite
nominal 0,60, omega=0,50 e 0<=q<=1 implicam omega*q<=0,50<0,60 para qualquer
s_transicao. Logo nenhuma suavização pode ativar a fuga nesse limite. Não há
valor de s que torne a fuga graduada mantendo esses parâmetros. O A1 anterior
ativou fuga em limites menores; não confundir esses ensaios com o nominal.
A caracterização “só opera fora do regime saturado” não é sustentada aqui.

## T-GOV.1 — fatores de robustez, desenho declarado

81 perfis = produto cartesiano de três níveis por fator:
- tau_inicial: 0,25 / 0,525 / 0,80;
- tau_min: 0,25 / 0,425 / 0,60;
- p_reporte: 0,15 / 0,45 / 0,75;
- p_deteccao: 0,03 / 0,075 / 0,12.

Extremos históricos e ponto médio, não estimativas calibradas. Cada perfil
roda nos dois rótulos: 4 instâncias x 4 sementes x 2 braços = 32 execuções.
Todos os 81 perfis adaptativos são comparados aos 81 centralizados: 6.561
contrastes por indicador. Os mesmos resultados são reutilizados; não são
6.561 experimentos independentes. Demais fatores e horizonte 256xCPM nominais.
Esta família dedicada promove efetivamente os quatro fatores, preservando
as famílias históricas e sem eleger a combinação mais favorável.

IC95 t sobre quatro médias por instância de diferenças pareadas por semente.
Intervalos pontuais exploratórios, sem ajuste para multiplicidade. Baixa
precisão com quatro instâncias; não extrapolar a malha à faixa contínua.
“Atraso relativo” aqui é makespan/CPM sem recursos, não crescimento de prazo
externo. Fração P1 é omissões/(omissões+inícios analíticos); fuga é contada
separadamente. Nenhum dos cinco usa TL no denominador.

Execuções: **2592**, completas **2592**, violações **0**.

Todas as linhas finais levam estatuto de censura/conclusão; contrastes
condicionais em pares completos também estão exportados. Nenhum NaN vira zero.

### Contraste nominal nesta subamostra (adaptativa − centralizada)

| metrica | media | ic95_inf | ic95_sup | estatuto |
| --- | --- | --- | --- | --- |
| atraso_relativo | -1.05075 | -1.891816 | -0.209684 | COMPLETO |
| taxa_omissao | -0.207292 | -0.244552 | -0.170031 | COMPLETO |
| divida_latente_sobre_plano | -0.067985 | -0.089434 | -0.046536 | COMPLETO |
| taxa_falha_efetiva | -0.047917 | -0.114107 | 0.018274 | COMPLETO |
| fracao_porta1 | -0.108333 | -0.11771 | -0.098957 | COMPLETO |

### Sinais em toda a malha

“Ordenação histórica” exige tau_inicial_A>=C, tau_min_A<=C, p_reporte_A>=C e
p_deteccao_A>=C. Perfis iguais são separados. A região restante contém pelo
menos uma premissa com ordenação invertida.

| regiao | metrica | N | negativos | zeros | positivos | IC_negativo | IC_positivo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| inclui_inversao_de_premissa | atraso_relativo | 5265 | 2130 | 27 | 3108 | 905 | 1599 |
| inclui_inversao_de_premissa | divida_latente_sobre_plano | 5265 | 2095 | 28 | 3142 | 912 | 1627 |
| inclui_inversao_de_premissa | fracao_porta1 | 5265 | 2392 | 49 | 2824 | 1124 | 1690 |
| inclui_inversao_de_premissa | taxa_falha_efetiva | 5265 | 2280 | 50 | 2935 | 235 | 375 |
| inclui_inversao_de_premissa | taxa_omissao | 5265 | 2136 | 34 | 3095 | 1539 | 2223 |
| ordenacao_historica | atraso_relativo | 1215 | 1083 | 27 | 105 | 697 | 3 |
| ordenacao_historica | divida_latente_sobre_plano | 1215 | 1117 | 28 | 70 | 716 | 1 |
| ordenacao_historica | fracao_porta1 | 1215 | 804 | 39 | 372 | 577 | 11 |
| ordenacao_historica | taxa_falha_efetiva | 1215 | 915 | 40 | 260 | 144 | 4 |
| ordenacao_historica | taxa_omissao | 1215 | 1071 | 32 | 112 | 687 | 3 |
| perfis_identicos | atraso_relativo | 81 | 0 | 81 | 0 | 0 | 0 |
| perfis_identicos | divida_latente_sobre_plano | 81 | 0 | 81 | 0 | 0 | 0 |
| perfis_identicos | fracao_porta1 | 81 | 0 | 81 | 0 | 0 | 0 |
| perfis_identicos | taxa_falha_efetiva | 81 | 0 | 81 | 0 | 0 | 0 |
| perfis_identicos | taxa_omissao | 81 | 0 | 81 | 0 | 0 | 0 |

A estabilidade em toda a faixa **não se sustenta**: o desenho contém os dois
sentidos de atribuição das premissas, e os contrastes trocam de sinal. Perfis
idênticos dão diferença exatamente zero: o rótulo de arranjo, isoladamente,
não acrescenta efeito. As conclusões devem especificar as combinações de
premissas e seu domínio, em vez de atribuir um sinal universal à governança.
As contagens acima também permitem distinguir inversões dentro da ordenação
histórica das inversões obtidas trocando a ordem das premissas.

[Regiões completas, parâmetros dos dois braços, sinal e IC95](../outputs/diagnosticos/SAT_GOV_20260919/GOV_regioes_IC95.csv).
[Todos os contrastes positivos](../outputs/diagnosticos/SAT_GOV_20260919/GOV_regioes_contraste_positivo.csv).
[Indicadores absolutos por braço](../outputs/diagnosticos/SAT_GOV_20260919/indicadores_por_braco_IC95.csv).
[Dados por execução](../outputs/diagnosticos/SAT_GOV_20260919/bruto.csv).

## Controles e continuidade

Perfis iguais reproduzem resultados exatamente nos dois rótulos. O subconjunto
nominal reproduz TW, TL, TU, TR, makespan e contadores históricos com resíduo
zero. Hashes da dinâmica/configuração nominal inalterados antes/depois.
A suíte bit a bit é registrada separadamente. Não houve recalibração, ajuste
de V_mod, eleição de alternativa ou alteração de conclusão por conveniência.
C4 e N da bancada F continuam parciais; lote 37 permanece encerrado com a
emenda anterior. Este diagnóstico adicional limita a leitura de regime e de
premissas; não demonstra validade externa do modelo.

## Inversões mantendo a ordenação histórica

Não é apenas efeito de trocar as premissas entre os nomes dos braços. Nos
1.215 pares não idênticos que mantêm a ordenação histórica há contrastes
positivos nos cinco indicadores. Para atraso: 105 médias positivas, 3 com
IC95 inteiramente positivo; omissão: 112 e 3; dívida: 70 e 1; falha efetiva:
260 e 4; fração P1: 372 e 11. São resultados exploratórios desta grade,
não evidência confirmatória após correção de multiplicidade.

Abaixo, a primeira célula em ordem lexicográfica com IC95 positivo por
indicador, não a de maior efeito. A/C identificam os dois braços; a tabela
completa inclui todas as regiões, inclusive as de intervalo cruzando zero.

| metrica | tau_inicial_A | tau_min_A | p_reporte_A | p_deteccao_A | tau_inicial_C | tau_min_C | p_reporte_C | p_deteccao_C | media | ic95_inf | ic95_sup |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fracao_porta1 | 0.25 | 0.25 | 0.45 | 0.12 | 0.25 | 0.25 | 0.15 | 0.12 | 0.019792 | 0.008469 | 0.031115 |
| taxa_omissao | 0.8 | 0.25 | 0.15 | 0.03 | 0.525 | 0.425 | 0.15 | 0.03 | 0.029167 | 0.002099 | 0.056234 |
| taxa_falha_efetiva | 0.8 | 0.25 | 0.15 | 0.03 | 0.525 | 0.425 | 0.15 | 0.03 | 0.029167 | 0.003205 | 0.055129 |
| divida_latente_sobre_plano | 0.8 | 0.25 | 0.75 | 0.03 | 0.8 | 0.6 | 0.75 | 0.03 | 0.002526 | 0.000942 | 0.00411 |
| atraso_relativo | 0.8 | 0.425 | 0.75 | 0.12 | 0.525 | 0.425 | 0.45 | 0.12 | 0.023259 | 0.009276 | 0.037241 |

## Registro dos controles de execução

A primeira chamada da suíte teve 2 testes aprovados e 1 erro de importação
(`test_mvp` fora do caminho de módulos). Com PYTHONPATH=research, passaram
os 3 testes, incluindo a identidade bit a bit. Ambos os logs foram preservados.
A primeira comparação memória/CSV reprovou a igualdade exata em TR: o parser
padrão difere do round-trip em até 2,842170943040401e-14. A leitura round_trip
preserva o float gravado e produziu resíduo zero, sem relaxar o alvo. A análise
foi refeita a partir dos mesmos dados; nenhuma simulação precisou ser repetida.
Logs originais e controle_leitura_csv.json preservam o diagnóstico. O manifesto
de execução conserva o hash do runner daquela execução; manifesto_final.json
registra o runner corrigido para leitura round-trip e os hashes dos artefatos.
