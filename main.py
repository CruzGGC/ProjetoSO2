import multiprocessing
import threading
import random
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
    
    # Inicialização das cotações das ações e semáforos para sincronização
    cotacoes = multiprocessing.Array('d', [random.uniform(10, 100) for _ in range(NUM_EMPRESAS)])
    semaphores = [multiprocessing.Semaphore(1) for _ in range(NUM_EMPRESAS)]
    saldos = multiprocessing.Array('d', [SALDO_INICIAL] * NUM_CORRETORES)
    
    processos = []
    algoritmos = [algoritmo_simples, algoritmo_complexo]
    
    # Criação e início dos processos dos corretores
    for i in range(NUM_CORRETORES):
        algoritmo = random.choice(algoritmos)
        p = multiprocessing.Process(target=corretor, args=(i, cotacoes, semaphores, algoritmo, saldos, PASTA_REGISTROS, NUM_TRANSACOES))
        processos.append(p)
        p.start()
    
    # Iniciando threads para o gestor da bolsa de valores e sistema de alertas
    cotacoes_thread = threading.Thread(target=atualizar_cotacoes, args=(cotacoes, semaphores, PASTA_REGISTROS, VARIACAO_MAXIMA))
    cotacoes_thread.start()

    apresentacao_thread = threading.Thread(target=apresentar_resultados, args=(cotacoes, saldos))
    apresentacao_thread.start()

    alertas_thread = threading.Thread(target=sistema_alertas, args=(cotacoes, semaphores, saldos, PASTA_REGISTROS))
    alertas_thread.start()

    # Aguarda a conclusão dos processos dos corretores
    for p in processos:
        p.join()

    # Aguarda a conclusão das threads
    cotacoes_thread.join()
    apresentacao_thread.join()
    alertas_thread.join()
