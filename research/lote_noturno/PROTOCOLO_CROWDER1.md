# T-CROWDER.1 — protocolo prévio, sem alvo externo

Dois parâmetros em aprendizado: incremento_base=15, fator_transferencia=3,
condição tcc1 ([TCC1]). Substituem os literais nos caminhos legado e Crowder,
sem corrigir a escala legada ou alterar a ordem aritmética. O teto de 0,30
em Crowder permanece; ganho/5 e teto da subtarefa permanecem. Ambos os braços
recebem os mesmos escalares em cada célula. Default e nominal inalterados.

Produto cartesiano: incremento_base [7,5;15;22,5] × fator_transferencia
[1,5;3;6]. A lista explícita prevalece: 22,5 é 1,5×15, não o dobro.
Sensibilidade sem alvo externo, sem ranking ou eleição. 16 instâncias
ordenadas [::30][:16], 12 sementes 0..11, ambos os braços: 384 por célula,
3.456 execuções. Mesmo conjunto do nominal congelado. Reutilização de sementes
não significa alinhamento evento a evento após trajetórias divergirem.

Porta antes da grade: identidade bit a bit em (15,3) contra dfc0d78 para
resultados completos, agentes, tarefas, eventos e RNG; caminhos MVP nominal,
MVP com comunicação legada e Simulacao legado. Teste local das duas alterações
numéricas e teto. Suíte de compatibilidade neutra permanece obrigatória.

Cinco indicadores, adaptativa−centralizada e leitura absoluta por braço:
atraso_relativo=makespan/CPM, taxa_omissao, divida_latente_sobre_plano,
taxa_falha_efetiva, fracao_porta1=omissões/(omissões+inícios analíticos).
IC95 t sobre 16 médias por instância de diferenças pareadas por semente.
Contrastes entre alternativas e (15,3) também pareados; sem correção múltipla.
Censura acompanha os valores finais e os pares completos são reportados
separadamente. Enfatizar dívida; seu pico continua estatística de extremo.

N_req, N_success, TL e ganhos dC realizados instrumentados sem sorteios extras.
Verificar centralizada inerte em toda a grade, não apenas assumir N_req=0.
Não inferir causalidade dos casos T-GOV.2: esta grade roda os cenários nominais,
não as regiões invertidas. Não alterar V_mod ou nominal.
