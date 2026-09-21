# 73 — C4 fechado: sensibilidade dinâmica da seleção heurística à pressão

**Data:** 21/09/2026 · **Executado por:** Claude (revisor), sem auditoria independente.
**Completa** o parecer 57, que fez a versão local e deixou a dinâmica pendente.
Script: `research/validacao/c4_dinamico.py` · Evidência: `outputs/diagnosticos/20260921_c4_dinamico/`

## O que foi feito

Trajetórias completas com a pressão **fixada** em 0,30 (mínimo do modelo) e em
1,00 (máximo), sem nenhuma outra mudança no modelo nominal. Malha `tau_sat`
{0,7; 1; 1,4} × `s_transicao` {0,01; 0,25; 0,6}, 16 instâncias do nominal,
sementes 0–3, dois arranjos: 2 304 execuções, teto de 16×CPM. Mede-se a fração de
tarefas executadas pela Porta 1 em cada extremo e a razão entre elas.

## Resultado — ponto nominal (`tau_sat = 1`, `s = 0,25`)

| arranjo | fração P1 com P = 0,30 | com P = 1,00 | razão | razão local (parecer 57) |
|---|---:|---:|---:|---:|
| adaptativo | 0,274 | 0,807 | **2,94** | 1,57 |
| centralizado | 0,373 | 0,822 | **2,20** | 1,39 |

Na malha inteira, com `s` ≥ 0,25 a razão fica entre 1,38 e 6,49. Com `s = 0,01`
fica entre 9 e 24, porque a transição vira degrau; nesse canto, no centralizado,
parte das execuções não termina no teto (o item 7 do README). Tabela completa em
`c4_dinamico_resumo.csv`.

**A versão local subestimava o efeito.** Com a trajetória completa, a pressão alta
drena a bateria, e bateria baixa aumenta o esforço percebido — o laço amplifica.

## Comparação com Rieskamp & Hoffrage (2008) — só descritiva

Estudo 2: 19,4% → 44,4% de participantes não compensatórios, razão ≈ 2,3. No ponto
nominal o modelo dá 2,2 a 2,9: **mesma ordem de grandeza**. Não é validação:

- Rieskamp conta **participante classificado**; o modelo conta **tarefa executada**.
- O contraste de Rieskamp é pressão contra **ausência** de pressão; o modelo nunca
  desce de 0,30.
- O Estudo 1 do mesmo artigo não achou o efeito.
- Nenhum parâmetro foi ajustado para chegar perto de 2,3.

O que se pode escrever: a sensibilidade da seleção heurística à pressão no modelo
é compatível em magnitude com o deslocamento de estratégia observado por Rieskamp
e Hoffrage (2008), com as ressalvas de unidade acima.

## Controle

O código usado é o nominal com opções default. Antes da execução, a cópia do
código reproduziu o nominal arquivado bit a bit (384 execuções, 45 campos).
