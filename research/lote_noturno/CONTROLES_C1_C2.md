# Controles prévios a C1/C2 — sequência posterior a A1

C1: seis pares k,p da ordem 37; tolerância absoluta 1e-12; nenhum ajuste.
C2: avaliar literalmente mu=0,0163 e CV=1,13 contra alpha=0,7546,
beta=45,4563. A ordem 37 requer reprodução na terceira casa; o lote noturno usa
aproximação mas não fixa uma nova tolerância. Publicar diferenças e testar a
regra estrita original, sem alargá-la até passar. Se falhar, não introduzir a
Beta no simulador nem varrer resultados dinâmicos de C2; item reprovado/pendente
de reconciliação metodológica. A-16 de C3 não autoriza trocar momentos aqui.

Fórmulas e domínio são verificáveis sem modificar o modelo. Domínio da Beta
não degenerada: 0<mu<1/(1+CV²), estrito no extremo. Não ajustar CV para caber.
