# Multiprocessamento em Python

Este projeto simula um mercado de ações com múltiplos corretores realizando transações. Aqui está uma visão geral dos principais componentes:

## Corretor.py

Este arquivo contém a função corretor, que simula as ações de um corretor de ações. Cada corretor executa transações de compra ou venda de ações de forma aleatória, atualiza as cotações das ações e registra as transações em arquivos individuais.

## Gestor.py

Este ficheiro contém funções para gerenciar a bolsa de valores, incluindo a atualização das cotações das ações e a apresentação dos resultados.

## Main.py

Este é o ponto de entrada do programa. Ele inicializa a simulação do mercado de ações, cria uma pasta para armazenar registros de transações, inicializa preços de ações e bloqueios para sincronização, e inicia processos para corretores, bem como threads para o gerenciador do mercado de ações e sistema de alerta.

# Explicação do Programa

O programa usa o módulo multiprocessing para criar processos separados para cada corretor e o módulo threading para criar threads para o gerenciador do mercado de ações e o sistema de alerta. Isso permite que várias tarefas sejam executadas simultaneamente, simulando um ambiente de mercado de ações em tempo real.

Os corretores realizam transações com base em algoritmos de negociação de ações, que podem ser simples ou complexos. Eles escolhem aleatoriamente entre os algoritmos disponíveis, permitindo que diferentes corretores usem diferentes estratégias.

As cotações das ações são atualizadas periodicamente pelo gerenciador do mercado de ações. Se a variação exceder o limite permitido, a negociação dessa ação é suspensa por um tempo. Os resultados da simulação são apresentados periodicamente, oferecendo uma visão contínua das cotações ao longo do tempo.