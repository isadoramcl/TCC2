# Ordem de serviço consolidada

Backlog unificado das três revisões independentes (auditoria de repositório com
execução de código; revisão metodológica; revisão de texto e fontes) mais as
verificações feitas depois. **80 itens.**

> **Fechamento da Entrega 1 (07/09/2026).** Concluídos nesta rodada: A1–A11, B2,
> B4, **B1**, **B3**, **B9** (mais a decomposição fatorial 2⁴, a sensibilidade de
> τ_mín e a comparação da Porta 2, que não estavam previstos e nasceram do que a
> B9 encontrou). As verificações desta entrega estão encerradas. Nada foi
> commitado por Claude; nenhuma alteração estrutural foi feita no modelo nominal.

Status: `[ ]` aberto · `[x]` feito · `[!]` decisão da autora · `[?]` a confirmar

Regra de entrega, para todos: diff/patch em branch, tabela ANTES/DEPOIS de todo
número publicado que mudar, e nada muda em silêncio.

---

## BLOCO A — código: correções mecânicas

- [ ] **A1** `src/nasa/06_figuras.py:191` lê `04_sobrevivencia_ao_controle_de_tamanho.csv`, que nenhum script gera (o 04 grava `04_complexidade_vs_tamanho.csv`). Corrigir a origem, regerar fig3 e fig4 com os números atuais (OR 0,944 [0,870; 1,024], LR 1,92, p 0,166), remover o CSV órfão, confirmar que clone limpo roda o pipeline inteiro.
- [ ] **A2** `05_figuras_modelo.py`: mover `figura_10()` para antes do `if __name__ == "__main__"` e chamá-la em `main()`. Ler 0,747 e ρ = −0,84 dos CSVs.
- [ ] **A3** Anotações literais: fig8 (30% → +44,8%; 118,2 vs 6,3 → 126,3 vs 5,9; +8,1% → +10,4%); docstring do ACHADO 6 em `simulador.py`; `especificacao_modelo.md` §10.2. Varrer o repositório atrás de outros números escritos à mão.
- [ ] **A4** `requirements.txt`: acrescentar scipy, matplotlib, pyyaml com versão fixa. Tirar `.venv` do versionamento e documentar a recriação no README.
- [ ] **A5** Unificar o resíduo de `S_UR_final` (registro diz 1,1e-13, simulador diz 1,4e-14, medido 8,9e-15) pelo valor medido.
- [ ] **A6** `03_experimento_cenarios.py:48-49`: padrões (24, 20) não reproduzem as tabelas publicadas (16, 12).
- [ ] **A7** `outputs/tables/psplib_04_carga_paralela.csv` é órfão: remover ou reintroduzir o gerador.
- [ ] **A8** Docstring do ACHADO 3 atribui ao TCC1 um defeito que o pseudocódigo não tem (lá a injeção ocorre dentro de `se E(t) > τsat` e é sempre positiva; o sinal negativo veio do ACHADO 2). Rejustificar pela **unidade** do estoque.
- [ ] **A9** `fuzzy.py`: a docstring afirma "nenhum valor numérico embutido", mas `n_malha` (201), `resolucao_cache` (0,001), `largura_saida` (0,30), `REGRAS` e o clip 0,05/0,98 estão no código. Corrigir o fallback `area <= 0` (devolve 0,633 mesmo sob partição uniforme). Ler `semente_padrao` do YAML ou removê-la.
- [ ] **A10** `01_derivar_parametros.py:229`: horizonte 9× derivado com μ_mín = 0,55. Derivar com o menor μ_mín da varredura (0,40 → 16×), ou registrar `concluiu` no History Matching e descartar pontos truncados. A especificação §7 ainda diz 5×.
- [ ] **A11** Remover ou marcar `retrabalho.p_deteccao: 0.05` (config morta) e resolver os outros 4 órfãos: `defuzzificacao`, `inferencia`, `pesos_Di`, `politica_atribuicao`, `replicacoes`. **`pesos_Di` é o mais grave**: está declarado no YAML com varredura, e o script do Di usa 1/3 fixo no código.

## BLOCO B — testes, estatística e re-execuções

