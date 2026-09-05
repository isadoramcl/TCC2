"""
03_transferencia_ordinal.py — Transferencia ordinal de risco NASA -> J60
=========================================================================

PROBLEMA QUE RESOLVE
--------------------
A base NASA fornece um risco basal por faixa de dificuldade; o J60 fornece
tarefas classificadas em quatro niveis de dificuldade pelo indice Di. Falta
ligar as duas. Este script executa essa ligacao e, mais importante, delimita
o que ela pode e o que ela nao pode afirmar.

ENTRADA
-------
  data/processed/nasa/base_dpp_consolidada.csv
  data/processed/psplib/tarefas_j60_com_di.csv

SAIDA
-----
  data/processed/psplib/tarefas_j60_com_risco.csv
  outputs/tables/psplib_03_razoes_de_risco.csv
  outputs/tables/psplib_03_ancora_sensibilidade.csv
  outputs/logs/psplib_03_transferencia_ordinal.log

A DECISAO METODOLOGICA CENTRAL
-------------------------------
`[DECISAO]` A transferencia e feita por RAZAO DE RISCO RELATIVO, e nao por
correspondencia direta de rotulos.

O motivo e numerico e verificavel. Os quatro niveis nao tem o mesmo tamanho
relativo nos dois dominios:

    nivel        NASA (modulos)      J60 (tarefas)
    baixa            86,24%              25,00%
    media             6,21%              25,00%
    alta              2,89%              25,00%
    muito alta        4,66%              25,00%

Atribuir a cada nivel do J60 o F_base absoluto do nivel homonimo da NASA
produziria risco medio de 0,3046 nas tarefas do J60, contra taxa observada de
0,1749 na NASA -- inflacao de 1,74 vezes gerada exclusivamente pela diferenca de
tamanho dos estratos, e nao por qualquer propriedade das tarefas. Seria um
artefato de construcao apresentado como resultado.

O que os dados NASA sustentam nao e o NIVEL absoluto de risco de um modulo de
software, que nao tem razao alguma para valer em tarefas de engenharia. E a
FORMA do gradiente: quantas vezes mais arriscada e uma tarefa dificil em relacao
a uma facil. Essa razao e adimensional e nao depende da taxa basal do dominio.

    F(nivel) = F_ancora * RR(nivel)

onde RR(nivel) e a razao de risco estimada na NASA e F_ancora e a taxa basal de
retrabalho do dominio de engenharia -- um PARAMETRO DO MODELO, nao um resultado
deste script. Enquanto nao houver dado empirico do dominio, F_ancora e varrido
em uma faixa plausivel e o efeito da escolha e reportado.

`[LIMITACAO]` Esta construcao assume que o gradiente ordinal de risco por
dificuldade e transferivel entre dominios, ainda que o nivel nao seja. E uma
suposicao, nao um resultado, e deve ser declarada como tal na monografia. Ela e
mais fraca do que supor equivalencia metrica direta, mas nao e vazia.

INTERVALOS DE CONFIANCA
-----------------------
`[DECISAO]` Os intervalos das razoes de risco sao obtidos por reamostragem
BOOTSTRAP POR PROJETO (cluster bootstrap): a cada replica sorteiam-se 12
projetos com reposicao e recalculam-se as frequencias por faixa.

Justificativa: as observacoes dentro de um mesmo projeto NAO sao independentes
-- compartilham equipe, processo, dominio e criterio de registro de defeito. Um
bootstrap sobre observacoes individuais trataria 17.377 modulos como 17.377
evidencias independentes e produziria intervalos artificialmente estreitos. A
unidade de reamostragem correta e o projeto, que e a unidade de agrupamento. E o
mesmo raciocinio da validacao leave-one-project-out do script 05.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. RR do nivel de referencia deve ser exatamente 1,0 por construcao.
  2. As RR pontuais devem reproduzir as razoes calculadas diretamente das
     frequencias do script 05.
  3. A mediana bootstrap deve ficar proxima da estimativa pontual; divergencia
     grande indicaria assimetria que invalida o intervalo percentil.
  4. O risco atribuido a cada tarefa deve permanecer em [0, 1] para toda ancora
     varrida; ancoras que violem isso devem ser sinalizadas.
"""

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
DIR_NASA = RAIZ / "data" / "processed" / "nasa"
DIR_PSP = RAIZ / "data" / "processed" / "psplib"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
for d in (DIR_TABELAS, DIR_LOGS):
    d.mkdir(parents=True, exist_ok=True)

NIVEIS = ["baixa", "media", "alta", "muito alta"]
CORTES_NASA = [10, 15, 20]
N_REPLICAS = 4000
SEMENTE = 20260905   # semente fixa: a reamostragem e aleatoria, o resultado nao

_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def faixas_nasa(base: pd.DataFrame) -> pd.Series:
    return pd.cut(base["CYCLOMATIC_COMPLEXITY"],
                  bins=[-np.inf] + CORTES_NASA + [np.inf], labels=NIVEIS, right=True)


