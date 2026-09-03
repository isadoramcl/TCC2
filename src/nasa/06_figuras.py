"""
06_figuras.py — Figuras para o documento de entrega
====================================================

ENTRADA : outputs/tables/*.csv (gerados pelos scripts 02, 04 e 05)
SAIDA   : outputs/figures/*.png a 300 dpi

DECISOES DE VISUALIZACAO
------------------------
- Paleta categorica de dois tons apenas (azul #2a78d6 e laranja #eb6834),
  validada para daltonismo. Duas series bastam em todas as figuras; nao ha
  necessidade de cores adicionais e cada cor extra e uma chance de confusao.
- Nenhum grafico usa dois eixos verticais. Quando duas grandezas tem escalas
  diferentes, elas viram figuras separadas.
- Barras finas, grade recessiva, sem bordas superiores e direitas, rotulos
  diretos nos valores. O objetivo e leitura, nao ornamento.
- Intervalos de confianca sempre visiveis onde ha estimativa pontual.
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

plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300,
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": TINTA2, "axes.labelcolor": TINTA,
    "text.color": TINTA, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def limpar(ax, eixo_y=True):
    ax.grid(axis="y" if eixo_y else "x", color=GRADE, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)


# =====================================================================
# FIGURA 1 — arquitetura do pipeline
# =====================================================================
def figura_1_arquitetura():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    def caixa(x, y, w, h, titulo, linhas, cor_borda=TINTA2, preenchimento="white"):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=preenchimento,
                                   edgecolor=cor_borda, linewidth=1.1, zorder=2))
        ax.text(x + w / 2, y + h - 0.30, titulo, ha="center", va="top",
                fontsize=8.2, fontweight="bold", color=TINTA, zorder=3)
        for i, t in enumerate(linhas):
            ax.text(x + w / 2, y + h - 0.68 - i * 0.32, t, ha="center", va="top",
                    fontsize=6.8, color=TINTA2, zorder=3)

    def seta(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=1,
                    arrowprops=dict(arrowstyle="-|>", color=TINTA2, linewidth=1.0,
                                    shrinkA=2, shrinkB=2))

    ax.text(5, 9.72, "Pipeline de dados — calibracao NASA MDP",
            ha="center", fontsize=10.5, fontweight="bold", color=TINTA)

    # Camada 1 — dados brutos imutaveis
    ax.add_patch(plt.Rectangle((0.25, 6.55), 9.5, 2.5, facecolor="#f5f5f2",
                               edgecolor="none", zorder=0))
    ax.text(0.45, 8.86, "data/raw/  — imutavel, versionado, integridade por SHA-256",
            fontsize=7.2, style="italic", color=TINTA2)
    caixa(0.6, 6.85, 2.7, 1.75, "PROMISE", ["cm1, jm1, kc1,", "kc2, pc1", "10 arquivos"], AZUL)
    caixa(3.65, 6.85, 2.7, 1.75, "MDP  D'", ["13 arquivos", "43.770 casos", "referencia"], AZUL)
    caixa(6.7, 6.85, 2.7, 1.75, "MDP  D''", ["13 arquivos", "17.377 casos", "base de analise"], AZUL)

    # Camada 2 — scripts
    caixa(0.6, 4.75, 2.05, 1.3, "01 auditar", ["hashes, formatos,", "pares ARFF/CSV"])
    caixa(2.85, 4.75, 2.05, 1.3, "03 validar", ["D' -> D''", "12/12 conferem"])
    caixa(5.1, 4.75, 2.05, 1.3, "02 consolidar", ["12 projetos", "20 metricas"])
    caixa(7.35, 4.75, 2.05, 1.3, "04 modelar", ["logistica,", "OR, IC, LRT"])
    caixa(3.97, 2.85, 2.05, 1.3, "05 F_base", ["faixas, tendencia,", "sensibilidade"])

    seta(1.95, 6.85, 1.62, 6.05)
    seta(5.0, 6.85, 3.87, 6.05)
    seta(8.05, 6.85, 6.12, 6.05)
    seta(6.12, 4.75, 8.37, 4.75 + 0.65) if False else seta(7.15, 5.40, 7.35, 5.40)
    seta(8.37, 4.75, 5.4, 4.15)

    # Camada 3 — saidas
    caixa(0.6, 0.75, 2.7, 1.5, "outputs/tables", ["14 tabelas .csv"], LARANJA)
    caixa(3.65, 0.75, 2.7, 1.5, "outputs/figures", ["figuras 300 dpi"], LARANJA)
    caixa(6.7, 0.75, 2.7, 1.5, "outputs/logs", ["log de cada execucao"], LARANJA)
    seta(4.6, 2.85, 2.0, 2.25)
    seta(5.0, 2.85, 5.0, 2.25)
    seta(5.4, 2.85, 8.0, 2.25)

    fig.tight_layout()
    fig.savefig(FIG / "fig1_arquitetura_pipeline.png", bbox_inches="tight")
    plt.close(fig)
    print("  fig1_arquitetura_pipeline.png")


# =====================================================================
# FIGURA 2 — F_base por faixa: frequencia bruta x probabilidade ajustada
# =====================================================================
def figura_2_fbase():
    d = pd.read_csv(TAB / "05_faixas_frequencias.csv")
    d = d[d["eixo"] == "CYCLOMATIC_COMPLEXITY"]
    niveis = list(d["nivel"])
    x = np.arange(len(niveis)); largura = 0.34

    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    limpar(ax)

    bruta, ajust = d["frequencia_bruta"].values, d["probabilidade_ajustada"].values
    erro = np.vstack([bruta - d["ic95_inferior"].values, d["ic95_superior"].values - bruta])

    ax.bar(x - largura / 2, bruta, largura, color=AZUL, zorder=3,
           label="Frequencia bruta observada", edgecolor="white", linewidth=1.4)
    ax.errorbar(x - largura / 2, bruta, yerr=erro, fmt="none",
                ecolor=TINTA2, elinewidth=1.0, capsize=3, zorder=4)
    ax.bar(x + largura / 2, ajust, largura, color=LARANJA, zorder=3,
           label="Probabilidade ajustada pelo projeto", edgecolor="white", linewidth=1.4)

    for xi, v in zip(x - largura / 2, bruta):
        ax.text(xi, v + 0.028, f"{v:.3f}", ha="center", fontsize=7.6, color=TINTA)
    for xi, v in zip(x + largura / 2, ajust):
        ax.text(xi, v + 0.012, f"{v:.3f}", ha="center", fontsize=7.6, color=TINTA)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{n}\n{r}" for n, r in zip(
        niveis, ["v(G) ≤ 10", "11–15", "16–20", "> 20"])], fontsize=8)
    ax.set_ylabel("Probabilidade de defeito")
    ax.set_ylim(0, 0.55)
    ax.set_title("Risco basal por faixa de complexidade ciclomatica\n"
                 "12 projetos NASA MDP, versao D'', n = 17.377",
                 fontsize=9.6, fontweight="bold", loc="left")
    ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_fbase_por_faixa.png", bbox_inches="tight")
    plt.close(fig)
    print("  fig2_fbase_por_faixa.png")


# =====================================================================
# FIGURA 3 — a complexidade sobrevive ao controle por tamanho?
# =====================================================================
def figura_3_controle_tamanho():
    cand = pd.read_csv(TAB / "04_metricas_candidatas.csv")
    sobr = pd.read_csv(TAB / "04_sobrevivencia_ao_controle_de_tamanho.csv")

    iso = cand[(cand["escala"] == "log1p") & (cand["ressalva"] != "CIRCULAR")].copy()
    iso["chave"] = "log_" + iso["metrica"]
    juntos = iso.merge(sobr, on=None, left_on="chave", right_on="variavel",
                       suffixes=("_iso", "_aj"))
    juntos = juntos[juntos["metrica"] != "LOC_TOTAL"].sort_values("razao_de_chances")

    nomes = [m.replace("_", " ").replace("COMPLEXITY", "COMPL.").title()
             for m in juntos["metrica"]]
    y = np.arange(len(juntos))

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.grid(axis="x", color=GRADE, linewidth=0.6, zorder=0); ax.set_axisbelow(True)
    ax.axvline(1.0, color=TINTA2, linewidth=1.0, linestyle="--", zorder=1)
    # Anotacao da linha de referencia posicionada DENTRO da area do grafico,
    # no topo: colocada abaixo do eixo ela colidia com o rotulo do tique "1.00".
    ax.text(1.03, len(y) - 0.38, "OR = 1\nsem efeito", fontsize=7.0,
            color=TINTA2, ha="left", va="top", linespacing=1.25)

    desloc = 0.17
    for (yi, r) in zip(y, juntos.itertuples()):
        ax.plot([r.ic95_inferior_iso, r.ic95_superior_iso], [yi + desloc] * 2,
                color=AZUL, linewidth=1.6, zorder=3, solid_capstyle="round")
        ax.plot(r.razao_de_chances, yi + desloc, "o", color=AZUL, markersize=6,
                markeredgecolor="white", markeredgewidth=1.0, zorder=4)
        ax.plot([r.ic95_inferior_aj, r.ic95_superior_aj], [yi - desloc] * 2,
                color=LARANJA, linewidth=1.6, zorder=3, solid_capstyle="round")
        ax.plot(r.or_ajustado, yi - desloc, "o", color=LARANJA, markersize=6,
                markeredgecolor="white", markeredgewidth=1.0, zorder=4)

    ax.set_yticks(y); ax.set_yticklabels(nomes, fontsize=8)
    ax.set_ylim(-0.75, len(y) - 0.25)
    ax.set_xscale("log")
    ax.set_xlim(0.6, 2.6)
    ax.set_xticks([0.7, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # Sem esta linha, a escala log imprime rotulos de tiques menores
    # ("6 x 10^-1") que poluem o eixo.
    ax.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Razao de chances (escala logaritmica) — IC 95%")
    ax.set_title("O efeito da complexidade desaparece ao controlar o tamanho do modulo\n"
                 "cada metrica em escala log(1+x); efeito de projeto sempre no modelo",
                 fontsize=9.4, fontweight="bold", loc="left", pad=26)

    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([0], [0], color=AZUL, marker="o", linewidth=1.6, markersize=6,
               label="Controlando apenas o projeto"),
        Line2D([0], [0], color=LARANJA, marker="o", linewidth=1.6, markersize=6,
               label="Controlando projeto + log(LOC_TOTAL)"),
    ], frameon=False, fontsize=7.6, loc="lower left",
       bbox_to_anchor=(0.0, 1.005), ncol=2)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_controle_por_tamanho.png", bbox_inches="tight")
    plt.close(fig)
    print("  fig3_controle_por_tamanho.png")


# =====================================================================
# FIGURA 4 — estabilidade leave-one-project-out
# =====================================================================
def figura_4_estabilidade():
    d = pd.read_csv(TAB / "05_leave_one_project_out.csv")
    niveis = ["baixa", "media", "alta", "muito alta"]
    colunas = [f"F_base_{n.replace(' ', '_')}" for n in niveis]
    x = np.arange(len(niveis))

    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    limpar(ax)
    for _, linha in d.iterrows():
        ax.plot(x, [linha[c] for c in colunas], color=AZUL, alpha=0.32,
                linewidth=1.0, marker="o", markersize=3.2, zorder=2)
    completo = pd.read_csv(TAB / "05_faixas_frequencias.csv")
    completo = completo[completo["eixo"] == "CYCLOMATIC_COMPLEXITY"]
    ax.plot(x, completo["frequencia_bruta"].values, color=LARANJA, linewidth=2.2,
            marker="o", markersize=7, markeredgecolor="white", markeredgewidth=1.2,
            zorder=5, label="Base completa (12 projetos)")
    for xi, v in zip(x, completo["frequencia_bruta"].values):
        ax.text(xi, v + 0.022, f"{v:.3f}", ha="center", fontsize=7.6,
                color=TINTA, zorder=6)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{n}\n{r}" for n, r in zip(
        niveis, ["v(G) ≤ 10", "11–15", "16–20", "> 20"])], fontsize=8)
    ax.set_ylabel("Frequencia de defeito")
    ax.set_ylim(0, 0.52)
    ax.set_title("Estabilidade da ordenacao: 12 reamostragens leave-one-project-out\n"
                 "cada linha clara retira um projeto; a ordenacao se mantem em 12/12",
                 fontsize=9.6, fontweight="bold", loc="left")
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([0], [0], color=LARANJA, marker="o", linewidth=2.2, markersize=7,
               label="Base completa (12 projetos)"),
        Line2D([0], [0], color=AZUL, alpha=0.45, linewidth=1.0, marker="o",
               markersize=3.2, label="Um projeto retirado (12 curvas)"),
    ], frameon=False, fontsize=7.8, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "fig4_estabilidade_loo.png", bbox_inches="tight")
    plt.close(fig)
    print("  fig4_estabilidade_loo.png")


if __name__ == "__main__":
    print("Gerando figuras em outputs/figures/")
    figura_1_arquitetura()
    figura_2_fbase()
    figura_3_controle_tamanho()
    figura_4_estabilidade()
    print("Concluido.")