- [x] **B1** Verificação 8: Spearman sobre 5 médias é inválido. Refazer sobre os 200 pontos individuais (ρ = 0,32, p = 4e-6), em ≥1 instância e nos **dois** cenários. Reportar que sobre médias o braço adaptativo reprovava (ρ = 0,6, p = 0,28).
- [ ] **B2** Verificações 1, 5, 6, 7, 9 rodam só em `j6010_1`. Rodar em ≥8 instâncias e nos dois cenários. Declarar quais são verdadeiras **por construção** (1, 5, 6, 7a, 7c).
- [x] **B3** Verificação 9a passa para todo `F_âncora` de 0,05 a 0,25 — não restringe nada. Rebaixar de "validação externa" para "verificação de ordem de grandeza".
- [ ] **B4** Restaurar a verificação 4 original: Σ(TW+TL+TU+TR) = tempo total de agente alocado (hoje 891,9 contra 1.426,1 na centralizada — ver C1).
- [ ] **B5** History Matching, onda 2: usar **gerador independente**, re-rodar as duas ondas, reportar as reduções contra a caixa a priori **e** contra a caixa amostrada em cada onda. Corrigir o comentário "sem excluir nada que a onda 1 não excluiu". Se as larguras continuarem estáveis com desenho independente, a conclusão de limite estrutural volta a valer; se não, **retirar a afirmação**.
- [ ] **B6** Gêmeo idêntico: declarar que os critérios são fracos e que `V_mod = 0` torna o teste otimista. Reportar que I(verdade) tem média 2,15 em 20 blocos e ultrapassa 3 em 10% deles, e que o z publicado está 3,4 EP abaixo da média de 160 execuções (Welch p = 0,002) sem mudar o veredito.
- [x] **B7** Experimento: refazer a inferência com a **instância** como unidade. Já medido: 16 de 16 favorecem o adaptativo, p = 3,05e-05, *d* de 3,07 a 7,82. IC bootstrap reamostrando instâncias.
- [ ] **B8** Rodar com as **480 instâncias**. A seleção atual cobre 16 das 48 células, todas com sufixo `_1`. Custo ~21 min.
- [x] **B9** **Ablação obrigatória.** Quatro parâmetros variam juntos. Rodar isoladamente: só `tau_inicial`; só `tau_min`; só `p_reporte` (em varredura, não binário); só `p_deteccao`; e o pacote completo.
- [ ] **B10** Sensibilidade de `F_âncora` (0,05–0,25) e do gradiente RR, incluindo **RR = (1,1,1,1)** — nenhuma transferência. Se a conclusão de governança sobreviver a isso, a transferência ordinal deixa de ser o ponto fraco do trabalho.
- [ ] **B11** Remover `n_com_erro` **ou** `taxa_omissao` da tabela do experimento: são a mesma grandeza dividida por 60. Rebaixar a métrica remanescente a *manipulation check*, com a razão mecânica (0,2941 prevista contra 0,2936 observada) explícita.

## BLOCO C — não implementar: medir e recomendar `[!]`

Branch separado, medição de impacto, recomendação. **Sem merge.** Cada um muda
o que o modelo afirma; a decisão é da autora.

- [!] **C1** Retrabalho ocupando agente e recursos (`simulador.py:383`, `:458`). Hoje `TR` é somado sem consumir tempo nem agente, divergindo da especificação §2/§6.1 e do TCC1 §4.2.
- [!] **C2** Condição de parada (`:368-370`). Cauda de 39,1 períodos (16,2% do makespan) sem tarefa ativa; atraso −36,2% → −22,2% até a última tarefa. Reportar as duas; recomendar qual é a principal.
- [!] **C3** `τ(t)` constante (`:256`). Com τ fixo a centralizada **nunca** ajuda (`TL = 0,00`) e de 7% a 27% das tarefas só saem em modo heurístico. Medir o efeito de uma regra de atualização.
- [!] **C4** "TWi reduzido" da Porta 1 (`:445`). O TCC1 prevê custo de tempo reduzido na omissão — é o alívio de curto prazo que sustenta o arquétipo de Soluções Sintomáticas. **Aqui provavelmente quem está errado é o código.**
- [!] **C5** Ramo de fuga da Porta 2 (`:406`; omega 0,50 contra limite 0,60): 0 adiamentos em 384 execuções. Ativar ou declarar desligado.
- [!] **C6** Competência de Crowder sobe permanentemente; o artigo especifica reset a cada subtarefa. Medir o efeito do reset e declarar como adaptação, seja qual for a escolha.

