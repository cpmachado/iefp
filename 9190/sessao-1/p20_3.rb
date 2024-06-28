# frozen_string_literal: true

print 'Número de dias: '
dias = gets.chomp.to_i

print 'Distância percorrida(km): '
distancia = gets.chomp.to_f

preco = 25 * dias + 0.15 * distancia

print "Preço a pagar: #{preco}\n"
