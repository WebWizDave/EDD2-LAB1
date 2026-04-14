# ── Colores del tablero ──────────────────────────────────────────────────────
define COLOR_FONDO        = "#1a1208"   # corcho oscuro
define COLOR_TITULO       = "#c8b882"   # crema dorado
define COLOR_SUBTITULO    = "#7a6a48"   # crema apagado
define COLOR_HILO         = "#8b3a3a"   # rojo oscuro para hilos
define COLOR_NODO_TEXTO   = "#f0e8d0"   # texto de nodo

# Nodos por nivel de gravedad
define COLOR_NODO_BAJO    = "#1e4d32"   # verde oscuro  (gravedad 10)
define COLOR_NODO_MEDIO   = "#4d3010"   # ámbar oscuro  (gravedad 20)
define COLOR_NODO_ALTO    = "#4d1a1a"   # rojo oscuro   (gravedad 30)
define COLOR_NODO_CRITICO = "#2a0d2e"   # púrpura oscuro (gravedad 40)
define COLOR_BORDE_BAJO   = "#4a7a5a"
define COLOR_BORDE_MEDIO  = "#8b6a2a"
define COLOR_BORDE_ALTO   = "#8b3a3a"
define COLOR_BORDE_CRIT   = "#7a3a8a"

# ── Función Python: color según gravedad ─────────────────────────────────────
init python:
    def color_nodo(gravedad):
        if gravedad <= 10:
            return ("#1e4d32", "#4a7a5a")   # fondo, borde
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

