# ── Colores del tablero ──────────────────────────────────────────────────────
define COLOR_FONDO        = "#1a1208"
define COLOR_TITULO       = "#c8b882"
define COLOR_SUBTITULO    = "#7a6a48"
define COLOR_HILO         = "#8b3a3a"
define COLOR_NODO_TEXTO   = "#f0e8d0"

define COLOR_NODO_BAJO    = "#1e4d32"
define COLOR_NODO_MEDIO   = "#4d3010"
define COLOR_NODO_ALTO    = "#4d1a1a"
define COLOR_NODO_CRITICO = "#2a0d2e"
define COLOR_BORDE_BAJO   = "#4a7a5a"
define COLOR_BORDE_MEDIO  = "#8b6a2a"
define COLOR_BORDE_ALTO   = "#8b3a3a"
define COLOR_BORDE_CRIT   = "#7a3a8a"

# ── Función Python: color según gravedad ─────────────────────────────────────
init python:
    def color_nodo(gravedad):
        if gravedad <= 10:
            return ("#1e4d32", "#4a7a5a")
        elif gravedad <= 20:
            return ("#4d3010", "#8b6a2a")
        elif gravedad <= 30:
            return ("#4d1a1a", "#8b3a3a")
        else:
            return ("#2a0d2e", "#7a3a8a")

    def etiqueta_gravedad(gravedad):
        if gravedad <= 10:   return "● LEVE"
        elif gravedad <= 20: return "●● MODERADO"
        elif gravedad <= 30: return "●●● GRAVE"
        else:                return "●●●● CRÍTICO"

    def color_bal(bal):
        return "#4a7a5a" if abs(bal) <= 1 else "#cc4444"

