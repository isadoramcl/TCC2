"""
03_experimento_cenarios.py — Experimento central: governança centralizada × adaptativa
========================================================================================

`[TCC1]` É o experimento previsto na Tabela 5.1 do TCC I: dois arranjos de
governança submetidos às MESMAS condições externas de pressão e dificuldade
técnica, variando apenas os parâmetros organizacionais.

DESENHO
-------
`[DEC]` **Pareado.** Cada par de execuções usa a mesma instância e a mesma
semente nos dois cenários. Assim a variação devida à instância e ao sorteio é
comum aos dois braços e cancela na diferença, o que eleva substancialmente a
potência em relação a um desenho independente de mesmo tamanho.

`[DEC]` Teste de Wilcoxon para amostras pareadas, e não teste t. As saídas do
modelo (dívida técnica, contagem de erros) são assimétricas e limitadas
inferiormente por zero; o Wilcoxon não pressupõe normalidade.

`[DEC]` Tamanho de efeito por **d de Cohen pareado** e pela **proporção de pares
em que o cenário adaptativo supera o centralizado**. Reportar apenas o valor-p
seria insuficiente: com pareamento e centenas de pares, diferenças irrelevantes
tornam-se significativas.

SAIDA
-----
  outputs/tables/modelo_03_experimento_bruto.csv
  outputs/tables/modelo_03_experimento_resumo.csv
  outputs/logs/modelo_03_experimento.log
"""

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import simulador as S  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
_log: list[str] = []

