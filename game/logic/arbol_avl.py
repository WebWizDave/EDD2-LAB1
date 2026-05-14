from .nodo_avl import Nodo, NodoAVL
from .caso_criminal import CasoCriminal

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    #getters
    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)
    
    #rotaciones simples
    def rotacion_derecha(self, y):
        # y es el nodo que está desbalanceado
        x = y.izquierdo
        T2 = x.derecho
        
        # efectuar la rotacion
        x.derecho = y
        y.izquierdo = T2
        
        # Actualizar alturas
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        x.altura = 1 + max(self.obtener_altura(x.izquierdo), self.obtener_altura(x.derecho))

        # Retorna la nueva raiz del sub arbol
        return x

    def rotacion_izquierda(self, x):
        # x es el nodo desbalanceado
        y = x.derecho
        T2 = y.izquierdo

        # efectuar la rotacion
        y.izquierdo = x
        x.derecho = T2

        # Actualizar alturas
        x.altura = 1 + max(self.obtener_altura(x.izquierdo), self.obtener_altura(x.derecho))
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))

        return y
     
    def insertar_pista(self, dato, peso_real, descripcion=""):
        """Inserta una pista sin balancear automáticamente."""
        self.raiz = self._insertar_recursivo(self.raiz, dato, peso_real, descripcion)

    def _insertar_recursivo(self, nodo, dato, peso_real, descripcion):
        # 1. Inserción normal de Árbol Binario de Búsqueda
        if not nodo:
            return Nodo(dato, peso_real, descripcion)
        
        if dato < nodo.dato:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, dato, peso_real, descripcion)
        elif dato > nodo.dato:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, dato, peso_real, descripcion)
        else:
            return nodo # No duplicados por ahora

        # 2. Actualizamos la altura basándonos en el peso máximo de los hijos + el propio
        nodo.altura = peso_real + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        
        return nodo
    
    #metodo para agregar los caso mas facil
    def agregar_caso(self, nuevo_caso):
        self.raiz = self.insertar(self.raiz, nuevo_caso)
        
        
    #usamos recorrido in orden porque devuelve los elementos ordenados de menor a mayor
    #necesario para el reporte final de los delitos procesados
    
    def recorrido_inorden(self, nodo_actual, lista_reporte):
        # Caso base
        if not nodo_actual:
            return

        # 1. Visitar subárbol IZQUIERDO (Casos menos graves)
        self.recorrido_inorden(nodo_actual.izquierdo, lista_reporte)
        # 2. Visitar la RAÍZ (El caso actual)
        lista_reporte.append(nodo_actual.dato)
        # 3. Visitar subárbol DERECHO (Casos más graves)
        self.recorrido_inorden(nodo_actual.derecho, lista_reporte)
   
    def obtener_lista_ordenada(self):
        """Método público para obtener el reporte desde el juego"""
        reporte = []
        self.recorrido_inorden(self.raiz, reporte)
        return reporte

    def ejecutar_rotacion_derecha(self, dato_padre):
        """Busca el nodo con el dato_padre y lo rota a la derecha."""
        self.raiz = self._buscar_y_rotar_der(self.raiz, dato_padre)

    def _buscar_y_rotar_der(self, nodo, dato):
        if not nodo: return None
        if dato < nodo.dato:
            nodo.izquierda = self._buscar_y_rotar_der(nodo.izquierda, dato)
        elif dato > nodo.dato:
            nodo.derecha = self._buscar_y_rotar_der(nodo.derecha, dato)
        else:
            # Encontramos el nodo desbalanceado, ejecutamos la rotación
            return self.rotar_derecha(nodo)
        return nodo

    def ejecutar_rotacion_izquierda(self, dato_padre):
        """Busca el nodo con el dato_padre y lo rota a la izquierda."""
        self.raiz = self._buscar_y_rotar_izq(self.raiz, dato_padre)

    def _buscar_y_rotar_izq(self, nodo, dato):
        if not nodo: return None
        if dato < nodo.dato:
            nodo.izquierda = self._buscar_y_rotar_izq(nodo.izquierda, dato)
        elif dato > nodo.dato:
            nodo.derecha = self._buscar_y_rotar_izq(nodo.derecha, dato)
        else:
            return self.rotar_izquierda(nodo)
        return nodo
                                                 
if __name__ == "__main__":
    #prueba
    #instanciar el arbol
    investigacion = ArbolAVL()
    
    #casos de prueba
    caso1 = CasoCriminal(1,"Injuria", "Art.220 CP", "Multa/Prision", 10)
    caso2 = CasoCriminal(2, "Calumnia", "Art. 221 CP", "Prision 16-72 meses", 20)
    caso3 = CasoCriminal(3,"Suplantación de sitios web", "Ley 1273 de 2009 Art. 269F","Prision 48-96 meses", 30)
    caso4 = CasoCriminal(4,"Acceso abusivo a sistemas informaticos", "Ley 1273 de 2009 Art. 269A","Prision 48-96 meses + multa", 40)
    
    #Intertar en el arbol
    investigacion.agregar_caso(caso1)
    investigacion.agregar_caso(caso2)
    investigacion.agregar_caso(caso3)
    investigacion.agregar_caso(caso4)
    
    print("---RECUENTO DE CASOS CRIMINALES---")
    for c in investigacion.obtener_reporte():
        print(f"[{c.gravedad}] -> {c.tipo} (Ley:{c.ley})")
