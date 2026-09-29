"""
01_derivar_parametros.py — Camada 1: parâmetros derivados da própria base
==========================================================================

PROBLEMA QUE RESOLVE
--------------------
Vários parâmetros do simulador foram inicialmente arbitrados por falta de base.
Alguns deles, porém, são OBSERVÁVEIS na instância de projeto fornecida: o número
de pessoas que faz sentido alocar, o horizonte de execução e a escala da pressão
de cronograma decorrem da estrutura da rede e da disponibilidade de recursos.

Este script os deriva por procedimento documentado, e não por escolha. A
consequência prática é que, ao trocar a base -- por exemplo, por um projeto real
--, os parâmetros são recalculados automaticamente, sem reedição de código.

ENTRADA
-------
  data/processed/psplib/tarefas_j60_com_di.csv
  data/processed/psplib/instancias_j60.csv
  config/parametros.yaml   (valores de partida; este script sobrescreve os derivados)

SAIDA
-----
  config/parametros_derivados.yaml    apenas os parâmetros derivados, com procedência
  outputs/tables/modelo_01_derivacao.csv
  outputs/logs/modelo_01_derivar_parametros.log

MÉTODO
------
`[DEC]` O escalonamento de referência usa o **serial schedule generation scheme**
(SGS serial) com regra de prioridade por **menor folga total**. Justificativa: é
o esquema construtivo padrão da literatura de RCPSP, e a regra de menor folga
(equivalente a LFT em redes com prazo único) está entre as regras de prioridade
clássicas avaliadas por Kolisch (1996). Não se busca aqui o escalonamento ótimo
-- busca-se um escalonamento VIÁVEL e reprodutível que sirva de referência para
dimensionar equipe, horizonte e pressão.
Fonte: KOLISCH, R. Serial and parallel resource-constrained project scheduling
methods revisited: theory and computation. *European Journal of Operational
Research*, v. 90, n. 2, p. 320-333, 1996.

PARÂMETROS DERIVADOS
--------------------
  n_agentes            — número de tarefas simultâneas no escalonamento de
                         referência. Justificativa: a equipe que faz sentido
                         alocar é a que a disponibilidade de recursos comporta;
                         mais pessoas do que isso ficariam ociosas por restrição
                         de recurso, não por falta de trabalho.
  horizonte_maximo     — múltiplo do makespan do CPM suficiente para acomodar o
                         pior atraso por recursos observado, com margem.
  escala_pressao       — razão entre o makespan com recursos e o do CPM, que é o
                         atraso estrutural que o gestor observa mesmo sem
                         nenhuma degradação humana. Define o ponto em que P(t)
                         atinge seu máximo.

COMO VERIFICAMOS
----------------
  1. O makespan com recursos nunca pode ser menor que o do CPM.
  2. Nenhum período pode exceder a disponibilidade de qualquer recurso.
  3. Toda precedência respeitada: nenhuma tarefa inicia antes de seus
     predecessores terminarem.
  4. Todas as 60 tarefas reais escalonadas em cada instância.
"""

import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
DIR_PROC = RAIZ / "data" / "processed" / "psplib"
DIR_CONFIG = RAIZ / "config"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
for d in (DIR_CONFIG, DIR_TABELAS, DIR_LOGS):
    d.mkdir(parents=True, exist_ok=True)

_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def sgs_serial(tarefas: pd.DataFrame, disponibilidade: list[int], colunas_recurso: list[str]):
    """
    Serial SGS com prioridade por menor folga total.

    A cada passo escolhe entre as tarefas ELEGÍVEIS -- aquelas cujos
    predecessores já foram escalonados -- e aloca no primeiro instante viável em
    recursos. Devolve (inicio, fim, makespan, ativas_por_periodo, uso_por_periodo).
    """
    dur = dict(zip(tarefas["tarefa"], tarefas["duracao"]))
    folga = dict(zip(tarefas["tarefa"], tarefas["folga_total"]))
    demanda = {r.tarefa: [getattr(r, c) for c in colunas_recurso] for r in tarefas.itertuples()}
    sucessores = {
        r.tarefa: ([int(x) for x in str(r.sucessores).split(";")]
                   if isinstance(r.sucessores, str) and r.sucessores.strip() else [])
        for r in tarefas.itertuples()
    }
    predecessores = defaultdict(set)
    for j, ss in sucessores.items():
        for s in ss:
            if s in dur:
                predecessores[s].add(j)

    K = len(colunas_recurso)
    inicio, fim = {}, {}
    uso = defaultdict(lambda: [0] * K)
    restantes = set(dur)

    while restantes:
        elegiveis = [j for j in restantes if predecessores[j] <= set(fim)]
        if not elegiveis:
            raise RuntimeError("nenhuma tarefa elegível — grafo inconsistente")
        # desempate determinístico pelo número da tarefa, para reprodutibilidade
        j = min(elegiveis, key=lambda x: (folga[x], -dur[x], x))
        t0 = max([fim[p] for p in predecessores[j]], default=0)
        while True:
            cabe = all(
                all(uso[tt][k] + demanda[j][k] <= disponibilidade[k] for k in range(K))
                for tt in range(t0, t0 + max(dur[j], 1))
            )
            if cabe:
                break
            t0 += 1
        for tt in range(t0, t0 + dur[j]):
            for k in range(K):
                uso[tt][k] += demanda[j][k]
        inicio[j], fim[j] = t0, t0 + dur[j]
        restantes.discard(j)

    makespan = max(fim.values())
    ativas = [sum(1 for j in dur if inicio[j] <= tt < fim[j]) for tt in range(makespan)]
    return inicio, fim, makespan, ativas, uso


