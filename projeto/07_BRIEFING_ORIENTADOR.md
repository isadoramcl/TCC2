# Briefing para a reunião de orientação — Entrega 1

Versão navegável publicada como artefato; esta é a cópia versionada, e serve
também de contexto para a próxima sessão de trabalho.
Última conferência contra o repositório: 08/09/2026.

---

## 1. O trabalho em uma página

TCC 1 = fase conceitual (modelo híbrido ABM + Dinâmica de Sistemas para
degradação cognitiva, ocultação de defeito e retrabalho tardio em equipes de
engenharia). TCC 2 = implementação: simulador que roda, calibrado com dados
reais, verificado, com experimento de governança.

Três camadas, nesta ordem:

1. **NASA MDP D″** (17.377 módulos, 12 projetos) → o **gradiente de risco por
   faixa de dificuldade**. É a única coisa calibrada empiricamente.
2. **PSPLIB J60** (480 instâncias, 28.800 tarefas) → topologia do projeto e
   índice de dificuldade `Di` por tarefa.
3. **Simulador + experimento** → três portas de decisão, sistema difuso,
   estoques, e o contraste centralizada × adaptativa.

Regra que organiza tudo: dado bruto imutável, toda transformação por código e
log, e cada decisão com rótulo de origem — `[LIT]`, `[TCC1]`, `[DEC]`,
`[CALIB]`, `[ABERTO]`, `[LIMITACAO]`.

## 2. Pipeline — 24 scripts

`src/nasa/` 01 auditar → 02 consolidar → 03 validar D″ → 04 modelos logísticos
→ 05 faixas de risco → 06 figuras

`src/psplib/` 01 auditar J60 → 02 índice Di → 03 transferência ordinal → 04 figuras

> **Precisão para a reunião.** O SGS serial com prioridade por menor folga
> (Kolisch 1996) é usado **apenas para derivar parâmetros** — tamanho de equipe,
> horizonte e escala de pressão. Ele **não escalona a simulação**: quem decide o
> que começa e quando são os agentes, pelas três portas. E a varredura de pesos
> do `Di` **existe** (seis esquemas, menor correlação de ordenação 0,847,
> `psplib_02_sensibilidade_pesos.csv`); o que é órfão é a declaração
> `pesos_Di` no YAML, que não é lida pelo script.

`src/modelo/` simulador.py + fuzzy.py · 01 derivar parâmetros → 02 verificar →
03 experimento → 04 gêmeo idêntico → 05 figuras → 06 exportar parâmetros →
07 ablação → 08 verificar ablação → 09 sensibilidade τ_mín → 10 decomposição
fatorial → 11 tendência sob pressão → 12 Porta 2 → 13 exportar tabelas →
14 experimento por instância

`docs/gerar_entrega.js` gera o .docx dos CSV e **falha** se uma citação não resolver.

## 3. Decisões a defender

- **Transição heurística estocástica**, não determinística — prevalece o texto do
  TCC 1 sobre o pseudocódigo; a escala tendendo a zero recupera o limiar.
- **p_falha incide em todas as execuções** — senão a calibração NASA ficaria
  inerte no caso nominal e a Porta 3 seria execução limpa garantida.
- **Ramo de reporte acrescentado à Porta 1** — sem ele o cenário adaptativo não
  teria como diferir no ponto que a matriz de cenários declara ser a distinção.
- **T-norma produto**, não mínimo — Van Broekhoven e De Baets (2009): é a única
  configuração de duas entradas com monotonicidade garantida sob centroide.
  Com máx-mín a derivada positiva era 0,259; com produto, ordem de 1e-14.
- **Saída difusa reescalada para [μ_mín, 1]** — separa a FORMA da degradação
  (aporte do método difuso) da MAGNITUDE (premissa declarada).
- **Instância como unidade de inferência**, não semente — pseudorreplicação.
- **Base do retrabalho = esforço planejado** — o realizado inclui ociosidade e
  invertia o sinal do efeito por auto-normalização.

## 4. Achados que mudaram o modelo

- **ACHADO 4** — drenagem da bateria era débito único; 4 de 6 agentes zeravam e
  travavam. Passou a ser por período trabalhado.
- **ACHADO 6** — métrica de retrabalho media visibilidade: termo latente nulo por
  construção (384/384) e denominador inflado pela própria disfunção.
- **ACHADO 8/9** — t-norma e bug de aplicação ao consequente; o fallback que
  devolvia valor médio passou a levantar erro.
- **ACHADO 10** — equifinalidade: `F_âncora` e `f_retrabalho` não se separam
  (36,8% e 6,0%), mas o produto identifica (74,7%).
- **ACHADO 11** — o modo heurístico é a patologia E a única válvula de escape do
  hiato de competência. Condição "ideal" mal especificada dava projeto PIOR
  (makespan 303,5 contra 249,2). Comportamento em P=0 declarado como fronteira
  fora do domínio operacional (P_min = 0,30); é lentidão (~56 períodos de espera
  por tarefa), não travamento.

## 5. Travas resolvidas

| trava | como foi resolvida |
|---|---|
| quatro parâmetros variando juntos | ablação (2.880 exec.) + fatorial 2⁴ saturado (3.072 exec.). Interações carregam 61,8% do contraste na dívida oculta |
| valor-p impossível (Spearman sobre 5 médias, p~1e-24 com piso exato 0,0167) | desenho em duas etapas: piloto n=200 dimensiona por potência, confirmatório n=500 com sementes disjuntas. Critério inalterado |
| pseudorreplicação na tabela principal | re-análise do bruto existente, sem simular. *d* de −2,4 → −7,8; 16/16 favoráveis |
| tabela com valores fabricados | montada do YAML; 12 das 17 tabelas vêm de CSV, as demais conferidas com zero divergência |
| verificador que dava falsa confiança (7 refs quebradas) | identificador simbólico + geração que falha; regra: testar o verificador contra um caso que ele deve pegar |
| testes que passavam por construção | 22 verificações classificadas por classe; a "validação externa" rebaixada com a evidência calculada no próprio script |
| divergência da Porta 2 com o TCC 1 | medida: não material (zero na centralizada, <3% na adaptativa). Declarada como operacionalização a formalizar |

