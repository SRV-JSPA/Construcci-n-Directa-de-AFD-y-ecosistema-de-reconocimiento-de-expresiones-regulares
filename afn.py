# Hay partes del código que fueron reutilizadas del proyecto 1 de la clase de teoría de la computación
# El código reutilizado pertenece al repositorio "Proyecto1_TC", adjunto link: https://github.com/SRV-JSPA/Proyecto1_TC.git
# El repositorio pertenece a Santiago Pereira 22318 y Gabriela Mazariegos 22513

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

def construir_afd(raiz, expresion):
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
    
def minimizar_afd(afd):
    particiones = []
    estados_no_finales = [estado for estado in afd['estados'] if estado not in afd['estados_finales']]
    if estados_no_finales:
        particiones.append(estados_no_finales)
    if afd['estados_finales']:
        particiones.append(afd['estados_finales'])


    simbolos = set(sym for pos, sym in afd['simbolos'].items() if sym != '#')

    cambio = True
    while cambio:
        cambio = False
        nuevas_particiones = []
        
        for bloque in particiones:
            particiones_temp = {}
            for estado in bloque:
                destinos = []
                for simbolo in simbolos:
                    destino = None
                    for (origen, sym), dest in afd['transiciones'].items():
                        if origen == estado and sym == simbolo:
                            destino = dest
                            break

                    if destino is not None:
                        for idx, particion in enumerate(particiones):
                            if destino in particion:
                                destinos.append((simbolo, idx))
                                break
                
                destinos_tuple = tuple(sorted(destinos))
                if destinos_tuple not in particiones_temp:
                    particiones_temp[destinos_tuple] = []
                particiones_temp[destinos_tuple].append(estado)
            
            if len(particiones_temp) > 1:
                cambio = True
                nuevas_particiones.extend(particiones_temp.values())
            else:
                nuevas_particiones.append(bloque)
        
        particiones = nuevas_particiones

    estado_a_particion = {}
    for i, particion in enumerate(particiones):
        for estado in particion:
            estado_a_particion[estado] = frozenset(particion)

    nuevos_estados = [frozenset(p) for p in particiones]
    nuevo_estado_inicial = estado_a_particion[afd['estado_inicial']]
    nuevos_estados_finales = []
    for estado_final in afd['estados_finales']:
        particion = estado_a_particion[estado_final]
        if particion not in nuevos_estados_finales:
            nuevos_estados_finales.append(particion)

    nuevas_transiciones = {}
    for particion in particiones:
        estado_repr = next(iter(particion))  
        for simbolo in simbolos:
            for (origen, sym), destino in afd['transiciones'].items():
                if origen == estado_repr and sym == simbolo:
                    nueva_origen = estado_a_particion[origen]
                    nuevo_destino = estado_a_particion[destino]
                    nuevas_transiciones[(nueva_origen, simbolo)] = nuevo_destino
                    break

    return {
        'estados': nuevos_estados,
        'estado_inicial': nuevo_estado_inicial,
        'estados_finales': nuevos_estados_finales,
        'transiciones': nuevas_transiciones,
        'simbolos': afd['simbolos']
    }

def visualizar_afd_minimizado(afd_min, nombre_archivo):
    dot = pgv.AGraph(directed=True)
    dot.graph_attr.update(rankdir='LR')
    
    estado_a_nombre = {estado: f'q{i}' for i, estado in enumerate(afd_min['estados'])}
    
    for estado in afd_min['estados']:
        attrs = {
            'shape': 'circle',
            'style': 'filled',
            'fillcolor': 'white'
        }
        if estado == afd_min['estado_inicial']:
            attrs['style'] = 'filled,bold'
        if estado in afd_min['estados_finales']:
            attrs['fillcolor'] = 'lightblue'
            attrs['shape'] = 'doublecircle'
            
        dot.add_node(estado_a_nombre[estado], **attrs)
    
    # Add edges
    for (origen, simbolo), destino in afd_min['transiciones'].items():
        dot.add_edge(estado_a_nombre[origen], estado_a_nombre[destino], label=simbolo)
    
    dot.layout(prog='dot')
    dot.draw(f'{nombre_archivo}_minimizado.png')
    dot.write(f'{nombre_archivo}_minimizado.dot')

def visualizar_afd(afd, nombre_archivo):
    dot = pgv.AGraph(directed=True)
    
    estado_a_nombre = {estado: f'q{i}' for i, estado in enumerate(afd['estados'])}
    
    for estado in afd['estados']:
        attrs = {'shape': 'circle'}
        if estado == afd['estado_inicial']:
            attrs['style'] = 'bold'
        if estado in afd['estados_finales']:
            attrs['shape'] = 'doublecircle'
        dot.add_node(estado_a_nombre[estado], **attrs)
    
    for (origen, simbolo), destino in afd['transiciones'].items():
        dot.add_edge(estado_a_nombre[origen], estado_a_nombre[destino], label=simbolo)
    
    dot.layout(prog='dot')
    dot.draw(f'{nombre_archivo}.png')
    
