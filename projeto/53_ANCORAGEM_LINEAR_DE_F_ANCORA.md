# C1 — ancoragem linear como alternativa sintética preservada

Controle publicado: k=1/2/3/4/5/8 devolve respectivamente
0,0128/0,0256/0,0384/0,0512/0,0640/0,1024. Maior resíduo absoluto
6,94e-18, abaixo de 1e-12. Nenhum ajuste aos seis pontos.

## O que a alternativa significa

`ancoragem_erro=historica` é default e preserva F_ancora×razão NASA.
`stewart_linear` usa F_base=k×0,0128, com dois mapas **declaradamente sintéticos**:
curto=(1,2,3,4), longo=(1,2,4,8), na ordem baixa/média/alta/muito alta.
[DEC] Esse gradiente por passos substitui, dentro da alternativa, o multiplicador
NASA; não empilha dois mapeamentos de dificuldade. Portanto a comparação muda
a escala e a forma do risco basal, não isola apenas uma troca de parâmetro.
O modelo histórico e o YAML nominal permanecem intactos. Nenhum mapa escolhido
como verdadeiro ou melhor. Fonte de ancoragem não mede passos de tarefas PSPLIB.

O transporte de construto permanece: cálculo elementar na fonte não é tarefa
de projeto. A linearidade empírica dos pontos publicados não prova independência
de erros e não autoriza extrapolação arbitrária. Função de ancoragem rejeita
k fora de [1,8]; mapa reverso pode mostrar extrapolação, mas não executá-la como
valor ancorado. Relatório C3/A-16 permanece preservado.

## Mapa reverso

| F_ancora histórico | k implícito | Estatuto |
|---:|---:|---|
| 0,05 | 3,90625 | Dentro da faixa publicada; transporte/interpolação declarados |
| 0,10 | 7,81250 | Dentro da faixa publicada; transporte/interpolação declarados |
| 0,15 | 11,71875 | CENÁRIO DE SENSIBILIDADE, acima de k=8 |
| 0,20 | 15,62500 | CENÁRIO DE SENSIBILIDADE, acima de k=8 |
| 0,25 | 19,53125 | CENÁRIO DE SENSIBILIDADE, acima de k=8 |

## Experimento declarado

96/96 completas, zero violações: histórico e dois mapas ×quatro instâncias
×quatro sementes ×dois braços. A1 permanece constante/limite0,60, portanto não
se confunde o novo risco com a alternativa de fuga. Mesmas sementes, sem afirmar
alinhamento evento a evento depois que as trajetórias divergem.

Diferença A−C, IC95 t sobre médias por instância (n=4, precisão limitada):

| Mapa | Indicador | Diferença | IC95 |
|---|---|---:|---|
| curto | atraso_relativo | -1.069970 | [-1.887648; -0.252293] |
| curto | taxa_omissao | -0.132292 | [-0.182894; -0.081690] |
| curto | divida_latente_sobre_plano | -0.061573 | [-0.099069; -0.024078] |
| curto | taxa_falha_efetiva | -0.089583 | [-0.143310; -0.035856] |
| curto | fracao_porta1 | -0.191667 | [-0.282735; -0.100598] |
| curto | retrabalho_sobre_esforco_total | -0.059526 | [-0.091426; -0.027625] |
| historica | atraso_relativo | -1.050750 | [-1.891816; -0.209684] |
| historica | taxa_omissao | -0.207292 | [-0.244552; -0.170031] |
| historica | divida_latente_sobre_plano | -0.067985 | [-0.089434; -0.046536] |
| historica | taxa_falha_efetiva | -0.047917 | [-0.114107; +0.018274] |
| historica | fracao_porta1 | -0.108333 | [-0.117710; -0.098957] |
| historica | retrabalho_sobre_esforco_total | -0.042822 | [-0.083046; -0.002598] |
| longo | atraso_relativo | -1.076609 | [-1.451730; -0.701488] |
| longo | taxa_omissao | -0.132292 | [-0.177055; -0.087528] |
| longo | divida_latente_sobre_plano | -0.059681 | [-0.099923; -0.019440] |
| longo | taxa_falha_efetiva | -0.092708 | [-0.127106; -0.058311] |
| longo | fracao_porta1 | -0.189583 | [-0.232380; -0.146786] |
| longo | retrabalho_sobre_esforco_total | -0.062536 | [-0.101021; -0.024051] |

As magnitudes de risco menores são consequência da ancoragem imposta como
alternativa, não prova de melhoria empírica. Não selecionar mapa por contraste
mais favorável. Sem alterar conclusões gerais de governança com este piloto.
`antes_depois.csv` publica todos os indicadores aqui reportados nos dois braços,
e `mapas_sinteticos.csv` o risco antes/depois de cada nível.

Verificação: dois testes dos seis pontos/domínio, três testes de integração
(p0 efetivamente usado, opção histórica exata, rejeição de opções inválidas),
três controles bit a bit gerais após a implementação e após o experimento.
Fontes conferidas por hash. Saídas em `outputs/diagnosticos/C1_20260919/`.
Reprodução: `python3 research/lote_noturno/c1.py` (preservar diretório anterior).
C1 executado como alternativa; lote não fechado. C2 tem controle próprio.
