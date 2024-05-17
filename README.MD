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

Esse código é uma implementação básica que pode ser expandida com funcionalidades adicionais conforme necessário, como diferentes algoritmos de negociação, threads para o servidor, e modelos de apresentação de resultados.