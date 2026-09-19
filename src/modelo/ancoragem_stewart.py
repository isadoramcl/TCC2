"""Stewart & Melchers: seis pontos da tabela e interpolação linear declarada.

O mapa de dificuldade de tarefa para passos é sintético, não medido em PSPLIB.
"""
import math
MAPAS_PASSOS={
    'curto':{'baixa':1,'media':2,'alta':3,'muito alta':4},
    'longo':{'baixa':1,'media':2,'alta':4,'muito alta':8},
}
def ancora_stewart(k):
    if not math.isfinite(k) or not 1<=k<=8:
        raise ValueError('Stewart: k deve estar entre 1 e 8; extrapolação não é ancoragem')
    return k*.0128
