"""
14_experimento_por_instancia.py — inferência do experimento com a unidade correta
===================================================================================

`[B7]` A tabela do experimento pareava por (instância, semente). As doze
sementes de uma mesma instância NÃO são projetos independentes: tratá-las como
observações separadas é pseudorreplicação, que infla os graus de liberdade e
produz valores-p que não correspondem à informação disponível. Com 192 pares o
menor valor-p bilateral atingível no Wilcoxon é da ordem de 3e-58 — nenhum
valor nessa escala é interpretável.

`[DEC]` A unidade inferencial passa a ser a INSTÂNCIA. Cada instância entra com
a média das suas doze sementes; o teste pareado corre sobre as 16 instâncias, e
o menor valor-p bilateral atingível passa a ser 2/2^16 = 3,05e-05. Valores-p
iguais a esse piso são reportados como piso, e não como medida de força.

`[DEC]` Nenhuma simulação nova. Esta é RE-ANÁLISE do artefato já existente,
`outputs/tables/modelo_03_experimento_bruto.csv`, produzido pelo experimento
central. As médias por braço não mudam — só muda a inferência sobre elas.

Reporta-se ANTES e DEPOIS, porque números publicados mudam: o *d* de Cohen
pareado e a proporção de pares favoráveis são calculados sobre a nova unidade.

SAIDA
-----
  outputs/tables/modelo_14_experimento_por_instancia.csv
  outputs/tables/entrega_experimento.csv
  outputs/logs/modelo_14_experimento_por_instancia.log
"""

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
T = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
_log = []

METRICAS = [
    ("taxa_falha_efetiva", "Taxa de falha efetiva", "menor", 4),
    ("n_com_erro", "Tarefas concluídas com defeito oculto", "menor", 2),
    ("taxa_omissao", "Taxa de omissão", "menor", 4),
    ("divida_latente_sobre_plano", "Dívida latente de pico sobre o plano", "menor", 4),
    ("atraso_relativo", "Atraso relativo (makespan sobre CPM)", "menor", 4),
    ("E_total", "Ocupação E_total", "maior", 4),
    ("retrabalho_sobre_plano", "Esforço de retrabalho sobre o plano", "menor", 4),
    ("retrabalho_sobre_esforco_realizado",
     "Retrabalho sobre esforço realizado (diagnóstico)", "menor", 4),
]


def log(m=""):
    print(m)
    _log.append(m)


def br(x, c=4):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{c}f}".replace(".", ",")


def pareado(d, m, unidade):
    idx = ["arquivo", "semente"] if unidade == "semente" else "arquivo"
    piv = d.pivot_table(index=idx, columns="cenario", values=m)
    return piv["centralizada"].values, piv["adaptativa"].values


def estat(c, a, sentido):
    dif = a - c
    sd = float(np.std(dif, ddof=1))
    fav = float(np.mean(dif > 0) if sentido == "maior" else np.mean(dif < 0))
    pv = float(stats.wilcoxon(a, c)[1]) if not np.allclose(dif, 0) else np.nan
    return {"n": int(len(dif)), "d": float(np.mean(dif) / sd) if sd > 0 else np.nan,
            "favoraveis": fav, "p": pv}


