;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                                                                     ;;;
;;;    Mini-SHRDLU: Um Exemplo Simplificado de Interação em Scheme      ;;;
;;;                                                                     ;;;
;;;   Este programa simula um robô que pode manipular blocos em um      ;;;
;;;   mundo virtual, respondendo a comandos em linguagem natural        ;;;
;;;   (representados como listas).                                      ;;;
;;;                                                                     ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; Importa a biblioteca SRFI-1 para ter acesso à função 'any'.
(use-modules (srfi srfi-1))

;;; ---------------------------------------------------------------------------
;;; 1. O ESTADO DO MUNDO E DO ROBÔ
;;; ---------------------------------------------------------------------------

;;; O *mundo* é uma lista de objetos. Cada objeto é uma lista contendo
;;; seu nome e uma lista de propriedades (como cor, tamanho e onde está).
(define *mundo*
  '( (bloco-vermelho ((cor vermelho) (tamanho pequeno) (em-cima-de mesa)))
     (bloco-azul     ((cor azul)     (tamanho pequeno) (em-cima-de bloco-vermelho)))
     (caixa-verde    ((cor verde)    (tamanho grande)  (em-cima-de mesa))) ))

;;; A *mao-do-robo* guarda o que o robô está segurando.
;;; Começa vazia.
(define *mao-do-robo* 'vazia)


;;; ---------------------------------------------------------------------------
;;; 2. FUNÇÕES AUXILIARES (Para consultar e modificar o mundo)
;;; ---------------------------------------------------------------------------

;;; Encontra um objeto no mundo pelo seu nome.
(define (encontrar-objeto nome-objeto)
  (assoc nome-objeto *mundo*))

;;; Encontra o valor de uma propriedade específica de um objeto.
(define (obter-propriedade objeto propriedade)
  (assoc propriedade (cadr objeto)))

;;; Modifica uma propriedade de um objeto no mundo.
;;; Usa 'set-cdr!' para modificar a estrutura de dados diretamente.
(define (definir-propriedade! objeto propriedade valor)
  (let ((prop (obter-propriedade objeto propriedade)))
    (if prop
        (set-cdr! prop (list valor))
        ;; Se a propriedade não existe, adiciona-a.
        (set-cdr! objeto (cons (list propriedade valor) (cadr objeto))))))

;;; Verifica se um objeto está livre (se não há nada em cima dele).
(define (objeto-esta-livre? nome-objeto)
  (not (any (lambda (obj)
                 (let ((prop-em-cima (obter-propriedade obj 'em-cima-de)))
                   (and prop-em-cima (eq? (cadr prop-em-cima) nome-objeto))))
               *mundo*)))


;;; ---------------------------------------------------------------------------
;;; 3. LÓGICA DAS AÇÕES (O que o robô pode fazer)
;;; ---------------------------------------------------------------------------

;;; Pega um objeto.
(define (acao-pegar nome-objeto)
  (let ((objeto (encontrar-objeto nome-objeto)))
    (cond
     ((not objeto)
      "Não vejo nenhum objeto com esse nome.")
     ((not (eq? *mao-do-robo* 'vazia))
      "Minha mão já está ocupada.")
     ((not (objeto-esta-livre? nome-objeto))
      (string-append "Não posso pegar o " (symbol->string nome-objeto) ", há algo em cima dele."))
     (else
      (set! *mao-do-robo* nome-objeto)
      (definir-propriedade! objeto 'em-cima-de 'mao-do-robo)
      "OK."))))

;;; Coloca um objeto em cima de outro.
(define (acao-colocar nome-objeto-movido nome-destino)
  (let ((objeto-movido (encontrar-objeto nome-objeto-movido))
        (objeto-destino (encontrar-objeto nome-destino)))
    (cond
     ((not (eq? *mao-do-robo* nome-objeto-movido))
      (string-append "Não estou segurando o " (symbol->string nome-objeto-movido) "."))
     ((and (not (eq? nome-destino 'mesa)) (not objeto-destino))
      "Não vejo o destino que você mencionou.")
     ((not (objeto-esta-livre? nome-destino))
      (string-append "Não posso colocar nada em cima do " (symbol->string nome-destino) ", ele não está livre."))
     (else
      (set! *mao-do-robo* 'vazia)
      (definir-propriedade! objeto-movido 'em-cima-de nome-destino)
      "OK."))))

;;; Descreve o estado atual do mundo.
(define (acao-olhar)
  (display "No mundo, eu vejo o seguinte:") (newline)
  (for-each
   (lambda (obj)
     (let* ((nome (car obj))
            (prop-em-cima (obter-propriedade obj 'em-cima-de))
            (local (cadr prop-em-cima)))
       (format #t " - O ~a está em cima do(a) ~a.~%" nome local)))
   *mundo*)
  "") ;; Retorna uma string vazia para o loop principal.


;;; ---------------------------------------------------------------------------
;;; 4. ANALISADOR DE COMANDOS E LOOP PRINCIPAL
;;; ---------------------------------------------------------------------------

;;; Analisa o comando do usuário e chama a ação correspondente.
(define (analisar-e-executar comando)
  ;; A função agora espera que o comando seja sempre uma lista.
  (if (not (list? comando))
      "Comando inválido. Por favor, coloque seus comandos entre parênteses, como (pegue bloco-azul)."
      (case (car comando)
        ;; REVERSÃO: Agora aceita apenas 'pegue'.
        ((pegue) (if (= (length comando) 2)
                     (acao-pegar (cadr comando))
                     "Comando 'pegue' incompleto. Ex: (pegue bloco-azul)"))
        ((coloque) (if (and (= (length comando) 4) (eq? (caddr comando) 'sobre))
                       (acao-colocar (cadr comando) (cadddr comando))
                       "Comando 'coloque' incompleto. Ex: (coloque bloco-azul sobre caixa-verde)"))
        ((olhe) (if (= (length comando) 1)
                    (acao-olhar)
                    "Comando 'olhe' não precisa de argumentos."))
        ((sair) 'quit)
        (else "Não conheço o comando."))))

;;; O loop interativo principal.
(define (loop-interativo)
  (display "> ")
  (let ((entrada (read)))
    ;; A lógica de saída foi simplificada, pois 'analisar-e-executar'
    ;; agora lida com o comando (sair).
    (let ((resposta (analisar-e-executar entrada)))
      (if (not (eq? resposta 'quit))
          (begin
            (display resposta)
            (newline)
            (loop-interativo))
          (display "Até logo!\n")))))


;;; ---------------------------------------------------------------------------
;;; INÍCIO DO PROGRAMA
;;; ---------------------------------------------------------------------------
(display "Olá! Eu sou um robô que manipula blocos. Dê-me um comando.")
(newline)
(loop-interativo)

