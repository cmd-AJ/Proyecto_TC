import nfa
import stack #AKA EL ALGORITMO DE SHUNTIN YAND


#Declara el stack utilizado para hacer el algoritmo de SHUNTING
output_stack = stack.estack()




print("Bienvenidos\nPor favor inserten la expresion regular")

print("Tomar nota de estos simbolos\noperadores:\n | OR uso: (a|b)\n * Estrella kleen uso: b*")

print(f"\033[1;33;40m TOMAR NOTA NO ES NECESARIO PONER • el algoritmo lo realiza por si mismo \033[0m " )

print(f"\033[1;31;40m EJEMPLO DE PRUEBA :\033[0m   (b|b)*abb(a|b)*\n\n" )




#Valores de prueba '(b|b)*abb(a|b)*'
lenguaje = input("Ingrese su expresion regular\n")

#De la clase STACK REALIZA EL ALGORITMO DE SHUNTING YAND
stack.regexp_a_postfix(lenguaje, output_stack)


#Regexp a postfix en lista
# print(output_stack.getstack())

#GUARDA LA EXPRESION QUE RETORNO DE LA CLASE STACK
postfix_expression =  stack.list_to_exp(output_stack.getstack())

print(f"\033[1;34;40m EXPRESION A POSTFIX :\033[0m",  postfix_expression)


#postfix_expression es la expresion ya en postfix Utilizarlo para Thompson