# ── Posiciones X por nivel (recalculadas para 1920px) ────────────────────────
init python:
    NODO_W  = 250   
    NODO_H  = 160
    NIVEL_Y = [45, 300, 555, 795]

    def posicion_nodo(nivel, slot):
        # Divide el canvas en slots según el nivel
        num_slots = 2 ** nivel
        slot_w    = 1920 / num_slots
        x = int(slot * slot_w + slot_w / 2 - NODO_W / 2)
        y = NIVEL_Y[nivel] if nivel < len(NIVEL_Y) else 45 + nivel * 255
        return x, y

    def construir_posiciones(niveles):
        pos = {}
        for nivel_idx, nivel in enumerate(niveles):
            for nodo in nivel:
                x, y = posicion_nodo(nivel_idx, nodo["slot"])  # ← usa slot
                pos[nodo["id"]] = (x + NODO_W // 2, y + NODO_H // 2)
        return pos

# ── Screen principal del árbol ────────────────────────────────────────────────
screen arbol_avl_view(niveles):
    modal True
    tag arbol

    add Solid(COLOR_FONDO)

    python:
        pos_map = construir_posiciones(niveles)

    # Título
    frame:
        xpos 0 ypos 0
        xsize 1920 ysize 65
        background Solid("#00000080")
        padding (40, 12)
        hbox:
            spacing 24
            text "TABLERO DE INVESTIGACIÓN" color COLOR_TITULO size 26 yalign 0.5
            text "— Árbol AVL de Casos —"   color COLOR_SUBTITULO size 18 yalign 0.5

    # Área del árbol
    viewport:
        xpos 0 ypos 70
        xsize 1920 ysize 940
        draggable True
        mousewheel True

        fixed:
            xsize 1920 ysize 960

            # ── Hilos entre nodos ────────────────────────────────────────────
            for nivel_idx, nivel in enumerate(niveles):
                for nodo in nivel:
                    if nodo["left"] is not None and nodo["left"] in pos_map:
                        python:
                            x1, y1 = pos_map[nodo["id"]]
                            x2, y2 = pos_map[nodo["left"]]
                        add Transform(
                            Solid(COLOR_HILO),
                            xpos  = min(x1, x2),
                            ypos  = y1,
                            xsize = max(abs(x2 - x1), 2),
                            ysize = 2,
                        )
                        add Transform(
                            Solid(COLOR_HILO),
                            xpos  = x2,
                            ypos  = y1,
                            xsize = 2,
                            ysize = max(abs(y2 - y1), 2),
                        )
                        text "L" color "#4a7a5a" size 14 xpos (x1 + x2) // 2 - 6 ypos y1 - 18

                    if nodo["right"] is not None and nodo["right"] in pos_map:
                        python:
                            x1, y1 = pos_map[nodo["id"]]
                            x2, y2 = pos_map[nodo["right"]]
                        add Transform(
                            Solid(COLOR_HILO),
                            xpos  = min(x1, x2),
                            ypos  = y1,
                            xsize = max(abs(x2 - x1), 2),
                            ysize = 2,
                        )
                        add Transform(
                            Solid(COLOR_HILO),
                            xpos  = x2,
                            ypos  = y1,
                            xsize = 2,
                            ysize = max(abs(y2 - y1), 2),
                        )
                        text "R" color "#8b6a2a" size 14 xpos (x1 + x2) // 2 - 4 ypos y1 - 18

            # ── Nodos (polaroids) ────────────────────────────────────────────
            for nivel_idx, nivel in enumerate(niveles):
                for pos_idx, nodo in enumerate(nivel):
                    python:
                        nx, ny = posicion_nodo(nivel_idx, nodo["slot"])
                        fn, fb = color_nodo(nodo["gravedad"])
                        etiq   = etiqueta_gravedad(nodo["gravedad"])
                        cb     = color_bal(nodo["balance"])
                        tipo_t = nodo["tipo"][:22] + "…" if len(nodo["tipo"]) > 23 else nodo["tipo"]
                        ley_t  = nodo["ley"][:24]  + "…" if len(nodo["ley"])  > 25 else nodo["ley"]

                    # Sombra
                    frame:
                        xpos nx + 5  ypos ny + 5
                        xsize NODO_W ysize NODO_H
                        background Solid("#00000060")

                    # Cuerpo del nodo
                    frame:
                        xpos nx  ypos ny
                        xsize NODO_W ysize NODO_H
                        background Solid(fn)
                        padding (0, 0)

                        frame:
                            xpos 0 ypos 0
                            xsize NODO_W ysize 5
                            background Solid(fb)

                        vbox:
                            xpos 10 ypos 8
                            spacing 4

                            text etiq color fb size 14
                            text "ID [nodo['id']] — [tipo_t]" color COLOR_NODO_TEXTO size 16 bold True
                            text "[ley_t]" color "#a09070" size 14
                            text "Pena: [nodo['pena']]" color "#a09070" size 14

                            frame:
                                xsize 190 ysize 1
                                background Solid("#ffffff20")

                            hbox:
                                spacing 12
                                text "bal: [nodo['balance']]" color cb size 14
                                text "L:[nodo['left']]  R:[nodo['right']]" color "#706050" size 14

                    # Chinche
                    frame:
                        xpos nx + NODO_W // 2 - 7  ypos ny - 8
                        xsize 14  ysize 14
                        background Solid("#cc3333")

    # Barra inferior con leyenda
    frame:
        xpos 0 ypos 1020
        xsize 1920 ysize 60
        background Solid("#00000090")
        padding (30, 10)

        hbox:
            spacing 30
            yalign 0.5

            text "LEYENDA:" color COLOR_SUBTITULO size 14 yalign 0.5

            frame:
                background Solid("#1e4d32")
                padding (10, 5)
                text "● LEVE  G≤10" color "#4a7a5a" size 13

            frame:
                background Solid("#4d3010")
                padding (10, 5)
                text "●● MODERADO  G≤20" color "#8b6a2a" size 13

            frame:
                background Solid("#4d1a1a")
                padding (10, 5)
                text "●●● GRAVE  G≤30" color "#8b3a3a" size 13

            frame:
                background Solid("#2a0d2e")
                padding (10, 5)
                text "●●●● CRÍTICO  G>30" color "#7a3a8a" size 13

            text "  |  bal = factor de balance AVL" color "#504030" size 13 yalign 0.5

            null width 40

            textbutton "Siguiente":
                action Return()
                text_color "#ffffff"
                text_size 16
                background "#3a1a1a"
                padding (14, 6)

    # Botón cerrar
    frame:
        xpos 1800 ypos 12
        xsize 110  ysize 44
        background Solid("#3a1a1a")
        padding (0, 0)

        textbutton "✕  Cerrar":
            action Hide("arbol_avl_view")
            text_color "#cc8888"
            text_size 15
            xalign 0.5 yalign 0.5


# ── Screen de reporte final ───────────────────────────────────────────────────
screen reporte_final(casos_ordenados):
    modal True
    tag reporte

    add Solid("#0d0d14")

    frame:
        xpos 80 ypos 40
        xsize 1760 ysize 1000
        background Solid("#12121e")
        padding (0, 0)

        # Encabezado
        frame:
            xpos 0 ypos 0
            xsize 1760 ysize 80
            background Solid("#1e3f66")
            padding (40, 18)
            vbox:
                text "EXPEDIENTE FINAL — CASO VALERIA" color "#9AD1FF" size 26 bold True
                text "404: GIRL NOT FOUND" color "#5a8aaa" size 16

        # Tabla de casos
        viewport:
            xpos 0 ypos 85
            xsize 1760 ysize 840
            draggable True
            mousewheel True

            vbox:
                xpos 30 ypos 20
                spacing 0

                # Encabezados
                frame:
                    xsize 1700 ysize 55
                    background Solid("#1a2a3a")
                    padding (10, 8)
                    hbox:
                        spacing 0
                        text "ID"        color "#9AD1FF" size 20 xsize 80
                        text "DELITO"    color "#9AD1FF" size 20 xsize 430
                        text "LEY"       color "#9AD1FF" size 20 xsize 460
                        text "PENA"      color "#9AD1FF" size 20 xsize 400
                        text "GRAVEDAD"  color "#9AD1FF" size 20 xsize 180

                for i, caso in enumerate(casos_ordenados):
                    python:
                        bg_row = "#0f1a24" if i % 2 == 0 else "#13202e"
                        fn, fb = color_nodo(caso.gravedad)

                    frame:
                        xsize 1700 ysize 50
                        background Solid(bg_row)
                        padding (10, 10)

                        hbox:
                            spacing 0
                            text "#[caso.id_caso]"   color "#c8c4b8" size 20 xsize 80
                            text "[caso.tipo]"        color "#e0dcc8" size 20 xsize 430
                            text "[caso.ley]"         color "#a09880" size 20 xsize 460
                            text "[caso.pena]"        color "#a09880" size 20 xsize 400
                            text "[caso.gravedad]"    color fb        size 20 xsize 180 bold True

        # Pie
        frame:
            xpos 0 ypos 930
            xsize 1760 ysize 70
            background Solid("#0a0a12")
            padding (40, 18)
            hbox:
                spacing 40
                text "Total de delitos documentados: [len(casos_ordenados)]" color "#5a7a5a" size 15 yalign 0.5
                text "Recorrido in-order (menor → mayor gravedad)" color "#404040" size 14 yalign 0.5

    textbutton "✕  Cerrar expediente":
        xpos 1760 ypos 45
        action Hide("reporte_final")
        text_color "#cc8888"
        text_size 16


# ── Screen de inventario ───────────────────────────────────────────────────

screen bandeja_inventario():
    # Esta pantalla muestra las pistas que el Jugador 1 encontró
    zorder 100 # Para que aparezca por encima de todo
    
    frame:
        xalign 0.98 yalign 0.2
        xsize 350 ysize 500
        background Solid("#1a1a1aee") # Un negro elegante semitransparente
        padding (15, 15)

        vbox:
            spacing 10
            text "BANDEJA DE EVIDENCIAS" size 22 color "#00e5ff" xalign 0.5 bold True
            
            null height 10

            if not inventario_pistas:
                text "Esperando recolección..." size 18 color "#777" italic True xalign 0.5 yalign 0.5
            else:
                viewport:
                    mousewheel True
                    scrollbars "vertical"
                    vbox:
                        spacing 8
                        for item in inventario_pistas:
                            # Botón para cada pista
                            button:
                                action [
                                    # Al dar clic, insertamos la pista en el árbol
                                    Function(investigacion.insertar_pista, item.id_delito, item.peso, item.descripcion),
                                    # La quitamos del inventario
                                    RemoveFromSet(inventario_pistas, item),
                                    # Forzamos a Ren'Py a refrescar la pantalla
                                    Function(renpy.restart)
                                ]
                                background Solid("#2c2c2c")
                                hover_background Solid("#444")
                                xfill True
                                padding (10, 10)
                                
                                vbox:
                                    text "[item.descripcion]" size 18 color "#ffffff"
                                    text "Valor AVL: [item.id_delito] | Peso: [item.peso]" size 14 color "#00e5ff"