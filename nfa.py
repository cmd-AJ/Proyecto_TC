# nfa.py
class State:
    def __init__(self, is_accept=False):
        self.transitions = {}  # Transiciones regulares
        self.epsilon_transitions = []  # Transiciones epsilon
        self.is_accept = is_accept

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

def regex_to_nfa(postfix_regex):
    stack = []

    for char in postfix_regex:
        if char.isalnum():  # Si es un símbolo del alfabeto
            start_state = State()
            accept_state = State(is_accept=True)
            start_state.transitions[char] = accept_state
            stack.append(NFA(start_state, accept_state))

        elif char == '*':  # Operador Kleene
            nfa = stack.pop()
            start_state = State()
            accept_state = State(is_accept=True)
            start_state.epsilon_transitions.append(nfa.start_state)
            nfa.accept_state.epsilon_transitions.append(nfa.start_state)
            nfa.accept_state.epsilon_transitions.append(accept_state)
            stack.append(NFA(start_state, accept_state))

        elif char == '|':  # Alternación (OR)
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start_state = State()
            accept_state = State(is_accept=True)
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

    return stack.pop()
