
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
            

lenguaje = '(b|b)*abb(a|b)*'
    
token = set('(b|b)*abb(a|b)*')
operations = set( '+*|' )
parenthesis = set( '()')
tr = token - operations - parenthesis

operator_stack = estack()
output_stack = estack()

def regexp_a_postfix(expresion):
    print("Regexp a Postfix")
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
        

    for e in operator_stack.getstack():
        if e != "(":
            output_stack.push(i)

            
regexp_a_postfix(lenguaje)

operator_stack.limpiarstack()

#Regexp a postfix
print(output_stack.getstack())


print(tr)

pr = []


trdict = {key: 0 for key in tr}

for li in lenguaje:

    for k in tr:
        if(k == li):
            trdict[k] = trdict[k] + 1
            li = li + str(trdict[k])
        
    pr.append(li)



##VALORES Iniciales EMPIEZAN AQUI


inicial = True

contador = 0
after_val = True
count_parenthesis = 0


prinicial = estack()

while inicial:
    #Si es una letra entonces hay dos casos si a la derecha hay un operador entonces no termina el inicial
    if  list(pr[contador])[0] in tr:
        after_val = True
        try:
            #operacion son +*|
            if list(pr[contador+1])[0] == '|':
                prinicial.push(pr[contador])
            if list(pr[contador+1])[0] == '*':
                after_val = False
                prinicial.push(pr[contador])
            if list(pr[contador+1])[0] == '+':
                inicial = False
                after_val = False
                prinicial.push(pr[contador])
            if list(pr[contador+1])[0] == ')' and list(pr[contador+2])[0] == '*':
                prinicial.push(pr[contador])
            if list(pr[contador+1])[0] == ')' and list(pr[contador+2])[0] == '+':
                prinicial.push(pr[contador])
                inicial = False

            elif count_parenthesis == 0:
                if after_val:
                    prinicial.push(pr[contador])
                    inicial = False
        except:
            print("No existe said operacion")
            inicial = False
    if list(pr[contador])[0] in parenthesis:
        
        if list(pr[contador])[0] == '(':
            count_parenthesis = count_parenthesis + 1
        if list(pr[contador])[0] == ')':
            count_parenthesis = count_parenthesis - 1
    contador += 1
        
print('valores', prinicial.getstack())

##VALORES FINALES EMPIEZAN AQUI
        
print(pr)


prfinal = estack()

for i in pr:
    prfinal.push(i)
    
estado = True
while estado:
    for e in prfinal.getstack():
        if prfinal.peek() == '*':
            print()


