from random import uniform
from time import sleep
from threading import Lock, Thread

# Contadores de refeições para cada filósofo
contagem_refeicoes = [0] * 5

# Criação de locks para representar os hashis
hashis = [Lock() for _ in range(5)]

# Nomes dos filósofos
filosofos = [f'Filósofo {i+1}' for i in range(5)]

def comer(filosofo, hashi_esquerda, hashi_direita):
    while True:
        print(f"\n{filosofo} está pensando...")
        sleep(uniform(10, 20))
        
        # Tentativa de pegar os hashis
        comendo = False
        while not comendo:
            with hashi_esquerda:
                if hashi_direita.acquire(blocking=False):
                    comendo = True
                else:
                    # Libera o hashi se o segundo não estiver disponível
                    hashi_esquerda.release()
        
        print(f"\n{filosofo} começou a comer.")
        sleep(uniform(5, 10))
        print(f"\n{filosofo} terminou de comer.")
        
        # Atualiza o contador de refeições
        idx = filosofos.index(filosofo)
        contagem_refeicoes[idx] += 1
        print(contagem_refeicoes)
        
        # Libera os hashis após comer
        hashi_direita.release()

def iniciar_filosofos():
    threads = []
    
    for i in range(5):
        nome_filosofico = filosofos[i]
        hashi_left = hashis[i]
        hashi_right = hashis[(i + 1) % 5]
        t = Thread(target=comer, args=(nome_filosofico, hashi_left, hashi_right))
        threads.append(t)
    
    # Inicia todas as threads
    for thread in threads:
        thread.start()
    
    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    iniciar_filosofos()