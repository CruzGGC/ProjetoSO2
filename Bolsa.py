import multiprocessing
import random
import time
import threading
from multiprocessing import Value, Array, Lock
import os

# Constantes
NUM_EMPRESAS = 20
NUM_CORRETORES = 10
VARIACAO_MAXIMA = 0.25
NUM_TRANSACOES = 100

# Inicialização das cotações das ações e locks para sincronização
cotacoes = Array('d', [random.uniform(10, 100) for _ in range(NUM_EMPRESAS)])
locks = [Lock() for _ in range(NUM_EMPRESAS)]
registros = [open(f"registro_corretor_{i}.txt", "w") for i in range(NUM_CORRETORES)]

def algoritmo_simples(quantidade):
    return quantidade * 0.01

def algoritmo_complexo(quantidade):
    return quantidade * 0.02

def corretor(id_corretor, cotacoes, locks, algoritmo):
    """
    Executes transactions for a stock broker.

    Args:
        id_corretor (int): The ID of the stock broker.
        cotacoes (list): A list of stock prices for different companies.
        locks (list): A list of locks for each company's stock.
        algoritmo (function): The algorithm used to calculate the variation in stock prices.

    Returns:
        None
    """
    for _ in range(NUM_TRANSACOES):
        empresa = random.randint(0, NUM_EMPRESAS - 1)
        quantidade = random.randint(1, 10)
        tipo_operacao = random.choice(['compra', 'venda'])
        preco = random.uniform(0.9, 1.1) * cotacoes[empresa]
        
        with locks[empresa]:
            variacao = algoritmo(quantidade)
            if tipo_operacao == 'compra':
                cotacoes[empresa] += variacao
            else:
                cotacoes[empresa] -= variacao
            
            registro = f"{tipo_operacao} {quantidade} ações da empresa {empresa} a {preco:.2f}\n"
            registros[id_corretor].write(registro)
            registros[id_corretor].flush()
        
        time.sleep(random.uniform(0.01, 0.1))

def atualizar_cotacoes(cotacoes, locks):
    while True:
        for i in range(NUM_EMPRESAS):
            with locks[i]:
                variacao = random.uniform(-VARIACAO_MAXIMA, VARIACAO_MAXIMA)
                cotacoes[i] *= (1 + variacao)
                if variacao > VARIACAO_MAXIMA or variacao < -VARIACAO_MAXIMA:
                    print(f"Negociação suspensa para a empresa {i} devido à variação de {variacao:.2f}%")
                    time.sleep(5)  # Suspende negociação por 5 segundos
        
        print("Cotacoes atualizadas:", [round(c, 2) for c in cotacoes])
        time.sleep(1)

def apresentar_resultados(cotacoes):
    while True:
        print("Estado atual das cotações:", [round(c, 2) for c in cotacoes])
        time.sleep(5)

if __name__ == '__main__':
    processos = []

    algoritmos = [algoritmo_simples, algoritmo_complexo]
    for i in range(NUM_CORRETORES):
        algoritmo = random.choice(algoritmos)
        p = multiprocessing.Process(target=corretor, args=(i, cotacoes, locks, algoritmo))
        processos.append(p)
        p.start()
    
    # Iniciando threads para o gestor da bolsa de valores
    cotacoes_thread = threading.Thread(target=atualizar_cotacoes, args=(cotacoes, locks))
    cotacoes_thread.start()

    apresentacao_thread = threading.Thread(target=apresentar_resultados, args=(cotacoes,))
    apresentacao_thread.start()

    for p in processos:
        p.join()
    
    cotacoes_thread.join()
    apresentacao_thread.join()
    
    for registro in registros:
        registro.close()
