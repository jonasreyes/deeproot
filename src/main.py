"""
DeepRoot - main.py
Versión: 0.1.0
Copyright (C) 2025 Jonás Reyes

Este programa es software libre: puedes redistribuirlo y/o modificarlo
bajo los términos de la Licencia de Software Libre de DeepRoot.
Más detalles en: https://github.com/jonasreyes/deeproot/blob/main/LICENSE.

Este programa se distribuye SIN GARANTÍA; sin siquiera la garantía implícita
de COMERCIALIZACIÓN o IDONEIDAD PARA UN PROPÓSITO PARTICULAR.
Consulta la licencia para más detalles.

Descripción:
Esta aplicación es un cliente de escritorio y móvil para facilitar el acceso y disfrute del Servicio API de DeepSeek. Se requiere de un token de DeepSeek Platform para poder funcionar. Es un desarrollo independiente, inspirado en los valores del Software Libre en Venezuela. Es resultado de los incentivos éticos de la Universidad Bolivariana de Venezuela y la Comunidad de Canaima GNU/Linux.

Licencia:
DeepRoot se distribuye bajo la [Licencia DeepRoot](LICENSE.md), compatible con GPL.  
Este código es libre y debe permanecer así. Si realizas modificaciones o derivados, debes mencionar al autor original (yo) y mantener esta misma licencia.

Contacto:
- Canal de Telegram: t.me/jonasroot (comenta una publicación)
- Repositorio: https://github.com/jonasreyes/deeproot.git

"La verdadera inteligencia no solo resuelve problemas, sino que cultiva la vida..."
#PatriaYSoftwareLibre
"""

from modules import instrucciones
from modules.utilidades import *
import openai
from openai import OpenAIError, APIConnectionError, APIError
import flet as ft
import asyncio
import json
import os
import platform
import shutil
import modules.themes as themes
import acerca
from modules.interfaz import *
import locale
from datetime import datetime
import urllib.parse
from flet import FilePicker, FilePickerResultEvent
import markdown
from modules import themes as tm
from modules.interfaz import GestorConversacion


# hora para la IA
def get_hoy(para_ia=True):
    hoy = datetime.now()
    if para_ia:
        fecha_de_hoy = hoy.strftime("(Fecha Actual Incorporada en el Historial de la IA al inicio de la conversación con el usuario: %A %d de %B del año %Y. Hora Actual: %I:%M%p. Horario en base a la locación: Caracas, Venezuela.)")
    else:
        fecha_de_hoy = hoy.strftime("(Fecha Actual Concatenada al inicio de cada prompt del usuario: %A %d de %B del año %Y. Hora Actual: %I:%M%p. Horario en base a la locación: Caracas, Venezuela.)")
    return fecha_de_hoy

# ARCHIVO DE CONFIGURACIÓN
# creamos directorio de configuración

sistema = platform.system()
if sistema == "Linux" and "ANDROID_ARGUMENT" in os.environ:
    config_dir = "./config/"
else:
    config_dir = get_directorio_configuracion()
    os.makedirs(config_dir, exist_ok=True)

# Si no existe el archivo de configuración de deeproot lo creamos.
CONFIG_FILE = os.path.join(config_dir,"deeproot.json")

# Carga de configuración inicial desde archivo
def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "usar_enter": False,
        "modelo": "deepseek-chat",
        "theme_mode": "ft.ThemeMode.LIGHT",
        "code_theme": "gruvbox-light",
        "code_theme_claro": "gruvbox-light",
        "code_theme_oscuro": "gruvbox-dark",
        "extension_set": "gitHubWeb",
        "api_key": "",
        "url_base": "",
        "stream": True,
        "max_tokens": 8192, # por defecto usa 4096, otros números: 2048, 1024, 512
        "temperature":0.0 
    }

# Guardar configuración
def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Cargar configuración e inicialización de variables importantes
config = cargar_configuracion()

# Interfáz gráfica con Flet
# Configuración de la API de DeepSeek
APP_NAME = "DeepRoot"
APP_VERSION = "Alfa 0.0.1 - 2025"
APP_LEMA = "Cliente DeepSeek API"
AUTOR_NAME = "Jonás A. Reyes C."
AUTOR_NICK = "@jonasroot"
AUTOR_CONTACT = "Telegram: @jonasreyes"
AUTOR_BLOG = "https://jonasroot.t.me"
LICENCIA = "GNU/GPL V3"
EXTENSION_SET = config["extension_set"]
CODE_THEME_CLARO = config["code_theme_claro"]
CODE_THEME_OSCURO = config["code_theme_oscuro"]
CODE_THEME = CODE_THEME_CLARO

# Configuración del Historial de conversación
HISTORIAL_LONGITUD_MAX = 100
CONVERSACIONES_MAX_A_ELIMINAR = 20
INSTRUCCIONES_LONGITUD = 30

# Otras Variables Globales
auto_scroll_activo = True

# Contador para actualizar cada N Chunks
contador_chunk = 0 

