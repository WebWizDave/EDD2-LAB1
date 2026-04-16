# ── Personajes ────────────────────────────────────────────────────────────────
default alex_tipo = "m"  # "m" para masculino, "f" para femenino, "n" para neutro
define alex    = Character("Alex",     color="#9AD1FF", what_slow_cps = 40, callback=name_callback, cb_name="alex")
define valeria = Character("Valeria",  color="#ffb3c6", what_slow_cps = 35, callback=name_callback, cb_name="valeria")
define rector  = Character("Director", color="#aaaaaa", what_slow_cps = 30, callback=name_callback, cb_name="rector")
define sistema = Character("SISTEMA",  color="#cc4444", what_slow_cps = 25)

# ── Placeholders de personajes ────────────────────────────────────────────────
image alex_cuerpo = ConditionSwitch(
    "alex_tipo == 'm'", "m_alex_cuerpo.png",
    "alex_tipo == 'f'", "f_alex_cuerpo.png",
    "alex_tipo == 'n'", "n_alex_cuerpo.png",
)

image alex_normal = ConditionSwitch(
    "alex_tipo == 'm'", "m_alex_normal.png",
    "alex_tipo == 'f'", "f_alex_normal.png",
    "alex_tipo == 'n'", "n_alex_normal.png",
)

image alex_serio = ConditionSwitch(
    "alex_tipo == 'm'", "m_alex_serio.png",
    "alex_tipo == 'f'", "f_alex_serio.png",
    "alex_tipo == 'n'", "n_alex_serio.png",
)

layeredimage alex:
    at sprite_highlight('alex')
    always:
        "alex_cuerpo"
    group expresion:
        attribute normal:
            "alex_normal"
        attribute serio:
            "alex_serio"
layeredimage valeria:
    at sprite_highlight('valeria')
    always:
        "valeria_cuerpo.png"
    always:
        "valeria_uniforme.png"
    always:
        "valeria_zapatos.png"
    group expresion:
        attribute triste:
            "valeria_triste.png"
        attribute normal:
            "valeria_normal.png"
layeredimage rector:
    at sprite_highlight('rector')
    always:
        "rector_cuerpo.png"
    group expresion:
        attribute neutral:
            "rector_neutral.png"

# ── Fondos ────────────────────────────────────────────────────────────────────
image bg_oficina   = im.Scale("bg_oficina.png", 1920, 1080)
image bg_salon     = im.Scale("bg_salon.png", 1920, 1080)
image bg_pasillo   = im.Scale("bg_pasillo.png", 1920, 1080)
image bg_ciudad = im.Scale("bg_ciudad.png", 1920, 1080)
image bg_director = im.Scale("bg_director.png", 1920, 1080)

# ─────────────────────────────────────────────────────────────────────────────
label start:
    
    # ── INTRODUCCIÓN ──────────────────────────────────────────────────────────
    play music "audio/musica_fondo.mp3" fadein 1.0

    # ── MENÚ DE GUÍA INICIAL ──────────────────────────────────────────────────────
