class CasoCriminal:
    def __init__(self, id_caso, tipo, ley, pena, gravedad):
        self.id_caso = id_caso          
        self.tipo = tipo                
        self.ley = ley                  
        self.pena = pena               
        self.gravedad = gravedad        
        self.evidencias = []            

    def __str__(self):
        return f"Caso {self.id_caso}: {self.tipo} ({self.ley})"