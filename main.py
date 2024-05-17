import multiprocessing
import random
import threading
from corretor import corretor, algoritmo_simples, algoritmo_complexo
from gestor import criar_pasta_registros, atualizar_cotacoes, apresentar_resultados, sistema_alertas

# Constantes
NUM_EMPRESAS = 20
NUM_CORRETORES = 10
VARIACAO_MAXIMA = 0.25
NUM_TRANSACOES = 100
SALDO_INICIAL = 100000
PASTA_REGISTROS = 'Registros'

if __name__ == '__main__':
    criar_pasta_registros(PASTA_REGISTROS)
    
    # Inicialização das cotações das ações e locks para sincronização
    cotacoes = multiprocessing.Array('d', [random.uniform(10, 100) for _ in range(NUM_EMPRESAS)])
    locks = [multiprocessing.Lock() for _ in range(NUM_EMPRESAS)]
    saldos = multiprocessing.Array('d', [SALDO_INICIAL] * NUM_CORRETORES)
    
    processos = []
    algoritmos = [algoritmo_simples, algoritmo_complexo]
    
    for i in range(NUM_CORRETORES):
        algoritmo = random.choice(algoritmos)
        p = multiprocessing.Process(target=corretor, args=(i, cotacoes, locks, algoritmo, saldos, PASTA_REGISTROS, NUM_TRANSACOES))
        processos.append(p)
        p.start()
    
    # Iniciando threads para o gestor da bolsa de valores e alertas
    cotacoes_thread = threading.Thread(target=atualizar_cotacoes, args=(cotacoes, locks, PASTA_REGISTROS, VARIACAO_MAXIMA))
    cotacoes_thread.start()

    apresentacao_thread = threading.Thread(target=apresentar_resultados, args=(cotacoes, saldos))
    apresentacao_thread.start()

    alertas_thread = threading.Thread(target=sistema_alertas, args=(cotacoes, locks, saldos, PASTA_REGISTROS))
    alertas_thread.start()

    for p in processos:
        p.join()
    
    cotacoes_thread.join()
    apresentacao_thread.join()
    alertas_thread.join()
