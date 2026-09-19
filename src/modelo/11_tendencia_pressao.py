"""
11_tendencia_pressao.py — Verificação 8 refeita com desenho de potência (item B1)
===================================================================================

O PROBLEMA
----------
A verificação 8 original calculava Spearman sobre CINCO MÉDIAS e reportava o
valor-p assintótico que o scipy devolve nesse caso. Com n = 5 o menor valor-p
bilateral EXATO é 2/5! = 0,0167; um p da ordem de 1e-24 não é atingível e não
podia ter sido usado como evidência. Além disso o teste só rodava no braço
centralizado, em uma instância.

Refeito sobre os pontos individuais e nos dois braços, ele **deixou de se
confirmar no braço adaptativo** (ρ = +0,042, p = 0,56). Antes de declarar a
propriedade como não verificada, foram medidas as duas causas candidatas.

CAUSA 1 — A DOSE RECEBIDA É MENOR NO BRAÇO ADAPTATIVO
------------------------------------------------------
`P(t)` é ENDÓGENA: pela definição da seção 7 da especificação, ela responde ao
atraso relativo ao cronograma do CPM. O braço adaptativo conclui mais perto do
CPM, atrasa menos, e por isso recebe MENOS pressão para o mesmo `P_max`
nominal. Medido (média de P(t) realizada, 2 instâncias × 40 sementes):

    P_max nominal        0,2     0,4     0,6     0,8     1,0    amplitude
    centralizada       0,200   0,347   0,495   0,641   0,796      0,596
    adaptativa         0,200   0,266   0,346   0,436   0,540      0,340

A manipulação entrega ao braço adaptativo **57% da amplitude** que entrega ao
centralizado. Os dois braços não recebem o mesmo tratamento, e comparar as
inclinações entre braços compara doses diferentes.

CAUSA 2 — O CANAL DE DEFEITO É POUCO SENSÍVEL À PRESSÃO, POR PARAMETRIZAÇÃO
----------------------------------------------------------------------------
Pela equação (4), `p_falha = F_base(nível) + R_error · (1 − μ_cog)`, com
`F_ancora = 0,10`, `R_error = 0,15` e `RR = 1,000 / 1,935 / 2,367 / 2,985`:

    nível         F_base   p_falha(μ=0,98)   p_falha(μ=0,69)   razão
    baixa         0,1000        0,1030            0,1465        1,42x
    média         0,1935        0,1965            0,2400        1,22x
    alta          0,2367        0,2397            0,2832        1,18x
    muito alta    0,2985        0,3015            0,3450        1,14x

Ir de pressão nula a pressão máxima acrescenta **no máximo 0,047** à
probabilidade de falha, contra uma base de 0,100 a 0,299. A DIFICULDADE varia
`p_falha` por um fator de 2,985; a PRESSÃO, por 1,14 a 1,42. Nesta
parametrização a dificuldade domina a pressão no canal de defeito por um fator
de 3 a 20. `[LIMITACAO]` Isto é propriedade declarada do modelo calibrado, não
defeito: `F_base` vem da transferência ordinal sobre a NASA MDP e `R_error` é
premissa.

CONSEQUÊNCIA E CORREÇÃO
-----------------------
Com dose menor e canal fraco, o efeito no braço adaptativo fica abaixo do que
n = 200 consegue detectar. Os intervalos de confiança do piloto mostram isso: no
braço adaptativo o IC95 de ρ para defeitos gerados é [−0,050; +0,225], ou seja,
compatível TANTO com ausência de efeito QUANTO com o efeito observado no braço
centralizado. **O teste é não informativo, não falsificador.**

`[DEC]` Desenho em duas etapas, que é a resposta correta a um teste
subdimensionado — e não mexer no critério até ele passar:

  ETAPA 1 (piloto, sementes 0-39): estima o tamanho de efeito. NÃO confirmatória.
  ETAPA 2 (confirmatória, sementes 1000+): n fixado por cálculo de potência
          ANTES de rodar, com sementes INDEPENDENTES do piloto, para que a
          escolha de n não contamine o teste.

`[DEC]` Tamanho de efeito de referência: ρ observado no braço centralizado
(dose plena) reescalado pela razão de amplitude de dose medida (0,340/0,596 =
0,57). Não é o menor ρ do piloto — usar o mais ruidoso inflaria n sem
justificativa. Não é escolhido para o teste passar: é derivado do braço onde a
dose é plena, e a mesma regra vale para os dois braços.

`[DEC]` n por célula pela aproximação de Fisher para Spearman:
    n = ( (z_{α/2} + z_β) / arctanh(ρ_ref) )² + 3,  α = 0,05 bilateral, potência 0,80.

`[DEC]` O CRITÉRIO NÃO MUDA: ρ > 0 e p < 0,05. Só n muda.

`[DEC]` Reporta-se sempre o IC95 de ρ, não só o p. Um p acima de 0,05 com IC
largo é ausência de informação; com IC estreito em torno de zero é ausência de
efeito. São conclusões diferentes e o documento precisa distingui-las.

SAIDA
-----
  outputs/tables/modelo_11_tendencia_piloto.csv
  outputs/tables/modelo_11_tendencia_confirmatorio.csv
  outputs/tables/modelo_11_tendencia_resumo.csv
  outputs/tables/modelo_11_dose_realizada.csv
  outputs/logs/modelo_11_tendencia_pressao.log
"""

