# dfa.py
class DFA:
    def __init__(self):
        self.states = []
        self.start_state = None
        self.accept_states = []
        self.transitions = {}  # {(frozenset(state), symbol): frozenset(next_state)}

def epsilon_closure(state):
    """ Compute the epsilon closure of a single state """
    stack = [state]
    closure = {state}

    while stack:
        current_state = stack.pop()
        for next_state in current_state.epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return frozenset(closure)  # Return frozenset to make it hashable

def move(states, symbol):
    """ Compute the move of a set of states on a given symbol """
    next_states = set()

    for state in states:
        if symbol in state.transitions:
            next_states.add(state.transitions[symbol])

    return frozenset(next_states)  # Return frozenset to make it hashable

def nfa_to_dfa(nfa, alphabet):
    start_closure = epsilon_closure(nfa.start_state)
    dfa = DFA()
    dfa.states.append(start_closure)
    dfa.start_state = start_closure

    unmarked_states = [start_closure]
    dfa_state_map = {frozenset(start_closure): 0}  # Use frozenset as key
    dfa.accept_states = []

    while unmarked_states:
        current_set = unmarked_states.pop()

        # Check if this set contains an accepting state
        if any(state.is_accept for state in current_set):
            dfa.accept_states.append(current_set)

        for symbol in alphabet:
            next_set = epsilon_closure(move(current_set, symbol))

            if next_set and frozenset(next_set) not in dfa_state_map:
                dfa.states.append(next_set)
                dfa_state_map[frozenset(next_set)] = len(dfa.states) - 1
                unmarked_states.append(next_set)

            if next_set:
                dfa.transitions[(frozenset(current_set), symbol)] = frozenset(next_set)

    return dfa
