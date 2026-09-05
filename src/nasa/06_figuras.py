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
    """
    Arquitetura completa do pipeline: os dois ramos e sua convergencia.

    A figura anterior mostrava apenas o ramo NASA. Com o ramo PSPLIB
    implementado, uma arquitetura que o omitisse descreveria um sistema que nao
    e mais o sistema construido.
    """
    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    def caixa(x, y, w, h, titulo, linhas, cor=TINTA2, fundo="white", tam=8.0):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fundo, edgecolor=cor,
                                   linewidth=1.1, zorder=2))
        ax.text(x + w / 2, y + h - 0.26, titulo, ha="center", va="top",
                fontsize=tam, fontweight="bold", color=TINTA, zorder=3)
        for i, t in enumerate(linhas):
            ax.text(x + w / 2, y + h - 0.60 - i * 0.29, t, ha="center", va="top",
                    fontsize=6.5, color=TINTA2, zorder=3)

    def seta(x1, y1, x2, y2, cor=TINTA2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=1,
                    arrowprops=dict(arrowstyle="-|>", color=cor, linewidth=1.0,
                                    shrinkA=2, shrinkB=2))

    ax.text(5, 9.78, "Arquitetura do pipeline — calibração NASA e transferência para o PSPLIB J60",
            ha="center", fontsize=10.0, fontweight="bold", color=TINTA)

    # --- camada de dados brutos ---
    ax.add_patch(plt.Rectangle((0.2, 7.55), 9.6, 1.85, facecolor="#f5f5f2",
                               edgecolor="none", zorder=0))
    ax.text(0.38, 9.26, "data/raw/  — imutável, versionado, integridade por SHA-256",
            fontsize=6.9, style="italic", color=TINTA2)

    caixa(0.45, 7.75, 2.0, 1.28, "PROMISE", ["5 conjuntos", "10 arquivos"], AZUL)
    caixa(2.65, 7.75, 2.0, 1.28, "MDP  D'", ["13 arquivos", "43.770 casos"], AZUL)
    caixa(4.85, 7.75, 2.0, 1.28, "MDP  D''", ["13 arquivos", "17.377 casos"], AZUL)
    caixa(7.35, 7.75, 2.2, 1.28, "PSPLIB J60", ["480 instâncias", "28.800 tarefas"], LARANJA)

    # --- ramo NASA ---
    ax.text(0.45, 7.22, "ramo NASA  —  calibração do risco basal",
            fontsize=7.4, fontweight="bold", color=AZUL)
    caixa(0.45, 5.75, 1.85, 1.15, "01 auditar", ["hashes, pares", "ARFF/CSV"])
    caixa(2.45, 5.75, 1.85, 1.15, "03 validar", ["D' → D''", "12/12"])
    caixa(4.45, 5.75, 1.85, 1.15, "02 consolidar", ["12 projetos", "20 métricas"])
    caixa(0.45, 4.15, 1.85, 1.15, "04 modelar", ["logística, RC,", "IC, VIF"])
    caixa(2.45, 4.15, 1.85, 1.15, "05 F_base", ["faixas, tendência,", "sensibilidade"])

    seta(1.40, 7.75, 1.38, 6.90)
    seta(3.60, 7.75, 3.38, 6.90)
    seta(5.85, 7.75, 5.38, 6.90)
    seta(5.38, 5.75, 1.90, 5.30)
    seta(2.30, 4.72, 2.45, 4.72)

    # --- ramo PSPLIB ---
    ax.text(6.55, 7.22, "ramo PSPLIB  —  dificuldade da tarefa",
            fontsize=7.4, fontweight="bold", color=LARANJA)
    caixa(6.55, 5.75, 1.5, 1.15, "01 auditar", ["NC, RF, RS", "3×4×4"], LARANJA)
    caixa(8.15, 5.75, 1.4, 1.15, "02 Di", ["CPM, folga,", "4 níveis"], LARANJA)
    seta(8.45, 7.75, 7.30, 6.90)
    seta(8.05, 6.32, 8.15, 6.32)

    # --- convergencia ---
    caixa(3.35, 2.35, 3.30, 1.30,
          "03  transferência ordinal",
          ["razão de risco NASA → J60", "bootstrap por projeto, IC 95%"],
          "#4a3aa7", "#f4f3fb", tam=8.6)
    seta(3.38, 4.15, 4.40, 3.65, AZUL)
    seta(8.60, 5.75, 5.90, 3.65, LARANJA)

    # --- saidas ---
    caixa(0.45, 0.45, 2.6, 1.15, "outputs/tables", ["23 tabelas .csv"], LARANJA)
    caixa(3.45, 0.45, 3.1, 1.15, "tarefas_j60_com_risco", ["28.800 multiplicadores", "com intervalo"], LARANJA)
    caixa(6.95, 0.45, 2.6, 1.15, "figuras e logs", ["300 dpi + rastro"], LARANJA)
    seta(4.40, 2.35, 2.10, 1.60)
    seta(5.00, 2.35, 5.00, 1.60)
    seta(5.60, 2.35, 8.00, 1.60)

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
