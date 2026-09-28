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

# 3. Validação nominal v3 (diretório novo; não sobrescreve a evidência)
python research/validacao_drenagem_79.py rodar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3
python research/validacao_drenagem_79.py analisar etapa3 outputs/diagnosticos/NOVA_VALIDACAO_V3
```

O nominal é a **v3**: opções em `config/mvp.yaml`, parâmetros em
`config/parametros.yaml`. A execução heurística usa `k_heuristico=k_analitico=0,04`;
a fuga usa `k_fuga=0,10` separado. A v2 histórica está em `config/mvp_v2.yaml`
com `config/parametros_v2.yaml`; a v1 mantém `config/mvp_v1.yaml` com os parâmetros
históricos. A identidade exclui o diagnóstico de violações e declara a exceção
de até 2 ULP em competências/confiança no Mac ARM (parecer 79).

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

### Camada de simulação — nominal v3 final

Contraste adaptativa − centralizada, pareado por instância/semente; IC95 sobre
instâncias. Valores negativos favorecem o arranjo adaptativo.

| Indicador | Nominal 16 | Fora da amostra 48 | Aleatórias 24 |
| --- | --- | --- | --- |
| Atraso relativo | -0.9100 [-1.0473; -0.7728] | -0.9381 [-1.0175; -0.8587] | -0.9528 [-1.0731; -0.8325] |
| Omissão | -0.1743 [-0.1896; -0.1590] | -0.1789 [-0.1882; -0.1697] | -0.1746 [-0.1856; -0.1636] |
| Dívida latente | -0.0547 [-0.0607; -0.0486] | -0.0567 [-0.0604; -0.0529] | -0.0542 [-0.0589; -0.0496] |
| Falha efetiva | -0.0194 [-0.0303; -0.0084] | -0.0192 [-0.0260; -0.0124] | -0.0176 [-0.0269; -0.0083] |
| Fração P1 | -0.0534 [-0.0673; -0.0394] | -0.0447 [-0.0510; -0.0384] | -0.0553 [-0.0661; -0.0446] |

**O que mudou.** A v3 resolve a tensão entre o alívio descrito no TCC I §4.1 e
a drenagem acelerada de §4.4.3: o atalho passa a ter a mesma intensidade por
período da execução analítica; a economia vem de terminar antes. Em tarefa/estado
pareados, o teste mede 25% de redução total quando a duração cai 25%; o
arredondamento pode anular essa economia em tarefas de um período. Adiar continua
sendo outro mecanismo: `k_fuga=0,10`. Não há mais coeficiente acelerado na execução
heurística. As etapas foram executadas e reportadas separadamente.

Comparação v2 → v3 inicial → v3 final, com IC95 e efeitos pareados:
[parecer 79](projeto/79_CONTRADICAO_TCC1_DRENAGEM_HEURISTICA.md) e
`outputs/diagnosticos/20260928_drenagem_heuristica/`.

## Estado atual

- Duas validações completas sequenciais: **4.704 execuções cada**, todas
  concluídas e sem violações. Cada lote cobre nominal, fora48, aleatórias24 e
  governança; a etapa 2 reaproveita 768 execuções da etapa 1.
- **107 testes aprovados** após a separação de fuga, incluindo controles negativos,
  guarda histórica/nova e drenagem efetivamente medida nos dois laços.
- Controle histórico final: **384 execuções × 48 campos**, sem diferenças fora
  da exceção autorizada de plataforma. A guarda dispara uma vez com kh=0,10 e
  zero no nominal v3. Não afirmar identidade integral do diagnóstico de violações.
- Os resultados acima foram recalculados para v3; as verificações de estresse,
  inclinação dos portões, sensibilidade à pressão e History Matching dos pareceres
  anteriores continuam históricas v1/v2 e não são apresentadas como revalidadas na v3.

### Ressalva de governança

A grade de 81 perfis contém 1.215 pares com premissas ordenadas. Frequência de
contrastes negativos não é significância estatística nem garantia universal:

<<<<<<< HEAD
- **Os parâmetros de governança são premissas sem fonte externa.** Na varredura
  de 81 perfis, restrita aos pares em que o arranjo adaptativo tem premissas
  pelo menos tão favoráveis quanto o centralizado (1 215 pares), o atraso, a
  dívida latente e a omissão favorecem o adaptativo em 76% a 93% dos pares, e a
  fração via Porta 1 em 66%. **A taxa de falha efetiva não é robusta:** favorece o adaptativo em 46% dos pares
  e o centralizado em 53%. A vantagem em falha efetiva vale para os parâmetros
  nominais, não para o espaço de governança como um todo. Um teste fatorial
  (`projeto/78`) mostrou que não há causa única: parte dos casos inverte com a
  abertura do pedido de ajuda, parte com a rota de fuga, parte só com as duas
  juntas, sem interação estatisticamente demonstrada — e 6 de 20 casos
  amostrados já favoreciam o centralizado na versão 1.
- **A inclinação dos portões suaves (0,25) é premissa.** Foi tomada da transição
  cognitiva que o modelo já usava, sem dado nem calibração. Varrida de 0,05 a
  1,00, os cinco contrastes mantêm o sinal em todos os valores; a magnitude de
  falha efetiva e de fração via Porta 1 depende dela.
=======
| Indicador | v2 (de 1.215) | v3 etapa 1/2 | v3 final |
| --- | --- | --- | --- |
| Atraso relativo | 1128 | 1115 | 1114 |
| Omissão | 926 | 940 | 950 |
| Dívida latente | 1101 | 1124 | 1103 |
| Falha efetiva | 564 | 504 | 531 |
| Fração P1 | 802 | 806 | 806 |
>>>>>>> c9d076c (v3: k_heuristico derivado de k_analitico; k_fuga separado (parecer 79))

A vantagem em falha efetiva **não é uma conclusão geral para todo o espaço de
governança**. Tabelas com sinal, magnitude e IC95 de cada par estão nos diretórios
etapa2/etapa3; regiões com inversão permanecem reportadas. Nenhum parâmetro foi
ajustado para melhorar essa contagem. Os valores de governança e a inclinação dos
portões seguem premissas, sem calibração externa.

### Histórico preservado

A v1 usa portões duros; a v2 introduziu portões suaves (pareceres 74/75).
A auditoria 76 tem correções registradas no 77. O fatorial 78 não sustentou causa
única para a perda de robustez da falha efetiva na v2; não atribuir toda a diferença
à assistência. A v3 altera drenagem e separa fuga conforme o parecer 79.
O nominal atual não substitui nem apaga os resultados dessas versões.

---

## Documentação detalhada

| onde | o quê |
|---|---|
| `docs/especificacao_modelo.md` | especificação do simulador, equações e portas de decisão |
| `docs/registro_de_decisoes.md` | registro de decisões com origem rotulada |
| `projeto/04_FONTES.md` | referências, com o que cada fonte sustenta e o que não sustenta |
| `projeto/` | auditorias, pareceres de revisão independente e ordens de serviço |
| `outputs/diagnosticos/README.md` | índice dos experimentos executados |
