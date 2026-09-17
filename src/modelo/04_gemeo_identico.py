"""
04_gemeo_identico.py — Calibração por History Matching e teste do gêmeo idêntico
=================================================================================

Responde a duas perguntas que a banca fará sobre qualquer modelo com parâmetros
não observados:

  1. **Existe procedimento de calibração?** Sim: History Matching, com medida de
     implausibilidade e corte declarado.
  2. **Esse procedimento funciona?** Testado pelo método do **gêmeo idêntico**:
     geram-se observações sintéticas a partir de um vetor de parâmetros
     CONHECIDO, roda-se a calibração às cegas e verifica-se se ela recupera o
     vetor verdadeiro.

Sem (2), (1) é só um algoritmo rodando — não há evidência de que ele identifique
coisa alguma.

METODO
------
`[LIT]` **History Matching.** Descarta-se do espaço de parâmetros tudo o que é
implausível à luz dos dados, em vez de buscar um único ótimo. A saída não é um
ponto: é o conjunto **NROY** (*Not Ruled Out Yet*).

    ANDRIANAKIS, I. et al. Bayesian History Matching of Complex Infectious
    Disease Models Using Emulation: A Tutorial and a Case Study on HIV in
    Uganda. PLoS Computational Biology, v. 11, n. 1, e1003968, 2015.
    DOI 10.1371/journal.pcbi.1003968
    <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003968>

`[LIT]` **Gêmeo idêntico e identificabilidade em modelos baseados em agentes.**

    McCULLOCH, J.; GE, J.; WARD, J. A.; HEPPENSTALL, A.; POLHILL, J. G.;
    MALLESON, N. Calibrating Agent-Based Models Using Uncertainty Quantification
    Methods. JASSS, v. 25, n. 2, artigo 1, 2022. DOI 10.18564/jasss.4791
    <https://www.jasss.org/25/2/1.html>

`[LIT/DEC]` **Corte de implausibilidade em 3.** A desigualdade de
Vysochanskii–Petunin fornece um limite marginal para variável com densidade
unimodal e variância finita. Seu uso com variâncias estimadas e o máximo de
vários observáveis NÃO garante cobertura conjunta de 95%. O corte legado é
preservado para comparação; ver research/SOURCES.md e a resposta à revisão.

    PUKELSHEIM, F. The Three Sigma Rule. The American Statistician, v. 48, n. 2,
    p. 88-91, 1994. DOI 10.1080/00031305.1994.10476030
    <https://www.tandfonline.com/doi/abs/10.1080/00031305.1994.10476030>

`[DEC]` **History Matching SEM emulador.** O emulador existe para substituir um
simulador caro. O nosso custa 0,108 s por execução, e o desenho completo cabe em
minutos. Avalia-se o simulador diretamente. Isso ELIMINA o termo de erro de
emulação da implausibilidade — uma aproximação a menos, não uma a mais. Se o
modelo for ampliado a ponto de encarecer, o emulador entra sem mudar o resto.

    I_j(x) = | z_j − f̄_j(x) | / sqrt( V_obs,j + V_sim,j + V_mod,j )
    I(x)   = max_j I_j(x)          x ∈ NROY  ⟺  I(x) ≤ 3

`[DEC]` **V_mod = 0 neste teste, com z publicada fixa, não torna o teste
automaticamente otimista.** O conjunto NROY compara a média simulada com uma
realização sintética já fixada. Ao aumentar réplicas, `V_sim` pode encolher e o
procedimento pode rejeitar o próprio vetor verdadeiro. Portanto, falhar não
condena o procedimento em geral e passar não garante desempenho com dados reais.
A direção pessimista é uma propriedade condicional à z publicada, não um teorema
para toda observação sintética.

O limite formal de implausibilidade para o vetor verdadeiro exigiria a média
exata `mu` do simulador. A estimativa baseada em 64 réplicas não prova
permanência no NROY. Com dados reais, `V_mod` também precisa ser especificado.

SAIDA
-----
  outputs/tables/modelo_04_hm_onda1.csv, ..._onda2.csv
  outputs/tables/modelo_04_identificabilidade.csv
  outputs/logs/modelo_04_gemeo_identico.log
"""

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import simulador as S  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
TAB = RAIZ / "outputs" / "tables"
LOGS = RAIZ / "outputs" / "logs"
_log: list[str] = []

