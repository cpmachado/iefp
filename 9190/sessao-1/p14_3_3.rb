# frozen_string_literal: true

print "Bom dia\n"

print 'Qual o 1º valor para a soma? '
a = gets.chomp.to_f

print 'Qual o 2º valor para a soma? '
b = gets.chomp.to_f

res = a + b
print "A soma é = #{res}\n"
