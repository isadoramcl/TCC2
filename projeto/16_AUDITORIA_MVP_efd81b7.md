# Auditoria do MVP — branch `codex/resposta-revisao-cientifica`, commit `efd81b7`

**Revisor:** Claude · 16/09/2026 · Base: `origin/main` = `dc8721f` (merge da autora, concluído)
Verificado por leitura de `src/modelo/simulador_mvp.py`, `research/test_mvp.py` e do diff da branch.

---

## Veredito

**O C4 foi implementado pela metade, e é a metade errada.**

O MVP entrega o atalho temporal da Porta 1 e não entrega o excesso de risco. Com isso a omissão
ficou **25% mais rápida com exatamente a mesma probabilidade de falha**. O teste local do revisor
(`projeto/15`, variante V1) mediu essa configuração: makespan −16%, TW −22%, retrabalho −15%.
Tudo melhora. A Porta 1 deixou de ser dominada — e passou a **dominar** a Porta 3 no cronograma,
pagando só bateria.

O arquétipo de Soluções Sintomáticas não foi restaurado. Ele foi invertido.

Isso também explica o resultado relatado pelo próprio Codex — *"o retrabalho pago mostrou
fragilidade"*. Com atalho puro, o retrabalho cai. É o comportamento esperado da V1.

---

## O que está correto e deve ser preservado

| item | evidência |
|---|---|
| Atalho temporal da P1 | `fator=o.fator_omissao if heu else 1.` com `fator_omissao=.75`; teste `test_omissao_reduz_tempo_imediato` confirma makespan 8→4 com fator 0,5 |
| C1 — retrabalho ocupa agente **e recurso** | fila FIFO de reparos, `a.tarefa_atual=-2`, demanda do reparo somada a `uso`; teste confirma `uso ≤ capacidade` |
| Invariante de conservação em tempo de execução | `erro = |gerado − TR − pendente| > 1e-8` → violação registrada. Boa engenharia: é o tipo de checagem que teria pego o `S_UR ≡ 0` antes |
| Horizonte automático | duplicação até teto, com contador `extensoes_horizonte` |
| Separação dos canais de τ | `multiplicadores()` sobrescrito com `tau_rede`, e `tau_portao` separado no filtro da Porta 2 |
| Legado intacto | `simulador.py` não aparece no diff; `efd81b7` não é ancestral de `origin/main` |
| Qualidade dos testes | casos degenerados com resposta analítica conhecida (`tau_sat=±100`, `F_ancora∈{0,1}`, competência 0,98). É a forma certa de testar simulador |

---

## O que falta, em ordem de consequência

### 1. A metade de qualidade do C4 — CRÍTICO

```python
falhou = self.rng.random() < float(np.clip(self.F_base(tar.nivel)+re*(1-mc),0,1))
```

Idêntico ao legado. Sem `ρ_omissão`, sem `q`, sem excesso algum para a P1.
E `mc,mr` continuam sendo calculados **antes** do sorteio de `heu` — o CRITICAL-6 persiste.

**Nenhum teste afirma `p_falha_P1 > p_falha_P3`**, porque não é verdade.

Implementar conforme acordado:

```
q        = max(0, 2*p_heu - 1)
p_fail_P1 = 1 - (1-p0)*(1 - rho_omissao*q)
p_fail_P3 = p0
```

com `rho_omissao` `[ABERTO]`, valor inicial ≈ 0,29 derivado do excesso relativo observado
em experimento de speed–accuracy (ver nota sobre a derivação). Lembrar que `q` é função de
`p_heu`, que seleciona a P1 — logo `E[q | P1] > E[q]` e a sensibilidade de `ρ` é amplificada.

### 2. A lei de confiança não é a do Crowder

Implementadas: `media_eventos` (média móvel exponencial) e `saldo_eventos` (±constante).
Nenhuma das duas é a Eq. (4), que foi verificada na fonte primária:

```
τ(t+1) = τ(t) + τ(t)·ΔC        se comunicação bem-sucedida
       = τ(t) − 0,05           se malsucedida            (escala [0,5])
```

Na escala [0,1] o decremento é 0,01, o incremento é multiplicativo e **atrelado a `ΔC`**,
com teto `ΔC ≤ 0,30`. A decisão já está tomada e não depende mais de orientação externa.

### 3. Bloqueio pelo limiar está sendo contado como recusa

```python
if capazes: eventos_tau.append((a,False))     # no ramo de bloqueio
```

Três divergências da fonte numa linha:

- **bloqueio ≠ recusa.** No Crowder a solicitação é enviada e a falha é o colega recusar ou estar
  indisponível. Aqui o portão filtra antes do pedido. A B9 mediu ~81 bloqueios por execução no
  braço centralizado: com `decremento_recusa = 0,01`, τ chega a zero em poucos períodos.
- **atualiza o solicitante, não o respondente.** No Crowder quem tem a confiança alterada é o
  agente que responde (ou não responde), não quem pede.
- **no sucesso credita os dois** (`(a,True),(k,True)`); na fonte sobe a do respondente.

Separar `N_req`, `N_fail` e `N_blocked`, e só `N_fail` move τ.

### 4. Não existe controle de compatibilidade — o teste mais importante que falta

O laço `executar()` foi **reimplementado**, não estendido método a método. Não há nenhum teste
afirmando que `SimulacaoMVP` com opções neutras — `fator_omissao=1`, `retrabalho_fila=False`,
`lei_confianca='constante'`, `horizonte_automatico=False`, `politica_porta2='nominal'` — reproduz
`Simulacao` **bit a bit** para as mesmas sementes.

Sem isso, qualquer número antes/depois pode carregar deriva silenciosa da reimplementação, e não
há como saber quanto do efeito medido é a alternativa e quanto é o laço novo. A ordem de iteração
de agentes confere com o legado (`sorted(..., key=-competencia)`), então a compatibilidade é
plausível — e por isso mesmo testável.

É literalmente a lição registrada em `00_INSTRUCOES`: verificador não testado dá falsa confiança.

### 5. Simplificação declarada que interage com o arquétipo

`[DEC] Reparos ... não geram novos defeitos.` Está declarado, o que é correto. Mas retrabalho que
não pode falhar remove um laço de reforço do arquétipo. Registrar como limitação no documento, não
só no cabeçalho do módulo.

---

## O que NÃO concluir a partir destes resultados

Os 17.920 execuções mediram um modelo com **atalho sem custo de qualidade**. O contraste de
governança relatado — direção mantida em atraso, omissões e dívida oculta — é o contraste dessa
versão, não do MVP pretendido. O teste local sugere que, com a metade de qualidade implementada,
os contrastes de omissão e retrabalho **crescem cerca de 3× e 4,5×**.

Portanto: não usar `11_MVP_RESULTADOS_2026-09-16.md` como resultado do MVP. Reexecutar depois
dos itens 1 a 4.

---

## Ordem recomendada

1. Controle de compatibilidade bit a bit (item 4). Antes de tudo, porque valida todo o resto.
2. Excesso de risco da P1 (item 1), com teste contrafactual: mesma tarefa e mesmo estado,
   forçar P1 e P3, verificar `dur_P1 ≤ dur_P3` e `p_fail_P1 ≥ p_fail_P3` sob sobrecarga positiva.
   **Com controle negativo:** com `fator_omissao=1` e `rho_omissao=0` o teste deve FALHAR em
   detectar diferença.
3. Lei de Crowder e os três contadores (itens 2 e 3).
4. Só então reexecutar experimento, robustez e canais.
