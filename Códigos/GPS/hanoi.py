def torre_de_hanoi(n, origem, destino, auxiliar):
    """
    Resolve o problema da Torre de Hanói de forma recursiva.

    Parâmetros:
    n (int): O número de discos a serem movidos.
    origem (str): O nome da estaca de origem.
    destino (str): O nome da estaca de destino.
    auxiliar (str): O nome da estaca auxiliar.
    """
    # Caso Base: Se houver apenas um disco, mova-o diretamente para o destino.
    # Este é o ponto onde a recursão para.
    if n == 1:
        print(f"Mover disco 1 da estaca {origem} para a estaca {destino}")
        return

    # Passo 1: Mover a torre de n-1 discos da origem para a estaca auxiliar,
    # usando a estaca de destino como o pino temporário.
    torre_de_hanoi(n - 1, origem, auxiliar, destino)

    # Passo 2: Mover o disco maior (o n-ésimo disco) que restou na origem
    # para a estaca de destino final.
    print(f"Mover disco {n} da estaca {origem} para a estaca {destino}")

    # Passo 3: Mover a torre de n-1 discos que está na estaca auxiliar
    # para a estaca de destino final, usando a estaca de origem como
    # o pino temporário.
    torre_de_hanoi(n - 1, auxiliar, destino, origem)


# --- Seção para executar o código ---
if __name__ == "__main__":
    # Defina o número de discos para o desafio
    numero_de_discos = 3

    # Define os nomes das estacas
    estaca_origem = 'A'
    estaca_destino = 'C'
    estaca_auxiliar = 'B'

    print(f"Iniciando a solução da Torre de Hanói para {numero_de_discos} discos:")
    print("-" * 30)

    # Faz a chamada inicial da função recursiva
    torre_de_hanoi(numero_de_discos, estaca_origem, estaca_destino, estaca_auxiliar)

    print("-" * 30)
    print("Solução concluída!")