## BLOCO D — documentação do repositório

- [ ] **D1** `especificacao_modelo.md` §10.2: números vencidos (TU 118,2 vs 6,3 → 126,3 vs 5,9; TR 69,1 vs 52,7 → 68,9 vs 52,5) e §7 (horizonte 5× → valor atual).
- [ ] **D2** Documentar na especificação a condição ΔD ≤ 0 da Porta 3, hoje implementada e omitida do texto normativo.
- [x] **D3** A Entrega 1 afirmava que `p_deteccao` era idêntico e "não é variável de governança". **Falso** — é 0,03 contra 0,12. Corrigido, com o parágrafo declarando que quatro parâmetros variam juntos.
- [ ] **D4** `S_UR(T)` ainda listado como saída substantiva na especificação, mas é nulo por construção. Rebaixar a invariante de encerramento.
- [ ] **D5** `registro_de_decisoes.md`: citações "equação (17)" e "(19)" anteriores à renumeração.
- [ ] **D6** Procedência: `F_base` classificado como calibrado — o calibrado é o **RR por faixa**. E a partição uniforme 0/0,5/1 está como `[LIT]`, mas é `[DEC]`.
- [x] **D7** Detector de parâmetros órfãos e de nomes ambíguos entre seções (`06_exportar_parametros.py`).

## BLOCO E — Entrega 1 (documento) `[?]`

A monografia do TCC1 é **consulta apenas**. As correções entram na Entrega 1.

- [x] **E1** Sete referências cruzadas de equação consertadas.
- [x] **E2** Causa eliminada: identificadores simbólicos + validação que falha a geração.
- [x] **E3** Matriz de cenários montada do YAML.
- [x] **E4** Legendas de figura em formato ABNT (identificação acima, fonte abaixo).
- [ ] **E5** Atualizar as afirmações listadas em `01_ESTADO_DO_TRABALHO.md` → "Afirmado sem sustentação", **depois** que B5, B7, B9 e C2 rodarem.
- [ ] **E6** Retirar "conforme especificado na fase conceitual" sobre a estrutura difusa (o TCC1 não a definiu) e "procedimento validado" sobre Liu et al.
- [ ] **E7** Precisão sobre Pukelsheim: a desigualdade exige distribuição com **densidade** unimodal, não "qualquer distribuição unimodal".
- [?] **E8** Caixa das citações (NBR 10520:2023) — conferir o guia do colegiado da UFMG, que prevalece. Aplicar de forma consistente.
- [?] **E9** Numerais por extenso × algarismos: regra declarada e uniforme.
- [?] **E10** Conferir o template do colegiado antes de assumir que o formato ABNT geral vale.

---

## Ordem recomendada

O critério é: primeiro o que impede reproduzir, depois o que muda número, depois
o que muda texto.

1. **A1, A2, A4** — sem isso ninguém reproduz o pipeline num clone limpo.
2. **B7, B8** — inferência correta e delineamento completo. Mata duas críticas.
3. **B9** — ablação. Sem ela não há atribuição causal a mecanismo nenhum.
4. **B5** — desenho independente na onda 2. Decide se a conclusão de
   identificabilidade estrutural fica ou cai.
5. **B1 a B4, B6, B10, B11** — o restante dos testes.
6. **C1 a C6** — medir, levar à autora, decidir.
7. **A3, A5 a A11, D1 a D6** — encanamento e documentação.
8. **E5 a E10** — regerar a Entrega 1 **por último**, quando os números pararem
   de se mexer.


---

## Pendências metodológicas para a Entrega 2

Em ordem de consequência, não de esforço.