# ---------------------------------------------------------------------
# `[DEC]` Parâmetros calibrados. São cinco dos treze `[ABERTO]`, escolhidos por
# terem efeito DIRETO sobre grandezas que um projeto real reporta. Calibrar os
# treze contra quatro observáveis seria garantir não-identificabilidade; o
# recorte é deliberado e a consequência (os outros oito permanecem premissa) é
# declarada no relatório.
# ---------------------------------------------------------------------
PARAMETROS = [
    ("risco",      "F_ancora",     0.05, 0.25),
    ("retrabalho", "f_retrabalho", 0.30, 0.80),
    ("agentes",    "tau_sat",      0.70, 1.40),
    ("agentes",    "k_heuristico", 0.06, 0.16),
    ("fuzzy",      "mu_minimo",    0.40, 0.70),
]
NOMES = [f"{a}.{b}" for a, b, _, _ in PARAMETROS]

# `[DEC]` Vetor verdadeiro. Deliberadamente NÃO no centro das faixas: um gêmeo
# cujo alvo esteja no meio do espaço é fácil demais e não testa as bordas.
VERDADE = {"risco.F_ancora": 0.180, "retrabalho.f_retrabalho": 0.420,
           "agentes.tau_sat": 0.850, "agentes.k_heuristico": 0.135,
           "fuzzy.mu_minimo": 0.620}

# `[DEC]` Observáveis: grandezas que um projeto de engenharia real registra —
# fração de entregas que voltaram com defeito, atraso contra o cronograma,
# esforço de retrabalho sobre o planejado e fração produtiva do esforço.
OBSERVAVEIS = ["taxa_omissao", "atraso_relativo", "retrabalho_sobre_plano", "E_total"]