label menu_tutorial:
    scene bg_salon 
    
    menu:
        sistema "SISTEMA NETCITY INICIADO. Seleccione un módulo de información:"

        "1. Las reglas del juego":
            sistema "Tu objetivo es construir un expediente sólido clasificando correctamente los casos de ciberacoso de Valeria."
            sistema "Deberás emparejar cada situación con su delito correspondiente, la ley colombiana que lo penaliza y su nivel de gravedad."
            sistema "Solo los casos correctamente clasificados serán admitidos en la estructura de datos de la investigación."
            jump menu_tutorial

        "2. Cómo funciona el árbol de datos (Árbol AVL)":
            sistema "El núcleo de este sistema es un Árbol Binario de Búsqueda Balanceado (AVL)."
            sistema "Cada caso se inserta como un nodo. El valor clave para organizarlos es el nivel de 'gravedad' del delito (10, 20, 30 o 40)."
            sistema "Si la diferencia de altura entre el lado izquierdo y derecho de un nodo supera 1 o es menor a -1, el sistema se desbalancea."
            sistema "Para corregirlo y mantener las búsquedas optimizadas, el árbol ejecutará rotaciones automáticas (simples o dobles, hacia la izquierda o derecha)."
            sistema "Al finalizar el juego, el sistema usará un 'recorrido in-order' para generar tu reporte final, ordenando los delitos desde el menos grave hasta el más severo."
            jump menu_tutorial

        "3. Cómo investigar cada caso":
            sistema "1. Escucha el testimonio para entender el contexto."
            sistema "2. Analiza las opciones de evidencia y selecciona las que prueben el delito."
            sistema "3. Determina el tipo de delito (Injuria, Calumnia, Suplantación, etc.)."
            sistema "Si te equivocas en la gravedad, la evidencia o la ley, la inserción en el árbol fallará y deberás reevaluar el caso."
            jump menu_tutorial

        "Todo claro. Iniciar partida":
            sistema "Cargando primer caso... Preparando raíz del árbol..."
    
    # ── MENÚ DE SELECCIÓN INCLUSIVA ──────────────────────────────────────────
    scene bg_ciudad with fade
    "SISTEMA: Configurando interfaz de usuario y perfil del agente..."

    menu:
        "Selecciona la apariencia del Detective Alex para esta investigación:"

        "Perfil A (Masculino)":
            $ alex_tipo = "m"
            "Perfil Alfa seleccionado."

        "Perfil B (Femenino)":
            $ alex_tipo = "f"
            "Perfil Beta seleccionado."

        "Perfil C (No Binario)":
            $ alex_tipo = "n"
            "Perfil Gamma seleccionado."

    # ── INTRODUCCIÓN CON EL DETECTIVE YA CONFIGURADO ──────────────────────────
    show alex normal at center with dissolve

    alex "NetCity. Una ciudad donde todo ocurre en pantallas."
    alex "Y donde los crímenes también."

    show alex serio at center
    alex "Llevo semanas recibiendo reportes sobre una estudiante: Valeria."
    alex "Lo que al principio parecían bromas... se convirtió en algo más oscuro."
    alex "Mi trabajo es organizar la evidencia. Clasificar cada delito."
    alex "Para eso uso mi sistema: un árbol AVL. Cada caso tiene su lugar."
    alex "Comencemos."

    hide alex with dissolve

    # ─────────────────────────────────────────────────────────────────────────
    # NIVEL 1 — INJURIA
    # ─────────────────────────────────────────────────────────────────────────
    scene bg_salon with fade
    show alex normal at left with dissolve
    show valeria triste at right with dissolve

    alex "Nivel 1 — Las primeras señales."
    valeria "Alex... llevo semanas recibiendo mensajes. Me dicen cosas horribles directamente."
    valeria "No son bromas. Son insultos deliberados, repetidos, para humillarme."

    show alex serio at left
    alex "¿Tienes capturas? ¿Sabes quién es el usuario?"

    show valeria normal at right
    valeria "Tengo capturas del chat y el nombre de usuario. Pero no sé a qué ley corresponde."

    show alex normal at left
    alex "Eso es lo que voy a determinar. Analicemos la evidencia."

    hide valeria with dissolve

    python:
        ok1 = jugar_caso(
            id_caso             = 1,
            descripcion         = "Mensajes ofensivos repetidos hacia Valeria",
            opciones_delito     = ["Injuria", "Calumnia", "Suplantación", "Hostigamiento"],
            respuesta_delito    = "Injuria",
            ley                 = "Art. 220 Código Penal",
            pena                = "Multa",
            gravedad_correcta   = 10,
            evidencias_opciones = [
                "Captura de pantalla del chat",
                "Usuario/ID del agresor",
                "Link a la publicación",
            ],
            evidencias_correctas = {
                "Captura de pantalla del chat",
                "Usuario/ID del agresor",
            },
            modo_estricto = True,
        )

    if ok1:
        show alex serio at left
        alex "Correcto. Mensajes que dañan el buen nombre: Injuria, Artículo 220."
        alex "Caso insertado en el árbol. Gravedad 10 — primer nodo, raíz inicial."

        python:
            niveles = exportar_por_niveles(investigacion)

        hide alex with dissolve
        call screen arbol_avl_view(niveles)

        scene bg_salon with fade
        show alex normal at left with dissolve
        alex "Así se ve el árbol ahora. Un solo nodo. La investigación comienza."
        hide alex with dissolve

    else:
        show alex serio at left
        sistema "Clasificación incorrecta. Delito, gravedad o evidencias no coinciden."
        alex "Necesito ser más cuidadoso. Revisemos desde el principio."
        hide alex with dissolve
        jump start

    # ─────────────────────────────────────────────────────────────────────────
    # NIVEL 2 — CALUMNIA
    # ─────────────────────────────────────────────────────────────────────────
    scene bg_pasillo with fade
    show alex normal at left with dissolve
    show valeria triste at right with dissolve

    alex "Nivel 2 — El rumor viral."
    valeria "Ahora están publicando cosas falsas sobre mí en redes sociales."
    valeria "Dicen que hice cosas que nunca ocurrieron. Lo comparten en todo el colegio."

    hide valeria with dissolve
    hide alex with dissolve
    scene bg_director with fade
    show alex normal at left with dissolve
    show rector neutral at right with dissolve

    rector "Detective, no exageremos. Son chicos. Estas cosas pasan."

    show alex serio at left
    alex "Director, difundir acusaciones falsas que dañan la reputación tiene nombre legal."
    alex "Necesito rastrear el origen y confirmar la falsedad."

    hide rector with dissolve

    python:
        ok2 = jugar_caso(
            id_caso             = 2,
            descripcion         = "Publicaciones falsas que dañan la reputación de Valeria",
            opciones_delito     = ["Injuria", "Calumnia", "Suplantación", "Hostigamiento"],
            respuesta_delito    = "Calumnia",
            ley                 = "Art. 221 Código Penal",
            pena                = "Multa / sanción",
            gravedad_correcta   = 20,
            evidencias_opciones = [
                "Captura de la publicación falsa",
                "Rastreo del origen (primer post)",
                "Testimonio de un compañero",
            ],
            evidencias_correctas = {
                "Captura de la publicación falsa",
                "Rastreo del origen (primer post)",
            },
            modo_estricto = True,
        )

    if ok2:
        show alex serio at left
        alex "Calumnia. Artículo 221. Esto ya no es una broma."
        alex "Al insertar este nodo con gravedad 20, el árbol puede necesitar reequilibrarse."

        python:
            niveles = exportar_por_niveles(investigacion)

        hide alex with dissolve
        call screen arbol_avl_view(niveles)

        scene bg_pasillo with fade
        show alex normal at left with dissolve
        alex "¿Ves cómo el árbol mantiene su balance? Eso es el AVL en acción."
        hide alex with dissolve

    else:
        show alex serio at left
        sistema "Clasificación incorrecta. Revisa el tipo de delito y las evidencias."
        hide alex with dissolve
        jump start

    # ─────────────────────────────────────────────────────────────────────────
    # NIVEL 3 — SUPLANTACIÓN
    # ─────────────────────────────────────────────────────────────────────────
    scene bg_salon with fade
    show alex serio at left with dissolve
    show valeria triste at right with dissolve

    alex "Nivel 3 — La cuenta fantasma."
    valeria "Apareció un perfil falso con mis fotos. Está publicando cosas horribles."
    valeria "La gente cree que soy yo. Me escriben diciéndome cosas terribles."

    show alex normal at left
    alex "Esto ya es un delito informático. La Ley 1273 cubre exactamente este caso."
    alex "Necesito evidencia del perfil y del daño causado."

    hide valeria with dissolve

    python:
        ok3 = jugar_caso(
            id_caso             = 3,
            descripcion         = "Perfil falso con fotos de Valeria publicando contenido ofensivo",
            opciones_delito     = ["Injuria", "Calumnia", "Suplantación", "Hostigamiento"],
            respuesta_delito    = "Suplantación",
            ley                 = "Ley 1273 de 2009",
            pena                = "Prisión 48-96 meses",
            gravedad_correcta   = 30,
            evidencias_opciones = [
                "Captura del perfil falso",
                "Rastreo de la dirección de creación",
                "Publicaciones del perfil falso",
            ],
            evidencias_correctas = {
                "Captura del perfil falso",
                "Rastreo de la dirección de creación",
            },
            modo_estricto = True,
        )

    if ok3:
        show alex serio at left
        alex "Suplantación de identidad. Ley 1273. Pena de hasta 96 meses."
        alex "Este nodo tiene gravedad 30. El árbol necesitará una rotación."

        python:
            niveles = exportar_por_niveles(investigacion)

        hide alex with dissolve
        call screen arbol_avl_view(niveles)

        scene bg_salon with fade
        show alex normal at left with dissolve
        alex "¿Ves cómo el árbol se reorganizó para mantenerse balanceado?"
        alex "Eso es exactamente lo que hace el algoritmo AVL automáticamente."
        hide alex with dissolve

    else:
        show alex serio at left
        sistema "Clasificación incorrecta."
        hide alex with dissolve
        jump start

    # ─────────────────────────────────────────────────────────────────────────
    # NIVEL 4 — ATAQUE COORDINADO
    # ─────────────────────────────────────────────────────────────────────────
    scene bg_ciudad with fade
    show alex serio at left with dissolve
    show valeria triste at right with dissolve

    alex "Nivel 4 — El ataque coordinado."
    valeria "Son muchas cuentas ahora. Atacan al mismo tiempo. No puedo con esto."

    show valeria normal at right
    valeria "¿Cuándo va a terminar esto, Alex?"

    show alex normal at left
    alex "Encontré un patrón. Todas las cuentas tienen el mismo comportamiento."

    show alex serio at left
    alex "Es hostigamiento digital coordinado. Ley 1010."
    alex "Este es el nodo más grave que hemos visto."

    hide valeria with dissolve

    python:
        ok4 = jugar_caso(
            id_caso             = 4,
            descripcion         = "Múltiples cuentas atacando a Valeria de forma coordinada",
            opciones_delito     = ["Injuria", "Calumnia", "Suplantación", "Hostigamiento"],
            respuesta_delito    = "Hostigamiento",
            ley                 = "Ley 1010 de 2006",
            pena                = "Sanción penal + proceso judicial",
            gravedad_correcta   = 40,
            evidencias_opciones = [
                "Registro de cuentas atacantes",
                "Patrón de comportamiento coordinado",
                "Testimonio de Valeria",
            ],
            evidencias_correctas = {
                "Registro de cuentas atacantes",
                "Patrón de comportamiento coordinado",
            },
            modo_estricto = True,
        )

    if ok4:
        show alex serio at left
        alex "Hostigamiento digital. El caso más grave del expediente."

        python:
            niveles = exportar_por_niveles(investigacion)

        hide alex with dissolve
        call screen arbol_avl_view(niveles)

        scene bg_ciudad with fade
        show alex normal at left with dissolve
        alex "El árbol ahora tiene cuatro nodos. Mira la estructura completa."
        alex "Cada rotación que hizo el AVL mantuvo la búsqueda eficiente."
        hide alex with dissolve

    else:
        show alex serio at left
        sistema "Clasificación incorrecta."
        hide alex with dissolve
        jump start

    # ─────────────────────────────────────────────────────────────────────────
    # NIVEL FINAL — REPORTE
    # ─────────────────────────────────────────────────────────────────────────
    scene bg_oficina with fade
    show alex serio at left with dissolve
    show rector neutral at right with dissolve

    alex "Es momento de presentar el expediente completo."
    rector "Detective... ¿qué tan grave es?"

    show alex normal at left
    alex "Usaré el recorrido in-order del árbol: de menor a mayor gravedad."
    alex "Así queda documentada la escalada del acoso, del primer insulto al ataque final."

    hide rector with dissolve
    show valeria normal at right with dissolve

    valeria "¿De verdad van a hacer algo esta vez?"

    show alex serio at left
    alex "Esta vez hay pruebas. Cuatro delitos. Cuatro leyes colombianas violadas."

    python:
        casos_reporte = investigacion.obtener_lista_ordenada()

    hide alex with dissolve
    hide valeria with dissolve
    call screen reporte_final(casos_reporte)

    scene bg_oficina with fade
    show alex normal at left with dissolve
    show valeria normal at right with dissolve
    show rector neutral at center with dissolve

    rector "Detective... esto es más grave de lo que pensaba."
    alex "Exactamente. Por eso la institución no puede mirar hacia otro lado."
    valeria "Gracias. Por primera vez alguien tomó esto en serio."

    show alex serio at left
    alex "La próxima vez que alguien diga que el ciberacoso no es grave..."
    alex "Muéstrale este árbol."

    hide alex with dissolve
    hide valeria with dissolve
    hide rector with dissolve

    return
