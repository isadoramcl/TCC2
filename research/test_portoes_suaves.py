"""Portões suaves (projeto/74): opcionais, desligados por default.

Contratos: (1) com as opções default o nominal arquivado é reproduzido bit a bit;
(2) o portão logístico abre a assistência no arranjo centralizado;
(3) a fuga logística dispara e o projeto termina;
(4) uma chave historicamente travada (B2, s_transicao=0,01) termina com o portão logístico."""
from dataclasses import asdict
from pathlib import Path
import sys,unittest
import pandas as pd,yaml
RAIZ=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(RAIZ/'src/modelo'))
import simulador as S
from simulador_mvp import SimulacaoMVP,OpcoesMVP

def opcoes(**extra):
    op=yaml.safe_load((RAIZ/'config/mvp.yaml').read_text())['opcoes']; op['instrumentar_tarefas']=False; op.update(extra)
    return OpcoesMVP(**op)

def rodar(arq,seed,cen,op,par=None):
    p=S.carregar_parametros()
    for (sec,k),v in (par or {}).items(): p[sec][k]['valor']=v
    g,d,c=S.carregar_instancia(arq); sim=SimulacaoMVP(g,d,c,p,cen,seed,opcoes=op); return sim,sim.executar()

class PortoesSuaves(unittest.TestCase):
    def test_default_nao_cria_fluxo_auxiliar_e_reproduz_nominal(self):
        arq=pd.read_csv(RAIZ/'outputs/diagnosticos/noturno_nominal/bruto.csv',float_precision='round_trip')
        for cen in ['centralizada','adaptativa']:
            sim,r=rodar('j6010_1.sm',0,cen,opcoes())
            self.assertIsNone(sim.rng_aux)
            ref=arq[(arq.arquivo=='j6010_1.sm')&(arq.semente==0)&(arq.cenario==cen)].iloc[0]
            linha={k:v for k,v in asdict(r).items() if isinstance(v,(int,float,bool))}; linha.update(r.contadores)
            for campo in ['makespan','TW','TL','TU','TR','taxa_omissao','taxa_falha_efetiva','divida_latente_sobre_plano','p1_omissao','p1_fuga','N_req']:
                self.assertEqual(float(linha[campo]).hex(),float(ref[campo]).hex(),campo)

    def test_portao_logistico_abre_assistencia_no_centralizado(self):
        _,base=rodar('j6010_1.sm',0,'centralizada',opcoes())
        _,novo=rodar('j6010_1.sm',0,'centralizada',opcoes(portao_assistencia='logistico'))
        self.assertEqual(base.contadores['N_req'],0)
        self.assertGreater(novo.contadores['N_req'],0)
        self.assertGreater(novo.contadores['confianca_media_final'],.25)
        self.assertTrue(novo.concluiu); self.assertEqual(novo.violacoes,[])

    def test_fuga_logistica_dispara_e_termina(self):
        _,r=rodar('j6010_1.sm',0,'centralizada',opcoes(regra_fuga='logistica'))
        self.assertGreater(r.contadores['p1_fuga'],0)
        self.assertTrue(r.concluiu); self.assertEqual(r.violacoes,[])

    def test_chave_travada_do_B2_termina_com_portao_logistico(self):
        b=pd.read_csv(RAIZ/'outputs/diagnosticos/lote41_B2_censura_20260918/bruto.csv')
        k=b[~b.concluiu].iloc[0]
        par={('agentes','tau_sat'):float(k.tau_sat),('agentes','s_transicao'):float(k.s_transicao)}
        _,r=rodar(k.arquivo,int(k.semente),k.cenario,opcoes(portao_assistencia='logistico',canal_erro_direto=k.canal,limite_horizonte_fator=16),par)
        self.assertTrue(r.concluiu)

    def test_opcoes_invalidas(self):
        with self.assertRaises(ValueError): OpcoesMVP(portao_assistencia='x')
        with self.assertRaises(ValueError): OpcoesMVP(efeito_fuga='x')
        with self.assertRaises(ValueError): OpcoesMVP(portao_assistencia='logistico')

if __name__=='__main__': unittest.main()