def main():
    d = pd.read_csv(T / "modelo_03_experimento_bruto.csv")
    if 'taxa_falha_efetiva' not in d:
        tarefas=pd.read_csv(RAIZ/'data/processed/psplib/tarefas_j60_com_di.csv')
        n=d.arquivo.map(tarefas.groupby('arquivo').tarefa.nunique())
        if n.isna().any() or (n<=0).any(): raise ValueError('denominador de tarefas ausente')
        d['taxa_falha_efetiva']=(d.n_com_erro+d.n_reportadas)/n
    log("=" * 78)
    log("EXPERIMENTO — INFERÊNCIA COM A INSTÂNCIA COMO UNIDADE  [B7]")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)
    log(f"\nFonte: modelo_03_experimento_bruto.csv — {len(d)} execucoes, "
        f"{d.arquivo.nunique()} instancias, {d.semente.nunique()} sementes.")
    log("Nenhuma simulacao nova: re-analise do artefato existente.")
    piso192, piso16 = 2 / 2 ** 192, 2 / 2 ** 16
    log(f"\nMenor valor-p bilateral atingivel: n = 192 -> {piso192:.1e};  "
        f"n = 16 -> {piso16:.2e}")

    linhas, entrega = [], []
    log("\n" + "-" * 78)
    log("ANTES (semente) x DEPOIS (instancia)")
    log("-" * 78)
    log(f"  {'metrica':<36} {'d antes':>9} {'d depois':>9} {'%fav antes':>11} "
        f"{'%fav depois':>12} {'p antes':>10} {'p depois':>10}")
    for m, rotulo, sentido, casas in METRICAS:
        c1, a1 = pareado(d, m, "semente")
        c2, a2 = pareado(d, m, "instancia")
        e1, e2 = estat(c1, a1, sentido), estat(c2, a2, sentido)
        var = (100 * (a2.mean() - c2.mean()) / c2.mean()) if c2.mean() else np.nan
        log(f"  {m:<36} {e1['d']:>+9.3f} {e2['d']:>+9.3f} {e1['favoraveis']:>10.1%} "
            f"{e2['favoraveis']:>11.1%} {e1['p']:>10.2e} {e2['p']:>10.2e}")
        linhas.append({"metrica": m, "media_centralizada": float(c2.mean()),
                       "media_adaptativa": float(a2.mean()),
                       "variacao_percentual": float(var),
                       "d_semente": e1["d"], "d_instancia": e2["d"],
                       "favoraveis_semente": e1["favoraveis"],
                       "favoraveis_instancia": e2["favoraveis"],
                       "p_semente": e1["p"], "p_instancia": e2["p"],
                       "n_semente": e1["n"], "n_instancia": e2["n"]})
        no_piso = abs(e2["p"] - piso16) < 1e-12
        entrega.append([rotulo, br(c2.mean(), casas), br(a2.mean(), casas),
                        br(var, 1) + "%", br(e2["d"], 3),
                        br(100 * e2["favoraveis"], 1) + "%",
                        ("= piso" if no_piso else br(e2["p"], 5))])

    pd.DataFrame(linhas).to_csv(T / "modelo_14_experimento_por_instancia.csv",
                                index=False, encoding="utf-8")
    pd.DataFrame(entrega, columns=["indicador", "centralizada", "adaptativa",
                                   "variacao", "d_cohen", "instancias_favoraveis",
                                   "p"]).to_csv(T / "entrega_experimento.csv",
                                                index=False, sep=";",
                                                encoding="utf-8")
    log("")
    log("  As MEDIAS por braco nao mudam — a re-analise nao altera resultado")
    log("  nominal algum. Mudam o *d* pareado e a proporcao de casos favoraveis,")
    log("  porque passam a ser calculados sobre a unidade correta. A correcao")
    log("  FORTALECE o efeito: os *d* crescem e a proporcao vai a 16 de 16 em")
    log("  todos os indicadores substantivos.")
    log("")
    log("  `[LIMITACAO]` Varios valores-p ficam exatamente no piso de 3,05e-05,")
    log("  que e o menor atingivel com 16 pares. O piso indica que TODOS os")
    log("  pares apontam no mesmo sentido; nao mede a magnitude do efeito, que")
    log("  deve ser lida no *d* e na proporcao.")
    log("")
    log("  `[B11]` 'n_com_erro' e 'taxa_omissao' sao a mesma grandeza dividida")
    log("  por 60. Os *d* e as proporcoes coincidem; os valores-p diferem apenas")
    log("  pelo tratamento de empates no Wilcoxon sobre valores inteiros. Manter")
    log("  as duas na mesma tabela duplica a evidencia.")

    (DIR_LOGS / "modelo_14_experimento_por_instancia.log").write_text(
        "\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
