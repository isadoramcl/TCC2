"""
01_auditar_j60.py — Auditoria e validacao das instancias PSPLIB J60
====================================================================

PROBLEMA QUE RESOLVE
--------------------
O conjunto J60 do PSPLIB fornece a estrutura de execucao de projeto sobre a qual
o modelo do TCC opera: tarefas, precedencias, duracoes e restricoes de recursos.
Antes de construir qualquer indice de dificuldade sobre essas instancias, e
preciso (i) ler os 480 arquivos sem intermediarios, (ii) verificar que sao o que
declaram ser, e (iii) reproduzir os tres parametros de projeto experimental com
que o conjunto foi gerado.

O terceiro ponto nao e formalidade. Se as formulas de NC, RF e RS aplicadas aos
arquivos reproduzirem exatamente a grade de niveis do delineamento, entao a
leitura dos arquivos esta correta E as formulas implementadas sao as corretas --
uma verificacao dupla que dispensa confiar em qualquer transcricao.

ENTRADA
-------
  data/raw/psplib/*.sm   (480 arquivos, somente leitura)

SAIDA
-----
  data/processed/psplib/instancias_j60.csv     uma linha por instancia
  data/processed/psplib/tarefas_j60.csv        uma linha por tarefa (28.800 linhas)
  outputs/tables/psplib_01_grade_parametros.csv
  outputs/logs/psplib_01_auditar_j60.log

PARAMETROS DE DELINEAMENTO — DEFINICOES
----------------------------------------
`[LITERATURA]` KOLISCH, R.; SPRECHER, A.; DREXL, A. Characterization and
Generation of a General Class of Resource-Constrained Project Scheduling
Problems. *Management Science*, v. 41, n. 10, p. 1693-1703, 1995.

  NC — complexidade de rede (network complexity)
      NC = |A| / |V|
      onde |A| e o numero de arcos de precedencia e |V| o numero de nos
      (atividades, incluindo as fictitias de origem e destino). Mede a densidade
      topologica: quantas relacoes de precedencia existem por atividade.

  RF — fator de recursos (resource factor)
      RF = (1/n) * SOMA_j [ (1/K) * SOMA_k  1{ r_jk > 0 } ]
      onde n e o numero de atividades reais, K o numero de tipos de recurso e
      r_jk a demanda da atividade j pelo recurso k. Mede a densidade da matriz
      de coeficientes: a fracao media de tipos de recurso que cada atividade
      requisita. RF = 1 significa que toda atividade usa todos os recursos.

  RS — forca de recursos (resource strength)
      RS_k = ( a_k - r_k^min ) / ( r_k^max - r_k^min )
      onde a_k e a disponibilidade do recurso k;
            r_k^min = max_j r_jk  e a menor disponibilidade que ainda torna o
                      problema viavel (nenhuma atividade isolada pode exceder);
            r_k^max = pico de demanda do recurso k no cronograma de inicios mais
                      cedo (CPM, ignorando restricao de recursos).
      RS = 0 significa recursos no limite minimo de viabilidade; RS = 1 significa
      recursos abundantes a ponto de a restricao deixar de ser ativa.

`[DECISAO]` O calculo de RS exige o cronograma de inicios mais cedo, obtido por
uma passagem para frente sobre o grafo em ordem topologica. A implementacao usa
ordenacao topologica explicita em vez de confiar na numeracao dos arquivos, para
que a leitura nao dependa de uma convencao nao documentada.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. Todos os arquivos devem declarar a mesma estrutura: 62 atividades (60 reais
     mais duas fictitias), 4 recursos renovaveis, nenhum nao renovavel.
  2. O grafo de precedencias deve ser aciclico, com uma unica origem e um unico
     destino.
  3. Os 480 arquivos devem se agrupar em 48 combinacoes de exatamente 10
     instancias, conforme a nomenclatura j60<combinacao>_<instancia>.sm.
  4. VERIFICACAO CENTRAL: dentro de cada combinacao, os valores calculados de
     NC, RF e RS devem ser identicos entre as 10 instancias, e o conjunto de
     valores distintos deve formar uma grade completa de niveis. Se isso
     ocorrer, leitura e formulas estao simultaneamente validadas.
"""

import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
DIR_ENTRADA = RAIZ / "data" / "raw" / "psplib"
DIR_PROCESSADO = RAIZ / "data" / "processed" / "psplib"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
for d in (DIR_PROCESSADO, DIR_TABELAS, DIR_LOGS):
    d.mkdir(parents=True, exist_ok=True)

_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