def frequencias(base: pd.DataFrame) -> np.ndarray:
    """Frequencia de defeito por faixa, na ordem de NIVEIS. NaN se a faixa estiver vazia."""
    g = base.groupby("faixa", observed=False)["defective"].agg(["sum", "count"])
    return np.array([g.loc[n, "sum"] / g.loc[n, "count"] if g.loc[n, "count"] > 0 else np.nan
                     for n in NIVEIS], dtype=float)


def main() -> None:
    log("=" * 78)
    log("TRANSFERENCIA ORDINAL DE RISCO — NASA -> PSPLIB J60")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    nasa = pd.read_csv(DIR_NASA / "base_dpp_consolidada.csv")
    nasa["faixa"] = faixas_nasa(nasa)
    j60 = pd.read_csv(DIR_PSP / "tarefas_j60_com_di.csv")

    log(f"\nNASA : {len(nasa)} modulos, {nasa['project'].nunique()} projetos")
    log(f"J60  : {len(j60)} tarefas, {j60['arquivo'].nunique()} instancias")

    # -----------------------------------------------------------------
    # Estimativa pontual das razoes de risco
    # -----------------------------------------------------------------
    f = frequencias(nasa)
    rr = f / f[0]

    log("\n" + "=" * 78)
    log("RAZOES DE RISCO ESTIMADAS NA BASE NASA")
    log("=" * 78)
    log("  Referencia: nivel 'baixa'. RR e adimensional: quantas vezes mais")
    log("  provavel e o defeito em relacao ao nivel mais facil.")

    # -----------------------------------------------------------------
    # Bootstrap por projeto
    # -----------------------------------------------------------------
    projetos = sorted(nasa["project"].unique())
    por_projeto = {p: nasa[nasa["project"] == p] for p in projetos}
    rng = np.random.default_rng(SEMENTE)

    replicas = np.empty((N_REPLICAS, len(NIVEIS)), dtype=float)
    for i in range(N_REPLICAS):
        escolhidos = rng.choice(projetos, size=len(projetos), replace=True)
        amostra = pd.concat([por_projeto[p] for p in escolhidos], ignore_index=True)
        fr = frequencias(amostra)
        replicas[i] = fr / fr[0] if fr[0] and not np.isnan(fr[0]) else np.nan

    validas = ~np.isnan(replicas).any(axis=1)
    replicas = replicas[validas]
    log(f"\n  Replicas bootstrap validas: {len(replicas)} de {N_REPLICAS}")

    linhas_rr = []
    log(f"\n  {'nivel':<12} {'F_base NASA':>12} {'RR':>8} {'IC95 bootstrap':>22} "
        f"{'mediana boot':>13}")
    for k, nivel in enumerate(NIVEIS):
        lo, hi = np.percentile(replicas[:, k], [2.5, 97.5])
        mediana = float(np.median(replicas[:, k]))
        log(f"  {nivel:<12} {f[k]:>12.4f} {rr[k]:>8.3f} "
            f"[{lo:>8.3f}; {hi:>8.3f}] {mediana:>13.3f}")
        linhas_rr.append({
            "nivel": nivel,
            "F_base_nasa": round(float(f[k]), 6),
            "razao_de_risco": round(float(rr[k]), 5),
            "ic95_inferior": round(float(lo), 5),
            "ic95_superior": round(float(hi), 5),
            "mediana_bootstrap": round(mediana, 5),
            "n_replicas": len(replicas),
        })
    pd.DataFrame(linhas_rr).to_csv(DIR_TABELAS / "psplib_03_razoes_de_risco.csv",
                                   index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # Por que nao rotulo-para-rotulo: a evidencia numerica
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("POR QUE NAO CORRESPONDENCIA DIRETA DE ROTULOS")
    log("=" * 78)
    prop_nasa = nasa["faixa"].value_counts(normalize=True).reindex(NIVEIS)
    prop_j60 = j60["nivel_dificuldade"].value_counts(normalize=True).reindex(NIVEIS)
    log(f"  {'nivel':<12} {'NASA':>9} {'J60':>9}")
    for nivel in NIVEIS:
        log(f"  {nivel:<12} {prop_nasa[nivel]:>9.2%} {prop_j60[nivel]:>9.2%}")

    risco_direto = float((prop_j60.values * f).sum())
    taxa_nasa = float(nasa["defective"].mean())
    log(f"\n  Risco medio no J60 sob correspondencia direta : {risco_direto:.4f}")
    log(f"  Taxa observada na NASA                        : {taxa_nasa:.4f}")
    log(f"  Fator de inflacao                             : {risco_direto / taxa_nasa:.2f}x")
    log("  Essa inflacao vem da diferenca de tamanho dos estratos, nao de")
    log("  qualquer propriedade das tarefas. E artefato, e por isso o metodo")
    log("  adotado transfere a razao e nao o nivel.")

    # -----------------------------------------------------------------
    # Aplicacao ao J60 com varredura da ancora
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("APLICACAO AO J60 — VARREDURA DA ANCORA F_ancora")
    log("=" * 78)
    log("  `[ABERTO]` F_ancora e a taxa basal de retrabalho do dominio de")
    log("  engenharia, no nivel de dificuldade mais baixo. NAO e estimada aqui:")
    log("  e parametro do modelo, a ser fixado por dado do dominio (ObrasGov,")
    log("  CoST, World Bank) ou tratado como incerteza na simulacao.")

    mapa_rr = dict(zip(NIVEIS, rr))
    ancoras = [0.05, 0.10, 0.15, 0.20, 0.25]
    linhas_anc, avisos = [], []

    log(f"\n  {'F_ancora':>9} | " + " ".join(f"{n:>11}" for n in NIVEIS) + f" | {'medio J60':>10}")
    for a in ancoras:
        riscos = {n: a * mapa_rr[n] for n in NIVEIS}
        medio = float(sum(prop_j60[n] * riscos[n] for n in NIVEIS))
        fora = [n for n, v in riscos.items() if v > 1.0]
        if fora:
            avisos.append(f"ancora {a}: risco > 1 em {fora}")
        log(f"  {a:>9.2f} | " + " ".join(f"{riscos[n]:>11.4f}" for n in NIVEIS)
            + f" | {medio:>10.4f}" + ("   [AVISO: >1]" if fora else ""))
        linhas_anc.append({"F_ancora": a,
                           **{f"risco_{n.replace(' ', '_')}": round(riscos[n], 6) for n in NIVEIS},
                           "risco_medio_j60": round(medio, 6),
                           "algum_risco_acima_de_1": bool(fora)})
    pd.DataFrame(linhas_anc).to_csv(DIR_TABELAS / "psplib_03_ancora_sensibilidade.csv",
                                    index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # Gravacao por tarefa: multiplicador, nao probabilidade
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("SAIDA POR TAREFA")
    log("=" * 78)
    log("  `[DECISAO]` A base de tarefas recebe o MULTIPLICADOR de risco e seu")
    log("  intervalo, nao uma probabilidade absoluta. A probabilidade so existe")
    log("  depois que o modelo fixa F_ancora; grava-la aqui embutiria um valor")
    log("  arbitrario na base como se fosse dado.")

    ic_lo = dict(zip(NIVEIS, [l["ic95_inferior"] for l in linhas_rr]))
    ic_hi = dict(zip(NIVEIS, [l["ic95_superior"] for l in linhas_rr]))
    j60["multiplicador_risco"] = j60["nivel_dificuldade"].map(mapa_rr)
    j60["multiplicador_ic95_inferior"] = j60["nivel_dificuldade"].map(ic_lo)
    j60["multiplicador_ic95_superior"] = j60["nivel_dificuldade"].map(ic_hi)
    j60.to_csv(DIR_PSP / "tarefas_j60_com_risco.csv", index=False, encoding="utf-8")
    log(f"\n  data/processed/psplib/tarefas_j60_com_risco.csv ({len(j60)} linhas)")

    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("VERIFICACOES")
    log("=" * 78)
    falhas = []

    if abs(rr[0] - 1.0) < 1e-12:
        log("  [OK]    RR do nivel de referencia = 1 por construcao")
    else:
        falhas.append("RR de referencia diferente de 1")

    fbase_05 = pd.read_csv(DIR_TABELAS / "05_faixas_frequencias.csv")
    fbase_05 = fbase_05[fbase_05["eixo"] == "CYCLOMATIC_COMPLEXITY"].reset_index(drop=True)
    esperado = fbase_05["frequencia_bruta"].values / fbase_05["frequencia_bruta"].values[0]
    if np.allclose(rr, esperado, atol=1e-4):
        log("  [OK]    RR reproduzem as razoes das frequencias do script 05")
    else:
        falhas.append(f"RR divergem do script 05: {rr} vs {esperado}")
        log(f"  [FALHA] RR divergem do script 05")

    desvio_mediana = float(np.max(np.abs(np.median(replicas, axis=0) - rr)))
    if desvio_mediana < 0.15:
        log(f"  [OK]    Mediana bootstrap proxima da estimativa pontual "
            f"(desvio maximo {desvio_mediana:.4f})")
    else:
        log(f"  [ATENCAO] Mediana bootstrap afastada da pontual ({desvio_mediana:.4f}); "
            f"distribuicao assimetrica")

    if not avisos:
        log("  [OK]    Nenhuma ancora varrida produz risco acima de 1")
    else:
        for a in avisos:
            log(f"  [AVISO] {a}")

    if j60["multiplicador_risco"].isna().any():
        falhas.append("tarefas sem multiplicador atribuido")
        log("  [FALHA] Ha tarefas sem multiplicador")
    else:
        log(f"  [OK]    Todas as {len(j60)} tarefas receberam multiplicador")

    log("\n" + "=" * 78)
    log("RESULTADO: " + ("CONCLUIDO COM FALHAS" if falhas else "CONCLUIDO, VERIFICACOES OK"))
    for f_ in falhas:
        log(f"  - {f_}")
    log("=" * 78)

    (DIR_LOGS / "psplib_03_transferencia_ordinal.log").write_text("\n".join(_log) + "\n",
                                                                  encoding="utf-8")
    if falhas:
        sys.exit(1)


if __name__ == "__main__":
    main()
