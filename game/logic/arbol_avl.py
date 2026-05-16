from .nodo_avl import Nodo
from .caso_criminal import CasoCriminal
from .caso_criminal import calcular_sentencia

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def actualizar_altura(self, nodo):
        if not nodo:
            return
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        # Rotación
        x.derecha = y
        y.izquierda = T2

        # Actualizar alturas
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        # Rotación
        y.izquierda = x
        x.derecha = T2

        # Actualizar alturas
        self.actualizar_altura(x)
        self.actualizar_altura(y)
        return y

    # Método principal para que interactúen los hermanos
    def insertar_capitulo(self, peso_total, caso_criminal):
        """ Inserta usando el peso como clave para el balanceo y guarda el caso. """
        self.raiz = self._insertar_recursivo(self.raiz, peso_total, caso_criminal)

    def _insertar_recursivo(self, nodo, clave, dato):
        # 1. Inserción normal de árbol binario
        if not nodo:
            return Nodo(clave, dato)
        
        if clave < nodo.clave:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, clave, dato)
        elif clave > nodo.clave:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, clave, dato)
        else:
            return nodo # No permitimos duplicados exactos de peso para no romper la lógica
        
        # 2. Actualizar altura del ancestro
        self.actualizar_altura(nodo)

        # 3. Obtener factor de balance
        balance = self.obtener_balance(nodo)

        # 4. Las 4 rotaciones del AVL (usando 'izquierda' y 'derecha')
        # Caso Izquierda-Izquierda
        if balance > 1 and clave < nodo.izquierda.clave:
            return self.rotar_derecha(nodo)
        
        # Caso Derecha-Derecha
        if balance < -1 and clave > nodo.derecha.clave:
            return self.rotar_izquierda(nodo)
        
        # Caso Izquierda-Derecha
        if balance > 1 and clave > nodo.izquierda.clave:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)
        
        # Caso Derecha-Izquierda
        if balance < -1 and clave < nodo.derecha.clave:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    # Métodos para extraer los datos para el Juez y la Interfaz Visual
    def obtener_lista_ordenada(self):
        """Devuelve una lista de tuplas: [(peso, objeto_caso), ...]"""
        lista = []
        self._recorrido_inorden(self.raiz, lista)
        return lista

    def _recorrido_inorden(self, nodo, lista):
        if nodo:
            self._recorrido_inorden(nodo.izquierda, lista)
            lista.append((nodo.clave, nodo.dato))
            self._recorrido_inorden(nodo.derecha, lista)
'''   
    print("---RECUENTO DE CASOS CRIMINALES---")
    for c in investigacion.obtener_reporte():
        print(f"[{c.gravedad}] -> {c.tipo} (Ley:{c.ley})")
        '''