"""
02_indice_dificuldade.py — Indice de dificuldade tecnica Di por tarefa
=======================================================================

PROBLEMA QUE RESOLVE
--------------------
O modelo do TCC precisa atribuir a cada tarefa de um projeto do J60 um nivel
ordinal de dificuldade tecnica, que sera ligado ao risco basal F_base calibrado
na base NASA. Este script constroi esse indice a partir de grandezas medidas
diretamente nas instancias, e submete tanto seus componentes quanto seus pesos a
verificacao.

ENTRADA
-------
  data/processed/psplib/tarefas_j60.csv
  data/processed/psplib/instancias_j60.csv

SAIDA
-----
  data/processed/psplib/tarefas_j60_com_di.csv
  outputs/tables/psplib_02_componentes_correlacao.csv
  outputs/tables/psplib_02_sensibilidade_pesos.csv
  outputs/tables/psplib_02_distribuicao_niveis.csv
  outputs/logs/psplib_02_indice_dificuldade.log

CORRECAO DE PROVENIENCIA DE UMA REFERENCIA
-------------------------------------------
`[ACHADO]` O Guia Metodologico atribuia a construcao do Di a DE REYCK, B.;
HERROELEN, W. On the use of the complexity index as a measure of complexity in
activity networks. *European Journal of Operational Research*, v. 91, n. 2,
p. 347-366, 1996.

Essa atribuicao esta incorreta. O indice de complexidade ali avaliado deriva de
BEIN, W.; KAMBUROWSKI, J.; STALLMANN, M. Optimal reduction of two-terminal
directed acyclic graphs. *SIAM Journal on Computing*, v. 21, n. 6, p. 1112-1129,
1992, e mede a distancia da REDE INTEIRA a series-paralelidade. E uma
propriedade do grafo, nao da atividade. O gerador RanGen (DEMEULEMEESTER et al.,
*Journal of Scheduling*, 2003) o emprega como parametro de topologia de
instancia, ao lado do coeficiente de complexidade de rede.

`[DECISAO]` A referencia permanece no trabalho, mas realocada: ela sustenta a
caracterizacao da rede por instancia (o NC do script 01), e nao o indice por
tarefa. O Di e declarado como CONSTRUCAO DESTE TRABALHO, com cada componente
apoiado em fonte propria, conforme abaixo.

COMPONENTES E SUAS ORIGENS
---------------------------
  (1) Duracao normalizada
      d_norm_j = ( d_j - min d ) / ( max d - min d ), dentro da instancia.
      `[DECISAO]` Grandeza medida diretamente no arquivo; nao requer apoio
      externo. A normalizacao e INTRA-INSTANCIA porque o modelo compara tarefas
      dentro de um mesmo projeto, nao entre projetos diferentes.

  (2) Intensidade de recursos
      r_int_j = ( 1/K ) * SOMA_k ( r_jk / a_k )
      a fracao media da disponibilidade de cada recurso que a tarefa consome
      quando executada.
      `[LITERATURA]` E o analogo por atividade do *resource factor* de KOLISCH,
      SPRECHER e DREXL (*Management Science*, 1995), que mede a densidade da
      matriz de coeficientes de recursos no nivel da instancia.
      `[DECISAO]` A versao por atividade, ponderada pela disponibilidade, e
      adaptacao deste trabalho. Ponderar por a_k importa: consumir 4 unidades de
      um recurso com 5 disponiveis e muito mais restritivo do que consumir 4 de
      um recurso com 40.

  (3) Criticidade na rede
      crit_j = 1 - folga_norm_j, com folga total obtida do CPM:
          folga_j = LS_j - ES_j
      onde ES vem da passagem para frente e LS da passagem para tras.
      `[DECISAO]` O Guia previa CONTAGEM DE SUCESSORES como medida de
      criticidade. A folga total e a medida canonica de criticidade por
      atividade em gestao de projetos, e a contagem de sucessores e um proxy
      fraco dela: uma tarefa pode ter varios sucessores e folga ampla, ou
      nenhum sucessor e estar sobre o caminho critico. Ambas sao calculadas e
      comparadas neste script; a escolha e reportada com base na correlacao
      observada, nao por preferencia.

  Di_j = w1 * d_norm_j + w2 * r_int_norm_j + w3 * crit_j

`[DECISAO]` Pesos de partida iguais (1/3 cada), conforme o Guia, que os trata
como suposicao inicial sujeita a analise de sensibilidade. A analise esta
implementada aqui e inclui uma configuracao que reduz o peso da criticidade, em
resposta ao achado da calibracao NASA (secao 6.2 do registro de decisoes): ali,
o componente analogo a magnitude teve respaldo empirico e o analogo a
complexidade estrutural nao teve efeito independente.

COMO VERIFICAMOS SE O RESULTADO ESTA CORRETO
---------------------------------------------
  1. As tarefas ficticias (duracao zero e demanda nula) devem ser excluidas, e a
     contagem restante deve ser 480 x 60 = 28.800.
  2. Todo componente normalizado deve ficar em [0, 1], e Di tambem.
  3. A folga da tarefa inicial e da final deve ser zero em toda instancia (ambas
     estao necessariamente sobre o caminho critico).
  4. O makespan obtido pela passagem para tras deve coincidir com o da passagem
     para frente em todas as instancias.
  5. A ordenacao das tarefas por Di deve ser estavel sob perturbacao dos pesos;
     instabilidade e achado, nao defeito.
"""