1. ~~**B7 — unidade inferencial.**~~ **FEITO** por re-análise do artefato
   existente (`14_experimento_por_instancia.py`), sem simulação nova. A Tabela 9
   passou à instância como unidade: *d* de −2,4 para −7,8 e 16 de 16 instâncias
   favoráveis. A figura de tamanhos de efeito construída na unidade antiga foi
   **retirada** da Entrega 1 — manter uma figura cuja legenda precisa avisar que
   ela não serve para inferência entrega à banca uma pergunta de graça, e a
   Tabela 9 já traz a análise válida. **Nada resta deste item.** Se um dia
   quisermos uma visualização da inferência por instância, será uma FIGURA NOVA;
   não confundir com a Figura 7 atual, que após a renumeração é outra figura e
   não deve ser alterada.

1b. **Números de resultado digitados no gerador, fora das seções novas.** A
   busca global confirmou que a Tabela 9 não era caso isolado: a Tabela 5
   (ensaios) e os valores citados no corpo das Seções 2.2 a 2.6 — camada de
   dados — ainda são transcritos à mão das saídas dos scripts. Conferidos por
   amostragem contra os CSV de origem (a razão de chances 0,944, o IC
   [0,870; 1,024] e o p = 0,17 batem exatamente), mas sem a garantia
   estrutural. O documento passou a declarar esse escopo. **Estender o
   mecanismo CSV → documento às seções de dados.**
2. **B5 — onda 2 do History Matching com gerador independente.** A afirmação de
   limite estrutural cai se não for reproduzida.
3. **C3 — τ dinâmico.** A B9 mostrou que a metade temporal do contraste depende
   inteiramente do portão de confiança, e a sensibilidade mostrou que, com τ
   constante, esse portão só pode ser um degrau. Reabrir.
4. **Porta 2 — formalizar na especificação** o filtro de competência, com a
   justificativa semântica registrada, ou adotar a regra literal do TCC1. A
   diferença medida não é material; a decisão é de formulação, não de desempenho.
5. **Coincidência τ_inicial = τ_mín = 0,25.** Os dois valores são premissa sem
   justificativa e caem exatamente sobre a fronteira do portão. Justificar ou
   afastar da fronteira — e declarar o que se escolheu.
6. **C2 — condição de parada.** O atraso de −36,2% vira −22,2% medido até a
   última tarefa. Reportar as duas, escolher a principal.
7. **B8 — 480 instâncias.** A seleção atual cobre 16 das 48 células.
8. **B11 — remover a métrica duplicada** (`n_com_erro` ou `taxa_omissao`).
9. **B10 — sensibilidade de F_âncora e do gradiente RR**, incluindo RR = (1,1,1,1).
10. **C1, C4, C5, C6** — medir e decidir. Dois já estão declarados no
    documento como adaptação, e precisam de medição antes de decisão:
    **C1** (TR não ocupa agente nem avança o cronograma) e **C6** (o ganho de
    competência de Crowder é permanente aqui, e o artigo especifica retorno ao
    valor inicial a cada subtarefa).
11. **Correção para comparações múltiplas na figura de sobrevivência.** O
    procedimento de Holm já está calculado em
    `04_sobrevivencia_ao_controle_de_tamanho.csv`, e o texto passou a reportá-lo,
    mas a **figura** ainda desenha o intervalo não corrigido. Marcar as métricas
    que não sobrevivem a Holm na própria figura.
12. **Inferência robusta a agrupamento na camada NASA.** Os valores-p dos
    modelos logísticos e do teste de tendência são calculados sobre 17.377
    módulos agrupados em 12 projetos. O efeito fixo de projeto trata o
    confundimento entre projetos, não a dependência dentro deles; os erros-padrão
    estão subestimados. Já declarado no documento. Refazer com erro-padrão
    robusto a agrupamento — não muda estimativa pontual, muda a precisão.
13. **Lacuna bibliográfica declarada.** A relação segurança psicológica →
    disposição a reportar → `p_reporte` está sustentada no TCC1, que a apoia em
    Cole et al. (2022), Danquah (2024), Siverbo (2023) e Ye et al. (2025).
    **Essas fontes não foram auditadas nesta entrega e não constam da lista de
    referências.** Enquanto isso não for feito, a relação está apresentada no
    documento como premissa de modelagem, e não como resultado da literatura.
    Auditar as quatro e incluí-las, ou manter a classificação como premissa.
