from graphviz import Graph
import pygraphviz as pgv
from collections import deque, defaultdict
import string


def get_precedencia(c):
    precedencia = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5
    }
    return precedencia.get(c, 6)

def balanceo(cadena):
    cadena = cadena.replace(' ', '')
    stack = []
    for char in cadena:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if stack and ((char == ')' and stack[-1] == '(') or
                          (char == '}' and stack[-1] == '{') or
                          (char == ']' and stack[-1] == '[')):
                stack.pop()
            else:
                stack.append(char)
                break
    return len(stack) == 0

def formatear(regex):
    regex = regex.replace(' ', '')
    todos_operadores = ['|', '?', '+', '*', '^']
    operadores_binarios = ['^', '|']
    res = ""

    i = 0
    while i < len(regex):
        c1 = regex[i]
        
        if c1 == '%' and i + 1 < len(regex):
            c1 = regex[i + 1]
            i += 1  
            
            if c1 in '()' and i + 1 < len(regex):
                res += c1 + '.'
                i += 1
                continue

        if i + 1 < len(regex):
            c2 = regex[i + 1]
            res += c1

            if c1 not in todos_operadores and c2 in todos_operadores and c2 not in operadores_binarios:
                i += 1
                continue
            if c1 in todos_operadores and c1 not in operadores_binarios and c2 == ')':
                i += 1
                continue
            if c1 == ')' and c2 in todos_operadores and c2 not in operadores_binarios:
                i += 1
                continue
            if (c1 not in operadores_binarios and c2 not in todos_operadores and c1 != '(' and c2 != ')') or \
               (c1 in todos_operadores and c1 not in operadores_binarios and c2 not in todos_operadores) or \
               (c1 == '(' and c2 == ')'):
                res += '.'
        else:
            res += c1

        i += 1

    res = res.replace('%', '')
    return res




def caracteres_escapados(cadena):
    cadena = cadena.replace(' ', '')
    nueva_cadena = ''
    escape = False
    for char in cadena:
        if escape:
            nueva_cadena += '%' + char  
            escape = False
        else:
            if char == '\\':
                escape = True  
            else:
                nueva_cadena += char  
    return nueva_cadena



def equivalencia(cadena):
    cadena = cadena.replace(' ', '')
    lista = [char for char in cadena]
    
    minusculas = list(string.ascii_lowercase)
    mayusculas = list(string.ascii_uppercase)
    numeros = list(string.digits)
    
    i = 0
    while i < len(lista):
        char = lista[i]
        match char:
            case '?':
                lista[i] = '|' + 'ε'
            case '+':
                if i > 0:
                    if lista[i - 1] in [']', ')', '}']:
                        start = i - 1
                        stack = [lista[start]]
                        while start > 0 and stack:
                            start -= 1
                            if lista[start] in [']', ')', '}']:
                                stack.append(lista[start])
                            elif lista[start] in ['[', '(', '{']:
                                stack.pop()
                        if not stack:
                            sub_expr = ''.join(lista[start:i])
                            lista[i] = sub_expr + '*'
                    else:
                        lista[i] = lista[i - 1] + '*'
            case '[':
                j = i + 1
                while j < len(lista) and lista[j] != ']':
                    j += 1
                if j < len(lista) and lista[j] == ']':
                    contenido = lista[i+1:j]
                    sub_expr = []
                    k = 0
                    while k < len(contenido):
                        if k + 2 < len(contenido) and contenido[k+1] == '-':
                            char_i = contenido[k]
                            char_f = contenido[k+2]
                            if char_i in minusculas and char_f in minusculas:
                                sub_expr.extend(minusculas[minusculas.index(char_i):minusculas.index(char_f)+1])
                            elif char_i in mayusculas and char_f in mayusculas:
                                sub_expr.extend(mayusculas[mayusculas.index(char_i):mayusculas.index(char_f)+1])
                            elif char_i in numeros and char_f in numeros:
                                sub_expr.extend(numeros[numeros.index(char_i):numeros.index(char_f)+1])
                            k += 3  
                        else:
                            sub_expr.append(contenido[k])
                            k += 1
                    
                    lista[i] = f"{'|'.join(sub_expr)}"
                    del lista[i+1:j+1]  
                    i += len(sub_expr)  
                else:
                    i = j  
        
        i += 1

    cadena = ''.join(lista)
    return cadena