# ajustes / personalización del modelo IA
async def main(page):

    gc = GestorConversacion(page)

    # Configuración del theme inicial
    dr_platform = get_platform(page, APP_NAME, APP_LEMA)
    locale.setlocale(locale.LC_TIME, 'es_VE.UTF-8') if dr_platform != "macos" else None #Deshabilitamos la localización profunda si el se deeproot se ejecuta desde MacOS ya que este sistema da problemas con locale.
    page.window.center()
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1024
    page.window.height = 768
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.locale_configuration = ft.Locale("es", "VE")

    # Gestión del Scroll - dándole usabilidad

    def on_scroll(e: ft.OnScrollEvent):
        global auto_scroll_activo

        if e.event_type == "user":
            auto_scroll_activo = False
            campo_respuesta.auto_scroll = False
            btn_ir_al_inicio.visible = True
            btn_ir_al_final.visible = True
            btn_scroll_mover_manual.visible = True
            btn_scroll_reactivar.visible = True
            #print("Auto-scroll desactivada (usuario interactuando.)")

        elif e.pixels == e.max_scroll_extent:
            auto_scroll_activo = True
            campo_respuesta.auto_scroll = True
            btn_ir_al_inicio.visible = False
            btn_ir_al_final.visible = False
            btn_scroll_mover_manual.visible = True
            btn_scroll_reactivar.visible = True
            #print("Auto-scroll reactivado (usuario en el final)")

        page.update()

    async def actualizar_interfaz():
        if auto_scroll_activo:
            campo_respuesta.scroll_to(offset=-1)
        page.update()
        await asyncio.sleep(0)

    def reactivar_auto_scroll(e):
        global auto_scroll_activo
        auto_scroll_activo = True
        campo_respuesta.auto_scroll = True
        campo_respuesta.scroll_to(offset=-1)
        # Actualización de visibilidad de botones scroll
        #btn_ir_al_inicio.visible = False
        #btn_ir_al_final.visible = False
        btn_scroll_mover_manual.visible = True
        btn_scroll_reactivar = False
        page.update()

    def mover_scroll_manual(e):
        global auto_scroll_activo

        # Desactivamos auto_scroll antes de usar scroll_to
        auto_scroll_activo = False
        campo_respuesta.auto_scroll = False

        # Actualización de visibilidad de botones scroll
        #btn_ir_al_inicio.visible = True
        #btn_ir_al_final.visible = True
        btn_scroll_mover_manual.visible = False
        btn_scroll_reactivar = True
        # movemos manualmente el scroll
        campo_respuesta.scroll_to(offset=500) # mover a 500 px
        page.update()

    # creamos una referencia a todos los elementos markdown.
    ref_cont_burbuja_usuario = ft.Ref[ft.Container]()
    ref_cont_burbuja_ia = ft.Ref[ft.Container]()
    ref_md_burbuja_ia = ft.Ref[ft.Markdown]()
    ref_md_acerca = ft.Ref[ft.Markdown]()

    # en futura actualización facilitaré la personalización completa del theme.
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density = ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary = tm.Color.AzulMincyt,
            secondary = ft.Colors.ORANGE,
            background = ft.Colors.GREY_900,
            surface = ft.Colors.GREY_800
        )
    )

    # Componentes de la interfáz
    barra_app = ft.AppBar(
        title=ft.Text(APP_NAME, size=22, color=tm.Color.BeigeFuturo, weight=ft.FontWeight.W_900),
        bgcolor=tm.Color.AzulMincyt, # Azul Mincyt
        actions=[
            ft.IconButton(ft.Icons.BRIGHTNESS_4 if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.BRIGHTNESS_7,
                          on_click=lambda e: cambiar_theme(),
                          tooltip="Cambiar Tema"
                          ),
            ft.IconButton(ft.Icons.CLOSE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.CLOSE,
                          on_click=lambda e: on_cerrar_click(e),
                          tooltip="Cerrar DeepRoot"
                          ),
        ]
    )
    page.appbar = barra_app

    barra_pie = ft.BottomAppBar(
        bgcolor=tm.Color.AzulMincyt,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),
            ]
        ),
    )
    page.bottom_appbar = barra_app

    ref_row_aviso = ft.Ref[ft.Row]()
    contenedor_respuesta_prompt_md = get_aviso(ref_row_aviso)

    # arreglo para almacenar conversación (chat con la ia)
    fecha_de_hoy = get_hoy()
    historial_conversacion = instrucciones.instrucciones

    # Función de limpieza del historial
    def limpiar_historial():
        global HISTORIAL_LONGITUD_MAX,CONVERSACIONES_MAX_A_ELIMINAR, INSTRUCCIONES_LONGITUD

        if len(historial_conversacion) > HISTORIAL_LONGITUD_MAX: # Limpiaremos los 10 primeros mensajes después de las instrucciones, siempre que hayan mas de 50 mensajes en historial
            for _ in range(CONVERSACIONES_MAX_A_ELIMINAR):
                historial_conversacion.pop(INSTRUCCIONES_LONGITUD) # Eliminamos desde la posición 30 para evitar borrar las instrucciones iniciales al modelo (user:system) que ocupan los primeros 30 mensajes.
            page.open(ft.SnackBar(ft.Text(f"Se han eliminado automáticamente los {CONVERSACIONES_MAX_A_ELIMINAR} mensajes más antiguos del historial."), bgcolor=tm.Color.TeMincyt))

    # referencia para scroll de respuesta
    # refactorizar próximamente
    campo_respuesta_ref = ft.Ref[ft.ListView]()

    # str: Campo de salida de la respuesta de la IA, el estilo y formato se dará desde la fución ectualizar_markdown()
    campo_respuesta = ft.ListView(
        ref=campo_respuesta_ref,
        controls=[
            contenedor_respuesta_prompt_md, # próximamente incluir Imágen Logotipo de DeepRoot
        ],
        expand=True,
        spacing=10,
        on_scroll=on_scroll,
        auto_scroll = True
    )

    # Función Actualizar Markdown
    def actualizar_markdown(campo, code_theme=CODE_THEME, extension_set="gitHubWeb", selectable=True, auto_follow_links=True):
        campo.extension_set = extension_set
        campo.code_theme = code_theme
        campo.selectable = selectable
        campo.auto_follow_links = auto_follow_links
        campo.update()

    # Actualizar los elementos markdown que tengar referencia
    def actualizar_markdown_ref(ref,code_theme):
        print(f"ref.current: {ref.current}")
        ref.current.code_theme = code_theme
        ref.current.update()

    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # Función de construcción de la burbuja Chat
    def burbuja_mensaje(mensaje, es_usuario, ref_cont_burbuja_ia=ref_cont_burbuja_ia, ref_cont_burbuja_usuario=ref_cont_burbuja_usuario, ref_md_burbuja_ia=ref_md_burbuja_ia):
        theme_mode = "light" if page.theme_mode == ft.ThemeMode.LIGHT else "dark"
        return gc.crear_burbuja(mensaje, es_usuario, theme_mode, ref_cont_burbuja_ia, ref_cont_burbuja_usuario, ref_md_burbuja_ia)
        


    # enviar_prompt :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Enviando consulta de usuarios a la API IA
    async def enviar_prompt(e):
        """Envía la consulta del usuario y gestiona la conversación."""

        # Verificamos que la app está configurada con un token de la API
        if not config["api_key"]:
            page.open(ft.SnackBar(ft.Text("Error: API Key no configurada."), bgcolor=tm.Color.RojoFuturo))
            input_prompt.focus()
            page.update()
            return

        prompt = input_prompt.value.strip()
        if not prompt:
            plataforma_actual=page.platform.value
            page.open(ft.SnackBar(ft.Text("Por favor, escribe una consulta."), bgcolor=tm.Color.RojoFuturo))
            input_prompt.focus()
            page.update()
            return


        # Verificamos si el aviso de bienvenida existe y lo eliminamos.
        if ref_row_aviso.current in campo_respuesta.controls:
            campo_respuesta.controls.remove(ref_row_aviso.current)
            campo_respuesta.update()

        # Agregamos en msj del usuario al Chat.
        # campo_respuesta.controls.clear() # Se comenta este llamado debido a que es importante tener 
        # |-> el historial al menos en pantalla. Puede pensarse en otra estratégia para mantener limpia la interfáz
        # |-> sin tener que desacer el historial.

        respuesta_temprana=burbuja_mensaje(prompt,es_usuario=True)
        campo_respuesta.controls.append(respuesta_temprana)
        input_prompt.value = ""
        input_prompt.disabled = True


        # evitar que el input_prompt vuelva a tener foco automatico en huespedes móviles, ya que activa el teclado en pantalla y es molesto.
        # en un dipositivo móvil el foco siempre está al alcance de los dedos, por eso el autofoco solo debe ser para huespedes de escritorio.
        input_prompt.focus() if dr_platform in ["macos","windows", "linux"] else None

        # conectamos 
        resp = await get_respuesta_ia(page, prompt, campo_respuesta)

    # get_respuesta_ia ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Inicializando cliente OpenAI
    async def get_respuesta_ia(page, prompt, campo_respuesta):
        """Genera la respuesta de la IA."""

        global contador_chunk, usuario_manejo_scroll

        try:
            client = openai.OpenAI(api_key=config["api_key"], base_url=config["url_base"])

            # obtenemos la fecha y hora actual para dar información de contexto temporal a la IA
            prompt_oculto = generar_prompt_oculto(prompt, config)

            # mensajes de configuración DeepRoot
            historial_conversacion.append({"role": "user", "content": f"{prompt_oculto}"})

            # Creamos la variable 'respuesta_temporal_para_historial'
            respuesta_temporal_para_historial = [""]

            # Avatar y Barra de Progreso temporales
            indicador_de_carga = ft.ProgressBar()
            # Añadimos el avatar y la barra de progreso al campo_respuesta

            campo_respuesta.controls.append(indicador_de_carga)
            page.update()
            await asyncio.sleep(0)

            # preparamos la burbuja de mensaje vacía para luego añadir la respuesta de la IA.
            respuesta_ia_burbuja = burbuja_mensaje("", es_usuario=False)
            campo_respuesta.controls.remove(indicador_de_carga) # eliminamos el indicador_de_carga temporal, de manera inperceptible para el usuario

            # Añadimos a campo_respuesta la burbuja para la respuesta de la IA, se cargará asícronamente.
            campo_respuesta.controls.append(respuesta_ia_burbuja)
            page.update()
            await asyncio.sleep(0)

            # Obtenemos la respuesta de la IA en streaming
            respuesta = client.chat.completions.create(
                model=config["modelo"],
                messages=historial_conversacion,
                temperature=config["temperature"],
                stream=config["stream"],
                max_tokens=config["max_tokens"]
            )

            # Procesar cada chunk de la respuesta
            for chunk in respuesta:
                if chunk.choices[0].delta.content:
                    chunk_texto = chunk.choices[0].delta.content
                    respuesta_ia_burbuja.controls[0].content.value += chunk_texto
                    respuesta_temporal_para_historial[0] += chunk_texto

                    contador_chunk += 1 # Se incrementará el contador
                    if contador_chunk % 5 == 0:
                        # Si el usuario no está manejando el scroll, desplazamos automáticamente
                        # gestión usable del Scroll
                        if auto_scroll_activo:
                            campo_respuesta.auto_scroll = True
                        await actualizar_interfaz()

            # Nos aseguramos de actualizar al final si el últim batch no se mostró.
            if contador_chunk % 5 != 0:
                page.update()
            # Si la app se ejecuta un SO de escritorio devolveremos el foco luego de haber recibido respuesta.
            input_prompt.disabled = False # habilitar y deshabilitar el prompt genera el inconveniente de la perdida del foco, pero evita el envío de nuevas consultas antes de recibir la respuesta.
            input_prompt.focus() if dr_platform in ["macos","windows", "linux"] else None

            # antes del cierre del ciclo, unimos la respuesta de la ia al historial
            historial_conversacion.append({"role": "assistant", "content": respuesta_temporal_para_historial[0]})
            limpiar_historial()

            # retornamos respuesta en limpio, que no se usará por ahora, pero que puede servir más adelante.
            return respuesta_temporal_para_historial[0]

        except asyncio.TimeoutError:
            # En caso de que el servidor no responda en el tiempo especificado
            page.open(ft.SnackBar(ft.Text("Error: El servidor no respondió a tiempo. Intenta de nuevo."), bgcolor=tm.Color.RojoFuturo))
            page.update()
        except (APIError, APIConnectionError, OpenAIError) as e:
            # Manejo de errores con la API
            page.open(ft.SnackBar(ft.Text(f"Error de conexión con la IA: {str(e)}"), bgcolor=tm.Color.RojoFuturo))
            page.update()
        except Exception as e:
            # Manejo de cualquier otro error no esperado
            page.open(ft.SnackBar(ft.Text(f"Error inesperado: {str(e)}"), bgcolor=tm.Color.RojoFuturo))
            page.update()


    # max_tokens # max_tokens ## max_tokens # max_tokens ## max_tokens # max_tokens ## max_tokens # max_tokens #
    # Variable para mostrar el valor actual de max_tokens
    text_max_tokens = ft.Text(f"{config['max_tokens']} Tokens", size=20, weight="W900")
    
    # Función para manejar el cambio en el slider de max_tokens
    def max_tokens_changed(e):
        new_value = round(e.control.value)
        
        # Aseguramos que el valor mínimo sea 1
        if new_value < 1:
            page.open(ft.SnackBar(
                ft.Text("El valor mínimo del máximo de tokens (max_tokens) es 1. Por favor ingrese un número mayor."),
                bgcolor=tm.Color.RojoFuturo
            ))
        else:
            # Ajustar el valor a múltiplos de 128, excepto si es 1
            if new_value > 1:
                new_value = (new_value // 128) * 128
                if new_value < 1:
                    new_value = 1
            
            config["max_tokens"] = new_value
            text_max_tokens.value = f"{new_value} Tokens"
        
        page.update()
    
    # Función para generar el control de configuración de max_tokens
    def get_max_tokens():
        return ft.Column(
            controls=[
                ft.Divider(),
                ft.Text("Configure el Máximo de Tokens", size=16, weight="W900"),
                text_max_tokens,
                ft.Slider(
                    min=1,  # Evitar valores inválidos desde el inicio
                    max=8192,
                    divisions=64,  # Aumentar divisiones para mayor precisión
                    value=config["max_tokens"],
                    #label="{value} Tokens",
                    on_change=max_tokens_changed
                ),
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )


    # referencia de la data table
    ref_col_guia_temperatura = ft.Ref[ft.DataTable]()

    # Tabla de configuración de Temperatura
    col_guia_temperatura = ft.Column([
        ft.Text("Guía de Temperaturas en IA por Actividad", size=16, weight="W900"),
        ft.Container(
        content = ft.DataTable(
                ref=ref_col_guia_temperatura,
            columns =[
                ft.DataColumn(ft.Text("CASO DE USO")),
                ft.DataColumn(ft.Text("TEMPERATURA")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Programación / Matemáticas")),
                        ft.DataCell(ft.Text("0.0", text_align=ft.TextAlign.CENTER)),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Limpieza de Datos / Análisis de Datos")),
                        ft.DataCell(ft.Text("1.0")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Conversación General")),
                        ft.DataCell(ft.Text("1.3")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Traducción")),
                        ft.DataCell(ft.Text("1.3")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Escritura Creativa")),
                        ft.DataCell(ft.Text("1.5")),
                    ]
                ),
            ],
            heading_row_color=tm.Color.AzulCian if page.theme_mode == ft.ThemeMode.LIGHT else tm.Color.AzulEgipcio,
            heading_row_height=40,
        ),
        border_radius=10,  # Bordes redondeados
    )
    ], horizontal_alignment = ft.CrossAxisAlignment.CENTER
                                     )


    # Variable para mostrar el valor actual de temperatura
    text_temperatura = ft.Text(f"Temperatura: {config['temperature']}", size=20, weight="W900")
    
    # Función para manejar el cambio en el slider de temperatura
    def temperatura_changed(e):
        new_temperature = round(e.control.value, 1)
        config["temperature"] = new_temperature
        text_temperatura.value = f"Temperatura: {new_temperature}"
        
        page.update()
    
    # Función para generar el control de configuración de temperatura
    def get_temperatura():
        return ft.Column(
            controls=[
                ft.Divider(),
                col_guia_temperatura,
                ft.Divider(), 
                ft.Text(f"Configurar Temperatura del Modelo {config["modelo"]}", size=16, weight="W900"),
                text_temperatura,
                ft.Slider(
                    min=0,  # Evitar valores inválidos desde el inicio
                    max=2,
                    divisions=20,
                    value=str(config["temperature"]),
                    label="{value}",
                    on_change=temperatura_changed,
                ),
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )


    btn_ir_al_final = ft.FloatingActionButton(
        #text = "⬇",
        tooltip="Ir al final del Scroll",
        icon=Icons.KEYBOARD_DOUBLE_ARROW_DOWN_ROUNDED,
        on_click = lambda e: ir_al_final(),
        visible = False,
        bgcolor = ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
    )

    btn_ir_al_inicio = ft.FloatingActionButton(
        #text = "⬆",
        tooltip="Ir al incio del Scroll",
        icon=Icons.KEYBOARD_DOUBLE_ARROW_UP_ROUNDED,
        on_click = lambda e: ir_al_inicio(),
        visible = False,
        bgcolor = ft.Colors.with_opacity(0.4, ft.Colors.WHITE)
    )

    btn_scroll_reactivar = ft.FloatingActionButton(
        #text = "⬆",
        tooltip = "Reactivar Scroll-Automático",
        icon=Icons.PLAY_CIRCLE_OUTLINED,
        on_click = reactivar_auto_scroll,
        visible = False,
        bgcolor = ft.Colors.with_opacity(0.4, ft.Colors.WHITE)
    )

    btn_scroll_mover_manual = ft.FloatingActionButton(
        #text = "⬆",
        tooltip = "Activar Scroll Manual",
        icon=Icons.WAVING_HAND_OUTLINED,
        on_click = mover_scroll_manual,
        visible = False,
        bgcolor = ft.Colors.with_opacity(0.4, ft.Colors.WHITE)
    )

    def ensamblar_campo_respuesta():
        stack = ft.Stack([
            campo_respuesta,  # Chat (se mantiene en el fondo)
            ft.Container(btn_scroll_reactivar,right=50,bottom=0, width=30, height=30),
            #ft.Container(btn_ir_al_inicio,right=0,bottom=80, width=30, height=30),
            ft.Container(btn_scroll_mover_manual,right=10,bottom=0, width=30, height=30),
            #ft.Container(btn_ir_al_final,right=0,bottom=0, width=30, height=30),
        ], expand=True)

        return stack

    def ir_al_final():
        """Forzamos el scroll hasta el final"""
        campo_respuesta.scroll_to(offset=-1, duration=300)
        page.update()

    def ir_al_inicio():
        """Forzamos el scroll hasta el inicio"""
        campo_respuesta.scroll_to(offset=0, duration=300)
        page.update()

    # Alternativa para usar enter
    def on_usar_enter(e):
        config["usar_enter"]=switch_enter.value
        guardar_configuracion(config)
        input_prompt.multiline = not config["usar_enter"]
        btn_enviar.visible = not config["usar_enter"]
        input_prompt.on_submit = enviar_prompt if config["usar_enter"] else False
        if config["usar_enter"]:
            page.open(ft.SnackBar(ft.Text("¡Puedes enviar tu consulta pulsando la Tecla Enter! Botón enviar ocultado."), bgcolor=tm.Color.TeMincyt))
        else:
            page.open(ft.SnackBar(ft.Text("Desactivada opción de envío de consulta pulsando la tecla 'Enter'. Restablecido el Botón de envío."), bgcolor=tm.Color.TeMincyt))
        page.update()

    #: str: Campo de ingreso de consulta o prompt
    input_prompt = ft.TextField(
        #label="Escribe tu consulta",
        hint_text="Consultar",
        prefix_icon=ft.Icons.SEARCH,
        autofocus=True if dr_platform in ["macos","windows", "linux"] else None # No olvidar que la coma la colocaremos al inicio de la siguiente línea.
        ,expand=True,
        min_lines=1,
        max_lines=10, #2 if dr_platform != "linux" else 10
        multiline=not config["usar_enter"],
        on_submit=enviar_prompt,
        shift_enter=True,
        content_padding = ft.padding.symmetric(horizontal = 20, vertical = 20),
        text_size=18,
        border_width=0,
        border_radius=ft.border_radius.all(40),
        bgcolor= lambda e: tm.Color.AzulCian if page.theme_mode == ft.ThemeMode.LIGHT else tm.Color.AzulEgipcio,
    )

    # switch para enviar con enter
    switch_enter = ft.Switch(
        value=config["usar_enter"],
        on_change=lambda e: on_usar_enter(e)
    )

    # Lista desplegable para seleccionar el modelo
    lista_modelos = ft.Dropdown(
        value=config["modelo"],
        options=[
            ft.dropdown.Option("deepseek-chat"),
            ft.dropdown.Option("deepseek-coder"),
            ft.dropdown.Option("deepseek-reasoner"),
            ft.dropdown.Option("gemini-2.0-flash"), # Usuarios deben obtener su API Key en Google AI Studio: https://aistudio.google.com
            #ft.dropdown.Option("qwen/qwen2.5-vl-72b-instruct:free"), # Se deshabilita hasta que concluyan las pruebas con los modelos Qwen.
        ],
        on_change=lambda e: actualizar_configuracion("modelo", e.control.value),
        
    )

    # Campos de configuración
    # str: Campo para depositar el string o token api key de deepseek
    campo_api_key = ft.TextField(
        label="API Key",
        value=config["api_key"],
        password=True,
        bgcolor= lambda e: tm.Color.AzulCian if page.theme_mode == ft.ThemeMode.LIGHT else tm.Color.AzulEgipcio,
        can_reveal_password=True
    )
    # str: Campo en el que debe colocarse la dirección del servidor con el model IA a acceder por API
    campo_url_base = ft.TextField(
        label="URL Base", 
        value=config["url_base"],
        bgcolor= lambda e: tm.Color.AzulCian if page.theme_mode == ft.ThemeMode.LIGHT else tm.Color.AzulEgipcio,
    )

    # Función Guardar Configuración Avanzada
    def guardar_configuracion_avanzada(e):
        config["api_key"] = campo_api_key.value
        config["url_base"] = campo_url_base.value
        guardar_configuracion(config)
        input_prompt.disabled = False
        page.open(ft.SnackBar(ft.Text("¡Configuración Guardada!"), bgcolor=tm.Color.TeMincyt))
        page.update()

    # Boton Guardar la Configuración Avanzada!
    btn_guardar_conf = ft.ElevatedButton("Guardar", on_click=guardar_configuracion_avanzada)

    # espacio de configuración del Campo de consulta o Prompt
    tab_interfaz = ft.Column(
        [
            ft.Text("Enviar Prompt con tecla Enter", size=16, weight=ft.FontWeight.BOLD),
            switch_enter,
            #btn_guardar_conf,
            ft.Text("Próxima Versión con muchas funcionalidades de personalización de la Interfáz", size=16, weight=ft.FontWeight.BOLD),
        ],
        spacing=10
    )

    # espacio configuración API
    tab_api = ft.Column(
        [
            ft.Text("Token de Acceso al Servicio API", size=16, weight=ft.FontWeight.BOLD),
            campo_api_key,
            campo_url_base,
            btn_guardar_conf
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,  # Habilita desplazamiento si es largo el contenido
    )

    # Slider para configurar max_tokens
    campo_max_tokens = get_max_tokens()

    # Slider para configurar la temperatura del modelo
    campo_temperatura = get_temperatura()


    # espacio configuración API
    tab_config_modelo = ft.Column(
        [
            ft.Text("Seleccione un Modelo:", size=16, weight=ft.FontWeight.W_900),
            lista_modelos,
            campo_max_tokens,
            campo_temperatura,
            btn_guardar_conf
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,  # Habilita desplazamiento si es largo el contenido,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


    acercade = ft.Markdown(
        acerca.filosofia,
        extension_set=EXTENSION_SET,
        code_theme=CODE_THEME,
        selectable = True,
        auto_follow_links = True,
        ref=ref_md_acerca
    )


    ref_row_acerca_aviso = ft.Ref[ft.Row]()
    acerca_aviso = get_aviso_acerca(ref_row_acerca_aviso, acerca.resumen)


    # panel configuración modelos
    tab_acerca = ft.Column(
        [
            acerca_aviso,
            acercade,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    # Función para actualizar configuraciones
    def actualizar_configuracion(clave, valor):
        config[clave] = valor
        guardar_configuracion(config)
        page.update()

    # Función de aplicación del theme
    def aplicar_theme(theme):
        page.bgcolor = theme["background_color"]
        page.update()

    def cambiar_theme():
        # definimos los colores según de modo y el tipo de usuario
        global CODE_THEME, CODE_THEME_CLARO, CODE_THEME_OSCURO

        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            config["theme_mode"] = "ft.ThemeMode.DARK"
            CODE_THEME = CODE_THEME_OSCURO
            theme_mode = "dark"
            ref_col_guia_temperatura.current.heading_row_color = tm.Color.AzulEgipcio
            #print(f"cambiar_theme disparado - Theme Actual: ThemeMode.LIGHT")
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            config["theme_mode"] = "ft.ThemeMode.LIGHT"
            CODE_THEME = CODE_THEME_CLARO
            theme_mode = "light"
            ref_col_guia_temperatura.current.heading_row_color = tm.Color.AzulCian
            #print(f"cambiar_theme disparado - Theme Actual: ThemeMode.DARK")
            

        #actualizar_markdown_ref(ref_md_burbuja_ia,CODE_THEME)
        actualizar_markdown(acercade)
        gc.actualizar_colores_burbujas(theme_mode) # Actualiza colores y code_theme de las burbujas
        guardar_configuracion(config)
        page.update()


    # Función cerrar la app
    def cerrar_click(e):
        page.window.close()

    # Resetear prompt
    def reset_prompt(e):
        input_prompt.value = ""
        input_prompt.focus()
        page.open(ft.SnackBar(ft.Text("¡Prompt borrado!"), bgcolor=tm.Color.TeMincyt))
        page.update()

    # Resetear todos los campos
    def resetear_campos(e):
        campo_respuesta.controls.clear()
        input_prompt.value = ""
        input_prompt.disabled = False
        input_prompt.focus()
        page.open(ft.SnackBar(ft.Text("¡Ya puedes empezar una nueva conversación!"), bgcolor=tm.Color.TeMincyt))
        page.update()

    # Función para copiar el prompt al portapapeles
    def copiar_prompt(e):
        page.set_clipboard(input_prompt.value)
        page.open(ft.SnackBar(ft.Text("¡Prompt copiado al portapapeles!"), bgcolor=tm.Color.TeMincyt))
        page.update()  # Actualiza la página para mostrar el SnackBar

    # Descarga el chat 
    def descargar_chat(e:FilePickerResultEvent,path="~/"):
        ruta_chat_a_guardar = e.path
        historial_chat = get_chat()

        if ruta_chat_a_guardar:
            try:
                ahora = datetime.now()
                fecha_ahora = ahora.strftime("%Y-%m-%d_%H%M%S")
                archivo_historial_chat_md = f"{ruta_chat_a_guardar}_historial_chat_dr-{dr_platform}_con_{config['modelo']}_{fecha_ahora}.md"

                # Generamos el archivo markdown con el historial del chat
                with open(archivo_historial_chat_md, "w", encoding="utf-8") as archivo:
                    archivo.write(historial_chat)
                    print("¡Chat guardado exitosamente!")
                    page.open(ft.SnackBar(ft.Text(f"Historial de Chat con la IA {config['modelo']} se ha guardado exitosamente en '{archivo_historial_chat_md}'."), bgcolor=tm.Color.TeMincyt))
            except Exception as e:
                page.open(ft.SnackBar(ft.Text(f"Error guardando el archivo: ",e), bgcolor=tm.Color.RojoFuturo))
            page.update()


    dialogo_guardar_chat = ft.FilePicker(on_result=descargar_chat)
    page.overlay.append(dialogo_guardar_chat)

    
    # comparte el chat a correo electrónico cuando la plataforma de ejecución de la app lo permite.
    def compartir_chat_por_email(e):
        texto_markdown = get_chat()
        texto = markdown.markdown(texto_markdown, extensions=['tables'])

        ahora = datetime.now()
        fecha_ahora = ahora.strftime("%A %d de %B/%Y | %H:%M:%S Hrs.")
        asunto = f"{fecha_ahora} - Conversación con IA modelo '{config['modelo']}' con DeepRoot Cliente API para {dr_platform}."

        if "android" == dr_platform:
            url_android_ios = f"intent://send/#Intent;action=android.intent.action.SEND;type=text/plain;S.android.intent.extra.SUBJECT={urllib.parse.quote(asunto)};type=text/plain;S.android.intent.extra.TEXT={urllib.parse.quote(texto)};end;"
            page.launch_url(url_android_ios)  # Esto abrirá el diálogo de compartir en Android
        elif "linux" == dr_platform:
            url_linux = f"mailto:?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(texto)}"
            os.system(f"xdg-open '{url_linux}'")
        page.open(ft.SnackBar(ft.Text(f"Se comparte el Chat para la plataforma {dr_platform}"), bgcolor=tm.Color.TeMincyt))
        page.update()

    # Obtener el chat actual
    def get_chat(ref=actualizar_markdown_ref):
        conversaciones_text = ""
        # Recorremos los controles en campo_respuesta
        for control in campo_respuesta.controls:
            if isinstance(control, ft.Row):
                for child in control.controls:
                    if isinstance(child, ft.Container):
                        # Si el hijo es un contenedor, buscamos dentro de él
                        if isinstance(child.content, ft.Markdown):
                            conversaciones_text += child.content.value + "\n\n"
                    elif isinstance(child, ft.Markdown):
                        # Si el hijo es directamente un Markdown lo agregamos
                        conversaciones_text += child.value + "\n\n"
        return conversaciones_text

    # Copiar Respuesta al portapapeles
    def copiar_respuesta(e):
        page.set_clipboard(get_chat())
        page.open(ft.SnackBar(ft.Text("¡Respuestas copiadas al portapepeles y en formato Markdown!"), bgcolor=tm.Color.TeMincyt))
        page.update()  # Actualiza la página para mostrar el SnackBa Gestion de dialogos de confirmación

    def on_resetear_campos(e):
        def cerrar_dialogo(e):
            dlg.open=False
            page.update()

        def confirmar_resetear_campos(e):
            resetear_campos(e)
            cerrar_dialogo(e)

        # Dialogo Alerta
        dlg=ft.AlertDialog(
            modal=True,
            title=ft.Text("Por favor confirme"),
            content=ft.Text("¿Realmente desea iniciar otra conversación? No podrá recuperar las conversaciones anteriores."),
            actions=[
                ft.TextButton("Sí", on_click=confirmar_resetear_campos),
                ft.TextButton("No", on_click=cerrar_dialogo),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)
        page.update()

    # Gestion de dialogos de cierre de la app
    def on_cerrar_click(e):
        def cerrar_dialogo(e):
            dlg.open=False
            page.update()

        def confirmar_cerrar_click(e):
            cerrar_click(e)
            cerrar_dialogo(e)

        # Dialogo Alerta
        dlg=ft.AlertDialog(
            modal=True,
            title=ft.Text("Por favor confirme"),
            content=ft.Text("¿Desea cerrar DeepRoot? Al salír se borrarán las conversacioes, asegurese de haber respaldado las de su interés."),
            actions=[
                ft.TextButton("Sí", on_click=confirmar_cerrar_click),
                ft.TextButton("No", on_click=cerrar_dialogo),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dlg)
        page.update()


    # --------- Botones --------------------
    # Botón flotante de envío de consulta, se oculta cuando se decide usar la tecla enter para enviar.
    #btn_enviar = ft.FloatingActionButton(icon=ft.Icons.SEND, visible=not config["usar_enter"])
    btn_enviar = ft.IconButton(
        icon=ft.Icons.SEND,
        visible=not config["usar_enter"],
        on_click=enviar_prompt
    )

    btn_descargar_chat = get_icon_boton_prompt(
            ft.Icons.DOWNLOAD,
            tm.Color.AzulMincyt,
            'Descargar Chat',
        'Descargar Chat',lambda e:dialogo_guardar_chat.save_file()
            )

    btn_compartir_chat = get_icon_boton_prompt(
            ft.Icons.SHARE if dr_platform != "linux" else ft.Icons.ALTERNATE_EMAIL # para que esta instrucción sea válida la coma se coloca al inicio de la linea inferior #Hack @jonasroot ;-)
            ,tm.Color.AzulMincyt,
            'Compartir por Email',
            'Compartir',compartir_chat_por_email
            )

    btn_copiar_prompt = get_icon_boton_prompt(
            ft.Icons.FILE_COPY,
            tm.Color.AzulMincyt,
            'Copiar Prompt',
            'Prompt',copiar_prompt
            )

    btn_copiar_resp = get_icon_boton_prompt(
            ft.Icons.OFFLINE_SHARE_ROUNDED,
            tm.Color.AzulMincyt,
            'Copiar Respuesta',
            'Respuesta',copiar_respuesta
            )

    btn_reset_prompt = get_icon_boton_prompt(
            ft.Icons.DELETE_FOREVER_ROUNDED,
            tm.Color.NaranjaMincyt,
            'Borrar prompt',
            'Borrar',reset_prompt
            )

    btn_nuevo_chat = get_icon_boton_prompt(
            ft.Icons.WECHAT,
            'green400',
            'Nuevo Chat',
            '+Chat',on_resetear_campos
            )

    btn_cerrar = get_icon_boton_prompt(
            ft.Icons.EXIT_TO_APP,
            'red400',
            'Salir de DeepRoot',
            'Salir',on_cerrar_click
            )

    # ---------- Fin Botones ----------------


    campos_prompt = ft.Row(
        controls=[
            input_prompt,
            btn_enviar
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )

    fila_prompt = ft.Container(
        content=campos_prompt
    )

    #if dr_platform in ["windows","linux","macos"]:
    if dr_platform in ["linux"]:
        fila_prompt_botones = ft.Row(
            [
                btn_nuevo_chat,
                btn_copiar_prompt,
                btn_copiar_resp,
                btn_compartir_chat,
                btn_descargar_chat,
                btn_reset_prompt,
            ], 
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
            #scroll=ft.ScrollMode.AUTO,  # Habilita desplazamiento si es largo el contenido
        )
        page.update()
    elif dr_platform in ["windows", "macos"]: # para estos sistemas el botón "Salír" funciona. en Macos y el Windows no funciona descargar porque para linux se apoya en Zenity. Más adelantes se buscarán alternativas.
        fila_prompt_botones = ft.Row(
            [
                btn_nuevo_chat,
                btn_copiar_prompt,
                btn_copiar_resp,
                btn_compartir_chat,
                btn_reset_prompt,
            ], 
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.update()
    else:
        fila_prompt_botones = ft.Row(
            [
                btn_nuevo_chat,
                btn_copiar_prompt,
                btn_copiar_resp,
                btn_compartir_chat,
                btn_reset_prompt,
            ], 
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.update()

    respuesta_area = ensamblar_campo_respuesta()

    container_panel_respuesta = ft.Container(
        content=respuesta_area,
        padding=20,
        expand=True,
    )

    # espacio alternativo para el Chat
    tab_chat = ft.Column(
        [
            container_panel_respuesta,
            fila_prompt,
            fila_prompt_botones,
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    container_panel_configuracion = ft.Container(
        content=ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Chat", content=tab_chat),
                ft.Tab(text="Interfáz", content=tab_interfaz),
                ft.Tab(text="Acceso API", content=tab_api),
                ft.Tab(text="Configuración Modelo", content=tab_config_modelo),
                ft.Tab(text="Acerca de", content=tab_acerca),
            ],
        ),
        expand=True,
    )

    # Agregamos componentes a la página
    page.add(
        ft.Column(
            controls=[
                container_panel_configuracion,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )
    )

# Ejecución del Programa
ft.app(target=main, assets_dir="assets")