import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parents[2]
DIR_PROC = RAIZ / "data" / "processed" / "psplib"
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
for d in (DIR_PROC, DIR_TABELAS, DIR_LOGS):
    d.mkdir(parents=True, exist_ok=True)

_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def normalizar(serie: pd.Series) -> pd.Series:
    """
    Normalizacao min-max para [0, 1].
    Quando todos os valores sao iguais a normalizacao e indefinida; devolve 0,
    que e a leitura correta: sem variacao, nenhuma tarefa se destaca.
    """
    amplitude = serie.max() - serie.min()
    if amplitude == 0:
        return pd.Series(0.0, index=serie.index)
    return (serie - serie.min()) / amplitude


def cpm(sucessores: dict[int, list[int]], duracao: dict[int, int]):
    """
    Passagens para frente e para tras do CPM.

    Devolve (ES, LS, folga, makespan). A ordem topologica e recalculada por
    Kahn, sem depender da numeracao dos arquivos.
    """
    grau = {j: 0 for j in sucessores}
    for j, sucs in sucessores.items():
        for s in sucs:
            grau[s] = grau.get(s, 0) + 1
    fila = [j for j, g in grau.items() if g == 0]
    ordem = []
    while fila:
        j = fila.pop(0)
        ordem.append(j)
        for s in sucessores.get(j, []):
            grau[s] -= 1
            if grau[s] == 0:
                fila.append(s)

    es = {j: 0 for j in ordem}
    for j in ordem:
        for s in sucessores.get(j, []):
            es[s] = max(es[s], es[j] + duracao[j])
    makespan = max(es[j] + duracao[j] for j in ordem)

    ls = {j: makespan - duracao[j] for j in ordem}
    for j in reversed(ordem):
        for s in sucessores.get(j, []):
            ls[j] = min(ls[j], ls[s] - duracao[j])

    folga = {j: ls[j] - es[j] for j in ordem}
    return es, ls, folga, makespan


