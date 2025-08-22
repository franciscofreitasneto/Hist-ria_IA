# -*- coding: utf-8 -*-

class Frame:
    """
    Representa um Frame de Minsky, uma estrutura de dados para uma
    situação estereotipada.
    """
    def __init__(self, nome):
        """
        Inicializa o frame com um nome e um dicionário vazio para os slots.
        """
        self.nome = nome
        self.slots = {}

    def adicionar_slot(self, nome_slot, prompt, default=None, tipo=None):
        """
        Adiciona um novo slot ao frame.

        Args:
            nome_slot (str): O nome do slot (e.g., 'destino').
            prompt (str): A pergunta a ser feita se o slot estiver vazio.
            default (any, optional): O valor padrão a ser assumido.
            tipo (str, optional): O tipo de frame esperado para este slot (e.g., 'cidade').
        """
        self.slots[nome_slot] = {
            'valor': default,
            'prompt': prompt,
            'tipo': tipo
        }

    def obter_valor(self, nome_slot):
        """Retorna o valor de um slot."""
        return self.slots.get(nome_slot, {}).get('valor')

    def definir_valor(self, nome_slot, valor):
        """Define o valor de um slot."""
        if nome_slot in self.slots:
            self.slots[nome_slot]['valor'] = valor
            return True
        return False

    def slots_por_preencher(self):
        """Retorna uma lista dos nomes dos slots que ainda não têm valor."""
        return [nome for nome, detalhes in self.slots.items() if detalhes['valor'] is None]

    def __str__(self):
        """Representação textual do estado atual do frame."""
        info = f"--- Frame: {self.nome} ---\n"
        for nome, detalhes in self.slots.items():
            valor = detalhes['valor']
            # Se o valor for outro frame, mostra o nome dele.
            if isinstance(valor, Frame):
                valor_str = f"{valor.nome} (País: {valor.obter_valor('pais')}, Aeroporto: {valor.obter_valor('aeroporto')})"
            elif valor is None:
                valor_str = "Vazio"
            else:
                valor_str = str(valor)
            info += f"- {nome.capitalize()}: {valor_str}\n"
        return info

class SistemaDeFrames:
    """
    Gerencia a interação com o utilizador, usando um frame para guiar o diálogo.
    """
    def __init__(self, frame_principal, base_de_conhecimento):
        self.frame = frame_principal
        self.base_de_conhecimento = base_de_conhecimento

    def analisar_entrada_simples(self, texto):
        """
        Um analisador de linguagem natural muito simples, baseado em palavras-chave.
        """
        palavras = texto.lower().split()
        alteracoes = {}
        try:
            # Procura por um nome próprio (simplesmente uma palavra capitalizada)
            for palavra in texto.split():
                if palavra.istitle():
                    alteracoes['viajante'] = palavra
                    break

            if 'de' in palavras:
                idx = palavras.index('de')
                if idx + 1 < len(palavras):
                    alteracoes['origem'] = palavras[idx + 1]
            if 'para' in palavras:
                idx = palavras.index('para')
                if idx + 1 < len(palavras):
                    alteracoes['destino'] = palavras[idx + 1]
            if 'data' in palavras:
                idx = palavras.index('data')
                if idx + 1 < len(palavras):
                    alteracoes['data_partida'] = palavras[idx + 1]
        except ValueError:
            pass
        return alteracoes

    def iniciar_dialogo(self):
        """
        Inicia e mantém o loop de conversação para preencher o frame.
        """
        print(f"Olá! Eu sou um assistente de viagens. Como posso ajudar?")
        print("Pode dizer algo como 'Francisco quer ir de Campos para o Rio na data 22/08/2025'.")
        print("Digite 'sair' para terminar ou 'mostrar' para ver o plano atual.")

        while True:
            slots_vazios = self.frame.slots_por_preencher()
            if not slots_vazios:
                print("\nPlano de viagem completo! Obrigado.")
                print(self.frame)
                break

            try:
                entrada = input(f"> ").strip()

                if not entrada: continue

                if entrada.lower() == 'sair':
                    print("Até logo!")
                    break
                if entrada.lower() == 'mostrar':
                    print(self.frame)
                    continue

                # O sistema agora sempre tenta analisar a frase primeiro.
                alteracoes = self.analisar_entrada_simples(entrada)
                
                if alteracoes:
                    for slot, valor in alteracoes.items():
                        self.preencher_slot(slot, valor)
                    print("Entendido. Que mais?")
                else:
                    # Se não conseguiu extrair informação, faz uma pergunta específica.
                    slot_atual = slots_vazios[0]
                    prompt_atual = self.frame.slots[slot_atual]['prompt']
                    print(f"Não entendi a sua frase. Vamos tentar de outra forma.")
                    resposta_direta = input(f"{prompt_atual} > ").strip()
                    self.preencher_slot(slot_atual, resposta_direta)


            except (EOFError, KeyboardInterrupt):
                print("\nAté logo!")
                break

    def preencher_slot(self, nome_slot, valor_texto):
        """
        Valida e preenche um slot. Se o slot espera um frame, busca na base de conhecimento.
        """
        detalhes_slot = self.frame.slots.get(nome_slot)
        if not detalhes_slot:
            return

        tipo_esperado = detalhes_slot.get('tipo')
        valor_texto_lower = valor_texto.lower()

        if tipo_esperado == 'cidade':
            # Busca o frame da cidade na base de conhecimento
            cidade_frame = self.base_de_conhecimento.get(valor_texto_lower)
            if cidade_frame:
                self.frame.definir_valor(nome_slot, cidade_frame)
            else:
                print(f"Desculpe, não tenho informações sobre a cidade '{valor_texto.capitalize()}'.")
        else:
            # Preenche com o valor de texto simples
            self.frame.definir_valor(nome_slot, valor_texto)

