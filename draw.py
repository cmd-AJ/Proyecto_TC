import json
import graphviz

def drawing_grapgh(path:str):

    with open(path, 'r') as file:
            data = json.load(file)

    dot = graphviz.Digraph(comment='DFA')


    for state in data['ESTADOS']:

        dot.node(state, shape='circle')

    # Add edges to the graph
    for transition in data['TRANSICIONES']:
        # Split transition details
        parts = transition.split('->')
        state_from = parts[0]
        symbol = parts[1]
        state_to = parts[2]  

        
        dot.edge(state_from, state_to, label=symbol)

    
    for start_state in data['INICIO']:
        dot.node(start_state, shape='ellipse', style='bold')

    for accept_state in data['ACEPTACION']:
        dot.node(accept_state, shape='doublecircle')
    dot.render(('dfa_graph'+ path) , format='png')
    dot.view()