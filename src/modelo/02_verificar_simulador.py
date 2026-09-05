"""
02_verificar_simulador.py — Bateria de verificações do simulador
=================================================================

Executa as oito verificações obrigatórias da seção 10 de
docs/especificacao_modelo.md, mais a validação externa da seção 10.1.

Uma verificação que falha interrompe com código de erro: um simulador
defeituoso não pode alimentar o experimento.

SAIDA
-----
  outputs/tables/modelo_02_verificacoes.csv
  outputs/logs/modelo_02_verificar_simulador.log
"""

import copy
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import simulador as S  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
DIR_TABELAS = RAIZ / "outputs" / "tables"
DIR_LOGS = RAIZ / "outputs" / "logs"
_log: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _log.append(m)


def main() -> None:
    log("=" * 78)
    log("VERIFICACOES DO SIMULADOR")
    log(f"Execucao: {datetime.now().isoformat(timespec='seconds')}")
    log("=" * 78)

    par = S.carregar_parametros()
    tarefas_todas = pd.read_csv(RAIZ / "data" / "processed" / "psplib" / "tarefas_j60_com_di.csv")
    instancias = sorted(tarefas_todas["arquivo"].unique())[::40]      # 12 instâncias
    log(f"\nInstancias na bateria: {len(instancias)}")

    resultados = []
    for arq in instancias:
        g, disp, cpm = S.carregar_instancia(arq)
        for cen in ("centralizada", "adaptativa"):
            sim = S.Simulacao(g, disp, cpm, par, cen, semente=42)
            r = sim.executar()
            resultados.append((arq, cen, sim, r))

    checagens = []

    def registrar(nome, ok, detalhe=""):
        checagens.append({"verificacao": nome, "resultado": "OK" if ok else "FALHA",
                          "detalhe": detalhe})
        log(f"  [{'OK   ' if ok else 'FALHA'}] {nome}" + (f" — {detalhe}" if detalhe else ""))
        return ok

    log("\n" + "=" * 78)
    log("1 a 5 — INVARIANTES ESTRUTURAIS")
    log("=" * 78)

    # 1. conservação: toda tarefa em estado terminal
    pendentes = sum(1 for _, _, sim, _ in resultados
                    for x in sim.tarefas.values() if not x.estado.startswith("concluida"))
    registrar("1. toda tarefa termina em estado terminal", pendentes == 0,
              f"{pendentes} tarefas nao terminais")

    # 2. precedência
    viol_prec = sum(len([v for v in r.violacoes if "precedencia" in v]) for *_, r in resultados)
    registrar("2. precedencia respeitada", viol_prec == 0, f"{viol_prec} violacoes")

    # 3. recursos — recalculado a posteriori sobre o cronograma realizado
    viol_rec = 0
    for _, _, sim, r in resultados:
        K = len(sim.disponibilidade)
        horizonte = max((x.fim or 0) for x in sim.tarefas.values())
        uso = np.zeros((horizonte + 1, K))
        for x in sim.tarefas.values():
            if x.inicio is None or x.fim is None:
                continue
            for tt in range(x.inicio, min(x.fim, horizonte + 1)):
                for k in range(K):
                    uso[tt][k] += x.demanda[k]
        for k in range(K):
            if (uso[:, k] > sim.disponibilidade[k]).any():
                viol_rec += 1
    registrar("3. disponibilidade de recursos nunca excedida", viol_rec == 0,
              f"{viol_rec} instancias com excesso")

    # 4. tempo: relógios não negativos e soma consistente
    ok_tempo = all(min(r.TW, r.TL, r.TU, r.TR) >= 0 and (r.TW + r.TL + r.TU + r.TR) > 0
                   for *_, r in resultados)
    registrar("4. relogios nao negativos e soma positiva", ok_tempo)

    # 5. faixas
    fora = []
    for _, _, sim, r in resultados:
        if not (0.0 <= r.E_total <= 1.0):
            fora.append(f"E_total={r.E_total:.4f}")
        for a in sim.agentes:
            if not (0.0 <= a.bateria <= 1.0):
                fora.append(f"bateria={a.bateria:.4f}")
            if not (0.0 <= a.competencia <= 1.0):
                fora.append(f"competencia={a.competencia:.4f}")
        for m in sim.traj["mu_cog"] + sim.traj["mu_rede"]:
            if not (0.0 <= m <= 1.0):
                fora.append(f"mu={m:.4f}")
                break
    registrar("5. E_total, bateria, competencia e multiplicadores em [0,1]",
              not fora, "; ".join(fora[:3]))

    log("\n" + "=" * 78)
    log("6 — DETERMINISMO")
    log("=" * 78)
    g, disp, cpm = S.carregar_instancia(instancias[0])
    r1 = S.Simulacao(g, disp, cpm, par, "centralizada", semente=7).executar()
    r2 = S.Simulacao(g, disp, cpm, par, "centralizada", semente=7).executar()
    igual = (r1.makespan == r2.makespan and abs(r1.E_total - r2.E_total) < 1e-12
             and abs(r1.S_UR_final - r2.S_UR_final) < 1e-12
             and r1.n_com_erro == r2.n_com_erro)
    registrar("6. mesma semente reproduz o mesmo resultado", igual)
    r3 = S.Simulacao(g, disp, cpm, par, "centralizada", semente=8).executar()
    registrar("6b. sementes diferentes produzem resultados diferentes",
              (r1.makespan, r1.n_com_erro) != (r3.makespan, r3.n_com_erro),
              "se falhar, o gerador nao esta sendo usado")

    log("\n" + "=" * 78)
    log("7 — CASO DEGENERADO (condicao ideal deve produzir execucao limpa)")
    log("=" * 78)
    ideal = copy.deepcopy(par)
    ideal["risco"]["F_ancora"]["valor"] = 0.0
    ideal["risco"]["R_error"]["valor"] = 0.0
    ideal["gestor"]["P_min"]["valor"] = 0.0
    ideal["gestor"]["P_max"]["valor"] = 0.0
    ideal["agentes"]["k_analitico"]["valor"] = 0.0
    ideal["agentes"]["k_heuristico"]["valor"] = 0.0
    r_id = S.Simulacao(g, disp, cpm, ideal, "adaptativa", semente=3).executar()
    registrar("7a. sem risco nem pressao, nenhuma tarefa falha",
              r_id.n_com_erro == 0 and r_id.n_reportadas == 0,
              f"erros={r_id.n_com_erro} reportadas={r_id.n_reportadas}")
    registrar("7b. sem risco nem pressao, E_total tende a 1",
              r_id.E_total > 0.95, f"E_total={r_id.E_total:.4f}")
    registrar("7c. sem risco nem pressao, divida tecnica nula",
              r_id.S_UR_maximo == 0.0, f"S_UR_max={r_id.S_UR_maximo:.4f}")

    log("\n" + "=" * 78)
    log("8 — MONOTONICIDADE ESPERADA: mais pressao nao pode reduzir a divida")
    log("=" * 78)
    # A primeira versao deste teste comparava tres medias com 12 replicacoes.
    # Com erro padrao da ordem de 0,75 e diferencas de 1 a 2 unidades, era
    # subpotenciado por construcao: acusava falha por ruido amostral. Substituido
    # por teste de tendencia sobre cinco niveis com 40 replicacoes cada, que e o
    # desenho adequado para detectar tendencia monotonica.
    from scipy import stats as _stats
    niveis_p, medias_sur, medias_heu = [], [], []
    for pmax in (0.2, 0.4, 0.6, 0.8, 1.0):
        p2 = copy.deepcopy(par)
        p2["gestor"]["P_max"]["valor"] = pmax
        p2["gestor"]["P_min"]["valor"] = min(0.2, pmax)
        sur, heu = [], []
        for sem in range(40):
            sim2 = S.Simulacao(g, disp, cpm, p2, "centralizada", semente=sem)
            r2 = sim2.executar()
            sur.append(r2.S_UR_maximo)
            tot = sum(a.periodos_heuristicos + a.periodos_analiticos for a in sim2.agentes)
            heu.append(sum(a.periodos_heuristicos for a in sim2.agentes) / max(1, tot))
        niveis_p.append(pmax); medias_sur.append(float(np.mean(sur)))
        medias_heu.append(float(np.mean(heu)))
        log(f"    P_max={pmax:.1f}  S_UR maximo medio = {np.mean(sur):>7.3f}  "
            f"(ep {np.std(sur)/np.sqrt(len(sur)):.3f})   tempo heuristico = {np.mean(heu):.1%}")

    rho_sur, p_sur = _stats.spearmanr(niveis_p, medias_sur)
    rho_heu, p_heu = _stats.spearmanr(niveis_p, medias_heu)
    log(f"\n    tendencia S_UR      vs pressao : Spearman rho={rho_sur:+.3f}  p={p_sur:.4f}")
    log(f"    tendencia t.heuristico vs pressao : Spearman rho={rho_heu:+.3f}  p={p_heu:.4f}")
    registrar("8a. divida tecnica cresce com a pressao (teste de tendencia)",
              rho_sur > 0 and p_sur < 0.05, f"rho={rho_sur:+.3f} p={p_sur:.4f}")
    registrar("8b. tempo em modo heuristico cresce com a pressao",
              rho_heu > 0 and p_heu < 0.05, f"rho={rho_heu:+.3f} p={p_heu:.4f}")

    log("\n" + "=" * 78)
    log("VALIDACAO EXTERNA — retrabalho contra a literatura de campo")
    log("=" * 78)
    log("  `[ACHADO 7]` A versao anterior deste teste comparava uma razao de")
    log("  ESFORCO (retrabalho/esforco) contra a faixa de LOVE, que e uma razao")
    log("  de CUSTO sobre VALOR DE CONTRATO. Sao grandezas de unidades distintas")
    log("  — a propria secao 10.1 da especificacao recusa essa confusao ao")
    log("  descartar Love como base de F_ancora, e o teste a reintroduzia. O")
    log("  criterio foi refeito sobre a construcao equivalente em unidade.")
    log("")
    log("  Referencia em ESFORCO (mesma unidade da saida do modelo):")
    log("    BOEHM, B.; BASILI, V. R. Software Defect Reduction Top 10 List.")
    log("    Computer, v. 34, n. 1, p. 135-137, jan. 2001. DOI 10.1109/2.962984.")
    log("    Item 2: projetos de software gastam de 40% a 50% do esforco em")
    log("    retrabalho evitavel. E o TETO de referencia.")
    log("")
    log("  Referencia em CUSTO (unidade distinta; piso de ordem de grandeza):")
    log("    LOVE, P. E. D. et al. Quantifying the Costs of Field Rework in")
    log("    Construction. JCEM, v. 152, n. 1, 2026. DOI 10.1061/JCEMD4.COENG-17026.")
    log("    0,38% do valor de contrato (max. 3,67%); 0,76% incluindo")
    log("    pos-conclusao (max. 7,34%). LOVE e LI (2000) reportam 3,15% e 2,40%.")
    log("")
    log("  `[DEC]` Faixa admitida: 1% a 50% do ESFORCO PLANEJADO. O piso vem da")
    log("  ordem de grandeza das cifras de campo em construcao; o teto, da cifra")
    log("  de esforco em software. `[LIMITACAO]` E um teste FRACO de")
    log("  plausibilidade, nao de calibracao: a faixa cobre uma ordem e meia de")
    log("  grandeza porque as duas literaturas medem construtos diferentes em")
    log("  dominios diferentes. Ele rejeita desalinhamento grosseiro e nada mais.")

    taxas = np.array([r.retrabalho_sobre_plano for *_, r in resultados])
    latente = np.array([r.divida_latente_sobre_plano for *_, r in resultados])
    mediana = float(np.median(taxas))
    fora = taxas[(taxas < 0.01) | (taxas > 0.50)]
    log(f"\n  retrabalho/plano     — min {taxas.min():.4f}  mediana {mediana:.4f}  "
        f"max {taxas.max():.4f}")
    log(f"  divida latente/plano — min {latente.min():.4f}  "
        f"mediana {np.median(latente):.4f}  max {latente.max():.4f}")
    log(f"  execucoes fora da faixa: {len(fora)} de {len(taxas)}"
        + (f"  (valores: {', '.join(f'{x:.4f}' for x in sorted(fora))})" if len(fora) else ""))
    # O criterio incide sobre a TENDENCIA CENTRAL. Um modelo estocastico produz
    # cauda; a fracao fora e reportada como limitacao, nao suprimida.
    registrar("9a. mediana do retrabalho na faixa de plausibilidade [1%; 50%]",
              0.01 <= mediana <= 0.50, f"mediana={mediana:.4f}")
    registrar("9b. cauda fora da faixa inferior a 10% das execucoes",
              len(fora) / len(taxas) < 0.10,
              f"{len(fora)}/{len(taxas)} = {len(fora)/len(taxas):.1%}")
    registrar("9c. divida latente estritamente positiva (estoque nao inerte)",
              float(np.median(latente)) > 0.0, f"mediana={np.median(latente):.4f}")

    # -----------------------------------------------------------------
    df = pd.DataFrame(checagens)
    df.to_csv(DIR_TABELAS / "modelo_02_verificacoes.csv", index=False, encoding="utf-8")
    falhou = (df["resultado"] == "FALHA").sum()

    log("\n" + "=" * 78)
    log(f"RESULTADO: {len(df) - falhou} de {len(df)} verificacoes aprovadas")
    log("=" * 78)
    (DIR_LOGS / "modelo_02_verificar_simulador.log").write_text("\n".join(_log) + "\n",
                                                                encoding="utf-8")
    if falhou:
        sys.exit(1)


if __name__ == "__main__":
    main()