def simular_cadena_afd(afd, cadena, verbose=False):
    estado_actual = afd['estado_inicial']
    
    if verbose:
        print(f"\nSimulando cadena: '{cadena}'")
        print(f"Estado inicial: {estado_actual}")
    
    for i, simbolo in enumerate(cadena):
        if verbose:
            print(f"\nPaso {i + 1}:")
            print(f"  Símbolo actual: '{simbolo}'")
            print(f"  Estado actual: {estado_actual}")
        
        siguiente_estado = None
        for (origen, sim), destino in afd['transiciones'].items():
            if origen == estado_actual and sim == simbolo:
                siguiente_estado = destino
                break
        
        if siguiente_estado is None:
            if verbose:
                print(f"  No hay transición válida para '{simbolo}' desde {estado_actual}")
                print("  Cadena RECHAZADA")
            return False
        
        estado_actual = siguiente_estado
        if verbose:
            print(f"  Nuevo estado: {estado_actual}")
    
    es_aceptada = estado_actual in afd['estados_finales']
    
    if verbose:
        print("\nResultado final:")
        print(f"  Estado final: {estado_actual}")
        print(f"  Cadena {'ACEPTADA' if es_aceptada else 'RECHAZADA'}")
    
    return es_aceptada

def probar_cadenas_en_afd(afd, cadenas_prueba):
    print("\nPruebas de simulación del AFD:")
    print("-" * 50)
    for cadena in cadenas_prueba:
        resultado = simular_cadena_afd(afd, cadena, verbose=True)
        print(f"\nResumen: Cadena '{cadena}' -> {'ACEPTADA' if resultado else 'RECHAZADA'}")
        print("-" * 50)
    
def procesar_expresion(expresion_postfix, nombre_archivo, cadenas_prueba=None):
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
    
    afd = construir_afd(raiz, expresion_postfix)
    visualizar_afd(afd, f'afd_{nombre_archivo}')
    
    afd_minimizado = minimizar_afd(afd)
    visualizar_afd_minimizado(afd_minimizado, nombre_archivo)
    
    if cadenas_prueba:
        probar_cadenas_en_afd(afd_minimizado, cadenas_prueba)
    
    return afd_minimizado

def get_precedencia_afn(c):
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

def balanceo_afn(cadena):
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

def formatear_afn(regex):
    regex = regex.replace(' ', '')
    todos_operadores = ['|', '?', '+', '*', '^']
    operadores_binarios = ['^', '|']
    res = ""

    i = 0
    while i < len(regex):
        c1 = regex[i]
        
        if c1 == '#' and i + 1 < len(regex):
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

    res = res.replace('#', '')
    return res




def caracteres_escapados_afn(cadena):
    cadena = cadena.replace(' ', '')
    nueva_cadena = ''
    escape = False
    for char in cadena:
        if escape:
            nueva_cadena += '#' + char  
            escape = False
        else:
            if char == '\\':
                escape = True  
            else:
                nueva_cadena += char  
    return nueva_cadena



def equivalencia_afn(cadena):
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

def infix_a_postfix_afn():
    expresiones_a_postfix = []
    with open('regex.txt') as archivo:
        for linea in archivo:
            cadena = linea.strip()
            cadena = caracteres_escapados_afn(cadena)
            if linea != cadena:
                cadena = equivalencia_afn(cadena)
                if not balanceo_afn(cadena):
                    return 'La cadena no está balanceada'
                
                cadena = formatear_afn(cadena)
                
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
                        while stack and get_precedencia_afn(stack[-1]) >= get_precedencia_afn(char):
                            postfix += stack.pop()
                        stack.append(char)

                while len(stack) > 0:
                    postfix += stack.pop()

                expresiones_a_postfix.append(postfix)


            else: 
                cadena = equivalencia_afn(cadena)
                if not balanceo_afn(cadena):
                    return 'La cadena no está balanceada'
                
                cadena = formatear_afn(cadena)
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
                        while stack and get_precedencia_afn(stack[-1]) >= get_precedencia_afn(char):
                            postfix += stack.pop()
                        stack.append(char)
                
                while len(stack) > 0:
                    postfix += stack.pop()
                
                expresiones_a_postfix.append(postfix)
    
    return expresiones_a_postfix

class OperadoresBinarios_afn:
    def __init__(self, operador, izquierda=None, derecha=None):
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha

    def __repr__(self):
        return f"OperadoresBinarios_afn(operador={self.operador}, izquierda={self.izquierda}, derecha={self.derecha})"

class OperadoresUnarios_afn:
    def __init__(self, operador, operando=None):
        self.operador = operador
        self.operando = operando

    def __repr__(self):
        return f"OperadoresUnarios_afn(operador={self.operador}, operando={self.operando})"

