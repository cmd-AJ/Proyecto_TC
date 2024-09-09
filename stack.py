
class estack:
    
#Inicializa el stack
    def __init__(self):
        #Lista como un stack
        self.lista = [] 
        #El valor a quitar y poner
        self.value = ""   
        #Si el valor es true entonces no hay más parentesis
        self.parenthesis = True
        self.setdeparentesis = [  ]

        
    #Quita cada elemento
    def poplista( self ):
        self.lista.pop()
        
    def keepvalue(self, element:str):
        self.value = element
    
    def getvalue(self):
        return self.value 
        
    def peek(self):
        try:
            return self.lista[len(self.lista)-1]
        except: 
            return True
        
    #Ingresa todos los elementos de la cadena w
    def push( self, digit :str ): # w es la cadena
        self.lista.append(digit)
            
    #Si la cadena tiene parentesis entonces tiene que retornar vacio si ya no hay nada.     
    def verificar(self):
        if self.setdeparentesis == [] :
            print("esta vacio")
            
    def getstack(self):
        return self.lista
    
    def limpiarstack(self):
        self.lista = []
            


def regexp_a_postfix(expression):
    def precedence(op):
        precedences = {'|': 1, '•': 2, '*': 3, '+': 3, '?': 3}
        return precedences.get(op, 0)

    def is_operator(c):
        return c in {'|', '•', '*', '+', '?'}

    output = []
    operator_stack = []

    # Formatear expresión para manejar la concatenación implícita
    formatted_expression = ""
    for i in range(len(expression)):
        c1 = expression[i]
        formatted_expression += c1

        # Agregar operador de concatenación explícito (•) si corresponde
        if i + 1 < len(expression):
            c2 = expression[i + 1]
            if (c1 not in "|(" and c2 not in "|)*+?"):
                formatted_expression += "•"

    for char in formatted_expression:
        if char.isalnum():  # Si es un símbolo alfanumérico
            output.append(char)
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Eliminar el '(' del stack
        elif is_operator(char):
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence(operator_stack[-1]) >= precedence(char)):
                output.append(operator_stack.pop())
            operator_stack.append(char)

    # Vaciar el resto del stack de operadores
    while operator_stack:
        output.append(operator_stack.pop())

    return ''.join(output)



def list_to_exp(lista):
    exp = ''
    for i in lista:
        exp = exp + str(i)
    
    return exp

