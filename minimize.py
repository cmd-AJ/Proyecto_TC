import json
import pandas

class minimize_dfa:
    def __init__(self, path):
        f = open(path)
        data = json.load(f)
        Q = data["ESTADOS"]
        sigma = data["SIMBOLOS"]
        q0 = data["INICIO"]
        F = data["ACEPTACION"]
        FUNC = data["TRANSICIONES"]
        f.close()

        mydict = {}
        reverse_dict = {}

        asciicode = 65
        for i in Q:
            mydict[chr(asciicode)] = i
            reverse_dict[i] = chr(asciicode)
            asciicode += 1

        self.diccionario = mydict
        self.reverse_dic = reverse_dict
        self.estados = Q
        self.transitiones = FUNC
        self.simbolos = sigma
        self.acceptacion = F
        self.inicio = q0
        self.statesLetters = Q
        self.letteraccept = F
        self.inicial = q0

        # Tabla de transiciones para el AFD
        self.df_transition = None

    def convertir_subconjuntos_a_letras(self):
        listaacpet = []
        for i in self.acceptacion:
            listaacpet.append(self.reverse_dic[i])

        listainicial = []
        for i in self.inicial:
            listainicial.append(self.reverse_dic[i])

        lista_transisiones = []
        for i in self.transitiones:
            lista = i.split('->')
            lista[0] = self.reverse_dic[lista[0]]
            lista[2] = self.reverse_dic[lista[2]]
            lista_transisiones.append(lista[0] + ',' + lista[1] + ',' + lista[2])

        self.letteraccept = listaacpet
        self.inicial = listainicial
        self.transitiones = lista_transisiones
        self.statesLetters = sorted(set(self.reverse_dic.values()))

    def convertir_letras_a_subconjuntos(self):
        listaacpet = []
        for i in self.acceptacion:
            listaacpet.append(self.diccionario[i])

        listainicial = []
        for i in self.inicial:
            listaacpet.append(self.diccionario[i])

        lista_transisiones = []
        for i in self.transitiones:
            lista = i.split(',')
            lista[0] = self.diccionario[lista[0]]
            lista[2] = self.diccionario[lista[2]]
            lista_transisiones.append(lista[0] + ',' + lista[1] + ',' + lista[2])

        self.letteraccept = listaacpet
        self.inicial = listainicial
        self.transitiones = lista_transisiones
        self.statesLetters = sorted(set(self.diccionario.values()))

    def tabla_subcon(self):
        headers = list(self.simbolos)
        headers = [str(item) for item in headers]

        headers.append('salida')
        emptydata = {'Estados': self.statesLetters}
        for e in headers:
            emptydata[e] = ['0'] * len(self.statesLetters)
        df = pandas.DataFrame(emptydata, index=list(self.statesLetters), columns=headers)

        # Aceptacion
        for k in self.letteraccept:
            s = ''
            if k in self.inicial:
                s = '--> '
            else:
                s = ''
            df.loc[k, 'salida'] = s + str(1)
        for k in self.inicial:
            df.loc[k, 'salida'] = '--> ' + df.loc[k, 'salida']

        for k in self.transitiones:
            k = k.split(',')
            df.loc[str(k[0]), str(k[1])] = str(k[2])

        hasnnul = False
        for e in headers:
            for i in self.statesLetters:
                if df.loc[i, e] == '0' and (e != 'salida'):
                    df.loc[i, e] = 'QT'
                    hasnnul = True

        if hasnnul:
            dictionary = {key: ['QT'] for key in headers}
            dictionary['salida'] = ['0']
            nullrow = pandas.DataFrame(dictionary, index=['QT'])
            df = pandas.concat([df, nullrow])
            self.statesLetters.append('QT')

        self.df_transition = df  # Guardar la tabla de transiciones para su uso posterior

        return df

    def minimizacion_tabla(self):
        indexing = list(self.statesLetters)

        # Incluir el estado QT en la tabla de minimización
        columns = []
        contador = 1
        while contador < len(indexing):
            columns.append(indexing[len(indexing) - contador])
            contador += 1

        emptydata = {'Estados': indexing}
        for i in columns:
            emptydata[i] = [''] * len(indexing)

        df = pandas.DataFrame(emptydata, index=indexing, columns=columns)

        # Empezamos a llenar la tabla de minimización solo en la parte superior
        for estado_i in df.index:
            for estado_j in df.columns:
                if estado_j is not None and estado_i != estado_j and indexing.index(estado_i) < indexing.index(estado_j):
                    if self.son_no_equivalentes(estado_i, estado_j):
                        df.loc[estado_i, estado_j] = 'X'

        return df

    def son_no_equivalentes(self, estado1, estado2):
        """
        Esta función determina si dos estados no son equivalentes
        basado en las transiciones y los estados de aceptación.
        """
        es_acept1 = estado1 in self.letteraccept
        es_acept2 = estado2 in self.letteraccept

        if es_acept1 != es_acept2:
            return True

        for simbolo in self.simbolos:
            trans1 = self.obtener_transicion(estado1, simbolo)
            trans2 = self.obtener_transicion(estado2, simbolo)
            if trans1 != trans2:
                return True

        return False

    def obtener_transicion(self, estado, simbolo):
        try:
            return self.df_transition.loc[estado, simbolo]
        except KeyError:
            return None


# Cargar y crear el AFD
s = minimize_dfa('dfa.json')
s.convertir_subconjuntos_a_letras()

# Imprime la tabla del AFD
print(f"\033[1;32;40m Tabla del AFD\033[0m")
print(s.tabla_subcon())

print('\n')

# Imprime la tabla de minimización
print(f"\033[1;34;40m Tabla de minimización\033[0m")
print(s.minimizacion_tabla())



#Tarea para KOU
# Llenado de tablas de la minimizacion

#DOCUMENTO PARA LEER 
# https://pfafner.github.io/tc2024/aulas/Aula09.pdf



# funcion df.loc[ fila, columna ] 
#Ejemplos de uso 
        # df.loc['A', 'C'] te va dar el valor de del espacio
        

#Hacer Si encuentra una pareja en las columnas 0 o 1 de la primera tabla
#Por lo tanto necesita recorrer la primera fila y la segunda fila de la columna 0 por ejemplo
#Si lo encuentra que lo ponga el simbolo 'X'  que significa que ya paso