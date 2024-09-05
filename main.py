# main.py
from nfa import regex_to_nfa
from stack import regexp_a_postfix  # Aquí importas tu función existente

# Expresión regular en infix
infix_regex = '(b|b)*abb(a|b)*'

# Usa la función que ya tienes para convertir a postfix
postfix_regex = ''.join(regexp_a_postfix(infix_regex))  # Asegúrate de que devuelva una lista y la unes a una cadena
print(f'Postfix: {postfix_regex}')  # Para verificar la conversión

# Generar AFN a partir de la expresión regular en postfix
nfa = regex_to_nfa(postfix_regex)
print(f"AFN creado con estado inicial: {nfa.start_state}")

# (Opcional) Aquí puedes continuar con la conversión del AFN a AFD o graficar el AFN
