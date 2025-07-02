;; Definição da função (seu código original)
(define (fatorial n)
  (if (<= n 1)
      1
      (* n (fatorial (- n 1)))))

;; --- LINHAS NOVAS ---
;; Chamada da função para um valor específico e impressão do resultado
(display (fatorial 10)) ; Calcula e exibe o fatorial de 10
(newline)               ; Adiciona uma quebra de linha para a saída ficar limpa
