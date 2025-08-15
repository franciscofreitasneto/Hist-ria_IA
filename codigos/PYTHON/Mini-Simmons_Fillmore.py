# -*- coding: utf-8 -*-

class SistemaSemantico:
    """
    Esta classe implementa um modelo simplificado da Gramática de Casos
    de Simmons/Fillmore. Ela analisa frases, armazena-as numa base de
    conhecimento e responde a perguntas sobre os eventos armazenados.
    """

    def __init__(self):
        """
        Inicializa a base de conhecimento.
        A memória de eventos é um dicionário que mapeia um ID de evento
        a um outro dicionário que representa o quadro de caso.
        """
        self.memoria_de_eventos = {}
        self.proximo_id_evento = 1

    # ---------------------------------------------------------------------------
    # 2. O ANALISADOR (Mapeamento M1: Linguagem -> Ideias)
    # ---------------------------------------------------------------------------

    def analisar_frase(self, frase_lista):
        """
        Analisa uma lista de palavras e a converte numa estrutura de quadro de caso.
        Retorna um dicionário representando os casos.
        """
        estrutura_caso = {}
        
        # Extrai os componentes obrigatórios (Agente, Verbo, Objeto)
        if len(frase_lista) >= 1:
            estrutura_caso['agente'] = frase_lista[0]
        if len(frase_lista) >= 2:
            estrutura_caso['verbo'] = frase_lista[1]
        if len(frase_lista) >= 3:
            estrutura_caso['objeto'] = frase_lista[2]

        # Extrai os componentes opcionais (Destino, Localização)
        try:
            idx_para = frase_lista.index('para')
            if idx_para + 1 < len(frase_lista):
                estrutura_caso['destino'] = frase_lista[idx_para + 1]
        except ValueError:
            pass  # 'para' não está na frase

        try:
            idx_em = frase_lista.index('em')
            if idx_em + 1 < len(frase_lista):
                # Junta o resto da frase para a localização (ex: "a biblioteca")
                estrutura_caso['localizacao'] = " ".join(frase_lista[idx_em + 1:])
        except ValueError:
            pass  # 'em' não está na frase
            
        return estrutura_caso

    def adicionar_evento(self, frase_lista):
        """
        Valida uma frase, analisa-a e adiciona o evento à memória.
        """
        if len(frase_lista) < 3:
            return "Não consegui analisar. Uma declaração precisa de pelo menos Agente, Verbo e Objeto."

        estrutura_caso = self.analisar_frase(frase_lista)
        
        id_evento = f"evento-{self.proximo_id_evento}"
        self.memoria_de_eventos[id_evento] = estrutura_caso
        print(self.memoria_de_eventos)
        self.proximo_id_evento += 1
        
        return "Entendido."

    # ---------------------------------------------------------------------------
    # 3. O RESPONDEDOR (Mapeamento M2: Ideias -> Ideias)
    # ---------------------------------------------------------------------------

    def analisar_pergunta(self, pergunta_lista):
        """
        Converte uma pergunta do utilizador num padrão de busca (dicionário).
        """
        palavra_interrogativa = pergunta_lista[0]
        resto_pergunta = pergunta_lista[1:]
        
        #padrao = self.analisar_frase(resto_pergunta)
        
        if palavra_interrogativa == 'quem':
            resto_pergunta.insert(0,'X')
            padrao = self.analisar_frase(resto_pergunta)
            padrao['agente'] = '?'
        elif palavra_interrogativa == 'o-que':
            resto_pergunta.insert(2,'X')
            padrao = self.analisar_frase(resto_pergunta)
            padrao['objeto'] = '?'
        elif palavra_interrogativa == 'onde':
            resto_pergunta.insert(3,'X')
            padrao = self.analisar_frase(resto_pergunta)
            padrao['localizacao'] = '?'
        else:
            return None # Pergunta não reconhecida
            
        return padrao

    def responder_pergunta(self, padrao):
        """
        Busca na memória um evento que corresponda ao padrão da pergunta.
        """
        caso_perguntado = None
        for caso, valor in padrao.items():
            if valor == '?':
                caso_perguntado = caso
                break
        
        if not caso_perguntado:
            return "Pergunta mal formada."

        # Itera sobre todos os eventos na memória
        for evento_id, estrutura_evento in self.memoria_de_eventos.items():
            corresponde = True
            # Verifica se todos os fatos da pergunta correspondem ao evento
            for caso, valor in padrao.items():
                if valor != '?' and estrutura_evento.get(caso) != valor:
                    corresponde = False
                    break
            
            # Se encontrou uma correspondência, retorna a resposta
            if corresponde:
                resposta = estrutura_evento.get(caso_perguntado)
                return resposta if resposta else "Encontrei o evento, mas não a informação específica."

        return "Não sei a resposta."

# ---------------------------------------------------------------------------
# 4. LOOP PRINCIPAL
# ---------------------------------------------------------------------------

def loop_interativo():
    """
    Inicia e mantém o loop de conversação com o utilizador.
    """
    sistema = SistemaSemantico()
    print("Olá! Eu sou um sistema de perguntas e respostas baseado em casos.")
    print("Diga-me algo, como: joao deu o livro para maria em a biblioteca")
    print("Ou pergunte algo, como: quem deu o livro")
    print("Digite 'sair' para terminar.")
    
    while True:
        try:
            entrada_bruta = input("> ")
            if not entrada_bruta:
                continue
            
            if entrada_bruta.lower() == 'sair':
                print("Até logo!")
                break
            
            entrada_lista = entrada_bruta.lower().split()
            primeira_palavra = entrada_lista[0]
            
            if primeira_palavra in ['quem', 'o-que', 'onde']:
                padrao = sistema.analisar_pergunta(entrada_lista)
                if padrao:
                    print(sistema.responder_pergunta(padrao))
                else:
                    print("Só sei responder a 'quem', 'o-que' e 'onde'.")
            else:
                print(sistema.adicionar_evento(entrada_lista))

        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

# ---------------------------------------------------------------------------
# INÍCIO DO PROGRAMA
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    loop_interativo()

