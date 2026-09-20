# A1 — rota de fuga dependente de estado, alternativa preservada

[DEC] `regra_fuga=constante` permanece default; alternativa
`dependente_estado` aplica omega*q>limite, q=max(0,2*p_heu−1).
Seleção P1, ação de fuga, RNG e nominal não foram substituídos.
Robustez dedicada: `config/robustez_a1.yaml`, quatro instâncias ×quatro sementes
×dois braços ×duas regras ×cinco limites (0,60 é controle). Horizonte256×CPM.
O limite está efetivamente varrido aqui; não foi acrescentado silenciosamente
à antiga família do runner20. Células/indefinições não são descartadas.

## Grade inteira

| Regra | Limite | Braço | Completas/N | Fuga média | Fração de fuga em P1 (média por execução) | Estatuto |
|---|---:|---|---:|---:|---:|---|
| constante | 0.10 | adaptativa | 5/16 | 84717.6875 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.10 | centralizada | 0/16 | 71356.5625 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.20 | adaptativa | 5/16 | 84717.6875 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.20 | centralizada | 0/16 | 71356.5625 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.30 | adaptativa | 5/16 | 84717.6875 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.30 | centralizada | 0/16 | 71356.5625 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.40 | adaptativa | 5/16 | 84717.6875 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.40 | centralizada | 0/16 | 71356.5625 | 1.000000 | CENSURADO; acumulado até teto |
| constante | 0.60 | adaptativa | 16/16 | 0.0000 | 0.000000 | COMPLETO |
| constante | 0.60 | centralizada | 16/16 | 0.0000 | 0.000000 | COMPLETO |
| dependente_estado | 0.10 | adaptativa | 8/16 | 57160.4375 | 0.795624 | CENSURADO; acumulado até teto |
| dependente_estado | 0.10 | centralizada | 0/16 | 129243.3750 | 0.999887 | CENSURADO; acumulado até teto |
| dependente_estado | 0.20 | adaptativa | 8/16 | 57163.3750 | 0.792429 | CENSURADO; acumulado até teto |
| dependente_estado | 0.20 | centralizada | 0/16 | 129245.0000 | 0.999885 | CENSURADO; acumulado até teto |
| dependente_estado | 0.30 | adaptativa | 8/16 | 57158.0625 | 0.764938 | CENSURADO; acumulado até teto |
| dependente_estado | 0.30 | centralizada | 0/16 | 129240.0625 | 0.999884 | CENSURADO; acumulado até teto |
| dependente_estado | 0.40 | adaptativa | 9/16 | 49893.6250 | 0.728281 | CENSURADO; acumulado até teto |
| dependente_estado | 0.40 | centralizada | 0/16 | 129225.6250 | 0.999875 | CENSURADO; acumulado até teto |
| dependente_estado | 0.60 | adaptativa | 16/16 | 0.0000 | 0.000000 | COMPLETO |
| dependente_estado | 0.60 | centralizada | 16/16 | 0.0000 | 0.000000 | COMPLETO |

Total: 320 execuções; 117 completas; zero violações.
Fuga positiva na alternativa: True. As taxas dividem por
seleções P1, não por tarefas; uma tarefa pode sofrer muitas fugas. Publicados
numeradores, denominadores, histogramas de q, médias por execução e pooled.

## Forma da resposta e estatuto científico

O comparador individual continua um **interruptor por estado**, com degrau em
q=limite/omega. A alternativa retira a degeneração de comparar duas constantes,
mas NÃO introduz probabilidade contínua de fuga. Uma mistura agregada de
limiares entre estados pode variar; não prova continuidade do comparador.
A análise local nos mesmos estados nominais, sem realimentação, produz
{'adaptativa': 51, 'centralizada': 51} valores distintos na malha 0..0,60 passo0,01; arquivo separado.
Os quatro limites dinâmicos não demonstram continuidade matemática. Platôs,
saltos e censura da grade devem ser lidos como tais. Não chamar a alternativa
de mecanismo empiricamente validado nem ajustar limite para obter uma curva
esperada. Ela permanece hipótese [DEC], sem eleger limite conveniente.

## Conexão com A-13 / T-B2.3

A-13 e A-14 foram identificados independentemente: ambos continham comparação
de constantes na inicialização/histórico capaz de desligar uma rota.
T-B2.3 mostrou a assistência como uma saída do bloqueio conjunto de três vias;
B2 suave confirmou a saída heurística. A1 modifica a segunda comparação, a fuga.
Isso não garante conclusão: fuga recorrente pode gerar outro bloqueio prático.
Não converter os indicadores ao teto em benefícios finais de governança.

## Verificação e limites

- Cinco testes A1: positivo, negativos, limiar estrito, opção inválida,
  constante explícita/default e contrafactual no mesmo estado/sorteios.
- Identidade neutra e nominal histórico bit a bit: três testes aprovados.
- Baseline constante/0,60 contra nominal arquivado: diferenças <1e-12.
- Primeira configuração de teste tinha rho ativo, misturando retrabalho C4;
  corrigida apenas a fixture com rho=0; falha preservada, experimento sem ajuste.
- `cinco_indicadores_IC95.csv`: IC t sobre médias por instância (n≤4), tanto
  diagnóstico ao término/teto quanto contraste condicional a pares completos.
  Nulo/NaN quando não há pares ou denominador. Condicionais não corrigem seleção.
- `antes_depois.csv`: nominal preservado e todos os indicadores publicados,
  componentes e contagens; rótulo de censura em cada linha afetada.
- Resultados em `outputs/diagnosticos/A1_20260919`; manifesto e hashes conferidos.

Lote não fechado. A regra solicitada está implementada/testada; a expectativa
de continuidade não é um controle aprovado por construção. Próximos: C1 e C2,
com os controles publicados antes de resultados dinâmicos.

## Veredito do controle de forma

- adaptativa: 33/64 completas nos quatro limites; fração das seleções P1 com q≥0,9: 0.999644.
- centralizada: 0/64 completas nos quatro limites; fração das seleções P1 com q≥0,9: 0.999866.

**A expectativa de continuidade não está aprovada.** A condição continua um
interruptor dependente do estado; a centralizada fica em um platô de fuga quase
total, e o agregado adaptativo varia com mistura de execuções completas e
censuradas. O salto para nenhuma fuga no controle limite=0,60 é imposto por
omega=0,50 e q≤1. A saturação em q alto explica por que os quatro limiares
podem produzir quase o mesmo regime. Não chamar a fuga de mecanismo contínuo
validado na monografia. Não houve reformulação ou escolha de limiar para passar
esse controle; alternativa experimental preservada, nominal histórico intacto.