# ── Posiciones X por nivel (precalculadas para hasta 4 niveles) ──────────────
# El canvas es 1280px ancho. Centramos los nodos manualmente.
# Cada nodo ocupa ~220px de ancho.
init python:
    NODO_W    = 210
    NODO_H    = 130
    NIVEL_Y   = [30, 200, 370, 530]   # Y de cada nivel
    # X por nivel y posición dentro del nivel
    NODO_X_POR_NIVEL = {
        0: [535],
        1: [270, 800],
        2: [140, 400, 665, 925],
        3: [75, 215, 355, 495, 640, 780, 920, 1060],
    }

    def posicion_nodo(nivel, idx_en_nivel):
        xs = NODO_X_POR_NIVEL.get(nivel, [])
        if idx_en_nivel < len(xs):
            return xs[idx_en_nivel], NIVEL_Y[nivel] if nivel < len(NIVEL_Y) else 30 + nivel * 170
        return 535, 30 + nivel * 170

    def construir_posiciones(niveles):
        """
        Retorna dict: id_caso -> (x_centro, y_centro)
        """
        pos = {}
        for nivel_idx, nivel in enumerate(niveles):
            for pos_idx, nodo in enumerate(nivel):
                x, y = posicion_nodo(nivel_idx, pos_idx)
                pos[nodo["id"]] = (x + NODO_W // 2, y + NODO_H // 2)
        return pos

# ── Screen principal del árbol ────────────────────────────────────────────────
screen arbol_avl_view(niveles):
    modal True
    tag arbol

    # Fondo corcho
    add Solid(COLOR_FONDO)

    # Canvas para los hilos (se dibuja primero, queda detrás)
    python:
        pos_map = construir_posiciones(niveles)

    # Título
    frame:
        xpos 0 ypos 0
        xsize 1280 ysize 60
        background Solid("#00000080")
        padding (30, 10)
        hbox:
            spacing 20
            text "TABLERO DE INVESTIGACIÓN" color COLOR_TITULO size 22 yalign 0.5
            text "— Árbol AVL de Casos —"   color COLOR_SUBTITULO size 14 yalign 0.5

    # Área del árbol
    viewport:
        xpos 0 ypos 65
        xsize 1280 ysize 600
        draggable True
        mousewheel True

        fixed:
            xsize 1280 ysize 650

            # ── Hilos entre nodos ────────────────────────────────────────────
            for nivel_idx, nivel in enumerate(niveles):
                for nodo in nivel:
                    if nodo["left"] is not None and nodo["left"] in pos_map:
                        python:
                            x1, y1 = pos_map[nodo["id"]]
                            x2, y2 = pos_map[nodo["left"]]
                        # Línea padre → hijo izquierdo
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
                        # Etiqueta L
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
                        # Etiqueta R
                        text "R" color "#8b6a2a" size 14 xpos (x1 + x2) // 2 - 4 ypos y1 - 18

            # ── Nodos (polaroids) ────────────────────────────────────────────
            for nivel_idx, nivel in enumerate(niveles):
                for pos_idx, nodo in enumerate(nivel):
                    python:
                        nx, ny = posicion_nodo(nivel_idx, pos_idx)
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

                        # Borde superior de color
                        frame:
                            xpos 0 ypos 0
                            xsize NODO_W ysize 5
                            background Solid(fb)

                        vbox:
                            xpos 10 ypos 8
                            spacing 4

                            # Etiqueta de gravedad
                            text etiq color fb size 11

                            # ID + tipo
                            text "ID [nodo['id']] — [tipo_t]" color COLOR_NODO_TEXTO size 13 bold True

                            # Ley
                            text "[ley_t]" color "#a09070" size 11

                            # Pena
                            text "Pena: [nodo['pena']]" color "#a09070" size 11

                            # Separador
                            frame:
                                xsize 190 ysize 1
                                background Solid("#ffffff20")

                            # Balance y altura
                            hbox:
                                spacing 12
                                text "bal: [nodo['balance']]" color cb size 11
                                text "L:[nodo['left']]  R:[nodo['right']]" color "#706050" size 11

                    # Chinche (círculo rojo arriba del nodo)
                    frame:
                        xpos nx + NODO_W // 2 - 7  ypos ny - 8
                        xsize 14  ysize 14
                        background Solid("#cc3333")

    # Barra inferior con leyenda
    frame:
        xpos 0 ypos 665
        xsize 1280 ysize 55
        background Solid("#00000090")
        padding (20, 8)

        hbox:
            spacing 30
            yalign 0.5

            text "LEYENDA:" color COLOR_SUBTITULO size 12 yalign 0.5

            frame:
                background Solid("#1e4d32")
                padding (8, 4)
                text "● LEVE  G≤10" color "#4a7a5a" size 11

            frame:
                background Solid("#4d3010")
                padding (8, 4)
                text "●● MODERADO  G≤20" color "#8b6a2a" size 11

            frame:
                background Solid("#4d1a1a")
                padding (8, 4)
                text "●●● GRAVE  G≤30" color "#8b3a3a" size 11

            frame:
                background Solid("#2a0d2e")
                padding (8, 4)
                text "●●●● CRÍTICO  G>30" color "#7a3a8a" size 11

            text "  |  bal = factor de balance AVL" color "#504030" size 11 yalign 0.5

            null width 40

            textbutton "Siguiente":
                action Return()
                text_color "#ffffff"
                text_size 14
                background "#3a1a1a"
                padding (10, 5)
           

    # Botón cerrar
    frame:
        xpos 1180 ypos 10
        xsize 90  ysize 40
        background Solid("#3a1a1a")
        padding (0, 0)

        textbutton "✕  Cerrar":
            action Hide("arbol_avl_view")
            text_color "#cc8888"
            text_size 14
            xalign 0.5 yalign 0.5

# ── Screen de reporte final ───────────────────────────────────────────────────
screen reporte_final(casos_ordenados):
    modal True
    tag reporte

    add Solid("#0d0d14")

    frame:
        xpos 80 ypos 40
        xsize 1120 ysize 640
        background Solid("#12121e")
        padding (0, 0)

        # Encabezado
        frame:
            xpos 0 ypos 0
            xsize 1120 ysize 70
            background Solid("#1e3f66")
            padding (30, 15)
            vbox:
                text "EXPEDIENTE FINAL — CASO VALERIA" color "#9AD1FF" size 20 bold True
                text "CyberDetective: El Árbol de la Verdad" color "#5a8aaa" size 13

        # Tabla de casos
        viewport:
            xpos 0 ypos 75
            xsize 1120 ysize 510
            draggable True
            mousewheel True

            vbox:
                xpos 30 ypos 20
                spacing 0

                # Encabezados
                frame:
                    xsize 1060 ysize 35
                    background Solid("#1a2a3a")
                    padding (10, 6)
                    hbox:
                        spacing 0
                        text "ID"        color "#9AD1FF" size 13 xsize 60
                        text "DELITO"    color "#9AD1FF" size 13 xsize 280
                        text "LEY"       color "#9AD1FF" size 13 xsize 300
                        text "PENA"      color "#9AD1FF" size 13 xsize 260
                        text "GRAVEDAD"  color "#9AD1FF" size 13 xsize 120

                for i, caso in enumerate(casos_ordenados):
                    python:
                        bg_row = "#0f1a24" if i % 2 == 0 else "#13202e"
                        fn, fb = color_nodo(caso.gravedad)

                    frame:
                        xsize 1060 ysize 45
                        background Solid(bg_row)
                        padding (10, 8)

                        hbox:
                            spacing 0
                            text "#[caso.id_caso]"   color "#c8c4b8" size 13 xsize 60
                            text "[caso.tipo]"        color "#e0dcc8" size 13 xsize 280
                            text "[caso.ley]"         color "#a09880" size 13 xsize 300
                            text "[caso.pena]"        color "#a09880" size 13 xsize 260
                            text "[caso.gravedad]"    color fb        size 13 xsize 120 bold True

        # Pie
        frame:
            xpos 0 ypos 585
            xsize 1120 ysize 55
            background Solid("#0a0a12")
            padding (30, 12)
            hbox:
                spacing 30
                text "Total de delitos documentados: [len(casos_ordenados)]" color "#5a7a5a" size 13 yalign 0.5
                text "Recorrido in-order (menor → mayor gravedad)" color "#404040" size 12 yalign 0.5

    textbutton "✕  Cerrar expediente":
        xpos 1120 ypos 45
        action Hide("reporte_final")
        text_color "#cc8888"
        text_size 14
