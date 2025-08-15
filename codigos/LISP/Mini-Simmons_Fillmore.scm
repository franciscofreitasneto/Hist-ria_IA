;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                                                                     ;;;
;;;     Modelo Demonstrativo da Gramática de Casos (Simmons/Fillmore)   ;;;
;;;                                                                     ;;;
;;;   Este programa analisa frases simples, representa-as numa rede     ;;;
;;;   semântica baseada em casos e responde a perguntas sobre o           ;;;
;;;   conhecimento armazenado. (Versão Corrigida)                       ;;;
;;;                                                                     ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; Importa a biblioteca SRFI-1 para ter acesso a funções como 'filter', 'find' e 'every'.
(use-modules (srfi srfi-1))

;;; ---------------------------------------------------------------------------
;;; 1. A BASE DE CONHECIMENTO (Memória de Eventos)
;;; ---------------------------------------------------------------------------

(define *memoria-de-eventos* '())
(define *proximo-id-evento* 1)


;;; ---------------------------------------------------------------------------
;;; 2. O ANALISADOR (Mapeamento M1: Linguagem -> Ideias)
;;; ---------------------------------------------------------------------------

(define (encontrar-caso palavra-chave frase)
  (let ((resultado (member palavra-chave frase)))
    (if (and resultado (not (null? (cdr resultado))))
        (cadr resultado)
        #f)))

;;; CORREÇÃO: A função agora é mais flexível e não exige um tamanho mínimo.
;;; Ela extrai os componentes que consegue encontrar.
(define (analisar-frase frase)
  (let* ((agente (if (>= (length frase) 1) (list-ref frase 0) #f))
         (verbo  (if (>= (length frase) 2) (list-ref frase 1) #f))
         (objeto (if (>= (length frase) 3) (list-ref frase 2) #f))
         (destino (encontrar-caso 'para frase))
         (localizacao (encontrar-caso 'em frase)))
    ;; Constrói a lista de associação de casos
    (list (cons 'verbo verbo)
          (cons 'agente agente)
          (cons 'objeto objeto)
          (if destino (cons 'destino destino) #f)
          (if localizacao (cons 'localizacao localizacao) #f))))

;;; CORREÇÃO: A validação da frase (tamanho >= 3) agora é feita aqui.
(define (adicionar-evento! frase)
  (if (< (length frase) 3)
      "Não consegui analisar. Uma declaração precisa de pelo menos Agente, Verbo e Objeto."
      (let ((estrutura-caso (analisar-frase frase)))
        (begin
          (let ((id-evento (string->symbol (string-append "evento-" (number->string *proximo-id-evento*)))))
            (set! *memoria-de-eventos*
                  (cons (cons id-evento (filter identity estrutura-caso))
                        *memoria-de-eventos*))
            (set! *proximo-id-evento* (+ *proximo-id-evento* 1)))
          "Entendido."))))


;;; ---------------------------------------------------------------------------
;;; 3. O RESPONDEDOR (Mapeamento M2: Ideias -> Ideias)
;;; ---------------------------------------------------------------------------

(define (corresponde-padrao? padrao evento)
  (every (lambda (par-padrao)
           (let ((caso-evento (assoc (car par-padrao) (cdr evento))))
             (or (eq? (cdr par-padrao) '?)
                 (and caso-evento (equal? (cdr caso-evento) (cdr par-padrao))))))
         padrao))

(define (responder-pergunta pergunta)
  (let* ((caso-perguntado (car (filter (lambda (p) (eq? (cdr p) '?)) pergunta)))
         (evento-encontrado (find (lambda (evento) (corresponde-padrao? pergunta evento))
                                  *memoria-de-eventos*)))
    (if evento-encontrado
        (let ((resposta (assoc (car caso-perguntado) (cdr evento-encontrado))))
          (if resposta
              (cadr resposta)
              "Encontrei o evento, mas não a informação específica."))
        "Não sei a resposta.")))

;;; CORREÇÃO: A função agora funciona corretamente, pois 'analisar-frase' é mais flexível.
(define (analisar-pergunta pergunta)
  (let ((palavra-interrogativa (car pergunta))
        (resto-pergunta (cdr pergunta)))
    (let ((estrutura-caso (analisar-frase resto-pergunta)))
      (case palavra-interrogativa
        ((quem) (cons '(agente . ?) estrutura-caso))
        ((o-que) (cons '(objeto . ?) estrutura-caso))
        ((onde) (cons '(localizacao . ?) estrutura-caso))
        (else "Só sei responder a 'quem', 'o-que' e 'onde'.")))))


;;; ---------------------------------------------------------------------------
;;; 4. LOOP PRINCIPAL
;;; ---------------------------------------------------------------------------

(define (loop-interativo)
  (display "> ")
  (let ((entrada (read)))
    (cond
     ((equal? entrada '(sair))
      (display "Até logo!\n"))
     ((memq (car entrada) '(quem o-que onde))
      (let ((padrao (analisar-pergunta entrada)))
        (if (string? padrao)
            (display padrao)
            (display (responder-pergunta padrao))))
      (newline)
      (loop-interativo))
     (else
      (display (adicionar-evento! entrada))
      (newline)
      (loop-interativo)))))

;;; ---------------------------------------------------------------------------
;;; INÍCIO DO PROGRAMA
;;; ---------------------------------------------------------------------------
(display "Olá! Eu sou um sistema de perguntas e respostas baseado em casos.")
(newline)
(display "Diga-me algo, como: (joao deu o livro para maria em a biblioteca)")
(newline)
(loop-interativo)

