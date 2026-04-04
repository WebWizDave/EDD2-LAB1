#este es el archivo main que se ejecuta en  renpy
init python:
    #control de errores
    try:
        from logic.arbol_avl import ArbolAVL
        from logic.visualizador import VisualizadorArbol
    except ImportError as e:
        print(f"Error cargando la logica: {e}")

#variables globales del juego
define detective = Character("Alex",color="#1e3f66")
define investigacion = ArbolAVL()
define vis = VisualizadorArbol(investigacion)

#escenas y conversaciones de prueba, modificar con la historia principal
label start:
    #escena inicial 
    scene bg_oficina_policial

    detective "Un nuevo caso en mi escritorio. Mmm.. Ciberacoso.. La ciudad ha estado muy movida ultimamente"
    detective "Necesito empezar a organizar esto antes de que se salga de control."

    detective "Primero revisaré el caso de injuria que me reportaron esta mañana."

    python:
        #insertar el caso 1
        from logic.caso_criminal import CasoCriminal
        caso1 = CasoCriminal(1,"Injuria","Art. 220 CP", "Multa", 10)
        investigacion.agregar_caso(caso1)

        #generar la imagen con visualizador
        vis.generar_imagen("arbol_actualizado")
    
    show arbol_actualizado at truecenter with fade
    detective "listo, el sistema lo ha organizado en el nivel 1, asi se ve la investigación hasta ahora."
    
    detective "ahora veamos el siguiente reporte..."
    
    return