# ---------------------------------------------------------------------
# Leitura do formato .sm
# ---------------------------------------------------------------------

def ler_sm(caminho: Path) -> dict:
    """
    Interpreta um arquivo .sm do PSPLIB.

    O formato e organizado em blocos separados por linhas de asteriscos:
    cabecalho, informacoes do projeto, PRECEDENCE RELATIONS, REQUESTS/DURATIONS
    e RESOURCEAVAILABILITIES. A leitura e feita por deteccao de secao, sem
    depender de numeros de linha fixos.
    """
    texto = caminho.read_text(encoding="latin-1")
    linhas = texto.splitlines()

    def inteiro_apos(padrao: str):
        for l in linhas:
            if padrao in l:
                achados = re.findall(r"-?\d+", l.split(":", 1)[-1])
                if achados:
                    return int(achados[0])
        return None

    n_nos = inteiro_apos("jobs (incl. supersource/sink )")
    n_renovaveis = inteiro_apos("- renewable")
    n_nao_renovaveis = inteiro_apos("- nonrenewable")
    n_duplo = inteiro_apos("- doubly constrained")
    horizonte = inteiro_apos("horizon")

    sucessores: dict[int, list[int]] = {}
    duracao: dict[int, int] = {}
    demanda: dict[int, list[int]] = {}
    disponibilidade: list[int] = []

    secao = None
    for l in linhas:
        despida = l.strip()
        if not despida or despida.startswith("*") or despida.startswith("-----"):
            continue
        if despida.startswith("PRECEDENCE RELATIONS"):
            secao = "prec"; continue
        if despida.startswith("REQUESTS/DURATIONS"):
            secao = "req"; continue
        if despida.startswith("RESOURCEAVAILABILITIES"):
            secao = "disp"; continue
        if despida.startswith("PROJECT INFORMATION"):
            secao = "proj"; continue

        if secao == "prec":
            if despida.startswith("jobnr"):
                continue
            campos = despida.split()
            if len(campos) >= 3 and campos[0].isdigit():
                j = int(campos[0]); n_suc = int(campos[2])
                sucessores[j] = [int(x) for x in campos[3:3 + n_suc]]
        elif secao == "req":
            if despida.startswith("jobnr"):
                continue
            campos = despida.split()
            if len(campos) >= 3 and campos[0].isdigit():
                j = int(campos[0])
                duracao[j] = int(campos[2])
                demanda[j] = [int(x) for x in campos[3:]]
        elif secao == "disp":
            if despida.startswith("R "):
                continue
            campos = despida.split()
            if all(c.lstrip("-").isdigit() for c in campos) and campos:
                disponibilidade = [int(x) for x in campos]

    return {
        "arquivo": caminho.name,
        "n_nos": n_nos, "horizonte": horizonte,
        "n_renovaveis": n_renovaveis, "n_nao_renovaveis": n_nao_renovaveis,
        "n_duplo": n_duplo,
        "sucessores": sucessores, "duracao": duracao,
        "demanda": demanda, "disponibilidade": disponibilidade,
    }


# ---------------------------------------------------------------------
# Metricas estruturais
# ---------------------------------------------------------------------

def ordem_topologica(sucessores: dict[int, list[int]]) -> list[int] | None:
    """
    Ordenacao topologica por algoritmo de Kahn.

    Devolve None se o grafo contiver ciclo -- o que seria um defeito grave da
    instancia e, portanto, um achado a reportar, nao um erro a silenciar.
    """
    grau_entrada = {j: 0 for j in sucessores}
    for j, sucs in sucessores.items():
        for s in sucs:
            grau_entrada[s] = grau_entrada.get(s, 0) + 1
    fila = [j for j, g in grau_entrada.items() if g == 0]
    ordem = []
    while fila:
        j = fila.pop(0)
        ordem.append(j)
        for s in sucessores.get(j, []):
            grau_entrada[s] -= 1
            if grau_entrada[s] == 0:
                fila.append(s)
    return ordem if len(ordem) == len(grau_entrada) else None


def inicios_mais_cedo(sucessores, duracao, ordem) -> dict[int, int]:
    """Passagem para frente do CPM: ES_j = max sobre predecessores de (ES_i + d_i)."""
    es = {j: 0 for j in ordem}
    for j in ordem:
        for s in sucessores.get(j, []):
            es[s] = max(es[s], es[j] + duracao[j])
    return es


