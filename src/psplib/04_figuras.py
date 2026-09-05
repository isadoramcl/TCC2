"""
04_figuras.py — Figuras do bloco PSPLIB J60 para o documento de entrega
========================================================================

ENTRADA : outputs/tables/psplib_*.csv
SAIDA   : outputs/figures/fig5_*.png, fig6_*.png a 300 dpi

Segue as mesmas convencoes do src/nasa/06_figuras.py: paleta de dois tons
validada para daltonismo, sem eixo duplo, barras finas, grade recessiva,
intervalos de confianca sempre visiveis onde ha estimativa pontual.
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

NIVEIS = ["baixa", "media", "alta", "muito alta"]
ROTULOS = ["baixa", "média", "alta", "muito alta"]


def figura_5_gradiente():
    """Razoes de risco transferidas, com intervalo bootstrap."""
    d = pd.read_csv(TAB / "psplib_03_razoes_de_risco.csv")
    x = np.arange(len(d))

    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.grid(axis="y", color=GRADE, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.axhline(1.0, color=TINTA2, linewidth=1.0, linestyle="--", zorder=1)
    ax.text(-0.42, 1.06, "referência\n(risco basal)", fontsize=7.0,
            color=TINTA2, va="bottom", ha="left", linespacing=1.25)

    baixo = d["razao_de_risco"] - d["ic95_inferior"]
    alto = d["ic95_superior"] - d["razao_de_risco"]
    # O nivel de referencia nao tem intervalo: e 1 por construcao, nao estimativa.
    baixo.iloc[0] = alto.iloc[0] = 0.0

    ax.errorbar(x, d["razao_de_risco"], yerr=np.vstack([baixo, alto]),
                fmt="o", color=AZUL, markersize=8, markeredgecolor="white",
                markeredgewidth=1.4, ecolor=AZUL, elinewidth=1.8, capsize=5,
                zorder=4)

    for xi, r in zip(x, d.itertuples()):
        deslocamento = 0.13 if xi == 0 else 0.0
        ax.text(xi + 0.16, r.razao_de_risco + deslocamento,
                f"{r.razao_de_risco:.2f}×", fontsize=8.4, color=TINTA,
                va="center", ha="left", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(ROTULOS, fontsize=9)
    ax.set_xlim(-0.5, len(d) - 0.35)
    ax.set_ylim(0, 4.6)
    ax.set_xlabel("Nível de dificuldade técnica da tarefa (índice $D_i$)")
    ax.set_ylabel("Razão de risco (adimensional)")
    ax.set_title("Gradiente de risco transferido da base NASA para o PSPLIB J60\n"
                 "estimativa pontual e IC 95% por bootstrap de projetos (4.000 réplicas)",
                 fontsize=9.6, fontweight="bold", loc="left")
    fig.tight_layout()
    fig.savefig(FIG / "fig5_gradiente_risco.png", bbox_inches="tight")
    plt.close(fig)
    print("  fig5_gradiente_risco.png")


def figura_6_niveis_di():
    """
    Comportamento dos niveis de Di: duracao media e folga media.

    Duas grandezas de escalas diferentes, portanto DOIS paineis lado a lado e
    nao um grafico de eixo duplo -- que confundiria a leitura e sugeriria uma
    relacao entre as escalas que nao existe.
    """
    d = pd.read_csv(TAB / "psplib_02_distribuicao_niveis.csv")
    x = np.arange(len(d))

    fig, eixos = plt.subplots(1, 2, figsize=(7.2, 3.3))

    for ax, coluna, cor, titulo, unidade in (
        (eixos[0], "duracao_media", AZUL, "Duração média da tarefa", "períodos"),
        (eixos[1], "folga_media", LARANJA, "Folga total média", "períodos"),
    ):
        ax.grid(axis="y", color=GRADE, linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        ax.bar(x, d[coluna], 0.58, color=cor, zorder=3,
               edgecolor="white", linewidth=1.4)
        for xi, v in zip(x, d[coluna]):
            ax.text(xi, v + max(d[coluna]) * 0.03, f"{v:.2f}",
                    ha="center", fontsize=8, color=TINTA)
        ax.set_xticks(x)
        ax.set_xticklabels(ROTULOS, fontsize=8, rotation=20, ha="right")
        ax.set_ylim(0, max(d[coluna]) * 1.22)
        ax.set_ylabel(unidade)
        ax.set_title(titulo, fontsize=9.2, fontweight="bold", loc="left")

    fig.suptitle("Comportamento dos níveis do índice $D_i$ — 28.800 tarefas do J60",
                 fontsize=9.8, fontweight="bold", x=0.012, ha="left", y=1.02)
    fig.tight_layout()
    fig.savefig(FIG / "fig6_niveis_di.png", bbox_inches="tight")
    plt.close(fig)
    print("  fig6_niveis_di.png")


if __name__ == "__main__":
    print("Gerando figuras do bloco PSPLIB em outputs/figures/")
    figura_5_gradiente()
    figura_6_niveis_di()
    print("Concluido.")
