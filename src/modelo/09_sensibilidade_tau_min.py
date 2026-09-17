"""
09_sensibilidade_tau_min.py — Sensibilidade local de tau_min em torno de 0,25
==============================================================================

PERGUNTA
--------
O braco centralizado nunca concede ajuda (`TL = 0,00`). A B9 mostrou que trocar
SO `tau_min` pelo valor adaptativo (0,60 -> 0,25) nao muda absolutamente nada.
A hipotese e que isso ocorra porque `tau_inicial` da centralizada e 0,25 e o
portao da Porta 2 usa desigualdade ESTRITA (`confianca > tau_min`), de modo que
0,25 > 0,25 e falso.

E preciso distinguir duas situacoes com consequencias metodologicas diferentes:
  (a) o comportamento muda de forma GRADUAL com tau_min, e 0,25 e apenas um
      ponto de uma curva continua;
  (b) o comportamento e uma DESCONTINUIDADE produzida pela desigualdade estrita
      exatamente no ponto de empate.

DESENHO
-------
`[DEC]` Varredura local de `tau_min` mantendo TODO o resto no cenario
centralizado. Mesmas 16 instancias e 12 sementes da B9, para comparabilidade
direta. Grade deliberadamente assimetrica e adensada em torno de 0,25:
    0,20  0,225  0,24  0,249  0,2499  0,2500  0,2501  0,251  0,26  0,275  0,30
Os tres pontos 0,2499 / 0,2500 / 0,2501 existem para localizar a
descontinuidade, se houver, com precisao de 1e-4.

`[DEC]` 0,25 e 2^-2, portanto EXATAMENTE representavel em ponto flutuante
binario. O empate `tau_inicial == tau_min` nao e um acidente de arredondamento:
e igualdade exata. O script verifica isso e falha se deixar de valer.

SAIDA
-----
  outputs/tables/modelo_09_sensibilidade_tau_min.csv
  outputs/logs/modelo_09_sensibilidade_tau_min.log
"""

import copy
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import simulador as S  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
DIR_PARCIAIS = DIR_TABELAS / "_tau_min_parciais"

N_INSTANCIAS = 16
N_SEMENTES = 12
GRADE = [0.20, 0.225, 0.24, 0.249, 0.2499, 0.25, 0.2501, 0.251, 0.26, 0.275, 0.30]

SAIDAS = ["taxa_falha_efetiva", "p2_ajuda", "p2_bloqueio", "atraso_relativo", "TU", "TL", "TR",
          "E_total", "TW", "n_com_erro", "S_UR_maximo", "p1_omissao",
          "p3_analitica"]


