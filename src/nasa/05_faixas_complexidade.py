"""
05_faixas_complexidade.py — Faixas de risco e calibracao do F_base
===================================================================

PROBLEMA QUE RESOLVE
--------------------
O modelo do TCC precisa de um risco basal F_base atribuivel a uma tarefa a
partir de um nivel ordinal de dificuldade (baixa, media, alta, muito alta).
Este script produz esse risco a partir da evidencia NASA, de forma auditavel,
e submete a construcao a testes de robustez.

ENTRADA
-------
  data/processed/nasa/base_dpp_consolidada.csv

SAIDA
-----
  outputs/tables/05_faixas_frequencias.csv
  outputs/tables/05_fbase.csv
  outputs/tables/05_sensibilidade_cortes.csv
  outputs/tables/05_leave_one_project_out.csv
  outputs/logs/05_faixas_complexidade.log

FONTE DOS CORTES
----------------
`[LITERATURA]` NASA Software Engineering Handbook, SWE-220 (Requisito 3.7.5):
"the project manager shall ensure all identified safety-critical software
components have a cyclomatic complexity value of 15 or lower. Any exceedance
shall be reviewed and waived with rationale by the project manager or technical
approval authority."
Faixas interpretativas apresentadas na mesma fonte: 1-10, 10-15, 15-20, 20-40,
>40.
<https://swehb.nasa.gov/spaces/SWEHBVD/pages/105709643/SWE-220+-+Cyclomatic+Complexity+for+Safety-Critical+Software>

`[LITERATURA]` NASA/TM-20205011566 (NESC): registra que a escolha de 15 e
deliberada, que a evidencia academica e "mixed", e que outras organizacoes
adotam 10-20.

`[DECISAO]` Adaptacao deste trabalho: as faixas da fonte se sobrepoem nos
extremos (10, 15, 20) e sao cinco. Adotamos quatro faixas nao sobrepostas,
alinhadas ao limiar normativo de 15 e ao numero de niveis exigido pelo modelo:
    baixa      v(G) <= 10        (faixa "bem estruturado" da fonte)
    media      11 <= v(G) <= 15  (limite normativo de seguranca critica)
    alta       16 <= v(G) <= 20  (exige revisao formal segundo a fonte)
    muito alta v(G) > 20         (fusao das faixas 20-40 e >40 da fonte)
Esta e uma ADAPTACAO METODOLOGICA, nao a classificacao oficial da NASA, e deve
ser descrita como tal na monografia.

ACHADO QUE CONDICIONA A INTERPRETACAO
--------------------------------------
`[ACHADO]` O script 04 mostrou que, nestes dados, a complexidade ciclomatica
NAO tem efeito independente do tamanho do modulo: seu OR ajustado por
log(LOC_TOTAL) e 0,944 com IC95 [0,870; 1,024], p = 0,17. O tamanho, ao
contrario, sobrevive ao controle pela complexidade (LR = 431, p ~ 1e-95).

Consequencia para este script: o F_base calculado sobre faixas de complexidade
ciclomatica descreve corretamente a FREQUENCIA OBSERVADA de defeito por faixa,
mas nao deve ser interpretado como efeito causal da complexidade. Por isso o
script calcula o F_base sobre DOIS eixos -- complexidade ciclomatica e tamanho
-- de modo que a escolha do eixo seja uma decisao explicita e informada, e nao
uma consequencia silenciosa do codigo.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. A soma das observacoes das faixas deve igualar o total da base.
  2. A frequencia global recomposta a partir das faixas deve igualar a taxa
     global de defeito.
  3. A ordenacao do F_base deve ser monotonicamente crescente; se nao for, o
     eixo nao sustenta uma leitura ordinal e isso e um achado.
  4. A validacao leave-one-project-out deve mostrar se a ordenacao se mantem
     quando cada projeto e retirado, ou se depende de um projeto especifico.
"""

import sys
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore")
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
ARQUIVO_BASE = RAIZ / "data" / "processed" / "nasa" / "base_dpp_consolidada.csv"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
for d in (DIR_TABELAS, DIR_LOGS):
    d.mkdir(parents=True, exist_ok=True)

_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


NIVEIS = ["baixa", "media", "alta", "muito alta"]

# Cortes por eixo. O primeiro elemento e -inf implicito; os valores sao limites
# superiores fechados de cada faixa, exceto a ultima, que e aberta.
CORTES = {
    "CYCLOMATIC_COMPLEXITY": [10, 15, 20],
    "LOC_TOTAL": None,  # definido por quartis, ver abaixo
}


