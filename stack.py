
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
            






def regexp_a_postfix(expresion  , output_stack):
    operator_stack = estack()
    token = set(expresion)
    operations = set( '+*|' )
    parenthesis = set( '()')
    tr = token - operations - parenthesis
    for i in expresion:
        # operador
        if (operator_stack.getvalue()+i == ')+') or (operator_stack.getvalue()+i == ')*'):
            output_stack.push(i)
            i = 'null'
            operator_stack.keepvalue('')
            
        if (operator_stack.getvalue() in tr) and (i in tr) and (operator_stack.peek() != '|'):
            output_stack.push('•')
            operator_stack.keepvalue('')

        if i == '(' :
            operator_stack.push(i)
        elif i in tr:
            output_stack.push(i) 
            operator_stack.keepvalue(i)
        elif i in operations:
            if (i != '|'):
                output_stack.push(str(i))
            else:
                operator_stack.push(str(i))
            
        elif i == ")":
            operador = operator_stack.peek()
            operator_stack.poplista()
            output_stack.push(operador)
            operator_stack.keepvalue(')')
        
    if (list(expresion)[len(expresion)-1] == '*' and list(expresion)[len(expresion)-2] in tr ) or list(expresion)[len(expresion)-1] in tr :
        output_stack.push('•')
        

    for e in operator_stack.getstack():
        if e != "(":
            output_stack.push(i)
    
    operator_stack.limpiarstack()
    return output_stack


def list_to_exp(lista):
    exp = ''
    for i in lista:
        exp = exp + str(i)
    
    return exp

