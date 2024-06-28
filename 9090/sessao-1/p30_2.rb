# frozen_string_literal: true

print 'Insira um número inteiro: '
n1 = gets.chomp.to_i
print 'Insira outro número inteiro: '
n2 = gets.chomp.to_i

print "n1: #{n1}\n"
print "n2: #{n2}\n"

n1, n2 = n2, n1

puts 'Trocando os valores'

print "n1: #{n1}\n"
print "n2: #{n2}\n"
