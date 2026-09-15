# Revisão independente — branch `codex/auditoria-documentacao` (72e6a64)

**Revisor:** Claude · **Autor/implementador:** Codex · **Data:** 15/09/2026
**Objeto:** commit `72e6a64fc53125b6c253bf1acea3eb11ba00b731`, autoria `isadoramcl`,
15/09/2026 00:41 −03, "Documenta estado local, divergencias e diagnostico das ondas HM".

Esta revisão não altera o modelo, não corrige código e não escolhe soluções. Ela
verifica o que foi feito, tenta falsificá-lo e registra o que sobreviveu.

---

## 0. Método e limites desta revisão

O que foi efetivamente executado por mim, e não apenas lido:

| verificação | como |
|---|---|
| Extração isolada da branch publicada | `git archive origin/codex/auditoria-documentacao` para diretório limpo, fora do checkout da autora |
| Reexecução do piloto | `python3 src/modelo/15_diagnostico_hm.py` nesse diretório, **em ambiente diferente do registrado no manifesto** |
| Reanálise das ondas de HM | script próprio sobre `modelo_04_hm_onda1.csv`, `..._onda2.csv`, `..._observacoes_sinteticas.csv` |
| Conferência de hashes | comparação entre `manifesto.json` (estado local) e `verificacao_publicacao.json` (base `8f27477`) e os arquivos em disco |
| Conferência de fontes | texto integral de Pukelsheim (1994) e de McCulloch et al. (2022) |

**Limites declarados.** Não consegui fazer `fetch` do remoto (o shell não tem
credencial): tudo que afirmo sobre o estado do GitHub vale **para as referências
do clone local**, não para o servidor. Não reexecutei os pipelines NASA nem
PSPLIB. Não auditei a monografia do TCC I. Não abri o DOCX.

---

## 1. Estado que consegui verificar

### 1.1 O que a branch é, estruturalmente

`72e6a64` é **um único commit**, cortado de `origin/main` (`8f27477`), com 14
arquivos e 1.283 inserções. `origin/main` não foi tocada — confirmado.

Mas a base importa mais do que o commit. A branch **não contém**:

- `projeto/00_INSTRUCOES_DO_PROJETO.md` a `projeto/06_B9_VERIFICACAO.md`;
- `src/modelo/06_exportar_parametros.py` a `src/modelo/14_experimento_por_instancia.py`;
- 29 das 70 tabelas de `outputs/tables/` que existem em `origin/revisao-auditoria`.