def classificar(serie: pd.Series, limites: list[float]) -> pd.Categorical:
    bordas = [-np.inf] + list(limites) + [np.inf]
    return pd.cut(serie, bins=bordas, labels=NIVEIS, right=True)


def intervalo_wilson(sucessos: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """
    Intervalo de confianca de Wilson para uma proporcao.

    Preferido ao intervalo normal simples (Wald) porque as taxas de defeito aqui
    sao baixas e alguns estratos tem poucas observacoes -- situacao em que o
    intervalo de Wald produz limites fora de [0,1] e cobertura ruim.
    """
    if total == 0:
        return (float("nan"), float("nan"))
    p = sucessos / total
    denom = 1 + z**2 / total
    centro = (p + z**2 / (2 * total)) / denom
    margem = z * np.sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / denom
    return (max(0.0, centro - margem), min(1.0, centro + margem))


def tabela_por_faixa(dados: pd.DataFrame, coluna_faixa: str) -> pd.DataFrame:
    linhas = []
    for nivel in NIVEIS:
        sub = dados[dados[coluna_faixa] == nivel]
        n, d = len(sub), int(sub["defective"].sum())
        lo, hi = intervalo_wilson(d, n)
        linhas.append({
            "nivel": nivel, "n": n, "defeituosos": d,
            "frequencia_bruta": round(d / n, 5) if n else float("nan"),
            "ic95_inferior": round(lo, 5), "ic95_superior": round(hi, 5),
        })
    return pd.DataFrame(linhas)


def probabilidade_ajustada(dados: pd.DataFrame, coluna_faixa: str) -> pd.DataFrame:
    """
    Probabilidade de defeito por faixa, ajustada pelo efeito do projeto.

    Metodo: ajusta-se logit(defeito) ~ C(project) + C(faixa) e entao, para cada
    faixa, calcula-se a media das probabilidades preditas SUPONDO que todas as
    observacoes da base estivessem naquela faixa (padronizacao marginal, tambem
    chamada de g-computation). Isso responde: "qual seria a taxa de defeito se
    a composicao de projetos fosse a mesma em todas as faixas?" -- separando o
    efeito da faixa do efeito de quais projetos a povoam.
    """
    modelo = smf.logit(f"defective ~ C(project) + C({coluna_faixa})", data=dados).fit(disp=0)
    linhas = []
    for nivel in NIVEIS:
        contrafactual = dados.copy()
        contrafactual[coluna_faixa] = pd.Categorical([nivel] * len(dados), categories=NIVEIS)
        linhas.append({
            "nivel": nivel,
            "probabilidade_ajustada": round(float(modelo.predict(contrafactual).mean()), 5),
        })
    return pd.DataFrame(linhas), modelo


def teste_de_tendencia(dados: pd.DataFrame, coluna_faixa: str) -> dict:
    """
    Teste de tendencia de Cochran-Armitage: existe tendencia MONOTONICA da
    proporcao de defeito ao longo dos niveis ordenados?

    Diferente de um qui-quadrado de independencia, que apenas detecta "alguma
    diferenca", este teste usa a ordem dos niveis -- que e exatamente o que
    interessa para uma transferencia ordinal.
    """
    escores = {n: i for i, n in enumerate(NIVEIS)}
    x = dados[coluna_faixa].map(escores).astype(float)
    y = dados["defective"].astype(float)
    n = len(dados)
    p = y.mean()
    xbar = x.mean()
    numerador = float(((x - xbar) * (y - p)).sum())
    denominador = float(np.sqrt(p * (1 - p) * ((x - xbar) ** 2).sum()))
    z = numerador / denominador if denominador else float("nan")
    return {"estatistica_z": round(z, 4), "p_valor": float(2 * stats.norm.sf(abs(z)))}


def main() -> None:
    log("=" * 78)
    log("FAIXAS DE RISCO E CALIBRACAO DO F_base")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    base = pd.read_csv(ARQUIVO_BASE)
    log(f"\nBase: {len(base)} observacoes | taxa global de defeito: {base['defective'].mean():.4%}")

    # Cortes de tamanho por quartis da propria base, para que o eixo alternativo
    # tenha estratos de tamanho comparavel. Declarado como decisao do trabalho.
    quartis = base["LOC_TOTAL"].quantile([0.25, 0.50, 0.75]).tolist()
    CORTES["LOC_TOTAL"] = [round(q, 2) for q in quartis]

    resultados_fbase: list[dict] = []
    todas_frequencias: list[dict] = []

    for eixo, limites in CORTES.items():
        origem = ("NASA SWE-220 (adaptado, 4 niveis nao sobrepostos)"
                  if eixo == "CYCLOMATIC_COMPLEXITY"
                  else "quartis da propria base (decisao deste trabalho)")

        log("\n" + "=" * 78)
        log(f"EIXO: {eixo}")
        log(f"  cortes : {limites}   ({origem})")
        log("=" * 78)

        coluna = f"faixa_{eixo}"
        base[coluna] = classificar(base[eixo], limites)

        frequencias = tabela_por_faixa(base, coluna)
        ajustadas, modelo = probabilidade_ajustada(base, coluna)
        tabela = frequencias.merge(ajustadas, on="nivel")
        tabela["eixo"] = eixo
        tabela["cortes"] = str(limites)
        todas_frequencias.append(tabela)

        log(f"\n  {'nivel':<12} {'n':>6} {'defeit.':>8} {'freq bruta':>11} "
            f"{'IC95 bruto':>20} {'prob ajustada':>14}")
        for _, r in tabela.iterrows():
            log(f"  {r['nivel']:<12} {r['n']:>6} {r['defeituosos']:>8} "
                f"{r['frequencia_bruta']:>11.4f} "
                f"[{r['ic95_inferior']:>8.4f};{r['ic95_superior']:>8.4f}] "
                f"{r['probabilidade_ajustada']:>14.4f}")

        tendencia = teste_de_tendencia(base, coluna)
        log(f"\n  Teste de tendencia (Cochran-Armitage): z = {tendencia['estatistica_z']}, "
            f"p = {tendencia['p_valor']:.3e}")

        monotonica_bruta = list(tabela["frequencia_bruta"]) == sorted(tabela["frequencia_bruta"])
        monotonica_ajustada = list(tabela["probabilidade_ajustada"]) == sorted(tabela["probabilidade_ajustada"])
        log(f"  Monotonicidade  frequencia bruta: {monotonica_bruta} | "
            f"probabilidade ajustada: {monotonica_ajustada}")

        for _, r in tabela.iterrows():
            resultados_fbase.append({
                "eixo": eixo, "origem_dos_cortes": origem, "cortes": str(limites),
                "nivel": r["nivel"], "n": r["n"], "defeituosos": r["defeituosos"],
                "F_base_frequencia_bruta": r["frequencia_bruta"],
                "F_base_ajustado_por_projeto": r["probabilidade_ajustada"],
                "ic95_inferior": r["ic95_inferior"], "ic95_superior": r["ic95_superior"],
                "tendencia_z": tendencia["estatistica_z"],
                "tendencia_p": tendencia["p_valor"],
                "monotonica_bruta": monotonica_bruta,
                "monotonica_ajustada": monotonica_ajustada,
            })

    pd.concat(todas_frequencias).to_csv(DIR_TABELAS / "05_faixas_frequencias.csv",
                                        index=False, encoding="utf-8")
    pd.DataFrame(resultados_fbase).to_csv(DIR_TABELAS / "05_fbase.csv",
                                          index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # Sensibilidade aos cortes
    #
    # Se pequenas mudancas nos limiares alterarem substancialmente o F_base,
    # entao o F_base e um artefato da escolha dos cortes, e nao uma propriedade
    # dos dados. Este teste existe para que essa possibilidade seja medida em
    # vez de ignorada.
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("SENSIBILIDADE AOS CORTES (eixo: complexidade ciclomatica)")
    log("=" * 78)
    alternativas = {
        "SWE-220 adaptado (referencia)": [10, 15, 20],
        "mais permissivo": [12, 18, 25],
        "mais restritivo": [8, 12, 16],
        "usado no TCC1 (exploratorio)": [3, 7, 15],
        "quartis da base": [round(q, 2) for q in base["CYCLOMATIC_COMPLEXITY"].quantile([.25, .5, .75])],
    }
    linhas_sensibilidade = []
    log(f"  {'esquema':<32} {'cortes':<20} " + " ".join(f"{n:>11}" for n in NIVEIS) + "   monot.")
    for nome, limites in alternativas.items():
        coluna = "faixa_teste"
        base[coluna] = classificar(base["CYCLOMATIC_COMPLEXITY"], limites)
        t = tabela_por_faixa(base, coluna)
        valores = list(t["frequencia_bruta"])
        mono = valores == sorted(valores)
        log(f"  {nome:<32} {str(limites):<20} " +
            " ".join(f"{v:>11.4f}" for v in valores) + f"   {mono}")
        registro = {"esquema": nome, "cortes": str(limites), "monotonica": mono}
        for nivel, valor, n in zip(NIVEIS, valores, t["n"]):
            registro[f"F_base_{nivel.replace(' ', '_')}"] = valor
            registro[f"n_{nivel.replace(' ', '_')}"] = int(n)
        linhas_sensibilidade.append(registro)
    pd.DataFrame(linhas_sensibilidade).to_csv(DIR_TABELAS / "05_sensibilidade_cortes.csv",
                                              index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # Leave-one-project-out
    #
    # Retira-se um projeto por vez e recalcula-se o F_base. Se a ordenacao so se
    # sustenta com um projeto especifico presente, ela nao e transferivel.
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("VALIDACAO LEAVE-ONE-PROJECT-OUT (eixo: complexidade ciclomatica)")
    log("=" * 78)
    base["faixa_ref"] = classificar(base["CYCLOMATIC_COMPLEXITY"], [10, 15, 20])
    log(f"  {'projeto retirado':<18} {'n restante':>11} " +
        " ".join(f"{n:>11}" for n in NIVEIS) + "   monot.")
    linhas_loo = []
    for projeto in sorted(base["project"].unique()):
        sub = base[base["project"] != projeto]
        t = tabela_por_faixa(sub, "faixa_ref")
        valores = list(t["frequencia_bruta"])
        mono = valores == sorted(valores)
        log(f"  {projeto:<18} {len(sub):>11} " +
            " ".join(f"{v:>11.4f}" for v in valores) + f"   {mono}")
        registro = {"projeto_retirado": projeto, "n_restante": len(sub), "monotonica": mono}
        for nivel, valor in zip(NIVEIS, valores):
            registro[f"F_base_{nivel.replace(' ', '_')}"] = valor
        linhas_loo.append(registro)

    df_loo = pd.DataFrame(linhas_loo)
    df_loo.to_csv(DIR_TABELAS / "05_leave_one_project_out.csv", index=False, encoding="utf-8")

    colunas_fbase = [f"F_base_{n.replace(' ', '_')}" for n in NIVEIS]
    log("\n  Amplitude do F_base entre as 12 reamostragens:")
    for nivel, coluna in zip(NIVEIS, colunas_fbase):
        log(f"    {nivel:<12} min={df_loo[coluna].min():.4f}  max={df_loo[coluna].max():.4f}  "
            f"amplitude={df_loo[coluna].max() - df_loo[coluna].min():.4f}")
    log(f"\n  Ordenacao monotonica preservada em {int(df_loo['monotonica'].sum())}/12 reamostragens")

    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("VERIFICACOES")
    log("=" * 78)
    falhas = []
    for eixo in CORTES:
        soma = int(base[f"faixa_{eixo}"].value_counts().sum())
        if soma == len(base):
            log(f"  [OK]    {eixo}: todas as {soma} observacoes classificadas")
        else:
            falhas.append(f"{eixo}: {soma} de {len(base)} classificadas")
            log(f"  [FALHA] {eixo}: {soma} de {len(base)}")

    fb = pd.DataFrame(resultados_fbase)
    for eixo in CORTES:
        sub = fb[fb["eixo"] == eixo]
        # Recomposicao a partir das CONTAGENS, e nao das frequencias arredondadas
        # gravadas na tabela: comparar valores arredondados a 5 casas contra a
        # taxa global exata produziria uma falha espuria de ordem 1e-6.
        recomposta = float(sub["defeituosos"].sum() / sub["n"].sum())
        if abs(recomposta - base["defective"].mean()) < 1e-9:
            log(f"  [OK]    {eixo}: frequencia recomposta = taxa global ({recomposta:.6f})")
        else:
            falhas.append(f"{eixo}: recomposicao {recomposta} != global")
            log(f"  [FALHA] {eixo}: recomposta {recomposta:.6f}")

    log("\n" + "=" * 78)
    log("RESULTADO: " + ("CONCLUIDO COM FALHAS" if falhas else "CONCLUIDO, VERIFICACOES OK"))
    for f in falhas:
        log(f"  - {f}")
    log("=" * 78)

    (DIR_LOGS / "05_faixas_complexidade.log").write_text("\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