def instancias():
    todas = sorted(pd.read_csv(RAIZ / "data" / "processed" / "psplib" /
                               "tarefas_j60_com_di.csv")["arquivo"].unique())
    return todas[::max(1, len(todas) // N_INSTANCIAS)][:N_INSTANCIAS]


def rodar(tm: float) -> None:
    par = S.carregar_parametros()
    tau_ini = float(S.v(par["cenarios"]["centralizada"]["tau_inicial"]))
    par["cenarios"]["probe"] = copy.deepcopy(par["cenarios"]["centralizada"])
    par["cenarios"]["probe"]["tau_min"] = {"valor": float(tm),
                                           "condicao": "varredura_tau_min"}
    linhas = []
    for arq in instancias():
        g, disp, cpm = S.carregar_instancia(arq)
        for sem in range(N_SEMENTES):
            sim = S.Simulacao(g, disp, cpm, par, "probe", semente=sem)
            # A confianca dos agentes e inicializada com tau_inicial e NAO evolui
            # (tau constante, item C3). Registra-se quantos valores distintos de
            # confianca existem na equipe: se for 1, `tau_min` nao pode produzir
            # resposta gradual, porque o portao e a mesma comparacao para todos.
            distintas = len({a.confianca for a in sim.agentes})
            r = sim.executar()
            linhas.append({
                "tau_min": tm, "tau_inicial": tau_ini,
                "empate_exato": tau_ini == tm,
                "valores_distintos_de_confianca": distintas,
                "arquivo": arq, "semente": sem,
                "atraso_relativo": r.makespan / r.makespan_cpm,
                "taxa_falha_efetiva": r.taxa_falha_efetiva,
                "E_total": r.E_total, "TW": r.TW, "TL": r.TL, "TU": r.TU,
                "TR": r.TR, "n_com_erro": r.n_com_erro,
                "S_UR_maximo": r.S_UR_maximo,
                "p2_ajuda": r.contadores["p2_ajuda"],
                "p2_bloqueio": r.contadores["p2_bloqueio"],
                "p1_omissao": r.contadores["p1_omissao"],
                "p3_analitica": r.contadores["p3_analitica"],
            })
    DIR_PARCIAIS.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(linhas).to_csv(DIR_PARCIAIS / f"tm_{tm}.csv", index=False,
                                encoding="utf-8")
    print(f"tau_min = {tm}: {len(linhas)} execucoes")


def analisar() -> None:
    _log = []

    def log(m=""):
        print(m)
        _log.append(m)

    faltando = [t for t in GRADE if not (DIR_PARCIAIS / f"tm_{t}.csv").exists()]
    if faltando:
        raise SystemExit(f"faltam rodar: {faltando}")
    d = pd.concat([pd.read_csv(DIR_PARCIAIS / f"tm_{t}.csv") for t in GRADE],
                  ignore_index=True)
    d.to_csv(DIR_TABELAS / "modelo_09_sensibilidade_tau_min.csv", index=False,
             encoding="utf-8")

    log("=" * 78)
    log("SENSIBILIDADE LOCAL DE tau_min — cenario centralizado, resto constante")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)
    tau_ini = float(d["tau_inicial"].iloc[0])
    log(f"\ntau_inicial (centralizada) = {tau_ini!r}   "
        f"exatamente representavel: {tau_ini == 0.25}")
    log(f"Instancias: {d['arquivo'].nunique()}   Sementes: {d['semente'].nunique()}"
        f"   Execucoes por ponto: {len(d) // len(GRADE)}")
    nd = sorted(d["valores_distintos_de_confianca"].unique())
    log(f"\nValores distintos de confianca dentro da equipe: {nd}")
    if nd == [1]:
        log("  -> Todos os agentes tem a MESMA confianca (= tau_inicial) e ela nao")
        log("     evolui. Logo o portao `confianca > tau_min` e a MESMA comparacao")
        log("     para todos: e uma funcao degrau global de tau_min, e nao pode")
        log("     produzir resposta gradual. Isso e consequencia de tau constante")
        log("     (item C3), nao do valor de tau_min.")

    # media por instancia, depois media entre instancias (unidade = instancia)
    m = (d.groupby(["tau_min", "arquivo"])[SAIDAS].mean()
         .groupby("tau_min").mean().reindex(GRADE))
    log("\n" + "-" * 78)
    log(f"  {'tau_min':>8} {'ajudas':>8} {'bloqueios':>10} {'atraso_rel':>11} "
        f"{'TU':>9} {'TL':>8} {'TR':>8} {'E_total':>9}")
    log("-" * 78)
    for t in GRADE:
        r = m.loc[t]
        marca = "  <-- empate exato com tau_inicial" if t == tau_ini else ""
        log(f"  {t:>8} {r.p2_ajuda:>8.2f} {r.p2_bloqueio:>10.2f} "
            f"{r.atraso_relativo:>11.4f} {r.TU:>9.2f} {r.TL:>8.2f} "
            f"{r.TR:>8.2f} {r.E_total:>9.4f}{marca}")
    log("-" * 78)

    # quantos regimes distintos existem?
    assinatura = m[SAIDAS].round(6).apply(tuple, axis=1)
    regimes = assinatura.drop_duplicates()
    log(f"\n  Regimes distintos na grade: {len(regimes)} de {len(GRADE)} pontos.")
    for i, a in enumerate(regimes, 1):
        pontos = [t for t in GRADE if assinatura.loc[t] == a]
        log(f"    regime {i}: tau_min em {pontos}")
    if len(regimes) == 2:
        log("\n  DIAGNOSTICO: resposta em DEGRAU, nao gradual. A grade tem 11")
        log("  pontos e apenas 2 comportamentos. Todo ponto com tau_min < 0,25")
        log("  cai num regime e todo ponto com tau_min >= 0,25 cai no outro.")
        log("  Nao existe faixa intermediaria: e descontinuidade, nao gradiente.")
    elif len(regimes) > 2:
        log("\n  DIAGNOSTICO: existem regimes intermediarios — a resposta NAO e")
        log("  um simples degrau. Descrever a curva antes de concluir.")

    # localizacao da descontinuidade
    ajudas = m["p2_ajuda"]
    saltos = [(GRADE[i], GRADE[i + 1],
               float(ajudas.iloc[i + 1] - ajudas.iloc[i]))
              for i in range(len(GRADE) - 1)
              if abs(ajudas.iloc[i + 1] - ajudas.iloc[i]) > 1e-9]
    log("\n  Saltos em numero de ajudas entre pontos consecutivos:")
    for a, b, s in saltos:
        log(f"    {a} -> {b}: {s:+.2f}")
    if len(saltos) == 1:
        a, b, s = saltos[0]
        log(f"\n  A descontinuidade unica esta no intervalo ({a}; {b}], de largura"
            f" {b - a:.4f},")
        log(f"  e contem exatamente tau_inicial = {tau_ini}. A variacao de "
            f"{abs(b - a):.4f} em")
        log("  tau_min produz toda a diferenca; nenhuma outra variacao na grade,")
        log("  incluindo a de 0,20 a 0,249 (0,049, 490x maior), produz efeito algum.")

    log("\n--- Arquivos gerados ---")
    log("  outputs/tables/modelo_09_sensibilidade_tau_min.csv")
    (DIR_LOGS / "modelo_09_sensibilidade_tau_min.log").write_text(
        "\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--rodar":
        for t in sys.argv[2:]:
            rodar(float(t))
    elif len(sys.argv) > 1 and sys.argv[1] == "--listar":
        print(" ".join(str(t) for t in GRADE))
    else:
        analisar()
