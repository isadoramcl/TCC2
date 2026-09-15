"""Recupera evidências históricas por commit e confere SHA-256, sem alterar checkout.

Uso: python3 research/recuperar_evidencias.py --destino /tmp/tcc2-evidencias
Requer clone Git com os objetos históricos (git fetch origin revisao-auditoria).
"""
import argparse
import csv
import hashlib
from pathlib import Path
import subprocess


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino',type=Path,required=True)
    out=p.parse_args().destino; root=Path(__file__).resolve().parents[1]
    rows=list(csv.DictReader((root/'research/EVIDENCE_INDEX.csv').open()))
    # Verifica todos os objetos antes de criar a pasta de saída.
    payloads=[]
    for row in rows:
        path=row['arquivo_local']; commit=row['commit_origem']
        if commit:
            data=subprocess.check_output(['git','show',commit+':'+path],cwd=root)
        else:
            data=(root/path).read_bytes()
        if hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('SHA divergente: '+path)
        payloads.append((path,data))
    out.mkdir(parents=True,exist_ok=False)
    for path,data in payloads:
        dest=out/path; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
    print('Evidências recuperadas e verificadas:',len(payloads))


if __name__=='__main__': main()