# ---------------------------------------------------------------------------
# INÍCIO DO PROGRAMA
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 1. Criar uma base de conhecimento com frames de Cidades
    base_de_conhecimento_cidades = {}
    
    # Usando 'adicionar_slot' e 'definir_valor' para popular os frames estáticos.
    campos = Frame("Campos")
    campos.adicionar_slot("pais", prompt=None)
    campos.adicionar_slot("aeroporto", prompt=None)
    campos.definir_valor("pais", "Brasil")
    campos.definir_valor("aeroporto", "CAW")
    base_de_conhecimento_cidades["campos"] = campos

    rio = Frame("Rio de Janeiro")
    rio.adicionar_slot("pais", prompt=None)
    rio.adicionar_slot("aeroporto", prompt=None)
    rio.definir_valor("pais", "Brasil")
    rio.definir_valor("aeroporto", "GIG")
    base_de_conhecimento_cidades["rio"] = rio
    base_de_conhecimento_cidades["rio de janeiro"] = rio # Alias

    sao_paulo = Frame("São Paulo")
    sao_paulo.adicionar_slot("pais", prompt=None)
    sao_paulo.adicionar_slot("aeroporto", prompt=None)
    sao_paulo.definir_valor("pais", "Brasil")
    sao_paulo.definir_valor("aeroporto", "GRU")
    base_de_conhecimento_cidades["são paulo"] = sao_paulo
    base_de_conhecimento_cidades["sao paulo"] = sao_paulo # Alias

    # 2. Criar o frame principal para a VIAGEM
    viagem_frame = Frame("VIAGEM DE AVIÃO")

    # 3. Definir os slots, indicando o TIPO de frame esperado onde for aplicável
    viagem_frame.adicionar_slot("viajante", prompt="Qual é o nome do viajante?")
    viagem_frame.adicionar_slot("origem", prompt="De que cidade partirá?", tipo="cidade")
    viagem_frame.adicionar_slot("destino", prompt="Para que cidade deseja ir?", tipo="cidade")
    viagem_frame.adicionar_slot("data_partida", prompt="Em que data gostaria de partir? (dd/mm/aaaa)")
    viagem_frame.adicionar_slot("classe", prompt="Qual a classe do voo? (Económica/Executiva)", default="Econômica")

    # 4. Iniciar o sistema de diálogo com o frame e a base de conhecimento
    sistema = SistemaDeFrames(viagem_frame, base_de_conhecimento_cidades)
    sistema.iniciar_dialogo()

