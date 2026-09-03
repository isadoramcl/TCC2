"""
04_modelos_logisticos.py — Modelos logisticos aninhados
========================================================

PROBLEMA QUE RESOLVE
--------------------
A pergunta do trabalho nao e "qual o melhor classificador de defeitos", e sim
se existe uma relacao INTERPRETAVEL e ESTAVEL entre complexidade e risco basal
de defeito, que possa depois ser transferida ordinalmente para tarefas de
projetos de engenharia.

Uma frequencia bruta de defeitos por faixa de complexidade nao serve para isso,
porque os projetos tem taxas de defeito muito diferentes entre si (de 2,15% no
PC2 a 35,20% no MC2, conforme o script 02). Se os projetos mais complexos forem
tambem os mais propensos a defeito por outras razoes (dominio, processo, rigor
de teste), a complexidade levaria o credito de um efeito que nao e dela. Por
isso o efeito do projeto entra no modelo ANTES da complexidade.

ENTRADA
-------
  data/processed/nasa/base_dpp_consolidada.csv

SAIDA
-----
  outputs/tables/04_coeficientes.csv       coeficientes, OR e IC de cada modelo
  outputs/tables/04_comparacao_modelos.csv ajuste e testes entre modelos
  outputs/tables/04_metricas_candidatas.csv comparacao entre metricas de complexidade
  outputs/tables/04_vif.csv                diagnostico de multicolinearidade
  outputs/logs/04_modelos_logisticos.log

CONCEITOS UTILIZADOS
--------------------
REGRESSAO LOGISTICA. O desfecho aqui e binario (o modulo tem defeito ou nao),
entao nao se modela a probabilidade diretamente — ela e limitada ao intervalo
[0,1] e uma reta a extrapolaria. Modela-se o LOG DA CHANCE (log-odds):
    log( p / (1-p) ) = b0 + b1*x1 + b2*x2 + ...
onde p e a probabilidade de defeito. A chance p/(1-p) e quantas vezes o evento
e mais provavel do que o nao-evento.

RAZAO DE CHANCES (odds ratio, OR). E exp(b). Se b1 e o coeficiente da
complexidade ciclomatica, exp(b1) diz por quanto a chance de defeito e
multiplicada a cada aumento de uma unidade na complexidade, mantidas as demais
variaveis constantes. OR = 1 significa nenhum efeito; OR = 1,10 significa +10%
na chance por unidade; OR < 1 significa efeito protetor.

INTERVALO DE CONFIANCA (IC 95%). Faixa de valores compativeis com os dados sob
o modelo. Se o IC do OR contem 1, o efeito nao e distinguivel de "nenhum efeito"
neste nivel de confianca. A LARGURA do intervalo importa tanto quanto o ponto
central: um OR de 1,05 com IC [1,04; 1,06] e uma estimativa precisa; o mesmo
1,05 com IC [0,80; 1,38] nao sustenta conclusao alguma.

TESTE DA RAZAO DE VEROSSIMILHANCA (LRT). Compara dois modelos ANINHADOS (um
contem todas as variaveis do outro, mais algumas). A estatistica
    LR = 2 * (loglik_completo - loglik_reduzido)
segue aproximadamente uma distribuicao qui-quadrado com graus de liberdade
iguais ao numero de parametros adicionais. Responde: as variaveis novas
melhoram o ajuste mais do que se esperaria pelo acaso?

MULTICOLINEARIDADE e VIF. Quando duas variaveis explicativas carregam
praticamente a mesma informacao (por exemplo, tamanho e complexidade, que
crescem juntos), o modelo nao consegue separar seus efeitos: os coeficientes
ficam instaveis e os erros-padrao inflam. O VIF (fator de inflacao da variancia)
mede isso: VIF = 1/(1-R2_j), onde R2_j vem da regressao da variavel j contra
todas as outras. Convencao usual: VIF > 5 merece atencao, VIF > 10 indica
problema serio. Esta e uma convencao de pratica estatistica, nao um limiar
teorico — e usada aqui como criterio declarado, nao como lei.

PSEUDO-R2 (McFadden). 1 - loglik_modelo/loglik_nulo. Nao e a proporcao de
variancia explicada como no R2 linear, e seus valores sao sistematicamente
menores; serve para comparar modelos sobre os MESMOS dados, nao para julgar
qualidade em termos absolutos.

DECISOES METODOLOGICAS DESTA ETAPA
-----------------------------------
1. O projeto de origem entra como efeito fixo (variavel categorica), nao como
   efeito aleatorio. Justificativa: sao 12 projetos conhecidos e fixos, nao uma
   amostra de uma populacao maior de projetos; e o interesse e controlar o
   efeito deles, nao estimar sua distribuicao.

2. As metricas de complexidade sao usadas em escala original E em escala
   log(1+x). Metricas de software sao fortemente assimetricas a direita, e um
   coeficiente linear na escala original e dominado pelos poucos modulos
   extremos. Ambas as versoes sao reportadas; a escolha entre elas e feita por
   ajuste e estabilidade, com o criterio declarado, nao por conveniencia.

3. HALSTEAD_ERROR_EST e analisada, mas sinalizada. Ela e definida na literatura
   como uma ESTIMATIVA do numero de erros derivada do volume do programa
   (B = V/3000). Usa-la para explicar a ocorrencia de defeito e circular: e uma
   previsao de defeito sendo usada para prever defeito. Ela aparece nas tabelas
   por completude, mas nao e candidata a compor o F_base.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. O numero de observacoes usadas em cada modelo deve ser 17.377 (nenhuma
     perda silenciosa por valor ausente).
  2. Os coeficientes do modelo so-projeto devem reproduzir as taxas de defeito
     por projeto calculadas no script 02, quando convertidos de volta a
     probabilidade.
  3. Modelos aninhados devem ter log-verossimilhanca monotonicamente melhor
     conforme se adicionam variaveis (propriedade matematica; se falhar, houve
     problema de convergencia).
"""

