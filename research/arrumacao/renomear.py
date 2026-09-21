"""Renomeia documentos de projeto/ e atualiza TODAS as referencias. Nao toca outputs/."""
import sys,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SECO='--aplicar' not in sys.argv

MAPA={
 # colisoes de numero: 42 e 44 estavam livres
 '42_AUTONOMIA_E_CONTINUIDADE.md':                        '42_AUTONOMIA_E_CONTINUIDADE.md',
 '44_REVISAO_INDEPENDENTE_RODADA2.md':'44_REVISAO_INDEPENDENTE_RODADA2.md',
 # sem numero -> 47..71, em ordem de entrada no repositorio
 '47_B2_ROBUSTEZ_DO_CANAL_DIRETO.md':             '47_B2_ROBUSTEZ_DO_CANAL_DIRETO.md',
 '48_C3_VALIDADO_E_RETOMADA_T4.md':                   '48_C3_VALIDADO_E_RETOMADA_T4.md',
 '49_HORIZONTE_DOBRADO_E_SELECAO.md':             '49_HORIZONTE_DOBRADO_E_SELECAO.md',
 '50_FUGA_DEPENDENTE_DE_ESTADO.md':           '50_FUGA_DEPENDENTE_DE_ESTADO.md',
 '51_ATUALIZACAO_B2_A1_C1_C2.md':    '51_ATUALIZACAO_B2_A1_C1_C2.md',
 '52_DEADLOCK_DE_TRES_VIAS_E_CENSURA.md':     '52_DEADLOCK_DE_TRES_VIAS_E_CENSURA.md',
 '53_ANCORAGEM_LINEAR_DE_F_ANCORA.md':      '53_ANCORAGEM_LINEAR_DE_F_ANCORA.md',
 '54_CONTROLE_DE_MOMENTOS_ARREDONDADOS.md':   '54_CONTROLE_DE_MOMENTOS_ARREDONDADOS.md',
 '55_HETEROGENEIDADE_BETA_ENTRE_AGENTES.md':       '55_HETEROGENEIDADE_BETA_ENTRE_AGENTES.md',
 '56_FECHAMENTO_DAS_ENTREGAS_OBRIGATORIAS.md':            '56_FECHAMENTO_DAS_ENTREGAS_OBRIGATORIAS.md',
 '57_SENSIBILIDADE_DA_SELECAO_A_PRESSAO.md':                  '57_SENSIBILIDADE_DA_SELECAO_A_PRESSAO.md',
 '58_READOUT_DE_RETRABALHO.md':                  '58_READOUT_DE_RETRABALHO.md',
 '59_COBERTURA_DO_HISTORY_MATCHING.md':                '59_COBERTURA_DO_HISTORY_MATCHING.md',
 '60_ESTIMANDO_DO_V_OBS.md':                '60_ESTIMANDO_DO_V_OBS.md',
 '61_GRADIENTE_POR_LINHAS_DE_CODIGO.md':                      '61_GRADIENTE_POR_LINHAS_DE_CODIGO.md',
 '62_TRAJETORIA_DE_CONFIANCA.md':                '62_TRAJETORIA_DE_CONFIANCA.md',
 '63_DISTRIBUICAO_DOS_MULTIPLICADORES.md':          '63_DISTRIBUICAO_DOS_MULTIPLICADORES.md',
 '64_NUMERACAO_E_DENOMINADORES.md':                 '64_NUMERACAO_E_DENOMINADORES.md',
 '65_ORDEM_DE_SERVICO_19_A_20.md':            '65_ORDEM_DE_SERVICO_19_A_20.md',
 '66_RELATORIO_CONSOLIDADO_19_A_20.md':        '66_RELATORIO_CONSOLIDADO_19_A_20.md',
 '67_RESPOSTA_NUMERICA_PORTAO_E_READOUT.md':           '67_RESPOSTA_NUMERICA_PORTAO_E_READOUT.md',
 '68_PORTAO_DE_ASSISTENCIA_E_INCOMPLETUDE.md':          '68_PORTAO_DE_ASSISTENCIA_E_INCOMPLETUDE.md',
 '69_SENSIBILIDADE_DOS_ESCALARES_DE_APRENDIZAGEM.md':    '69_SENSIBILIDADE_DOS_ESCALARES_DE_APRENDIZAGEM.md',
 '70_LOCALIZACAO_DAS_INVERSOES_DE_SINAL.md':'70_LOCALIZACAO_DAS_INVERSOES_DE_SINAL.md',
 '71_REGIMES_DE_SATURACAO_E_GOVERNANCA.md':          '71_REGIMES_DE_SATURACAO_E_GOVERNANCA.md',
}
p=ROOT/'projeto'
faltando=[k for k in MAPA if not (p/k).exists()]
colide=[v for v in MAPA.values() if (p/v).exists()]
if faltando: print('ERRO origem inexistente:',faltando); sys.exit(1)
if colide:  print('ERRO destino ja existe:',colide); sys.exit(1)

# arquivos onde procurar referencias (nunca outputs/, .git/, .venv/)
alvos=[]
for ext in ('*.md','*.py','*.yaml','*.yml','*.js','*.txt','*.json'):
    for f in ROOT.rglob(ext):
        s=str(f.relative_to(ROOT))
        if s.startswith(('.git/','outputs/','_to_delete/','.venv/','Claude outputs/')): continue
        alvos.append(f)

print(f'{"DE":48s} -> PARA')
for k,v in MAPA.items(): print(f'{k:48s} -> {v}')
print(f'\n{len(MAPA)} renomeacoes | {len(alvos)} arquivos varridos para referencias')

# quantas referencias serao reescritas
tot=0; porarq={}
for f in alvos:
    try: t=f.read_text(encoding='utf-8')
    except Exception: continue
    n=sum(t.count(k.rsplit('.md')[0]) for k in MAPA)
    if n: porarq[str(f.relative_to(ROOT))]=n; tot+=n
print(f'\n{tot} referencias em {len(porarq)} arquivos serao atualizadas:')
for k,v in sorted(porarq.items(),key=lambda x:-x[1])[:20]: print(f'  {v:4d}  {k}')

if SECO:
    print('\n*** ENSAIO. Nada foi alterado. Rode com --aplicar para executar. ***'); sys.exit(0)

for k,v in MAPA.items():
    subprocess.run(['git','mv','projeto/'+k,'projeto/'+v],cwd=ROOT,check=True)
for f in alvos:
    if not f.exists(): continue
    try: t=f.read_text(encoding='utf-8')
    except Exception: continue
    o=t
    for k,v in MAPA.items():
        t=t.replace(k,v).replace(k.rsplit('.md')[0],v.rsplit('.md')[0])
    if t!=o: f.write_text(t,encoding='utf-8'); print('atualizado:',f.relative_to(ROOT))
print('\nFEITO. Confira com git status e rode a verificacao.')
