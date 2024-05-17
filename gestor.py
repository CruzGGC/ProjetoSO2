import random
import time
import os
from datetime import datetime

def criar_pasta_registros(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

def atualizar_cotacoes(cotacoes, locks, pasta_registros, variacao_maxima):
    with open(os.path.join(pasta_registros, "Alertas.txt"), "w", encoding='utf-8') as alertas_arquivo:
        while True:
            for i in range(len(cotacoes)):
                with locks[i]:
                    variacao = random.uniform(-variacao_maxima, variacao_maxima)
                    cotacoes[i] *= (1 + variacao)
                    if abs(variacao) > variacao_maxima:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        alerta = f"{timestamp} - Negociação suspensa para a empresa {i} devido à variação de {variacao:.2f}%\n"
                        print(alerta)
                        alertas_arquivo.write(alerta)
                        alertas_arquivo.flush()
                        time.sleep(5)  # Suspende negociação por 5 segundos
            time.sleep(1)

def apresentar_resultados(cotacoes, saldos):
    while True:
        resultado = f"Estado atual das cotações: {[round(c, 2) for c in cotacoes]}\nSaldos dos corretores: {[round(s, 2) for s in saldos]}\n"
        print(resultado)
        time.sleep(5)

def sistema_alertas(cotacoes, locks, saldos, pasta_registros):
    with open(os.path.join(pasta_registros, "Alertas.txt"), "a", encoding='utf-8') as alertas_arquivo:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for i in range(len(cotacoes)):
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
