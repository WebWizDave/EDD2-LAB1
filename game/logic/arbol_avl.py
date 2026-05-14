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
    
    
    def actualizar_altura(self, nodo):
        if not nodo:
            return
        # La altura considera el peso_real del nodo actual + el máximo de sus hijos
        nodo.altura = nodo.peso_real + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        
    #rotaciones simples
    def rotar_derecha(self, y):
        # x es el nuevo padre, y es el nodo que baja a la derecha
        x = y.izquierda
        T2 = x.derecha

        # Realizar rotación
        x.derecha = y
        y.izquierda = T2

        # Actualizar alturas
        self.actualizar_altura(y)
        self.actualizar_altura(x)

        return x

    def rotar_izquierda(self, x):
        # y es el nuevo padre, x es el nodo que baja a la izquierda
        y = x.derecha
        T2 = y.izquierda

        # Realizar rotación
        y.izquierda = x
        x.derecha = T2

        # Actualizar alturas
        self.actualizar_altura(x)
        self.actualizar_altura(y)

        return y
     
    def insertar_pista(self, dato, peso_real, descripcion=""):
        self.raiz = self._insertar_recursivo(self.raiz, dato, peso_real, descripcion)

    def _insertar_recursivo(self, nodo, dato, peso_real, descripcion):
        if not nodo:
            return Nodo(dato, peso_real, descripcion)
        
        if dato < nodo.dato:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, dato, peso_real, descripcion)
        elif dato > nodo.dato:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, dato, peso_real, descripcion)
        
        self.actualizar_altura(nodo)
        return nodo
    
    # Funciones cooperativo para que el Jugador 2 llame desde la interfaz
    def ejecutar_rotacion_derecha(self, dato_objetivo):
        self.raiz = self._buscar_y_rotar(self.raiz, dato_objetivo, "derecha")

    def ejecutar_rotacion_izquierda(self, dato_objetivo):
        self.raiz = self._buscar_y_rotar(self.raiz, dato_objetivo, "izquierda")

    def _buscar_y_rotar(self, nodo, dato, tipo):
        if not nodo:
            return None
        
        if dato < nodo.dato:
            nodo.izquierda = self._buscar_y_rotar(nodo.izquierda, dato, tipo)
        elif dato > nodo.dato:
            nodo.derecha = self._buscar_y_rotar(nodo.derecha, dato, tipo)
        else:
            # Encontramos el nodo que el jugador quiere rotar
            if tipo == "derecha":
                if nodo.izquierda: # Solo rotamos si tiene hijo izquierdo
                    return self.rotar_derecha(nodo)
            else:
                if nodo.derecha: # Solo rotamos si tiene hijo derecho
                    return self.rotar_izquierda(nodo)
        return nodo
    
    
    
    
    
    
    
    #metodo para agregar los caso mas facil
    
    def agregar_caso(self, nuevo_caso, peso=1, desc=""):
        # Ahora usa insertar_pista para mantener la lógica de pesos
        self.raiz = self._insertar_recursivo(self.raiz, nuevo_caso, peso, desc)
    
    def recorrido_inorden(self, nodo_actual, lista_reporte):
        if not nodo_actual:
            return

        # 1. Visitar subárbol IZQUIERDA
        self.recorrido_inorden(nodo_actual.izquierda, lista_reporte)
        # 2. Visitar la RAÍZ (El caso actual)
        lista_reporte.append(nodo_actual.dato)
        # 3. Visitar subárbol DERECHA
        self.recorrido_inorden(nodo_actual.derecha, lista_reporte)
   
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