def agregar_nodo_afn(dot, nodo, nodo_id):
    if isinstance(nodo, OperadoresBinarios_afn):
        operador_id = nodo_id + '_operador'
        izquierda_id = nodo_id + '_izquierda'
        derecha_id = nodo_id + '_derecha'
        dot.node(operador_id, f'{nodo.operador}')
        dot.edge(operador_id, agregar_nodo_afn(dot, nodo.izquierda, izquierda_id))
        dot.edge(operador_id, agregar_nodo_afn(dot, nodo.derecha, derecha_id))
        return operador_id
    elif isinstance(nodo, OperadoresUnarios_afn):
        operador_id = nodo_id + '_operador'
        operando_id = nodo_id + '_operando'
        dot.node(operador_id, f'{nodo.operador}')
        dot.edge(operador_id, agregar_nodo_afn(dot, nodo.operando, operando_id))
        return operador_id
    else:
        dot.node(nodo_id, f'{nodo}')
        return nodo_id

def grafo_afn(cadena, nombre_archivo):
    dot = Graph()
    stack = []
    operadores_binarios = ['|', '.']
    operadores_unarios = ['*']
    
    nodo_id = 0

    def nuevo_nodo_id_afn():
        nonlocal nodo_id
        nodo_id += 1
        return f'n{nodo_id}'
    
    for char in cadena:
        if char in operadores_binarios:
            print(f'Se encontro el caracter: {char} el cual es un operador binario')
            if len(stack) >= 2:
                derecha = stack.pop()
                izquierda = stack.pop()
                print(f'Se hace ".pop()" a "{derecha}" y "{izquierda}" que seran las ramas del arbol binario de este operador')
                nodo_binario = OperadoresBinarios_afn(char, izquierda=izquierda, derecha=derecha)
                stack.append(nodo_binario)
                print(f'Luego de armar el arbol binario para el operador: {char}, almacenamos el arbol binario en el stack\n')
                print(f'Stack al momento: {stack}\n')
        elif char in operadores_unarios:
            print(f'Se encontro el caracter: {char} el cual es un operador unario')
            if len(stack) >= 1:
                operando = stack.pop()
                print(f'Se hace ".pop()" a "{operando}" que sera la rama de este operador unario')
                nodo_unario = OperadoresUnarios_afn(char, operando)
                stack.append(nodo_unario)
                print(f'Luego de armar el arbol unario para el operador: {char}, almacenamos el arbol unario en el stack\n')
                print(f'Stack al momento: {stack}\n')
        else:
            print(f'El caracter: "{char}" no es ningun tipo de operador entonces se agrega al stack')
            stack.append(char)
            print(f'Stack al momento: {stack}\n')
        nombre_archivo_info = f'{nombre_archivo}_info'
        with open(nombre_archivo_info, 'w') as archivo:
            archivo.write(str(stack))
    

    if stack:
        agregar_nodo_afn(dot, stack.pop(), nuevo_nodo_id_afn())
    dot.render(nombre_archivo, format='png', view=True)
    dot.save(f'{nombre_archivo}.dot')
    
    
    print('---------\n')


def construir_afn_desde_arbol(grafo_afn, nodo):
    if grafo_afn.get_node(nodo).attr['label'] in ['|', '.']:
        hijos = list(grafo_afn.successors(nodo))
        izquierda = construir_afn_desde_arbol(grafo_afn, hijos[0])
        derecha = construir_afn_desde_arbol(grafo_afn, hijos[1])
        
        if grafo_afn.get_node(nodo).attr['label'] == '|':
            return union_afn(izquierda, derecha)
        elif grafo_afn.get_node(nodo).attr['label'] == '.':
            return concatenacion_afn(izquierda, derecha)

    elif grafo_afn.get_node(nodo).attr['label'] == '*':
        hijo = list(grafo_afn.successors(nodo))[0]
        operando = construir_afn_desde_arbol(grafo_afn, hijo)
        return kleene_afn(operando)

    else:
        simbolo = grafo_afn.get_node(nodo).attr['label']
        return crear_afn_basico(simbolo)

def crear_afn_basico(simbolo):
    graph = pgv.AGraph(directed=True)
    start = next(id_unico)
    end = next(id_unico)
    graph.add_node(start, label='0')
    graph.add_node(end, label='1')
    graph.add_edge(start, end, label=simbolo)
    return graph

expresiones_postfix = infix_a_postfix_afn()
if expresiones_postfix != 'La cadena no está balanceada':
    for i, cadena in enumerate(expresiones_postfix):
        print(f'Analizando la expresión {cadena}\n')
        grafo_afn(cadena, f'grafo_afn_no_dirigido_{i}')
        
def generador_id_afn():
    contador = 0
    while True:
        contador += 1
        yield f'nodo_{contador}'

id_unico = generador_id_afn()

