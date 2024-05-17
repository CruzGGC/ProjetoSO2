import multiprocessing
import threading
import os
import random
import time
from datetime import datetime

# Constantes
NUM_EMPRESAS = 20
NUM_CORRETORES = 10
VARIACAO_MAXIMA = 0.25
NUM_TRANSACOES = 100
SALDO_INICIAL = 100000
PASTA_REGISTROS = 'Registros'

# Função para garantir a existência do diretório
def criar_pasta_registros(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Inicialização das cotações das ações e locks para sincronização
cotacoes = multiprocessing.Array('d', [random.uniform(10, 100) for _ in range(NUM_EMPRESAS)])
locks = [multiprocessing.Lock() for _ in range(NUM_EMPRESAS)]
saldos = multiprocessing.Array('d', [SALDO_INICIAL] * NUM_CORRETORES)

# Funções dos algoritmos de negociação
def algoritmo_simples(quantidade):
    return quantidade * 0.01

def algoritmo_complexo(quantidade):
    return quantidade * 0.02

# Função do corretor
def corretor(id_corretor, cotacoes, locks, algoritmo, saldos):
    with open(os.path.join(PASTA_REGISTROS, f"registro_corretor_{id_corretor}.txt"), "w", encoding='utf-8') as registro_arquivo:
        for _ in range(NUM_TRANSACOES):
            empresa = random.randint(0, NUM_EMPRESAS - 1)
            quantidade = random.randint(1, 10)
            tipo_operacao = random.choice(['compra', 'venda'])
            preco = cotacoes[empresa] * random.uniform(0.9, 1.1)
            
            with locks[empresa]:
                variacao = algoritmo(quantidade)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if tipo_operacao == 'compra':
                    cotacoes[empresa] += variacao
                    custo = quantidade * preco
                    saldos[id_corretor] -= custo
                    registro = f"{timestamp} - Compra de {quantidade} ações da empresa {empresa} a {preco:.2f} cada. Custo: {custo:.2f}. Saldo: {saldos[id_corretor]:.2f}\n"
                else:
                    cotacoes[empresa] -= variacao
                    ganho = quantidade * preco
                    saldos[id_corretor] += ganho
                    registro = f"{timestamp} - Venda de {quantidade} ações da empresa {empresa} a {preco:.2f} cada. Ganho: {ganho:.2f}. Saldo: {saldos[id_corretor]:.2f}\n"
                
                registro_arquivo.write(registro)
                registro_arquivo.flush()
            
            time.sleep(random.uniform(0.01, 0.1))

# Função para atualizar as cotações
def atualizar_cotacoes(cotacoes, locks):
    with open(os.path.join(PASTA_REGISTROS, "Alertas.txt"), "w", encoding='utf-8') as alertas_arquivo:
        while True:
            for i in range(NUM_EMPRESAS):
                with locks[i]:
                    variacao = random.uniform(-VARIACAO_MAXIMA, VARIACAO_MAXIMA)
                    cotacoes[i] *= (1 + variacao)
                    if variacao > VARIACAO_MAXIMA or variacao < -VARIACAO_MAXIMA:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        alerta = f"{timestamp} - Negociação suspensa para a empresa {i} devido à variação de {variacao:.2f}%\n"
                        print(alerta)
                        alertas_arquivo.write(alerta)
                        alertas_arquivo.flush()
                        time.sleep(5)  # Suspende negociação por 5 segundos
            time.sleep(1)

# Função para apresentar os resultados
def apresentar_resultados(cotacoes, saldos):
    while True:
        resultado = f"Estado atual das cotações: {[round(c, 2) for c in cotacoes]}\nSaldos dos corretores: {[round(s, 2) for s in saldos]}\n"
        print(resultado)
        time.sleep(5)

# Função para o sistema de alertas
def sistema_alertas(cotacoes, locks):
    with open(os.path.join(PASTA_REGISTROS, "Alertas.txt"), "a", encoding='utf-8') as alertas_arquivo:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for i in range(NUM_EMPRESAS):
                with locks[i]:
                    if cotacoes[i] < 10:
                        alerta = f"{timestamp} - ALERTA: A cotação da empresa {i} está extremamente baixa: {cotacoes[i]:.2f}\n"
                        print(alerta)
                        alertas_arquivo.write(alerta)
                        alertas_arquivo.flush()
                    elif cotacoes[i] > 150:
                        alerta = f"{timestamp} - ALERTA: A cotação da empresa {i} está extremamente alta: {cotacoes[i]:.2f}\n"
                        print(alerta)
                        alertas_arquivo.write(alerta)
                        alertas_arquivo.flush()
            
            saldos_atualizados = [round(s, 2) for s in saldos]
            alerta_saldos = f"{timestamp} - Saldos dos corretores: {saldos_atualizados}\n"
            alertas_arquivo.write(alerta_saldos)
            alertas_arquivo.flush()
            
            time.sleep(2)

if __name__ == '__main__':
    criar_pasta_registros(PASTA_REGISTROS)
    
    processos = []
    algoritmos = [algoritmo_simples, algoritmo_complexo]
    
    for i in range(NUM_CORRETORES):
        algoritmo = random.choice(algoritmos)
        p = multiprocessing.Process(target=corretor, args=(i, cotacoes, locks, algoritmo, saldos))
        processos.append(p)
        p.start()
    
    # Iniciando threads para o gestor da bolsa de valores e alertas
    cotacoes_thread = threading.Thread(target=atualizar_cotacoes, args=(cotacoes, locks))
    cotacoes_thread.start()

    apresentacao_thread = threading.Thread(target=apresentar_resultados, args=(cotacoes, saldos))
    apresentacao_thread.start()

    alertas_thread = threading.Thread(target=sistema_alertas, args=(cotacoes, locks))
    alertas_thread.start()

    for p in processos:
        p.join()
    
    cotacoes_thread.join()
    apresentacao_thread.join()
    alertas_thread.join()
