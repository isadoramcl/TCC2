"""
simulador.py — Núcleo do modelo híbrido ABM + Dinâmica de Sistemas
===================================================================

Implementa a especificação de docs/especificacao_modelo.md. Nenhum valor
numérico está embutido: tudo vem de config/parametros.yaml e
config/parametros_derivados.yaml.

RECONCILIAÇÕES ENTRE O PSEUDOCÓDIGO E AS EQUAÇÕES DO TCC I
-----------------------------------------------------------
Ao implementar, três incompatibilidades entre o texto, as equações e o
pseudocódigo do TCC I exigiram decisão explícita. Nenhuma é opcional: sem
resolvê-las o modelo não roda, ou roda com um componente inerte.

`[ACHADO 1] Transição estocástica × limiar determinístico.`
O texto do TCC I afirma que o agente "transita de forma estocástica" para o modo
heurístico; o pseudocódigo escreve `se E(t) > τ_sat`, que é determinístico.
`[DEC]` Prevalece o texto. A transição usa
    p_heuristico = 1 / (1 + exp(−(E − τ_sat)/s))
com `s → 0` recuperando o limiar determinístico. As duas leituras passam a ser
testáveis por sensibilidade em vez de escolhidas por decreto.

`[ACHADO 2] F_base ficaria inerte.`
A equação (4) faz o risco basal incidir sobre a geração de dívida técnica, mas a
Porta 3 do pseudocódigo atribui `Concluída_Limpa` incondicionalmente. Se a Porta
3 nunca falha, `F_base` só atuaria sob sobrecarga — e toda a calibração NASA,
que é a contribuição empírica do trabalho, ficaria sem efeito no caso nominal.
`[DEC]` A probabilidade de defeito segue a equação (4) em TODAS as execuções:
    p_falha = clip( F_base(nível) + R_error · (1 − μ_cognitivo) , 0 , 1 )
Sob a Porta 3, μ_cognitivo é alto e p_falha aproxima-se de F_base; sob a Porta 1,
μ_cognitivo cai e p_falha cresce. A Porta 3 deixa de garantir execução limpa e
passa a ser a execução de MENOR risco, o que é a leitura coerente com a equação.

`[ACHADO 3] A injeção em S_UR é negativa fora da sobrecarga.`
O pseudocódigo injeta `(E − τ_sat) · f_corrup` no estoque, expressão que é
negativa sempre que não há sobrecarga — o estoque diminuiria por execução
limpa, o que não tem sentido físico.
`[DEC]` O estoque passa a acumular **esforço latente de retrabalho**, medido em
períodos, que é a grandeza que será efetivamente paga depois:
    S_UR += f_retrabalho · duração · ( 1 + f_corrup · max(E − τ_sat, 0) )
O termo do TCC I é preservado como **amplificador de severidade**: defeitos
nascidos sob sobrecarga custam mais caro do que defeitos nascidos em execução
nominal. A unidade do estoque passa a ser interpretável e comparável ao esforço
total do projeto, o que permite confrontá-la com os alvos externos de validação
da seção 10.1 da especificação.

`[ACHADO 4] Espiral de morte da bateria.`
Na primeira implementação a drenagem era aplicada de uma só vez no momento da
atribuição, no valor `k · E · duração_efetiva`. Para uma tarefa longa isso zera
a bateria instantaneamente; e como a recuperação só ocorria com o agente livre,
um agente preso numa tarefa longa nunca se recuperava. Diagnóstico: quatro de
seis agentes terminavam com bateria exatamente zero e a execução travava.
`[DEC]` A drenagem passa a ser **por período trabalhado**, e a recuperação
ocorre em todo período em que o agente não está executando. É a leitura
fisicamente coerente de "drena B(t) em taxa acelerada/sustentável" do TCC I: uma
taxa é por unidade de tempo, não um débito único.

`[ACHADO 5] A produtividade colapsava e nunca alcançava o nominal.`
A saída bruta do sistema difuso varia em [0,300; 0,867]. Usada diretamente como
multiplicador, o produto `μ_cog · μ_rede` cai a 0,09 no pior caso — uma tarefa
de 7 períodos levaria 78 — e não passa de 0,76 no melhor, penalizando em 24% uma
equipe descansada e coesa, o que não tem justificativa.
`[DEC]` A saída difusa é **reescalada** para a faixa [μ_mín, 1]: condição ideal
devolve 1 (sem penalidade) e condição extrema devolve μ_mín. O sistema difuso
passa a produzir um índice relativo de degradação, e a faixa do multiplicador
vira parâmetro declarado, com varredura. Isso separa a FORMA da degradação, que
é o que o método difuso aporta, da sua MAGNITUDE, que é premissa.

`[ACHADO 6] A razão de retrabalho media visibilidade, não dano.`
A métrica original era

    retrabalho_sobre_esforco = ( TR + S_UR ) / ( TW + TL + TU + TR )

e apresentava DOIS defeitos independentes, ambos verificados nos dados do
experimento (384 execuções pareadas, `outputs/tables/modelo_03_experimento_bruto.csv`).

(i) **O termo de dívida latente é estruturalmente nulo.** O laço só termina
quando `divida_pendente` está vazia; logo `S_UR_final = 0` em 384 de 384
execuções (resíduo máximo 1,4·10⁻¹⁴, compatível com erro de ponto flutuante).
A métrica prometia somar dívida oculta e, de fato, nunca somava nada: reduzia-se
a `TR / esforço_realizado`.

(ii) **O denominador é inflado pela própria disfunção que se quer medir.** O
esforço realizado inclui `TU`, o tempo ocioso ou bloqueado. No braço
centralizado `TU = 118,2` contra `6,3` no adaptativo, e o denominador total é
30% maior (910,4 contra 636,9). Como consequência, o cenário centralizado
diluía seu retrabalho e parecia MELHOR nessa razão (0,0757 contra 0,0819),
enquanto o retrabalho ABSOLUTO era 23,8% MAIOR (69,1 contra 52,7 períodos). A
razão invertia o sinal do efeito por artefato de auto-normalização.

`[DEC]` A base passa a ser o **esforço planejado** do projeto,
`E_plano = Σ_j duração_j`, que é propriedade da instância e portanto idêntica
nos dois braços — a razão só pode se mover pelo numerador. A métrica
conflacionada é substituída por duas, reportadas separadamente:

    retrabalho_sobre_plano        = TR            / E_plano   (retrabalho pago)
    divida_latente_sobre_plano    = max_t S_UR(t) / E_plano   (exposição oculta)

`retrabalho_sobre_esforco_realizado = TR / esforço_realizado` é mantida apenas
como diagnóstico da eficiência alocativa; não é usada como medida de dano nem
como alvo de validação externa. A separação é necessária porque os dois cenários
diferem justamente em `p_reporte` (0,15 contra 0,75): o adaptativo converte
dívida oculta em retrabalho visível, e um agregado que soma as duas parcelas com
bases diferentes não distingue conversão de redução.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fuzzy import SistemaDifuso  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
NIVEIS = ["baixa", "media", "alta", "muito alta"]


# =====================================================================
# Configuração
# =====================================================================
def carregar_parametros(caminho_base: Path | None = None,
                        caminho_derivados: Path | None = None) -> dict:
    """
    Carrega os parâmetros e aplica por cima os derivados da base.

    Os derivados TÊM PRECEDÊNCIA: são calculados a partir dos dados e devem
    sobrepor os valores de partida arbitrados. É esse mecanismo que faz o modelo
    se readaptar quando a base é trocada.
    """
    base = yaml.safe_load((caminho_base or RAIZ / "config" / "parametros.yaml").read_text(encoding="utf-8"))
    p_der = caminho_derivados or RAIZ / "config" / "parametros_derivados.yaml"
    if p_der.exists():
        der = yaml.safe_load(p_der.read_text(encoding="utf-8"))
        base["agentes"]["n_agentes"]["valor"] = der["n_agentes"]["valor"]
        base["agentes"]["n_agentes"]["condicao"] = "derivado"
        base["execucao"]["horizonte_maximo_fator"]["valor"] = der["horizonte_maximo_fator"]["valor"]
        base["execucao"]["horizonte_maximo_fator"]["condicao"] = "derivado"
        base["gestor"]["escala_pressao"] = {"valor": der["escala_pressao"]["valor"],
                                            "condicao": "derivado"}
    else:
        base["gestor"]["escala_pressao"] = {"valor": 1.5, "condicao": "premissa"}
    return base


def v(no):
    """Extrai o campo 'valor' de um nó de parâmetro."""
    return no["valor"] if isinstance(no, dict) and "valor" in no else no


# =====================================================================
# Estado
# =====================================================================
@dataclass
class Agente:
    ident: int
    competencia: float
    bateria: float
    confianca: float
    livre_em: int = 0
    tarefa_atual: int | None = None
    esforco_corrente: float = 0.0      # E(t) da tarefa em execução
    modo_corrente: str = "analitico"
    periodos_heuristicos: int = 0
    periodos_analiticos: int = 0


@dataclass
class Tarefa:
    ident: int
    duracao: int
    demanda: list[int]
    sucessores: list[int]
    dificuldade: float
    nivel: str
    estado: str = "pendente"
    inicio: int | None = None
    fim: int | None = None
    porta: str | None = None
    defeito_oculto: bool = False


@dataclass
class Resultado:
    concluiu: bool
    makespan: int
    makespan_cpm: int
    E_total: float
    S_UR_final: float
    S_UR_maximo: float
    S_PV_final: float
    TW: float
    TL: float
    TU: float
    TR: float
    n_limpas: int
    n_com_erro: int
    n_reportadas: int
    n_adiamentos: int
    taxa_omissao: float
    E_plano: float
    retrabalho_sobre_plano: float
    divida_latente_sobre_plano: float
    retrabalho_sobre_esforco_realizado: float
    trajetorias: dict = field(default_factory=dict)
    violacoes: list = field(default_factory=list)


# =====================================================================
# Simulador
# =====================================================================
class Simulacao:
    def __init__(self, tarefas: pd.DataFrame, disponibilidade: list[int],
                 makespan_cpm: int, parametros: dict, cenario: str, semente: int):
        self.par = parametros
        self.cen = parametros["cenarios"][cenario]
        self.nome_cenario = cenario
        self.rng = np.random.default_rng(semente)
        self.disponibilidade = list(disponibilidade)
        self.makespan_cpm = makespan_cpm

        cols_r = [c for c in tarefas.columns if c.startswith("R") and c[1:].isdigit()]
        self.tarefas: dict[int, Tarefa] = {}
        for r in tarefas.itertuples():
            sucs = ([int(x) for x in str(r.sucessores).split(";")]
                    if isinstance(r.sucessores, str) and r.sucessores.strip() else [])
            self.tarefas[int(r.tarefa)] = Tarefa(
                ident=int(r.tarefa), duracao=int(r.duracao),
                demanda=[int(getattr(r, c)) for c in cols_r],
                sucessores=sucs, dificuldade=float(r.Di), nivel=str(r.nivel_dificuldade))
        # `[DEC]` Esforco PLANEJADO do projeto: soma das duracoes nominais. E uma
        # propriedade da instancia, identica nos dois cenarios, e por isso serve
        # de base fixa para razoes comparaveis entre bracos (ver ACHADO 6).
        self.E_plano = float(sum(t.duracao for t in self.tarefas.values()))
        self.predecessores: dict[int, set] = {j: set() for j in self.tarefas}
        for j, t in self.tarefas.items():
            for s in t.sucessores:
                if s in self.predecessores:
                    self.predecessores[s].add(j)

        # agentes
        ag = self.par["agentes"]
        n = int(v(ag["n_agentes"]))
        media = v(ag["competencia_inicial"])["media"]
        desvio = v(ag["competencia_inicial"])["desvio"]
        self.agentes = [
            Agente(ident=i,
                   competencia=float(np.clip(self.rng.normal(media, desvio), 0.05, 0.98)),
                   bateria=float(v(ag["b_inicial"])),
                   confianca=float(v(self.cen["tau_inicial"])))
            for i in range(n)
        ]

        # sistema difuso
        fz = self.par["fuzzy"]
        self.difuso = SistemaDifuso(
            v(fz["vertices_triangulares"]), v(fz["consequentes"]),
            t_norma=str(v(fz["t_norma"])),
            particao_saida=str(v(fz["particao_saida"])))
        # faixa bruta do sistema difuso, medida nos cantos, para o reescalonamento
        self._bruto_max = self.difuso.avaliar(0.0, 0.0)
        self._bruto_min = self.difuso.avaliar(1.0, 1.0)
        self._mu_min = float(v(fz["mu_minimo"]))

        # estoques e relógios
        self.S_UR = 0.0
        self.S_PV = 0.0
        self.S_DC = 0.0
        self.TW = self.TL = self.TU = self.TR = 0.0
        self.n_adiamentos = 0
        self.n_reportadas = 0
        self.divida_pendente: list[tuple[int, float]] = []   # (tarefa, esforço latente)
        self.traj = {k: [] for k in ("t", "P", "bateria_media", "mu_cog", "mu_rede",
                                     "S_PV", "S_UR", "concluidas")}
        self.violacoes: list[str] = []

    # -----------------------------------------------------------------
    def pressao(self, t: int) -> float:
        """
        P(t) proporcional ao atraso relativo em relação ao cronograma do CPM.

        `[DEC]` Pressão que responde ao desvio observado, e não crescente no
        tempo de forma exógena — é o que fecha o laço de realimentação. Um
        projeto adiantado não sofre pressão.
        """
        g = self.par["gestor"]
        p_min, p_max = float(v(g["P_min"])), float(v(g["P_max"]))
        escala = float(v(g["escala_pressao"]))
        concluidas = sum(1 for x in self.tarefas.values()
                         if x.estado.startswith("concluida"))
        fracao = concluidas / max(1, len(self.tarefas))
        t_esperado = fracao * self.makespan_cpm
        atraso = (t - t_esperado) / max(1.0, self.makespan_cpm)
        return float(p_min + (p_max - p_min) * np.clip(atraso / max(escala - 1.0, 1e-6), 0.0, 1.0))

    def _reescalar(self, bruto: float) -> float:
        """
        Mapeia a saída bruta do sistema difuso para a faixa [mu_minimo, 1].

        O sistema difuso informa a FORMA da degradação; a faixa do multiplicador
        é parâmetro declarado. Sem isso, condição ideal ainda penalizaria a
        produtividade em 24%, o que não tem justificativa (ver ACHADO 5).
        """
        amplitude = self._bruto_max - self._bruto_min
        if amplitude <= 0:
            return 1.0
        normalizado = (bruto - self._bruto_min) / amplitude
        return float(self._mu_min + (1.0 - self._mu_min) * np.clip(normalizado, 0.0, 1.0))

    def multiplicadores(self, agente: Agente, P: float) -> tuple[float, float]:
        fadiga = 1.0 - agente.bateria
        ocupados = sum(1 for a in self.agentes if a.tarefa_atual is not None)
        carga = ocupados / max(1, len(self.agentes))
        desconfianca = 1.0 - agente.confianca
        return (self._reescalar(self.difuso.avaliar(fadiga, P)),
                self._reescalar(self.difuso.avaliar(desconfianca, carga)))

    def F_base(self, nivel: str) -> float:
        r = self.par["risco"]
        ancora = float(v(r["F_ancora"]))
        rr = v(r["razoes_de_risco"])[nivel.replace(" ", "_")]
        return float(ancora * rr)

    def elegiveis(self, t: int, uso: dict) -> list[int]:
        prontas = []
        for j, tar in self.tarefas.items():
            if tar.estado != "pendente":
                continue
            if not all(self.tarefas[p].estado.startswith("concluida")
                       for p in self.predecessores[j]):
                continue
            if all(uso[k] + tar.demanda[k] <= self.disponibilidade[k]
                   for k in range(len(self.disponibilidade))):
                prontas.append(j)
        return prontas

    # -----------------------------------------------------------------
    def executar(self) -> Resultado:
        par, cen = self.par, self.cen
        ag, ret, ex = par["agentes"], par["retrabalho"], par["execucao"]
        tau_sat = float(v(ag["tau_sat"])); s_tr = float(v(ag["s_transicao"]))
        b_min = float(v(ag["b_min"])); k_an = float(v(ag["k_analitico"]))
        k_he = float(v(ag["k_heuristico"])); r_rec = float(v(ag["r_recuperacao"]))
        omega = float(v(par["gestor"]["omega"]))
        lim_av = float(v(par["gestor"]["limite_aversao_perda"]))
        f_cor = float(v(ret["f_corrup"])); f_ret = float(v(ret["f_retrabalho"]))
        R_err = float(v(par["risco"]["R_error"]))
        p_rep = float(v(cen["p_reporte"])); p_det = float(v(cen["p_deteccao"]))
        tau_min = float(v(cen["tau_min"]))
        horizonte = int(v(ex["horizonte_maximo_fator"])) * self.makespan_cpm

        if k_he <= k_an:
            self.violacoes.append("k_heuristico deve exceder k_analitico (TCC I)")

        t = 0
        while t < horizonte:
            # --- libera agentes que terminaram ---
            for a in self.agentes:
                if a.tarefa_atual is not None and a.livre_em <= t:
                    a.tarefa_atual = None

            if all(x.estado.startswith("concluida") for x in self.tarefas.values()) \
               and not self.divida_pendente:
                break

            P = self.pressao(t)
            uso = [0] * len(self.disponibilidade)
            for x in self.tarefas.values():
                if x.estado == "em_execucao":
                    for k in range(len(uso)):
                        uso[k] += x.demanda[k]

            # --- detecção de dívida oculta ---
            ainda = []
            for (j, esforco) in self.divida_pendente:
                if self.rng.random() < p_det:
                    self.TR += esforco
                    self.S_UR = max(0.0, self.S_UR - esforco)
                else:
                    ainda.append((j, esforco))
            self.divida_pendente = ainda

            # --- atribuição ---
            livres = [a for a in self.agentes if a.tarefa_atual is None]
            for a in sorted(livres, key=lambda x: -x.competencia):
                prontas = self.elegiveis(t, uso)
                if not prontas:
                    break
                j = max(prontas, key=lambda x: self.tarefas[x].dificuldade)
                tar = self.tarefas[j]
                b = max(a.bateria, b_min)
                E = tar.dificuldade * P / b
                dD = tar.dificuldade - a.competencia
                mu_cog, mu_rede = self.multiplicadores(a, P)

                # PORTA 1 — sobrecarga, transição estocástica
                p_heu = 1.0 / (1.0 + math.exp(-(E - tau_sat) / max(s_tr, 1e-9)))
                heuristico = self.rng.random() < p_heu

                if heuristico and omega > lim_av:
                    # fuga: adia
                    self.TU += 1.0
                    self.n_adiamentos += 1
                    a.bateria = max(0.0, a.bateria - k_he * E)
                    continue

                # PORTA 2 — hiato de competência (só se não saturado)
                if not heuristico and dD > 0:
                    apoio = [k for k in self.agentes
                             if k.ident != a.ident and k.tarefa_atual is None
                             and k.confianca > tau_min and k.competencia > a.competencia]
                    if apoio:
                        melhor = max(apoio, key=lambda k: k.competencia)
                        a.competencia = min(0.98, a.competencia +
                                            (15 + 3 * (melhor.competencia - a.competencia)) / 100)
                        self.TL += 1.0
                        melhor.livre_em = t + 1
                        melhor.tarefa_atual = -1     # ocupado dando suporte
                        continue
                    else:
                        self.TU += 1.0
                        continue

                # PORTA 1 (omissão) ou PORTA 3 (analítica) — executa
                produtividade = max(1e-6, mu_cog * mu_rede)
                dur_efetiva = max(1, int(math.ceil(tar.duracao / produtividade)))
                p_falha = float(np.clip(self.F_base(tar.nivel) + R_err * (1 - mu_cog), 0.0, 1.0))
                falhou = self.rng.random() < p_falha

                tar.estado = "em_execucao"
                tar.inicio = t
                tar.fim = t + dur_efetiva
                tar.porta = "P1_omissao" if heuristico else "P3_analitica"
                a.tarefa_atual = j
                a.livre_em = t + dur_efetiva
                for k in range(len(uso)):
                    uso[k] += tar.demanda[k]

                self.TW += dur_efetiva
                # A drenagem é POR PERÍODO, aplicada no avanço do tempo (ACHADO 4).
                a.esforco_corrente = E
                a.modo_corrente = "heuristico" if heuristico else "analitico"
                if heuristico:
                    a.periodos_heuristicos += dur_efetiva
                else:
                    a.periodos_analiticos += dur_efetiva

                if falhou:
                    severidade = 1.0 + f_cor * max(E - tau_sat, 0.0)
                    esforco_latente = f_ret * tar.duracao * severidade
                    if self.rng.random() < p_rep:
                        self.TR += esforco_latente
                        self.n_reportadas += 1
                        tar.estado_final = "reportada"
                    else:
                        self.S_UR += esforco_latente
                        self.divida_pendente.append((j, esforco_latente))
                        tar.defeito_oculto = True

            # --- avança o tempo ---
            for x in self.tarefas.values():
                if x.estado == "em_execucao" and x.fim is not None and x.fim <= t + 1:
                    x.estado = "concluida_com_erro" if x.defeito_oculto else "concluida_limpa"
                    self.S_PV += x.duracao if not x.defeito_oculto else 0.0

            # Drenagem por período trabalhado e recuperação por período livre.
            for a in self.agentes:
                if a.tarefa_atual is not None and a.tarefa_atual != -1:
                    taxa = k_he if a.modo_corrente == "heuristico" else k_an
                    drenagem = taxa * a.esforco_corrente
                    a.bateria = max(0.0, a.bateria - drenagem)
                    self.S_DC += drenagem
                else:
                    a.bateria = min(1.0, a.bateria + r_rec)
                if a.tarefa_atual == -1 and a.livre_em <= t + 1:
                    a.tarefa_atual = None

            self.traj["t"].append(t)
            self.traj["P"].append(P)
            self.traj["bateria_media"].append(float(np.mean([x.bateria for x in self.agentes])))
            self.traj["mu_cog"].append(float(np.mean([self.multiplicadores(x, P)[0]
                                                      for x in self.agentes])))
            self.traj["mu_rede"].append(float(np.mean([self.multiplicadores(x, P)[1]
                                                       for x in self.agentes])))
            self.traj["S_PV"].append(self.S_PV)
            self.traj["S_UR"].append(self.S_UR)
            self.traj["concluidas"].append(sum(1 for x in self.tarefas.values()
                                               if x.estado.startswith("concluida")))
            t += 1

        return self._resultado(t)

    # -----------------------------------------------------------------
    def _resultado(self, t: int) -> Resultado:
        concluiu = all(x.estado.startswith("concluida") for x in self.tarefas.values())
        total = self.TW + self.TL + self.TU + self.TR
        limpas = sum(1 for x in self.tarefas.values() if x.estado == "concluida_limpa")
        erros = sum(1 for x in self.tarefas.values() if x.estado == "concluida_com_erro")

        # verificações de precedência e recursos, a posteriori
        for j, tar in self.tarefas.items():
            if tar.inicio is None:
                continue
            for p in self.predecessores[j]:
                fp = self.tarefas[p].fim
                if fp is not None and tar.inicio < fp:
                    self.violacoes.append(f"precedencia violada: {p} -> {j}")
                    break

        return Resultado(
            concluiu=concluiu, makespan=t, makespan_cpm=self.makespan_cpm,
            E_total=float(self.TW / total) if total > 0 else 0.0,
            S_UR_final=self.S_UR,
            S_UR_maximo=float(max(self.traj["S_UR"])) if self.traj["S_UR"] else 0.0,
            S_PV_final=self.S_PV, TW=self.TW, TL=self.TL, TU=self.TU, TR=self.TR,
            n_limpas=limpas, n_com_erro=erros, n_reportadas=self.n_reportadas,
            n_adiamentos=self.n_adiamentos,
            taxa_omissao=float(erros / max(1, len(self.tarefas))),
            E_plano=self.E_plano,
            retrabalho_sobre_plano=float(self.TR / self.E_plano) if self.E_plano > 0 else 0.0,
            divida_latente_sobre_plano=(
                float(max(self.traj["S_UR"]) / self.E_plano)
                if self.traj["S_UR"] and self.E_plano > 0 else 0.0),
            retrabalho_sobre_esforco_realizado=(
                float(self.TR / total) if total > 0 else 0.0),
            trajetorias=self.traj, violacoes=self.violacoes,
        )


# =====================================================================
def carregar_instancia(arquivo: str):
    t = pd.read_csv(RAIZ / "data" / "processed" / "psplib" / "tarefas_j60_com_di.csv")
    i = pd.read_csv(RAIZ / "data" / "processed" / "psplib" / "instancias_j60.csv")
    g = t[t["arquivo"] == arquivo].copy()
    linha = i[i["arquivo"] == arquivo].iloc[0]
    disp = [int(x) for x in str(linha["disponibilidades"]).split(";")]
    return g, disp, int(linha["makespan_sem_recursos"])
