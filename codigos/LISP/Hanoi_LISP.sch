;; Define a funcao 'hanoi' que recebe o numero de discos (n)
;; e os nomes das torres de origem, destino e auxiliar.
(define (hanoi n origem destino auxiliar)

  ;; A condicao de parada (caso base) e quando n > 0.
  ;; Se n for 0, nao faz nada.
  (if (> n 0)
      (begin
        ;; Passo 1: Mover n-1 discos da torre de ORIGEM para a AUXILIAR,
        ;; usando a torre de DESTINO como pino temporario.
        (hanoi (- n 1) origem auxiliar destino)

        ;; Passo 2: Mover o disco n (o maior) da ORIGEM para o DESTINO.
        ;; A funcao 'format' imprime a instrucao do movimento.
        ;; #t indica para imprimir na saida padrao (tela).
        ;; ~a sao placeholders para os argumentos, e ~% e uma nova linha.
        (format #t "Mova o disco ~a da torre ~a para a torre ~a~%"
                n origem destino)

        ;; Passo 3: Mover os n-1 discos da torre AUXILIAR para a DESTINO,
        ;; usando a torre de ORIGEM como pino temporario.
        (hanoi (- n 1) auxiliar destino origem)
      )
  )
)

(hanoi 3 'A 'C 'B)


