# TCC2 — Modelagem e simulação da gestão de equipes de engenharia

Simulador híbrido que combina Modelagem Baseada em Agentes e Dinâmica de
Sistemas para estudar como fatores cognitivos e arranjos de governança afetam o
desempenho de equipes em projetos de engenharia. Dá continuidade ao modelo
conceitual formulado no TCC I.

UFMG · Engenharia de Sistemas · Isadora Maria Carvalho Lopes
Orientação: Prof. André Costa Batista

---

## Como executar

Requer Python 3.10 ou superior.

```bash
git clone https://github.com/isadoramcl/TCC2.git
cd TCC2

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

O pipeline roda em três camadas, na ordem. Cada script termina com verificações
automáticas e **sai com código de erro se alguma falhar**, de modo que uma etapa
defeituosa não alimente a seguinte.

```bash
# 1. Camada de dados — NASA MDP e PSPLIB J60
python src/nasa/01_auditar_raw.py
python src/nasa/02_consolidar_dpp.py
python src/nasa/03_validar_dpp.py
python src/nasa/04_modelos_logisticos.py
python src/nasa/05_faixas_complexidade.py

python src/psplib/01_auditar_j60.py
python src/psplib/02_indice_dificuldade.py
python src/psplib/03_transferencia_ordinal.py

# 2. Simulador — parâmetros derivados e verificação
python src/modelo/01_derivar_parametros.py
python src/modelo/02_verificar_simulador.py

# 3. Experimentos
python src/modelo/20_experimento_mvp.py
```

Para rodar a suíte de testes:

```bash
python -m unittest discover -s research -p "test_*.py" -v
```

---

## Objetivo

Investigar a gestão de equipes em projetos de engenharia por modelagem e
simulação.

A camada NASA MDP fornece um gradiente ordinal de risco de defeito. O PSPLIB J60
fornece redes de tarefas, durações e restrições de recursos. O simulador combina
esses elementos com premissas declaradas sobre cognição, assistência e
governança. A taxa basal absoluta de retrabalho em engenharia permanece aberta e
não foi estimada a partir da NASA.

---

## Estrutura do repositório

```
data/
├── raw/            arquivos originais — nunca modificados
│   ├── nasa_promise/        versões brutas do repositório PROMISE
│   ├── nasa_dp_reference/   versão D' — usada para validar o D''
│   ├── nasa_dpp_reference/  versão D'' — base de análise
│   └── psplib/              480 instâncias do PSPLIB J60
└── processed/      bases derivadas, geradas exclusivamente por código

src/
├── nasa/           pipeline NASA MDP
├── psplib/         pipeline PSPLIB
└── modelo/         simulador, verificações e experimentos

config/             parâmetros do modelo, com condição de origem declarada
research/           experimentos, testes e controles
outputs/
├── tables/         tabelas de resultado
├── figures/        figuras
├── logs/           logs de execução
└── diagnosticos/   evidência datada de cada experimento — ver README próprio

