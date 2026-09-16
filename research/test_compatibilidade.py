"""Contrato bit a bit de TODOS os campos legados, RNG e estados internos."""
import copy
from dataclasses import asdict
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP


def projetar(novo,legado):
    if isinstance(legado,dict): return {k:projetar(novo[k],v) for k,v in legado.items()}
    return novo

def bits(x):
    if isinstance(x,float):return x.hex()
    if isinstance(x,dict):return {k:bits(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [bits(v) for v in x]
    return x

class Compatibilidade(unittest.TestCase):
    def test_horizonte_fixo_nao_aplica_teto_automatico(self):
        from test_mvp import caso
        g,par=caso(falha=True)
        g['duracao']=1
        par['cenarios']['centralizada']['p_reporte']['valor']=0.
        par['cenarios']['centralizada']['p_deteccao']['valor']=0.
        for horizonte in [0,1,256,257,300]:
            with self.subTest(horizonte=horizonte):
                par['execucao']['horizonte_maximo_fator']['valor']=horizonte
                a=S.Simulacao(g,[1],1,copy.deepcopy(par),'centralizada',0)
                b=SimulacaoMVP(g,[1],1,copy.deepcopy(par),'centralizada',0,
                    opcoes=OpcoesMVP(rho_omissao=0.,fator_omissao=1.,
                        retrabalho_fila=False,lei_confianca='constante',
                        horizonte_automatico=False,politica_porta2='nominal'))
                antigo=asdict(a.executar())
                with patch.object(S.Simulacao,'executar',side_effect=AssertionError('delegação')):
                    novo=asdict(b.executar())
                self.assertEqual([k for k in antigo if bits(antigo[k])!=bits(projetar(novo[k],antigo[k]))],[])
                self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
                self.assertEqual(bits(a.divida_pendente),bits(b.divida_pendente))
                self.assertEqual(bits([vars(x) for x in a.agentes]),bits([vars(x) for x in b.agentes]))
                self.assertEqual(bits({k:vars(x) for k,x in a.tarefas.items()}),bits({k:vars(x) for k,x in b.tarefas.items()}))

    def test_laco_neutro_bit_a_bit(self):
        import pandas as pd
        nomes=sorted(pd.read_csv(S.RAIZ/'data/processed/psplib/instancias_j60.csv').arquivo.unique())[::120]
        for arquivo in nomes:
            g,disp,cpm=S.carregar_instancia(arquivo)
            for cen in ['centralizada','adaptativa']:
                for seed in range(4):
                    with self.subTest(arquivo=arquivo,cenario=cen,semente=seed):
                        par=S.carregar_parametros()
                        a=S.Simulacao(g,disp,cpm,copy.deepcopy(par),cen,seed)
                        # rho=0 é neutro; nenhuma delegação ao executar legado.
                        opts=dict(rho_omissao=0.,fator_omissao=1.,retrabalho_fila=False,lei_confianca='constante',horizonte_automatico=False,politica_porta2='nominal')
                        b=SimulacaoMVP(g,disp,cpm,copy.deepcopy(par),cen,seed,opcoes=OpcoesMVP(**opts))
                        antigo=asdict(a.executar())
                        with patch.object(S.Simulacao,'executar',side_effect=AssertionError('delegação não valida laço MVP')):
                            novo=asdict(b.executar())
                        campos=[k for k in antigo if bits(antigo[k])!=bits(projetar(novo[k],antigo[k]))]
                        self.assertEqual(campos,[])
                        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
                        self.assertEqual(bits(a.divida_pendente),bits(b.divida_pendente))
                        self.assertEqual(bits([vars(x) for x in a.agentes]),bits([vars(x) for x in b.agentes]))
                        self.assertEqual(bits({k:vars(x) for k,x in a.tarefas.items()}),bits({k:vars(x) for k,x in b.tarefas.items()}))
if __name__=='__main__':unittest.main()
