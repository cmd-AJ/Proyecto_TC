import nfa
import stack  # Algoritmo de Shunting Yard
from dfa import nfa_to_dfa

# Declara el stack utilizado para hacer el algoritmo de Shunting Yard
output_stack = stack.estack()

def main():
    print("Bienvenidos\nPor favor inserten la expresión regular")
    print("Tomar nota de estos símbolos\nOperadores:\n | OR uso: (a|b)\n * Estrella de Kleene uso: b*\n Epsilon como &")
    print(f"\033[1;33;40m TOMAR NOTA NO ES NECESARIO PONER • el algoritmo lo realiza por sí mismo \033[0m")
    print(f"\033[1;31;40m EJEMPLO DE PRUEBA :\033[0m   (b|b)*abb(a|b)*\n\n")

    # Paso 1: Recibir la expresión regular y convertirla a postfix
    lenguaje = input("Ingrese su expresión regular:\n")

    # Realiza el algoritmo de Shunting Yard
    stack.regexp_a_postfix(lenguaje, output_stack)

    # Convertir la lista de postfix a una cadena
    postfix_expression = stack.list_to_exp(output_stack.getstack())
    print(f"\033[1;34;40m EXPRESIÓN EN POSTFIX :\033[0m", postfix_expression)

    # Paso 2: Generar el AFN a partir de la expresión regular en postfix
    print("Generando el AFN (Automata Finito No Determinista)...")
    nfa_automaton = nfa.regex_to_nfa(postfix_expression)
    print("AFN generado exitosamente.")

    # Exportar el AFN a JSON (si lo necesitas)
    

    # Paso 3: Convertir el AFN en AFD usando el algoritmo de construcción de subconjuntos
    alphabet = set(lenguaje) - set("()*|")  # Extraer el alfabeto de la expresión regular
    print("Convirtiendo el AFN a AFD (Automata Finito Determinista)...")
    dfa_automaton = nfa_to_dfa(nfa_automaton, alphabet)
    print("AFD generado exitosamente.")

    # Paso 4: Recibir la cadena de prueba w y simular el AFD
    w = input("Ingrese la cadena a evaluar (w): ")

    # Simulación del AFD con la cadena w
    result, transitions = simulate_dfa(dfa_automaton, w)

    # Paso 5: Imprimir el resultado de la simulación y las transiciones realizadas
    print(f"\033[1;34;40m Resultado de la simulación: {result}\033[0m")
    print("Transiciones realizadas:")
    for t in transitions:
        print(t)

# Simulación del AFD con la cadena w
def simulate_dfa(dfa, input_string):
    current_state = dfa.start_state
    transitions_made = []

    for symbol in input_string:
        # Si el símbolo no está en las transiciones del estado actual, se rechaza la cadena
        if (current_state, symbol) not in dfa.transitions:
            return "NO", transitions_made
        next_state = dfa.transitions[(current_state, symbol)]
        transitions_made.append(f"{', '.join([state.name for state in current_state])} --{symbol}--> {', '.join([state.name for state in next_state])}")
        current_state = next_state

    # Al final, si el estado actual es un estado de aceptación, la cadena es aceptada
    if current_state in dfa.accept_states:
        return "SÍ", transitions_made
    else:
        return "NO", transitions_made

if __name__ == "__main__":
    main()