Ela salta de `05_figuras_modelo.py` para `15_diagnostico_hm.py`. O Codex declara
isso com todas as letras ("Esta auditoria descreve o estado local, que inclui
código e tabelas ainda pendentes de integração") — a declaração é honesta. A
consequência, porém, permanece: **o artefato publicado descreve uma árvore que
não existe em nenhum commit.**

### 1.2 Reprodução do piloto — **REPRODUZIDO**

Extraí a branch para um diretório limpo e rodei o diagnóstico publicado. Saída:

```
desenho.csv        IDÊNTICO
piloto_bruto.csv   IDÊNTICO
piloto_resumo.csv  IDÊNTICO
verificacoes.json  IDÊNTICO   (7/7 verificações verdadeiras)
```

E isso num ambiente **diferente** do registrado:

| | manifesto do Codex | minha reexecução |
|---|---|---|
| Python | 3.9.6 | 3.10.12 |
| numpy | 1.26.4 | 2.2.6 |
| pandas | 2.2.3 | 2.3.3 |
| PyYAML | 6.0.2 | 6.0.3 |

A reprodução é portanto **mais forte do que o Codex reivindicou**: atravessa uma
mudança de major do numpy. Tempo total: 9,8 s, 128 execuções.

A afirmação paralela — de que o piloto saiu idêntico no estado local e num
checkout isolado de `origin/main` — também se sustenta, e vale mais do que
parece. Os hashes do manifesto mostram que as duas bases têm `simulador.py`,
`fuzzy.py` e `config/parametros.yaml` **diferentes**, e ainda assim a saída é
igual byte a byte. Isso é evidência real de que a instrumentação de ablação é
neutra *neste caminho de código*. Não certifica igualdade fora dele, e o Codex
diz exatamente isso.

**Escopo correto da alegação:** o que foi reproduzido é o piloto — 8 dos 400
pontos da onda 2, 2 instâncias, 4 sementes. Não é reprodução do History
Matching. O documento do Codex não confunde as duas coisas.

### 1.3 O defeito do RNG — confirmado por reconstrução independente

Recalculei as coordenadas normalizadas das duas ondas a partir dos CSV
publicados, sem usar o script do Codex:

```
máx |u_onda1 − u_onda2| = 1,22e-15
```

`main()` cria `rng_desenho = default_rng(20260905)` a cada invocação, e tanto
`onda1` quanto `onda2` consomem esse RNG recém-semeado. A onda 2 é a **imagem
afim exata** do desenho da onda 1 dentro da nova caixa. Defeito real.

A retificação do Codex também está certa: dizer que "a onda 2 não avaliou nenhum
ponto novo" é falso — a caixa mudou, logo os vetores físicos mudaram. O erro é
usar um desenho dependente como evidência de refinamento independente.

### 1.4 O empate de τ — o Codex está factualmente certo

YAML nominal: centralizada `tau_inicial=0,25`, `tau_min=0,60`; adaptativa
`tau_inicial=0,80`, `tau_min=0,25`. Nenhum cenário tem os dois iguais. A
formulação do `02_ORDEM_DE_SERVICO.md` ("Coincidência τ_inicial = τ_mín = 0,25")
é ambígua e merecia a correção. Ver, porém, **MAJOR-6**.

---

## 2. Problemas confirmados

### CRITICAL-1 — A não-identificabilidade "estrutural" é contradita pelos dados da própria onda 1

**Problema.** `04_gemeo_identico.py` imprime, no relatório e no log, que
"os observáveis agregados só veem o PRODUTO" de `F_ancora × f_retrabalho` e que
isso é "não-identificabilidade ESTRUTURAL, não falta de amostra". A onda 1
falsifica essa afirmação.

**Evidência.** Correlação de cada observável com cada parâmetro, 400 pontos:

| | taxa_omissao | atraso_relativo | retrabalho/plano | E_total |
|---|---|---|---|---|
| **risco.F_ancora** | **0,950** | 0,011 | 0,780 | −0,775 |
| **retrabalho.f_retrabalho** | **0,022** | −0,013 | 0,570 | −0,568 |
| agentes.tau_sat | −0,053 | −0,123 | −0,093 | 0,029 |
| agentes.k_heuristico | 0,038 | 0,090 | 0,080 | −0,045 |
| **fuzzy.mu_minimo** | −0,025 | **−0,977** | −0,077 | −0,221 |

`taxa_omissao` é quase função pura de `F_ancora` (r = 0,950) e praticamente
independente de `f_retrabalho` (r = 0,022). O R² de `taxa_omissao` cai de **0,904**
(cinco parâmetros) para **0,613** quando se substitui o par pelo produto. Ou
seja: o desenho **contém** o canal que separa frequência de severidade. O Codex
levantou a suspeita ("a taxa de omissão é um observável separado do custo de
correção"); os dados confirmam e quantificam.

**Arquivos.** `src/modelo/04_gemeo_identico.py` (bloco "REPARAMETRIZACAO SUGERIDA
PELA CRISTA", ACHADO 10); `outputs/logs/modelo_04_gemeo_identico.log`;
`outputs/tables/modelo_04_hm_onda1.csv`.

**Impacto.** A recomendação registrada — "tratar o produto como o parâmetro a
estimar e declarar a divisão entre frequência e severidade como NÃO
identificada" — descarta informação que o modelo produz. Se essa frase for para
a monografia, a banca pode derrubá-la com a própria tabela do trabalho.

**Causa:** demonstrada. **Confiança:** alta.
**Como testar:** recalcular o NROY com ponderação que não deixe um único
observável dominar (ver CRITICAL-2 e MAJOR-4) e verificar se a largura marginal
de `F_ancora` colapsa.

---

### CRITICAL-2 — A largura do NROY é piso de ruído de Monte Carlo, não limite estrutural

**Problema.** Cada ponto do desenho é avaliado com **K = 8 execuções**
(2 instâncias × 4 sementes). `V_sim` é a variância dessa média. A largura do NROY
é governada por esse denominador, não pela geometria do modelo.

**Evidência 1 — escala.** Amplitude de `media_taxa_omissao` no desenho: 0,1354.
Desvio-padrão médio da média com 8 execuções: 0,0139. Razão sinal/ruído ≈ **9,8**.

**Evidência 2 — experimento de escritório.** Recalculando I com V/8 (equivalente
a K = 64), mantidas as médias:

| | NROY | F_ancora | f_retrabalho | tau_sat | k_heuristico | mu_minimo |
|---|---|---|---|---|---|---|
| atual (K = 8) | 40 (10%) | 34% | 3% | 11% | 2% | 69% |
| K = 64 | 4 (1%) | **60%** | **42%** | 20% | **32%** | **95%** |

**Evidência 3 — referência externa verificada.** McCulloch et al. (2022), a fonte
que o próprio script cita para o gêmeo idêntico, usa K = 30, 100 e 200 réplicas
por ponto nos seus três estudos de caso. K = 8 está uma ordem de grandeza abaixo
da prática da fonte citada.

**Impacto.** A frase impressa sem condicional — "as ondas CONVERGIRAM. Uma
terceira onda não reduziria o espaço — o limite é a identificabilidade
estrutural, não o tamanho da amostra" — inverte o diagnóstico. O limite observado
é de **amostra**, só que na dimensão errada: o esforço foi alocado em 400 pontos
× 8 réplicas, quando o que trava a inferência é o número de réplicas.

**Causa:** demonstrada como hipótese forte. A aproximação mantém as médias fixas;
réplicas reais também as deslocariam ligeiramente.
**Confiança:** alta quanto à direção e à ordem de grandeza; média quanto aos
percentuais exatos.
**Como testar:** reexecutar ~40 pontos da onda 1 com K = 64 e recomputar as
larguras. Se `f_retrabalho` sair de 3% para algo próximo de 40%, está encerrado.

---

### CRITICAL-3 — O portão de confiança é um booleano constante: "confiança" não é mecanismo no modelo

**Problema.** `confianca` é atribuída uma única vez, na construção do agente, com
`tau_inicial` do cenário, e nunca mais é alterada. A Porta 2 testa
`k.confianca > tau_min`, desigualdade estrita. Portanto:

| cenário | confiança | τ_mín | teste | resultado |
|---|---|---|---|---|
| centralizada | 0,25 | 0,60 | 0,25 > 0,60 | **falso sempre** |
| adaptativa | 0,80 | 0,25 | 0,80 > 0,25 | **verdadeiro sempre** |

O portão não é um portão: é uma chave liga/desliga fixada por dois números do
YAML. `TL = 0,00` no braço centralizado é aritmética, não comportamento
simulado. Em 2.880 execuções o portão não variou uma única vez.

**Agravante não documentado em lugar nenhum.** `confianca` também alimenta o
sistema difuso, como `desconfianca = 1 − confianca`. Logo `tau_inicial` move
**dois canais ao mesmo tempo**: o portão de assistência e o multiplicador
cognitivo (desconfiança 0,75 na centralizada contra 0,20 na adaptativa).
Procurei menção a esse duplo papel em `05_B9_ABLACAO.md`,
`06_B9_VERIFICACAO.md` e `especificacao_modelo.md`: não há.

**Impacto.** O braço "só τ_inicial" da ablação B9, que reproduz 91% a 99,8% do
contraste de tempo e ocupação, e o fator A do fatorial 2⁴ **confundem dois
mecanismos distintos**. A leitura corrigida proposta em `06_B9_VERIFICACAO.md`
§1.3 — "ao neutralizar a assistência, o contraste de ociosidade desaparece" —
ainda atribui a um mecanismo um efeito que pode ser em parte do outro.

**Crédito devido.** `05_B9_ABLACAO.md` §1.1 já registra o empate exato e a
descontinuidade (τ_mín = 0,2499 faz `TL` saltar de 0,000 para 8,042) e conclui
que `TL = 0` "não é uma propriedade robusta do arranjo". Esse achado é correto e
é bom. O que falta é o duplo papel de `tau_inicial` e a consequência para a
interpretabilidade da ablação.

**Causa:** demonstrada por leitura de código e pelos valores do YAML.
**Confiança:** alta.
**Como testar:** separar `confianca_portao` de `confianca_cognitiva` no
simulador e ablacionar cada uma isoladamente. Se o efeito de A se dividir entre
as duas, a atribuição atual precisa ser reescrita.

---

## 3. Problemas suspeitos que ainda precisam de teste

### MAJOR-4 — O corte I ≤ 3 é aplicado a um máximo de quatro observáveis; a justificativa vale para um

Verifiquei o texto de Pukelsheim (1994). O teorema exige distribuição com
**densidade de Lebesgue unimodal**, dá o limite 4/81 < 0,05, e trata de **uma**
variável aleatória. Não há nenhuma discussão de máximos.

O projeto define `I(x) = max_j I_j(x)` sobre quatro observáveis e herda a
garantia de 95% como se fosse conjunta. Corroboração empírica: o próprio backlog
(B6) registra que `I(verdade)` ultrapassa 3 em cerca de 10% dos blocos — o dobro
do que a justificativa citada implicaria.

Agravante que só apareceu na reanálise: **`atraso_relativo` é o máximo em 205 dos
400 pontos**, e é o observável que menos informa sobre os parâmetros em disputa
(|r| ≈ 0,01 com `F_ancora` e `f_retrabalho`). `taxa_omissao`, que carrega r = 0,950
com `F_ancora`, é o máximo em apenas 32 pontos e tem I mediano 1,789. O NROY está
sendo esculpido por uma dimensão que não identifica o que se quer identificar.

| corte aplicado a | NROY (onda 1) |
|---|---|
| só `taxa_omissao` | 282 |
| só `atraso_relativo` | 115 |
| só `retrabalho_sobre_plano` | 151 |
| só `E_total` | 144 |
| máx dos quatro (atual) | **40** |

**Ressalva de justiça:** McCulloch et al. (2022) usam a mesma construção e a
mesma justificativa. Isto é herdado da literatura, não invenção do trabalho.
Classificação da relação afirmação-fonte: **INFERENCE**, não SUPPORTED.
Deve ser declarado como tal, não corrigido às pressas.

**Confiança:** alta quanto ao fato; média quanto ao melhor remédio.

---

### MAJOR-5 — "Convergência" está sendo medida por casco envolvente, estatística insensível

A onda 2 amostra dentro do casco do NROY da onda 1, logo `largura₂ ≤ largura₁`
por construção. As larguras caíram entre 0,3% e 4,4% — e isso foi lido como
convergência. Enquanto isso:

```
NROY onda 1 : 40/400 = 10,0%
NROY onda 2 : 115/400 = 28,7%
```

A fração quase **triplicou**. O conjunto mudou muito; a caixa que o envolve, quase
nada. Além disso, 71% do volume do casco da onda 1 é implausível — o NROY não
tem forma de caixa, e as "larguras marginais" que sustentam os veredictos de
identificabilidade são projeções de um conjunto que não é retangular.

**Hipótese minha que NÃO sobreviveu, e registro isso:** eu previa que, sendo o
desenho da onda 2 imagem afim do da onda 1, os extremos do casco se preservariam
e as larguras seriam *exatamente* iguais. Falso: apenas 3 dos 9 pontos extremos
da onda 1 sobrevivem no NROY da onda 2 (Jaccard entre os conjuntos = 0,165). A
quase-igualdade das larguras tem causa substantiva — o piso de ruído do
CRITICAL-2 — e não é tautologia do desenho.

**Como testar:** medir volume ou densidade do NROY, não o casco.

---

### MAJOR-3 — `V_sim` trata 8 execuções correlacionadas como independentes

`var(ddof=1)/n` com n = 8, sobre 2 instâncias × 4 sementes. Decomposição que fiz
sobre `piloto_bruto.csv`:

| observável | fração da variância entre instâncias |
|---|---|
| E_total | 24,2% |
| retrabalho_sobre_plano | 23,3% |
| taxa_omissao | 13,9% |
| atraso_relativo | 9,4% |

Parte de `V_sim` é diferença sistemática entre duas instâncias, que **não encolhe
com mais sementes**. Com 2 instâncias há 1 grau de liberdade para essa
componente: ela não é estimável de forma confiável. A razão entre a variância
por agrupamento e a iid vai de 0,45 a 1,23 conforme o observável — isto é, o
tratamento atual erra em ambas as direções, por um fator de até ~2.

**Consequência prática para o CRITICAL-2:** aumentar sementes reduz só a
componente interna. Reduzir o piso de ruído exige aumentar **instâncias e**
sementes, não apenas sementes.

---

### MAJOR-1 — A documentação publicada aponta para evidências que não estão na branch

Dez arquivos citados no `08_AUDITORIA_AUTONOMA_2026-09-15.md` e no
`07_AUTONOMIA.md` não existem na árvore publicada:

`06_B9_VERIFICACAO.md`, `00_INSTRUCOES_DO_PROJETO.md`,
`modelo_07_ablacao_bruto.csv`, `modelo_09_sensibilidade_tau_min.csv`,
`modelo_10_fatorial_celulas.csv`, `modelo_11_tendencia_piloto.csv`,
`modelo_11_tendencia_confirmatorio.csv`, `modelo_12_porta2_bruto.csv`,
`modelo_14_experimento_por_instancia.csv`, `modelo_04_hm_onda2.csv` (citado por
apelido).

O inventário afirma 61 tabelas de nível superior; a branch tem 41. Nenhum link
markdown está quebrado — as citações são em texto —, mas quem clonar a branch não
alcança a evidência. A auditoria diz que descreve "o estado local"; ainda assim,
um relatório de auditoria cuja base probatória não é versionada não é auditável
por terceiros, que é exatamente o que a regra 1 do `00_INSTRUCOES` existe para
garantir.

---

### MAJOR-2 — O "documento oficial" não existe em nenhum commit

Três versões distintas do DOCX:

| onde | bytes |
|---|---|
| cópia local (declarada oficial) | 2.589.341 |
| `origin/main` | 2.038.596 |
| `origin/revisao-auditoria` | 1.897.843 |

O README passou a instruir que "a versão no Git pode estar atrasada" em relação a
uma cópia que **não está no Git**. Isso institucionaliza como referência um
artefato sem cópia de segurança, num projeto que trabalha em duas máquinas
sincronizadas por Git, e contraria a regra de que o documento é gerado por
`gerar_entrega.js` — se ele foi editado fora do gerador, deixou de ser
reproduzível.

Além disso, o checkout do Mac tem **73 alterações preparadas e não commitadas**
sobre `main`, e o conteúdo delas coincide com `origin/revisao-auditoria` exceto
por README e DOCX. Resultado: o único artefato insubstituível do projeto é o DOCX
local, e ele está numa única máquina.

**Verificação da instrução da autora:** o Codex atribui a designação do DOCX
oficial a instrução explícita da autora, registrada em `07_AUTONOMIA.md`. Esse
registro é auto-atestado pelo próprio Codex; não tenho como confirmá-lo de
forma independente. **NÃO VERIFICÁVEL.**

---

### MAJOR-6 — A correção do empate está certa, mas enterra o achado que ela corrige

`08_AUDITORIA` diz: "não descrever o cenário centralizado nominal como se já
tivesse igualdade entre os dois parâmetros". Correto quanto ao YAML, e correto
como crítica à redação do `02_ORDEM_DE_SERVICO.md`.

Mas `05_B9_ABLACAO.md` §1.1 não cometeu esse erro: ela identifica exatamente a
coincidência cruzada e extrai dela um resultado — o braço "só τ_mín" da ablação é
**identicamente nulo por empate**, e a descontinuidade aparece na quarta casa
decimal. Quem ler apenas a branch publicada concluirá que a questão foi
exagerada, e não terá como chegar à evidência, porque `05_B9_ABLACAO.md` não está
publicada nela. Erro de omissão, não de fato — mas com consequência.

---

## 4. Onde discordo da priorização do Codex

O backlog do Codex põe **B5 (desenho do HM)** em primeiro lugar. Discordo da
ordem, não do item.

Trocar a semente por onda, mantendo K = 8 e o máximo sobre quatro observáveis,
vai produzir larguras muito parecidas com as atuais — e esse resultado será lido
como **confirmação** de que a não-identificabilidade é estrutural. Seria o pior
desfecho possível: um teste que parece falsificar e na verdade só reencena o piso
de ruído.

Ordem que proponho:

1. **CRITICAL-2 e MAJOR-4** — número de réplicas e regra de agregação de I. São o
   denominador de tudo o mais.
2. **CRITICAL-1** — reavaliar a reparametrização pelo produto à luz do canal
   `taxa_omissao → F_ancora`.
3. **B5 / desenho independente** — só agora, quando o resultado for interpretável.
4. **CRITICAL-3** — desacoplar portão e entrada difusa; sem isso, a ablação B9 e o
   fatorial 2⁴ não atribuem efeito a mecanismo.
5. A10/B6 (`concluiu`, horizonte) — mantenho na posição que o Codex deu.
6. C1/C2/C3 e o restante — sem alteração.

Também elevaria **C3 (confiança dinâmica)** da posição 5 para logo depois do item
4: não é ajuste fino, é uma lacuna conceitual entre o TCC I, que trata confiança
como variável, e o TCC II, onde ela é constante de cenário.

---

## 5. A pergunta central: o que emerge e o que é imposto

| resultado | emerge do fenômeno? |
|---|---|
| `TL = 0,00` no braço centralizado | **Imposto.** `0,25 > 0,60` é falso. Aritmética de duas constantes. |
| Contraste de tempo/ocupação entre arranjos | **Imposto em grande parte.** Chave liga/desliga da assistência, confundida com deslocamento constante do multiplicador cognitivo. |
| Largura do NROY / "não-identificabilidade estrutural" | **Imposto.** Piso de ruído com K = 8 e regra do máximo. |
| Qual observável define I | **Imposto.** Escala de variância, não conteúdo informativo. |
| `S_UR_final = 0` em 384/384 | **Imposto.** Condição de parada exige dívida vazia. Já reconhecido no projeto. |
| Interação antagônica CD (p_reporte × p_detecção), −45,5% da dívida oculta | **Plausivelmente emergente.** Dois canais fazendo o mesmo trabalho. Melhor candidato a achado genuíno do trabalho. |
| Crista `F_ancora × f_retrabalho` em `retrabalho/plano` e `E_total` | **Parcialmente emergente.** Real nesses dois observáveis (r = 0,98 e 0,97 com o produto); mas não é estrutural no conjunto, porque `taxa_omissao` separa os fatores. |
| Hiato estrutural de 24,2% das tarefas acima da competência máxima | **Imposto pela instância**, e o `05_B9_ABLACAO.md` já o trata corretamente como controle. |

---

## 6. Referências verificadas

| fonte | existe | o que sustenta | relação |
|---|---|---|---|
| Pukelsheim, F. *The Three Sigma Rule*. The American Statistician, 48(2):88–91, 1994 | **sim**, metadados conferidos | Desigualdade de Vysochanskii–Petunin para distribuição com **densidade de Lebesgue unimodal**; limite 4/81 < 0,05 para **uma** variável; nenhuma discussão de máximos | **PARTIALLY SUPPORTED.** O uso no corte I ≤ 3 sobre `max_j` extrapola. |
| Andrianakis, I. et al. PLoS Comput Biol 11(1):e1003968, 2015 | **sim**, metadados conferidos | History Matching bayesiano com emulação, implausibilidade e NROY | **SUPPORTED** para o método. |
| McCulloch, J. et al. JASSS 25(2):1, 2022 | **sim**, texto integral consultado | Gêmeo idêntico; identificabilidade/equifinalidade em ABM; I = d²/(V_o+V_s+V_m) com corte 3 por Pukelsheim; K = 30/100/200 réplicas nos estudos de caso | **SUPPORTED** para gêmeo idêntico e HM. E fornece **contraevidência** ao K = 8 adotado. |

Fontes **não revalidadas nesta rodada**, e portanto sem sustentação renovada:
Shepperd et al. (2013), De Reyck e Herroelen (1996), Crowder et al., NASA
SWE-220, Liu/Triantis/Sarangi, Van Broekhoven, e as quatro fontes de segurança
psicológica já declaradas pendentes (Cole et al. 2022; Danquah 2024; Siverbo
2023; Ye et al. 2025). O próprio Codex declarou que não as revalidou.

---

## 7. O que o Codex fez bem, e deve ser preservado

Registro porque uma revisão que só aponta defeito é inútil para calibrar a
próxima rodada.

1. **O script de diagnóstico tem controle positivo e negativo.** `15_diagnostico_hm.py`
   falha por `assert` se o defeito legado **não** for reproduzido. Isso implementa
   literalmente a lição "antes de confiar num verificador, alimente-o com um caso
   que ele deveria pegar". Verifiquei que as asserções são vivas: rodei o script.
2. **Recusa-se a sobrescrever.** `mkdir(exist_ok=False)`, hashes de entrada
   conferidos ao fim, nenhuma escrita nas ondas publicadas.
3. **O escopo das alegações está correto.** Piloto não é HM; contagem de pontos
   aceitos não é medida de qualidade; a semente nova é escolha declarada, não
   calibrada para aumentar aceitação. Todas essas ressalvas estão no documento e
   todas se confirmam.
4. **A retificação sobre "não avaliou pontos novos" é tecnicamente correta** e
   corrige um erro real do registro anterior.
5. **A retificação sobre o empate de τ é factualmente correta** (ver MAJOR-6 para
   o que falta nela).
6. **Preservou o trabalho não commitado da autora.** Confirmado: as 73 alterações
   preparadas continuam intactas e `origin/main` não foi tocada.

---

## 8. Backlog científico revisado

| # | item | classe | critério de encerramento |
|---|---|---|---|
| 1 | Réplicas por ponto: K = 8 → K ≥ 32, com mais instâncias, não só sementes | CRITICAL-2 + MAJOR-3 | Larguras marginais recomputadas; declarar explicitamente se a identificabilidade era de amostra |
| 2 | Regra de agregação de I: máximo sobre 4 observáveis com garantia de 1 | MAJOR-4 | Ou justificar o máximo com cobertura conjunta medida, ou declarar como INFERENCE na entrega |
| 3 | Reparametrização pelo produto: reavaliar à luz de `taxa_omissao → F_ancora` | CRITICAL-1 | Retirar ou requalificar o ACHADO 10 e a recomendação dele |
| 4 | B5: gerador independente por onda, com guarda contra desenho repetido | confirmado | Rodar **depois** de 1 e 2, nunca antes |
| 5 | Desacoplar `confianca` do portão e da entrada difusa; reablacionar | CRITICAL-3 | Efeito do fator A dividido entre os dois canais |
| 6 | Medir NROY por volume/densidade, não por casco | MAJOR-5 | Critério de convergência que reaja quando o conjunto muda |
| 7 | Publicar a base probatória: integrar `revisao-auditoria` ou republicar a auditoria sobre ela | MAJOR-1 | Clone limpo da branch contém todos os arquivos citados |
| 8 | Versionar o DOCX oficial ou restaurar a geração por script | MAJOR-2 | Nenhum artefato insubstituível fora do Git |
| 9 | Reinserir em `08_AUDITORIA` o achado de `05_B9_ABLACAO` §1.1 | MAJOR-6 | Descontinuidade em τ_mín = 0,2499 citada onde a correção aparece |
| 10 | A10/B6 (`concluiu`, horizonte), inferência NASA agrupada, A11, B11, C1/C2/C4/C5/C6 | do backlog do Codex | como ele definiu |

---

## 9. Questões que voltam ao Codex

Todas são investigáveis autonomamente. Nenhuma pede decisão da autora.

1. Reexecutar 40 pontos da onda 1 com K = 64 (16 instâncias × 4 sementes, ou
   4 × 16) e reportar as larguras marginais antes/depois. **A predição desta
   revisão é que `f_retrabalho` sai de ~3% para ~40%.** Se não sair, esta crítica
   cai e o argumento estrutural ganha força — registrar o resultado nos dois casos.
2. Medir a cobertura empírica do corte I ≤ 3: gerar N conjuntos de observações
   sintéticas a partir do vetor verdadeiro com sementes distintas e contar em que
   fração delas o verdadeiro é excluído. Se ficar perto de 10%, o corte precisa
   ser recalibrado ou declarado.
3. Separar `confianca_portao` de `confianca_cognitiva` e repetir a ablação B9.
   Quanto do efeito de A é assistência e quanto é multiplicador cognitivo?
4. Verificar se `taxa_omissao` sozinha identifica `F_ancora` quando `V_sim` cai:
   largura marginal de `F_ancora` sob corte aplicado só a esse observável, com
   K = 64.
5. Instrumentar `rodar()` para registrar `concluiu`, dívida pendente e violações,
   e varrer os **extremos** da caixa a priori, não só o interior já reduzido.
6. Confirmar se a instrumentação de ablação é neutra fora do caminho testado:
   impressão digital sobre o cenário centralizado e sobre `03_experimento_cenarios.py`,
   comparando `origin/main` e `origin/revisao-auditoria`.

---

## 10. Memória científica desta rodada

**Verificado e sobrevive:** reprodução do piloto (cross-version); defeito do RNG;
valores nominais de τ; neutralidade da instrumentação de ablação neste caminho;
existência e metadados de Pukelsheim, Andrianakis e McCulloch; preservação do
trabalho não commitado e de `origin/main`.

**Falsificado nesta rodada:** a afirmação de não-identificabilidade estrutural
(CRITICAL-1); a leitura de que as ondas convergiram (CRITICAL-2, MAJOR-5).

**Hipótese minha que não sobreviveu:** a de que as larguras da onda 2 seriam
exatamente iguais às da onda 1 por construção do desenho afim. Falsa — apenas
3 dos 9 pontos extremos sobrevivem. Fica registrada porque a razão pela qual ela
falhou é o que levou ao diagnóstico correto.

**Em aberto:** magnitude real do ganho com K maior (medida, não estimada);
cobertura empírica do corte 3; divisão do efeito de `tau_inicial` entre os dois
canais; se o casco envolvente foi usado em mais lugares além do relatório de
identificabilidade.

**Não verificável por mim:** estado do GitHub remoto (sem credencial no shell);
a instrução da autora sobre o DOCX oficial (auto-atestada em `07_AUTONOMIA.md`);
conteúdo do DOCX.