import sys
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
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

CAMINHO_LOG = DIR_LOGS / "04_modelos_logisticos.log"
_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


CANDIDATAS = [
    "CYCLOMATIC_COMPLEXITY",
    "DESIGN_COMPLEXITY",
    "ESSENTIAL_COMPLEXITY",
    "HALSTEAD_DIFFICULTY",
    "HALSTEAD_EFFORT",
    "LOC_TOTAL",
    "HALSTEAD_ERROR_EST",   # incluida com ressalva de circularidade
]
CIRCULARES = {"HALSTEAD_ERROR_EST"}


def ajustar(formula: str, dados: pd.DataFrame):
    """Ajusta um modelo logistico e devolve o resultado do statsmodels."""
    return smf.logit(formula, data=dados).fit(disp=0, maxiter=200)


def linhas_de_coeficientes(nome_modelo: str, resultado) -> list[dict]:
    """Extrai coeficiente, erro-padrao, OR e IC 95% de cada termo."""
    ic = resultado.conf_int()
    linhas = []
    for termo in resultado.params.index:
        b = resultado.params[termo]
        linhas.append({
            "modelo": nome_modelo,
            "termo": termo,
            "coeficiente": round(b, 6),
            "erro_padrao": round(resultado.bse[termo], 6),
            "p_valor": resultado.pvalues[termo],
            "razao_de_chances": round(float(np.exp(b)), 6),
            "ic95_inferior": round(float(np.exp(ic.loc[termo, 0])), 6),
            "ic95_superior": round(float(np.exp(ic.loc[termo, 1])), 6),
        })
    return linhas


def teste_razao_verossimilhanca(reduzido, completo) -> tuple[float, int, float]:
    """LRT entre dois modelos aninhados. Devolve (estatistica, gl, p-valor)."""
    lr = 2 * (completo.llf - reduzido.llf)
    gl = int(completo.df_model - reduzido.df_model)
    p = float(stats.chi2.sf(lr, gl)) if gl > 0 else float("nan")
    return float(lr), gl, p


