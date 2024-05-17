import random
import time
from datetime import datetime
import os

# Funções dos algoritmos de negociação
def algoritmo_simples(quantidade):
    return quantidade * 0.01

def algoritmo_complexo(quantidade):
    return quantidade * 0.02

# Função do corretor
def corretor(id_corretor, cotacoes, locks, algoritmo, saldos, pasta_registros, num_transacoes):
    with open(os.path.join(pasta_registros, f"registro_corretor_{id_corretor}.txt"), "w", encoding='utf-8') as registro_arquivo:
        for _ in range(num_transacoes):
            empresa = random.randint(0, len(cotacoes) - 1)
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
