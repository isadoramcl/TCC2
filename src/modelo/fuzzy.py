"""
fuzzy.py — Sistema de inferência difusa de Mamdani
===================================================

Implementa o mecanismo que o TCC I especifica na seção 4.4.2: fuzzificação por
funções de pertinência triangulares, inferência pelo método Max-Min, e
defuzzificação para obter o valor exato que alimenta as equações de fluxo.

`[TCC1]` As três etapas e a escolha de pertinências triangulares e de inferência
Max-Min vêm da fase conceitual.
`[LIT]` LIU, S.; TRIANTIS, K. P.; SARANGI, S. Representing qualitative variables
and their interactions with fuzzy logic in system dynamics modeling. *Systems
Research and Behavioral Science*, v. 28, p. 245-263, 2011.

`[DEC]` A defuzzificação é feita por **centroide sobre a função de pertinência
agregada**, calculada por integração numérica em malha regular. A alternativa —
consequentes como valores isolados e média ponderada — seria mais barata, mas
não é centroide de fato, e o TCC I especifica centroide. A malha é fixa e
declarada, de modo que o resultado é determinístico.

`[ACHADO 8]` **A configuração especificada pelo TCC I não pode ser monótona, e
existe teorema que diz exatamente por quê.**

A monotonicidade é requisito do modelo, não preferência estética: a saída é um
multiplicador de produtividade, e produtividade não pode SUBIR quando a fadiga
ou a pressão sobem. A primeira implementação, fiel ao TCC I (Mamdani com
t-norma **mínimo**, agregação por máximo, defuzzificação por centroide),
apresentava regiões de derivada positiva. A caracterização por refinamento de
malha mostrou que o efeito é de INCLINAÇÃO, não de discretização — a violação
escala linearmente com o passo e a razão converge para ≈ 0,26.

A explicação é um resultado publicado:

> VAN BROEKHOVEN, E.; DE BAETS, B. *Only Smooth Rule Bases Can Generate Monotone
> Mamdani–Assilian Models Under Center-of-Gravity Defuzzification.* **IEEE
> Transactions on Fuzzy Systems**, v. 17, n. 5, p. 1157-1174, out. 2009.
> DOI 10.1109/TFUZZ.2009.2023328.
> `https://ieeexplore.ieee.org/document/4957084/`

A **Tabela IX** do artigo enumera as CINCO únicas configurações de modelo
Mamdani–Assilian sob defuzzificação por centroide para as quais a monotonicidade
é garantida:

| # | entradas `m` | t-norma | base de regras | exigência extra sobre os consequentes |
|---|---|---|---|---|
| 1 | 1 | mínimo `T_M` | monótona | não usar os termos extremos; intervalos de transição de igual comprimento |
| 2 | 1 | produto `T_P` | monótona | — |
| 3 | 1 | Łukasiewicz `T_L` | monótona | não usar os termos extremos; intervalos de igual comprimento |
| 4 | **2** | **produto `T_P`** | **monótona e suave** | **—** |
| 5 | 3 | produto `T_P` | monótona e suave | várias |

Este sistema tem **duas** entradas. A combinação (m = 2, `T_M`) **não aparece na
tabela**: para duas entradas, o artigo conclui textualmente que *"when designing
a monotone model with more than one input variable, one should opt for the
product `T_P` and use a monotone smooth rule base"*. A não-monotonicidade
observada não era, portanto, defeito de implementação nem ruído numérico — era o
comportamento previsto pela teoria para a configuração escolhida.

Duas premissas do artigo foram verificadas por código (ver autoteste):

1. **Base de regras monótona e suave** (Definições 2.1 e 2.2). A matriz 3×3
   satisfaz ambas: as diferenças de índice de consequente entre regras vizinhas
   são todas 0 ou +1. Esta condição **já era atendida**.
2. **Termos de saída formando partição difusa** (Seção II). Os conjuntos
   originais — centros 0,30 / 0,65 / 0,95 com meia-base 0,30 — somam entre 0 e 1
   e **não** constituem partição. Esta condição **não era atendida**.

`[ACHADO 9]` A implementação também aplicava `mínimo` para modificar o
consequente qualquer que fosse a t-norma escolhida. As equações (2), (5) e (6)
do artigo usam a **mesma** t-norma `T` na conjunção do antecedente e na
modificação do consequente: `A'_i(y) = T(α_i, A_i(y))`. Com `T_M` isso é
truncamento e coincidia com o que estava escrito; com `T_P` é **escala**, e sem a
correção o produto não recuperava a monotonicidade. Corrigido.

`[DEC]` Adota-se a configuração da **linha 4 da Tabela IX**: t-norma produto e
partição difusa uniforme na saída. A escolha do TCC I permanece disponível como
`fuzzy.t_norma: minimo` e é executada em varredura, de modo que a diferença seja
mensurada e não decretada. Medição em malha de 161 × 161 pontos:

    configuracao                                   pior derivada positiva
    T_M (mínimo)  + conjuntos originais (TCC I)              0,258112
    T_P (produto) + conjuntos originais                      0,000000
    T_M (mínimo)  + partição difusa                          0,420881
    T_P (produto) + partição difusa   <-- Tabela IX, linha 4  0,000000

A configuração adotada é **exatamente monótona** dentro da precisão da
integração, e não apenas tolerável. O critério do autoteste deixa de ser uma
tolerância escolhida por nós e passa a ser a previsão do teorema: derivada
positiva nula.

`[DEC]` A partição uniforme torna os centros de saída **estruturais** (núcleos em
0, 0,5 e 1) em vez de arbitrados. Com isso `consequentes` e `largura_saida`
deixam de ser premissas numéricas do modelo. A faixa bruta muda de
[0,300; 0,867] para [0,167; 0,834], mas isso é absorvido pelo reescalonamento
para [μ_mín, 1] descrito no ACHADO 5 de `simulador.py`: o sistema difuso fornece
a FORMA da degradação, e a magnitude é parâmetro declarado.

`[A9]` **Correção de uma afirmação falsa.** Esta docstring dizia "nenhum valor
numérico está embutido aqui". Não era verdade: `n_malha` (201),
`resolucao_cache` (0,001), `largura_saida` (0,30), a matriz `REGRAS` e o clip
0,05/0,98 da competência estavam — e continuam — no código.

A afirmação honesta é: **os parâmetros que o modelo varre** (vértices,
consequentes, t-norma, partição de saída, μ_mín) vêm de
`config/parametros.yaml`. Os demais são constantes de implementação, declaradas
aqui e não varridas: a malha e a resolução do cache governam apenas precisão
numérica, e seu efeito é medido pelo autoteste; a base `REGRAS` é estrutural e
sua monotonicidade e suavidade são verificadas por código.

Afirmar "nenhum valor embutido" quando há cinco é pior do que não afirmar nada:
dá ao leitor uma garantia que o arquivo não cumpre.
"""