## 6. Travas abertas — decisão da autora com o orientador

- **C3 τ constante** — sustenta a metade temporal do resultado. Sob ablação,
  ociosidade e ocupação INVERTEM. Agravante: `τ_inicial` (centr.) = `τ_mín`
  (adapt.) = 0,25, ambos premissa sem justificativa, exatamente na fronteira do
  portão. Varredura de 11 pontos: degrau, não gradiente; salto único em largura
  1e-4. A desigualdade estrita é do TCC 1 §4.4.3 (conferido); a coincidência dos
  valores é escolha deste trabalho.
- **C1** — TR é esforço contabilizado, não ocupa agente nem avança cronograma.
  Custo de prazo subestimado; E_total tem no denominador parcela que não consome
  capacidade.
- **C2** — makespan inclui cauda após a última tarefa; magnitude do −36,2% é
  condicionada à definição de conclusão. Sinal não está em questão.
- **C4** — "TWi reduzido" da omissão não implementado. **Sem ele o arquétipo de
  Soluções Sintomáticas não existe no modelo.** Provavelmente o código é que está
  errado. É a primeira a levar ao orientador.
- **C6** — ganho de competência permanente aqui, temporário em Crowder.
  Declarado como adaptação, sem juízo de mérito (nenhum teste feito).
- **C5** — ramo de fuga é código morto (0 adiamentos em 384; ω 0,50 < limite 0,60).
- **B5** — onda 2 do HM usou o mesmo gerador. Conclusão reescrita como preliminar.
- **Estrutural** — **não existe validação externa do simulador.** Declarado.

## 7. O que os números dizem

Experimento, instância como unidade (n = 16), todos 16/16 favoráveis:
defeitos ocultos −70,6% (*d* −7,815) · dívida latente de pico −72,8% (−6,726) ·
atraso −36,2% (−5,546) · ocupação +13,3% (+3,752) · retrabalho/plano −23,9% (−3,074).

Sob ablação do mecanismo de assistência: dívida oculta **permanece** (93,5%),
defeitos ocultos permanecem (97,8%), atraso diminui (72,6%), retrabalho pago cai
a 26,0%, ociosidade e ocupação **invertem**.

**Leitura:** não existe "o efeito de governança"; existem dois. A redução da
dívida oculta é robusta e vem conjuntamente de `p_reporte` e `p_deteccao`, que
interagem antagonicamente. A vantagem em tempo/ocupação é condicionada a τ constante.

**Rebaixado:** taxa de omissão é manipulation check — razão prevista 0,2941 vs
observada 0,2892; 98,3% da diferença é o parâmetro reaparecendo na saída.

**NASA:** complexidade ciclomática não sobrevive ao controle de tamanho
(OR 0,944 [0,870; 1,024], p = 0,17). Complexidade de projeto tem OR 1,098
[1,010; 1,194] p = 0,028, mas sob Holm p = 0,084 — **nenhuma das seis sobrevive**.
Os p da ordem de 1e-141 tratam 17.377 módulos como independentes quando estão
agrupados em 12 projetos; o que sustenta a conclusão é o leave-one-project-out e
o bootstrap de projetos.

## 8. Falta fazer

C1–C6 · B5 (onda independente) · B8 (480 instâncias, ~21 min) · B10 (sensibilidade
de F_âncora e do gradiente RR) · B6 (fraquezas do gêmeo idêntico) · B11 (métrica
duplicada) · A10 (horizonte derivado com μ_mín errado) · D1–D6 (documentação) ·
auditar Cole/Danquah/Siverbo/Ye (segurança psicológica) · estender CSV→documento
às seções de dados (engenharia, não bloqueador).

## 9. Perguntas para o Prof. André

1. **C4 é bug ou decisão?** Sem o alívio de curto prazo da omissão, o arquétipo
   que o trabalho formaliza não existe no modelo.
2. **Reabrir τ dinâmico?** Muda experimento, gêmeo idêntico e HM juntos.
3. **O que fazer com τ_inicial = τ_mín = 0,25?** Justificar ou afastar da fronteira.
4. **Porta 2:** voltar à regra literal do TCC 1 ou formalizar o filtro?
5. **Qual definição de conclusão do projeto é a principal?**
6. **O trabalho pode fechar sem validação externa?**
7. **Rodar as 480 instâncias antes ou depois das decisões do bloco C?**
8. **Auditar as quatro fontes de segurança psicológica ou manter como premissa?**
9. **Escopo do TCC final:** o que fecha para a defesa, o que é trabalho futuro.

## 10. Perguntas prováveis de banca

- *"Quatro parâmetros variam juntos — como atribuem o efeito?"* Não atribuímos;
  a decomposição está no fatorial 2⁴ e mostra 61,8% de interação na dívida oculta.
- *"O que significa esse p de 1e-33?"* Que a unidade estava errada. Corrigido
  para n = 16; p no piso significa que todos os pares apontam no mesmo sentido.
- *"Vocês validaram o simulador?"* Não. Verificamos, e a distinção está explícita.
- *"Por que a complexidade ciclomática se ela não sobrevive?"* Como marcador
  ordinal estável, não como fator causal — a afirmação causal foi abandonada.
- *"Esse número veio de onde?"* Seção de rastreabilidade: instâncias, sementes,
  execuções e arquivo de saída por procedimento.
