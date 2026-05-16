# ==========================================
# 1. EL MODELO DE DATOS Y EL JUEZ (caso_criminal.py)
# ==========================================

class CasoCriminal:
    def __init__(self, id_caso, tipo, ley, pena, gravedad):
        self.id_caso = id_caso          
        self.tipo = tipo                
        self.ley = ley                  
        self.pena = pena               
        self.gravedad = gravedad  # El ID objetivo ideal (10, 20, 30, 40)
        self.evidencias = []            

    def __str__(self):
        return f"Caso {self.id_caso}: {self.tipo} ({self.ley})"

def calcular_sentencia(arbol_jugador):
    """
    Actúa como el Juez. Compara el árbol generado por 
    los jugadores contra la verdad del caso.
    """
    nodos_jugador = arbol_jugador.obtener_lista_ordenada()
    
    aciertos = 0
    total_objetivo = 4
    
    # La verdad absoluta del caso
    verdad = {
        10: "Injuria",
        20: "Calumnia",
        30: "Suplantación",
        40: "Hostigamiento"
    }

    for peso_en_arbol, objeto_caso in nodos_jugador:
        # Verificamos si el peso que sumaron existe en la ley
        if peso_en_arbol in verdad:
            # Verificamos si la clasificación que hizo Alexa coincide con el peso
            if verdad[peso_en_arbol] == objeto_caso.tipo:
                aciertos += 1
    
    # Devuelve el porcentaje de justicia (0 a 100)
    porcentaje = (aciertos / total_objetivo) * 100
    return porcentaje