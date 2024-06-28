# frozen_string_literal: true

print 'Nome: '
nome = gets.chomp

print 'Valor: '
valor = gets.chomp.to_f

print 'Prazo em meses: '
prazo = gets.chomp.to_f

print 'Finalidade: '
finalidade = gets.chomp

print 'Taxa de juro por mês: '
taxa_de_juro = gets.chomp.to_f / 100.0

print "\n"
print "########################################################\n"
print "Perguntas sobre crédito para #{finalidade} do #{nome}:\n"
print "########################################################\n"

valor_juro_mensal = taxa_de_juro * valor
printf("Valor a pagar do juro mensal? %.2f\n", valor_juro_mensal)
valor_mensalidade = valor / prazo + valor_juro_mensal
printf("Valor da mensalidade com o juro? %.2f\n", valor_mensalidade)
valor_anual = valor_mensalidade * 12
printf("Valor anual de mensalidades? (com juros) %.2f\n", valor_anual)
valor_final = valor_mensalidade * prazo
printf("Montante final do empréstimo? %.2f\n", valor_final)
