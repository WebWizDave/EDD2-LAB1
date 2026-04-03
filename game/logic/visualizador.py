from graphviz import Digraph
import os

class VisualizadorArbol:
    def __init__(self, arbol):
        self.arbol = arbol
        # Creamos el objeto de Graphviz
        self.dot = Digraph(comment='Sistema de Investigacion AVL')
        # Personalización visual (Colores de la policía/detective)
        self.dot.attr('node', shape='record', style='filled', color='skyblue')

    def generar_imagen(self, nombre_archivo="arbol_casos"):
        self.dot.clear() # Limpiamos para no duplicar nodos
        self._construir_grafo(self.arbol.raiz)
        
        # Definimos la ruta de salida (Carpeta images de Ren'Py)
        ruta_salida = os.path.join('game', 'images', nombre_archivo)
        
        # Renderizamos la imagen (formato png)
        self.dot.render(ruta_salida, format='png', cleanup=True)
        print(f"Imagen generada en: {ruta_salida}.png")

    def _construir_grafo(self, nodo):
        if nodo:
            # 1. Creamos el nodo visual con Info del Caso
            # Usamos el ID y el Tipo de delito para la etiqueta
            etiqueta = f"ID: {nodo.dato.id_caso} | {nodo.dato.tipo}\nGravedad: {nodo.dato.gravedad}"
            self.dot.node(str(nodo.dato.id_caso), etiqueta)

            # 2. Conectamos con el hijo IZQUIERDO
            if nodo.izquierdo:
                self.dot.edge(str(nodo.dato.id_caso), str(nodo.izquierdo.dato.id_caso), label="L")
                self._construir_grafo(nodo.izquierdo)

            # 3. Conectamos con el hijo DERECHO
            if nodo.derecho:
                self.dot.edge(str(nodo.dato.id_caso), str(nodo.derecho.dato.id_caso), label="R")
                self._construir_grafo(nodo.derecho)