from __future__ import annotations

import numpy as np


def pertinencia_triangular(x: float | np.ndarray, a: float, b: float, c: float):
    """
    Grau de pertinência triangular com vértices (a, b, c).

    Trata os casos degenerados a == b e b == c, que ocorrem nos termos das
    extremidades ("baixa" com vértices 0,0,0.5 e "alta" com 0.5,1,1) — nesses
    casos a rampa correspondente é vertical e vale 1 no vértice.
    """
    x = np.asarray(x, dtype=float)
    subida = np.where(b > a, (x - a) / np.where(b > a, b - a, 1.0), np.where(x >= a, 1.0, 0.0))
    descida = np.where(c > b, (c - x) / np.where(c > b, c - b, 1.0), np.where(x <= c, 1.0, 0.0))
    return np.clip(np.minimum(subida, descida), 0.0, 1.0)


class SistemaDifuso:
    """
    Sistema Mamdani de duas entradas e uma saída, com três termos linguísticos
    por variável e base de nove regras.

    A base de regras é a matriz 3x3 declarada na especificação do modelo: o
    consequente piora à medida que qualquer das entradas cresce, e a combinação
    das duas entradas é o que o TCC I exige ao falar em "processar as combinações
    dessas variáveis".
    """

    TERMOS = ("baixa", "media", "alta")

    # regras[i][j] = termo de saída quando entrada1 é TERMOS[i] e entrada2 é TERMOS[j]
    REGRAS = (
        ("alto",  "alto",  "medio"),
        ("alto",  "medio", "baixo"),
        ("medio", "baixo", "baixo"),
    )

    def __init__(self, vertices: dict, consequentes: dict, n_malha: int = 201,
                 largura_saida: float = 0.30, resolucao_cache: float = 0.001,
                 t_norma: str = "produto", particao_saida: str = "uniforme"):
        """
        vertices     — {'baixa': [a,b,c], 'media': [...], 'alta': [...]} das ENTRADAS
        consequentes — {'baixo': v, 'medio': v, 'alto': v} centros dos termos de SAÍDA
        n_malha      — pontos da malha de integração para o centroide
        largura_saida— meia-base dos triângulos de saída
        """
        if t_norma not in ("produto", "minimo"):
            raise ValueError(f"t_norma desconhecida: {t_norma!r}")
        if particao_saida not in ("uniforme", "centros_declarados"):
            raise ValueError(f"particao_saida desconhecida: {particao_saida!r}")
        self.t_norma = t_norma
        self.particao_saida = particao_saida
        self.vertices = {k: tuple(v) for k, v in vertices.items()}
        self.consequentes = dict(consequentes)
        self.malha = np.linspace(0.0, 1.0, n_malha)
        self.largura = largura_saida
        # Memoização: a superfície de saída é suave, e o simulador reavalia o
        # sistema milhares de vezes por execução com entradas muito próximas.
        # As entradas são arredondadas a uma resolução declarada e o resultado é
        # reaproveitado. O erro introduzido é medido pelo autoteste.
        self.resolucao = resolucao_cache
        self._cache: dict[tuple[int, int], float] = {}

        # conjuntos de saída pré-computados na malha
        self._saida = {}
        if self.particao_saida == "uniforme":
            # Partição difusa de três termos em [0,1]: os núcleos ficam em 0,
            # 0,5 e 1 e a soma das pertinências vale 1 em todo o domínio, que é
            # a premissa da Seção II de Van Broekhoven & De Baets (2009). Os
            # vértices fora de [0,1] tornam as funções extremas trapezoidais com
            # um lado vertical no limite do domínio, como a Fig. 4 do artigo.
            self._saida = {
                "baixo": pertinencia_triangular(self.malha, -1.0, 0.0, 0.5),
                "medio": pertinencia_triangular(self.malha, 0.0, 0.5, 1.0),
                "alto": pertinencia_triangular(self.malha, 0.5, 1.0, 2.0),
            }
        else:
            for nome, centro in self.consequentes.items():
                a = max(0.0, centro - self.largura)
                c = min(1.0, centro + self.largura)
                self._saida[nome] = pertinencia_triangular(self.malha, a, centro, c)

    def _graus(self, x: float) -> dict:
        return {t: float(pertinencia_triangular(x, *self.vertices[t])) for t in self.TERMOS}

    def avaliar(self, entrada1: float, entrada2: float) -> float:
        """
        Devolve o valor defuzzificado em [0,1], com memoização.

        entrada1 e entrada2 são grandezas em [0,1] em que 0 é a condição
        favorável e 1 a desfavorável (por exemplo, fadiga e pressão).
        """
        chave = (int(round(np.clip(entrada1, 0.0, 1.0) / self.resolucao)),
                 int(round(np.clip(entrada2, 0.0, 1.0) / self.resolucao)))
        memo = self._cache.get(chave)
        if memo is not None:
            return memo
        valor = self._avaliar_exato(chave[0] * self.resolucao, chave[1] * self.resolucao)
        self._cache[chave] = valor
        return valor

    def _avaliar_exato(self, entrada1: float, entrada2: float) -> float:
        e1 = np.clip(entrada1, 0.0, 1.0)
        e2 = np.clip(entrada2, 0.0, 1.0)
        g1, g2 = self._graus(e1), self._graus(e2)

        # Grau de disparo da regra s, equação (1) do artigo: conjunção do
        # antecedente pela t-norma T. Regras de mesmo consequente agregam pelo
        # MÁXIMO — equação (5), alpha_i = max{ beta_s : i_s = i }.
        ativacao = {nome: 0.0 for nome in self._saida}
        for i, t1 in enumerate(self.TERMOS):
            for j, t2 in enumerate(self.TERMOS):
                forca = (min(g1[t1], g2[t2]) if self.t_norma == "minimo"
                         else g1[t1] * g2[t2])
                if forca > 0.0:
                    saida = self.REGRAS[i][j]
                    ativacao[saida] = max(ativacao[saida], forca)

        # `[ACHADO 9]` A MESMA t-norma modifica o consequente — equações (2) e
        # (5): A'_i(y) = T(alpha_i, A_i(y)). Com o mínimo isso é truncamento;
        # com o produto é escala. Aplicar sempre o mínimo aqui anularia o efeito
        # da escolha da t-norma e a monotonicidade não seria recuperada.
        agregada = np.zeros_like(self.malha)
        for nome, forca in ativacao.items():
            if forca > 0.0:
                modificado = (np.minimum(self._saida[nome], forca)
                              if self.t_norma == "minimo" else forca * self._saida[nome])
                agregada = np.maximum(agregada, modificado)

        area = agregada.sum()
        if area <= 0.0:
            # `[A9]` O fallback devolvia a média dos consequentes DECLARADOS
            # (0,633), valor que não pertence à partição uniforme efetivamente em
            # uso — devolveria uma saída de um sistema que não é este. Como as
            # entradas formam partição e a base é completa, alguma regra SEMPRE
            # dispara: chegar aqui é defeito, não caso de contorno. Falha alto.
            raise RuntimeError(
                f"nenhuma regra disparou em ({entrada1:.4f}, {entrada2:.4f}): "
                "a base de regras deixou de ser completa ou a partição de "
                "entrada deixou de cobrir [0,1]")
        return float((self.malha * agregada).sum() / area)


