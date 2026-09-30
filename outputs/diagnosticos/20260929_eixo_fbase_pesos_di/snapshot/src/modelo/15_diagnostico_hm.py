"""[DEC] Diagnóstico B5 isolado; não substitui ondas nem resultados publicados.

Uso: python3 src/modelo/15_diagnostico_hm.py --saida outputs/diagnosticos/hm_20260915
Compara 8 índices pré-fixados do desenho de 400 pontos em duas alternativas,
com as mesmas 2 instâncias e sementes 0..3. Não é teste de convergência.
"""
import argparse
import hashlib
import importlib.util
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("hm", Path(__file__).with_name("04_gemeo_identico.py"))
hm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hm)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", type=Path, required=True)
    args = parser.parse_args()
    # Falhar em vez de sobrescrever um diagnóstico anterior.
    args.saida.mkdir(parents=True, exist_ok=False)
    fontes = [RAIZ / "src/modelo" / f for f in
              ("04_gemeo_identico.py", "simulador.py", "fuzzy.py", "15_diagnostico_hm.py")]
    fontes += list((RAIZ / "config").glob("*.yaml"))
    fontes += list((RAIZ / "data/processed/psplib").glob("*.csv"))
    fontes += list((RAIZ / "outputs/tables").glob("modelo_04_*.csv"))
    hashes = {str(p.relative_to(RAIZ)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in fontes}
    a = pd.read_csv(hm.TAB / "modelo_04_hm_onda1.csv").sort_values("ponto").reset_index(drop=True)
    b = pd.read_csv(hm.TAB / "modelo_04_hm_onda2.csv").sort_values("ponto").reset_index(drop=True)
    z = pd.read_csv(hm.TAB / "modelo_04_observacoes_sinteticas.csv").iloc[0]
    assert len(a) == len(b) == hm.N_PONTOS
    assert a.ponto.tolist() == b.ponto.tolist() == list(range(hm.N_PONTOS))
    prior = np.array([(lo, hi) for _, _, lo, hi in hm.PARAMETROS])
    nroy = a[a.implausibilidade <= hm.CORTE]
    assert len(nroy) > 0
    box = np.array([(nroy[n].min(), nroy[n].max()) for n in hm.NOMES])
    assert np.all(box[:, 1] > box[:, 0])
    u1 = (a[hm.NOMES].to_numpy() - prior[:, 0]) / np.diff(prior, axis=1).ravel()
    u2 = (b[hm.NOMES].to_numpy() - box[:, 0]) / np.diff(box, axis=1).ravel()
    antigo = hm.lhs(hm.N_PONTOS, box, np.random.default_rng(20260905))
    # [DEC] Nova semente apenas para o desenho; sementes das réplicas preservadas.
    novo = hm.lhs(hm.N_PONTOS, box, np.random.default_rng(20260915))
    un = (novo - box[:, 0]) / np.diff(box, axis=1).ravel()
    igual = lambda x, y: bool(np.allclose(x, y, rtol=0, atol=1e-12))
    # Controles positivo e negativo: o detector precisa pegar o defeito legado.
    assert igual(u1, u2), "O defeito registrado não foi reproduzido; revisar diagnóstico"
    assert not igual(u1, un), "A alternativa também repetiu o desenho"
    assert igual(antigo, b[hm.NOMES].to_numpy())
    assert np.array_equal(novo, hm.lhs(hm.N_PONTOS, box, np.random.default_rng(20260915)))
    for j in range(len(hm.NOMES)):
        assert np.array_equal(np.sort(np.floor(un[:, j] * hm.N_PONTOS).astype(int)),
                              np.arange(hm.N_PONTOS)), "LHS perdeu estratificação"
    pd.DataFrame({"parametro": hm.NOMES,
                  "erro_normalizado_legado": np.max(abs(u1-u2), axis=0),
                  "erro_normalizado_alternativa": np.max(abs(u1-un), axis=0),
                  "prior_min": prior[:, 0], "prior_max": prior[:, 1],
                  "caixa_onda2_min": box[:, 0], "caixa_onda2_max": box[:, 1]}
                 ).to_csv(args.saida / "desenho.csv", index=False)
    indices = np.linspace(0, hm.N_PONTOS-1, 8, dtype=int).tolist()
    insts = hm.instancias()
    sementes = list(range(hm.N_SEMENTES_SIM))
    manifesto = {"hipotese": "Reinicializar o RNG repete o LHS normalizado entre ondas",
                 "limite": "Piloto de instrumentação; não testa convergência ou identificabilidade estrutural",
                 "python": platform.python_version(), "numpy": np.__version__,
                 "pandas": pd.__version__, "pyyaml": yaml.__version__,
                 "semente_desenho_legado": 20260905, "semente_desenho_alternativa": 20260915,
                 "indices": indices, "instancias": insts, "sementes_simulador": sementes,
                 "corte": hm.CORTE, "hashes_entrada": hashes}
    (args.saida / "manifesto.json").write_text(json.dumps(manifesto, indent=2, ensure_ascii=False)+"\n")
    par = hm.S.carregar_parametros()
    cache = {arq: hm.S.carregar_instancia(arq) for arq in insts}
    bruto, resumo = [], []
    for desenho, X in (("legado", antigo), ("alternativa", novo)):
        for i in indices:
            x = dict(zip(hm.NOMES, X[i]))
            p = hm.aplicar(par, x)
            linhas = []
            for arq in insts:
                g, disp, cpm = cache[arq]
                for sem in sementes:
                    sim = hm.S.Simulacao(g, disp, cpm, p, hm.CENARIO, semente=sem)
                    r = sim.executar()
                    vals = {o: float(r.makespan/r.makespan_cpm if o == "atraso_relativo"
                                     else getattr(r, o)) for o in hm.OBSERVAVEIS}
                    linhas.append(vals)
                    bruto.append({"desenho": desenho, "ponto": i, "instancia": arq,
                                  "semente": sem, **x, **vals, "retrabalho_sobre_esforco_total": r.retrabalho_sobre_esforco_total, "taxa_falha_efetiva": r.taxa_falha_efetiva, "concluiu": r.concluiu,
                                  "divida_pendente": len(sim.divida_pendente),
                                  "violacoes": len(r.violacoes), "makespan": r.makespan})
            d = pd.DataFrame(linhas)
            medias = {f"{tipo}_{o}": float(d[o].mean() if tipo == "media" else d[o].var(ddof=1)/len(d))
                      for o in hm.OBSERVAVEIS for tipo in ("media", "var_media")}
            row = {"desenho": desenho, "ponto": i, **x, **medias,
                   "implausibilidade": hm.implausibilidade(pd.Series(medias), z)}
            # Sem mudar a unidade inferencial: replica a fórmula legada para
            # isolar o efeito do desenho. A adequação de V_sim é questão separada.
            row["erro_max_reproducao_legado"] = (max(abs(medias[k]-float(b.iloc[i][k])) for k in medias)
                                                  if desenho == "legado" else np.nan)
            resumo.append(row)
            print(f"{desenho} ponto {i}: I={row['implausibilidade']:.4f}", flush=True)
    raw, res = pd.DataFrame(bruto), pd.DataFrame(resumo)
    raw.to_csv(args.saida / "piloto_bruto.csv", index=False)
    res.to_csv(args.saida / "piloto_resumo.csv", index=False)
    checks = {"dependencia_legada_detectada": igual(u1, u2),
              "alternativa_nao_repete_desenho": not igual(u1, un),
              "legado_reproduz_amostra": bool(res.erro_max_reproducao_legado.max() < 1e-10),
              "todas_tarefas_concluidas": bool(raw.concluiu.all()),
              "nenhuma_divida_pendente": bool((raw.divida_pendente == 0).all()),
              "nenhuma_violacao": bool((raw.violacoes == 0).all()),
              "entradas_preservadas": all(hashlib.sha256((RAIZ/p).read_bytes()).hexdigest() == h
                                         for p, h in hashes.items())}
    (args.saida / "verificacoes.json").write_text(json.dumps(checks, indent=2)+"\n")
    print(json.dumps(checks, indent=2))
    assert all(checks.values()), "Diagnóstico encontrou falha; consultar saídas sem expandir experimento"


if __name__ == "__main__":
    main()