def primero_y_ultimo_afn(grafo_afn):
    primero = None
    ultimo = None
    for node in grafo_afn.nodes():
        if grafo_afn.in_degree(node) == 0:
            primero = node
            break
    for node in grafo_afn.nodes():
        if grafo_afn.out_degree(node) == 0:
            ultimo = node
            break

    return primero, ultimo
        
def union_afn(a, b):
    graph = pgv.AGraph(directed=True)

    if isinstance(a, pgv.AGraph) and not isinstance(b, pgv.AGraph):
        mapeos = {}
        labels = {}
        nodo_u1 = next(id_unico)

        graph.add_node(nodo_u1, label='S')
        
        for node in a.nodes():
            id_unico_nodo = next(id_unico)
            label = node.attr['label'] if 'label' in node.attr else node
            mapeos[node] = id_unico_nodo
            labels[id_unico_nodo] = label
            graph.add_node(id_unico_nodo, label=label)
        for edge in a.edges():
            graph.add_edge(mapeos[edge[0]], mapeos[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')
           
        nodo_u2 = next(id_unico)
        nodo_u3 = next(id_unico)
        nodo_u4 = next(id_unico) 
        graph.add_node(nodo_u2, label='P')
        graph.add_node(nodo_u3, label='O')
        graph.add_node(nodo_u4, label='T')

        primer_nodo, ultimo_nodo = primero_y_ultimo_afn(a)
        primer_nodo = mapeos[primer_nodo]
        ultimo_nodo = mapeos[ultimo_nodo]

        graph.add_edge(nodo_u1, primer_nodo, label='ep')
        graph.add_edge(ultimo_nodo, nodo_u4, label='ep')
        graph.add_edge(nodo_u1, nodo_u2, label='ep')
        graph.add_edge(nodo_u2, nodo_u3, label=f'{b}')
        graph.add_edge(nodo_u3, nodo_u4, label='ep')
        
        contador_label = 0
        for node in graph.nodes():
            if graph.get_node(node).attr.get('label') == '':
                graph.get_node(node).attr['label'] = str(contador_label)
            else:
                graph.get_node(node).attr['label'] = str(contador_label)
                contador_label += 1

        with graph.subgraph(name=primer_nodo) as sg:
            sg.add_node(primer_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        with graph.subgraph(name=ultimo_nodo) as sg:
            sg.add_node(ultimo_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        graph.get_node(primer_nodo).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo).attr['shape'] = 'circle'
        graph.get_node(nodo_u1).attr['shape'] = 'circle'
        graph.get_node(nodo_u2).attr['shape'] = 'circle'
        graph.get_node(nodo_u3).attr['shape'] = 'circle'
        graph.get_node(nodo_u4).attr['shape'] = 'circle'

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'
       

    elif not isinstance(a, pgv.AGraph) and isinstance(b, pgv.AGraph):
        mapeos = {}
        labels = {}
        S = next(id_unico)
        
        graph.add_node(S, label='S')
        
        for node in b.nodes():
            id_unico_nodo = next(id_unico)
            label = node.attr['label'] if 'label' in node.attr else node
            mapeos[node] = id_unico_nodo
            labels[id_unico_nodo] = label
            graph.add_node(id_unico_nodo, label=label)
        for edge in b.edges():
            graph.add_edge(mapeos[edge[0]], mapeos[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')
            
        P = next(id_unico)
        O = next(id_unico)
        T = next(id_unico)
        graph.add_node(P, label='P')
        graph.add_node(O, label='O')
        graph.add_node(T, label='T')

        primer_nodo, ultimo_nodo = primero_y_ultimo_afn(b)
        primer_nodo = mapeos[primer_nodo]
        ultimo_nodo = mapeos[ultimo_nodo]

        graph.add_edge(S, primer_nodo, label='ep')
        graph.add_edge(ultimo_nodo, T, label='ep')
        graph.add_edge(S, P, label='ep')
        graph.add_edge(P, O, label=f'{a}')
        graph.add_edge(O, T, label='ep')
        
        contador_label = 0
        for node in graph.nodes():
            if graph.get_node(node).attr.get('label') == '':
                graph.get_node(node).attr['label'] = str(contador_label)
            else:
                graph.get_node(node).attr['label'] = str(contador_label)
                contador_label += 1

        with graph.subgraph(name=primer_nodo) as sg:
            sg.add_node(primer_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        with graph.subgraph(name=ultimo_nodo) as sg:
            sg.add_node(ultimo_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        graph.get_node(primer_nodo).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo).attr['shape'] = 'circle'
        graph.get_node(S).attr['shape'] = 'circle'
        graph.get_node(P).attr['shape'] = 'circle'
        graph.get_node(O).attr['shape'] = 'circle'
        graph.get_node(T).attr['shape'] = 'circle'

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'
        

    elif isinstance(a, pgv.AGraph) and isinstance(b, pgv.AGraph):
        mapeos_a = {}
        mapeos_b = {}
        labels_a = {}
        labels_b = {}
        
        X = next(id_unico)
        
        graph.add_node(X, label='X')
        
        for node in a.nodes():
            id_unico_nodo = next(id_unico)
            label_a = node.attr['label'] if 'label' in node.attr else node
            mapeos_a[node] = id_unico_nodo
            labels_a[id_unico_nodo] = label_a
            graph.add_node(id_unico_nodo, label=label_a)
        for edge in a.edges():
            graph.add_edge(mapeos_a[edge[0]], mapeos_a[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')
        for node in b.nodes():
            id_unico_nodo = next(id_unico)
            label_b = node.attr['label'] if 'label' in node.attr else node
            mapeos_b[node] = id_unico_nodo
            labels_b[id_unico_nodo] = label_b
            graph.add_node(id_unico_nodo, label=label_b)
        for edge in b.edges():
            graph.add_edge(mapeos_b[edge[0]], mapeos_b[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')
            
        Y = next(id_unico)    
        graph.add_node(Y, label='Y')

        primer_nodo_a, ultimo_nodo_a = primero_y_ultimo_afn(a)
        primer_nodo_a = mapeos_a[primer_nodo_a]
        ultimo_nodo_a = mapeos_a[ultimo_nodo_a]

        primer_nodo_b, ultimo_nodo_b = primero_y_ultimo_afn(b)
        primer_nodo_b = mapeos_b[primer_nodo_b]
        ultimo_nodo_b = mapeos_b[ultimo_nodo_b]

        graph.add_edge(X, primer_nodo_a, label='ep')
        graph.add_edge(X, primer_nodo_b, label='ep')
        graph.add_edge(ultimo_nodo_a, Y, label='ep')
        graph.add_edge(ultimo_nodo_b, Y, label='ep')
        
        contador_label = 0
        for node in graph.nodes():
            if graph.get_node(node).attr.get('label') == '':
                graph.get_node(node).attr['label'] = str(contador_label)
            else:
                graph.get_node(node).attr['label'] = str(contador_label)
                contador_label += 1

        with graph.subgraph(name=primer_nodo_a) as sg:
            sg.add_node(primer_nodo_a)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        with graph.subgraph(name=ultimo_nodo_a) as sg:
            sg.add_node(ultimo_nodo_a)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        with graph.subgraph(name=primer_nodo_b) as sg:
            sg.add_node(primer_nodo_b)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        with graph.subgraph(name=ultimo_nodo_b) as sg:
            sg.add_node(ultimo_nodo_b)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''

        graph.get_node(primer_nodo_a).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo_a).attr['shape'] = 'circle'
        graph.get_node(primer_nodo_b).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo_b).attr['shape'] = 'circle'
        graph.get_node(X).attr['shape'] = 'circle'
        graph.get_node(Y).attr['shape'] = 'circle'

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'
        

    else:
        nodo_1 = next(id_unico)
        nodo_2 = next(id_unico)
        nodo_3 = next(id_unico)
        nodo_4 = next(id_unico)
        nodo_5 = next(id_unico)
        nodo_6 = next(id_unico)

        graph.add_node(nodo_1, label='0')
        graph.add_node(nodo_2, label='1')
        graph.add_node(nodo_3, label='3')
        graph.add_node(nodo_4, label='2')
        graph.add_node(nodo_5, label='4')
        graph.add_node(nodo_6, label='5')

        graph.add_edge(nodo_1, nodo_2, label='ep')
        graph.add_edge(nodo_1, nodo_3, label='ep')
        graph.add_edge(nodo_2, nodo_4, label=f'{a}')
        graph.add_edge(nodo_4, nodo_6, label='ep')
        graph.add_edge(nodo_3, nodo_5, label=f'{b}')
        graph.add_edge(nodo_5, nodo_6, label='ep')

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'
        
    return graph

def kleene_afn(a):
    graph = pgv.AGraph(directed=True)

    if isinstance(a, pgv.AGraph):
        nodo_1 = next(id_unico)
        graph.add_node(nodo_1, label='0')

        mapeos = {}
        labels = {}
        for node in a.nodes():
            id_unico_nodo = next(id_unico)
            label = node.attr['label'] if 'label' in node.attr else node
            mapeos[node] = id_unico_nodo
            labels[id_unico_nodo] = label
            graph.add_node(id_unico_nodo, label=label)
            
        nodo_2 = next(id_unico)
        graph.add_node(nodo_2, label='')
        for edge in a.edges():
            graph.add_edge(mapeos[edge[0]], mapeos[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')

        primer_nodo, ultimo_nodo = primero_y_ultimo_afn(a)
        primer_nodo = mapeos[primer_nodo]
        ultimo_nodo = mapeos[ultimo_nodo]

        total_nodos = len(graph.nodes()) + 2  

        label_nodo_2 = str(total_nodos - 1)
        graph.get_node(nodo_2).attr['label'] = label_nodo_2
        
        graph.add_edge(nodo_1, primer_nodo, label='ep')
        graph.add_edge(ultimo_nodo, nodo_2, label='ep')
        graph.add_edge(ultimo_nodo, primer_nodo, label='ep')
        graph.add_edge(nodo_1, nodo_2, label='ep')

        contador_label = 0
        for node in graph.nodes():
            if graph.get_node(node).attr.get('label') == '':
                graph.get_node(node).attr['label'] = str(contador_label)
            else:
                graph.get_node(node).attr['label'] = str(contador_label)
                contador_label += 1
        
        with graph.subgraph(name=primer_nodo) as sg:
            sg.add_node(primer_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        with graph.subgraph(name=ultimo_nodo) as sg:
            sg.add_node(ultimo_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        graph.get_node(primer_nodo).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo).attr['shape'] = 'circle'
        graph.get_node(nodo_1).attr['shape'] = 'circle'
        graph.get_node(nodo_2).attr['shape'] = 'circle'

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'

        
    else:
        nodo_1 = next(id_unico)
        nodo_2 = next(id_unico)
        nodo_3 = next(id_unico)
        nodo_4 = next(id_unico)

        graph.add_node(nodo_1, label='0')
        graph.add_node(nodo_2, label='3')
        graph.add_node(nodo_3, label='1')
        graph.add_node(nodo_4, label='2')
        
        graph.add_edge(nodo_1, nodo_2, label='ep')
        graph.add_edge(nodo_4, nodo_3, label='ep')
        graph.add_edge(nodo_3, nodo_4, label=f'{a}')
        graph.add_edge(nodo_1, nodo_3, label='ep')
        graph.add_edge(nodo_4, nodo_2, label='ep')

        graph.graph_attr['rankdir'] = 'BT'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'

        
    
    return graph

def concatenacion_afn(a, b):
    graph = pgv.AGraph(directed=True)
    
    if isinstance(a, pgv.AGraph) and not isinstance(b, pgv.AGraph):
        mapeos = {}
        labels = {}
        
        for node in a.nodes():
            id_unico_nodo = next(id_unico)
            label = node.attr['label'] if 'label' in node.attr else node
            mapeos[node] = id_unico_nodo
            labels[id_unico_nodo] = label
            graph.add_node(id_unico_nodo, label=label)
        
        for edge in a.edges():
            graph.add_edge(mapeos[edge[0]], mapeos[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')
            
        primer_nodo, ultimo_nodo = primero_y_ultimo_afn(a)
        primer_nodo = mapeos[primer_nodo]
        ultimo_nodo = mapeos[ultimo_nodo]
        
        nodo_1 = next(id_unico)
        graph.add_node(nodo_1, label='4')
        nodo_2 = next(id_unico)
        graph.add_node(nodo_2, label='')
        
        graph.add_edge(ultimo_nodo, nodo_1, label='ep')
        graph.add_edge(nodo_1, nodo_2, label=f'{b}')
        
        contador_label = 0
        for node in graph.nodes():
            if graph.get_node(node).attr.get('label') == '':
                graph.get_node(node).attr['label'] = str(contador_label)
            else:
                graph.get_node(node).attr['label'] = str(contador_label)
                contador_label += 1

        with graph.subgraph(name=primer_nodo) as sg:
            sg.add_node(primer_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        with graph.subgraph(name=ultimo_nodo) as sg:
            sg.add_node(ultimo_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        graph.get_node(primer_nodo).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo).attr['shape'] = 'circle'
        graph.get_node(nodo_1).attr['shape'] = 'circle'
        graph.get_node(nodo_2).attr['shape'] = 'circle'

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'
       
        
    elif not isinstance(a, pgv.AGraph) and isinstance(b, pgv.AGraph):
        mapeos = {}
        labels = {}
        
        nodo_c1 = next(id_unico)
        nodo_c2 = next(id_unico)
        graph.add_node(nodo_c1, label='0')
        graph.add_node(nodo_c2, label='1')
        
        for node in b.nodes():
            id_unico_nodo = next(id_unico)
            label = node.attr['label'] if 'label' in node.attr else node
            mapeos[node] = id_unico_nodo
            labels[id_unico_nodo] = label
            graph.add_node(id_unico_nodo, label=label)
        
        for edge in b.edges():
            graph.add_edge(mapeos[edge[0]], mapeos[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')
            
        primer_nodo, ultimo_nodo = primero_y_ultimo_afn(b)
        primer_nodo = mapeos[primer_nodo]
        ultimo_nodo = mapeos[ultimo_nodo]
        
        graph.add_edge(nodo_c1, nodo_c2, label=f'{a}')
        graph.add_edge(nodo_c2, primer_nodo, label='ep')
        
        contador_label = 0
        for node in graph.nodes():
            if graph.get_node(node).attr.get('label') == '':
                graph.get_node(node).attr['label'] = str(contador_label)
            else:
                graph.get_node(node).attr['label'] = str(contador_label)
                contador_label += 1

        with graph.subgraph(name=primer_nodo) as sg:
            sg.add_node(primer_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        with graph.subgraph(name=ultimo_nodo) as sg:
            sg.add_node(ultimo_nodo)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        graph.get_node(primer_nodo).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo).attr['shape'] = 'circle'
        graph.get_node(nodo_c1).attr['shape'] = 'circle'
        graph.get_node(nodo_c2).attr['shape'] = 'circle'

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'
        
        
    elif isinstance(a, pgv.AGraph) and isinstance(b, pgv.AGraph):
        mapeos_a = {}
        mapeos_b = {}
        labels_a = {}
        labels_b = {}

        for node in a.nodes():
            id_unico_nodo = next(id_unico)
            label_a = node.attr['label'] if 'label' in node.attr else node
            mapeos_a[node] = id_unico_nodo
            labels_a[id_unico_nodo] = label_a
            graph.add_node(id_unico_nodo, label=label_a)
        
        for edge in a.edges():
            graph.add_edge(mapeos_a[edge[0]], mapeos_a[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')

        for node in b.nodes():
            id_unico_nodo = next(id_unico)
            label_b = node.attr['label'] if 'label' in node.attr else node
            mapeos_b[node] = id_unico_nodo
            labels_b[id_unico_nodo] = label_b
            graph.add_node(id_unico_nodo, label=label_b)
        
        for edge in b.edges():
            graph.add_edge(mapeos_b[edge[0]], mapeos_b[edge[1]], label=edge.attr['label'] if 'label' in edge.attr else '')

        primer_nodo_a, ultimo_nodo_a = primero_y_ultimo_afn(a)
        primer_nodo_b, ultimo_nodo_b = primero_y_ultimo_afn(b)
        primer_nodo_a = mapeos_a[primer_nodo_a]
        ultimo_nodo_a = mapeos_a[ultimo_nodo_a]
        primer_nodo_b = mapeos_b[primer_nodo_b]
        ultimo_nodo_b = mapeos_b[ultimo_nodo_b]
        
        graph.add_edge(ultimo_nodo_a, primer_nodo_b, label='ep')
        
        contador_label = 0
        for node in graph.nodes():
            if graph.get_node(node).attr.get('label') == '':
                graph.get_node(node).attr['label'] = str(contador_label)
            else:
                graph.get_node(node).attr['label'] = str(contador_label)
                contador_label += 1

        with graph.subgraph(name=primer_nodo_a) as sg:
            sg.add_node(primer_nodo_a)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        with graph.subgraph(name=ultimo_nodo_a) as sg:
            sg.add_node(ultimo_nodo_a)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
            
        with graph.subgraph(name=primer_nodo_b) as sg:
            sg.add_node(primer_nodo_b)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        with graph.subgraph(name=ultimo_nodo_b) as sg:
            sg.add_node(ultimo_nodo_b)
            sg.graph_attr['style'] = 'invisible'
            sg.graph_attr['label'] = ''
        
        graph.get_node(primer_nodo_a).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo_a).attr['shape'] = 'circle'
        graph.get_node(primer_nodo_b).attr['shape'] = 'circle'
        graph.get_node(ultimo_nodo_b).attr['shape'] = 'circle'

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'

        
    else:
        nodo_1 = next(id_unico)
        nodo_2 = next(id_unico)
        nodo_3 = next(id_unico)
        nodo_4 = next(id_unico)

        graph.add_node(nodo_1, label='0')
        graph.add_node(nodo_2, label='1')
        graph.add_node(nodo_3, label='2')
        graph.add_node(nodo_4, label='3')
        
        graph.add_edge(nodo_1, nodo_2, label=f'{a}')
        graph.add_edge(nodo_2, nodo_3, label='ep')
        graph.add_edge(nodo_3, nodo_4, label=f'{b}')

        graph.graph_attr['rankdir'] = 'LR'
        graph.graph_attr['ranksep'] = '1.0'
        graph.graph_attr['nodesep'] = '0.5'
        graph.node_attr['shape'] = 'circle'
        graph.edge_attr['fontsize'] = '10'
        
    return graph


indices = [0]

for i in indices:

    archivo_dot = f"grafo_afn_no_dirigido_{i}.dot"
    archivo_afn = f"afn_resultante_{i}.png"
    archivo_afn_dot = f"afn_resultante_{i}.dot"
    

    arbol_dot = pgv.AGraph(archivo_dot)
    nodo_raiz = list(arbol_dot.nodes())[0]  

    afn = construir_afn_desde_arbol(arbol_dot, nodo_raiz)
    

    nodo_inicial = [node for node in afn.nodes() if len(afn.predecessors(node)) == 0 and len(afn.successors(node)) > 0]
    nodo_final = [node for node in afn.nodes() if len(afn.successors(node)) == 0 and len(afn.predecessors(node)) > 0]
    

    for node in afn.nodes():
        if node in nodo_inicial:
            afn.get_node(node).attr.update(color='red', style='filled', fillcolor='lightcoral')
        elif node in nodo_final:
            afn.get_node(node).attr.update(color='blue', style='filled', fillcolor='lightblue')
            
    afn.draw(archivo_afn, format='png', prog='dot')
    afn.write(archivo_afn_dot)

def cargar_afn(nombre_archivo):
    return pgv.AGraph(nombre_archivo)

def mover_afn(afn, estados, simbolo):
    resultados = set()
    for estado in estados:
        for sucesor in afn.successors(estado):
            if afn.get_edge(estado, sucesor).attr['label'] == simbolo:
                resultados.add(sucesor)
    return resultados

def cerradura_afn(afn, estados):
    stack = list(estados)
    resultado = set(estados)

    while stack:
        estado = stack.pop()
        for sucesor in afn.successors(estado):
            if afn.get_edge(estado, sucesor).attr['label'] == 'ep' and sucesor not in resultado:
                resultado.add(sucesor)
                stack.append(sucesor)

    return resultado

indices = [0]

def encontrar_nodo_inicial_afn(grafo_afn):
    for nodo in grafo_afn.nodes():
        if grafo_afn.in_degree(nodo) == 0:  
            return nodo
    return None

def avanzar_nodos_afn(grafo_afn, nodos_actuales, char):
    nuevos_nodos = set()
    for nodo in nodos_actuales:
        for vecino in grafo_afn.successors(nodo):
            edge = grafo_afn.get_edge(nodo, vecino)
            if edge.attr['label'] == char:
                nuevos_nodos.add(vecino)
    return nuevos_nodos

def expandir_transiciones_epsilon_afn(grafo_afn, nodos):
    nodos_a_explorar = list(nodos)
    nodos_expandidos = set(nodos)
    
    while nodos_a_explorar:
        nodo = nodos_a_explorar.pop()
        for vecino in grafo_afn.successors(nodo):
            edge = grafo_afn.get_edge(nodo, vecino)
            if edge.attr['label'] == 'ep' and vecino not in nodos_expandidos:
                nodos_expandidos.add(vecino)
                nodos_a_explorar.append(vecino)
                
    return nodos_expandidos

def nodos_son_aceptacion_afn(grafo_afn, nodos_actuales):
    for nodo in nodos_actuales:
        if grafo_afn.get_node(nodo).attr.get('color') == 'blue':  
            return True
    return False

def simulacion_afn(cadena):
    grafo_afn = pgv.AGraph('afn_resultante_0.dot')
    
    nodo_inicial = encontrar_nodo_inicial_afn(grafo_afn)
    
    if nodo_inicial is None:
        return 'no'
    
    nodos_actuales = {nodo_inicial}
    
    nodos_actuales = expandir_transiciones_epsilon_afn(grafo_afn, nodos_actuales)
    
    for char in cadena:
        nodos_actuales = avanzar_nodos_afn(grafo_afn, nodos_actuales, char)
        nodos_actuales = expandir_transiciones_epsilon_afn(grafo_afn, nodos_actuales)
    
    if nodos_son_aceptacion_afn(grafo_afn, nodos_actuales):
        return 'si'
    else:
        return 'no'
    
def nodo_es_aceptacion_afn(nodo):
    return nodo.attr.get('fillcolor') == 'lightblue'

def avanzar_nodo(grafo_afn, nodo_actual, char):
    for edge in grafo_afn.out_edges(nodo_actual):
        label = edge.attr.get('label', '')
        if label == char:
            return edge[1]
    
    return None
    
def encontrar_nodo_inicial_afn_minimizado_afn(grafo_afn):
    for node in grafo_afn.nodes():
        if node == 's0':
            return node
    return None

def main():
    expresiones_postfix = infix_a_postfix()

    if expresiones_postfix != 'La cadena no está balanceada':
        indices = list(range(len(expresiones_postfix))) 
        
        for i, expresion in enumerate(expresiones_postfix):
            print(f'\n🔍 Analizando la expresión: {expresion}')
            
            cadenas_prueba = ['aaabb', '', 'a']
            
            print(f"\n🛠 Probando cadenas en el AFD para la expresión: {expresion}")
            afd = procesar_expresion(expresion, f'expresion_{i}', cadenas_prueba)

        print("\n Simulación de AFN:")
        for i in indices:
            archivo_afn_dot = f"afn_resultante_{i}.dot"
            
            try:
                afn = pgv.AGraph(archivo_afn_dot)
                resultado = simulacion_afn('abb')
                print(f"AFN {archivo_afn_dot}: {'Aceptado' if resultado == 'si' else 'Rechazado'}")
            except Exception as e:
                print(f"Error al procesar {archivo_afn_dot}: {e}")

if __name__ == "__main__":
    main()
