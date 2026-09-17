"""Reconfere artefatos publicados; não executa HM nem altera o simulador."""
import csv
import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BRUTO = RAIZ / 'outputs/diagnosticos/teste_TL_20260917/bruto.csv'
ROBUSTEZ = RAIZ / 'outputs/diagnosticos/correcao_estrutural_20260916/robustez/resumo.csv'
METRICAS = ('atraso_relativo', 'taxa_omissao', 'divida_latente_sobre_plano')


def valor(linha, metrica):
    if metrica == 'atraso_relativo':
        return float(linha['makespan']) / float(linha['makespan_cpm'])
    return float(linha[metrica])


def verificar(linhas):
    grupos = {}
    for linha in linhas:
        chave = tuple(linha[k] for k in ('arquivo', 'semente', 'cenario'))
        grupo = grupos.setdefault(chave, {})
        assert linha['lei'] not in grupo, ('duplicata', chave)
        grupo[linha['lei']] = linha
    assert grupos
    for chave, grupo in grupos.items():
        assert set(grupo) == {'unitario', 'crowder_eq3'}, chave
        for m in METRICAS:
            assert valor(grupo['unitario'], m).hex() == valor(grupo['crowder_eq3'], m).hex(), (chave, m)
    return len(grupos)


def main():
    with BRUTO.open() as f:
        linhas = list(csv.DictReader(f))
    pares = verificar(linhas)
    # Controle do verificador: cada indicador adulterado deve provocar rejeição.
    negativos = {}
    for m in METRICAS:
        adulteradas = [dict(x) for x in linhas]
        campo = 'makespan' if m == 'atraso_relativo' else m
        adulteradas[0][campo] = str(float(adulteradas[0][campo]) + 1)
        try:
            verificar(adulteradas)
        except AssertionError:
            negativos[m] = 'rejeitado'
        else:
            raise AssertionError(('verificador não detectou adulteração', m))
    with ROBUSTEZ.open() as f:
        robustez = list(csv.DictReader(f))
    sinais = {}
    for m in METRICAS:
        celulas = [x for x in robustez if x['metrica'] == m]
        assert len({x['configuracao'] for x in celulas}) == len(celulas) == 129
        assert all(float(x['media_diferenca']) < 0 for x in celulas)
        sinais[m] = {'negativos': len(celulas), 'IC95_inteiro_negativo': sum(float(x['ic95_superior']) < 0 for x in celulas)}
    saida = {'pares_csv_identicos': pares, 'metricas': list(METRICAS),
             'controles_adulterados': negativos, 'robustez': sinais,
             'escopo': '384 pares nominais TL; 129 células históricas de robustez unitária, não reexecutadas',
             'sha256': {str(p.relative_to(RAIZ)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (BRUTO, ROBUSTEZ)}}
    destino = RAIZ / 'outputs/diagnosticos/observaveis_20260917'
    destino.mkdir(exist_ok=True)
    (destino/'verificacao.json').write_text(json.dumps(saida, indent=2, ensure_ascii=False)+'\n')
    tabela = '| Indicador | Pares TL idênticos | Contrastes negativos | IC95 inteiramente negativo |\n|---|---:|---:|---:|\n'
    for m, s in sinais.items():
        tabela += f"| {m} | {pares}/{pares} | {s['negativos']}/{len(celulas)} | {s['IC95_inteiro_negativo']}/{len(celulas)} |\n"
    (destino/'evidencia.md').write_text(tabela)
    print(json.dumps(saida, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
