"""
07_ablacao_governanca.py — Ablacao do experimento de governanca (item B9)
==========================================================================

MOTIVO
------
Os dois arranjos de governanca do experimento diferem em QUATRO parametros ao
mesmo tempo (`tau_inicial`, `tau_min`, `p_reporte`, `p_deteccao`). Enquanto
variarem juntos, nenhum efeito observado pode ser atribuido a mecanismo nenhum:
a comparacao mede o PACOTE, nao um mecanismo. Este script separa as parcelas.

Sao tres blocos, com perguntas distintas:

  BLOCO 1 — ablacao de PARAMETRO. Parte da centralizada e troca um parametro de
  cada vez pelo valor adaptativo. Responde: quanto do efeito total vem de cada
  parametro isolado, e quanto so aparece na combinacao?

  BLOCO 2 — ablacao de MECANISMO. Mantem os dois cenarios como estao e desliga
  (ou universaliza) a concessao de ajuda da Porta 2 nos DOIS bracos. Responde:
  quanto da diferenca entre as politicas depende da assistencia associada a
  `tau` constante, e o efeito principal permanece, diminui, some ou inverte?

  BLOCO 3 — varredura de `p_reporte`. O parametro entra binario no experimento;
  aqui e varrido, para separar gradiente de artefato de dois pontos.

`[DEC]` UNIDADE INFERENCIAL: a INSTANCIA. As 12 sementes de uma mesma instancia
nao sao projetos independentes; tratar cada semente como observacao e
pseudorreplicacao. Cada instancia entra com a MEDIA das suas sementes, e os
testes pareados correm sobre as instancias. Com n = 16, o menor valor-p bilateral
possivel no Wilcoxon e 2/2^16 = 3,05e-05: valores-p menores do que isso nao sao
atingiveis e qualquer numero abaixo disso em outra tabela e artefato de unidade.

`[DEC]` PAREAMENTO: mesma instancia e mesma semente em todos os bracos. A
construcao dos agentes consome os mesmos sorteios em todos eles, de modo que a
competencia inicial de cada agente e IDENTICA entre bracos para uma dada
(instancia, semente). O que diverge e apenas a trajetoria posterior.

`[LIMITACAO]` A ablacao de mecanismo altera a dinamica e portanto o consumo de
numeros aleatorios a partir do primeiro ponto de divergencia. O pareamento
garante o mesmo ponto de partida, nao a mesma sequencia de sorteios ao longo da
execucao. E o mesmo limite de qualquer ablacao em modelo estocastico sequencial.

`[DEC]` Este script NAO altera o modelo. A instrumentacao em `simulador.py` e
composta de contadores observacionais e de um parametro `ablacoes` vazio por
padrao; com o padrao, a execucao nominal e bit-a-bit identica a de antes da
instrumentacao (conferido por impressao digital SHA-256 sobre 32 execucoes).

SAIDA
-----
  outputs/tables/modelo_07_ablacao_bruto.csv
  outputs/tables/modelo_07_ablacao_parametros.csv
  outputs/tables/modelo_07_ablacao_mecanismo.csv
  outputs/tables/modelo_07_ablacao_portas.csv
  outputs/tables/modelo_07_ablacao_p_reporte.csv
  outputs/logs/modelo_07_ablacao.log
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
_log: list[str] = []

# `[DEC]` Execucao em PARTES. Cada braco e uma invocacao independente que grava
# o proprio CSV parcial em outputs/tables/_b9_parciais/. O motivo e operacional:
# o ambiente onde isto roda encerra processos ao fim de cada chamada de shell, e
# uma execucao unica de ~15 min nao sobrevive. A consequencia metodologica e
# nula: cada braco e semeado por (instancia, semente) e independe da ordem.
#   python3 07_ablacao_governanca.py --rodar <braco>   ... um braco
#   python3 07_ablacao_governanca.py --listar          ... nomes dos bracos
#   python3 07_ablacao_governanca.py --analisar        ... junta e analisa
N_INSTANCIAS = 16
N_SEMENTES = 12
DIR_PARCIAIS = RAIZ / "outputs" / "tables" / "_b9_parciais"

# Parametros organizacionais que separam os dois arranjos.
ORGANIZACIONAIS = ("tau_inicial", "tau_min", "p_reporte", "p_deteccao")

# Metricas principais, as mesmas ja usadas nos resultados do experimento.
METRICAS = [
    ("atraso_relativo", "menor e melhor"),
    ("E_total", "maior e melhor"),
    ("TL", "informativa"),
    ("TU", "menor e melhor"),
    ("TR", "menor e melhor"),
    ("TW", "informativa"),
    ("n_com_erro", "menor e melhor"),
    ("taxa_omissao", "menor e melhor"),
    ("taxa_falha_efetiva", "menor e melhor"),
    ("retrabalho_sobre_plano", "menor e melhor"),
    ("divida_latente_sobre_plano", "menor e melhor"),
    ("S_UR_maximo", "menor e melhor"),
]

CONTADORES = ["p1_omissao", "p1_fuga", "p2_ajuda", "p2_bloqueio", "p3_analitica",
              "hiato_encontrado", "hiato_sem_colega_capaz",
              "hiato_sem_colega_livre", "hiato_colega_capaz_sem_confianca",
              "tarefas_acima_da_competencia_maxima_inicial",
              "competencia_minima_inicial", "competencia_maxima_inicial",
              "competencia_maxima_final"]


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def montar_cenarios(par: dict) -> dict:
    """
    Acrescenta os cenarios sinteticos do BLOCO 1 ao dicionario de parametros.

    Cada um parte da centralizada e recebe o valor ADAPTATIVO de um subconjunto
    dos parametros organizacionais. Nenhum valor e digitado: todos vem do YAML.
    """
    par = copy.deepcopy(par)
    cen = par["cenarios"]
    base, alvo = cen["centralizada"], cen["adaptativa"]

    combinacoes = {f"so_{k}": (k,) for k in ORGANIZACIONAIS}
    # O par (tau_inicial, tau_min) e testado junto porque e ele, e nao cada um
    # isolado, que define se a condicao `confianca > tau_min` da Porta 2 pode
    # ser satisfeita. Isolar so um dos dois pode nao destravar nada.
    combinacoes["so_par_tau"] = ("tau_inicial", "tau_min")
    combinacoes["sem_par_tau"] = ("p_reporte", "p_deteccao")

    for nome, chaves in combinacoes.items():
        novo = copy.deepcopy(base)
        for k in chaves:
            novo[k] = copy.deepcopy(alvo[k])
        cen[nome] = novo
    return par


def executar(par, instancias, cenario, ablacoes=frozenset(), rotulo=None):
    """Roda a grade (instancia x semente) de UM braco e devolve as linhas."""
    linhas = []
    for arq in instancias:
        g, disp, cpm = S.carregar_instancia(arq)
        for sem in range(N_SEMENTES):
            r = S.Simulacao(g, disp, cpm, par, cenario, semente=sem,
                            ablacoes=ablacoes).executar()
            linha = {
                "braco": rotulo or cenario, "cenario": cenario,
                "ablacao": ";".join(sorted(ablacoes)) or "nenhuma",
                "arquivo": arq, "semente": sem,
                "concluiu": r.concluiu, "makespan": r.makespan,
                "atraso_relativo": r.makespan / r.makespan_cpm,
                "retrabalho_sobre_esforco_total": r.retrabalho_sobre_esforco_total, "taxa_falha_efetiva": r.taxa_falha_efetiva,
                "E_total": r.E_total, "TW": r.TW, "TL": r.TL,
                "TU": r.TU, "TR": r.TR,
                "n_com_erro": r.n_com_erro, "n_reportadas": r.n_reportadas,
                "n_adiamentos": r.n_adiamentos, "taxa_omissao": r.taxa_omissao,
                "S_UR_maximo": r.S_UR_maximo, "E_plano": r.E_plano,
                "retrabalho_sobre_plano": r.retrabalho_sobre_plano,
                "divida_latente_sobre_plano": r.divida_latente_sobre_plano,
            }
            for c in CONTADORES:
                linha[c] = r.contadores.get(c)
            linhas.append(linha)
    return linhas


def por_instancia(d: pd.DataFrame, braco: str, metrica: str) -> np.ndarray:
    """Media das sementes dentro de cada instancia, ordenada por instancia."""
    sel = d[d["braco"] == braco]
    return sel.groupby("arquivo")[metrica].mean().sort_index().values


def comparar(x: np.ndarray, y: np.ndarray) -> dict:
    """Comparacao pareada y - x sobre instancias. y = tratamento, x = referencia."""
    dif = y - x
    if np.allclose(dif, 0):
        return {"dif_absoluta": 0.0, "dif_relativa_pct": 0.0, "p_valor": np.nan,
                "d_cohen_pareado": np.nan, "prop_instancias_com_dif": 0.0,
                "n_instancias": int(len(dif))}
    est, pv = stats.wilcoxon(y, x)
    dp = float(np.std(dif, ddof=1))
    return {
        "dif_absoluta": float(np.mean(dif)),
        "dif_relativa_pct": (float(100 * np.mean(dif) / np.mean(x))
                             if np.mean(x) != 0 else np.nan),
        "p_valor": float(pv),
        "d_cohen_pareado": float(np.mean(dif) / dp) if dp > 0 else np.nan,
        "prop_instancias_com_dif": float(np.mean(dif != 0)),
        "n_instancias": int(len(dif)),
    }


def preparar():
    """Devolve (par, instancias, bracos, ablacao_de_cada_braco)."""
    par = montar_cenarios(S.carregar_parametros())
    todas = sorted(pd.read_csv(RAIZ / "data" / "processed" / "psplib" /
                               "tarefas_j60_com_di.csv")["arquivo"].unique())
    passo = max(1, len(todas) // N_INSTANCIAS)
    instancias = todas[::passo][:N_INSTANCIAS]

    bracos: dict[str, tuple[str, frozenset]] = {}
    for b in (["centralizada", "adaptativa"]
              + [f"so_{k}" for k in ORGANIZACIONAIS]
              + ["so_par_tau", "sem_par_tau"]):
        bracos[b] = (b, frozenset())
    for abl in ("sem_assistencia", "assistencia_universal",
                "sem_filtro_competencia"):
        for cen in ("centralizada", "adaptativa"):
            bracos[f"{cen}__{abl}"] = (cen, frozenset({abl}))

    p_c = float(S.v(par["cenarios"]["centralizada"]["p_reporte"]))
    p_a = float(S.v(par["cenarios"]["adaptativa"]["p_reporte"]))
    niveis = [round(x, 4) for x in np.linspace(p_c, p_a, 5)]
    for pr in niveis[1:-1]:
        nome = f"pr_{pr:.4f}"
        novo = copy.deepcopy(par["cenarios"]["centralizada"])
        novo["p_reporte"] = {"valor": pr, "condicao": "varredura_B9"}
        par["cenarios"][nome] = novo
        bracos[nome] = (nome, frozenset())
    return par, instancias, bracos, (p_c, p_a, niveis)


def rodar_braco(nome: str) -> None:
    par, instancias, bracos, _ = preparar()
    if nome not in bracos:
        raise SystemExit(f"braco desconhecido: {nome}\n{sorted(bracos)}")
    cen, abl = bracos[nome]
    DIR_PARCIAIS.mkdir(parents=True, exist_ok=True)
    linhas = executar(par, instancias, cen, abl, rotulo=nome)
    pd.DataFrame(linhas).to_csv(DIR_PARCIAIS / f"{nome}.csv", index=False,
                                encoding="utf-8")
    print(f"{nome}: {len(linhas)} execucoes gravadas")


def main() -> None:
    log("=" * 78)
    log("B9 — ABLACAO DO EXPERIMENTO DE GOVERNANCA")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    par, instancias, todos_bracos, (p_c, p_a, niveis) = preparar()

    log(f"\nInstancias : {len(instancias)}   Sementes: {N_SEMENTES}")
    log(f"Unidade inferencial: INSTANCIA (n = {len(instancias)}); "
        f"menor p bilateral atingivel = {2 / 2**len(instancias):.2e}")
    log("\nValores dos parametros organizacionais (lidos do YAML):")
    log(f"  {'parametro':<14} {'centralizada':>13} {'adaptativa':>12}")
    for k in ORGANIZACIONAIS:
        log(f"  {k:<14} {S.v(par['cenarios']['centralizada'][k]):>13} "
            f"{S.v(par['cenarios']['adaptativa'][k]):>12}")

    bracos = ["centralizada", "adaptativa"] + [f"so_{k}" for k in ORGANIZACIONAIS] \
             + ["so_par_tau", "sem_par_tau"]
    faltando = [b for b in todos_bracos if not (DIR_PARCIAIS / f"{b}.csv").exists()]
    if faltando:
        raise SystemExit("bracos ainda nao rodados: " + ", ".join(faltando))
    d = pd.concat([pd.read_csv(DIR_PARCIAIS / f"{b}.csv") for b in todos_bracos],
                  ignore_index=True)
    d.to_csv(DIR_TABELAS / "modelo_07_ablacao_bruto.csv", index=False,
             encoding="utf-8")
    log(f"\n  {len(d)} execucoes; nao concluiram: {int((~d['concluiu']).sum())}")

    # -----------------------------------------------------------------
    # Tabela de portas
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("CONTAGEM POR PORTA (media por execucao, sobre instancia x semente)")
    log("=" * 78)
    portas = (d.groupby("braco")[CONTADORES + ["n_adiamentos"]]
              .mean().round(4).reset_index())
    portas.to_csv(DIR_TABELAS / "modelo_07_ablacao_portas.csv", index=False,
                  encoding="utf-8")
    log(f"\n  {'braco':<34} {'P1 omis':>8} {'P1 fuga':>8} {'P2 ajuda':>9} "
        f"{'P2 bloq':>8} {'P3 anal':>8} {'hiato':>7} {'>comp':>6}")
    for r in portas.itertuples():
        log(f"  {r.braco:<34} {r.p1_omissao:>8.2f} {r.p1_fuga:>8.2f} "
            f"{r.p2_ajuda:>9.2f} {r.p2_bloqueio:>8.2f} {r.p3_analitica:>8.2f} "
            f"{r.hiato_encontrado:>7.2f} "
            f"{r.tarefas_acima_da_competencia_maxima_inicial:>6.2f}")
    log("\n  '>comp' = tarefas cuja dificuldade excede a MAIOR competencia inicial")
    log("  disponivel na equipe. Depende so da instancia e da semente, portanto e")
    log("  identico entre bracos — e a medida do hiato estrutural.")
    log("\n  Decomposicao do hiato (por que a ajuda nao foi concedida):")
    log(f"  {'braco':<34} {'hiato':>8} {'sem colega':>11} {'colega s/ conf':>15} "
        f"{'ajuda':>8}")
    for r in portas.itertuples():
        log(f"  {r.braco:<34} {r.hiato_encontrado:>8.2f} "
            f"{r.hiato_sem_colega_capaz:>11.2f} "
            f"{r.hiato_colega_capaz_sem_confianca:>15.2f} {r.p2_ajuda:>8.2f}")

    # -----------------------------------------------------------------
    # BLOCO 1 — resultados
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("BLOCO 1 — ABLACAO DE PARAMETRO (referencia: centralizada)")
    log("=" * 78)
    saida1 = []
    for m, sentido in METRICAS:
        ref = por_instancia(d, "centralizada", m)
        total = por_instancia(d, "adaptativa", m) - ref
        efeito_total = float(np.mean(total))
        log(f"\n  {m}   [{sentido}]   centralizada = {np.mean(ref):.4f}   "
            f"efeito total (adapt - centr) = {efeito_total:+.4f}")
        log(f"    {'braco':<18} {'media':>10} {'dif abs':>10} {'dif %':>9} "
            f"{'p':>11} {'d':>8} {'% do efeito total':>18}")
        for b in bracos:
            y = por_instancia(d, b, m)
            c = comparar(ref, y)
            fracao = (100 * c["dif_absoluta"] / efeito_total
                      if abs(efeito_total) > 1e-12 else np.nan)
            log(f"    {b:<18} {np.mean(y):>10.4f} {c['dif_absoluta']:>+10.4f} "
                f"{c['dif_relativa_pct']:>+8.1f}% {c['p_valor']:>11.2e} "
                f"{c['d_cohen_pareado']:>8.2f} {fracao:>17.1f}%")
            saida1.append({"metrica": m, "sentido": sentido, "braco": b,
                           "media_referencia_centralizada": float(np.mean(ref)),
                           "media_braco": float(np.mean(y)),
                           "efeito_total_adaptativa": efeito_total,
                           "fracao_do_efeito_total_pct": fracao, **c})
    pd.DataFrame(saida1).to_csv(DIR_TABELAS / "modelo_07_ablacao_parametros.csv",
                                index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # BLOCO 2 — resultados
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("BLOCO 2 — ABLACAO DE MECANISMO: efeito centralizada x adaptativa")
    log("=" * 78)
    configs = [("nominal", "centralizada", "adaptativa"),
               ("sem_assistencia", "centralizada__sem_assistencia",
                "adaptativa__sem_assistencia"),
               ("assistencia_universal", "centralizada__assistencia_universal",
                "adaptativa__assistencia_universal")]
    saida2 = []
    for m, sentido in METRICAS:
        log(f"\n  {m}   [{sentido}]")
        log(f"    {'config':<24} {'centr.':>10} {'adapt.':>10} {'dif abs':>10} "
            f"{'dif %':>9} {'p':>11} {'d':>8}")
        ref_abs = None
        for nome, bc, ba in configs:
            x = por_instancia(d, bc, m)
            y = por_instancia(d, ba, m)
            c = comparar(x, y)
            if nome == "nominal":
                ref_abs = c["dif_absoluta"]
            resto = (100 * c["dif_absoluta"] / ref_abs
                     if ref_abs not in (None, 0) and abs(ref_abs) > 1e-12 else np.nan)
            log(f"    {nome:<24} {np.mean(x):>10.4f} {np.mean(y):>10.4f} "
                f"{c['dif_absoluta']:>+10.4f} {c['dif_relativa_pct']:>+8.1f}% "
                f"{c['p_valor']:>11.2e} {c['d_cohen_pareado']:>8.2f}")
            saida2.append({"metrica": m, "sentido": sentido, "configuracao": nome,
                           "media_centralizada": float(np.mean(x)),
                           "media_adaptativa": float(np.mean(y)),
                           "efeito_nominal_absoluto": ref_abs,
                           "efeito_restante_pct_do_nominal": resto, **c})
        # diagnostico de direcao
        e = [s for s in saida2 if s["metrica"] == m]
        d_nom = e[0]["dif_absoluta"]
        for s in e[1:]:
            if abs(d_nom) < 1e-12:
                v = "sem efeito nominal a comparar"
            elif np.sign(s["dif_absoluta"]) != np.sign(d_nom) and abs(s["dif_absoluta"]) > 1e-12:
                v = "INVERTE"
            elif abs(s["dif_absoluta"]) < 0.05 * abs(d_nom):
                v = "DESAPARECE (< 5% do nominal)"
            elif abs(s["dif_absoluta"]) < abs(d_nom):
                v = f"DIMINUI (resta {100*s['dif_absoluta']/d_nom:.0f}%)"
            else:
                v = f"PERMANECE ou cresce ({100*s['dif_absoluta']/d_nom:.0f}%)"
            log(f"      -> sob '{s['configuracao']}': {v}")
            s["veredito"] = v
    pd.DataFrame(saida2).to_csv(DIR_TABELAS / "modelo_07_ablacao_mecanismo.csv",
                                index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # BLOCO 3 — varredura
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("BLOCO 3 — VARREDURA DE p_reporte (demais parametros na centralizada)")
    log("=" * 78)
    escada = ([("centralizada", p_c)]
              + [(f"pr_{p:.4f}", p) for p in niveis[1:-1]]
              + [("so_p_reporte", p_a)])
    saida3 = []
    log(f"\n  {'p_reporte':>10} {'n_com_erro':>11} {'taxa_omis':>10} "
        f"{'TR':>9} {'retr/plano':>11} {'atraso_rel':>11} {'E_total':>9}")
    for b, pr in escada:
        linha = {"braco": b, "p_reporte": pr}
        for m, _ in METRICAS:
            linha[m] = float(np.mean(por_instancia(d, b, m)))
        log(f"  {pr:>10.4f} {linha['n_com_erro']:>11.4f} "
            f"{linha['taxa_omissao']:>10.4f} {linha['TR']:>9.3f} "
            f"{linha['retrabalho_sobre_plano']:>11.4f} "
            f"{linha['atraso_relativo']:>11.4f} {linha['E_total']:>9.4f}")
        saida3.append(linha)
    pd.DataFrame(saida3).to_csv(DIR_TABELAS / "modelo_07_ablacao_p_reporte.csv",
                                index=False, encoding="utf-8")

    # razao mecanica prevista para a taxa de omissao
    prev = (1 - p_a) / (1 - p_c)
    obs = (np.mean(por_instancia(d, "so_p_reporte", "taxa_omissao"))
           / max(1e-12, np.mean(por_instancia(d, "centralizada", "taxa_omissao"))))
    log(f"\n  Razao mecanica prevista so por p_reporte: (1-{p_a})/(1-{p_c}) = {prev:.4f}")
    log(f"  Razao observada com SO p_reporte trocado:                  {obs:.4f}")
    log("  Se as duas coincidem, a taxa de omissao e o parametro reaparecendo na")
    log("  saida — manipulation check, nao achado independente (item B11).")

    log("\n--- Arquivos gerados ---")
    for f in ("bruto", "parametros", "mecanismo", "portas", "p_reporte"):
        log(f"  outputs/tables/modelo_07_ablacao_{f}.csv")
    log("\n" + "=" * 78)
    log("RESULTADO: CONCLUIDO")
    log("=" * 78)
    (DIR_LOGS / "modelo_07_ablacao.log").write_text("\n".join(_log) + "\n",
                                                    encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--listar":
        print("\n".join(preparar()[2]))
    elif len(sys.argv) > 2 and sys.argv[1] == "--rodar":
        for nome in sys.argv[2:]:
            rodar_braco(nome)
    else:
        main()
