"""Inventário estático por arquivo + evidências executadas, sem importar runners."""
import ast,csv,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/diagnosticos/20260928_hm_v3'

def main():
 rows=[]
 for folder in ['src','research']:
  for p in sorted((ROOT/folder).rglob('*.py')):
   if any(x in p.parts for x in ['__pycache__','snapshot']):continue
   rel=str(p.relative_to(ROOT));txt=p.read_text();tree=ast.parse(txt);calls=[]
   for n in ast.walk(tree):
    if isinstance(n,ast.Call):
     f=ast.unparse(n.func)
     if any(x in f for x in ['Simulacao','executar','rodar','carregar_parametros','job_b9']):calls.append(f'{n.lineno}:{f}')
   conf=[x for x in ['mvp.yaml','mvp_v1.yaml','mvp_v2.yaml','parametros_v2.yaml'] if x in txt]
   evidence='inspeção estática; nenhuma execução nominal v3 comprovada para esta entrada'
   status='NÃO EXECUTADO SOB NOMINAL V3'
   why='Entrada histórica/auxiliar; não presumir cobertura porque importa núcleo testado. Exige desenho e saída nova antes de reexecutar.'
   if rel.startswith(('src/nasa/','src/psplib/')):
    status='NÃO APLICÁVEL À DINÂMICA V3';why='Pipeline de dados NASA/PSPLIB; não simula agentes. Dados preservados, reprocessamento fora do escopo.'
   if p.name in ['simulador.py','simulador_mvp.py','fuzzy.py','ancoragem_stewart.py','heterogeneidade_erro.py']:
    status='BIBLIOTECA, NÃO PIPELINE';why='Cobertura depende das opções chamadas; núcleo nominal exercitado pela 79 e HM, sem alegação sobre todos os ramos.'
   if rel.startswith('research/test_'):
    status='TESTE, NÃO EXPERIMENTO NOMINAL';evidence='unittest discover -s research -p test_*.py -v; ver log desta entrega';why='Casos unitários e controles históricos incluem entradas inválidas intencionais. Suíte não substitui rodada de cada pipeline.'
   if rel=='research/lote_noturno/test_cobertura.py':
    status='TESTE HISTÓRICO NÃO EXECUTADO NESTE LOTE';why='Módulo aninhado não deve ser presumido executado pelo discover raiz; teste do desenho legado. Novos testes v3 são explícitos.'
   if 'mvp_v1.yaml' in conf:
    why='Configuração histórica v1: executar esse caminho não é validar nominal v3. Leitura de parâmetros vivos exige snapshot correspondente para replay.'
   if rel.startswith('src/modelo/') and p.name[:2] in ['02','03','07','09','10','11']:
    why='Usa Simulacao legado, não as opções MVP v3; saídas históricas e cenários/ablações próprios. Não executado como nominal v3.'
   if rel=='src/modelo/05_figuras_modelo.py':
    why='Figura 9 simula 8×6×2=96 trajetórias no núcleo legado; outras figuras leem evidências. Não é apenas renderização; não executar sobre saídas congeladas.'
   if rel=='src/modelo/22_consolidar_mvp.py':
    why='rodar_b9 também executa simulações via 20, com opções v1; não é só relatório. Preservado sem reexecução v3.'
   if rel=='src/modelo/20_experimento_mvp.py':
    why='Desenho completo de alternativas/robustez não reexecutado sob v3; importação em teste não prova cobertura. Grupo nominal coberto pela 79 não equivale a todas as células deste runner.'
   if p.name[:2] in ['04','15','17','19'] and rel.startswith('src/modelo/') or rel=='research/lote_noturno/cobertura.py':
    why='Espaço histórico com k_heuristico livre, direta ou indiretamente; nova execução com parâmetros v3 incompatível. Substituto versionado: research/hm_v3.py. Não rodar legado para produzir evidência v3.'
   if rel in ['research/validacao/nominal_v2.py','research/validacao/gov_v2.py','research/validacao/teste_aleatorio.py']:
    why='Desenho foi coberto pelo runner 79, mas esta entrada não foi rodada como v3. Lê nominal vivo e conserva caminhos/rótulos v2: risco de sobrescrita ou mistura de versão.'
    evidence='equivalência de desenho: 20260928_drenagem_heuristica/etapa3; não equivalência de entrada executada'
   if rel=='research/validacao/c4_dinamico.py':
    why='Alias v2 aponta a mvp.yaml vivo; fixa pressão e limita horizonte a 16. Nem nominal v3 nem replay seguro sem snapshot; não reexecutado.'
   if rel in ['research/discriminante_falha.py','research/fatorial_78.py','research/conferencia_round_trip_78.py']:
    why='Teste histórico 78, anterior à v3; não promover sua evidência ao nominal atual. Alguns caminhos verificam manifesto antigo ou escrevem em destino fixo.'
   if rel=='research/controle_previo_79.py':
    status='CONTROLE HISTÓRICO EXECUTADO NA 79';evidence='20260928_drenagem_heuristica/controle_previo';why='k_heuristico=0,10 intencional, guardas antigas/novas; não constitui rodada nominal v3.'
   if rel=='research/etapa1_drenagem_79.py':
    status='EXECUTADO: CANDIDATO INTERMEDIÁRIO';evidence='20260928_drenagem_heuristica/etapa1';why='Drenagem antes de separar k_fuga; v3 final validada depois pela etapa3, não confundir versões intermediárias.'
   if rel=='research/validacao_drenagem_79.py':
    status='EXECUTADO SOB V3 FINAL';evidence='20260928_drenagem_heuristica/etapa3/bruto_completo.csv e verificacoes.json';why='4704 execuções: nominal384, fora1152, aleatório576, GOV2592; zero violações e todas completas. Governança é varredura sobre a base v3.'
   if rel in ['research/hm_v3.py','research/cobertura_pareada_v3.py']:
    status='EXECUTADO SOBRE BASE V3, PARÂMETROS VARRIDOS';evidence='20260928_hm_v3/ e subdiretório cobertura_pareada; validade nos CSVs';why='Substituto 5D novo. Não é repetição apenas do ponto nominal: verifica todas as propostas e verdade derivada.'
   if rel in ['research/analisar_hm_v3.py','research/inventariar_pipelines_v3.py']:
    status='ANÁLISE DESTA ENTREGA, SEM NOVAS SIMULAÇÕES';evidence='20260928_hm_v3/auditoria e inventario_pipelines.csv';why='Reconferência de resultados e classificação estática, não valida ramos de simulador.'
   if rel=='research/arrumacao/renomear.py':
    status='MANUTENÇÃO NÃO EXECUTADA';why='Renomeia artefatos; incompatível com a preservação de evidência solicitada.'
   if rel in ['src/modelo/'+name for name in ['01_derivar_parametros.py','06_exportar_parametros.py','08_verificar_ablacao.py','12_porta2_operacionalizacao.py','13_exportar_tabelas_entrega.py','14_experimento_por_instancia.py','16_reanalise_revisao.py','18_analisar_pilotos_revisao.py','24_analisar_correcao.py']]:
    status='ANÁLISE/PREPARAÇÃO NÃO REEXECUTADA';why='Não contém chamada direta de simulação neste caminho; depende de dados/evidências de sua versão. Não gera prova nova de zero violações.'
   if why.startswith('Entrada histórica'):
    analysis_names={'gerar_relatorio_arranjo.py','a1_relatorio.py','analisar_nominal.py','analisar_tb23.py','crowder1_relatorio.py','gov2.py','sat_gov_relatorio.py','relatar_fatorial_78.py','relatorio.py','rotas_rotulos.py','analise.py','analise_portoes.py'}
    if p.name in analysis_names:
     status='ANÁLISE HISTÓRICA NÃO REEXECUTADA';why='Recalcula tabelas/figuras de evidência histórica; não simula o nominal v3. Reexecução pode escrever no destino antigo; análise nova deve escolher entrada/saída versionadas.'
    elif p.name in {'distribuicoes.py','validar_c3.py','validar_c3_39.py','c3.py','c2_precontrole.py'}:
     status='CONTROLE MATEMÁTICO, NÃO SIMULAÇÃO V3';why='Bancada Stewart/Beta: sem agentes nem guarda de drenagem. Protocolos 37/39/41 têm critérios históricos distintos; não reexecutar como novo veredito. Testes atuais de fórmula/discriminação estão na suíte.'
     if p.name=='c2_precontrole.py':why+=' Este arquivo ainda registra o critério de casas decimais retratado; serve como histórico, não critério vigente.'
    elif p.name=='rotulagem.py':
     status='BIBLIOTECA DE CENSURA';why='Formata/propaga rótulos de censura, não roda agentes. Cobertura unitária nos testes B2/rotulagem; grade B2 não reexecutada como v3.'
    elif p.name=='nasa_offline.py':
     status='DADOS NASA, NÃO SIMULAÇÃO V3';why='Reprocessa faixas NASA offline e escreve noturno_E1; drenagem não se aplica. Evidência antiga preservada.'
    elif p.name=='recuperar_evidencias.py':
     status='RECUPERAÇÃO DE ARTEFATOS NÃO EXECUTADA';why='Extrai objetos históricos com git show e verifica hash; sem simulação. Evidências necessárias já presentes.'
    elif p.name=='verificar_documento_oficial.py':
     status='VERIFICADOR DOCUMENTAL';why='Confere integridade documental, sem agentes. Teste test_documento_oficial executado na suíte; CLI não reexecutada como pipeline v3.'
    elif p.name=='verificar_independencia_tl.py':
     status='REANÁLISE TL HISTÓRICA NÃO EXECUTADA';why='Verifica CSVs TL de setembro e escreve observaveis_20260917; não roda simulação. Não sobrescrever a evidência congelada.'
   rows.append(dict(arquivo=rel,status=status,evidencia=evidence,motivo=why,configs_literais=';'.join(conf),chamadas_relevantes=';'.join(calls),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 out=OUT/'inventario_pipelines_final.csv'
 with out.open('x') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 text='''# 82 — Inventário de pipelines e alcance da validação v3

28/09/2026. Lista por arquivo de `src/` e `research/`, incluindo módulos sem main, testes e análise. Não executa imports para descobrir tarefas: alguns scripts escrevem ao importar. O CSV final (`inventario_pipelines_final.csv`) refina a classificação auxiliar; a primeira listagem permanece preservada. O CSV associado contém hash, chamadas e configurações literais por arquivo. A classificação estática não constitui prova de execução. Não foram encontrados entrypoints shell/notebooks/Makefile no levantamento com rg.

## O que está comprovado e o que não está

- Runner 79, etapa3: 4704 execuções da base v3 final (384 nominal, 1152 fora, 576 amostra aleatória, 2592 governança). Todas completas, zero violações. Etapa1 é intermediária; controle prévio usa kh inválido deliberadamente.
- HM e cobertura 81/81A: novos pipelines versionados; as contagens e a validade finais estão no parecer 81 e nos brutos. Derivação checada antes de cada execução.
- Suíte: ver log da entrega. Testes de casos neutros/legados não equivalem a reexecutar todos os desenhos sob v3. O módulo aninhado lote_noturno/test_cobertura.py é listado separadamente, sem presumir descoberta recursiva.
- Não há evidência de que TODAS as entradas antigas executem corretamente sob a v3. Não faço essa alegação. Cada entrada não executada tem justificativa abaixo; a base v3 foi validada pelos runners explicitamente indicados.

## Riscos operacionais encontrados no inventário

1. 04, 15, 17, 19 e cobertura antiga continuam sendo código de experimento histórico, com dimensão kh livre. **Não usar esses caminhos para HM v3.** O substituto é research/hm_v3.py, com cobertura pareada complementar. Manter o código anterior não autoriza executá-lo com config viva.
2. `nominal_v2.py`, `gov_v2.py` e `c4_dinamico.py` combinam rótulo/caminho v2 com `mvp.yaml` vivo. A v3 foi executada via 79 em saídas novas. Não rodar os caminhos antigos sobre outputs congelados. Corrigir a CLI histórica para exigir versão/saída explícita é pendência operacional, não uma execução feita neste lote.
3. `mvp_v1.yaml` congela opções, mas sozinho não congela os parâmetros carregados de `parametros.yaml` vivo nem o núcleo. Replay requer o conjunto de snapshots correspondente. Não anunciar identidade v1 só pela seleção desse YAML.
4. `05_figuras_modelo.py` inclui simulação na figura 9; `22_consolidar_mvp.py` inclui repetição B9. Corrige a classificação ampla de “apenas figuras/relatório” no parecer 80. Os scripts 12 e 14, apesar do nome, são análise de resultados.
5. Runner 20 pode ler a configuração atual, mas sua grade completa não foi reexecutada sob v3. Não estender as 4704 execuções da 79 a todas as suas ablações.

**Critério de continuidade:** acrescentar linha/evidência quando um novo pipeline rodar; registrar versão das opções, parâmetros, núcleo e saída; nunca inferir cobertura a partir do nome do arquivo ou de teste de importação.

## Inventário por arquivo

| Arquivo | Estatuto | Evidência / motivo |
|---|---|---|
'''
 for row in rows:text+=f"| `{row['arquivo']}` | {row['status']} | {row['evidencia']}. {row['motivo']} |\n"
 (ROOT/'projeto/82_INVENTARIO_PIPELINES_V3.md').write_text(text)
 print('Inventariados',len(rows),'arquivos')
if __name__=='__main__':main()