import copy
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
DIR_PARCIAIS = DIR_TABELAS / "_tendencia_parciais"

NIVEIS_P = (0.2, 0.4, 0.6, 0.8, 1.0)
CENARIOS = ("centralizada", "adaptativa")
SEM_PILOTO = range(0, 40)                 # 40 x 5 = 200 por celula
SEM_CONFIRMATORIO = range(1000, 1100)     # 100 x 5 = 500 por celula, independentes
ALVOS = ("defeitos_gerados", "S_UR_maximo", "fracao_heuristica")
ALFA, POTENCIA = 0.05, 0.80


def instancias():
    todas = sorted(pd.read_csv(RAIZ / "data" / "processed" / "psplib" /
                               "tarefas_j60_com_di.csv")["arquivo"].unique())
    return todas[::40][:2]


def celulas():
    return [(a, c) for a in instancias() for c in CENARIOS]


def n_por_potencia(rho: float, alfa=ALFA, potencia=POTENCIA) -> int:
    """n mínimo para detectar rho num teste bilateral, aproximação de Fisher."""
    if abs(rho) >= 1 or rho == 0:
        return 10 ** 9
    z_a = stats.norm.ppf(1 - alfa / 2)
    z_b = stats.norm.ppf(potencia)
    return int(np.ceil(((z_a + z_b) / np.arctanh(abs(rho))) ** 2 + 3))


def ic_spearman(rho: float, n: int, alfa=ALFA):
    """IC de Fisher para rho de Spearman (Bonett-Wright: ep = sqrt(1.06/(n-3)))."""
    if n <= 4:
        return (np.nan, np.nan)
    ep = np.sqrt(1.06 / (n - 3))
    z = np.arctanh(np.clip(rho, -0.999999, 0.999999))
    q = stats.norm.ppf(1 - alfa / 2)
    return float(np.tanh(z - q * ep)), float(np.tanh(z + q * ep))


def rodar(arq: str, cen: str, sementes, etapa: str) -> None:
    par = S.carregar_parametros()
    g, disp, cpm = S.carregar_instancia(arq)
    linhas = []
    for pmax in NIVEIS_P:
        p2 = copy.deepcopy(par)
        p2["gestor"]["P_max"]["valor"] = pmax
        p2["gestor"]["P_min"]["valor"] = min(0.2, pmax)
        for sem in sementes:
            sim = S.Simulacao(g, disp, cpm, p2, cen, semente=sem)
            r = sim.executar()
            tot = sum(a.periodos_heuristicos + a.periodos_analiticos
                      for a in sim.agentes)
            linhas.append({
                "etapa": etapa, "arquivo": arq, "cenario": cen,
                "P_max": pmax, "semente": sem,
                "P_realizada_media": float(np.mean(sim.traj["P"])),
                "mu_cog_medio": float(np.mean(sim.traj["mu_cog"])),
                "defeitos_gerados": r.n_com_erro + r.n_reportadas,
                "retrabalho_sobre_esforco_total": r.retrabalho_sobre_esforco_total, "taxa_falha_efetiva": r.taxa_falha_efetiva,
                "S_UR_maximo": r.S_UR_maximo,
                "fracao_heuristica": sum(a.periodos_heuristicos
                                         for a in sim.agentes) / max(1, tot),
            })
    DIR_PARCIAIS.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(linhas).to_csv(
        DIR_PARCIAIS / f"{etapa}_{arq}_{cen}.csv", index=False, encoding="utf-8")
    print(f"{etapa} {arq} {cen}: {len(linhas)} execucoes")


