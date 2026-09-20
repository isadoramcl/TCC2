LOTE NOTURNO — 19 para 20/09. Trabalho sem supervisao.

POLITICA DE FALHA PARA TRABALHO NOTURNO (substitui, so para esta noite, a regra
de parada total da ordem 37):
- Se um controle publicado falhar, PARE AQUELE ITEM, registre o observado x o
  esperado, e SIGA para o proximo item independente. Nao pare o lote inteiro.
- O lote continua NAO FECHADO enquanto houver controle publicado reprovado.
  Fechar o lote continua sendo decisao do dia seguinte, com revisao.
- Identidade bit a bit com opcoes neutras e porta de cada item, como sempre. Se
  quebrar, reverta AQUELE item e siga.
- Commit e push depois de CADA item concluido. Nao acumule a noite inteira num
  unico commit; se a maquina cair, o que ja rodou tem de sobreviver.
- Nao conclua nada que dependa de algo que voce nao conseguiu verificar. Marque
  como pendente e diga por que.

ORDEM DA NOITE

1. T-B2.3 — PRIMEIRO, protege o resultado central
   Varra tau_inicial na centralizada, tudo o mais identico, e reporte a partir
   de que valor as execucoes incompletas desaparecem. Reporte junto a trajetoria
   de hiato_colega_capaz_sem_confianca e de N_req.
   Esperado: se as incompletas sumirem ao abrir o portao, as 36 sao desfecho do
   portao degenerado (A-13), nao limitacao da familia de modelos, e o B2 muda de
   leitura. Se persistirem, e travamento estrutural.
   PROIBIDO escolher um tau_inicial conveniente. O resultado e a varredura.

2. D2 — LANCE EM SEGUNDO PLANO agora, e siga para o item 3 enquanto roda
   Cobertura repetida do History Matching, B=500 (1000 se couber).
   Cada replica: z_b novo no vetor verdadeiro pelo desenho declarado; reestimar
   a resposta do verdadeiro com sementes independentes; os quatro I_j e I_max,b;
   registrar I_max,b > 3.
   Saida: taxa empirica de falsa exclusao com IC binomial, e percentil 95 de
   I_max sob o vetor verdadeiro.
   Se a taxa passar de ~30%: NAO trate como resultado. Pode haver erro de
   desenho. Reporte e nao use o HM.
   PROIBIDO ajustar V_mod ate o gabarito passar, ou escolher pseudo-observacao
   favoravel.

3. D1 — readout de retrabalho
   retrabalho_sobre_esforco_total = TR / (E_plano + TR), campo derivado, sem
   alterar RNG, decisoes ou estados.
   Controle ANTES/DEPOIS em todos os campos preexistentes.
   Esperado: campos anteriores inalterados, residuo maximo da ordem de 1e-14,
   e o campo novo ~0,190 na adaptativa e ~0,224 na centralizada, no nominal.
   Se algum campo preexistente mudar, houve efeito colateral — refaca.

4. D3 — declarar o estimando do V_obs sintetico
   Escreva o estimando explicitamente e faca geracao e estimacao respeitarem a
   mesma unidade amostral. Renomeie o gemeo identico para "verificacao interna
   do procedimento" — ele nao informa o V_obs externo e o texto nao pode
   sugerir que informa.

5. C1 — ancorar F_ancora em Stewart & Melchers (1988)
   F_ancora = k * 0,0128, com k derivado do nivel de dificuldade por decomposicao
   DECLARADA SINTETICA e varrida.
   Controle exato: k = 1,2,3,4,5,8 deve devolver 0,0128 / 0,0256 / 0,0384 /
   0,0512 / 0,0640 / 0,1024, por float.hex() ou tolerancia 1e-12.
   Mapa reverso publicado: k implicito de cada valor varrido de F_ancora.
   Esperado: os seis pontos exatos, e k ~ 3,9 para 0,05 e k ~ 7,8 para 0,10.
   Rotulo obrigatorio: F_ancora de 0,15 a 0,25 exige k acima de 8, o maior
   publicado. Entram como CENARIO DE SENSIBILIDADE, nunca como valor ancorado.
   A decomposicao sintetica deve preferencialmente cair em k <= 8.

