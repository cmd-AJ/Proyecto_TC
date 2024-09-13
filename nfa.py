import json

class State:
    def __init__(self, name, is_accept=False):
        self.name = name
        self.transitions = {}
        self.epsilon_transitions = []
        self.is_accept = is_accept

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state
    
    def laststate(self, name):
        self.accept_state = State(name, True)

def regex_to_nfa(postfix_regex):
    stack = []
    state_count = 0

    def new_state(is_accept=False):
        nonlocal state_count
        state = State(f'q{state_count}', is_accept)
        state_count += 1
        return state

    # Proceso para convertir el postfix a NFA

    previouschar = ''
    for char in postfix_regex:
        
        if char.isalnum():  # Símbolo del alfabeto
            previouschar = char
            start_state = new_state()
            accept_state = new_state(is_accept=True) #prob
            start_state.transitions[char] = accept_state
            stack.append(NFA(start_state, accept_state))
            

        elif char == '|':  # OR operator
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start_state = new_state()
            accept_state = new_state(is_accept=True)
            
            # Reset accept states of previous NFAs
            nfa1.accept_state.is_accept = False
            nfa2.accept_state.is_accept = False
            
            start_state.epsilon_transitions.append(nfa1.start_state)
            start_state.epsilon_transitions.append(nfa2.start_state)
            nfa1.accept_state.epsilon_transitions.append(accept_state)
            nfa2.accept_state.epsilon_transitions.append(accept_state)
            
            stack.append(NFA(start_state, accept_state))

        elif char == '*':  # Kleene star
            nfa = stack.pop()
            start_state = new_state()
            accept_state = new_state(is_accept=True)
            
            # Reset accept state of the NFA before applying *
            nfa.accept_state.is_accept = False
            
            start_state.epsilon_transitions.append(nfa.start_state)
            nfa.accept_state.epsilon_transitions.append(nfa.start_state)
            nfa.accept_state.epsilon_transitions.append(accept_state)
            
            # Allow epsilon transition from start to accept for zero occurrences
            start_state.epsilon_transitions.append(accept_state)
            
            stack.append(NFA(start_state, accept_state))

        elif char == '•':  # Concatenación
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept_state.is_accept = False  # El estado intermedio ya no es de aceptación
            nfa1.accept_state.epsilon_transitions.append(nfa2.start_state)
            stack.append(NFA(nfa1.start_state, nfa2.accept_state))
        
    



    final_nfa = stack.pop()

    # Crear el JSON en un formato similar al DFA
    nfa_dict = {
        "ESTADOS": [],
        "SIMBOLOS": [],
        "INICIO": [final_nfa.start_state.name],
        "ACEPTACION": [],
        "TRANSICIONES": []
    }

    visited = set()

    def add_state_to_json(state):
        if state.name not in visited:
            visited.add(state.name)
            nfa_dict["ESTADOS"].append(state.name)

            if state.is_accept:
                nfa_dict["ACEPTACION"].append(state.name)

            # Agregar las transiciones
            for symbol, next_state in state.transitions.items():
                nfa_dict["TRANSICIONES"].append(f"{state.name}->{symbol}->{next_state.name}")
                if symbol not in nfa_dict["SIMBOLOS"]:
                    nfa_dict["SIMBOLOS"].append(symbol)
                add_state_to_json(next_state)

            # Transiciones epsilon
            for epsilon_state in state.epsilon_transitions:
                nfa_dict["TRANSICIONES"].append(f"{state.name}->$->{epsilon_state.name}")
                add_state_to_json(epsilon_state)

    add_state_to_json(final_nfa.start_state)

    # Guardar el JSON
    with open('nfa_output.json', 'w') as f:
        json.dump(nfa_dict, f, indent=4)

    return final_nfa

# Ejemplo de uso
if __name__ == "__main__":
    postfix_expression = "bb|*a•b•"  # Expresión en notación postfix
    nfa = regex_to_nfa(postfix_expression)
    print("NFA generado y guardado en 'nfa_output.json'")