def juntar(etapa: str):
    fs = [DIR_PARCIAIS / f"{etapa}_{a}_{c}.csv" for a, c in celulas()]
    faltando = [f.name for f in fs if not f.exists()]
    if faltando:
        raise SystemExit(f"faltam rodar ({etapa}): {faltando}")
    return pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)


def testar(d: pd.DataFrame, arq: str, cen: str, alvo: str, preditor="P_max"):
    s = d[(d.arquivo == arq) & (d.cenario == cen)]
    rho, pv = stats.spearmanr(s[preditor], s[alvo])
    lo, hi = ic_spearman(rho, len(s))
    return {"arquivo": arq, "cenario": cen, "alvo": alvo, "preditor": preditor,
            "n": int(len(s)), "rho": float(rho), "ic95_baixo": lo,
            "ic95_alto": hi, "p_valor": float(pv),
            "aprova": bool(rho > 0 and pv < ALFA)}


def analisar() -> None:
    _log = []

    def log(m=""):
        print(m)
        _log.append(m)

    dp = juntar("piloto")
    dc = juntar("confirmatorio")
    dp.to_csv(DIR_TABELAS / "modelo_11_tendencia_piloto.csv", index=False,
              encoding="utf-8")
    dc.to_csv(DIR_TABELAS / "modelo_11_tendencia_confirmatorio.csv", index=False,
              encoding="utf-8")

    log("=" * 78)
    log("VERIFICACAO 8 REFEITA — resposta a pressao, desenho em duas etapas [B1]")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)
    log(f"\nInstancias: {sorted(dp.arquivo.unique())}   Cenarios: {list(CENARIOS)}")
    log(f"Niveis de P_max: {list(NIVEIS_P)}")
    log(f"Piloto       : sementes {min(SEM_PILOTO)}-{max(SEM_PILOTO)}, "
        f"n = {len(dp) // 4} por celula, {len(dp)} execucoes")
    log(f"Confirmatorio: sementes {min(SEM_CONFIRMATORIO)}-{max(SEM_CONFIRMATORIO)}, "
        f"n = {len(dc) // 4} por celula, {len(dc)} execucoes")
    log("As sementes do confirmatorio sao DISJUNTAS das do piloto: a escolha de n")
    log("nao contamina o teste.")

    # ---------------- dose realizada -------------------------------------
    dose = (dp.groupby(["cenario", "P_max"])["P_realizada_media"].mean()
            .unstack().reindex(CENARIOS))
    amp = (dose.max(axis=1) - dose.min(axis=1))
    log("\n" + "-" * 78)
    log("DOSE REALIZADA — P(t) e endogena, logo os bracos nao recebem o mesmo")
    log("tratamento para o mesmo P_max nominal")
    log("-" * 78)
    log(f"  {'cenario':<14} " + " ".join(f"P_max={x:.1f}" for x in NIVEIS_P)
        + "   amplitude")
    for cen in CENARIOS:
        log(f"  {cen:<14} " + " ".join(f"{dose.loc[cen, x]:9.4f}" for x in NIVEIS_P)
            + f"   {amp[cen]:9.4f}")
    razao_dose = float(amp["adaptativa"] / amp["centralizada"])
    log(f"\n  Razao de amplitude adaptativa/centralizada = {razao_dose:.4f}")
    dose.assign(amplitude=amp, razao_vs_centralizada=amp / amp["centralizada"]).to_csv(
        DIR_TABELAS / "modelo_11_dose_realizada.csv", encoding="utf-8")

    # ---------------- piloto e calculo de n ------------------------------
    log("\n" + "-" * 78)
    log("ETAPA 1 — PILOTO (nao confirmatorio): estimativa do tamanho de efeito")
    log("-" * 78)
    log(f"  {'instancia':<13} {'cenario':<13} {'alvo':<18} {'n':>4} {'rho':>7} "
        f"{'IC95':>18} {'p':>10}")
    piloto = [testar(dp, a, c, alvo) for a, c in celulas() for alvo in ALVOS]
    for r in piloto:
        log(f"  {r['arquivo']:<13} {r['cenario']:<13} {r['alvo']:<18} {r['n']:>4} "
            f"{r['rho']:>+7.3f}  [{r['ic95_baixo']:+.3f}; {r['ic95_alto']:+.3f}] "
            f"{r['p_valor']:>10.2e}")

    log("\n  Calculo de n, por alvo (alfa 0,05 bilateral, potencia 0,80):")
    log(f"  {'alvo':<18} {'rho ref. (centr.)':>18} {'rho esperado adapt.':>21} "
        f"{'n necessario':>13}")
    n_alvo = {}
    for alvo in ALVOS:
        ref = float(np.mean([r["rho"] for r in piloto
                             if r["alvo"] == alvo and r["cenario"] == "centralizada"]))
        esperado = ref * razao_dose
        n_alvo[alvo] = n_por_potencia(esperado)
        log(f"  {alvo:<18} {ref:>+18.3f} {esperado:>+21.3f} {n_alvo[alvo]:>13,}")
    log("")
    log(f"  n adotado no confirmatorio: {len(dc) // 4} por celula.")
    for alvo in ALVOS:
        situacao = ("suficiente" if len(dc) // 4 >= n_alvo[alvo]
                    else f"INSUFICIENTE (faltam {n_alvo[alvo] - len(dc)//4:,})")
        log(f"    {alvo:<18} exige {n_alvo[alvo]:>9,}  ->  {situacao}")

    # ---------------- confirmatorio --------------------------------------
    log("\n" + "-" * 78)
    log("ETAPA 2 — CONFIRMATORIO (criterio inalterado: rho > 0 e p < 0,05)")
    log("-" * 78)
    log(f"  {'instancia':<13} {'cenario':<13} {'alvo':<18} {'n':>4} {'rho':>7} "
        f"{'IC95':>18} {'p':>10}  veredito")
    conf = [testar(dc, a, c, alvo) for a, c in celulas() for alvo in ALVOS]
    for r in conf:
        potente = len(dc) // 4 >= n_alvo[r["alvo"]]
        if r["aprova"]:
            v = "CONFIRMA"
        elif not potente:
            v = "NAO INFORMATIVO (subdimensionado)"
        elif r["ic95_alto"] < 0.05:
            v = "REFUTA (IC exclui efeito relevante)"
        else:
            v = "NAO CONFIRMA"
        r["veredito"] = v
        r["potencia_suficiente"] = bool(potente)
        log(f"  {r['arquivo']:<13} {r['cenario']:<13} {r['alvo']:<18} {r['n']:>4} "
            f"{r['rho']:>+7.3f}  [{r['ic95_baixo']:+.3f}; {r['ic95_alto']:+.3f}] "
            f"{r['p_valor']:>10.2e}  {v}")

    res = pd.DataFrame([{**r, "etapa": "piloto"} for r in piloto]
                       + [{**r, "etapa": "confirmatorio"} for r in conf])
    res.to_csv(DIR_TABELAS / "modelo_11_tendencia_resumo.csv", index=False,
               encoding="utf-8")

    log("\n" + "-" * 78)
    log("SINTESE POR BRACO E ALVO")
    log("-" * 78)
    for alvo in ALVOS:
        for cen in CENARIOS:
            rs = [r for r in conf if r["alvo"] == alvo and r["cenario"] == cen]
            n_ok = sum(r["aprova"] for r in rs)
            log(f"  {alvo:<18} {cen:<14} confirma em {n_ok} de {len(rs)} instancias"
                + ("" if n_ok == len(rs)
                   else "   -> " + "; ".join(sorted({r["veredito"] for r in rs
                                                     if not r["aprova"]}))))
    log("")
    log("  `[LIMITACAO]` 'NAO CONFIRMA' nao e 'refutado'. Quando o IC95 de rho")
    log("  contem tanto o zero quanto o efeito observado no braco de dose plena,")
    log("  os dados nao distinguem as duas hipoteses.")
    log("  `[LIMITACAO]` A dose recebida difere entre bracos por construcao do")
    log("  modelo (P(t) endogena). O experimento manipula P_max, nao P(t), e")
    log("  portanto nao e um contraste de mesma dose entre bracos.")

    log("\n--- Arquivos gerados ---")
    for f in ("piloto", "confirmatorio", "resumo", ):
        log(f"  outputs/tables/modelo_11_tendencia_{f}.csv")
    log("  outputs/tables/modelo_11_dose_realizada.csv")
    (DIR_LOGS / "modelo_11_tendencia_pressao.log").write_text(
        "\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--listar":
        for a, c in celulas():
            print(f"{a} {c}")
    elif len(sys.argv) > 3 and sys.argv[1] in ("--piloto", "--confirmatorio"):
        etapa = sys.argv[1][2:]
        sems = SEM_PILOTO if etapa == "piloto" else SEM_CONFIRMATORIO
        rodar(sys.argv[2], sys.argv[3], sems, etapa)
    else:
        analisar()
