"""
02_verificar_simulador.py — Bateria de verificações do simulador
=================================================================

Executa as verificações obrigatórias da seção 10 de docs/especificacao_modelo.md.

CLASSIFICAÇÃO DAS VERIFICAÇÕES — cada uma declara o que sustenta:

  VERDADEIRA POR CONSTRUÇÃO  passa qualquer que seja o modelo; não é evidência.
                             Declaradas como tal: 1, 4a, 5, 6, 7a, 7c.
  VERIFICAÇÃO DE IMPLEMENTAÇÃO  testa se o código realiza o que a formulação
                             especifica. Não é evidência sobre equipes reais: 8.
  ORDEM DE GRANDEZA          rejeita desalinhamento grosseiro contra a
                             literatura; não calibra nem valida: 9.
  VALIDAÇÃO EXTERNA          nenhuma. Não há, neste trabalho, critério
                             confrontado com dado externo que possa reprovar o
                             modelo. `[B3]` A seção 9 já foi chamada assim e
                             foi rebaixada, com a evidência do rebaixamento
                             calculada no próprio script (verificação 9d).

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

    pd.DataFrame([dict(arquivo=arq,cenario=cen,retrabalho_sobre_esforco_total=r.retrabalho_sobre_esforco_total,taxa_falha_efetiva=r.taxa_falha_efetiva,
                       n_com_erro=r.n_com_erro,n_reportadas=r.n_reportadas,
                       n_tarefas=len(sim.tarefas),concluiu=r.concluiu)
                  for arq,cen,sim,r in resultados]).to_csv(
                      DIR_TABELAS / "modelo_02_desfechos.csv", index=False)
    checagens = []

    def registrar(nome, ok, detalhe=""):
        checagens.append({"verificacao": nome, "resultado": "OK" if ok else "FALHA",
                          "detalhe": detalhe})
        log(f"  [{'OK   ' if ok else 'FALHA'}] {nome}" + (f" — {detalhe}" if detalhe else ""))
        return ok

    def registrar_nao_confirmada(nome, ok, detalhe, motivo):
        """
        Propriedade esperada que NAO se confirma, ja analisada pela autora e
        declarada como limitacao.

        `[DEC]` Existe para nao haver escolha entre duas saidas ruins: converter
        a falha em aprovacao (fraude) ou derrubar o pipeline por uma propriedade
        que o trabalho declara como nao verificada. NUNCA conta como aprovacao —
        entra no CSV com resultado 'NAO CONFIRMADA' e exige um `motivo` escrito.
        Usar SOMENTE apos analise; nunca para fazer um teste passar.
        """
        assert motivo, "toda nao confirmacao exige motivo escrito"
        checagens.append({"verificacao": nome,
                          "resultado": "OK" if ok else "NAO CONFIRMADA",
                          "detalhe": detalhe if ok else f"{detalhe} | {motivo}"})
        log(f"  [{'OK   ' if ok else 'N/CONF'}] {nome} — {detalhe}")
        if not ok:
            log(f"           motivo declarado: {motivo}")
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
    registrar("4a. relogios nao negativos e soma positiva", ok_tempo,
              "VERDADEIRA POR CONSTRUCAO — nao e evidencia")

    # `[B4]` A verificacao 4 ORIGINAL comparava a soma dos relogios com o tempo
    # de agente efetivamente alocado. Ela havia sido trocada por "relogios nao
    # negativos", que passa por construcao e nao testa nada. Restaurada.
    #
    # `[C1]` Ela FALHA hoje, e a falha e informativa: TR e somado sem consumir
    # tempo de agente (ver ACHADO em simulador.py). A diferenca mede exatamente
    # o "relogio fantasma" — retrabalho contabilizado que ninguem executou.
    log("")
    desvios = []
    for arq, cen, sim, r in resultados:
        soma_relogios = r.TW + r.TL + r.TU + r.TR
        alocado = len(sim.agentes) * r.makespan
        desvios.append((cen, soma_relogios, alocado, r.TR))
    import statistics as _st
    for cen in ("centralizada", "adaptativa"):
        d = [(sr, al, tr) for c, sr, al, tr in desvios if c == cen]
        log(f"    {cen:<14} soma dos relogios {_st.mean(x[0] for x in d):>9.1f}  "
            f"tempo de agente alocado {_st.mean(x[1] for x in d):>9.1f}  "
            f"TR {_st.mean(x[2] for x in d):>7.1f}")
    conserva = all(abs(sr - (al - tr)) < 1e-6 or sr <= al for _, sr, al, tr in desvios)
    # `[AUDITORIA]` PODER DE DETECCAO DESTA VERIFICACAO — declarado.
    # TW, TL e TU sao incrementados um a um a partir de periodos de agente
    # efetivamente gastos (executando, apoiando, bloqueado). A desigualdade
    # TW+TL+TU <= n_agentes x makespan e, portanto, VERDADEIRA POR CONSTRUCAO.
    # A unica parcela que poderia viola-la e TR, que nao consome agente. Logo:
    # esta verificacao NAO e evidencia comportamental independente; ela so
    # detecta erro se a inflacao dos relogios exceder a folga de periodos de
    # agente livre. A folga e reportada abaixo para que o leitor veja o quanto
    # o teste consegue apertar — quanto maior a folga, menor o poder.
    folga = min(1.0 - sr / al for _, sr, al, _ in desvios if al > 0)
    registrar("4b. [construcao, poder fraco] soma dos relogios nao excede o "
              "tempo de agente alocado", conserva,
              f"folga minima {folga:.1%} — o teste so pega inflacao acima disso; "
              f"TR e contabilizado sem consumir agente (item C1)")

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
    # `[B2]` As verificacoes 6, 7 e 9 rodavam numa unica instancia. Passam a
    # rodar em TODAS as 12 da bateria e, onde faz sentido, nos dois cenarios.
    # (As verificacoes 1 a 5 ja rodavam nas 12 — a critica de instancia unica
    # nao se aplicava a elas.)
    g, disp, cpm = S.carregar_instancia(instancias[0])
    r1 = S.Simulacao(g, disp, cpm, par, "centralizada", semente=7).executar()
    r2 = S.Simulacao(g, disp, cpm, par, "centralizada", semente=7).executar()
    igual = (r1.makespan == r2.makespan and abs(r1.E_total - r2.E_total) < 1e-12
             and abs(r1.S_UR_final - r2.S_UR_final) < 1e-12
             and r1.n_com_erro == r2.n_com_erro)
    # repete em todas as instancias e nos dois cenarios
    falhas_det = []
    for arq in instancias:
        gg, dd, cc = S.carregar_instancia(arq)
        for cen in ("centralizada", "adaptativa"):
            a = S.Simulacao(gg, dd, cc, par, cen, semente=7).executar()
            b = S.Simulacao(gg, dd, cc, par, cen, semente=7).executar()
            if (a.makespan, a.n_com_erro) != (b.makespan, b.n_com_erro):
                falhas_det.append(f"{arq}/{cen}")
    igual = igual and not falhas_det
    registrar("6. mesma semente reproduz o mesmo resultado "
              f"({len(instancias)} instancias x 2 cenarios)", igual,
              "VERDADEIRA POR CONSTRUCAO se o RNG e semeado corretamente")
    r3 = S.Simulacao(g, disp, cpm, par, "centralizada", semente=8).executar()
    registrar("6b. sementes diferentes produzem resultados diferentes",
              (r1.makespan, r1.n_com_erro) != (r3.makespan, r3.n_com_erro),
              "se falhar, o gerador nao esta sendo usado")

    log("\n" + "=" * 78)
    log("7 — CASO DEGENERADO (condicao ideal deve produzir execucao limpa)")
    log("=" * 78)
    log("  `[ACHADO 11]` A condicao 'ideal' anterior NAO era ideal. Ela zerava")
    log("  risco, pressao e drenagem, mas deixava a competencia nominal — e o")
    log("  resultado era um projeto PIOR que o nominal: makespan 303,5 contra")
    log("  249,2 e ociosidade 1.030 contra 97.")
    log("")
    log("  A causa e estrutural e vale como achado do modelo: a Porta 3 exige")
    log("  DeltaD <= 0, isto e, o agente em modo analitico so executa tarefa")
    log("  dentro da sua competencia. Com pressao zero o agente praticamente")
    log("  nunca entra em modo heuristico (E = D_i*P/B = 0), de modo que as")
    log("  tarefas acima da competencia so poderiam sair por ajuda — e com tau")
    log("  constante a centralizada nunca ajuda (TL = 0).")
    log("")
    log("  Ou seja: NO MODELO, o modo heuristico e simultaneamente a patologia")
    log("  E a unica valvula de escape para o hiato de competencia. Desligar a")
    log("  patologia sem resolver a causa fundamental trava o projeto. Isso e")
    log("  coerente com o arquetipo de Solucoes Sintomaticas do TCC I, mas")
    log("  precisa ser DECLARADO, e nao descoberto pela banca.")
    log("")
    log("  A condicao degenerada correta zera risco, pressao e drenagem E torna")
    log("  a competencia suficiente. So entao 'ideal' significa ideal.")

    ideal = copy.deepcopy(par)
    ideal["risco"]["F_ancora"]["valor"] = 0.0
    ideal["risco"]["R_error"]["valor"] = 0.0
    ideal["gestor"]["P_min"]["valor"] = 0.0
    ideal["gestor"]["P_max"]["valor"] = 0.0
    ideal["agentes"]["k_analitico"]["valor"] = 0.0
    ideal["agentes"]["k_heuristico"]["valor"] = 0.0
    ideal["agentes"]["competencia_inicial"]["valor"] = {"media": 0.99, "desvio": 0.001}

    ids = []
    for arq in instancias:
        gg, dd, cc = S.carregar_instancia(arq)
        for cen in ("centralizada", "adaptativa"):
            ids.append((arq, cen,
                        S.Simulacao(gg, dd, cc, ideal, cen, semente=3).executar()))
    log(f"\n    {len(ids)} execucoes na condicao ideal — "
        f"E_total minimo {min(r.E_total for _, _, r in ids):.4f}, "
        f"ociosidade maxima {max(r.TU for _, _, r in ids):.1f}")

    registrar("7a. sem risco nem pressao, nenhuma tarefa falha",
              all(r.n_com_erro == 0 and r.n_reportadas == 0 for _, _, r in ids),
              f"{len(ids)} execucoes — VERDADEIRA POR CONSTRUCAO (F_ancora=0)")
    registrar("7c. sem risco nem pressao, divida tecnica nula",
              all(r.S_UR_maximo == 0.0 for _, _, r in ids),
              "VERDADEIRA POR CONSTRUCAO (F_ancora=0)")

    # `[B2]` Criterios que NAO sao verdadeiros por construcao: a condicao ideal
    # tem de eliminar a ociosidade e concluir mais rapido que a nominal, NA MESMA
    # instancia. Sao os unicos itens da verificacao 7 que constituem evidencia.
    tu_max = max(r.TU for _, _, r in ids)
    # `[AUDITORIA]` PODER DE DETECCAO DE 7d — declarado.
    # Na condicao ideal a competencia sorteada e 0,99 com desvio 0,001, mas o
    # simulador aplica clip em 0,98: todos os agentes ficam com 0,98 exatos.
    # A ociosidade so pode nascer de dois lugares: (i) o ramo de fuga da Porta 1,
    # que NUNCA dispara porque omega (0,50) nao excede o limite de aversao
    # (0,60) — item C5; (ii) a Porta 2, que exige dD > 0, isto e, alguma tarefa
    # com dificuldade acima de 0,98. Logo 7d passa se e somente se nenhuma
    # tarefa das instancias amostradas ultrapassar 0,98.
    # NAO e verdadeira por construcao: 32 das 28.800 tarefas da base tem
    # Di > 0,98, distribuidas em 32 das 480 instancias. Nas 12 instancias desta
    # bateria o maximo e 0,9530, e por isso o teste passa. O resultado e,
    # portanto, CONTINGENTE A AMOSTRA DE INSTANCIAS e nao se generaliza as 480.
    di_max = float(tarefas_todas[tarefas_todas["arquivo"].isin(instancias)]["Di"].max())
    registrar("7d. [contingente a amostra] condicao ideal elimina a ociosidade "
              "(TU = 0)", tu_max == 0.0,
              f"TU maximo = {tu_max:.1f}; Di maximo nas {len(instancias)} "
              f"instancias = {di_max:.4f} contra competencia 0,98 — falharia em "
              f"instancia com Di > 0,98 (32 das 480)")

    nominal = {(arq, cen): r for arq, cen, _, r in resultados}
    pares = [(arq, cen, r, nominal[(arq, cen)])
             for arq, cen, r in ids if (arq, cen) in nominal]
    lentos = [(a, c) for a, c, ri, rn in pares if ri.makespan >= rn.makespan]
    ganho = sum(rn.makespan - ri.makespan for _, _, ri, rn in pares) / len(pares)
    log(f"    pareado por instancia e cenario: {len(pares)} pares, "
        f"ganho medio de makespan {ganho:+.1f} periodos")
    # `[AUDITORIA]` PODER DE DETECCAO DE 7e — declarado.
    # A condicao ideal desliga TODOS os mecanismos que alongam o cronograma
    # (risco, pressao, drenagem) e ainda remove o hiato de competencia. Que ela
    # conclua antes e, portanto, quase garantido pela propria construcao da
    # condicao. NAO e vacuo: esta verificacao JA FALHOU, na versao anterior da
    # condicao ideal, e foi essa falha que expos o ACHADO 11 — a condicao dita
    # ideal produzia projeto PIOR que o nominal (makespan 303,5 contra 249,2).
    # O teste tem poder demonstrado; o que ele nao e e evidencia estrutural
    # independente: e uma DEMONSTRACAO DE COMPORTAMENTO sob condicao completa.
    registrar("7e. [comportamento sob condicao ideal] conclui mais rapido que a "
              "nominal (pareado)", not lentos,
              f"{len(pares) - len(lentos)} de {len(pares)} pares favoraveis; "
              f"ganho medio {ganho:+.1f} periodos")

    log("\n" + "=" * 78)
    log("8 — RESPOSTA A PRESSAO: teste de tendencia  [B1]")
    log("=" * 78)
    log("  `[B1]` A versao original calculava Spearman sobre CINCO MEDIAS e")
    log("  reportava o valor-p assintotico do scipy. Com n = 5 o menor valor-p")
    log("  bilateral EXATO e 2/5! = 0,0167; um p da ordem de 1e-24 nao e")
    log("  atingivel e nao podia ser evidencia. O teste tambem so rodava no")
    log("  braco centralizado, numa instancia.")
    log("")
    log("  Refeito em `src/modelo/11_tendencia_pressao.py`, com desenho em duas")
    log("  etapas: piloto (sementes 0-39) para estimar o tamanho de efeito e")
    log("  dimensionar n por calculo de potencia, e confirmatorio (sementes")
    log("  1000-1099, DISJUNTAS) com o criterio inalterado, rho > 0 e p < 0,05.")
    log("  Resultados lidos daqui; nao sao recalculados neste script.")
    log("")
    log("  `[CLASSIFICACAO]` VERIFICACAO DE IMPLEMENTACAO. Testa se o codigo")
    log("  realiza a direcao que a formulacao preve. Nao e evidencia sobre")
    log("  equipes reais e nao restringe magnitude.")

    caminho_b1 = DIR_TABELAS / "modelo_11_tendencia_resumo.csv"
    if not caminho_b1.exists():
        registrar("8. resposta a pressao", False,
                  "modelo_11_tendencia_resumo.csv ausente — rodar "
                  "src/modelo/11_tendencia_pressao.py antes")
    else:
        b1 = pd.read_csv(caminho_b1)
        b1 = b1[b1["etapa"] == "confirmatorio"]
        log(f"\n  {'alvo':<18} {'cenario':<14} {'instancia':<13} {'n':>5} "
            f"{'rho':>7} {'IC95':>18} {'p':>11}")
        for r in b1.itertuples():
            log(f"  {r.alvo:<18} {r.cenario:<14} {r.arquivo:<13} {r.n:>5} "
                f"{r.rho:>+7.3f}  [{r.ic95_baixo:+.3f}; {r.ic95_alto:+.3f}] "
                f"{r.p_valor:>11.2e}")

        def celulas_do(alvo, cen):
            x = b1[(b1.alvo == alvo) & (b1.cenario == cen)]
            return list(x["aprova"].astype(bool)), x

        log("")
        for cen_b1 in ("centralizada", "adaptativa"):
            v, _ = celulas_do("S_UR_maximo", cen_b1)
            registrar(f"8a-{cen_b1}. divida oculta (S_UR max) cresce com a "
                      f"pressao", all(v) and len(v) > 0,
                      f"{sum(v)} de {len(v)} instancias, n = 500 por celula")
        for cen_b1 in ("centralizada", "adaptativa"):
            v, _ = celulas_do("fracao_heuristica", cen_b1)
            registrar(f"8b-{cen_b1}. tempo em modo heuristico cresce com a "
                      f"pressao", all(v) and len(v) > 0,
                      f"{sum(v)} de {len(v)} instancias, n = 500 por celula")

        log("")
        log("  `[POST HOC — declarado]` 8c foi acrescentada DEPOIS de ver a")
        log("  versao subdimensionada de 8a nao se confirmar. Nao e")
        log("  confirmatoria e nao substitui 8a. Fica declarada como")
        log("  exploratoria no documento, com o resultado que deu — inclusive")
        log("  onde nao se confirma.")
        for cen_b1 in ("centralizada", "adaptativa"):
            v, x = celulas_do("defeitos_gerados", cen_b1)
            nome = (f"8c-{cen_b1}. [exploratoria, post hoc] defeitos GERADOS "
                    f"crescem com a pressao")
            det = f"{sum(v)} de {len(v)} instancias, n = 500 por celula"
            if all(v) and len(v) > 0:
                registrar(nome, True, det)
            else:
                registrar_nao_confirmada(
                    nome, False,
                    det + f", IC95 ate {x['ic95_alto'].max():+.3f}",
                    "duas causas MEDIDAS, nenhuma delas defeito de codigo. "
                    "(1) DOSE MENOR: P(t) e endogena ao atraso; o braco "
                    "adaptativo atrasa menos e recebe 57,1% da amplitude de "
                    "P(t) que o centralizado recebe para o mesmo P_max "
                    "(0,3399 contra 0,5956 — modelo_11_dose_realizada.csv). "
                    "(2) CANAL FRACO: por p_falha = F_base + R_error(1-mu_cog), "
                    "com F_ancora 0,10 e R_error 0,15, a pressao acrescenta no "
                    "maximo 0,047 a p_falha sobre uma base de 0,100 a 0,299 — "
                    "a dificuldade domina a pressao de 3 a 20 vezes neste canal. "
                    "O criterio (rho>0, p<0,05) e o n (500 >= 421 exigido) NAO "
                    "foram alterados para acomodar o resultado")

        log("")
        log("  `[LIMITACAO]` 'nao confirmada' nao e 'refutada': o IC95 no braco")
        log("  adaptativo contem o zero e valores positivos pequenos.")
        log("  `[LIMITACAO]` A dose difere entre bracos por construcao. O")
        log("  experimento manipula P_max, nao P(t); nao e contraste de mesma")
        log("  dose entre bracos.")
        log("  `[LIMITACAO]` Vale nas 2 instancias e 2 cenarios testados, nao")
        log("  nas 480 instancias.")

    log("\n" + "=" * 78)
    log("9 — VERIFICACAO DE ORDEM DE GRANDEZA — retrabalho contra a literatura")
    log("=" * 78)
    log("  `[B3]` RECLASSIFICADA. Esta secao chamava-se VALIDACAO EXTERNA. Nao e.")
    log("  Uma validacao externa restringe o modelo: existe valor do parametro")
    log("  que ela reprova. Esta nao reprova nenhum — ver a varredura ao final")
    log("  desta secao. Passa a ser declarada como VERIFICACAO DE ORDEM DE")
    log("  GRANDEZA: rejeita desalinhamento grosseiro e nada mais. Nao sustenta")
    log("  afirmacao de validacao nem de calibracao de F_ancora.")
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
    registrar("9a. [ordem de grandeza, NAO validacao] mediana do retrabalho "
              "na faixa [1%; 50%]",
              0.01 <= mediana <= 0.50, f"mediana={mediana:.4f}")
    registrar("9b. cauda fora da faixa inferior a 10% das execucoes",
              len(fora) / len(taxas) < 0.10,
              f"{len(fora)}/{len(taxas)} = {len(fora)/len(taxas):.1%}")
    registrar("9c. divida latente estritamente positiva (estoque nao inerte)",
              float(np.median(latente)) > 0.0, f"mediana={np.median(latente):.4f}")

    # `[B3]` EVIDENCIA de que 9a nao restringe nada: varredura de F_ancora
    # sobre toda a faixa aberta declarada. Se a mediana permanece dentro de
    # [1%; 50%] em todos os valores, o criterio nao tem poder de rejeicao e
    # nao pode ser apresentado como validacao.
    log("\n  `[B3]` Poder de rejeicao do criterio 9a — varredura de F_ancora:")
    log(f"    {'F_ancora':>9} {'mediana retrab./plano':>22} {'9a aprova?':>12}")
    linhas_b3 = []
    g3, disp3, cpm3 = S.carregar_instancia(instancias[0])
    for fa in (0.05, 0.10, 0.15, 0.20, 0.25):
        p3 = copy.deepcopy(par)
        p3["risco"]["F_ancora"]["valor"] = fa
        resultados_b3 = [S.Simulacao(g3, disp3, cpm3, p3, c, semente=sm).executar()
              for c in ("centralizada", "adaptativa") for sm in range(8)]
        tx = [r.retrabalho_sobre_plano for r in resultados_b3]
        med3 = float(np.median(tx))
        aprova = bool(0.01 <= med3 <= 0.50)
        linhas_b3.append({"F_ancora": fa, "mediana_retrabalho_sobre_plano": med3,
                          "criterio_9a_aprova": aprova, "n_execucoes": len(tx),
                          "taxa_falha_efetiva": float(np.mean([r.taxa_falha_efetiva for r in resultados_b3]))})
        log(f"    {fa:>9.2f} {med3:>22.4f} {'sim' if aprova else 'NAO':>12}")
    d_b3 = pd.DataFrame(linhas_b3)
    d_b3.to_csv(DIR_TABELAS / "modelo_02_b3_poder_do_criterio_9a.csv", index=False,
                encoding="utf-8")
    todos = bool(d_b3["criterio_9a_aprova"].all())
    log("")
    if todos:
        log("    O criterio aprova em TODA a faixa de F_ancora. Poder de rejeicao")
        log("    nulo sobre este parametro. Confirmado o rebaixamento: ordem de")
        log("    grandeza, nao validacao externa, nao calibracao.")
    else:
        log("    O criterio reprova em algum ponto da faixa — reavaliar B3.")
    registrar("9d. [meta] o criterio 9a NAO restringe F_ancora (evidencia do "
              "rebaixamento)", todos,
              f"aprova em {int(d_b3['criterio_9a_aprova'].sum())} de {len(d_b3)} valores")

    # -----------------------------------------------------------------
    df = pd.DataFrame(checagens)
    df.to_csv(DIR_TABELAS / "modelo_02_verificacoes.csv", index=False, encoding="utf-8")
    falhou = int((df["resultado"] == "FALHA").sum())
    nconf = int((df["resultado"] == "NAO CONFIRMADA").sum())

    log("\n" + "=" * 78)
    log(f"RESULTADO: {len(df) - falhou - nconf} aprovadas, "
        f"{nconf} NAO CONFIRMADAS (declaradas), {falhou} falhas")
    if nconf:
        log("")
        for r in df[df["resultado"] == "NAO CONFIRMADA"].itertuples():
            log(f"  NAO CONFIRMADA: {r.verificacao}")
        log("  Nao contam como aprovacao e estao declaradas no documento.")
    log("=" * 78)
    (DIR_LOGS / "modelo_02_verificar_simulador.log").write_text("\n".join(_log) + "\n",
                                                                encoding="utf-8")
    if falhou:
        sys.exit(1)


if __name__ == "__main__":
    main()
