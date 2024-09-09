
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
            

def list_to_exp(lista):
    exp = ''
    for i in lista:
        exp = exp + str(i)
    
    return exp




def regexp_a_postfix_v2(expresion  , output_stack):
    operator_stack = estack()
    token = set(expresion)
    operations = set( '+*|' )
    parenthesis = set( '()')
    tr = token - operations - parenthesis
    
    contador = 0
    previusval = 0 # parentesis
    parentesislocation = []
    partof_expression = []
    for i in expresion:
        if( i == '(' ):
            parentesislocation.append(contador)   
            previusval += 1 
        if(i == ')'):
            exp = ''
            for i in range(parentesislocation[len(parentesislocation)-1], contador+1):
                exp = exp + list(expresion)[i] 
            try:
                if list(expresion)[i+1] == '*':
                    exp = exp + '*'
            except:
                None
            
            partof_expression.append(exp)
            parentesislocation.pop()
            previusval -= 1   
        
        if( previusval == 0 ) and ( i in tr ):
            exp = i
            try:
                if list(expresion)[contador+1] == '*':
                    exp = exp + '*'
            except:
                None
            
            partof_expression.append(exp)
            
        contador += 1
            
    operatorstack = []
    letterstack = []
    for i in partof_expression:
        for e in i:
            if e in tr:
                letterstack.append(e)
            if e in operations:
                operatorstack.append(e)
        
        output_stack.push(list_to_exp(letterstack + operatorstack))
        letterstack = []
        operatorstack = []
    
    output = ''
    for e in range( len(output_stack.getstack()) ):
        if e != 0:
            output = output + output_stack.getstack()[e] + '•'
        else:
            output = output + output_stack.getstack()[e]
    
        
        
   
   
    return output