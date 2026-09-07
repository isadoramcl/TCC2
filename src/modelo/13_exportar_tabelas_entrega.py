"""
13_exportar_tabelas_entrega.py — tabelas da Entrega 1, prontas para o gerador
==============================================================================

`[DEC]` O gerador do documento (`docs/gerar_entrega.js`) lê CSV com um analisador
simples, que não trata vírgula dentro de campo. Este script consolida as saídas
das verificações em CSVs limpos — sem vírgula em campo algum, já arredondados e
já rotulados — de modo que NENHUM número seja digitado no gerador. É a mesma
regra do `06_exportar_parametros.py`, aplicada às tabelas de verificação.

SAIDA
-----
  outputs/tables/entrega_verificacoes.csv
  outputs/tables/entrega_b1_tendencia.csv
  outputs/tables/entrega_b3_poder.csv
  outputs/tables/entrega_tau_min.csv
  outputs/tables/entrega_ablacao_mecanismo.csv
  outputs/tables/entrega_fatorial.csv
  outputs/tables/entrega_porta2.csv
  outputs/tables/entrega_rastreabilidade.csv
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
T = RAIZ / "outputs" / "tables"


def br(x, c=4):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{c}f}".replace(".", ",")


def sci(x):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return (f"{x:.0e}".replace("e-0", " × 10⁻").replace("e-", " × 10⁻")
            if x < 0.001 else br(x, 3))


ACENTOS = [
    ("relogios", "relógios"), ("nao ", "não "), ("precedencia", "precedência"),
    ("disponibilidade de recursos nunca excedida",
     "disponibilidade de recursos nunca excedida"),
    ("variaveis", "variáveis"), ("intervalo unitario", "intervalo unitário"),
    ("reprodutibilidade", "reprodutibilidade"), ("semente", "semente"),
    ("divida", "dívida"), ("tecnica", "técnica"), ("pressao", "pressão"),
    ("heuristico", "heurístico"), ("condicao", "condição"),
    ("ociosidade", "ociosidade"), ("execucoes", "execuções"),
    ("mediana do retrabalho", "mediana do retrabalho"),
    ("faixa de plausibilidade", "faixa de plausibilidade"),
    ("estritamente positiva", "estritamente positiva"),
    ("criterio", "critério"), ("restringe", "restringe"),
    ("validacao", "validação"), ("evidencia", "evidência"),
    ("rebaixamento", "rebaixamento"), ("alocada", "alocada"),
    ("consistencia", "consistência"), ("violacoes", "violações"),
    ("instancias", "instâncias"), ("celula", "célula"),
    ("terminais", "terminais"), ("VERDADEIRA POR CONSTRUCAO",
                                 "verdadeira por construção"),
    ("exploratoria", "exploratória"), ("cresce com a", "cresce com a"),
    ("competencia", "competência"), ("tarefa termina", "tarefa termina"),
    ("estado terminal", "estado terminal"), ("soma positiva", "soma positiva"),
    ("relogio", "relógio"), ("agente alocado", "agente alocado"),
    ("maximo", "máximo"), ("minimo", "mínimo"), ("numero", "número"),
    ("defeitos GERADOS", "defeitos gerados"), ("divida oculta", "dívida oculta"),
    ("post hoc", "post hoc"), ("meta", "meta"),
]


EXTRA = [
    ("NAO ", "não "), ("nao ", "não "), ("F_ancora", "F_âncora"),
    ("rapido", "rápido"), ("favoraveis", "favoráveis"), ("esta sendo", "está sendo"),
    ("sementes diferentes", "sementes diferentes"), ("estoque", "estoque"),
    ("[exploratória - post hoc]", "exploratória"),
    ("[ordem de grandeza - não validação] ", ""),
    ("[meta] ", ""), ("mediana=", "mediana = "),
    ("critério 9a", "critério 9a"),
]


def acentuar(s):
    """Reacentua os rotulos, que sao gravados em ASCII nos logs, e converte o
    separador decimal para o padrao brasileiro. E camada de APRESENTACAO: os
    logs permanecem em ASCII e os numeros continuam vindo dos CSV de origem."""
    s = str(s)
    for a, b in ACENTOS + EXTRA:
        s = s.replace(a, b)
    return re.sub(r"(\d)\.(\d)", r"\1,\2", s)


def limpo(s):
    """Remove os dois separadores possiveis do texto livre."""
    return str(s).replace(";", " -").replace(",", " -")


def salvar(nome, linhas, cols):
    # `[DEC]` Separador PONTO E VIRGULA. Os campos trazem decimal brasileiro
    # (virgula), portanto a virgula nao pode ser separador. O gerador le estes
    # arquivos com `lerCsvPV`.
    pd.DataFrame(linhas, columns=cols).to_csv(T / nome, index=False,
                                              sep=";", encoding="utf-8")
    print(f"  {nome}: {len(linhas)} linhas")


# ---------------------------------------------------------------- verificações
v = pd.read_csv(T / "modelo_02_verificacoes.csv")
CLASSE = {
    "1.": "construção", "2.": "estrutural", "3.": "estrutural", "4a": "construção",
    "4b": "estrutural", "5.": "construção", "6.": "construção", "7a": "construção",
    "7b": "comportamento", "7c": "construção", "7d": "comportamento",
    "7e": "comportamento", "8a": "implementação", "8b": "implementação",
    "8c": "exploratória", "9a": "ordem de grandeza", "9b": "ordem de grandeza",
    "9c": "ordem de grandeza", "9d": "meta",
}
linhas = []
for r in v.itertuples():
    ch = str(r.verificacao)[:2]
    medido = acentuar(limpo(str(r.detalhe).split("|")[0].strip()))
    if len(medido) > 46:
        medido = medido[:44].rsplit(" ", 1)[0] + "…"
    ident = limpo(r.verificacao.split(".", 1)[0])
    ident = (ident.replace("-centralizada", "\u2011C")
                  .replace("-adaptativa", "\u2011A"))
    linhas.append([ident,
                   acentuar(limpo(r.verificacao.split(". ", 1)[-1]))[:110],
                   CLASSE.get(ch, "estrutural"),
                   {"OK": "aprovada", "NAO CONFIRMADA": "não confirmada",
                    "FALHA": "falha"}[r.resultado],
                   medido])
salvar("entrega_verificacoes.csv", linhas,
       ["id", "verificacao", "classe", "situacao", "medido"])

# ---------------------------------------------------------------- B1
b1 = pd.read_csv(T / "modelo_11_tendencia_resumo.csv")
b1c = b1[b1.etapa == "confirmatorio"]
b1p = b1[b1.etapa == "piloto"]
ROT = {"S_UR_maximo": "dívida oculta de pico",
       "fracao_heuristica": "fração de tempo em modo heurístico",
       "defeitos_gerados": "defeitos gerados (ocultos + reportados)"}
linhas = []
for alvo in ("S_UR_maximo", "fracao_heuristica", "defeitos_gerados"):
    for cen in ("centralizada", "adaptativa"):
        pp = b1p[(b1p.alvo == alvo) & (b1p.cenario == cen)]
        cc = b1c[(b1c.alvo == alvo) & (b1c.cenario == cen)]
        linhas.append([
            ROT[alvo], cen,
            f"{br(pp.rho.min(), 3)} a {br(pp.rho.max(), 3)}",
            f"{br(cc.rho.min(), 3)} a {br(cc.rho.max(), 3)}",
            f"[{br(cc.ic95_baixo.min(), 3)} a {br(cc.ic95_alto.max(), 3)}]",
            f"{int(cc.aprova.sum())} de {len(cc)}",
        ])
salvar("entrega_b1_tendencia.csv", linhas,
       ["grandeza", "cenario", "rho_piloto_n200", "rho_confirmatorio_n500",
        "ic95_confirmatorio", "confirma"])

# ---------------------------------------------------------------- B3
b3 = pd.read_csv(T / "modelo_02_b3_poder_do_criterio_9a.csv")
salvar("entrega_b3_poder.csv",
       [[br(r.F_ancora, 2), br(r.mediana_retrabalho_sobre_plano, 4),
         "aprova" if r.criterio_9a_aprova else "reprova"] for r in b3.itertuples()],
       ["f_ancora", "mediana", "criterio_9a"])

# ---------------------------------------------------------------- tau_min
tm = pd.read_csv(T / "modelo_09_sensibilidade_tau_min.csv")
ag = (tm.groupby(["tau_min", "arquivo"])[["p2_ajuda", "p2_bloqueio",
                                          "atraso_relativo", "TU", "TL", "TR",
                                          "E_total"]]
      .mean().groupby("tau_min").mean())
salvar("entrega_tau_min.csv",
       [[br(i, 4), br(r.p2_ajuda, 2), br(r.p2_bloqueio, 2),
         br(r.atraso_relativo, 4), br(r.TU, 2), br(r.TL, 2), br(r.TR, 2),
         br(r.E_total, 4)] for i, r in ag.iterrows()],
       ["tau_min", "ajudas", "bloqueios", "atraso_relativo", "tu", "tl", "tr",
        "e_total"])

# ---------------------------------------------------------------- ablação
ab = pd.read_csv(T / "modelo_07_ablacao_mecanismo.csv")
ROTM = {"atraso_relativo": "atraso relativo", "E_total": "ocupação E_total",
        "TL": "tempo de ajuda TL", "TU": "ociosidade TU",
        "TR": "retrabalho pago TR", "TW": "trabalho efetivo TW",
        "n_com_erro": "tarefas com defeito oculto",
        "taxa_omissao": "taxa de omissão",
        "retrabalho_sobre_plano": "retrabalho sobre o plano",
        "divida_latente_sobre_plano": "dívida latente sobre o plano",
        "S_UR_maximo": "dívida latente de pico"}
linhas = []
for m in ROTM:
    s = ab[ab.metrica == m].set_index("configuracao")
    if "nominal" not in s.index:
        continue
    linhas.append([
        ROTM[m], br(s.loc["nominal", "dif_absoluta"], 4),
        br(s.loc["sem_assistencia", "dif_absoluta"], 4),
        br(s.loc["assistencia_universal", "dif_absoluta"], 4),
        br(s.loc["sem_assistencia", "efeito_restante_pct_do_nominal"], 1) + "%",
        br(s.loc["assistencia_universal", "efeito_restante_pct_do_nominal"], 1) + "%",
        limpo(s.loc["sem_assistencia", "veredito"]).split("(")[0].strip()
        if "veredito" in s.columns else "—",
    ])
salvar("entrega_ablacao_mecanismo.csv", linhas,
       ["metrica", "nominal", "sem_assistencia", "assistencia_universal",
        "resta_sem", "resta_univ", "veredito"])

# ---------------------------------------------------------------- fatorial
fa = pd.read_csv(T / "modelo_10_fatorial_decomposicao.csv")
linhas = []
for m in ROTM:
    s = fa[fa.metrica == m].set_index("termo")
    if "SOMA_principais" not in s.index:
        continue
    ints = s[(s.ordem > 1)]
    maior = ints.reindex(ints["pct_do_contraste"].abs()
                         .sort_values(ascending=False).index)
    linhas.append([
        ROTM[m],
        br(s.loc["SOMA_principais", "pct_do_contraste"], 1) + "%",
        br(s.loc["SOMA_interacoes", "pct_do_contraste"], 1) + "%",
        (f"{maior.index[0]} ({br(maior.iloc[0]['pct_do_contraste'], 1)}%)"
         if len(maior) else "—"),
    ])
salvar("entrega_fatorial.csv", linhas,
       ["metrica", "efeitos_principais", "interacoes", "maior_interacao"])

# ---------------------------------------------------------------- Porta 2
p2 = pd.read_csv(T / "modelo_12_porta2_comparacao.csv")
p2m = p2[p2.tipo == "metrica"]
linhas = []
for cen in ("centralizada", "adaptativa"):
    s = p2m[p2m.cenario == cen]
    for m in ("atraso_relativo", "E_total", "TL", "TU", "TR",
              "S_UR_maximo", "n_com_erro"):
        r = s[s.grandeza == m]
        if not len(r):
            continue
        r = r.iloc[0]
        dif = br(r.dif_relativa_pct, 1)
        linhas.append([cen, ROTM[m], br(r.media_A_nominal, 4),
                       br(r.media_B_tcc1, 4),
                       dif if dif == "—" else dif + "%", sci(r.p_valor)])
salvar("entrega_porta2.csv", linhas,
       ["cenario", "metrica", "a_nominal", "b_tcc1", "dif_relativa", "p"])

# ---------------------------------------------------------------- rastreab.
abl = pd.read_csv(T / "modelo_07_ablacao_bruto.csv")
fat = pd.read_csv(T / "modelo_10_fatorial_celulas.csv")
salvar("entrega_rastreabilidade.csv", [
    ["Experimento central", "16 instâncias J60 (todas[::30][:16])", "0 a 11",
     "384", "modelo_03_experimento_bruto.csv"],
    ["Ablação de governança (B9)", "as mesmas 16 instâncias", "0 a 11",
     f"{len(abl)}", "modelo_07_ablacao_bruto.csv"],
    ["Decomposição fatorial 2⁴", "as mesmas 16 instâncias", "0 a 11",
     f"{len(fat)}", "modelo_10_fatorial_celulas.csv"],
    ["Sensibilidade de τ_mín", "as mesmas 16 instâncias", "0 a 11",
     f"{len(tm)}", "modelo_09_sensibilidade_tau_min.csv"],
    ["Tendência sob pressão — piloto", "j6010_1 e j6014_1", "0 a 39", "800",
     "modelo_11_tendencia_piloto.csv"],
    ["Tendência sob pressão — confirmatório", "j6010_1 e j6014_1",
     "1000 a 1099", "2000", "modelo_11_tendencia_confirmatorio.csv"],
    ["Porta 2 — TCC1 × TCC2", "as mesmas 16 instâncias", "0 a 11", "768",
     "modelo_12_porta2_comparacao.csv"],
], ["procedimento", "instancias", "sementes", "execucoes", "arquivo"])

# Conferencia: o separador nunca aparece dentro de campo. Testado contra um
# caso que ele DEVE pegar, para nao repetir o erro do verificador nao testado.
print("\nConferencia do separador:")
assert len("a;b;c".split(";")) != 2, "sanidade do proprio teste"
for f in sorted(T.glob("entrega_*.csv")):
    n = len(pd.read_csv(f, sep=";").columns)
    for i, l in enumerate(f.read_text(encoding="utf-8").strip().split("\n")):
        assert len(l.split(";")) == n, (
            f"{f.name} linha {i}: {len(l.split(';'))} campos, esperado {n}")
print("  ok — numero de campos constante em todos os arquivos")
import tempfile
mau = Path(tempfile.gettempdir()) / "_teste_separador.csv"
mau.write_text("a;b\nx;y;z\n", encoding="utf-8")
try:
    n = 2
    for l in mau.read_text().strip().split("\n"):
        assert len(l.split(";")) == n
    raise SystemExit("FALHA: o teste do separador nao pegou um caso invalido")
except AssertionError:
    print("  ok — o teste PEGA um arquivo malformado (verificador testado)")
finally:
    mau.unlink()