def calcular_vif(dados: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    """
    VIF de cada coluna contra as demais, por regressao linear auxiliar.
    Implementado explicitamente (em vez de importado) para deixar visivel que
    o VIF e apenas 1/(1-R2) da regressao da variavel contra as outras.
    """
    linhas = []
    for alvo in colunas:
        outras = [c for c in colunas if c != alvo]
        X = sm.add_constant(dados[outras])
        r2 = sm.OLS(dados[alvo], X).fit().rsquared
        vif = float("inf") if r2 >= 1 else 1.0 / (1.0 - r2)
        linhas.append({
            "variavel": alvo,
            "r2_contra_as_demais": round(r2, 4),
            "vif": round(vif, 3),
            "situacao": "OK" if vif < 5 else ("atencao" if vif < 10 else "problema serio"),
        })
    return pd.DataFrame(linhas).sort_values("vif", ascending=False)


def main() -> None:
    log("=" * 78)
    log("MODELOS LOGISTICOS — complexidade e risco de defeito")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    base = pd.read_csv(ARQUIVO_BASE)
    log(f"\nBase: {len(base)} observacoes, {base['project'].nunique()} projetos, "
        f"{int(base['defective'].sum())} defeituosos ({base['defective'].mean():.2%})")

    # Versoes em log(1+x) das metricas candidatas.
    for m in CANDIDATAS:
        base[f"log_{m}"] = np.log1p(base[m])

    coeficientes: list[dict] = []
    comparacoes: list[dict] = []

    # -----------------------------------------------------------------
    # Modelos aninhados principais
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("MODELOS ANINHADOS")
    log("=" * 78)

    especificacoes = {
        "M0_nulo": "defective ~ 1",
        "M1_projeto": "defective ~ C(project)",
        "M2_projeto_complexidade": "defective ~ C(project) + log_CYCLOMATIC_COMPLEXITY",
        "M3_projeto_complexidade_tamanho": "defective ~ C(project) + log_CYCLOMATIC_COMPLEXITY + log_LOC_TOTAL",
        "M4_completo": ("defective ~ C(project) + log_CYCLOMATIC_COMPLEXITY + log_LOC_TOTAL "
                        "+ log_DESIGN_COMPLEXITY + log_ESSENTIAL_COMPLEXITY + log_HALSTEAD_DIFFICULTY"),
    }

    modelos = {}
    for nome, formula in especificacoes.items():
        r = ajustar(formula, base)
        modelos[nome] = r
        coeficientes.extend(linhas_de_coeficientes(nome, r))
        log(f"\n{nome}")
        log(f"  formula        : {formula}")
        log(f"  n              : {int(r.nobs)}")
        log(f"  log-verossim.  : {r.llf:.2f}")
        log(f"  pseudo-R2      : {r.prsquared:.4f}")
        log(f"  AIC / BIC      : {r.aic:.1f} / {r.bic:.1f}")

    log("\n" + "-" * 78)
    log("TESTES DE RAZAO DE VEROSSIMILHANCA ENTRE MODELOS ANINHADOS")
    log("-" * 78)
    log(f"  {'comparacao':<48} {'LR':>10} {'gl':>4} {'p':>12}")
    sequencia = list(especificacoes.keys())
    for anterior, atual in zip(sequencia, sequencia[1:]):
        lr, gl, p = teste_razao_verossimilhanca(modelos[anterior], modelos[atual])
        rotulo = f"{anterior} -> {atual}"
        log(f"  {rotulo:<48} {lr:>10.2f} {gl:>4} {p:>12.3e}")
        comparacoes.append({
            "comparacao": rotulo,
            "loglik_reduzido": round(modelos[anterior].llf, 3),
            "loglik_completo": round(modelos[atual].llf, 3),
            "estatistica_LR": round(lr, 3),
            "graus_de_liberdade": gl,
            "p_valor": p,
            "pseudo_r2_completo": round(modelos[atual].prsquared, 5),
            "aic_completo": round(modelos[atual].aic, 2),
        })

    # -----------------------------------------------------------------
    # Comparacao entre metricas candidatas de complexidade
    #
    # Cada metrica entra SOZINHA sobre o modelo so-projeto, de modo que as
    # comparacoes sejam entre iguais.
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("COMPARACAO ENTRE METRICAS CANDIDATAS (cada uma sobre M1_projeto)")
    log("=" * 78)
    log(f"  {'metrica':<24} {'escala':<8} {'OR':>8} {'IC95':>20} {'LR':>9} {'pseudoR2':>9}  obs")

    linhas_candidatas = []
    for metrica in CANDIDATAS:
        for escala, coluna in (("original", metrica), ("log1p", f"log_{metrica}")):
            r = ajustar(f"defective ~ C(project) + {coluna}", base)
            lr, gl, p = teste_razao_verossimilhanca(modelos["M1_projeto"], r)
            b = r.params[coluna]
            ic = r.conf_int().loc[coluna]
            razao = float(np.exp(b))
            ic_baixo, ic_alto = float(np.exp(ic[0])), float(np.exp(ic[1]))
            nota = "CIRCULAR" if metrica in CIRCULARES else ""
            linhas_candidatas.append({
                "metrica": metrica, "escala": escala,
                "coeficiente": round(b, 6),
                "razao_de_chances": round(razao, 5),
                "ic95_inferior": round(ic_baixo, 5),
                "ic95_superior": round(ic_alto, 5),
                "p_valor": r.pvalues[coluna],
                "estatistica_LR_vs_M1": round(lr, 3),
                "pseudo_r2": round(r.prsquared, 5),
                "aic": round(r.aic, 2),
                "ressalva": nota,
            })
            log(f"  {metrica:<24} {escala:<8} {razao:>8.4f} "
                f"[{ic_baixo:>8.4f};{ic_alto:>8.4f}] {lr:>9.1f} {r.prsquared:>9.4f}  {nota}")

    # -----------------------------------------------------------------
    # A complexidade sobrevive ao controle por TAMANHO?
    #
    # Esta e a pergunta decisiva do trabalho. Complexidade e tamanho crescem
    # juntos (Spearman ~0,75): modulos maiores tendem a ter mais caminhos de
    # controle. Se a associacao entre complexidade e defeito desaparecer quando
    # o tamanho e controlado, entao "complexidade" seria apenas tamanho com
    # outro nome, e o eixo do trabalho nao se sustentaria.
    #
    # Testamos a entrada nas duas ordens. Cada teste responde a pergunta
    # "esta variavel acrescenta algo ao que a outra ja explica?".
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("COMPLEXIDADE x TAMANHO: quem sobrevive ao controle do outro")
    log("=" * 78)

    ordem = []
    m_loc = ajustar("defective ~ C(project) + log_LOC_TOTAL", base)
    m_cc = ajustar("defective ~ C(project) + log_CYCLOMATIC_COMPLEXITY", base)
    m_ambos = ajustar("defective ~ C(project) + log_LOC_TOTAL + log_CYCLOMATIC_COMPLEXITY", base)

    for rotulo, reduzido, completo, termo in (
        ("tamanho acrescenta sobre complexidade", m_cc, m_ambos, "log_LOC_TOTAL"),
        ("complexidade acrescenta sobre tamanho", m_loc, m_ambos, "log_CYCLOMATIC_COMPLEXITY"),
    ):
        lr, gl, pv = teste_razao_verossimilhanca(reduzido, completo)
        b = m_ambos.params[termo]
        ic = m_ambos.conf_int().loc[termo]
        log(f"\n  {rotulo}")
        log(f"    LR = {lr:.2f}  gl = {gl}  p = {pv:.3e}")
        log(f"    OR ajustado de {termo} = {float(np.exp(b)):.4f} "
            f"[{float(np.exp(ic[0])):.4f}; {float(np.exp(ic[1])):.4f}]")
        ordem.append({
            "teste": rotulo, "termo": termo,
            "estatistica_LR": round(lr, 3), "graus_de_liberdade": gl, "p_valor": pv,
            "or_ajustado": round(float(np.exp(b)), 5),
            "ic95_inferior": round(float(np.exp(ic[0])), 5),
            "ic95_superior": round(float(np.exp(ic[1])), 5),
        })

    log("\n  OR isolados (cada um sobre M1_projeto, para comparacao):")
    log(f"    log_CYCLOMATIC_COMPLEXITY sozinho : "
        f"{float(np.exp(m_cc.params['log_CYCLOMATIC_COMPLEXITY'])):.4f}")
    log(f"    log_LOC_TOTAL sozinho             : "
        f"{float(np.exp(m_loc.params['log_LOC_TOTAL'])):.4f}")
    log("\n  Leitura: a reducao do OR de uma variavel quando a outra entra no")
    log("  modelo mede quanto do seu efeito aparente era, na verdade, da outra.")

    pd.DataFrame(ordem).to_csv(DIR_TABELAS / "04_complexidade_vs_tamanho.csv",
                               index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # Multicolinearidade
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("MULTICOLINEARIDADE ENTRE AS METRICAS (escala log1p)")
    log("=" * 78)
    colunas_vif = [f"log_{m}" for m in CANDIDATAS]
    vif = calcular_vif(base, colunas_vif)
    log(f"  {'variavel':<30} {'R2 vs demais':>13} {'VIF':>10}  situacao")
    for _, linha in vif.iterrows():
        log(f"  {linha['variavel']:<30} {linha['r2_contra_as_demais']:>13.4f} "
            f"{linha['vif']:>10.2f}  {linha['situacao']}")

    # -----------------------------------------------------------------
    # Correlacao de Spearman entre as metricas
    # -----------------------------------------------------------------
    log("\n" + "-" * 78)
    log("CORRELACAO DE SPEARMAN ENTRE AS METRICAS CANDIDATAS")
    log("(Spearman, e nao Pearson, porque as metricas sao fortemente")
    log(" assimetricas e a relacao entre elas nao e necessariamente linear;")
    log(" Spearman mede associacao monotonica, baseada em postos.)")
    log("-" * 78)
    correlacao = base[CANDIDATAS].corr(method="spearman").round(3)
    cabecalho = "  " + " " * 24 + " ".join(f"{c[:9]:>10}" for c in CANDIDATAS)
    log(cabecalho)
    for nome, linha in correlacao.iterrows():
        log(f"  {nome:<24}" + " ".join(f"{v:>10.3f}" for v in linha.values))
    correlacao.to_csv(DIR_TABELAS / "04_correlacao_spearman.csv", encoding="utf-8")

    # -----------------------------------------------------------------
    # Verificacoes
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("VERIFICACOES")
    log("=" * 78)
    falhas = []

    for nome, r in modelos.items():
        if int(r.nobs) != len(base):
            falhas.append(f"{nome} usou {int(r.nobs)} de {len(base)} observacoes")
    if not falhas:
        log(f"  [OK]    Todos os modelos usaram as {len(base)} observacoes")

    llfs = [modelos[n].llf for n in sequencia]
    if all(b >= a - 1e-6 for a, b in zip(llfs, llfs[1:])):
        log("  [OK]    Log-verossimilhanca melhora monotonicamente nos aninhados")
    else:
        falhas.append("log-verossimilhanca nao monotonica — possivel falha de convergencia")
        log("  [FALHA] Log-verossimilhanca nao monotonica")

    # M1 deve reproduzir as taxas por projeto
    predito = base.assign(p=modelos["M1_projeto"].predict(base)).groupby("project")["p"].mean()
    observado = base.groupby("project")["defective"].mean()
    erro_max = float((predito - observado).abs().max())
    if erro_max < 1e-6:
        log(f"  [OK]    M1 reproduz as taxas por projeto (erro maximo {erro_max:.2e})")
    else:
        falhas.append(f"M1 nao reproduz taxas por projeto (erro {erro_max:.2e})")
        log(f"  [FALHA] M1 nao reproduz taxas por projeto (erro {erro_max:.2e})")

    # -----------------------------------------------------------------
    # Gravacao
    # -----------------------------------------------------------------
    pd.DataFrame(coeficientes).to_csv(DIR_TABELAS / "04_coeficientes.csv", index=False, encoding="utf-8")
    pd.DataFrame(comparacoes).to_csv(DIR_TABELAS / "04_comparacao_modelos.csv", index=False, encoding="utf-8")
    pd.DataFrame(linhas_candidatas).to_csv(DIR_TABELAS / "04_metricas_candidatas.csv", index=False, encoding="utf-8")
    vif.to_csv(DIR_TABELAS / "04_vif.csv", index=False, encoding="utf-8")

    log("\n--- Arquivos gerados ---")
    for n in ("04_coeficientes.csv", "04_comparacao_modelos.csv",
              "04_metricas_candidatas.csv", "04_vif.csv", "04_correlacao_spearman.csv"):
        log(f"  outputs/tables/{n}")

    log("\n" + "=" * 78)
    log("RESULTADO: " + ("CONCLUIDO COM FALHAS" if falhas else "CONCLUIDO, VERIFICACOES OK"))
    for f in falhas:
        log(f"  - {f}")
    log("=" * 78)

    CAMINHO_LOG.write_text("\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
