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

# 3. Experimentos — nominal (16 instâncias) e validação fora da amostra (48)
python research/validacao/nominal_v2.py nominal
python research/validacao/nominal_v2.py fora1
python research/validacao/nominal_v2.py fora2
python research/validacao/nominal_v2.py fora3
python research/validacao/nominal_v2.py analise
```

O modelo nominal está em `config/mvp.yaml` (versão 2, desde 21/09/2026). A versão
anterior está congelada em `config/mvp_v1.yaml` e continua reproduzindo, bit a
bit, toda a evidência produzida até aquela data.

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
semente, com intervalo de confiança sobre as instâncias. Valores negativos
favorecem o arranjo adaptativo.

| indicador | 16 instâncias | 48 instâncias fora da amostra |
|---|---:|---:|
| atraso relativo | −0,9429 [−1,0864; −0,7994] | −0,9860 [−1,0731; −0,8988] |
| taxa de omissão | −0,2016 [−0,2137; −0,1894] | −0,2074 [−0,2163; −0,1985] |
| dívida latente | −0,0694 [−0,0761; −0,0628] | −0,0727 [−0,0778; −0,0676] |
| taxa de falha efetiva | −0,0229 [−0,0347; −0,0111] | −0,0213 [−0,0276; −0,0149] |
| fração via Porta 1 | −0,0511 [−0,0697; −0,0326] | −0,0499 [−0,0587; −0,0410] |

A replicação fora da amostra usou 48 instâncias sorteadas de forma
estratificada, uma por combinação de desenho, excluindo as 16 do nominal. Os
cinco indicadores mantêm sinal e significância, e nos 50 cruzamentos de
indicador com estrato (complexidade de rede, fator de recursos e força de
recursos) todos são negativos com intervalo excluindo zero.

**O que mudou na versão 2.** Na versão 1, o arranjo centralizado não conseguia
pedir ajuda em nenhum momento, por construção. Com os portões suaves, ele passa
a pedir ajuda à medida que a confiança se constrói, e a vantagem do adaptativo
diminui — sobretudo em falha efetiva (−0,0431 → −0,0229) e fração via Porta 1
(−0,1165 → −0,0511). A diferença entre as versões é a parte do efeito que vinha
da proibição, e não da governança.

---

## Estado atual

### Funciona e está verificado

- Simulador implementado, com identidade bit a bit preservada em todas as
  alterações. A versão 1 continua reproduzível exatamente a partir de
  `config/mvp_v1.yaml`.
- Cinco indicadores com intervalo de confiança, replicados fora da amostra.
- **As três decisões do modelo usam a mesma transição suave.** No TCC I eram
  comparações duras entre dois números, e duas delas degeneravam: a rota de fuga
  nunca disparava e o arranjo centralizado nunca pedia ajuda. Agora a fuga
  dispara de forma gradual, crescendo com a sobrecarga, e a confiança no arranjo
  centralizado sobe de 0,25 para cerca de 0,60 ao longo do projeto, sem alcançar
  a do adaptativo (0,95). Todas as execuções terminam, inclusive as 36 que
  travavam na versão 1.
- Controles publicados reproduzidos: seis pontos de Stewart & Melchers (1988),
  parâmetros da beta-binomial de Stewart (1992) e as frequências da Tabela 2.
- Bateria de controles negativos estabelecendo a resolução do instrumento.
- Cobertura do History Matching: taxa empírica de falsa exclusão de 6,2%,
  IC 95% de Wilson [4,40%; 8,67%], compatível com o nominal de 5%.
- Sensibilidade da seleção heurística à pressão: entre a pressão mínima e a
  máxima, a fração de tarefas pela Porta 1 cresce 2,9 vezes no ponto nominal,
  nos dois arranjos — mesma ordem de grandeza do deslocamento de estratégia
  observado por Rieskamp e Hoffrage (2008), razão ≈ 2,3. Comparação descritiva,
  sem ajuste.
- **Achado sobre fonte primária:** a Tabela 2 de Stewart (1992) não é
  internamente reprodutível na precisão impressa — nenhum par de parâmetros
  satisfaz os três conjuntos publicados ao mesmo tempo (discrepância de 0,012%,
  dentro do arredondamento). A implementação reproduz a fonte; o efeito sobre
  o modelo é nulo.

### Funciona, com ressalva declarada

- **Os parâmetros de governança são premissas sem fonte externa.** Na varredura
  de 81 perfis, restrita aos pares em que o arranjo adaptativo tem premissas
  pelo menos tão favoráveis quanto o centralizado (1 215 pares), o atraso, a
  dívida latente e a omissão favorecem o adaptativo em 76% a 93% dos pares, e a
  fração via Porta 1 em 66%. **A taxa de falha efetiva não é robusta:** favorece o adaptativo em 46% dos pares
  e o centralizado em 53%. A vantagem em falha efetiva vale para os parâmetros
  nominais, não para o espaço de governança como um todo.
- **A inclinação dos portões suaves (0,25) é premissa.** Foi tomada da transição
  cognitiva que o modelo já usava, sem dado nem calibração. Varrida de 0,05 a
  1,00, os cinco contrastes mantêm o sinal em todos os valores; a magnitude de
  falha efetiva e de fração via Porta 1 depende dela.
- **Os experimentos de 20 e 21/09 foram executados pelo revisor e ainda não
  passaram por auditoria independente**: validação fora da amostra, portões
  suaves, nominal versão 2, sensibilidade à pressão e varredura de governança
  da versão 2.

### O que o TCC I previa e mudou

As três decisões de comportamento do agente eram, no TCC I, comparações duras
entre dois números. Duas delas se mostraram degeneradas na implementação — a rota
de fuga, porque a conta nunca passava do limiar, e o pedido de ajuda, porque a
confiança não tinha como mudar. A versão 2 aplica a elas a mesma transição suave
que o TCC2 já usava na primeira decisão. Ver `projeto/74_PORTOES_SUAVES.md` e o
critério de adoção, escrito antes da execução, em
`projeto/75_CRITERIO_DE_ADOCAO_DOS_PORTOES_SUAVES.md`.

---

## Documentação detalhada

| onde | o quê |
|---|---|
| `docs/especificacao_modelo.md` | especificação do simulador, equações e portas de decisão |
| `docs/registro_de_decisoes.md` | registro de decisões com origem rotulada |
| `projeto/04_FONTES.md` | referências, com o que cada fonte sustenta e o que não sustenta |
| `projeto/` | auditorias, pareceres de revisão independente e ordens de serviço |
| `outputs/diagnosticos/README.md` | índice dos experimentos executados |