def infix_a_postfix():
    expresiones_a_postfix = []
    with open('regex.txt') as archivo:
        for linea in archivo:
            cadena = linea.strip()
            cadena += '#'  

            cadena = caracteres_escapados(cadena)
            if linea != cadena:
                cadena = equivalencia(cadena)
                if not balanceo(cadena):
                    return 'La cadena no está balanceada'
                
                cadena = formatear(cadena)
                
                postfix = ''
                stack = []
                operadores = ['|', '.', '?', '*', '+', '^']
                
                for i, char in enumerate(cadena):
                    if char in '()' and (
                        (i > 0 and cadena[i - 1] == '.') or
                        (i < len(cadena) - 1 and cadena[i + 1] == '.')
                    ):
                        postfix += char  
                        continue  
                    
                    if char == '(':
                        stack.append(char)
                    elif char == ')':
                        while stack and stack[-1] != '(':
                            postfix += stack.pop()
                        if stack:
                            stack.pop()
                    else:
                        while stack and get_precedencia(stack[-1]) >= get_precedencia(char):
                            postfix += stack.pop()
                        stack.append(char)

                while len(stack) > 0:
                    postfix += stack.pop()

                expresiones_a_postfix.append(postfix)

            else: 
                cadena = equivalencia(cadena)
                if not balanceo(cadena):
                    return 'La cadena no está balanceada'
                
                cadena = formatear(cadena)
                postfix = ''
                stack = []
                operadores = ['|', '.', '?', '*', '+', '^']
                
                for char in cadena:
                    if char == '(':
                        stack.append(char)
                    elif char == ')':
                        while stack and stack[-1] != '(':
                            postfix += stack.pop()
                        if stack:
                            stack.pop()
                    else:
                        while stack and get_precedencia(stack[-1]) >= get_precedencia(char):
                            postfix += stack.pop()
                        stack.append(char)
                
                while len(stack) > 0:
                    postfix += stack.pop()
                
                expresiones_a_postfix.append(postfix)
    
    return expresiones_a_postfix

class Nodo:
    contador_posicion = 1  

    def __init__(self, valor, anulable=None, posicion=None):
        self.valor = valor
        self.posicion = posicion if valor not in ['|', '.', '*', '+', '?'] else None  
        self.primeraPos = {self.posicion} if self.posicion is not None else set() 
        self.ultimaPos = {self.posicion} if self.posicion is not None else set() 

        if anulable is None:
            self.anulable = (valor == 'ε')  
        else:
            self.anulable = anulable

        self.nodo_id = None  

    def __repr__(self):
        return f"Nodo(valor={self.valor}, posicion={self.posicion}, primeraPos={self.primeraPos}, ultimaPos={self.ultimaPos}, anulable={self.anulable})"

