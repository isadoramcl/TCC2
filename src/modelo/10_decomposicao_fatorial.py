"""
10_decomposicao_fatorial.py — Decomposicao EXATA do contraste de governanca
=============================================================================

POR QUE ESTE SCRIPT EXISTE
--------------------------
A B9 rodou ablacoes de um parametro por vez e reportou, para cada uma, a fracao
do contraste nominal que ela reproduzia. Aquilo NAO e uma decomposicao: as
fracoes nao somam 100% (o atraso relativo dava 52,6 + 0,0 + 27,8 + 38,4 = 118,8)
justamente porque os efeitos nao sao aditivos. Descrever aquelas fracoes como
"X% do efeito vem do parametro Y" e atribuicao causal indevida.

`[DEC]` Este script substitui a linguagem por uma medida que de fato decompoe.
Roda o fatorial COMPLETO 2^4 dos quatro parametros organizacionais (16 celulas;
a celula 0000 e a centralizada e a 1111 e a adaptativa) e ajusta, para cada
instancia, o modelo SATURADO

    y = b0 + SUM b_k x_k + SUM b_kl x_k x_l + ... + b_ABCD x_A x_B x_C x_D

com x_k em {0, 1} (0 = valor centralizado, 1 = valor adaptativo). Com 16
parametros e 16 celulas o ajuste e exato — nao ha residuo nem escolha de
modelo — e vale a identidade

    y(1111) - y(0000) = SUM de TODOS os termos, menos b0

que E uma decomposicao aditiva legitima do contraste nominal em efeitos
principais e interacoes de todas as ordens. As parcelas podem ser negativas;
e assim que interacao antagonica se manifesta.

`[LIMITACAO]` A decomposicao e valida nos DOIS niveis testados de cada
parametro. Ela nao diz o que aconteceria em valores intermediarios, e nao
transforma correlacao em causa fora do modelo: e a atribuicao interna a este
simulador, sob estes valores.

`[DEC]` Unidade inferencial: a INSTANCIA. Cada celula entra com a media das 12
sementes; o modelo saturado e ajustado por instancia; reportam-se media e
Wilcoxon pareado sobre as 16 instancias.

SAIDA
-----
  outputs/tables/modelo_10_fatorial_celulas.csv
  outputs/tables/modelo_10_fatorial_decomposicao.csv
  outputs/logs/modelo_10_decomposicao_fatorial.log
"""

import copy
import itertools
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
DIR_PARCIAIS = DIR_TABELAS / "_fatorial_parciais"

N_INSTANCIAS = 16
N_SEMENTES = 12
FATORES = ["tau_inicial", "tau_min", "p_reporte", "p_deteccao"]
SIGLA = {"tau_inicial": "A", "tau_min": "B", "p_reporte": "C", "p_deteccao": "D"}
CELULAS = ["".join(str(b) for b in c)
           for c in itertools.product([0, 1], repeat=len(FATORES))]
METRICAS = ["taxa_falha_efetiva", "atraso_relativo", "E_total", "TL", "TU", "TR", "TW", "n_com_erro",
            "taxa_omissao", "retrabalho_sobre_plano",
            "divida_latente_sobre_plano", "S_UR_maximo"]


