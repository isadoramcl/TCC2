"""Rótulos obrigatórios de censura/indefinição para tabelas finais B2."""
import pandas as pd

def rotular(d):
    if 'censuradas' not in d or 'media' not in d:
        raise ValueError('tabela final exige media e contagem censuradas')
    x=d.copy();labels=[];values=[]
    for r in x.to_dict('records'):
        parts=[]
        if r['censuradas']>0:parts.append(f"CENSURADO: {int(r['censuradas'])} execucoes; nao terminal")
        n=r.get('pares_indefinidos',r.get('fracao_indefinida',0))
        if n>0 or pd.isna(r['media']):parts.append(f'INDEFINIDO/PARCIAL: {int(n)} sem denominador')
        status='; '.join(parts) or 'COMPLETO';labels.append(status)
        values.append(('NA' if pd.isna(r['media']) else f"{r['media']:+.6f}")+' ['+status+']')
    x['estatuto']=labels;x['valor_rotulado']=values
    return x

def publicar(d,path):
    x=rotular(d);x.to_csv(path,index=False)
    cols=[c for c in ['etapa','canal','tau_sat','s_transicao','cenario','metrica','valor_rotulado','ic95_inferior','ic95_superior'] if c in x]
    lines=['| '+' | '.join(cols)+' |','|'+'|'.join(['---']*len(cols))+'|']
    for row in x[cols].itertuples(index=False,name=None):lines.append('| '+' | '.join('NA' if pd.isna(v) else str(v) for v in row)+' |')
    path.with_suffix('.md').write_text('# Tabela final — rótulo integra o valor\n\n'+ '\n'.join(lines)+'\n')
    return x
