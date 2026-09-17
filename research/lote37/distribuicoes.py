"""Fórmulas de Stewart, apenas diagnóstico C3; não importadas pelo simulador."""
import math
import numpy as np


def binomial(n,p):
    if n<0 or not 0<=p<=1:raise ValueError('n/p inválidos')
    return np.array([math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)])


def beta_parametros(mu,cv):
    if not 0<mu<1 or cv<=0:raise ValueError('média/CV inválidos')
    t=mu*(1-mu)/(cv*mu)**2-1
    if t<=0:raise ValueError(f'Beta inexistente: mu={mu}, CV={cv}; exige mu<1/(1+CV²)')
    return mu*t,(1-mu)*t


def beta_binomial(n,a,b):
    if n<0 or min(a,b)<=0:raise ValueError('parâmetros beta inválidos')
    lb=lambda x,y:math.lgamma(x)+math.lgamma(y)-math.lgamma(x+y)
    return np.array([math.exp(math.log(math.comb(n,k))+lb(a+k,b+n-k)-lb(a,b)) for k in range(n+1)])


def recorrencia(n,taxa):
    prob=np.zeros(n+1);prob[0]=1.
    for etapa in range(n):
        prox=np.zeros(n+1)
        for k in range(etapa+1):
            p=taxa(k)
            if not 0<=p<=1:raise ValueError(f'probabilidade inválida: k={k}, p={p}')
            prox[k]+=prob[k]*(1-p);prox[k+1]+=prob[k]*p
        prob=prox
    return prob


def p_dependente(n,p_av,phi):
    return recorrencia(n,lambda k:phi*p_av*(k+1))


def terceira_casa(calculado,publicado):
    return f'{calculado:.3f}'==f'{publicado:.3f}'