6. C2 — heterogeneidade entre agentes, CV = 1,13
   Alternativa heterogeneidade_erro: 'nenhuma' (default, preserva bits) e
   'beta_cv113'. Cada agente recebe taxa basal de uma Beta com media F_base e
   CV 1,13:  sigma = 1,13*mu ; t = mu(1-mu)/sigma^2 - 1 ; alpha = mu*t ;
   beta = (1-mu)*t
   Controle positivo decisivo: para mu = 0,0163 a formula deve devolver
   alpha ~ 0,7546 e beta ~ 45,46. Ja validado no C3 — confirme que bate aqui.
   ARMADILHA: a Beta com CV = 1,13 so existe para mu <= 0,4392. Com F_ancora
   alto e o multiplicador da camada NASA, F_base PODE ultrapassar. O codigo tem
   de FALHAR COM MENSAGEM EXPLICITA, nunca reduzir o CV em silencio. Registre em
   quais celulas isso ocorre.
   Verifique media e CV empiricos da amostra de agentes.

7. A1 — rota de fuga da Porta 1 (defeito A-14)
   Hoje p1_fuga = 0 sempre, porque omega = 0,50 > limite = 0,60 e falso por
   construcao: dois lados sao constantes lidas uma vez.
   Alternativa regra_fuga: 'constante' (atual, default, preserva bits) e
   'dependente_estado', com omega*q > limite, q = max(0, 2*p_heu - 1),
   declarada como [DEC].
   Inclua limite_aversao_perda no desenho de robustez, ou declare por que ficou
   fora. Varra limite em pelo menos [0,10; 0,20; 0,30; 0,40].
   Esperado: sob dependente_estado, p1_fuga > 0 em alguma configuracao E
   variacao continua com limite, nao degrau.
   Se p1_fuga continuar 0 em toda a varredura, a condicao ainda e degenerada —
   refaca a formulacao. Se for funcao degrau, REPORTE COMO TAL: significa que a
   fuga continua sendo interruptor, e isso muda o que a monografia pode dizer.
   Registre a conexao com o T-B2.3: sao os dois portoes degenerados por
   comparacao de constantes.

8. E2 — saturacao da confianca
   Exporte a trajetoria e reporte o periodo em que a media cruza 0,95.
   Contexto: 0,9364 no adaptativo (de 0,80) e 0,2500 congelada no centralizado;
   102,9 sucessos contra 39,1 insucessos por execucao, catraca de mao unica.
   Objetivo: poder declarar com numero que a confianca e, na pratica, condicao
   inicial e nao variavel de estado com dinamica propria.

9. C4 — faixa de sensibilidade de p_heu (ANALISE, nada no modelo)
   Varra tau_sat e s_transicao e reporte a razao entre a fracao via Porta 1 no
   extremo superior e no inferior da faixa de P do modelo.
   Compare com a razao de 2,3x de Rieskamp DECLARANDO o descasamento de unidade:
   Rieskamp conta participante classificado, o modelo conta execucao de tarefa.
   PROIBIDO ajustar tau_sat ou s_transicao para bater em 19,4% -> 44,4%.
   Registre que o Estudo 1 do mesmo artigo nao achou o efeito (chi2 = 0,10,
   p = 0,75) e que o P do modelo nunca desce abaixo de 0,30.

10. E3 — faixa de mu_minimo contra Reichelt & Lyneis (1999), Tabelas 1-2
    Distribuicao observada de mu_cog e mu_rede no nominal, e compatibilidade com
    medias da ordem de 0,95 (pressao) e 0,97 (fadiga).
    Ressalva obrigatoria no texto: sao saidas de modelo de Dinamica de Sistemas
    da mesma linhagem deste trabalho — consistencia com a literatura de
    modelagem, nao medicao independente.

11. E1 — gradiente sobre linhas de codigo
    So se os dados NASA estiverem acessiveis offline. Se exigirem rede que voce
    nao tem, PULE e registre como pendente — nao improvise fonte.
    Recalcule e republique. NAO e conferencia: os numeros mudam. Declare qual
    versao dos dados foi usada (Shepperd et al. publicam versoes limpas).

12. F — arrumacao
    Resolva os dois arquivos numerados 07. Corrija a rotulagem de
    taxa_reversao_pct (e proporcao de commits QUE FORAM revertidos, nao que SAO
    reversoes; publique o tamanho de base) e o descasamento de denominador da
    tabela de tenis (dupla falta por ponto no CSV, por 2o saque no relatorio).

AO TERMINAR
Um relatorio unico com: o que rodou, o que passou, o que reprovou com observado
x esperado, e o que ficou pendente e por que. Nao declare o lote fechado — isso
e decisao do dia seguinte.