def pico_por_recurso(es, duracao, demanda, n_recursos) -> list[int]:
    """Pico de demanda de cada recurso no cronograma de inicios mais cedo."""
    perfil = defaultdict(lambda: [0] * n_recursos)
    for j, inicio in es.items():
        d = duracao[j]
        if d <= 0:
            continue
        for t in range(inicio, inicio + d):
            for k in range(n_recursos):
                perfil[t][k] += demanda[j][k]
    if not perfil:
        return [0] * n_recursos
    return [max(perfil[t][k] for t in perfil) for k in range(n_recursos)]


def calcular_parametros(inst: dict) -> dict:
    sucessores, duracao, demanda = inst["sucessores"], inst["duracao"], inst["demanda"]
    K = inst["n_renovaveis"]
    nos = sorted(sucessores)
    n_nos = len(nos)

    # NC = arcos / nos
    n_arcos = sum(len(s) for s in sucessores.values())
    nc = n_arcos / n_nos

    # Atividades reais: as que tem duracao positiva ou demanda positiva.
    # As fictitias de origem e destino tem duracao 0 e demanda nula.
    reais = [j for j in nos if duracao.get(j, 0) > 0 or any(demanda.get(j, [0]))]
    n_reais = len(reais)

    # RF = fracao media de tipos de recurso requisitados por atividade real
    rf = sum(sum(1 for k in range(K) if demanda[j][k] > 0) / K for j in reais) / n_reais

    # RS por recurso
    ordem = ordem_topologica(sucessores)
    aciclico = ordem is not None
    rs_por_recurso, rs_medio = [], None
    if aciclico:
        es = inicios_mais_cedo(sucessores, duracao, ordem)
        r_max = pico_por_recurso(es, duracao, demanda, K)
        r_min = [max(demanda[j][k] for j in nos) for k in range(K)]
        a = inst["disponibilidade"]
        for k in range(K):
            denom = r_max[k] - r_min[k]
            rs_por_recurso.append((a[k] - r_min[k]) / denom if denom > 0 else float("nan"))
        validos = [v for v in rs_por_recurso if v == v]
        rs_medio = sum(validos) / len(validos) if validos else float("nan")

    return {
        "n_nos": n_nos, "n_arcos": n_arcos, "n_atividades_reais": n_reais,
        "aciclico": aciclico,
        "NC": nc, "RF": rf, "RS": rs_medio,
        "RS_por_recurso": rs_por_recurso,
        "duracao_total": sum(duracao[j] for j in nos),
        "duracao_media": sum(duracao[j] for j in reais) / n_reais,
        "duracao_maxima": max(duracao[j] for j in reais),
        "makespan_sem_recursos": max(inicios_mais_cedo(sucessores, duracao, ordem).values()) if aciclico else None,
    }


