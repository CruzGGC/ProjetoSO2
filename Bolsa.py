import multiprocessing
import random
import time
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

def corretor(id_corretor, cotacoes, locks):
    for _ in range(NUM_TRANSACOES):
        empresa = random.randint(0, NUM_EMPRESAS - 1)
        quantidade = random.randint(1, 10)
        tipo_operacao = random.choice(['compra', 'venda'])
        preco = random.uniform(0.9, 1.1) * cotacoes[empresa]
        
        with locks[empresa]:
            if tipo_operacao == 'compra':
                cotacoes[empresa] += 0.01 * quantidade
            else:
                cotacoes[empresa] -= 0.01 * quantidade
            
            registro = f"{tipo_operacao} {quantidade} acoes da empresa {empresa} a {preco:.2f}\n"
            registros[id_corretor].write(registro)
            registros[id_corretor].flush()
        
        time.sleep(random.uniform(0.01, 0.1))

def servidor(cotacoes, locks):
    while True:
        for i in range(NUM_EMPRESAS):
            with locks[i]:
                variacao = random.uniform(-VARIACAO_MAXIMA, VARIACAO_MAXIMA)
                cotacoes[i] *= (1 + variacao)
                if variacao > VARIACAO_MAXIMA or variacao < -VARIACAO_MAXIMA:
                    print(f"Negociacao suspensa para a empresa {i} devido a variacao de {variacao:.2f}%")
                    time.sleep(5)  # Suspende negociação por 5 segundos
        
        print("Cotacoes atualizadas:", [round(c, 2) for c in cotacoes])
        time.sleep(1)

if __name__ == '__main__':
    processos = []
    for i in range(NUM_CORRETORES):
        p = multiprocessing.Process(target=corretor, args=(i, cotacoes, locks))
        processos.append(p)
        p.start()
    
    servidor_proc = multiprocessing.Process(target=servidor, args=(cotacoes, locks))
    processos.append(servidor_proc)
    servidor_proc.start()
    
    for p in processos:
        p.join()
    
    for registro in registros:
        registro.close()