def instancias():
    todas = sorted(pd.read_csv(RAIZ / "data" / "processed" / "psplib" /
                               "tarefas_j60_com_di.csv")["arquivo"].unique())
    return todas[::max(1, len(todas) // N_INSTANCIAS)][:N_INSTANCIAS]


def rodar(celula: str) -> None:
    par = S.carregar_parametros()
    c, a = par["cenarios"]["centralizada"], par["cenarios"]["adaptativa"]
    novo = copy.deepcopy(c)
    for bit, f in zip(celula, FATORES):
        if bit == "1":
            novo[f] = copy.deepcopy(a[f])
    par["cenarios"]["celula"] = novo
    linhas = []
    for arq in instancias():
        g, disp, cpm = S.carregar_instancia(arq)
        for sem in range(N_SEMENTES):
            r = S.Simulacao(g, disp, cpm, par, "celula", semente=sem).executar()
            linhas.append({
                "celula": celula, "arquivo": arq, "semente": sem,
                **{SIGLA[f]: int(b) for b, f in zip(celula, FATORES)},
                "atraso_relativo": r.makespan / r.makespan_cpm,
                "retrabalho_sobre_esforco_total": r.retrabalho_sobre_esforco_total, "taxa_falha_efetiva": r.taxa_falha_efetiva,
                "E_total": r.E_total, "TW": r.TW, "TL": r.TL, "TU": r.TU,
                "TR": r.TR, "n_com_erro": r.n_com_erro,
                "taxa_omissao": r.taxa_omissao, "S_UR_maximo": r.S_UR_maximo,
                "retrabalho_sobre_plano": r.retrabalho_sobre_plano,
                "divida_latente_sobre_plano": r.divida_latente_sobre_plano,
                "p2_ajuda": r.contadores["p2_ajuda"],
            })
    DIR_PARCIAIS.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(linhas).to_csv(DIR_PARCIAIS / f"c{celula}.csv", index=False,
                                encoding="utf-8")
    print(f"celula {celula}: {len(linhas)} execucoes")


def termos():
    """Subconjuntos nao vazios de {A,B,C,D}, em ordem de ordem crescente."""
    letras = [SIGLA[f] for f in FATORES]
    saida = []
    for k in range(1, len(letras) + 1):
        saida += ["".join(s) for s in itertools.combinations(letras, k)]
    return saida


def matriz_projeto():
    """Matriz 16x16 do modelo saturado com codificacao 0/1 (dummy)."""
    letras = [SIGLA[f] for f in FATORES]
    cols = ["intercepto"] + termos()
    M = np.zeros((len(CELULAS), len(cols)))
    for i, cel in enumerate(CELULAS):
        x = dict(zip(letras, [int(b) for b in cel]))
        for j, t in enumerate(cols):
            M[i, j] = 1.0 if t == "intercepto" else float(
                np.prod([x[l] for l in t]))
    return M, cols


def analisar() -> None:
    _log = []

    def log(m=""):
        print(m)
        _log.append(m)

    faltando = [c for c in CELULAS if not (DIR_PARCIAIS / f"c{c}.csv").exists()]
    if faltando:
        raise SystemExit(f"faltam rodar as celulas: {faltando}")
    d = pd.concat([pd.read_csv(DIR_PARCIAIS / f"c{c}.csv") for c in CELULAS],
                  ignore_index=True)
    d["celula"] = d["celula"].astype(str).str.zfill(len(FATORES))
    d.to_csv(DIR_TABELAS / "modelo_10_fatorial_celulas.csv", index=False,
             encoding="utf-8")

    log("=" * 78)
    log("DECOMPOSICAO FATORIAL 2^4 DO CONTRASTE DE GOVERNANCA")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)
    log(f"\nFatores: " + ", ".join(f"{SIGLA[f]} = {f}" for f in FATORES))
    log(f"Celulas: {len(CELULAS)}   Instancias: {d['arquivo'].nunique()}   "
        f"Sementes: {d['semente'].nunique()}   Execucoes: {len(d)}")
    log("Codificacao: 0 = valor da centralizada, 1 = valor da adaptativa.")
    log("0000 = centralizada nominal; 1111 = adaptativa nominal.")

    M, cols = matriz_projeto()
    Minv = np.linalg.inv(M)
    log(f"\nModelo saturado: {M.shape[1]} termos para {M.shape[0]} celulas — "
        f"ajuste exato (numero de condicao {np.linalg.cond(M):.1f}).")

    # ---- B e inerte? teste explicito -------------------------------------
    log("\n" + "-" * 78)
    log("TESTE PREVIO — o fator B (tau_min) tem algum efeito no fatorial?")
    log("-" * 78)
    pares = [(c, c[0] + ("1" if c[1] == "0" else "0") + c[2:]) for c in CELULAS
             if c[1] == "0"]
    inertes = []
    for c0, c1 in pares:
        x = d[d.celula == c0].set_index(["arquivo", "semente"]).sort_index()
        y = d[d.celula == c1].set_index(["arquivo", "semente"]).sort_index()
        ig = x[METRICAS].round(9).equals(y[METRICAS].round(9))
        inertes.append(ig)
        log(f"  {c0} vs {c1}: {'IDENTICAS linha a linha' if ig else 'DIFEREM'}")
    if all(inertes):
        log("\n  B (tau_min) e INERTE em todas as 8 comparacoes. Consequencia:")
        log("  todo termo do modelo saturado que contenha B e exatamente zero, e")
        log("  o fatorial 2^4 colapsa num 2^3 replicado. Isso NAO e propriedade")
        log("  do parametro: e consequencia de tau ser constante e igual para")
        log("  todos os agentes (item C3), de modo que o portao `confianca >")
        log("  tau_min` so compara tau_inicial com tau_min — e os dois niveis")
        log("  testados de tau_min (0,60 e 0,25) caem do mesmo lado dos dois")
        log("  niveis testados de tau_inicial (0,25 e 0,80).")

    # ---- decomposicao por metrica ---------------------------------------
    saida = []
    for m in METRICAS:
        # media por (celula, instancia); depois solve por instancia
        tab = (d.groupby(["celula", "arquivo"])[m].mean().unstack("arquivo")
               .reindex(CELULAS))
        B = Minv @ tab.values                      # (16 termos) x (16 instancias)
        nomes = cols
        contraste = tab.loc["1111"].values - tab.loc["0000"].values
        soma = B[1:].sum(axis=0)
        erro = float(np.max(np.abs(soma - contraste)))
        log("\n" + "=" * 78)
        log(f"{m}")
        log(f"  centralizada (0000) = {tab.loc['0000'].mean():.4f}    "
            f"adaptativa (1111) = {tab.loc['1111'].mean():.4f}")
        log(f"  contraste nominal   = {contraste.mean():+.4f}")
        log(f"  soma das parcelas   = {soma.mean():+.4f}   "
            f"(erro maximo por instancia: {erro:.2e})")
        assert erro < 1e-8, "a identidade da decomposicao falhou"
        log(f"\n  {'termo':<8} {'parcela':>12} {'% do contraste':>15} "
            f"{'p (Wilcoxon)':>13}")
        for j, nome in enumerate(nomes):
            if nome == "intercepto":
                continue
            v = B[j]
            if np.allclose(v, 0):
                pv = np.nan
            else:
                pv = float(stats.wilcoxon(v)[1])
            pct = (100 * v.mean() / contraste.mean()
                   if abs(contraste.mean()) > 1e-12 else np.nan)
            if abs(v.mean()) > 1e-9:
                log(f"  {nome:<8} {v.mean():>+12.4f} {pct:>14.1f}% {pv:>13.2e}")
            saida.append({"metrica": m, "termo": nome, "ordem": len(nome),
                          "parcela_media": float(v.mean()),
                          "pct_do_contraste": float(pct) if pct == pct else np.nan,
                          "p_valor": pv, "n_instancias": int(len(v))})
        principais = sum(B[j].mean() for j, n in enumerate(nomes)
                         if n != "intercepto" and len(n) == 1)
        interacoes = sum(B[j].mean() for j, n in enumerate(nomes)
                         if n != "intercepto" and len(n) > 1)
        log(f"\n  efeitos principais somados : {principais:>+10.4f} "
            f"({100*principais/contraste.mean():>6.1f}% do contraste)")
        log(f"  interacoes somadas         : {interacoes:>+10.4f} "
            f"({100*interacoes/contraste.mean():>6.1f}% do contraste)")
        saida.append({"metrica": m, "termo": "SOMA_principais", "ordem": 0,
                      "parcela_media": float(principais),
                      "pct_do_contraste": float(100*principais/contraste.mean()),
                      "p_valor": np.nan, "n_instancias": int(len(contraste))})
        saida.append({"metrica": m, "termo": "SOMA_interacoes", "ordem": 0,
                      "parcela_media": float(interacoes),
                      "pct_do_contraste": float(100*interacoes/contraste.mean()),
                      "p_valor": np.nan, "n_instancias": int(len(contraste))})

    pd.DataFrame(saida).to_csv(DIR_TABELAS / "modelo_10_fatorial_decomposicao.csv",
                               index=False, encoding="utf-8")
    log("\n--- Arquivos gerados ---")
    log("  outputs/tables/modelo_10_fatorial_celulas.csv")
    log("  outputs/tables/modelo_10_fatorial_decomposicao.csv")
    (DIR_LOGS / "modelo_10_decomposicao_fatorial.log").write_text(
        "\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--rodar":
        for c in sys.argv[2:]:
            rodar(c)
    elif len(sys.argv) > 1 and sys.argv[1] == "--listar":
        print(" ".join(CELULAS))
    else:
        analisar()
