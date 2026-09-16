# Auditoria independente da correção estrutural — commit `1fd22ff`

**Data:** 16/09/2026 · **Revisor:** Claude · **Autor do código:** Codex
**Objeto:** `codex/resposta-revisao-cientifica`, commit `1fd22ff`, e o parecer 19
**Método:** leitura do código e dos testes, verificação da fonte primária, recomputação aritmética.
Nada foi aceito por ter sido reportado.

---

## Resumo do veredito

| Achado anterior | Estado | Confiança |
|---|---|---|
| A-08 · sem controle de identidade bit a bit | **RESOLVIDO**, acima do pedido | alta |
| A-03 · metade de qualidade da Porta 1 ausente | **RESOLVIDO** | alta |
| A-07 · bloqueio contado como recusa | **RESOLVIDO** | alta |
| D-01 · lei de confiança inventada | **RESOLVIDO** — e o revisor é que estava errado | alta |
| — | **NOVO · MAJOR-7**: a inversão de `E_total` pode ser artefato da convenção de TL | média |
| — | **NOVO · MINOR-8**: o braço legado usa a fórmula de competência fora de escala | alta |

---

## 1. A-08 — controle de identidade bit a bit · RESOLVIDO

`research/test_compatibilidade.py` faz mais do que eu havia pedido:

- compara **todos** os campos do resultado legado por `float.hex()`, não por tolerância;
- compara o **estado do gerador de números aleatórios** (`rng.bit_generator.state`) — o teste
  mais forte possível de identidade de fluxo;
- compara estados internos de agentes, tarefas e dívida pendente;
- usa `patch.object(S.Simulacao,'executar', side_effect=AssertionError)` para **provar que o
  laço do MVP realmente executou**, em vez de delegar ao legado. Sem isso, um teste de
  identidade passaria trivialmente;
- roda sobre instâncias reais do J60, nos dois cenários, com quatro sementes, e cobre
  cinco horizontes de fronteira.

O achado A-08 dizia que sem esse controle não se sabia se as diferenças vinham das mudanças
pretendidas ou de efeitos colaterais. Agora se sabe. Encerrado.

## 2. A-03 — metade de qualidade da Porta 1 · RESOLVIDO

`risco_porta(p0,p_heu,heuristico,rho)` implementa exatamente a formulação especificada:
`q = max(0, 2·p_heu − 1)`; `p_falha,P1 = 1 − (1−p0)(1 − ρ·q)`; `p_falha,P3 = p0`.

Recomputei o caso do teste: `risco_porta(.2,.9,True,.35)` → `1 − 0,8·(1 − 0,35·0,8) = 0,424`. Confere.

Dois cuidados de implementação que merecem registro porque não eram óbvios:

- o retorno antecipado quando `rho==0` ou `q==0` devolve `p0` **por identidade**, sem passar
  pela aritmética — é o que permite que o controle neutro preserve bits exatamente. O teste
  verifica isso com `.hex()`, inclusive em `p0 = 0,19999999999997`;
- o risco é instrumentado por oportunidade (`p0`, `p_fail`, `excesso` no registro), o que
  torna o mecanismo auditável e não apenas o agregado.

## 3. A-07 — bloqueio × recusa · RESOLVIDO

Quatro contadores separados: `N_req`, `N_fail`, `N_blocked`, `N_success`. E, mais importante
que a contagem, a **atribuição** foi corrigida: quando o pedido é enviado e não respondido,
`atualizar_confianca(k, False)` penaliza o **respondente**, não o solicitante. O bloqueio
anterior ao pedido não toca em τ nenhum.

Os testes fixam isso como contrato: `N_req == N_success + N_fail`, e o bloqueio deixa as
duas confianças intactas.

## 4. D-01 — a lei de confiança · CORRETA, E EU ESTAVA ERRADO

Abri o PDF do artigo. Equação (4), p. 1431, literal:

