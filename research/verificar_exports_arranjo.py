"""Smoke dos exportadores em diretórios temporários; não executa HM."""
import importlib.util,sys,tempfile
from pathlib import Path
import pandas as pd
import yaml
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src/modelo'));sys.argv=['smoke']
import simulador as S

def mod(n):
 p=next((R/'src/modelo').glob(n+'_*.py'));sp=importlib.util.spec_from_file_location('smoke'+n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m

a='j6010_1.sm';checks=[]
with tempfile.TemporaryDirectory(prefix='tcc2-export-') as tmp:
 o=Path(tmp)
 m=mod('07');m.N_SEMENTES=1;rows=m.executar(S.carregar_parametros(),[a],'centralizada');assert 'taxa_falha_efetiva' in rows[0];checks.append('07')
 for n,arg in [('09',.6),('10','0000')]:
  m=mod(n);m.N_SEMENTES=1;m.instancias=lambda:[a];m.DIR_PARCIAIS=o/n;m.rodar(arg)
  d=pd.read_csv(next((o/n).glob('*.csv')));assert d.taxa_falha_efetiva.between(0,1).all();checks.append(n)
 m=mod('11');m.NIVEIS_P=[.5];m.DIR_PARCIAIS=o/'11';m.rodar(a,'centralizada',[0],'smoke')
 assert 'taxa_falha_efetiva' in pd.read_csv(next((o/'11').glob('*.csv')));checks.append('11')
 m=mod('20');cfg=yaml.safe_load((R/'config/mvp_v1.yaml').read_text());conf=m.desenho(cfg,S.carregar_parametros(),'alternativas')[-2];d=m.executar_job((conf,a,0,'centralizada'));assert 'taxa_falha_efetiva' in d;checks.append('20')
 m=mod('21');d=m.rodar_job(('mvp',a,'00000',1));assert 'taxa_falha_efetiva' in d[0];checks.append('21')
 m=mod('25');d=m.job((a,0,'adaptativa'));assert d[0]['taxa_falha_efetiva']==d[1]['taxa_falha_efetiva'];checks.append('25')
 m=mod('05');d,p=m.carregar();assert d.taxa_falha_efetiva.between(0,1).all();checks.append('05 histórico')
 print('Exportações reais e leitura histórica aprovadas:',checks)
