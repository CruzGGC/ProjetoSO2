# Explicação do Código

## Importação de Módulos:

Importamos módulos necessários como multiprocessing, random, time, e os.

## Definição de Constantes:

Definimos constantes que serão usadas ao longo do código, como o número de empresas, corretores, variação máxima permitida e número de transações.

## Inicialização de Cotações e Locks:

Inicializamos as cotações das ações com valores aleatórios e criamos locks para sincronização ao acessar as cotações.

## Função corretor:

Cada corretor executa transações de compra ou venda de ações de forma aleatória. Eles atualizam as cotações das ações e registram as transações em arquivos individuais.

## Função servidor:

O servidor atualiza periodicamente as cotações das ações. Se a variação exceder o limite permitido, ele suspende a negociação dessa ação por um tempo.

## Execução Principal:

Criamos processos para cada corretor e um processo para o servidor. Em seguida, iniciamos e aguardamos a conclusão de todos os processos. Finalmente, fechamos os arquivos de registro.

# Melhorias nas Funcionalidades

## Algoritmo de negociação de ações:

Adicionamos duas funções de algoritmo (algoritmo_simples e algoritmo_complexo) que modificam a quantidade de variação nas cotações. Corretores podem usar um desses algoritmos aleatoriamente.

## Diferentes algoritmos de negociação de ações para diferentes corretores:

Corretores agora escolhem aleatoriamente entre os algoritmos disponíveis, permitindo que diferentes corretores usem diferentes estratégias.

## Gestor da bolsa de valores com vários threads:

Usamos threads para o gestor da bolsa de valores (atualizar_cotacoes) e para a apresentação dos resultados (apresentar_resultados), permitindo multitarefas dentro do servidor.

## Modelo de apresentação dos resultados da simulação:

A função apresentar_resultados imprime periodicamente o estado atual das cotações, oferecendo uma visão contínua das cotações ao longo do tempo.
