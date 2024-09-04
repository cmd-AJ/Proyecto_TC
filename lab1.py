
import pandas as pd
import json
import time

path =input("Archivo .json\n")
#lab2.json o # lab2problema.json

f = open(path)

data = json.load(f)
Q = data["Q"]
sigma = data["sigma"]
q0 = data["q0"]
F = data["F"]
FUNC = data["FUNC"]
f.close()

priority_map = {key: index for index, key in enumerate(Q)}

def sort_key(item):
    first_part = item.split(',')[0]  # Extract the first part before the comma
    priority_level = priority_map.get(first_part, len(Q))  # Get priority level
    return (priority_level, item)  # Return tuple for sorting


sorted_list = sorted(FUNC, key=sort_key)
headers = sorted(set(sigma) - set(Q))  # Calculate headers
array = [[None for _ in range(len(headers))] for _ in range(len(Q))]
i = 0
while i <= len(Q):
    for a in sorted_list:
        s = a.split(',')
        if i == priority_map[s[0]]:
            array[i][int(s[1])] = s[2]
    i += 1
lenght = 0

for i in F:
    array[int(priority_map[i])].append(1)
    lenght = len(array[int(priority_map[i])])
    
for e in array:
    if len(e) < lenght:
        e.append(0)
        
headers.append('salida')
df = pd.DataFrame(array, index=Q, columns=headers)
for i  in Q:
    df.loc[i, 0] = "{ "+ df.loc[i, 0] + " }"
    df.loc[i, 1] = "{ "+ df.loc[i, 1] + " }"

def transition(q,a,FUNC):
    print("Tabla AFN")
    print(FUNC)
    print("q′ = δ(" + str(q) + ", "+ str(a) +") = " + FUNC.loc[q, a])

finalestado = None
#la cual devuelve el estado q obtenido por el aut´omata despu´es de terminar de leer la cadena w ∈ Σ∗.
def final_state(q, word, FUNC):
    # Accept the dictionary
    if len(word) > 0:
        a = int(word[0])
        if "{" in q:
            q = q.split(" ")
            q = q[1]
        
        q = FUNC.loc[q, int(a)]  # Access the DataFrame correctly
        return final_state(q, word[1:], FUNC)  # Recurse with the rest of the word
    else:
        return q  # Base case: return the final state

def derivacion(q,w,FUNC):
    stacku = []
    number = 1
    for i in list(w):
        a = int(i)
        if "{" in q:
            q = q.split(" ")
            q = q[1]
        stacku.append("q_" + str(number) +" = δ(" + str(q) + ", "+ str(a) +") = " + FUNC.loc[q, int(a)])
        q = FUNC.loc[q, int(a)]  # Access the DataFrame correctly
        number = number + 1
    
    for i in stacku[::-1]:
        print(i)

def accepted(q,w,F,FUNC):
    boleanus = False
    estado = final_state(q,w,FUNC)
    for i in F:
        if i in estado:
            boleanus = True
    return boleanus

menu = False
while menu == False:
    print("Leyendo lab2.json....")
    print(df)
    print("1.Funcion de transición")
    print("2.Obtener estado final")
    print("3.Obtener la derivacion")
    print("4.Cadena acceptada")
    print("5.Salir")
    opcion = input("Opcion: ")
    if opcion == "1":
        print("la caracteres validos ", (set(sigma)))
        estado = input("Ingresa el estado: ")
        wording = input("Ingresa el caracter: ")
        try:
            transition(estado, int(wording), df )
            time.sleep(5)
        except:
            print("Cadena invalida")
    if opcion == "2":
        print("la cadena solo acepta ", (set(sigma) - set(Q)))
        wording = input("Ingresa la cadena: ")
        try:
            print(final_state(q0, wording, df ))   
            time.sleep(5)
        except:
            print("Cadena invalida")
    if opcion == "3":
        print("la cadena solo acepta ", (set(sigma) - set(Q)))
        wording = input("Ingresa la cadena: ")
        try:
            derivacion(q0, wording, df )    
            time.sleep(5)
        except:
            print("Cadena invalida")
    if opcion == "4":
        print("la cadena solo acepta ", (set(sigma) - set(Q)))
        wording = input("Ingresa la cadena: ")
        try:
            print(accepted(q0, wording, F ,df))
            time.sleep(5)
        except:
            print("Cadena invalida")
    if opcion == "5":
        menu = True
        
        