CENARIO = "adaptativa"      # um projeto real opera sob UM arranjo de governança
N_INSTANCIAS = 2
N_SEMENTES_SIM = 4          # réplicas por ponto do desenho
SEMENTES_OBS = range(100, 110)   # DISJUNTAS das do simulador
CORTE = 3.0
N_PONTOS = 400


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def instancias():
    todas = sorted(pd.read_csv(RAIZ / "data" / "processed" / "psplib" /
                               "tarefas_j60_com_di.csv")["arquivo"].unique())
    return todas[::len(todas) // N_INSTANCIAS][:N_INSTANCIAS]


def aplicar(par: dict, x: dict) -> dict:
    import copy
    p = copy.deepcopy(par)
    for (sec, nome, _, _) in PARAMETROS:
        p[sec][nome]["valor"] = float(x[f"{sec}.{nome}"])
    return p


def rodar(par: dict, x: dict, sementes, insts, cache={}) -> dict:
    """Média dos observáveis sobre instâncias × sementes, e variância da média."""
    p = aplicar(par, x)
    linhas = []
    for arq in insts:
        if arq not in cache:
            cache[arq] = S.carregar_instancia(arq)
        g, disp, cpm = cache[arq]
        for sem in sementes:
            r = S.Simulacao(g, disp, cpm, p, CENARIO, semente=int(sem)).executar()
            # atraso_relativo nao e campo de Resultado: e derivado, como no
            # experimento (03_experimento_cenarios.py).
            vals = {"atraso_relativo": r.makespan / r.makespan_cpm}
            linhas.append({o: float(vals[o] if o in vals else getattr(r, o))
                           for o in OBSERVAVEIS})
    d = pd.DataFrame(linhas)
    n = len(d)
    saida = {}
    for o in OBSERVAVEIS:
        saida[f"media_{o}"] = float(d[o].mean())
        saida[f"var_media_{o}"] = float(d[o].var(ddof=1) / n)
    return saida


def lhs(n: int, limites, rng) -> np.ndarray:
    """Hipercubo latino: uma amostra por estrato em cada dimensão."""
    k = len(limites)
    X = np.empty((n, k))
    for j, (lo, hi) in enumerate(limites):
        cortes = (np.arange(n) + rng.random(n)) / n
        X[:, j] = lo + (hi - lo) * rng.permutation(cortes)
    return X


def implausibilidade(linha: pd.Series, z: dict) -> float:
    """I(x) = max_j |z_j - f̄_j(x)| / sqrt(V_obs + V_sim). V_mod = 0 (ver cabeçalho)."""
    piores = []
    for o in OBSERVAVEIS:
        denom = np.sqrt(z[f"var_media_{o}"] + linha[f"var_media_{o}"])
        if denom <= 0:
            denom = 1e-12
        piores.append(abs(z[f"media_{o}"] - linha[f"media_{o}"]) / denom)
    return float(max(piores))


# =====================================================================
def main() -> None:
    modo = sys.argv[1] if len(sys.argv) > 1 else "relatorio"
    par = S.carregar_parametros()
    insts = instancias()
    rng_desenho = np.random.default_rng(20260905)

    if modo in ("onda1", "onda2"):
        parte = int(sys.argv[2]); n_partes = int(sys.argv[3])
        if modo == "onda1":
            X = lhs(N_PONTOS, [(lo, hi) for _, _, lo, hi in PARAMETROS], rng_desenho)
        else:
            d1 = pd.read_csv(TAB / "modelo_04_hm_onda1.csv")
            nroy = d1[d1["implausibilidade"] <= CORTE]
            # `[DEC]` A onda 2 amostra dentro da CAIXA envolvente do NROY da onda
            # 1. É o refinamento padrão do metodo: concentra o esforco onde ainda
            # ha massa plausivel, sem excluir nada que a onda 1 nao excluiu.
            lim = [(float(nroy[n].min()), float(nroy[n].max())) for n in NOMES]
            X = lhs(N_PONTOS, lim, rng_desenho)
        ini = (parte - 1) * len(X) // n_partes
        fim = parte * len(X) // n_partes
        linhas = []
        for i in range(ini, fim):
            x = {n: X[i, j] for j, n in enumerate(NOMES)}
            linhas.append({**x, "ponto": i,
                           **rodar(par, x, range(N_SEMENTES_SIM), insts)})
        arq = TAB / f"modelo_04_hm_{modo}_parte{parte}.csv"
        pd.DataFrame(linhas).to_csv(arq, index=False, encoding="utf-8")
        print(f"{modo} parte {parte}/{n_partes}: pontos {ini}..{fim - 1} -> {arq.name}")
        return

    if modo == "verdade":
        z = rodar(par, VERDADE, SEMENTES_OBS, insts)
        pd.DataFrame([{**VERDADE, **z}]).to_csv(
            TAB / "modelo_04_observacoes_sinteticas.csv", index=False, encoding="utf-8")
        print("observacoes sinteticas geradas em modelo_04_observacoes_sinteticas.csv")
        for o in OBSERVAVEIS:
            print(f"  {o:<26} z = {z['media_' + o]:.4f}   "
                  f"dp da media = {np.sqrt(z['var_media_' + o]):.5f}")
        return

    if modo == "juntar":
        onda = sys.argv[2]
        ps = sorted(TAB.glob(f"modelo_04_hm_{onda}_parte*.csv"))
        d = pd.concat([pd.read_csv(p) for p in ps], ignore_index=True)
        z = pd.read_csv(TAB / "modelo_04_observacoes_sinteticas.csv").iloc[0]
        d["implausibilidade"] = d.apply(lambda r: implausibilidade(r, z), axis=1)
        d.sort_values("ponto").to_csv(TAB / f"modelo_04_hm_{onda}.csv",
                                      index=False, encoding="utf-8")
        # Os arquivos de parte sao mantidos: sao o registro bruto de cada
        # execucao do desenho e permitem reconferir a juncao sem re-rodar.
        (TAB / "partes_hm").mkdir(exist_ok=True)
        for p in ps:
            destino = TAB / "partes_hm" / p.name
            try:
                p.replace(destino)
            except OSError:
                pass   # ambiente sem permissao de mover; parte permanece onde esta
        n_nroy = int((d["implausibilidade"] <= CORTE).sum())
        print(f"{onda}: {len(d)} pontos, NROY = {n_nroy} ({n_nroy / len(d):.1%})")
        return

    # ---------------- relatorio ----------------
    log("=" * 78)
    log("CALIBRACAO POR HISTORY MATCHING E TESTE DO GEMEO IDENTICO")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)
    z = pd.read_csv(TAB / "modelo_04_observacoes_sinteticas.csv").iloc[0]

    log(f"\nParametros calibrados : {len(PARAMETROS)} dos 13 [ABERTO]")
    log(f"Observaveis           : {len(OBSERVAVEIS)}")
    log(f"Cenario               : {CENARIO}   instancias: {len(insts)}")
    log(f"Corte de implausibilidade: {CORTE}  (convencao legada; sem garantia conjunta de 95%)")
    log("\nVetor verdadeiro (desconhecido do procedimento):")
    for n in NOMES:
        log(f"  {n:<28} {VERDADE[n]:.4f}")
    log("\nObservacoes sinteticas (sementes 100-109, disjuntas das do simulador):")
    for o in OBSERVAVEIS:
        log(f"  {o:<26} z = {z['media_' + o]:.4f}   "
            f"dp da media = {np.sqrt(z['var_media_' + o]):.5f}")

    tabela = []
    for onda in ("onda1", "onda2"):
        arq = TAB / f"modelo_04_hm_{onda}.csv"
        if not arq.exists():
            continue
        d = pd.read_csv(arq)
        nroy = d[d["implausibilidade"] <= CORTE]
        log("\n" + "=" * 78)
        log(f"{onda.upper()} — {len(d)} pontos avaliados")
        log("=" * 78)
        log(f"  NROY: {len(nroy)} pontos ({len(nroy) / len(d):.1%} do desenho)")
        log(f"  implausibilidade — min {d['implausibilidade'].min():.3f}   "
            f"mediana {d['implausibilidade'].median():.3f}   "
            f"max {d['implausibilidade'].max():.3f}")
        if len(nroy) == 0:
            log("  [FALHA] NROY vazio — o procedimento excluiu todo o espaco")
            continue
        log(f"\n  {'parametro':<28}{'verdade':>9}{'NROY min':>10}{'NROY max':>10}"
            f"{'largura':>9}{'prior':>8}{'reducao':>9}{'contem':>8}")
        for (sec, nome, lo, hi) in PARAMETROS:
            n = f"{sec}.{nome}"
            a, b = float(nroy[n].min()), float(nroy[n].max())
            larg, prior = b - a, hi - lo
            contem = a <= VERDADE[n] <= b
            log(f"  {n:<28}{VERDADE[n]:>9.4f}{a:>10.4f}{b:>10.4f}"
                f"{larg:>9.4f}{prior:>8.4f}{1 - larg / prior:>8.1%}"
                f"{'sim' if contem else 'NAO':>8}")
            tabela.append({"onda": onda, "parametro": n, "verdade": VERDADE[n],
                           "nroy_min": round(a, 5), "nroy_max": round(b, 5),
                           "largura_nroy": round(larg, 5), "largura_prior": prior,
                           "reducao": round(1 - larg / prior, 4),
                           "contem_verdade": bool(contem)})

    # ---- criterios do teste do gemeo ----
    log("\n" + "=" * 78)
    log("VEREDITO DO TESTE DO GEMEO IDENTICO")
    log("=" * 78)
    ultima = "onda2" if (TAB / "modelo_04_hm_onda2.csv").exists() else "onda1"
    d = pd.read_csv(TAB / f"modelo_04_hm_{ultima}.csv")
    nroy = d[d["implausibilidade"] <= CORTE]
    falhas = []
    if len(nroy) == 0:
        falhas.append("NROY vazio")
    for n in NOMES:
        if not (float(nroy[n].min()) <= VERDADE[n] <= float(nroy[n].max())):
            falhas.append(f"NROY nao contem a verdade em {n}")
    if len(nroy) / len(d) >= 0.95:
        falhas.append("o espaco praticamente nao foi reduzido")
    log(f"  1. NROY nao vazio                          : "
        f"{'OK' if len(nroy) else 'FALHA'}  ({len(nroy)} pontos)")
    log(f"  2. NROY contem o vetor verdadeiro em todos : "
        f"{'OK' if not [f for f in falhas if 'contem' in f or 'nao contem' in f] else 'FALHA'}")
    log(f"  3. o espaco foi efetivamente reduzido      : "
        f"{'OK' if len(nroy) / len(d) < 0.95 else 'FALHA'}  "
        f"({len(nroy) / len(d):.1%} do desenho sobrevive)")
    log("  [LIMITACAO] Conter a verdade nas projecoes marginais nao prova")
    log("  que o vetor verdadeiro conjunto pertence ao NROY. Criterios fracos.")

    # ---- identificabilidade (Camada 4) ----
    log("\n" + "=" * 78)
    log("IDENTIFICABILIDADE — quais parametros os dados determinam")
    log("=" * 78)
    log("  `[DEC]` Criterio: reducao da largura marginal do NROY em relacao a")
    log("  faixa a priori. Abaixo de 25% a calibracao praticamente nao informou")
    log("  o parametro, e ele deve ser reportado como NAO identificado — nao")
    log("  como 'estimado'. Esconder isso seria apresentar como resultado o que")
    log("  e artefato do desenho.")
    log("  Os rotulos abaixo descrevem apenas a contracao marginal neste desenho;")
    log("  essa classificacao nao demonstra identificabilidade estrutural.")
    log("")
    for r_ in [t for t in tabela if t["onda"] == ultima]:
        st = ("identificado" if r_["reducao"] >= 0.50 else
              "parcialmente identificado" if r_["reducao"] >= 0.25 else
              "NAO identificado")
        log(f"  {r_['parametro']:<28} reducao {r_['reducao']:>6.1%}   {st}")

    # equifinalidade: correlacoes dentro do NROY revelam cristas
    log("\n  Equifinalidade — correlacao de Spearman DENTRO do NROY.")
    log("  Correlacao alta sugere compensacao dentro do conjunto aceito;")
    log("  nao prova equivalencia das saidas nem impossibilidade de separar fatores.")
    cor = nroy[NOMES].corr(method="spearman")
    pares = [(a, b, float(cor.loc[a, b])) for i, a in enumerate(NOMES)
             for b in NOMES[i + 1:]]
    for a, b, c in sorted(pares, key=lambda t: -abs(t[2]))[:4]:
        marca = "  <-- crista" if abs(c) >= 0.30 else ""
        log(f"    {a:<28} x {b:<28} rho = {c:+.3f}{marca}")

    # ---- combinacao derivada sugerida pela crista ----
    log("\n" + "=" * 78)
    log("PRODUTO DOS PARAMETROS — DESCRICAO DO CONJUNTO LEGADO")
    log("=" * 78)
    log("  [REVISAO] A interpretacao anterior de produto suficiente foi refutada")
    log("  pelo piloto pareado em research/PLANO_REVISAO.md. O esforco de")
    log("  retrabalho gerado por tarefa e, em esperanca,")
    log("")
    log("      E[retrabalho por tarefa] ~ p_falha x f_retrabalho x duracao")
    log("")
    log("  mas p_falha inclui um termo cognitivo aditivo e taxa_omissao informa")
    log("  sobre frequencia separadamente. A crista observada nao justifica")
    log("  substituir automaticamente os dois parametros pelo produto.")
    log("")
    prod_nroy = (nroy["risco.F_ancora"] * nroy["retrabalho.f_retrabalho"])
    prod_todos = (d["risco.F_ancora"] * d["retrabalho.f_retrabalho"])
    lo_p, hi_p = 0.05 * 0.30, 0.25 * 0.80          # faixa a priori do produto
    larg_p = float(prod_nroy.max() - prod_nroy.min())
    verdade_prod = VERDADE["risco.F_ancora"] * VERDADE["retrabalho.f_retrabalho"]
    red_prod = 1 - larg_p / (hi_p - lo_p)
    log(f"  {'grandeza':<34}{'verdade':>9}{'NROY min':>10}{'NROY max':>10}{'reducao':>9}")
    for (sec, nome, lo, hi) in PARAMETROS:
        n = f"{sec}.{nome}"
        if n in ("risco.F_ancora", "retrabalho.f_retrabalho"):
            a, b = float(nroy[n].min()), float(nroy[n].max())
            log(f"  {n:<34}{VERDADE[n]:>9.4f}{a:>10.4f}{b:>10.4f}"
                f"{1 - (b - a) / (hi - lo):>8.1%}")
    log(f"  {'F_ancora x f_retrabalho (produto)':<34}{verdade_prod:>9.4f}"
        f"{float(prod_nroy.min()):>10.4f}{float(prod_nroy.max()):>10.4f}{red_prod:>8.1%}")
    log("")
    if red_prod > max(t["reducao"] for t in tabela
                      if t["onda"] == ultima
                      and t["parametro"] in ("risco.F_ancora", "retrabalho.f_retrabalho")):
        log("  O produto apresenta maior contracao relativa nesta tabela.")
        log("  [LIMITACAO] Isso nao demonstra que ele contenha toda a informacao")
        log("  das saidas. A recomendacao automatica de reparametrizacao foi retirada.")
    else:
        log("  O produto NAO e mais bem determinado que os fatores; a crista tem")
        log("  outra origem e precisa ser reexaminada.")

    # ---- reducao acumulada de volume da caixa envolvente ----
    d1 = pd.read_csv(TAB / "modelo_04_hm_onda1.csv")
    n1 = d1[d1["implausibilidade"] <= CORTE]
    vol_prior = float(np.prod([hi - lo for _, _, lo, hi in PARAMETROS]))
    vol_final = float(np.prod([nroy[n].max() - nroy[n].min() for n in NOMES]))
    log("\n  Volume da caixa envolvente do NROY sobre o volume a priori: "
        f"{vol_final / vol_prior:.4f}")
    log("  [LIMITACAO] Estabilidade do casco nao estabelece convergencia.")
    log("  As ondas legadas repetem o desenho normalizado. Ruido, observacao e")
    log("  estimando precisam ser avaliados antes de novas ondas independentes.")

    pd.DataFrame(tabela).to_csv(TAB / "modelo_04_identificabilidade.csv",
                                index=False, encoding="utf-8")
    log("\n" + "=" * 78)
    log(f"CRITERIOS LEGADOS (nao validacao estrutural): {'APROVADO' if not falhas else 'REPROVADO'}"
        + ("" if not falhas else "  falhas: " + "; ".join(falhas)))
    log("=" * 78)
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "modelo_04_gemeo_identico.log").write_text("\n".join(_log), encoding="utf-8")


if __name__ == "__main__":
    main()