> τ_{t+1} = τ_t + { τ_t·[15 + 3(C_pn − C_r)]/100  se bem-sucedido
>                 { −0,05                          se falhou
> onde 0 ≤ τ ≤ 5

O código faz `tau*(1+dC)` no sucesso e `tau − 0.01` no insucesso, com τ normalizada em [0,1].

- O termo **multiplicativo** no sucesso está correto: τ + τ·ΔC = τ(1+ΔC).
- O decremento de **0,01** é a conversão correta de −0,05 na escala 0–5 do artigo
  (0,05 / 5 = 0,01). **Não é o antigo `decremento_recusa` inventado sobrevivendo disfarçado** —
  eu suspeitei disso e a aritmética não sustenta a suspeita.
- A conversão de escala (`5·C`) antes de aplicar a fórmula está correta, porque todo o modelo
  de Crowder roda em 0–5 (Tabela II: *"data were recalibrated to fit the model's 0–5 scale"*).
- O incremento de competência `dC/5` converte de volta para a escala normalizada. Correto.
- O teto em `min(tar.dificuldade, ...)` reproduz a eq. (2), que limita C_r(t) por D_r. Correto.

### 4.1 Correção que o autor fez no revisor

O parecer 19, item 5, diz: *"O documento 18 contém 'reset da confiança'; prevalecem instrução
da autora e fonte primária, ambas indicando competência."*

Ele está certo. O artigo, p. 1431, logo abaixo da eq. (2):

> *"Note that although a DesignerAgent's competency value may increase during a subtask, once
> completed, this value reverts to its originally inputted level for the next subtask."*

É a **competência** que reinicia. A confiança não tem reset em Crowder. Meu documento 18
escreveu "reset da confiança por subtarefa" no campo da decisão, embora o campo de condições
de contorno do mesmo documento dissesse corretamente "a competência volta ao valor inicial" —
ou seja, o documento se contradizia internamente, e ele foi à fonte primária em vez de seguir
o revisor. Registrado como **R-07** no histórico.

## 5. NOVO · MAJOR-7 — a inversão de `E_total` pode ser artefato da convenção de TL

Este é o achado que importa, e ele nasce de um desvio que o próprio autor declara.

**O desvio declarado.** O parecer 19 diz: *"TL mantém uma unidade por sucesso; não se alega
transplante da Eq. (3)."* A equação (3) de Crowder, p. 1431, é:

> T L(t+1) = T L(t) + 0,5·ΔC_r  se bem-sucedido; +0,05 se falhou

O código faz `self.TL += 1.` por sucesso. Declarado, honesto, e **não é Crowder**.

**Por que isso deixa de ser detalhe.** `E_total = TW/(TW+TL+TU+TR)`. O parecer 19 atribui a
inversão de sinal justamente ao movimento de TL: *"TL adaptativo passa de 10,854 (C4+C1) a
102,859 (com reset). Ao mesmo tempo TW cai de 500,922 para 433,016."*

Ou seja: o denominador da razão que inverteu o sinal é dominado por uma grandeza contada
segundo uma convenção sem base externa — e cuja **forma** difere da fonte por cerca de uma
ordem de grandeza.

**Aritmética.** Com ΔC ≈ 0,21 (valor do próprio teste de Crowder do repositório), a eq. (3)
daria por sucesso 0,5 × 0,21 ≈ 0,105 em vez de 1,0 — fator ~9,5×. Reconstruindo o ramo
adaptativo a partir dos números publicados:

- TW = 433,016 e E_total = 0,655868 ⟹ TW+TL+TU+TR = 660,22 ⟹ TL+TU+TR = 227,20;
- com TL = 102,859, sobra TU+TR = 124,34;
- TL sob a eq. (3) ≈ 0,105 × 102,859 ≈ 10,80;
- E_total adaptativo passaria a 433,016 / (433,016 + 10,80 + 124,34) ≈ **0,762**.

Isso é um deslocamento de **+0,106** contra uma diferença nominal de **−0,0508**. Se o ramo
centralizado — que tem menos eventos de ajuda bem-sucedidos — se deslocar menos, a diferença
volta a ser positiva, e a inversão desaparece. O valor legado era +0,1046, da mesma ordem
do deslocamento estimado.

**Confiança: média.** Não tenho os componentes TW/TL/TU/TR do ramo centralizado, que o
parecer 19 não publica. A conta acima é do ramo adaptativo apenas.

**Teste discriminante (barato).** Rodar a configuração nominal com `TL += 0.5*dC` em vez de
`TL += 1.`, mantendo todo o resto idêntico, e reportar `E_total` nos dois cenários. Duas
linhas de código e uma rodada. Se o sinal voltar a ser positivo, a conclusão de governança
sobre `E_total` **não é um resultado do modelo** — é uma escolha de unidade contábil.

**Por que isso tem de ser resolvido e não apenas declarado.** O parecer 19 já adverte que
`E_total` "é uma razão contábil do modelo" e "não é medida empiricamente calibrada de
produtividade" — a ressalva certa. Mas o mesmo documento apresenta a inversão de sinal como
achado de destaque, em negrito. Não dá para sustentar as duas coisas ao mesmo tempo: ou a
inversão é informativa sobre governança, e então a unidade que a produz precisa de defesa,
ou ela é uma consequência da convenção, e então não deve ser destacada como resultado.
Publicar uma inversão de sinal cuja causa provável é uma escolha de contagem é o caminho
mais curto para uma pergunta de banca que não tem resposta.

**Recomendação.** Adotar a eq. (3) como alternativa varrida no lote — do mesmo jeito que
protocolo, lei e reset já têm alternativas separadas — e reportar `E_total` nas duas
convenções. Se o sinal for estável, o achado ganha força. Se não for, some, e é melhor que
suma agora.

## 6. NOVO · MINOR-8 — o braço legado usa a fórmula de competência fora de escala

Há dois caminhos de ajuda no código, e eles aplicam a mesma fórmula em escalas diferentes.

Caminho Crowder (`comunicar`, l. 140–141), correto:

```python
dC = clip((15. + 3.*(5.*k.competencia - 5.*a.competencia))/100., 0., .30)
a.competencia = min(tar.dificuldade, a.competencia + dC/5.)
```

Caminho legado (`executar`, l. 258), preservado para compatibilidade:

```python
a.competencia = min(.98, a.competencia + (15 + 3*(k.competencia - a.competencia))/100)
```

Aqui as competências entram normalizadas (0–1) numa fórmula calibrada para 0–5, e o resultado
é somado sem dividir por 5. Para `k = 0,8` e `a = 0,4`: o caminho legado dá **+0,162**; o
caminho correto dá **+0,042**. Fator 3,9×.

Pior que a magnitude é o que isso faz com o **mecanismo**: na escala errada o termo constante
15 domina o termo `3·(C_p − C_r)`, que vale 1,2. O incremento vira praticamente **fixo**,
independente de quem ajudou. O mecanismo central de Crowder — aprender mais com colegas mais
competentes — está essencialmente desligado no braço legado. E o teto é `0,98` em vez da
dificuldade da subtarefa, então a competência pode ultrapassar o que a eq. (2) permite.

**Isto não é um defeito da correção** — a preservação é deliberada e é o que sustenta o
controle exato de identidade. O problema é de **interpretação da escada incremental**: os
degraus `C4_completo` e `C4_C1` carregam a versão fora de escala, e o degrau
`C4_C1_comunicacao` muda o protocolo **e** corrige a escala ao mesmo tempo. A atribuição
"o que o protocolo de comunicação mudou" está confundida com "o que a correção de escala
mudou". Basta declarar isso na leitura da tabela incremental; não exige recodificar nada.

## 7. Desvios declarados que continuam de pé

Ambos estão marcados `[DEC]` no parecer 19, o que é o tratamento correto. Ficam registrados
porque afetam o que o trabalho pode afirmar:

1. **Destinatário único em vez de difusão.** Em Crowder, o agente difunde o pedido a todos, e
   a eq. (2) soma ΔC sobre os `q` respondentes. Aqui há um destinatário por tentativa, o que
   limita o aprendizado por evento e altera a velocidade com que o hiato de competência fecha.
2. **TL não é a eq. (3).** Ver MAJOR-7.

## 8. O que o parecer 19 acerta e que vale preservar no texto final

Registro porque um parecer que só aponta problemas dá uma imagem falsa do que foi entregue:

- separa explicitamente os denominadores de `taxa_omissao` (oportunidades × tarefas executadas)
  e diz que a comparação com os 64% anteriores só vale com o denominador correspondente;
- declara que a fonte humana de ρ é transporte de construto, não calibração;
- recusa usar médias por porta como teste causal, e monta um contrafactual com o mesmo
  estado e os mesmos sorteios;
- diz que a ablação "sem assistência" não isola o portão quando Crowder está ligado, porque
  eliminar comunicação elimina as atualizações de confiança junto;
- reporta que 3 de 129 células de TR e 5 de 129 de `E_total` têm contraste positivo, em vez de
  esconder, e observa que os intervalos dessas células incluem zero;
- separa o controle estatístico de ambiente (SciPy 1.11.4) do efeito de modelo;
- fecha dizendo que fechamento de software e robustez interna não equivalem a validação
  empírica. É a frase certa.

---

## 9. Recomendação sobre o merge

Não bloquear o merge por MAJOR-7. O código está melhor do que estava, os controles são reais
e o legado permanece intacto. Mas **rodar o teste discriminante de TL antes de qualquer
redação final que cite a inversão de `E_total`** — porque é mais barato descobrir agora do que
retirar o achado depois de escrito.

Ordem sugerida: teste de TL → merge em `main` → V_obs/V_mod.
