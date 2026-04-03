from graphviz import Digraph
import os

class VisualizadorArbol:
    def __init__(self, arbol):
        self.arbol = arbol
        # crear el objeto de graphviz
        self.dot = Digraph(comment='Sistema de Investigacion AVL')
        # colores
        self.dot.attr('node', shape='record', style='filled', color='skyblue')

    def generar_imagen(self, nombre_archivo="arbol_casos"):
        self.dot.clear()
        self._construir_grafo(self.arbol.raiz)
        
        # la ruta de salida carpeta images
        ruta_salida = os.path.join('game', 'images', nombre_archivo)
        
        # renderizar la imagen a formato png
        self.dot.render(ruta_salida, format='png', cleanup=True)
        print(f"Imagen generada en: {ruta_salida}.png")

    def _construir_grafo(self, nodo):
        if nodo:
            # 1. creamos el nodo con la informacion del caso
            #  usamos el ID y el tipo de delito para la etiqueta de los nodos
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