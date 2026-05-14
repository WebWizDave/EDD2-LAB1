class Nodo:
    def __init__(self, dato, peso_real=1, descripcion=""):
        self.dato = dato           # Este es el valor del delito (para posición)
        self.peso_real = peso_real   # Este es el peso oculto que afecta el balance
        self.descripcion = descripcion
        self.izquierda = None
        self.derecha = None
        self.altura = peso_real    # Iniciamos la altura con el peso de la pista