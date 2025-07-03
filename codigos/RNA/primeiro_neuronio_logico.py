def mcculloch_pitts_neuron(inputs, weights, threshold):
    """
    Simula um único neurônio de McCulloch-Pitts.

    Argumentos:
    inputs (list): Lista de entradas binárias (0 ou 1).
    weights (list): Lista de pesos correspondentes a cada entrada.
    threshold (int): O limiar de ativação.

    Retorna:
    int: A saída do neurônio (0 ou 1).
    """
    # Garante que o número de entradas e pesos seja o mesmo
    if len(inputs) != len(weights):
        raise ValueError("O número de entradas deve ser igual ao número de pesos.")

    # Calcula a soma ponderada das entradas
    soma_ponderada = sum(i * w for i, w in zip(inputs, weights))

    # Aplica a função de ativação (degrau)
    if soma_ponderada >= threshold:
        return 1
    else:
        return 0

# --- Seção para executar e testar as Portas Lógicas ---
if __name__ == "__main__":

    # --- 1. Porta AND ---
    # Dispara apenas se ambas as entradas forem 1.
    # Soma Ponderada: (x1*1 + x2*1). Precisa ser >= 2.
    print("--- Porta Lógica AND ---")
    pesos_and = [1, 1]
    limiar_and = 2
    for entradas in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        saida = mcculloch_pitts_neuron(entradas, pesos_and, limiar_and)
        print(f"Entradas: {entradas}, Saída: {saida}")
    print("-" * 25)

    # --- 2. Porta OR ---
    # Dispara se pelo menos uma entrada for 1.
    # Soma Ponderada: (x1*1 + x2*1). Precisa ser >= 1.
    print("--- Porta Lógica OR ---")
    pesos_or = [1, 1]
    limiar_or = 1
    for entradas in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        saida = mcculloch_pitts_neuron(entradas, pesos_or, limiar_or)
        print(f"Entradas: {entradas}, Saída: {saida}")
    print("-" * 25)

    # --- 3. Porta NOT ---
    # Inverte a entrada. Usa um peso inibitório (negativo).
    # Soma Ponderada: (x1*-1). Precisa ser >= 0 para disparar (quando x1=0).
    print("--- Porta Lógica NOT ---")
    pesos_not = [-1]
    limiar_not = 0
    for entrada in [(0,), (1,)]: # A vírgula cria uma tupla de um elemento
        saida = mcculloch_pitts_neuron(entrada, pesos_not, limiar_not)
        print(f"Entrada: {entrada[0]}, Saída: {saida}")
    print("-" * 25)

    # --- 4. Porta NAND ---
    # O oposto de AND. Usa pesos inibitórios.
    # Soma Ponderada: (x1*-1 + x2*-1). Só não dispara quando a soma é -2.
    # Portanto, o limiar deve ser > -2. Ex: -1.
    print("--- Porta Lógica NAND ---")
    pesos_nand = [-1, -1]
    limiar_nand = -1
    for entradas in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        saida = mcculloch_pitts_neuron(entradas, pesos_nand, limiar_nand)
        print(f"Entradas: {entradas}, Saída: {saida}")
    print("-" * 25)

    # --- 5. O Desafio da Porta XOR ---
    # A porta XOR (OU Exclusivo) é famosa por ser "não-linearmente separável".
    # Isso significa que é IMPOSSÍVEL para um ÚNICO neurônio M-P resolver o XOR.
    # A solução é usar uma rede de neurônios.
    #
    # Lógica: XOR(x1, x2) = AND( OR(x1, x2), NAND(x1, x2) )
    print("--- Rede para a Porta Lógica XOR ---")

    def rede_xor(entradas):
        # Primeiro nível da rede
        saida_or = mcculloch_pitts_neuron(entradas, pesos_or, limiar_or)
        saida_nand = mcculloch_pitts_neuron(entradas, pesos_nand, limiar_nand)

        # Segundo nível da rede: um neurônio AND que recebe a saída dos anteriores
        entradas_finais = [saida_or, saida_nand]
        saida_final = mcculloch_pitts_neuron(entradas_finais, pesos_and, limiar_and)

        return saida_final

    for entradas in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        saida = rede_xor(entradas)
        print(f"Entradas: {entradas}, Saída: {saida}")
    print("-" * 25)