class NodoBinario(Nodo):
    def __init__(self, valor, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
        
        if valor == '|': 
            anulable = izquierda.anulable or derecha.anulable  
            primeraPos = izquierda.primeraPos.union(derecha.primeraPos)
            ultimaPos = izquierda.ultimaPos.union(derecha.ultimaPos)    
        elif valor == '.':  
            anulable = izquierda.anulable and derecha.anulable  
            primeraPos = izquierda.primeraPos if not izquierda.anulable else izquierda.primeraPos.union(derecha.primeraPos)
            
            if derecha.anulable:
                ultimaPos = izquierda.ultimaPos.union(derecha.ultimaPos)
            else:
                ultimaPos = derecha.ultimaPos  

        super().__init__(valor, anulable, None)  
        self.primeraPos = primeraPos  
        self.ultimaPos = ultimaPos 

    def __repr__(self):
        return f"NodoBinario(valor={self.valor}, primeraPos={self.primeraPos}, ultimaPos={self.ultimaPos}, anulable={self.anulable})"

class NodoUnario(Nodo):
    def __init__(self, valor, operando):
        self.operando = operando
        
        if valor == '*':  
            anulable = True
        elif valor == '+':  
            anulable = operando.anulable
        elif valor == '?':  
            anulable = True

        primeraPos = operando.primeraPos 
        ultimaPos = operando.ultimaPos  

        super().__init__(valor, anulable, None)  
        self.primeraPos = primeraPos  
        self.ultimaPos = ultimaPos   

    def __repr__(self):
        return f"NodoUnario(valor={self.valor}, primeraPos={self.primeraPos}, ultimaPos={self.ultimaPos}, anulable={self.anulable})"

def construir_arbol(expresion_postfix):
    stack = []
    operadores_binarios = ['|', '.']
    operadores_unarios = ['*', '+', '?']

    for char in expresion_postfix:
        if char in operadores_binarios:
            if len(stack) >= 2:
                derecha = stack.pop()
                izquierda = stack.pop()
                nodo_binario = NodoBinario(char, izquierda, derecha)
                stack.append(nodo_binario)
        elif char in operadores_unarios:
            if len(stack) >= 1:
                operando = stack.pop()
                nodo_unario = NodoUnario(char, operando)
                stack.append(nodo_unario)
        else:
            posicion = Nodo.contador_posicion if char != 'ε' else None
            if char != 'ε':
                Nodo.contador_posicion += 1
            stack.append(Nodo(char, posicion=posicion))  

    return stack.pop() if stack else None  

def agregar_nodo(dot, nodo, nodo_id, siguientePos):
    if isinstance(nodo, NodoBinario):
        operador_id = nodo_id + '_operador'
        izquierda_id = nodo_id + '_izquierda'
        derecha_id = nodo_id + '_derecha'
        dot.node(operador_id, f'{nodo.valor}\nAnulable: {nodo.anulable}\nPrimeraPos: {nodo.primeraPos}\nUltimaPos: {nodo.ultimaPos}')
        dot.edge(operador_id, agregar_nodo(dot, nodo.izquierda, izquierda_id, siguientePos))
        dot.edge(operador_id, agregar_nodo(dot, nodo.derecha, derecha_id, siguientePos))
        return operador_id
    elif isinstance(nodo, NodoUnario):
        operador_id = nodo_id + '_operador'
        operando_id = nodo_id + '_operando'
        dot.node(operador_id, f'{nodo.valor}\nAnulable: {nodo.anulable}\nPrimeraPos: {nodo.primeraPos}\nUltimaPos: {nodo.ultimaPos}')
        dot.edge(operador_id, agregar_nodo(dot, nodo.operando, operando_id, siguientePos))
        return operador_id
    else:
        hoja_id = f'{nodo_id}_hoja'
        nodo.nodo_id = hoja_id  
        siguiente = siguientePos.get(nodo.posicion, set())
        siguiente_str = f'{siguiente}' if siguiente else '{}'  
        dot.node(hoja_id, f'{nodo.valor}\nAnulable: {nodo.anulable}\nPos: {nodo.posicion}\nPrimeraPos: {nodo.primeraPos}\nUltimaPos: {nodo.ultimaPos}\nSiguientePos: {siguiente_str}')
        return hoja_id

def calcular_siguiente_pos(raiz):
    siguientePos = defaultdict(set)

    def recorrer_nodo(nodo):
        if isinstance(nodo, NodoBinario):
            recorrer_nodo(nodo.izquierda)
            recorrer_nodo(nodo.derecha)

            if nodo.valor == '.':  
                for pos in nodo.izquierda.ultimaPos:
                    siguientePos[pos].update(nodo.derecha.primeraPos)

        elif isinstance(nodo, NodoUnario):
            recorrer_nodo(nodo.operando)

            if nodo.valor == '*':  
                for pos in nodo.ultimaPos:
                    siguientePos[pos].update(nodo.primeraPos)

    recorrer_nodo(raiz)
    return siguientePos

def grafo(expresion_postfix, nombre_archivo):
    dot = Graph()
    nodo_id = 0

    def nuevo_nodo_id():
        nonlocal nodo_id
        nodo_id += 1
        return f'n{nodo_id}'
    
    raiz = construir_arbol(expresion_postfix)
    if raiz:
        siguientePos = calcular_siguiente_pos(raiz)  
        agregar_nodo(dot, raiz, nuevo_nodo_id(), siguientePos)

    dot.render(nombre_archivo, format='png', view=True)
    dot.save(f'{nombre_archivo}.dot')

    print(f"Anulabilidad de la expresión '{expresion_postfix}': {raiz.anulable}")
    print(f"PrimeraPos de la raíz: {raiz.primeraPos}")
    print(f"UltimaPos de la raíz: {raiz.ultimaPos}")
    print('---------\n')

def construir_dfa(raiz, expresion):
    Dstates = []
    simbolos_pos = {}  
    
    def obtener_simbolos(nodo):
        if isinstance(nodo, (NodoBinario, NodoUnario)):
            if isinstance(nodo, NodoBinario):
                obtener_simbolos(nodo.izquierda)
                obtener_simbolos(nodo.derecha)
            else:
                obtener_simbolos(nodo.operando)
        elif nodo.posicion is not None:
            simbolos_pos[nodo.posicion] = nodo.valor
    
    obtener_simbolos(raiz)
    siguientePos = calcular_siguiente_pos(raiz)
    
    estado_inicial = frozenset(raiz.primeraPos)
    Dstates.append(estado_inicial)
    estados_marcados = set()
    
    simbolos = set(v for k, v in simbolos_pos.items() if v != '#')
    
    transiciones = {}
    
    while len(estados_marcados) < len(Dstates):
        estado_actual = next(iter(set(Dstates) - estados_marcados))
        estados_marcados.add(estado_actual)
        
        for simbolo in simbolos:
            pos_simbolo = {pos for pos, sym in simbolos_pos.items() if sym == simbolo}
            
            U = set()
            for pos in estado_actual:
                if pos in pos_simbolo:
                    U.update(siguientePos.get(pos, set()))
            
            if U:  
                U = frozenset(U)
                if U not in Dstates:
                    Dstates.append(U)
                
                transiciones[(estado_actual, simbolo)] = U
    
    pos_aceptacion = max(simbolos_pos.keys()) 
    estados_finales = [estado for estado in Dstates if pos_aceptacion in estado]
    
    return {
        'estados': Dstates,
        'estado_inicial': estado_inicial,
        'estados_finales': estados_finales,
        'transiciones': transiciones,
        'simbolos': simbolos_pos
    }

def visualizar_dfa(dfa, nombre_archivo):
    dot = pgv.AGraph(directed=True)
    
    estado_a_nombre = {estado: f'q{i}' for i, estado in enumerate(dfa['estados'])}
    
    for estado in dfa['estados']:
        attrs = {'shape': 'circle'}
        if estado == dfa['estado_inicial']:
            attrs['style'] = 'bold'
        if estado in dfa['estados_finales']:
            attrs['shape'] = 'doublecircle'
        dot.add_node(estado_a_nombre[estado], **attrs)
    
    for (origen, simbolo), destino in dfa['transiciones'].items():
        dot.add_edge(estado_a_nombre[origen], estado_a_nombre[destino], label=simbolo)
    
    dot.layout(prog='dot')
    dot.draw(f'{nombre_archivo}.png')
    
def procesar_expresion(expresion_postfix, nombre_archivo):
    Nodo.contador_posicion = 1
    
    raiz = construir_arbol(expresion_postfix)
    if not raiz:
        return None
        
    print(f"Anulabilidad de la expresión '{expresion_postfix}': {raiz.anulable}")
    print(f"PrimeraPos de la raíz: {raiz.primeraPos}")
    print(f"UltimaPos de la raíz: {raiz.ultimaPos}")
    print('---------\n')
    
    dot = Graph()
    siguientePos = calcular_siguiente_pos(raiz)
    agregar_nodo(dot, raiz, 'n1', siguientePos)
    dot.render(f'grafo_no_dirigido_{nombre_archivo}', format='png', view=True)
    dot.save(f'grafo_no_dirigido_{nombre_archivo}.dot')
    
    dfa = construir_dfa(raiz, expresion_postfix)
    
    visualizar_dfa(dfa, f'dfa_{nombre_archivo}')
    
    return dfa

expresiones_postfix = infix_a_postfix()
if expresiones_postfix != 'La cadena no está balanceada':
    for i, cadena in enumerate(expresiones_postfix):
        print(f'Analizando la expresión {cadena}\n')
        dfa = procesar_expresion(cadena, f'expresion_{i}')