def main() -> None:
    log("=" * 78)
    log("AUDITORIA DAS INSTANCIAS PSPLIB J60")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    arquivos = sorted(DIR_ENTRADA.glob("*.sm"))
    log(f"\nArquivos encontrados: {len(arquivos)}")
    if not arquivos:
        raise SystemExit(f"Nenhum arquivo .sm em {DIR_ENTRADA}")

    padrao = re.compile(r"^j60(\d+)_(\d+)\.sm$")
    registros, tarefas, falhas = [], [], []

    for caminho in arquivos:
        m = padrao.match(caminho.name)
        if not m:
            falhas.append(f"nome fora do padrao esperado: {caminho.name}")
            continue
        combinacao, instancia = int(m.group(1)), int(m.group(2))

        inst = ler_sm(caminho)
        par = calcular_parametros(inst)

        registros.append({
            "arquivo": caminho.name,
            "combinacao": combinacao, "instancia": instancia,
            "n_nos": par["n_nos"], "n_atividades_reais": par["n_atividades_reais"],
            "n_arcos": par["n_arcos"], "aciclico": par["aciclico"],
            "n_recursos_renovaveis": inst["n_renovaveis"],
            "n_recursos_nao_renovaveis": inst["n_nao_renovaveis"],
            "horizonte": inst["horizonte"],
            "NC": round(par["NC"], 6), "RF": round(par["RF"], 6),
            "RS": round(par["RS"], 6) if par["RS"] == par["RS"] else None,
            "duracao_media": round(par["duracao_media"], 4),
            "duracao_maxima": par["duracao_maxima"],
            "makespan_sem_recursos": par["makespan_sem_recursos"],
            "disponibilidades": ";".join(str(x) for x in inst["disponibilidade"]),
        })

        for j in sorted(inst["sucessores"]):
            tarefas.append({
                "arquivo": caminho.name, "combinacao": combinacao, "instancia": instancia,
                "tarefa": j, "duracao": inst["duracao"][j],
                "n_sucessores": len(inst["sucessores"][j]),
                "sucessores": ";".join(str(s) for s in inst["sucessores"][j]),
                **{f"R{k+1}": inst["demanda"][j][k] for k in range(inst["n_renovaveis"])},
            })

    df = pd.DataFrame(registros)
    dft = pd.DataFrame(tarefas)

    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("ESTRUTURA DECLARADA")
    log("=" * 78)
    for coluna, esperado in (("n_nos", 62), ("n_atividades_reais", 60),
                             ("n_recursos_renovaveis", 4), ("n_recursos_nao_renovaveis", 0)):
        valores = sorted(df[coluna].unique())
        ok = valores == [esperado]
        log(f"  {coluna:<28} valores distintos: {valores}  {'[OK]' if ok else '[ATENCAO]'}")
        if not ok:
            falhas.append(f"{coluna} nao uniforme: {valores}")
    n_ciclicos = int((~df["aciclico"]).sum())
    log(f"  {'grafos aciclicos':<28} {len(df) - n_ciclicos}/{len(df)}  "
        f"{'[OK]' if n_ciclicos == 0 else '[FALHA]'}")
    if n_ciclicos:
        falhas.append(f"{n_ciclicos} instancias com ciclo")

    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("GRADE DE PARAMETROS RECONSTRUIDA A PARTIR DOS ARQUIVOS")
    log("=" * 78)

    grupos = df.groupby("combinacao")
    log(f"  Combinacoes encontradas : {len(grupos)}")
    tamanhos = sorted(grupos.size().unique())
    log(f"  Instancias por combinacao: {tamanhos}  "
        f"{'[OK]' if tamanhos == [10] else '[ATENCAO]'}")
    if tamanhos != [10]:
        falhas.append(f"tamanhos de combinacao irregulares: {tamanhos}")

    # -----------------------------------------------------------------
    # NIVEL REALIZADO x NIVEL NOMINAL
    #
    # NC e RF saem exatamente constantes dentro de cada combinacao. O RS, nao:
    # seus valores se agrupam em torno de poucos patamares sem coincidir com
    # eles. A causa e estrutural, nao um defeito da leitura: a disponibilidade
    # a_k precisa ser um inteiro, de modo que o gerador nao consegue realizar o
    # RS pretendido exatamente e arredonda. O RS efetivamente realizado desvia,
    # portanto, do RS nominal do delineamento.
    #
    # Consequencia metodologica: o nivel nominal e uma variavel de projeto
    # experimental (um fator), enquanto o RS realizado e uma variavel continua
    # medida. Confundir os dois levaria a tratar ruido de arredondamento como
    # variacao de tratamento. Abaixo os niveis nominais sao RECONSTRUIDOS a
    # partir dos dados, por agrupamento, e nao assumidos de nenhuma tabela.
    # -----------------------------------------------------------------
    log("\n" + "-" * 78)
    log("RECONSTRUCAO DOS NIVEIS NOMINAIS")
    log("-" * 78)

    resumo = grupos.agg(
        NC=("NC", "first"), RF=("RF", "first"),
        RS_medio=("RS", "mean"), RS_min=("RS", "min"), RS_max=("RS", "max"),
        n=("arquivo", "size"),
    ).reset_index()

    for p_nome in ("NC", "RF"):
        constante = all(g[p_nome].nunique() == 1 for _, g in grupos)
        log(f"  {p_nome}: constante dentro de cada combinacao? {constante}")
    rs_constante = all(g["RS"].nunique() == 1 for _, g in grupos)
    log(f"  RS: constante dentro de cada combinacao? {rs_constante}")

    def agrupar_em_niveis(valores, k):
        """
        Agrupa valores ordenados em k grupos, cortando nos k-1 maiores saltos.
        Deriva os patamares dos proprios dados, sem supor quais sao.
        """
        ordenados = sorted(valores)
        saltos = sorted(range(1, len(ordenados)),
                        key=lambda i: ordenados[i] - ordenados[i - 1], reverse=True)
        cortes = sorted(saltos[:k - 1])
        grupos_, anterior = [], 0
        for c in cortes + [len(ordenados)]:
            grupos_.append(ordenados[anterior:c]); anterior = c
        return grupos_

    n_nc = resumo["NC"].round(6).nunique()
    n_rf = resumo["RF"].round(6).nunique()
    n_rs = len(resumo) // (n_nc * n_rf) if n_nc * n_rf else 0
    log(f"\n  Niveis de NC: {n_nc} | niveis de RF: {n_rf}")
    log(f"  Logo, para {len(resumo)} combinacoes, o delineamento exige {n_rs} niveis de RS.")

    faixas_rs = agrupar_em_niveis(resumo["RS_medio"].tolist(), n_rs)
    mapa_rs = {}
    log(f"\n  {'nivel':>6} {'combinacoes':>12} {'RS realizado (min - max)':>28} {'media':>9}")
    for i, faixa in enumerate(faixas_rs, start=1):
        media = sum(faixa) / len(faixa)
        log(f"  {i:>6} {len(faixa):>12} {min(faixa):>13.4f} - {max(faixa):<12.4f} {media:>9.4f}")
        for v in faixa:
            mapa_rs[round(v, 9)] = i

    resumo["nivel_RS"] = resumo["RS_medio"].round(9).map(mapa_rs)
    resumo["nivel_NC"] = resumo["NC"].rank(method="dense").astype(int)
    resumo["nivel_RF"] = resumo["RF"].rank(method="dense").astype(int)

    celulas = resumo.groupby(["nivel_NC", "nivel_RF", "nivel_RS"]).size()
    log(f"\n  Celulas do delineamento fatorial : {n_nc} x {n_rf} x {n_rs} = {n_nc * n_rf * n_rs}")
    log(f"  Celulas efetivamente preenchidas  : {len(celulas)}")
    log(f"  Combinacoes por celula            : {sorted(celulas.unique())}")
    if len(celulas) == n_nc * n_rf * n_rs and sorted(celulas.unique()) == [1]:
        log("  [OK]    Delineamento fatorial completo e balanceado, "
            f"{n_nc}x{n_rf}x{n_rs}, 10 instancias por celula")
    else:
        falhas.append("delineamento fatorial incompleto ou desbalanceado")
        log("  [FALHA] Delineamento nao e fatorial completo balanceado")

    desvio = (resumo["RS_max"] - resumo["RS_min"]).max()
    log(f"\n  Maior amplitude de RS realizado dentro de uma combinacao: {desvio:.4f}")
    log("  Interpretacao: e a margem de arredondamento do gerador, nao variacao")
    log("  de tratamento. O nivel nominal deve ser usado como fator; o RS")
    log("  realizado, se necessario, como covariavel continua.")

    log("\n  Grade final (nivel nominal -> valores realizados):")
    log(f"    {'comb':>5} {'nvNC':>5} {'nvRF':>5} {'nvRS':>5} {'NC':>8} {'RF':>8} {'RS medio':>9}")
    for _, r in resumo.sort_values(["nivel_NC", "nivel_RF", "nivel_RS"]).iterrows():
        log(f"    {int(r['combinacao']):>5} {int(r['nivel_NC']):>5} {int(r['nivel_RF']):>5} "
            f"{int(r['nivel_RS']):>5} {r['NC']:>8.4f} {r['RF']:>8.4f} {r['RS_medio']:>9.4f}")

    grade = resumo

    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("DESCRITIVAS DAS TAREFAS")
    log("=" * 78)
    reais = dft[(dft["duracao"] > 0)]
    log(f"  Tarefas registradas (todas)   : {len(dft)}")
    log(f"  Tarefas com duracao positiva  : {len(reais)}")
    log(f"  Duracao   min/mediana/max     : {reais['duracao'].min()} / "
        f"{reais['duracao'].median():.1f} / {reais['duracao'].max()}")
    log(f"  Sucessores min/mediana/max    : {dft['n_sucessores'].min()} / "
        f"{dft['n_sucessores'].median():.1f} / {dft['n_sucessores'].max()}")

    # -----------------------------------------------------------------
    df.to_csv(DIR_PROCESSADO / "instancias_j60.csv", index=False, encoding="utf-8")
    dft.to_csv(DIR_PROCESSADO / "tarefas_j60.csv", index=False, encoding="utf-8")
    grade.to_csv(DIR_TABELAS / "psplib_01_grade_parametros.csv", index=False, encoding="utf-8")

    log("\n--- Arquivos gerados ---")
    log(f"  data/processed/psplib/instancias_j60.csv  ({len(df)} linhas)")
    log(f"  data/processed/psplib/tarefas_j60.csv     ({len(dft)} linhas)")
    log(f"  outputs/tables/psplib_01_grade_parametros.csv ({len(grade)} linhas)")

    log("\n" + "=" * 78)
    log("RESULTADO: " + ("CONCLUIDO COM RESSALVAS" if falhas else "CONCLUIDO, VERIFICACOES OK"))
    for f in falhas:
        log(f"  - {f}")
    log("=" * 78)

    (DIR_LOGS / "psplib_01_auditar_j60.log").write_text("\n".join(_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
