"""
05_figuras_modelo.py — Figuras do experimento de governanca
============================================================

ENTRADA : outputs/tables/modelo_03_experimento_bruto.csv
SAIDA   : outputs/figures/fig7_efeitos_pareados.png
          outputs/figures/fig8_decomposicao_esforco.png
          outputs/figures/fig9_trajetorias.png

Mesmas convencoes de src/nasa/06_figuras.py e src/psplib/04_figuras.py:
paleta de dois tons validada para daltonismo, sem eixo duplo, grade
recessiva, intervalo de confianca sempre visivel onde ha estimativa pontual.

`[DEC]` A fig7 usa o d de Cohen pareado com IC de 95% obtido por bootstrap
sobre os PARES (4000 replicas), e nao o valor-p. Com 192 pares, o valor-p
nao distingue diferenca relevante de diferenca meramente detectavel; o
tamanho de efeito com incerteza distingue.

`[DEC]` A metrica de diagnostico `retrabalho_sobre_esforco_realizado` aparece
na fig7 em tom neutro e explicitamente rotulada, para que o leitor veja que
ela move em sentido contrario e por que (ACHADO 6).
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
TAB = RAIZ / "outputs" / "tables"
FIG = RAIZ / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

AZUL, LARANJA = "#2a78d6", "#eb6834"
TINTA, TINTA2, GRADE = "#0b0b0b", "#52514e", "#dcdcd8"
NEUTRO = "#9a9a96"

plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300,
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": TINTA2, "axes.labelcolor": TINTA,
    "text.color": TINTA, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})

N_BOOT = 4000
SEMENTE = 20260905

ROTULOS = {
    "E_total": "diagnóstico interno\n$E_{total}$",
    "atraso_relativo": "atraso relativo\n(makespan / CPM)",
    "n_com_erro": "tarefas concluídas\ncom defeito",
    "taxa_omissao": "taxa de omissão",
    "taxa_falha_efetiva": "taxa de falha efetiva",
    "divida_latente_sobre_plano": "dívida latente de pico\n(/ esforço planejado)",
    "retrabalho_sobre_plano": "retrabalho pago\n(/ esforço planejado)",
    "retrabalho_sobre_esforco_realizado":
        "retrabalho / esforço realizado\n(diagnóstico; excluído de z — parecer 22)",
}
ORDEM = ["taxa_falha_efetiva", "n_com_erro", "taxa_omissao", "divida_latente_sobre_plano",
         "atraso_relativo", "E_total", "retrabalho_sobre_plano",
         "retrabalho_sobre_esforco_realizado"]
DIAGNOSTICO = "retrabalho_sobre_esforco_realizado"


def carregar():
    d = pd.read_csv(TAB / "modelo_03_experimento_bruto.csv")
    if 'retrabalho_sobre_esforco_total' not in d and 'E_plano' in d:
        d['retrabalho_sobre_esforco_total']=d.TR/(d.E_plano+d.TR)
    if 'taxa_falha_efetiva' not in d:
        # Derivação em memória de artefato histórico; nunca sobrescrever o bruto.
        tarefas = pd.read_csv(RAIZ/'data/processed/psplib/tarefas_j60_com_di.csv')
        n = d.arquivo.map(tarefas.groupby('arquivo').tarefa.nunique())
        if n.isna().any() or (n<=0).any(): raise ValueError('denominador de tarefas ausente')
        d['taxa_falha_efetiva'] = (d.n_com_erro+d.n_reportadas)/n
    piv = d.pivot_table(index=["arquivo", "semente"], columns="cenario",
                        values=ORDEM)
    return d, piv


def d_cohen_ic(dif, rng):
    """d de Cohen pareado com IC bootstrap percentil sobre os pares."""
    s = np.std(dif, ddof=1)
    if s == 0:
        return 0.0, 0.0, 0.0
    ponto = float(np.mean(dif) / s)
    n = len(dif)
    reps = np.empty(N_BOOT)
    for b in range(N_BOOT):
        am = dif[rng.integers(0, n, n)]
        sb = np.std(am, ddof=1)
        reps[b] = np.mean(am) / sb if sb > 0 else 0.0
    return ponto, float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))


# =====================================================================
def figura_7(piv):
    """Floresta de tamanhos de efeito pareados, com IC bootstrap."""
    rng = np.random.default_rng(SEMENTE)
    linhas = []
    for m in ORDEM:
        dif = (piv[(m, "adaptativa")] - piv[(m, "centralizada")]).values
        # orienta o eixo: valor negativo = adaptativo melhor, para toda metrica
        sinal = -1.0 if m == "E_total" else 1.0
        p, lo, hi = d_cohen_ic(sinal * dif, rng)
        linhas.append((m, p, lo, hi))

    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    y = np.arange(len(linhas))[::-1]
    ax.grid(axis="x", color=GRADE, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.axvline(0.0, color=TINTA2, linewidth=1.0, linestyle="--", zorder=1)

    for yi, (m, p, lo, hi) in zip(y, linhas):
        diag = (m == DIAGNOSTICO)
        cor = NEUTRO if diag else (AZUL if p < 0 else LARANJA)
        ax.plot([lo, hi], [yi, yi], color=cor, linewidth=2.0,
                solid_capstyle="round", zorder=3)
        ax.plot([p], [yi], "o", color=cor, markersize=6.5,
                markeredgecolor="white", markeredgewidth=1.0, zorder=4)
        ax.annotate(f"{p:+.2f}", (p, yi), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=7.4, color=cor)

    ax.set_yticks(y)
    ax.set_yticklabels([ROTULOS[m] for m, *_ in linhas], fontsize=7.8,
                       linespacing=1.3)
    for tick, (m, *_) in zip(ax.get_yticklabels(), linhas):
        if m == DIAGNOSTICO:
            tick.set_color(NEUTRO)
    ax.set_xlabel("d de Cohen pareado — orientado de modo que valores negativos\n"
                  "indicam vantagem do arranjo adaptativo", fontsize=8.2,
                  linespacing=1.35)
    ax.set_title("Efeito do arranjo de governança sobre o desempenho do projeto",
                 fontsize=10.2, pad=40, loc="left")
    ax.text(0, 1.020, "192 pares (16 instâncias J60 × 12 sementes); "
                      "mesma instância e mesma semente nos dois braços.\n"
                      "Barras: IC 95% por bootstrap sobre os pares "
                      f"({N_BOOT} réplicas).",
            transform=ax.transAxes, fontsize=7.4, color=TINTA2,
            va="bottom", linespacing=1.35)
    ax.set_ylim(-0.55, len(linhas) - 0.4)
    fig.tight_layout()
    fig.savefig(FIG / "fig7_efeitos_pareados.png", bbox_inches="tight")
    plt.close(fig)
    return linhas


# =====================================================================
def figura_8(d):
    """Decomposicao do esforco: mostra o artefato do denominador."""
    comp = ["TW", "TL", "TU", "TR"]
    nomes = ["trabalho produtivo", "aprendizado", "ocioso / bloqueado",
             "retrabalho"]
    cores = [AZUL, "#8fbdf0", NEUTRO, LARANJA]
    g = d.groupby("cenario")[comp].mean()
    ordem = ["centralizada", "adaptativa"]
    plano = d.groupby("cenario")["E_plano"].mean()

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.9),
                                  gridspec_kw={"width_ratios": [1.35, 1]})

    # --- painel A: composicao absoluta ---
    ax.grid(axis="y", color=GRADE, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    base = np.zeros(len(ordem))
    x = np.arange(len(ordem))
    for c, nome, cor in zip(comp, nomes, cores):
        v = g.loc[ordem, c].values
        ax.bar(x, v, 0.5, bottom=base, color=cor, zorder=3,
               label=nome, edgecolor="white", linewidth=0.6)
        for xi, (b, vi) in enumerate(zip(base, v)):
            if vi > 25:
                ax.text(xi, b + vi / 2, f"{vi:.0f}", ha="center", va="center",
                        fontsize=7.2, color="white" if cor != NEUTRO else TINTA)
        base = base + v
    for xi, tot in zip(x, base):
        ax.text(xi, tot + 14, f"total {tot:.0f}", ha="center", fontsize=7.6,
                color=TINTA)
    ax.axhline(plano.mean(), color=TINTA, linewidth=1.0, linestyle=":", zorder=4)
    ax.text(1.42, plano.mean(), "esforço\nplanejado", fontsize=7.0, color=TINTA,
            va="center", ha="left", linespacing=1.25)
    ax.set_xticks(x)
    ax.set_xticklabels(["centralizada", "adaptativa"], fontsize=8.4)
    ax.set_ylabel("períodos-agente (média por execução)", fontsize=8.2)
    ax.set_ylim(0, base.max() * 1.20)
    ax.set_xlim(-0.55, 1.9)
    ax.legend(fontsize=7.0, frameon=False, loc="upper right",
              bbox_to_anchor=(1.02, 1.02), handlelength=1.1, labelspacing=0.35)
    ax.set_title("A. composição do esforço realizado", fontsize=9.0, loc="left",
                 pad=8)

    # --- painel B: a mesma quantidade sob duas bases ---
    ax2.grid(axis="y", color=GRADE, linewidth=0.6, zorder=0)
    ax2.set_axisbelow(True)
    r_plano = (g.loc[ordem, "TR"] / plano.loc[ordem]).values
    r_real = (g.loc[ordem, "TR"] / g.loc[ordem, comp].sum(axis=1)).values
    larg = 0.32
    xo, xc = x - larg / 2 - 0.02, x + larg / 2 + 0.02
    ax2.bar(xo, r_plano, larg, color=LARANJA, zorder=3,
            label="/ esforço planejado")
    ax2.bar(xc, r_real, larg, color=NEUTRO, zorder=3,
            label="/ esforço realizado")
    for xi, v in zip(xo, r_plano):
        ax2.text(xi, v + 0.006, f"{v:.3f}".replace(".", ","), ha="center",
                 fontsize=7.2, color=LARANJA)
    for xi, v in zip(xc, r_real):
        ax2.text(xi, v + 0.006, f"{v:.3f}".replace(".", ","), ha="center",
                 fontsize=7.2, color=TINTA2)

    topo = r_plano.max() * 1.62
    # setas de variacao, desenhadas acima das barras para nao colidir
    y_lar, y_cin = topo * 0.80, topo * 0.62
    ax2.annotate("", xy=(xo[1], y_lar), xytext=(xo[0], y_lar),
                 arrowprops=dict(arrowstyle="->", color=LARANJA, linewidth=1.3))
    # `[A3]` Estes percentuais estavam ESCRITOS A MAO e ficaram vencidos apos a
    # troca da t-norma difusa: diziam 30% / 118,2 vs 6,3 / +8,1% quando os
    # valores corretos ja eram outros. Passam a ser calculados do CSV.
    var_plano = 100 * (r_plano[1] / r_plano[0] - 1)
    var_real = 100 * (r_real[1] / r_real[0] - 1)
    ax2.text((xo[0] + xo[1]) / 2, y_lar + topo * 0.022,
             f"{var_plano:+.1f}%".replace(".", ","), ha="center",
             va="bottom", fontsize=7.8, color=LARANJA)
    ax2.annotate("", xy=(xc[1], y_cin), xytext=(xc[0], y_cin),
                 arrowprops=dict(arrowstyle="->", color=TINTA2, linewidth=1.3))
    ax2.text((xc[0] + xc[1]) / 2, y_cin + topo * 0.022,
             f"{var_real:+.1f}%".replace(".", ","), ha="center",
             va="bottom", fontsize=7.8, color=TINTA2)

    ax2.set_xticks(x)
    ax2.set_xticklabels(["centralizada", "adaptativa"], fontsize=8.4)
    ax2.set_ylabel("retrabalho como fração da base", fontsize=8.2)
    ax2.set_ylim(0, topo)
    ax2.set_xlim(-0.55, 1.55)
    ax2.set_title("B. o mesmo retrabalho sob duas bases", fontsize=9.0,
                  loc="left", pad=8)
    ax2.legend(fontsize=7.0, frameon=False, loc="upper left",
               handlelength=1.1, labelspacing=0.35, borderaxespad=0.2)

    fig.suptitle("Por que a razão sobre o esforço realizado inverte o sinal",
                 fontsize=10.2, x=0.005, ha="left", y=1.035)
    var_total = 100 * (base[0] / base[1] - 1)          # centralizada sobre adaptativa
    var_tr = 100 * (g.loc[ordem[0], "TR"] / g.loc[ordem[1], "TR"] - 1)
    tu_c, tu_a = g.loc[ordem[0], "TU"], g.loc[ordem[1], "TU"]
    fig.text(0.005, 0.975,
             f"O braço centralizado gasta {var_total:.1f}% mais esforço total, "
             f"quase todo improdutivo (ocioso {tu_c:.1f} contra {tu_a:.1f}). "
             f"Isso infla o denominador\ne dilui o retrabalho — que "
             f"em termos absolutos é {var_tr:.1f}% maior.".replace(".", ","),
             fontsize=7.4, color=TINTA2, ha="left", va="top", linespacing=1.35)
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    fig.savefig(FIG / "fig8_decomposicao_esforco.png", bbox_inches="tight")
    plt.close(fig)


# =====================================================================
def figura_9():
    """Trajetorias medias dos estoques nos dois cenarios."""
    sys.path.insert(0, str(RAIZ / "src" / "modelo"))
    import simulador as S

    par = S.carregar_parametros()
    todas = sorted(pd.read_csv(RAIZ / "data" / "processed" / "psplib" /
                               "tarefas_j60_com_di.csv")["arquivo"].unique())
    inst = todas[::len(todas) // 8][:8]

    desfechos = []
    series = {c: {k: [] for k in ("S_UR", "bateria_media", "P", "S_PV")}
              for c in ("centralizada", "adaptativa")}
    for arq in inst:
        g, disp, cpm = S.carregar_instancia(arq)
        for sem in range(6):
            for cen in ("centralizada", "adaptativa"):
                r = S.Simulacao(g, disp, cpm, par, cen, semente=sem).executar()
                desfechos.append(dict(arquivo=arq,semente=sem,cenario=cen,
                    retrabalho_sobre_esforco_total=r.retrabalho_sobre_esforco_total,taxa_falha_efetiva=r.taxa_falha_efetiva,concluiu=r.concluiu))
                plano = float(r.E_plano)
                tn = np.array(r.trajetorias["t"]) / r.makespan_cpm
                for k in series[cen]:
                    v = np.array(r.trajetorias[k], dtype=float)
                    if k in ("S_UR", "S_PV"):
                        v = v / plano
                    series[cen][k].append((tn, v))

    pd.DataFrame(desfechos).to_csv(TAB/'modelo_05_desfechos.csv',index=False)

    def media_em_malha(pares, malha):
        acc = []
        for tn, v in pares:
            if len(tn) < 2:
                continue
            acc.append(np.interp(malha, tn, v, left=v[0], right=v[-1]))
        return (np.mean(acc, axis=0), np.percentile(acc, 25, axis=0),
                np.percentile(acc, 75, axis=0))

    malha = np.linspace(0, 3.2, 240)
    paineis = [("S_UR", "dívida técnica latente\n(fração do esforço planejado)"),
               ("bateria_media", "bateria cognitiva média $B(t)$"),
               ("P", "pressão $P(t)$"),
               ("S_PV", "progresso validado\n(fração do esforço planejado)")]

    fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.2))
    for ax, (k, rot) in zip(axs.ravel(), paineis):
        ax.grid(color=GRADE, linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        for cen, cor, nome in (("centralizada", LARANJA, "centralizada"),
                               ("adaptativa", AZUL, "adaptativa")):
            m, q1, q3 = media_em_malha(series[cen][k], malha)
            ax.fill_between(malha, q1, q3, color=cor, alpha=0.16, zorder=2,
                            linewidth=0)
            ax.plot(malha, m, color=cor, linewidth=1.7, zorder=3, label=nome)
        ax.axvline(1.0, color=TINTA2, linewidth=0.9, linestyle="--", zorder=1)
        ax.set_ylabel(rot, fontsize=7.8, linespacing=1.3)
        ax.set_xlabel("tempo / makespan do CPM", fontsize=7.8)
        ax.tick_params(labelsize=7.4)
    axs[0, 0].legend(fontsize=7.4, frameon=False, loc="upper left",
                     handlelength=1.3)
    fig.suptitle("Trajetórias médias dos estoques nos dois arranjos de governança",
                 fontsize=10.2, x=0.005, ha="left", y=1.025)
    fig.text(0.005, 0.972, "8 instâncias × 6 sementes por braço. Linha: média; "
                           "faixa: quartis 1 e 3.\nTempo normalizado pelo prazo do CPM da "
                           "instância; a linha tracejada vertical marca esse prazo.",
             fontsize=7.4, color=TINTA2, ha="left", va="top")
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    fig.savefig(FIG / "fig9_trajetorias.png", bbox_inches="tight")
    plt.close(fig)


def main():
    d, piv = carregar()
    linhas = figura_7(piv)
    figura_8(d)
    figura_9()
    figura_10()
    print("=" * 74)
    print("FIGURAS DO EXPERIMENTO")
    print("=" * 74)
    print(f"\n  {'metrica':<38} {'d':>7} {'IC 95% bootstrap':>22}")
    for m, p, lo, hi in linhas:
        print(f"  {m:<38} {p:>7.3f}   [{lo:>7.3f}; {hi:>7.3f}]")
    print("\n  Orientacao: negativo = vantagem do arranjo adaptativo.")
    print("\n--- Arquivos gerados ---")
    for f in ("fig7_efeitos_pareados.png", "fig8_decomposicao_esforco.png",
              "fig9_trajetorias.png", "fig10_nroy_identificabilidade.png"):
        print(f"  outputs/figures/{f}")



def figura_10():
    """NROY do History Matching: a crista e a identificabilidade."""
    d = pd.read_csv(TAB / "modelo_04_hm_onda2.csv")
    ident = pd.read_csv(TAB / "modelo_04_identificabilidade.csv")
    ident = ident[ident["onda"] == "onda2"]
    CORTE = 3.0
    nroy = d[d["implausibilidade"] <= CORTE]
    fora = d[d["implausibilidade"] > CORTE]
    # `[A2]` vetor verdadeiro lido da tabela de identificabilidade
    VF = float(ident[ident["parametro"] == "risco.F_ancora"]["verdade"].iloc[0])
    VR = float(ident[ident["parametro"] == "retrabalho.f_retrabalho"]["verdade"].iloc[0])

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.9),
                                  gridspec_kw={"width_ratios": [1.15, 1]})

    # --- painel A: a crista ---
    ax.grid(color=GRADE, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.scatter(fora["risco.F_ancora"], fora["retrabalho.f_retrabalho"],
               s=9, color=GRADE, zorder=2, label="descartado (I > 3)")
    ax.scatter(nroy["risco.F_ancora"], nroy["retrabalho.f_retrabalho"],
               s=13, color=AZUL, zorder=3, label="NROY (I ≤ 3)")
    # hiperbole de produto constante passando pelo vetor verdadeiro
    xx = np.linspace(0.05, 0.25, 300)
    yy = (VF * VR) / xx
    m = (yy >= 0.30) & (yy <= 0.80)
    ax.plot(xx[m], yy[m], color=LARANJA, linewidth=1.6, zorder=4,
            label="produto constante")
    ax.plot([VF], [VR], "*", color=LARANJA, markersize=15, zorder=5,
            markeredgecolor="white", markeredgewidth=0.8, label="vetor verdadeiro")
    ax.set_xlabel("$F_{âncora}$  (frequência de defeito)", fontsize=8.4)
    ax.set_ylabel("$f_{retrabalho}$  (severidade)", fontsize=8.4)
    ax.set_xlim(0.05, 0.25); ax.set_ylim(0.30, 0.80)
    ax.legend(fontsize=6.9, frameon=False, loc="upper right", handlelength=1.2,
              labelspacing=0.3, borderaxespad=0.2)
    rho = nroy[["risco.F_ancora", "retrabalho.f_retrabalho"]].corr(
        method="spearman").iloc[0, 1]
    ax.set_title(f"A. crista de equifinalidade  (ρ = {rho:+.2f})".replace(".", ","),
                 fontsize=9.0, loc="left", pad=8)

    # --- painel B: reducao marginal ---
    rot = {"risco.F_ancora": "$F_{âncora}$",
           "retrabalho.f_retrabalho": "$f_{retrabalho}$",
           "agentes.tau_sat": r"$\tau_{sat}$",
           "agentes.k_heuristico": "$k_{heurístico}$",
           "fuzzy.mu_minimo": r"$\mu_{mín}$"}
    linhas = [(rot[r.parametro], r.reducao) for r in ident.itertuples()]
    # `[A2]` A reducao do produto e a correlacao vinham FIXAS no codigo.
    # Passam a ser calculadas do proprio NROY, como todo o resto.
    prod = nroy["risco.F_ancora"] * nroy["retrabalho.f_retrabalho"]
    red_prod = 1 - (prod.max() - prod.min()) / (0.25 * 0.80 - 0.05 * 0.30)
    linhas.append(("$F_{âncora}\\times f_{retrabalho}$", float(red_prod)))
    linhas.sort(key=lambda t: t[1])
    y = np.arange(len(linhas))
    cores = [LARANJA if v < 0.25 else (AZUL if v >= 0.50 else "#8fbdf0")
             for _, v in linhas]
    ax2.grid(axis="x", color=GRADE, linewidth=0.6, zorder=0)
    ax2.set_axisbelow(True)
    ax2.barh(y, [v for _, v in linhas], 0.6, color=cores, zorder=3)
    for yi, (_, v) in zip(y, linhas):
        ax2.text(v + 0.015, yi, f"{v:.0%}", va="center", fontsize=7.4,
                 color=TINTA2)
    ax2.axvline(0.25, color=TINTA2, linewidth=1.0, linestyle="--", zorder=4)
    ax2.axvline(0.50, color=TINTA2, linewidth=1.0, linestyle=":", zorder=4)
    ax2.set_yticks(y)
    ax2.set_yticklabels([n for n, _ in linhas], fontsize=8.2)
    ax2.set_xlabel("redução da largura marginal do NROY", fontsize=8.4)
    ax2.set_xlim(0, 1.0)
    ax2.set_title("B. identificabilidade", fontsize=9.0, loc="left", pad=8)
    ax2.text(0.265, 1.0, "não identificado\nà esquerda de 25%",
             fontsize=6.8, color=TINTA2, va="center", linespacing=1.3)
    ax2.text(0.515, 3.0, "identificado\nà direita de 50%",
             fontsize=6.8, color=TINTA2, va="center", linespacing=1.3)

    fig.suptitle("Calibração por History Matching — o que os dados determinam",
                 fontsize=10.2, x=0.005, ha="left", y=1.045)
    fig.text(0.005, 0.982, "400 pontos da onda 2; corte de implausibilidade 3 "
                           "(Pukelsheim, 1994). O NROY contém o vetor verdadeiro "
                           "em todos os cinco parâmetros.\nA divisão entre "
                           "frequência e severidade não é identificável — só o "
                           "produto é.",
             fontsize=7.4, color=TINTA2, ha="left", va="top", linespacing=1.35)
    fig.tight_layout(rect=[0, 0, 1, 0.935])
    fig.savefig(FIG / "fig10_nroy_identificabilidade.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()


# =====================================================================