docs/               especificação do modelo, registro de decisões e entrega
projeto/            revisão independente, auditorias e ordens de serviço
```

---

## Princípios metodológicos

1. **Imutabilidade dos brutos.** Nenhum arquivo em `data/raw/` é editado. Uma
   correção necessária é feita por código, e o resultado vai para
   `data/processed/`.
2. **Toda transformação é código.** Não há edição manual de dados. Cada etapa de
   limpeza registra quantas linhas removeu e por qual critério.
3. **Rastreabilidade.** As bases derivadas preservam `project`, `source_file` e
   `source_row`, permitindo devolver qualquer observação ao arquivo de origem.
4. **Separação de origens.** Cada parâmetro e cada decisão carrega rótulo: o que
   vem da literatura, o que é decisão metodológica deste trabalho, o que é
   herdado do TCC I, o que é derivado de dados e o que permanece em aberto.
5. **Controle publicado antes de uso.** Distribuição ou parametrização tomada da
   literatura é primeiro reproduzida contra os valores publicados pela fonte, e
   o comparador é testado contra implementações deliberadamente erradas para
   demonstrar que separa certo de errado.
6. **Alteração não muda resultado em silêncio.** Toda modificação do simulador
   passa por controle de identidade bit a bit — todos os campos comparados por
   representação binária, mais o estado do gerador aleatório — com as opções
   neutras ativadas.

---

## Dados

**NASA MDP.** Treze bases de defeitos de módulos de software, na versão D'' de
Shepperd, Song, Sun e Mair (2013). A consolidação foi validada contra o
algoritmo publicado: aplicando ao conjunto D' os dois passos que o separam do
D'', o conjunto de módulos preservados foi reproduzido em 12 de 12 bases. As
questões encontradas na entrada dos dados — base vazia, estrutura divergente,
rótulos conflitantes — estão registradas e resolvidas em
`outputs/logs/01_auditar_raw.log` e em `docs/registro_de_decisoes.md`.

**PSPLIB J60.** As 480 instâncias do conjunto de 60 atividades. O delineamento
fatorial foi reconstruído a partir dos arquivos, não suposto: recalculando NC,
RF e RS pelas definições de Kolisch, Sprecher e Drexl (1995), recupera-se o
fatorial completo e balanceado de 3 × 4 × 4 = 48 células com 10 instâncias cada.

---

## Resultados

### Camada de dados

**A complexidade não sobrevive ao controle por tamanho.** Isolada, a
complexidade ciclomática tem razão de chances 1,90 sobre a ocorrência de
defeito. Controlando `LOC_TOTAL`, cai para 0,944, IC 95% [0,870; 1,024],
p = 0,17 — o intervalo contém o nulo. O tamanho, ao contrário, sobrevive ao
controle pela complexidade (LR = 431,2). Nenhuma métrica candidata apresenta
efeito positivo independente do tamanho. A complexidade é preservada como
**marcador ordinal** de risco, não como fator causal.

**Risco basal por faixa, monotônico e robusto.** Sobre faixas adaptadas do
requisito NASA SWE-220: 0,147 → 0,285 → 0,348 → 0,439. Tendência de
Cochran-Armitage z = 25,6. Monotonicidade preservada em 5 de 5 esquemas
alternativos de corte e em 12 de 12 reamostragens por exclusão de projeto.

**Transferência ordinal.** Uma tarefa de dificuldade muito alta carrega 2,99
vezes o risco basal de uma de dificuldade baixa, IC 95% [1,878; 4,156], com
bootstrap por projeto.

### Camada de simulação

Contraste entre o arranjo adaptativo e o centralizado, pareado por instância e
semente, com intervalo de confiança sobre as instâncias.

| indicador | 16 instâncias | 48 instâncias fora da amostra |
|---|---:|---:|
| atraso relativo | −1,0234 [−1,1139; −0,9330] | −1,1387 [−1,2086; −1,0687] |
| taxa de omissão | −0,2282 [−0,2428; −0,2136] | −0,2253 [−0,2332; −0,2174] |
| dívida latente | −0,0778 [−0,0862; −0,0694] | −0,0816 [−0,0865; −0,0766] |
| taxa de falha efetiva | −0,0431 [−0,0568; −0,0293] | −0,0370 [−0,0446; −0,0294] |
| fração via Porta 1 | −0,1165 [−0,1366; −0,0964] | −0,0967 [−0,1092; −0,0841] |

A replicação fora da amostra usou 48 instâncias sorteadas de forma
estratificada, uma por combinação de desenho, excluindo as 16 dos experimentos
originais. Os cinco indicadores mantiveram sinal e significância, com intervalos
sobrepostos aos originais. A estratificação por complexidade de rede, fator de
recursos e força de recursos não revelou estrato em que o resultado se
dissolvesse.

**O mecanismo.** A vantagem do arranjo adaptativo decorre principalmente do
portão de assistência: sua abertura reduz a taxa de falha efetiva em cerca de
4,5 pontos percentuais. O reporte imediato reduz a taxa de omissão por fator de
3,6 e a dívida latente pela metade, sem custo de prazo.

---

## Estado atual

### Funciona e está verificado

- Simulador implementado, com identidade bit a bit preservada em todas as
  alterações.
- Cinco indicadores com intervalo de confiança, replicados fora da amostra.
- Controles publicados reproduzidos: seis pontos de Stewart & Melchers (1988),
  parâmetros da beta-binomial de Stewart (1992) e as frequências da Tabela 2.
- Bateria de controles negativos estabelecendo a resolução do instrumento.
- Cobertura do History Matching: taxa empírica de falsa exclusão de 6,2%,
  IC 95% de Wilson [4,40%; 8,67%], compatível com o nominal de 5%.
- **Achado sobre fonte primária:** a Tabela 2 de Stewart (1992) não é
  internamente reprodutível na precisão impressa — nenhum par de parâmetros
  satisfaz os três conjuntos publicados ao mesmo tempo (discrepância de 0,012%,
  dentro do arredondamento). A implementação reproduz a fonte; o efeito sobre
  o modelo é nulo.

### Funciona, com ressalva declarada

- **Os parâmetros de governança são premissas sem fonte externa.** Uma varredura
  de 81 perfis mostra que o sinal do contraste se mantém na quase totalidade do
  espaço, mas o valor não está ancorado empiricamente.
- **A validação fora da amostra não passou por auditoria independente**, ao
  contrário dos demais experimentos.
- Análise de sensibilidade de pressão e uma contagem da base de fatores humanos
  permanecem parciais.

### Não funciona como o modelo conceitual previa

- **A rota de fuga da Porta 1 nunca executa** no ponto de operação. É resultado
  aritmético, não estatístico: o máximo da condição é 0,50 contra um limiar de
  0,60. Com limiares menores (0,10 a 0,40, 320 execuções) a rota passa a
  disparar, mas como interruptor liga-desliga, não como mecanismo gradual. Não
  pode ser descrita como mecanismo ativo.
- **O portão de assistência do arranjo centralizado nasce fechado**, porque a
  confiança inicial está abaixo do limiar exigido para pedir ajuda. Nenhum
  pedido ocorre naquele braço, e a confiança, que só se atualiza por evento de
  pedido, não tem como sair do estado inicial.
- **Com o parâmetro de transição em seu valor mínimo varrido** (0,01), em um
  canto específico da grade — arranjo centralizado, competência insuficiente e
  limiar de saturação alto —, a probabilidade de seleção heurística fica na
  ordem de 10⁻¹⁴, e a rota heurística se torna inacessível na prática. Não é
  erro numérico: o valor é representável. Esse canto está declarado como fora
  da faixa de validade; o ponto nominal (0,25) não é afetado.

Os três são condições de decisão comparadas entre constantes, identificadas por
varredura e documentadas. Dois deles são herdados da especificação conceitual do
TCC I, não introduzidos na implementação.

---

## Documentação detalhada

| onde | o quê |
|---|---|
| `docs/especificacao_modelo.md` | especificação do simulador, equações e portas de decisão |
| `docs/registro_de_decisoes.md` | registro de decisões com origem rotulada |
| `projeto/04_FONTES.md` | referências, com o que cada fonte sustenta e o que não sustenta |
| `projeto/` | auditorias, pareceres de revisão independente e ordens de serviço |
| `outputs/diagnosticos/README.md` | índice dos experimentos executados |
