class Nodo:
    def __init__(self, clave, dato):
        self.clave = clave         # EL PESO SUMADO (Ej. 7, 10, 25...)
        self.dato = dato           # El objeto CasoCriminal completo
        self.izquierda = None      # Mantenemos tu unificación impecable
        self.derecha = None        # Mantenemos tu unificación impecable
        self.altura = 1