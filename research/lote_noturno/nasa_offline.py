"""Reexecução NASA offline com saídas independentes, sem editar parâmetros."""
import importlib.util,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
out=ROOT/'outputs/diagnosticos/noturno_E1';out.mkdir(exist_ok=False)
p=ROOT/'src/nasa/05_faixas_complexidade.py'
spec=importlib.util.spec_from_file_location('nasa05',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.DIR_TABELAS=out;m.DIR_LOGS=out
files=[p,m.ARQUIVO_BASE,*sorted((ROOT/'data/raw/nasa_dpp_reference').glob('*.arff'))]
(out/'manifesto.json').write_text(json.dumps(dict(versao='NASA D double-prime (Dpp) de Shepperd; arquivos offline do repositório',hashes={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in files}),indent=2)+'\n')
m.main()
