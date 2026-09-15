"""Verificacao da ablacao B9. Cada teste tem um caso que ele DEVERIA pegar."""
import pandas as pd, numpy as np, sys
d = pd.read_csv("outputs/tables/modelo_07_ablacao_bruto.csv")
falhas = []
def ok(nome, cond, detalhe=""):
    print(("  OK   " if cond else "  FALHA") + f" {nome}   {detalhe}")
    if not cond: falhas.append(nome)

CH = ["arquivo","semente"]
MET = ["makespan","TW","TL","TU","TR","n_com_erro","S_UR_maximo","E_total"]
def sub(b): return d[d.braco==b].set_index(CH).sort_index()

print("\n1. A ablacao DESLIGA o que promete desligar")
a_abl = sub("adaptativa__sem_assistencia")
ok("adaptativa sob sem_assistencia nao concede nenhuma ajuda",
   a_abl.p2_ajuda.sum()==0, f"soma p2_ajuda = {a_abl.p2_ajuda.sum()}")
ok("adaptativa nominal CONCEDE ajuda (o teste acima poderia falhar)",
   sub("adaptativa").p2_ajuda.sum()>0, f"soma = {sub('adaptativa').p2_ajuda.sum()}")
c_uni = sub("centralizada__assistencia_universal")
ok("centralizada sob assistencia_universal zera 'colega capaz sem confianca'",
   c_uni.hiato_colega_capaz_sem_confianca.sum()==0,
   f"soma = {c_uni.hiato_colega_capaz_sem_confianca.sum()}")
c_nom = sub("centralizada")
ok("centralizada nominal TEM colega capaz barrado por confianca",
   c_nom.hiato_colega_capaz_sem_confianca.sum()>0,
   f"soma = {c_nom.hiato_colega_capaz_sem_confianca.sum()}")

print("\n2. Nao-efeito PREVISTO (se falhar, a ablacao faz algo nao pretendido)")
ok("centralizada nominal nunca concede ajuda (tau constante)",
   c_nom.p2_ajuda.sum()==0, f"soma p2_ajuda = {c_nom.p2_ajuda.sum()}")
c_abl = sub("centralizada__sem_assistencia")
ok("centralizada: sem_assistencia e IDENTICA ao nominal, linha a linha",
   c_nom[MET].equals(c_abl[MET]))
a_uni = sub("adaptativa__assistencia_universal")
ok("adaptativa: assistencia_universal e IDENTICA ao nominal, linha a linha",
   sub("adaptativa")[MET].equals(a_uni[MET]))

print("\n3. Pareamento: mesma equipe inicial em todos os bracos")
ref = sub("centralizada")["competencia_maxima_inicial"]
iguais = all(sub(b)["competencia_maxima_inicial"].equals(ref)
             for b in d.braco.unique())
ok("competencia_maxima_inicial identica entre todos os bracos", iguais)
ref2 = sub("centralizada")["tarefas_acima_da_competencia_maxima_inicial"]
ok("hiato estrutural identico entre bracos (so depende de instancia+semente)",
   all(sub(b)["tarefas_acima_da_competencia_maxima_inicial"].equals(ref2)
       for b in d.braco.unique()))

print("\n4. O nominal reproduz o experimento ja publicado")
try:
    e = pd.read_csv("outputs/tables/modelo_03_experimento_bruto.csv")
    for cen in ("centralizada","adaptativa"):
        x = e[e.cenario==cen].set_index(CH).sort_index()
        y = sub(cen)
        com = x.index.intersection(y.index)
        cols = ["makespan","TW","TL","TU","TR","n_com_erro"]
        ok(f"{cen}: {len(com)} pares (instancia,semente) coincidem com o 03",
           len(com)>0 and x.loc[com,cols].round(9).equals(y.loc[com,cols].round(9)))
except FileNotFoundError:
    print("  (03_experimento_bruto.csv ausente — pulado)")

print("\n5. Conservacao: nenhuma tarefa perdida")
ok("P1_omissao + P3_analitica = numero de tarefas, em toda execucao",
   bool(((d.p1_omissao + d.p3_analitica) == d.n_tarefas).all()) if "n_tarefas" in d
   else ((d.p1_omissao+d.p3_analitica)==60).all())
ok("todas as execucoes concluiram", bool(d.concluiu.all()),
   f"nao concluiram: {int((~d.concluiu).sum())}")

print(f"\n{len(d.braco.unique())} bracos, {len(d)} execucoes.")
print(("TODAS AS VERIFICACOES PASSARAM" if not falhas
       else f"FALHAS: {falhas}"))
sys.exit(1 if falhas else 0)