def main() -> None:
    log("=" * 78)
    log("CAMADA 1 — PARÂMETROS DERIVADOS DA BASE")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    tarefas = pd.read_csv(DIR_PROC / "tarefas_j60_com_di.csv")
    instancias = pd.read_csv(DIR_PROC / "instancias_j60.csv")
    colunas_recurso = [c for c in tarefas.columns if c.startswith("R") and c[1:].isdigit()]
    disponibilidades = {
        r.arquivo: [int(x) for x in str(r.disponibilidades).split(";")]
        for r in instancias.itertuples()
    }
    log(f"\nInstancias : {tarefas['arquivo'].nunique()}")
    log(f"Recursos   : {colunas_recurso}")

    registros, falhas = [], []
    for arquivo, g in tarefas.groupby("arquivo", sort=True):
        a = disponibilidades[arquivo]
        inicio, fim, makespan, ativas, uso = sgs_serial(g, a, colunas_recurso)
        cpm = int(instancias.loc[instancias["arquivo"] == arquivo, "makespan_sem_recursos"].iloc[0])

        # --- verificações, por instância ---
        if makespan < cpm:
            falhas.append(f"{arquivo}: makespan {makespan} < CPM {cpm}")
        if len(fim) != len(g):
            falhas.append(f"{arquivo}: {len(fim)} de {len(g)} tarefas escalonadas")
        for tt, u in uso.items():
            for k in range(len(colunas_recurso)):
                if u[k] > a[k]:
                    falhas.append(f"{arquivo}: recurso {k+1} excedido em t={tt}")
                    break

        registros.append({
            "arquivo": arquivo,
            "combinacao": int(g["combinacao"].iloc[0]),
            "makespan_cpm": cpm,
            "makespan_recursos": makespan,
            "razao_makespan": makespan / cpm,
            "ativas_media": float(np.mean(ativas)),
            "ativas_p90": float(np.percentile(ativas, 90)),
            "ativas_max": int(max(ativas)),
        })

    d = pd.DataFrame(registros)

    log("\n" + "=" * 78)
    log("VERIFICACOES DO ESCALONAMENTO DE REFERENCIA")
    log("=" * 78)
    if falhas:
        log(f"  [FALHA] {len(falhas)} violacoes:")
        for f in falhas[:8]:
            log(f"    {f}")
    else:
        log(f"  [OK]    {len(d)} instancias escalonadas sem violar precedencia,")
        log( "          recursos, nem produzir makespan inferior ao do CPM")
    log(f"  Razao makespan_recursos/CPM  minima: {d.razao_makespan.min():.4f} "
        f"(deve ser >= 1)")

    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("PARAMETROS DERIVADOS")
    log("=" * 78)

    n_agentes = int(round(d["ativas_p90"].mean()))
    log(f"\n  n_agentes = {n_agentes}")
    log(f"    tarefas simultaneas — media das medias : {d.ativas_media.mean():.2f}")
    log(f"    tarefas simultaneas — media do p90     : {d.ativas_p90.mean():.2f}  <- adotado")
    log(f"    tarefas simultaneas — media do maximo  : {d.ativas_max.mean():.2f}")
    log( "    Adotado o p90 e nao o maximo: o maximo e um pico transitorio, e")
    log( "    dimensionar a equipe pelo pico deixaria agentes ociosos a maior")
    log( "    parte do tempo. O p90 cobre a carga sustentada.")

    # O horizonte precisa cobrir DOIS efeitos multiplicativos: o atraso
    # estrutural por restricao de recursos (medido) e a inflacao de duracao
    # causada pela queda de produtividade (equacao 3 do TCC I). No pior caso a
    # produtividade e mu_minimo^2, de modo que a duracao infla por 1/mu_minimo^2.
    # A primeira versao deste script ignorava o segundo efeito e produzia
    # horizonte curto demais: instancias eram interrompidas com tarefas ainda em
    # execucao, o que seria lido como "projeto nao converge" quando na verdade
    # era o horizonte que faltava.
    import yaml as _yaml
    mu_min = float(_yaml.safe_load(
        (RAIZ / "config" / "parametros.yaml").read_text(encoding="utf-8")
    )["fuzzy"]["mu_minimo"]["valor"])
    razao_max = float(d["razao_makespan"].max())
    inflacao_pior = 1.0 / (mu_min ** 2)
    horizonte = int(np.ceil(razao_max * inflacao_pior))
    log(f"\n  horizonte_maximo_fator = {horizonte}")
    log(f"    maior razao makespan/CPM observada : {razao_max:.4f}")
    log(f"    mu_minimo                          : {mu_min:.4f}")
    log(f"    inflacao de duracao no pior caso   : 1/mu_minimo^2 = {inflacao_pior:.4f}")
    log( "    O horizonte cobre o produto dos dois efeitos. Nao terminar dentro")
    log( "    dele passa a ser ACHADO -- configuracao degenerada -- e nao artefato")
    log( "    de horizonte apertado.")

    escala_pressao = float(d["razao_makespan"].quantile(0.90))
    log(f"\n  escala_pressao = {escala_pressao:.4f}")
    log(f"    p90 da razao makespan_recursos/CPM")
    log( "    Interpretacao: atraso estrutural que o gestor observa mesmo sem")
    log( "    nenhuma degradacao humana. P(t) atinge o maximo quando o atraso")
    log( "    relativo alcanca esse valor.")

    derivados = {
        "versao": "1.0",
        "origem": "derivado de data/processed/psplib/ pelo script src/modelo/01_derivar_parametros.py",
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "procedimento": ("serial SGS com prioridade por menor folga total; "
                         "KOLISCH, R. EJOR v.90 n.2 p.320-333, 1996"),
        "n_agentes": {
            "valor": n_agentes, "condicao": "derivado",
            "fonte": "media do p90 de tarefas simultaneas no escalonamento de referencia",
            "estatisticas": {
                "media_das_medias": round(float(d.ativas_media.mean()), 4),
                "media_do_p90": round(float(d.ativas_p90.mean()), 4),
                "media_do_maximo": round(float(d.ativas_max.mean()), 4),
                "faixa_do_maximo": [int(d.ativas_max.min()), int(d.ativas_max.max())],
            },
            "varredura": sorted({max(1, n_agentes - 2), n_agentes, n_agentes + 3}),
        },
        "horizonte_maximo_fator": {
            "valor": horizonte, "condicao": "derivado",
            "fonte": "razao makespan_recursos/CPM maxima multiplicada por 1/mu_minimo^2",
            "razao_maxima_observada": round(razao_max, 4),
            "inflacao_por_produtividade": round(inflacao_pior, 4),
        },
        "escala_pressao": {
            "valor": round(escala_pressao, 4), "condicao": "derivado",
            "fonte": "p90 da razao makespan_recursos/CPM",
            "razao_mediana": round(float(d.razao_makespan.median()), 4),
            "razao_media": round(float(d.razao_makespan.mean()), 4),
        },
    }

    (DIR_CONFIG / "parametros_derivados.yaml").write_text(
        yaml.safe_dump(derivados, allow_unicode=True, sort_keys=False), encoding="utf-8")
    d.to_csv(DIR_TABELAS / "modelo_01_derivacao.csv", index=False, encoding="utf-8")

    log("\n--- Arquivos gerados ---")
    log("  config/parametros_derivados.yaml")
    log(f"  outputs/tables/modelo_01_derivacao.csv ({len(d)} linhas)")

    log("\n" + "=" * 78)
    log("RESULTADO: " + ("CONCLUIDO COM FALHAS" if falhas else "CONCLUIDO, VERIFICACOES OK"))
    log("=" * 78)

    (DIR_LOGS / "modelo_01_derivar_parametros.log").write_text("\n".join(_log) + "\n",
                                                               encoding="utf-8")
    if falhas:
        sys.exit(1)


if __name__ == "__main__":
    main()
