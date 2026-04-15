init python:
    # Lógica del proyecto (AVL + casos)
    from logic.arbol_avl import ArbolAVL
    from logic.caso_criminal import CasoCriminal
    from collections import deque

    # Estado global
    investigacion = ArbolAVL()

    # ---- Utilidad: exportar el árbol por niveles (para mostrarlo en pantalla, sin Graphviz) ----
    def exportar_por_niveles(arbol):
        """Devuelve una lista de niveles; cada nivel es una lista de dicts con id/tipo/gravedad/L/R."""
        raiz = getattr(arbol, "raiz", None)
        if raiz is None:
            return []

        niveles = []
        q = deque([(raiz, 0, 0)])

        while q:
            nodo, depth, slot = q.popleft()
            if len(niveles) <= depth:
                niveles.append([])

            dato = getattr(nodo, "dato", None)
            izq = getattr(nodo, "izquierdo", None)
            der = getattr(nodo, "derecho", None)

            left_id = getattr(getattr(izq, "dato", None), "id_caso", None) if izq else None
            right_id = getattr(getattr(der, "dato", None), "id_caso", None) if der else None

            # FIX: calcular bal aquí mismo antes de usarlo
            altura_izq = getattr(izq, "altura", 0) if izq else 0
            altura_der = getattr(der, "altura", 0) if der else 0
            bal = altura_izq - altura_der

            niveles[depth].append({
                "id":       getattr(dato, "id_caso",  "?"),
                "tipo":     getattr(dato, "tipo",     "?"),
                "ley":      getattr(dato, "ley",      "?"),
                "pena":     getattr(dato, "pena",     "?"),
                "gravedad": getattr(dato, "gravedad", 0),
                "balance":  bal,
                "left":     left_id,
                "right":    right_id,
                "slot": slot,
            })

            if izq: q.append((izq, depth + 1, slot * 2))
            if der: q.append((der, depth + 1, slot * 2 + 1))

        return niveles

    # ---- Jugabilidad: recolección de evidencias + clasificación del caso ----
    def jugar_caso(
        id_caso,
        descripcion,
        opciones_delito,
        respuesta_delito,
        ley,
        pena,
        gravedad_correcta,
        evidencias_opciones,
        evidencias_correctas,
        modo_estricto=True,
    ):
        """Retorna True si el jugador clasifica e inserta bien; False si falla."""

        evidencias = []

        # 1) Recolectar evidencias (sí/no por cada una)
        for ev in evidencias_opciones:
            r = renpy.display_menu([
                ("Recolectar evidencia: " + ev, True),
                ("Ignorar", False),
            ])
            if r:
                evidencias.append(ev)
        
        # 2) Elegir delito
        delito = renpy.display_menu([(d, d) for d in opciones_delito])

        # 3) Elegir gravedad / nivel
        gravedad = renpy.display_menu([
            ("10 (Nivel 1)", 10),
            ("20 (Nivel 2)", 20),
            ("30 (Nivel 3)", 30),
            ("40 (Nivel 4)", 40),
        ])

        ok_delito = (delito.strip().lower() == respuesta_delito.strip().lower())        
        ok_gravedad = (gravedad == gravedad_correcta)

        if modo_estricto:
            ok_evidencias = set(evidencias_correctas).issubset(set(evidencias))        
        else:
            ok_evidencias = set(evidencias_correctas).issubset(set(evidencias))

        if ok_delito and ok_gravedad and ok_evidencias:
            caso = CasoCriminal(id_caso, delito, ley, pena, gravedad)
            caso.evidencias = evidencias
            investigacion.agregar_caso(caso)
            return True

        return False
