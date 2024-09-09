import json
from graphviz import Digraph


class State:
    def __init__(self, name, is_accept=False):
        self.name = name
        self.transitions = {}  # Transiciones regulares
        self.epsilon_transitions = []  # Transiciones epsilon
        self.is_accept = is_accept

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

def regex_to_nfa(postfix_regex):
    stack = []
    state_count = 0  # Para generar nombres únicos de estados

    def new_state(is_accept=False):
        nonlocal state_count
        state = State(f'q{state_count}', is_accept)
        state_count += 1
        return state

    for char in postfix_regex:
        if char.isalnum():  # Si es un símbolo del alfabeto
            start_state = new_state()
            accept_state = new_state(is_accept=True)
            start_state.transitions[char] = accept_state
            stack.append(NFA(start_state, accept_state))

        elif char == '*':  # Operador Kleene
            nfa = stack.pop()
            start_state = new_state()
            accept_state = new_state(is_accept=True)
            start_state.epsilon_transitions.append(nfa.start_state)
            nfa.accept_state.epsilon_transitions.append(nfa.start_state)
            nfa.accept_state.epsilon_transitions.append(accept_state)
            stack.append(NFA(start_state, accept_state))

        elif char == '|':  # Alternación (OR)
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start_state = new_state()
            accept_state = new_state(is_accept=True)
            start_state.epsilon_transitions.append(nfa1.start_state)
            start_state.epsilon_transitions.append(nfa2.start_state)
            nfa1.accept_state.epsilon_transitions.append(accept_state)
            nfa2.accept_state.epsilon_transitions.append(accept_state)
            stack.append(NFA(start_state, accept_state))

        elif char == '.':  # Concatenación
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept_state.epsilon_transitions.append(nfa2.start_state)
            nfa1.accept_state.is_accept = False
            stack.append(NFA(nfa1.start_state, nfa2.accept_state))

    final_nfa = stack.pop()

    # Crear estructura para el archivo JSON
    nfa_dict = {
        "Q": [],
        "sigma": [],
        "q0": final_nfa.start_state.name,
        "F": [],
        "FUNC": []
    }

    def add_state_to_json(state):
        if state.name not in nfa_dict["Q"]:
            nfa_dict["Q"].append(state.name)
            if state.is_accept:
                nfa_dict["F"].append(state.name)
            for symbol, next_state in state.transitions.items():
                nfa_dict["FUNC"].append(f"{state.name},{symbol},{next_state.name}")
                if symbol not in nfa_dict["sigma"]:
                    nfa_dict["sigma"].append(symbol)
                add_state_to_json(next_state)
            for epsilon_state in state.epsilon_transitions:
                nfa_dict["FUNC"].append(f"{state.name},ε,{epsilon_state.name}")
                add_state_to_json(epsilon_state)

    add_state_to_json(final_nfa.start_state)

    # Guardar el NFA como archivo .json
    with open('nfa_output.json', 'w') as f:
        json.dump(nfa_dict, f, indent=4)

    return final_nfa

# Ejemplo de uso:
# a(a|b)*b
postfix_expression = "a•ab|*"  # Expresión en postfix
nfa = regex_to_nfa(postfix_expression)