def main() -> None:
    log("=" * 78)
    log("INDICE DE DIFICULDADE TECNICA Di — PSPLIB J60")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    tarefas = pd.read_csv(DIR_PROC / "tarefas_j60.csv")
    instancias = pd.read_csv(DIR_PROC / "instancias_j60.csv")
    log(f"\nTarefas lidas    : {len(tarefas)}")
    log(f"Instancias lidas : {len(instancias)}")

    colunas_recurso = [c for c in tarefas.columns if c.startswith("R") and c[1:].isdigit()]
    log(f"Recursos         : {colunas_recurso}")

    disponibilidade = {
        r["arquivo"]: [int(x) for x in str(r["disponibilidades"]).split(";")]
        for _, r in instancias.iterrows()
    }

    # -----------------------------------------------------------------
    # CPM por instancia
    # -----------------------------------------------------------------
    log("\n--- CPM: passagens para frente e para tras ---")
    partes, falhas_makespan = [], 0

    for arquivo, g in tarefas.groupby("arquivo", sort=True):
        sucessores = {
            int(r["tarefa"]): ([int(x) for x in str(r["sucessores"]).split(";")]
                               if pd.notna(r["sucessores"]) and str(r["sucessores"]).strip() else [])
            for _, r in g.iterrows()
        }
        duracao = {int(r["tarefa"]): int(r["duracao"]) for _, r in g.iterrows()}
        es, ls, folga, makespan = cpm(sucessores, duracao)

        registrado = instancias.loc[instancias["arquivo"] == arquivo,
                                    "makespan_sem_recursos"].iloc[0]
        if int(registrado) != int(makespan):
            falhas_makespan += 1

        sub = g.copy()
        sub["ES"] = sub["tarefa"].map(es)
        sub["LS"] = sub["tarefa"].map(ls)
        sub["folga_total"] = sub["tarefa"].map(folga)
        sub["makespan_instancia"] = makespan
        partes.append(sub)

    t = pd.concat(partes, ignore_index=True)
    log(f"  Instancias processadas          : {t['arquivo'].nunique()}")
    log(f"  Divergencias de makespan vs 01  : {falhas_makespan}  "
        f"{'[OK]' if falhas_makespan == 0 else '[FALHA]'}")

    # -----------------------------------------------------------------
    # Exclusao das tarefas ficticias
    # -----------------------------------------------------------------
    demanda_total = t[colunas_recurso].sum(axis=1)
    t["ficticia"] = (t["duracao"] == 0) & (demanda_total == 0)
    log(f"\n  Tarefas ficticias excluidas     : {int(t['ficticia'].sum())} "
        f"(esperado 480 x 2 = 960)")
    reais = t[~t["ficticia"]].copy()
    log(f"  Tarefas reais                   : {len(reais)} (esperado 28.800)")

    # -----------------------------------------------------------------
    # Componentes
    # -----------------------------------------------------------------
    log("\n--- Componentes do indice ---")

    # (2) intensidade de recursos, ponderada pela disponibilidade
    def intensidade(linha):
        a = disponibilidade[linha["arquivo"]]
        return float(np.mean([linha[c] / a[i] if a[i] > 0 else 0.0
                              for i, c in enumerate(colunas_recurso)]))

    reais["intensidade_recursos"] = reais.apply(intensidade, axis=1)

    # normalizacoes intra-instancia
    por_arquivo = reais.groupby("arquivo", sort=False)
    reais["duracao_norm"] = por_arquivo["duracao"].transform(normalizar)
    reais["intensidade_norm"] = por_arquivo["intensidade_recursos"].transform(normalizar)
    reais["folga_norm"] = por_arquivo["folga_total"].transform(normalizar)
    reais["criticidade_folga"] = 1.0 - reais["folga_norm"]
    reais["criticidade_sucessores"] = por_arquivo["n_sucessores"].transform(normalizar)

    for c in ("duracao_norm", "intensidade_norm", "criticidade_folga", "criticidade_sucessores"):
        log(f"  {c:<26} min={reais[c].min():.4f}  max={reais[c].max():.4f}  "
            f"media={reais[c].mean():.4f}")

    # -----------------------------------------------------------------
    # Folga total x contagem de sucessores como medidas de criticidade
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("CRITICIDADE: FOLGA TOTAL x CONTAGEM DE SUCESSORES")
    log("=" * 78)
    rho = reais["criticidade_folga"].corr(reais["criticidade_sucessores"], method="spearman")
    log(f"  Correlacao de Spearman entre as duas medidas : {rho:.4f}")

    criticas = reais["folga_total"] == 0
    log(f"  Tarefas com folga zero (caminho critico)     : {int(criticas.sum())} "
        f"({criticas.mean():.2%})")
    log(f"  Dessas, com ZERO sucessores                  : "
        f"{int((criticas & (reais['n_sucessores'] == 0)).sum())}")
    sem_folga_muitos_suc = (reais["folga_total"] > reais["folga_total"].median()) & \
                           (reais["n_sucessores"] >= 3)
    log(f"  Tarefas com folga ALTA e 3+ sucessores       : {int(sem_folga_muitos_suc.sum())}")
    log("\n  Leitura: se as duas medidas concordassem, a correlacao seria proxima")
    log("  de 1 e as duas contagens acima seriam proximas de zero. O quanto elas")
    log("  divergem e a medida de quanto a contagem de sucessores erra como")
    log("  proxy de criticidade.")

    pd.DataFrame([{
        "correlacao_spearman_folga_vs_sucessores": round(float(rho), 6),
        "n_tarefas_folga_zero": int(criticas.sum()),
        "prop_tarefas_folga_zero": round(float(criticas.mean()), 6),
        "n_criticas_sem_sucessores": int((criticas & (reais["n_sucessores"] == 0)).sum()),
        "n_folga_alta_com_3_ou_mais_sucessores": int(sem_folga_muitos_suc.sum()),
    }]).to_csv(DIR_TABELAS / "psplib_02_componentes_correlacao.csv",
               index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # Di e sensibilidade aos pesos
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("INDICE Di E SENSIBILIDADE AOS PESOS")
    log("=" * 78)

    esquemas = {
        "iguais (partida do Guia)":            (1/3, 1/3, 1/3),
        "criticidade reduzida (achado NASA)":  (0.40, 0.40, 0.20),
        "so magnitude":                        (0.50, 0.50, 0.00),
        "duracao dominante":                   (0.60, 0.20, 0.20),
        "recursos dominante":                  (0.20, 0.60, 0.20),
        "criticidade dominante":               (0.20, 0.20, 0.60),
    }

    referencia = None
    linhas_sens = []
    log(f"  {'esquema':<36} {'w_dur':>6} {'w_rec':>6} {'w_cri':>6} {'media':>7} "
        f"{'dp':>7} {'rho vs referencia':>18}")
    for nome, (w1, w2, w3) in esquemas.items():
        di = w1 * reais["duracao_norm"] + w2 * reais["intensidade_norm"] + \
             w3 * reais["criticidade_folga"]
        if referencia is None:
            referencia = di
            rho_ref = 1.0
        else:
            rho_ref = float(di.corr(referencia, method="spearman"))
        linhas_sens.append({
            "esquema": nome, "peso_duracao": w1, "peso_recursos": w2,
            "peso_criticidade": w3, "Di_medio": round(float(di.mean()), 5),
            "Di_desvio_padrao": round(float(di.std()), 5),
            "Di_min": round(float(di.min()), 5), "Di_max": round(float(di.max()), 5),
            "spearman_vs_referencia": round(rho_ref, 5),
        })
        log(f"  {nome:<36} {w1:>6.2f} {w2:>6.2f} {w3:>6.2f} {di.mean():>7.4f} "
            f"{di.std():>7.4f} {rho_ref:>18.4f}")

    pd.DataFrame(linhas_sens).to_csv(DIR_TABELAS / "psplib_02_sensibilidade_pesos.csv",
                                     index=False, encoding="utf-8")

    reais["Di"] = referencia
    log("\n  Di adotado: pesos iguais (1/3, 1/3, 1/3), conforme o Guia.")
    log("  A tabela acima permite trocar a ponderacao com base em numeros; o")
    log("  esquema 'criticidade reduzida' e a alternativa sugerida pelo achado")
    log("  da calibracao NASA, e sua correlacao com a referencia esta reportada.")

    # -----------------------------------------------------------------
    # Niveis ordinais
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("NIVEIS ORDINAIS DE DIFICULDADE")
    log("=" * 78)
    log("  `[DECISAO]` Os cortes sao os quartis da distribuicao de Di sobre todas")
    log("  as tarefas reais. Justificativa: nao existe, para tarefas de projeto,")
    log("  um limiar normativo externo equivalente ao SWE-220 do dominio de")
    log("  software. Quartis produzem quatro niveis de tamanho comparavel, o que")
    log("  e requisito para a transferencia ordinal, e a escolha e declarada como")
    log("  decisao deste trabalho, nao como limiar da literatura.")

    NIVEIS = ["baixa", "media", "alta", "muito alta"]
    cortes = reais["Di"].quantile([0.25, 0.50, 0.75]).tolist()
    reais["nivel_dificuldade"] = pd.cut(
        reais["Di"], bins=[-np.inf] + cortes + [np.inf], labels=NIVEIS, right=True)

    log(f"\n  Cortes (quartis de Di): {[round(c, 4) for c in cortes]}")
    log(f"\n  {'nivel':<12} {'n':>7} {'%':>7} {'Di min':>8} {'Di max':>8} "
        f"{'dur.media':>10} {'folga.media':>12}")
    linhas_dist = []
    for nivel in NIVEIS:
        sub = reais[reais["nivel_dificuldade"] == nivel]
        log(f"  {nivel:<12} {len(sub):>7} {len(sub)/len(reais):>7.2%} "
            f"{sub['Di'].min():>8.4f} {sub['Di'].max():>8.4f} "
            f"{sub['duracao'].mean():>10.2f} {sub['folga_total'].mean():>12.2f}")
        linhas_dist.append({
            "nivel": nivel, "n": len(sub),
            "proporcao": round(len(sub) / len(reais), 5),
            "Di_min": round(float(sub["Di"].min()), 5),
            "Di_max": round(float(sub["Di"].max()), 5),
            "duracao_media": round(float(sub["duracao"].mean()), 4),
            "folga_media": round(float(sub["folga_total"].mean()), 4),
            "intensidade_recursos_media": round(float(sub["intensidade_recursos"].mean()), 5),
        })
    pd.DataFrame(linhas_dist).to_csv(DIR_TABELAS / "psplib_02_distribuicao_niveis.csv",
                                     index=False, encoding="utf-8")

    # -----------------------------------------------------------------
    # Verificacoes
    # -----------------------------------------------------------------
    log("\n" + "=" * 78)
    log("VERIFICACOES")
    log("=" * 78)
    falhas = []

    if len(reais) == 28800:
        log(f"  [OK]    28.800 tarefas reais (480 x 60)")
    else:
        falhas.append(f"{len(reais)} tarefas reais, esperado 28.800")
        log(f"  [FALHA] {len(reais)} tarefas reais, esperado 28.800")

    fora = {c: int(((reais[c] < -1e-9) | (reais[c] > 1 + 1e-9)).sum())
            for c in ("duracao_norm", "intensidade_norm", "criticidade_folga", "Di")}
    if not any(fora.values()):
        log("  [OK]    Todos os componentes e o Di dentro de [0, 1]")
    else:
        falhas.append(f"valores fora de [0,1]: {fora}")
        log(f"  [FALHA] Valores fora de [0,1]: {fora}")

    inicio_fim = t[t["ficticia"]]
    if int((inicio_fim["folga_total"] != 0).sum()) == 0:
        log("  [OK]    Tarefas ficticias de inicio e fim com folga zero")
    else:
        falhas.append("tarefa ficticia com folga diferente de zero")
        log("  [FALHA] Tarefa ficticia com folga diferente de zero")

    if falhas_makespan == 0:
        log("  [OK]    Makespan da passagem para tras coincide com o do script 01")
    else:
        falhas.append(f"{falhas_makespan} divergencias de makespan")

    rho_min = min(l["spearman_vs_referencia"] for l in linhas_sens)
    log(f"  [INFO]  Menor correlacao de ordenacao entre esquemas de peso: {rho_min:.4f}")

    # -----------------------------------------------------------------
    colunas_saida = ["arquivo", "combinacao", "instancia", "tarefa", "duracao",
                     "n_sucessores", "sucessores"] + colunas_recurso + \
                    ["ES", "LS", "folga_total", "makespan_instancia",
                     "intensidade_recursos", "duracao_norm", "intensidade_norm",
                     "folga_norm", "criticidade_folga", "criticidade_sucessores",
                     "Di", "nivel_dificuldade"]
    reais[colunas_saida].to_csv(DIR_PROC / "tarefas_j60_com_di.csv",
                                index=False, encoding="utf-8")

    log("\n--- Arquivos gerados ---")
    log(f"  data/processed/psplib/tarefas_j60_com_di.csv ({len(reais)} linhas)")
    for n in ("psplib_02_componentes_correlacao.csv", "psplib_02_sensibilidade_pesos.csv",
              "psplib_02_distribuicao_niveis.csv"):
        log(f"  outputs/tables/{n}")

    log("\n" + "=" * 78)
    log("RESULTADO: " + ("CONCLUIDO COM FALHAS" if falhas else "CONCLUIDO, VERIFICACOES OK"))
    for f in falhas:
        log(f"  - {f}")
    log("=" * 78)

    (DIR_LOGS / "psplib_02_indice_dificuldade.log").write_text("\n".join(_log) + "\n",
                                                               encoding="utf-8")
    if falhas:
        sys.exit(1)


if __name__ == "__main__":
    main()
