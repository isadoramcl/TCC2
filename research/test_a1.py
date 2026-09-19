import copy,sys,unittest
from pathlib import Path
from dataclasses import asdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/modelo'))
from simulador_mvp import SimulacaoMVP,OpcoesMVP
from test_mvp import caso
from test_compatibilidade import bits
class Fuga(unittest.TestCase):
    def sim(self,regra,limite,heu=True):
        g,p=caso(heuristico=heu);p['gestor']['limite_aversao_perda']['valor']=limite
        s=SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(regra_fuga=regra,limite_horizonte_fator=1,rho_omissao=0.))
        return s,s.executar()
    def test_acao_e_controle_negativo(self):
        _,a=self.sim('dependente_estado',.4);_,b=self.sim('dependente_estado',.6)
        self.assertGreater(a.contadores['p1_fuga'],0);self.assertFalse(a.concluiu)
        self.assertEqual(b.contadores['p1_fuga'],0);self.assertTrue(b.concluiu)
        _,c=self.sim('dependente_estado',.1,False);self.assertEqual(c.contadores['p1_fuga'],0)
    def test_condicao_depende_do_estado_e_estrita(self):
        g,p=caso();s=SimulacaoMVP(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(regra_fuga='dependente_estado'))
        self.assertFalse(s.deve_fugir(.75,.5,.25))
        self.assertTrue(s.deve_fugir(.76,.5,.25))
        self.assertFalse(s.deve_fugir(.4,.5,.1))
    def test_constante_explicita_identica_default(self):
        g,p=caso(heuristico=True)
        a=SimulacaoMVP(g,[1],8,copy.deepcopy(p),'centralizada',2)
        b=SimulacaoMVP(g,[1],8,copy.deepcopy(p),'centralizada',2,opcoes=OpcoesMVP(regra_fuga='constante'))
        self.assertEqual(bits(asdict(a.executar())),bits(asdict(b.executar())))
        self.assertEqual(a.rng.bit_generator.state,b.rng.bit_generator.state)
    def test_contrafactual_mesmo_estado_e_sorteio(self):
        import math
        class ForcarP1(SimulacaoMVP):
            def decidir_porta(self,p_heu,sorteio):return True
        def executar(regra,limite):
            g,p=caso();p['agentes']['tau_sat']['valor']=.03-math.log(3.)
            p['gestor']['limite_aversao_perda']['valor']=limite
            a=ForcarP1(g,[1],8,p,'centralizada',0,opcoes=OpcoesMVP(regra_fuga=regra,rho_omissao=0.,limite_horizonte_fator=1))
            a.executar();return a.registros_tarefas[0]
        a,b=executar('constante',.3),executar('dependente_estado',.3)
        for k in ['tarefa','agente','Di','P','B','mu_cog','mu_rede','E','p_heu','sorteio_porta']:
            self.assertEqual(a[k],b[k])
        self.assertEqual(a['porta'],'P1_fuga');self.assertEqual(b['porta'],'P1_omissao')
        c,d=executar('constante',.6),executar('dependente_estado',.6)
        self.assertEqual(bits(c),bits(d))  # controle negativo: não detecta diferença

    def test_opcao_invalida(self):
        with self.assertRaises(ValueError):OpcoesMVP(regra_fuga='typo')
if __name__=='__main__':unittest.main()
