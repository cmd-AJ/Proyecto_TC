# main.py
from draw import drawing_grapgh
from minimize import minimize_dfa
from nfa import regex_to_nfa  # Importamos la función regex_to_nfa desde nfa.py
from stack import list_to_exp, regexp_a_postfix_v2  # Importamos la función regexp_a_postfix desde stack.py
from dfa import nfa_to_dfa  # Mantén esta importación si tienes un archivo dfa.py

# Declara el stack utilizado para hacer el algoritmo de Shunting Yard
import stack  # Para usar estack
output_stack = stack.estack()
import json
import pandas as pd

def tabla(path):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1200)
        # Load the JSON data
        with open(path, 'r') as file:
            data = json.load(file)
        
        # Extract states and symbols
        estados = data['ESTADOS']  # Treat states as literal strings
        simbolos = data['SIMBOLOS']
        inicio = data['INICIO']  # Start state as a literal string
        aceptacion = data['ACEPTACION']  # Acceptance states as literal strings
        transiciones = data['TRANSICIONES']

        headers = simbolos.copy()  # Copy the symbols as headers
        if 'nfa' in path:
            headers.append('$')
            simbolos.append('$')
        headers.append('salida')   # Add 'salida' for start/acceptance status

        # States letters for index
        index = estados
        emptydata = {
            
        }

        # Initialize table with '0's for every state and symbol
        for symbol in headers:
            emptydata[symbol] = ['0'] * len(index)
            
        

        # Create the DataFrame
        df = pd.DataFrame(emptydata, index=index, columns= headers)
        

        # Mark start and accept states in the 'salida' column
        for e in aceptacion:
            if e in aceptacion:
                df.loc[e, 'salida'] = '1'  # Mark accept states
        
        for e in inicio:
            df.loc[e, 'salida'] = '--> ' + df.loc[e, 'salida']  # Mark start state
            

        # Fill transitions based on the TRANSICIONES data
        for transition in transiciones:
            parts = transition.split('->')
            from_state = parts[0]  # No need to strip {} since it's treated as string
            symbol = parts[1]
            to_state = parts[2]

            # Get state index based on the state strings in 'estados'
            from_state_idx = estados.index(from_state)
            to_state_idx = estados.index(to_state)

            # Set the transition in the dataframe
            df.loc[from_state, symbol] = to_state
        
        

        # Handle null transitions (QT row)
        has_null = False
        for symbol in simbolos:
            for state_name in index:
                if df.loc[state_name, symbol] == '0':
                    df.loc[state_name, symbol] = 'QT'
                    has_null = True

        if has_null:
            # Add QT row if null transitions exist
            qt_row = {symbol: 'QT' for symbol in headers}
            qt_row['salida'] = '0'
            df = pd.concat([df, pd.DataFrame(qt_row, index=['QT'])])
            index.append('QT')
            

        return df


def main():
    print("Bienvenidos\nPor favor inserten la expresión regular")
    print("Tomar nota de estos símbolos\nOperadores:\n | OR uso: (a|b)\n * Estrella de Kleene uso: b*\n Epsilon como $")
    print(f"\033[1;33;40m TOMAR NOTA NO ES NECESARIO PONER • el algoritmo lo realiza por sí mismo \033[0m")
    print(f"\033[1;31;40m EJEMPLO DE PRUEBA :\033[0m   (b|b)*abb(a|b)*\n\n")

    # Paso 1: Recibir la expresión regular y convertirla a postfix
    lenguaje = input("Ingrese su expresión regular:\n")

    try:
        postfix_expression = regexp_a_postfix_v2(lenguaje, output_stack)
        print()
        print(f"\033[1;34;40m EXPRESIÓN EN POSTFIX :\033[0m", postfix_expression)
    except Exception as e:
        print(f"Error al convertir la expresión a postfix: {e}")
        return

    try:
        # Paso 2: Generar el AFN a partir de la expresión regular en postfix
        print("Generando el AFN (Automata Finito No Determinista)...")
        nfa_automaton = regex_to_nfa(postfix_expression)
        print("AFN generado exitosamente.")
        
        print(tabla('nfa_output.json'))   
        drawing_grapgh('nfa_output.json')    
        
    except Exception as e:
        print(f"Error al generar el AFN: {e}")
        return

    try:
        # Paso 3: Convertir el AFN en AFD usando el algoritmo de construcción de subconjuntos
        alphabet = set(lenguaje) - set("()*|")  # Extraer el alfabeto de la expresión regular
        print("Convirtiendo el AFN a AFD (Automata Finito Determinista)...")
        dfa_automaton = nfa_to_dfa(nfa_automaton, alphabet)
        print("AFD generado exitosamente.")
        print(tabla('dfa.json'))
        drawing_grapgh('dfa.json')
    except Exception as e:
        print(f"Error al generar el AFD: {e}")
        return
    
    
    try:
        #Paso 4 minimizar
        s = minimize_dfa('dfa.json')
        s.convertir_subconjuntos_a_letras()

        # Imprime la tabla del AFD
        print(f"\033[1;32;40m Tabla del AFD\033[0m")
        tabla_afd = s.tabla_subcon()
        print(tabla_afd)

        print('\n')

        # Imprime la tabla de minimización
        print(f"\033[1;34;40m Tabla de minimización\033[0m")
        tabla_minimizacion = s.minimizacion_tabla()
        print(tabla_minimizacion)
        print()
        print(f"\033[1;32;40m Tabla AFD MINIMIZADA\033[0m")
        tabla_minimizada = s.exposetablaafd(tabla_minimizacion, tabla_afd)
        print(tabla_minimizada)

        s.tojson(tabla_minimizada)
        drawing_grapgh('dfa_min.json')
        
    except Exception as e:
        print(f"Error al generar el AFD MINIMIZADA: {e}")
        return


    # Paso 4: Recibir la cadena de prueba w y simular el AFD
    w = input("Ingrese la cadena a evaluar (w): ")

    try:
        # Simulación del AFD con la cadena w
        result, transitions = simulate_dfa(dfa_automaton, w)

        # Paso 5: Imprimir el resultado de la simulación y las transiciones realizadas
        print(f"\033[1;34;40m Resultado de la simulación: {result}\033[0m")
        print("Transiciones realizadas:")
        for t in transitions:
            print(t)
    except Exception as e:
        print(f"Error en la simulación del AFD: {e}")


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