# ---------------------------------------------------------------------
# Autoteste
# ---------------------------------------------------------------------
def _base_de_regras_monotona_e_suave() -> tuple[bool, bool, list[int]]:
    """
    Verifica as Definições 2.1 (monótona) e 2.2 (suave) de Van Broekhoven &
    De Baets (2009) sobre a matriz de regras, por código e não por inspeção.

    As entradas são "quanto maior, pior" e a saída decresce com elas; inverte-se
    a ordem das duas entradas para obter o modelo crescente equivalente que as
    definições do artigo pressupõem.
    """
    ordem = {"baixo": 1, "medio": 2, "alto": 3}
    M = np.array([[ordem[SistemaDifuso.REGRAS[i][j]] for j in range(3)]
                  for i in range(3)])[::-1, ::-1]
    monotona = all(M[a, b] <= M[c, d]
                   for a in range(3) for b in range(3)
                   for c in range(3) for d in range(3) if a <= c and b <= d)
    difs = []
    for a in range(3):
        for b in range(3):
            if a < 2:
                difs.append(int(M[a + 1, b] - M[a, b]))
            if b < 2:
                difs.append(int(M[a, b + 1] - M[a, b]))
    suave = all(d in (-1, 0, 1) for d in difs)
    return monotona, suave, sorted(set(difs))


