# dfa.py
class DFA:
    def __init__(self):
        self.states = []
        self.start_state = None
        self.accept_states = []
        self.transitions = {}  # {(frozenset(state), symbol): frozenset(next_state)}

def epsilon_closure(states):
    """ Compute the epsilon closure of a set of states """
    stack = list(states)  # Trabajamos con un conjunto de estados
    closure = set(states)  # Inicializamos el closure con los estados recibidos

    while stack:
        current_state = stack.pop()
        for next_state in current_state.epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return frozenset(closure)

def move(states, symbol):
    """ Compute the move of a set of states on a given symbol """
    next_states = set()

    for state in states:
        if symbol in state.transitions:
            next_states.add(state.transitions[symbol])

    return frozenset(next_states)

def nfa_to_dfa(nfa, alphabet):
    start_closure = epsilon_closure({nfa.start_state})  # Pasar como conjunto de un solo elemento
    dfa = DFA()
    dfa.states.append(start_closure)
    dfa.start_state = start_closure

    unmarked_states = [start_closure]
    dfa_state_map = {start_closure: 0}
    dfa.accept_states = []

    while unmarked_states:
        current_set = unmarked_states.pop()

        if any(state.is_accept for state in current_set):
            dfa.accept_states.append(current_set)

        for symbol in alphabet:
            next_set = epsilon_closure(move(current_set, symbol))

            if next_set and next_set not in dfa_state_map:
                dfa.states.append(next_set)
                dfa_state_map[next_set] = len(dfa.states) - 1
                unmarked_states.append(next_set)

            if next_set:
                dfa.transitions[(current_set, symbol)] = next_set

    return dfa
