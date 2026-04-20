from .nodo_avl import NodoAVL
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
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)
    
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
    
    
    def insertar(self, nodo_actual, caso_nuevo):
        # 1. insercion normal
        if not nodo_actual:
            return NodoAVL(caso_nuevo)

        if caso_nuevo.gravedad < nodo_actual.dato.gravedad:
            nodo_actual.izquierdo = self.insertar(nodo_actual.izquierdo, caso_nuevo)
        elif caso_nuevo.gravedad > nodo_actual.dato.gravedad:
            nodo_actual.derecho = self.insertar(nodo_actual.derecho, caso_nuevo)
        else:
            return nodo_actual 

        # 2. actualizar la altura 
        nodo_actual.altura = 1 + max(self.obtener_altura(nodo_actual.izquierdo), self.obtener_altura(nodo_actual.derecho))

        # 3. obtener el factor de equilibrio
        balance = self.obtener_balance(nodo_actual)

        # 4. casos de desbalance:

        # Caso Izquierda-Izquierda (Simple Derecha)
        if balance > 1 and caso_nuevo.gravedad < nodo_actual.izquierdo.dato.gravedad:
            return self.rotacion_derecha(nodo_actual)

        # Caso Derecha-Derecha (Simple Izquierda)
        if balance < -1 and caso_nuevo.gravedad > nodo_actual.derecho.dato.gravedad:
            return self.rotacion_izquierda(nodo_actual)

        # Caso Izquierda-Derecha (Doble Derecha)
        if balance > 1 and caso_nuevo.gravedad > nodo_actual.izquierdo.dato.gravedad:
            nodo_actual.izquierdo = self.rotacion_izquierda(nodo_actual.izquierdo)
            return self.rotacion_derecha(nodo_actual)

        # Caso Derecha-Izquierda (Doble Izquierda)
        if balance < -1 and caso_nuevo.gravedad < nodo_actual.derecho.dato.gravedad:
            nodo_actual.derecho = self.rotacion_derecha(nodo_actual.derecho)
            return self.rotacion_izquierda(nodo_actual)

        return nodo_actual
    
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