def _autoteste() -> int:
    vertices = {"baixa": [0.0, 0.0, 0.5], "media": [0.0, 0.5, 1.0], "alta": [0.5, 1.0, 1.0]}
    consequentes = {"baixo": 0.30, "medio": 0.65, "alto": 0.95}
    s = SistemaDifuso(vertices, consequentes)          # configuração adotada
    falhas = []

    # 1. partição das pertinências de ENTRADA: em qualquer x, os graus somam ~1
    for x in np.linspace(0, 1, 21):
        soma = sum(s._graus(float(x)).values())
        if abs(soma - 1.0) > 1e-9:
            falhas.append(f"graus de entrada nao somam 1 em x={x:.2f}: {soma:.6f}")
            break

    # 1b. partição difusa na SAÍDA — premissa da Seção II do artigo, sem a qual
    #     os teoremas da Tabela IX não se aplicam.
    soma_saida = sum(s._saida.values())
    if not np.allclose(soma_saida, 1.0, atol=1e-9):
        falhas.append(f"termos de saida nao formam particao difusa: soma varia em "
                      f"[{soma_saida.min():.4f}, {soma_saida.max():.4f}]")

    # 1c. base de regras monótona e suave — Definições 2.1 e 2.2
    monotona, suave, difs = _base_de_regras_monotona_e_suave()
    if not monotona:
        falhas.append("base de regras nao e monotona (Def. 2.1)")
    if not suave:
        falhas.append(f"base de regras nao e suave (Def. 2.2): diferencas {difs}")

    # 2. saída sempre em [0,1]
    xs = np.linspace(0, 1, 81)
    v = np.array([[s.avaliar(a, b) for b in xs] for a in xs])
    if v.min() < 0 or v.max() > 1:
        falhas.append(f"saida fora de [0,1]: [{v.min():.4f}, {v.max():.4f}]")

    # 3. MONOTONICIDADE EXATA. `[ACHADO 8]` O critério deixou de ser uma
    #    tolerância escolhida por nós e passou a ser a previsão do teorema: com
    #    m = 2, t-norma produto, base monótona e suave e partição difusa na
    #    saída (Tabela IX, linha 4), a monotonicidade é GARANTIDA. Exige-se
    #    portanto derivada positiva nula, a menos do erro de integração.
    passo = float(xs[1] - xs[0])
    derivada_positiva_maxima = max(float(np.diff(v, axis=0).max()),
                                   float(np.diff(v, axis=1).max())) / passo
    TOL_INTEGRACAO = 1e-9
    if derivada_positiva_maxima > TOL_INTEGRACAO:
        falhas.append(f"derivada positiva {derivada_positiva_maxima:.3e} — a "
                      f"configuracao adotada deveria ser exatamente monotona")

    # 3b. a configuração do TCC I (t-norma mínimo) é executada em varredura e
    #     DEVE violar a monotonicidade: se não violasse, o diagnóstico do
    #     ACHADO 8 estaria errado e a troca de t-norma seria injustificada.
    s_min = SistemaDifuso(vertices, consequentes, t_norma="minimo",
                          particao_saida="centros_declarados")
    v_min = np.array([[s_min.avaliar(a, b) for b in xs] for a in xs])
    d_min = max(float(np.diff(v_min, axis=0).max()),
                float(np.diff(v_min, axis=1).max())) / passo
    if d_min <= TOL_INTEGRACAO:
        falhas.append("a configuracao max-min do TCC I nao violou a monotonicidade; "
                      "o diagnostico do ACHADO 8 precisa ser reexaminado")

    # 4. simetria: o sistema trata as duas entradas igualmente
    if not np.allclose(v, v.T, atol=1e-9):
        falhas.append("sistema nao e simetrico nas entradas")

    # 5. extremos
    melhor, pior = s.avaliar(0.0, 0.0), s.avaliar(1.0, 1.0)
    if not (melhor > pior):
        falhas.append(f"extremos invertidos: melhor={melhor:.4f} pior={pior:.4f}")

    # 6. erro introduzido pela memoização, medido contra a avaliação exata
    rng = np.random.default_rng(0)
    amostras = rng.random((4000, 2))
    erro = np.array([abs(s.avaliar(float(a), float(b)) - s._avaliar_exato(float(a), float(b)))
                     for a, b in amostras])
    erro_max, erro_medio = float(erro.max()), float(erro.mean())
    # Limite principiado: 0,5% da faixa de saída do sistema, e não um número
    # escolhido para o teste passar.
    LIMITE_ERRO = 0.005 * (v.max() - v.min())
    if erro_max > LIMITE_ERRO:
        falhas.append(f"erro de memoizacao {erro_max:.6f} excede {LIMITE_ERRO:.6f}")

    print("AUTOTESTE DO SISTEMA DIFUSO")
    print(f"  saida em (0,0)   = {melhor:.4f}   (condicao favoravel)")
    print(f"  saida em (0.5,0.5)= {s.avaliar(0.5,0.5):.4f}")
    print(f"  saida em (1,1)   = {pior:.4f}   (condicao desfavoravel)")
    print(f"  faixa da saida   = [{v.min():.4f}, {v.max():.4f}]")
    print(f"  base de regras — monotona: {monotona}   suave: {suave}   "
          f"(diferencas entre regras vizinhas: {difs})")
    print(f"  particao difusa na saida — soma em [{float(soma_saida.min()):.6f}, "
          f"{float(soma_saida.max()):.6f}]")
    print(f"  maior derivada positiva — configuracao adotada (T_P + particao): "
          f"{derivada_positiva_maxima:.3e}")
    print(f"  maior derivada positiva — configuracao do TCC I (max-min)      : "
          f"{d_min:.6f}")
    print("  Tabela IX, linha 4 de Van Broekhoven & De Baets (2009): para m=2, a")
    print("  monotonicidade so e garantida com t-norma produto e base monotona e")
    print("  suave. A configuracao adotada e exatamente monotona; a do TCC I nao.")
    print(f"  erro da memoizacao — maximo {erro_max:.6f}, medio {erro_medio:.6f}  "
          f"(limite {LIMITE_ERRO})")
    for f in falhas:
        print(f"  [FALHA] {f}")
    if not falhas:
        print("  [OK] particao de entrada e de saida, base monotona e suave,")
        print("       faixa, monotonicidade EXATA, simetria, extremos, memoizacao,")
        print("       e violacao confirmada na configuracao max-min do TCC I")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(_autoteste())