N_INSTANCIAS = int(sys.argv[1]) if len(sys.argv) > 1 else 24
N_SEMENTES = int(sys.argv[2]) if len(sys.argv) > 2 else 20


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def main() -> None:
    log("=" * 78)
    log("EXPERIMENTO — GOVERNANCA CENTRALIZADA x ADAPTATIVA")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    par = S.carregar_parametros()
    todas = sorted(pd.read_csv(RAIZ / "data" / "processed" / "psplib" /
                               "tarefas_j60_com_di.csv")["arquivo"].unique())
    passo = max(1, len(todas) // N_INSTANCIAS)
    instancias = todas[::passo][:N_INSTANCIAS]

    log(f"\nInstancias : {len(instancias)}")
    log(f"Sementes   : {N_SEMENTES}")
    log(f"Execucoes  : {len(instancias) * N_SEMENTES * 2} (pareadas)")
    log(f"\nParametros organizacionais que variam entre cenarios:")
    for k in ("tau_inicial", "tau_min", "p_reporte", "p_deteccao"):
        c = S.v(par["cenarios"]["centralizada"][k])
        a = S.v(par["cenarios"]["adaptativa"][k])
        log(f"  {k:<14} centralizada={c:<6} adaptativa={a}")
    log("  P(t) e D_i sao IDENTICOS entre cenarios — controle experimental")

    registros = []
    for arq in instancias:
        g, disp, cpm = S.carregar_instancia(arq)
        for sem in range(N_SEMENTES):
            for cen in ("centralizada", "adaptativa"):
                r = S.Simulacao(g, disp, cpm, par, cen, semente=sem).executar()
                registros.append({
                    "arquivo": arq, "semente": sem, "cenario": cen,
                    "concluiu": r.concluiu, "makespan": r.makespan,
                    "makespan_cpm": r.makespan_cpm,
                    "atraso_relativo": r.makespan / r.makespan_cpm,
                    "E_total": r.E_total, "S_UR_maximo": r.S_UR_maximo,
                    "n_com_erro": r.n_com_erro, "n_reportadas": r.n_reportadas,
                    "taxa_omissao": r.taxa_omissao,
                    "E_plano": r.E_plano,
                    "retrabalho_sobre_plano": r.retrabalho_sobre_plano,
                    "divida_latente_sobre_plano": r.divida_latente_sobre_plano,
                    "retrabalho_sobre_esforco_realizado":
                        r.retrabalho_sobre_esforco_realizado,
                    "TW": r.TW, "TL": r.TL, "TU": r.TU, "TR": r.TR,
                })

    d = pd.DataFrame(registros)
    d.to_csv(DIR_TABELAS / "modelo_03_experimento_bruto.csv", index=False, encoding="utf-8")

    nao_concluiu = int((~d["concluiu"]).sum())
    log(f"\n  Execucoes que nao concluiram no horizonte: {nao_concluiu} de {len(d)}")

    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("COMPARACAO PAREADA")
    log("=" * 78)

    metricas = [
        ("E_total", "maior e melhor"),
        ("S_UR_maximo", "menor e melhor"),
        ("n_com_erro", "menor e melhor"),
        ("atraso_relativo", "menor e melhor"),
        ("taxa_omissao", "menor e melhor"),
        ("retrabalho_sobre_plano", "menor e melhor"),
        ("divida_latente_sobre_plano", "menor e melhor"),
        ("retrabalho_sobre_esforco_realizado", "menor e melhor"),
        ("TR", "menor e melhor"),
        ("TU", "menor e melhor"),
    ]

    pivo = d.pivot_table(index=["arquivo", "semente"], columns="cenario",
                         values=[m for m, _ in metricas])
    resumo = []
    log(f"\n  {'metrica':<26} {'central.':>10} {'adapt.':>10} {'dif %':>9} "
        f"{'p (Wilcoxon)':>13} {'d Cohen':>9} {'% pares':>9}")
    for m, sentido in metricas:
        c = pivo[(m, "centralizada")].values
        a = pivo[(m, "adaptativa")].values
        dif = a - c
        if np.allclose(dif, 0):
            log(f"  {m:<26} {c.mean():>10.4f} {a.mean():>10.4f}  (sem variacao)")
            continue
        est, pv = stats.wilcoxon(a, c)
        cohen = float(np.mean(dif) / np.std(dif, ddof=1)) if np.std(dif, ddof=1) > 0 else np.nan
        melhor = (dif > 0) if "maior" in sentido else (dif < 0)
        prop = float(np.mean(melhor))
        variacao = 100 * (a.mean() - c.mean()) / c.mean() if c.mean() != 0 else np.nan
        log(f"  {m:<26} {c.mean():>10.4f} {a.mean():>10.4f} {variacao:>8.1f}% "
            f"{pv:>13.2e} {cohen:>9.3f} {prop:>8.1%}")
        resumo.append({
            "metrica": m, "sentido": sentido,
            "media_centralizada": round(float(c.mean()), 6),
            "media_adaptativa": round(float(a.mean()), 6),
            "variacao_percentual": round(float(variacao), 4),
            "wilcoxon_estatistica": float(est), "p_valor": float(pv),
            "d_cohen_pareado": round(cohen, 4),
            "proporcao_pares_favoraveis_ao_adaptativo": round(prop, 4),
            "n_pares": int(len(dif)),
        })

    pd.DataFrame(resumo).to_csv(DIR_TABELAS / "modelo_03_experimento_resumo.csv",
                                index=False, encoding="utf-8")

    log("")
    log("  `[ACHADO 6]` 'retrabalho_sobre_esforco_realizado' e reportada apenas")
    log("  como DIAGNOSTICO. Ela divide pelo esforco realizado, que inclui o")
    log("  tempo ocioso TU; o braco centralizado infla o proprio denominador e")
    log("  parece melhor nessa razao enquanto seu retrabalho ABSOLUTO (TR) e")
    log("  maior. A medida de dano e 'retrabalho_sobre_plano', cuja base")
    log("  (E_plano) e propriedade da instancia e identica nos dois bracos.")
    log("")
    log("\n  Leitura: 'd Cohen' e o tamanho do efeito na diferenca pareada;")
    log("  '% pares' e a fracao de pares em que o cenario adaptativo foi melhor.")
    log("  Com centenas de pares, o valor-p sozinho nao distingue diferenca")
    log("  relevante de diferenca detectavel.")

    log("\n--- Arquivos gerados ---")
    log(f"  outputs/tables/modelo_03_experimento_bruto.csv ({len(d)} linhas)")
    log(f"  outputs/tables/modelo_03_experimento_resumo.csv ({len(resumo)} linhas)")
    log("\n" + "=" * 78)
    log("RESULTADO: CONCLUIDO")
    log("=" * 78)
    (DIR_LOGS / "modelo_03_experimento.log").write_text("\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
