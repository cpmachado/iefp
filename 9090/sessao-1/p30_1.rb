# frozen_string_literal: true

print 'Temperatura em Celsius: '
c = gets.chomp.to_f

f = 9.0 * c / 5.0 + 32.0

print "#{c} ºC = #{f} ºF\n"
