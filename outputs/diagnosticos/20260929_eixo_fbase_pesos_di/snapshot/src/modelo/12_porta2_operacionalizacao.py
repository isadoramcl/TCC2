"""
12_porta2_operacionalizacao.py — Porta 2: regra do TCC1 x operacionalização do TCC2
=====================================================================================

A DIVERGÊNCIA
-------------
TCC1, §4.4.3, "Regra de Transição Lógica", Porta 2 — Hiato de competência:

    1  se ∆D > 0 então
    2       Muda estado para Espera_por_Suporte;
    3       Transmite Request(∆D) à rede;
    4       se ∃ agente k com a_k > 0 e τ_k > τ_min então
    5             ∆C ← [15 + 3(C_k − C)]/100;
    ...

Condição conceitual: **disponibilidade e confiança**. Nada sobre competência.

Implementação em `simulador.py`: disponibilidade, confiança **e**
`k.competencia > a.competencia`. O terceiro termo é acréscimo deste trabalho e
não estava declarado em lugar nenhum.

`[DEC]` Este script mede a diferença entre as duas operacionalizações, com
instâncias, sementes e demais parâmetros IDÊNTICOS ao experimento nominal.
Não escolhe entre elas: a escolha não pode ser feita por desempenho.

SAIDA
-----
  outputs/tables/modelo_12_porta2_comparacao.csv
  outputs/logs/modelo_12_porta2_operacionalizacao.log
"""

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
DIR = RAIZ / "outputs" / "tables" / "_b9_parciais"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"

METRICAS = ["taxa_falha_efetiva", "atraso_relativo", "E_total", "TL", "TU", "TR", "TW", "n_com_erro",
            "taxa_omissao", "retrabalho_sobre_plano",
            "divida_latente_sobre_plano", "S_UR_maximo"]
CONTADORES = ["p2_ajuda", "p2_bloqueio", "hiato_encontrado",
              "hiato_sem_colega_capaz", "hiato_sem_colega_livre",
              "hiato_colega_capaz_sem_confianca", "p1_omissao", "p3_analitica"]
_log = []


def log(m=""):
    print(m)
    _log.append(m)


def por_instancia(d, col):
    return d.groupby("arquivo")[col].mean().sort_index().values


def main():
    log("=" * 78)
    log("PORTA 2 — regra do TCC1 (B) x operacionalizacao do TCC2 (A)")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)
    log("\n  A = nominal implementado : disponivel + tau_k > tau_min + "
        "competencia_k > competencia")
    log("  B = fiel ao TCC1 §4.4.3  : disponivel + tau_k > tau_min")
    log("  Diferenca                : o filtro de competencia, ausente no TCC1")

    linhas = []
    for cen in ("centralizada", "adaptativa"):
        A = pd.read_csv(DIR / f"{cen}.csv")
        B = pd.read_csv(DIR / f"{cen}__sem_filtro_competencia.csv")
        assert set(zip(A.arquivo, A.semente)) == set(zip(B.arquivo, B.semente)), \
            "pareamento quebrado: instancias/sementes diferentes"
        log("\n" + "=" * 78)
        log(f"CENARIO {cen.upper()}   "
            f"({A['arquivo'].nunique()} instancias x {A['semente'].nunique()} "
            f"sementes, pareadas)")
        log("=" * 78)

        log(f"\n  Contadores da Porta 2 (media por execucao):")
        log(f"    {'contador':<36} {'A nominal':>11} {'B TCC1':>11} {'dif':>10}")
        for c in CONTADORES:
            if c not in A.columns:
                continue
            a, b = A[c].mean(), B[c].mean()
            log(f"    {c:<36} {a:>11.2f} {b:>11.2f} {b - a:>+10.2f}")
            linhas.append({"cenario": cen, "tipo": "contador", "grandeza": c,
                           "media_A_nominal": float(a), "media_B_tcc1": float(b),
                           "dif_absoluta": float(b - a),
                           "dif_relativa_pct": (float(100 * (b - a) / a)
                                                if a else np.nan)})

        log(f"\n  Metricas principais (unidade inferencial: instancia, n = "
            f"{A['arquivo'].nunique()}):")
        log(f"    {'metrica':<28} {'A nominal':>11} {'B TCC1':>11} {'dif':>10} "
            f"{'dif %':>8} {'p':>10} {'d':>7}")
        for m in METRICAS:
            x, y = por_instancia(A, m), por_instancia(B, m)
            dif = y - x
            if np.allclose(dif, 0):
                pv, dc = np.nan, np.nan
            else:
                pv = float(stats.wilcoxon(y, x)[1])
                sd = float(np.std(dif, ddof=1))
                dc = float(np.mean(dif) / sd) if sd > 0 else np.nan
            rel = 100 * np.mean(dif) / np.mean(x) if np.mean(x) else np.nan
            log(f"    {m:<28} {np.mean(x):>11.4f} {np.mean(y):>11.4f} "
                f"{np.mean(dif):>+10.4f} {rel:>+7.1f}% {pv:>10.2e} {dc:>7.2f}")
            linhas.append({"cenario": cen, "tipo": "metrica", "grandeza": m,
                           "media_A_nominal": float(np.mean(x)),
                           "media_B_tcc1": float(np.mean(y)),
                           "dif_absoluta": float(np.mean(dif)),
                           "dif_relativa_pct": float(rel), "p_valor": pv,
                           "d_cohen_pareado": dc,
                           "n_instancias": int(len(dif))})

    d = pd.DataFrame(linhas)
    d.to_csv(DIR_TABELAS / "modelo_12_porta2_comparacao.csv", index=False,
             encoding="utf-8")

    log("\n" + "=" * 78)
    log("MAGNITUDE DA DIVERGENCIA")
    log("=" * 78)
    met = d[d.tipo == "metrica"].copy()
    for cen in ("centralizada", "adaptativa"):
        sel = met[met.cenario == cen]
        maior = sel.reindex(sel["dif_relativa_pct"].abs().sort_values(
            ascending=False).index).iloc[0]
        n_signif = int((sel["p_valor"] < 0.05).sum())
        log(f"\n  {cen}: {n_signif} de {len(sel)} metricas com p < 0,05; "
            f"maior efeito relativo em '{maior.grandeza}' "
            f"({maior.dif_relativa_pct:+.1f}%)")
    log("")
    log("  `[DEC]` Criterio de materialidade declarado ANTES de olhar o")
    log("  resultado: a divergencia e MATERIAL se alterar em mais de 5% alguma")
    log("  metrica publicada nos resultados, ou se inverter algum sinal. Os 5%")
    log("  vem da menor diferenca entre politicas que o trabalho reporta como")
    log("  achado (E_total, +13,3%): abaixo de metade disso a escolha de")
    log("  operacionalizacao nao muda nenhuma conclusao.")
    material = met[(met["dif_relativa_pct"].abs() > 5.0) & (met["p_valor"] < 0.05)]
    if len(material):
        log(f"\n  MATERIAL. {len(material)} metrica(s) acima do criterio:")
        for r in material.itertuples():
            log(f"    {r.cenario:<14} {r.grandeza:<28} {r.dif_relativa_pct:>+8.1f}%"
                f"   p = {r.p_valor:.2e}")
    else:
        log("\n  NAO MATERIAL: nenhuma metrica publicada muda mais de 5% com")
        log("  significancia. A divergencia e registrada e a harmonizacao fica")
        log("  para a proxima versao.")

    (DIR_LOGS / "modelo_12_porta2_operacionalizacao.log").write_text(
        "\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
