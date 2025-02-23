"""
Nombre de la aplicación: DEEPROOT
Versión: 0.0.1
Autor: Jonás Antonio Reyes Casanova (jonasroot)
Fecha de creación: 28-01-2025
Última actualización: 17-02-2025

Descripción:
Esta aplicación es un cliente de escritorio y móvil para facilitar el acceso y disfrute del Servicio API de DeepSeek. Se requiere de un token de DeepSeek Platform para poder funcionar. Es un desarrollo independiente, inspirado en los valores del Software Libre en Venezuela. Es resultado de los incentivos éticos de la Universidad Bolivariana de Venezuela y la Comunidad de Canaima GNU/Linux.

Licencia:
Este software se distribuye bajo la licencia GNU GPL v3.0.
Puedes encontrar una copia de la licencia en https://www.gnu.org/licenses/gpl-3.0.html#license-text
Este código es libre y debe permanecer así. Si realizas modificaciones o derivados, debes mencionar al autor original (yo) y mantener esta misma licencia.

Contacto:
- Canal de Telegram: t.me/jonasroot (comenta una publicación)
- Repositorio: https://github.com/jonasreyes/deeproot.git

"La verdadera inteligencia no solo resuelve problemas, sino que cultiva la vida..."
#PatriaYSoftwareLibre
"""

import openai
from openai import OpenAIError, APIConnectionError, APIError
import flet as ft
import asyncio
import json
import os
import modules.themes as themes
import acerca
from modules.interfaz import *
import locale
from datetime import datetime

# contexto de tiempo
hoy = datetime.now()
fecha_formateada = hoy.strftime("(%d/%m/%Y - %H:%M:%S)")

# ARCHIVO DE CONFIGURACIÓN
CONFIG_FILE = "deeproot.json"

# Carga de configuración inicial desde archivo
def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "usar_enter": False,
        "modelo": "deepseek-chat",
        "theme_mode": "theme_claro",
        "code_theme": "claro",
        "code_theme_claro": "gruvbox-light",
        "code_theme_oscuro": "gruvbox-dark",
        "extension_set": "gitHubWeb",
        "api_key": "",
        "url_base": "",
        "stream": True,
        "max_tokens": 8192 # por defecto usa 4096, otros números: 2048, 1024, 512
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
VERDE_MINCYT = "#026E71"
TEAL_MINCYT = "#02A7AB"
AZUL_MINCYT = "#1D70B7"
GRIS_MINCYT = "#9C9B9B"
NARANJA_MINCYT = "#F08427"

async def main(page: ft.Page):

    # Configuración del theme inicial
    dr_platform = get_platform(page, APP_NAME, APP_LEMA)
    page.window.width = 400
    page.window.height = 800
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.auto_scroll = True

    # en futura actualización facilitaré la personalización completa del theme.
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density = ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary = AZUL_MINCYT,
            secondary = ft.Colors.ORANGE,
            background = ft.Colors.GREY_900,
            surface = ft.Colors.GREY_800
        )
    )

    # Componentes de la interfáz
    barra_app = ft.AppBar(
        title=ft.Text(APP_NAME, size=22, color="#FFFFFF", weight=ft.FontWeight.W_900),
        bgcolor="#1D70B7", # Azul Mincyt
        actions=[
            ft.IconButton(ft.Icons.SUNNY if not page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE,
                          on_click=lambda e: cambiar_theme(),
                          tooltip="Cambiar Tema"
                          ),
        ]
    )
    page.appbar = barra_app

    barra_pie = ft.BottomAppBar(
        bgcolor=ft.Colors.BLUE,
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

    # Respuestas - EXPERIMENTAL
    # Respuesta que devuelve la IA
    respuesta_prompt_md = ft.Text(
        "Bienvenido a DeepRoot Cliente API de DeepSeek AI", 
        weight=ft.FontWeight.W_800, 
        size=16, 
        text_align=ft.TextAlign.CENTER, 
        selectable=True
    )

    contenedor_respuesta_prompt_md = ft.Container(
        content=respuesta_prompt_md,
        bgcolor=AZUL_MINCYT,
        border_radius=10,
        padding=10,
        expand=True,
    )
    
    # Prompt del usuario que será devuelto a la interfáz
    respuesta_ia_text = ft.Markdown(
        f"\n\n",
        extension_set=EXTENSION_SET,
        code_theme=CODE_THEME
    )

    # referencia para scroll de respuesta
    respuesta_area_ref = ft.Ref[ft.Column]()

    # str: Campo de salida de la respuesta de la IA, el estilo y formato se dará desde la fución ectualizar_markdown()
    campo_respuesta = ft.ListView(
        controls=[
            contenedor_respuesta_prompt_md,
            respuesta_ia_text
        ],
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    # Función Actualizar Markdown
    def actualizar_markdown(campo, code_theme="gruvbox-light", extension_set="gitHubWeb", selectable=True, auto_follow_links=True):
        campo.extension_set = extension_set
        campo.code_theme = code_theme
        campo.selectable = selectable
        campo.auto_follow_links = auto_follow_links
        campo.update()

    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # Función de construcción de la burbuja Chat
    def burbuja_mensaje(mensaje, es_usuario):
        msj = ft.Row(
            alignment = ft.MainAxisAlignment.START if es_usuario else ft.MainAxisAlignment.SPACE_BETWEEN,
            wrap = True,
            controls = [
                ft.Container(
                    content = ft.Markdown(
                        value = mensaje, 
                        extension_set=EXTENSION_SET, 
                        code_theme=CODE_THEME,
                        selectable = True,
                        auto_follow_links = True,

                    ),
                    padding = 10 if es_usuario else 5,
                    bgcolor = NARANJA_MINCYT if es_usuario else None,
                    border_radius = 10,
                )
            ]
        )
        return msj


    # enviar_prompt :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # enviar_prompt :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # enviar_prompt :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # enviar_prompt :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Enviando consulta de usuarios a la API IA
    async def enviar_prompt(e):
        # Verificamos que la app está configurada con un token de la API
        if not config["api_key"]:
            # campo_respuesta es un ListView
            campo_respuesta.controls.append(ft.Text("Error: API Key no configurada."))
            await campo_respuesta.update_async()
            return

        prompt = input_prompt.value.strip()
        if not prompt:
            campo_respuesta.controls.append(ft.Text("Por favor, escribe una consulta."))
            await campo_respuesta.update_async()
            return

        # Agregamos en msj del usuario al Chat.
        input_prompt.value = ""
        await input_prompt.focus_async()

        campo_respuesta.controls.append(burbuja_mensaje(prompt, True))
        await campo_respuesta.update_async()

        # conectamos 
        await get_respuesta_ia(page, prompt, campo_respuesta)



    # get_respuesta_ia ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # get_respuesta_ia ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # get_respuesta_ia ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # get_respuesta_ia ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # get_respuesta_ia ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Inicializando cliente OpenAI
    async def get_respuesta_ia(page, prompt, campo_respuesta):
        try:
            client = openai.OpenAI(api_key=config["api_key"], base_url=config["url_base"])

            # Decorando el Prompt
            respuesta_ia_burbuja = burbuja_mensaje("", False)
            campo_respuesta.controls.append(respuesta_ia_burbuja)
            await campo_respuesta.update_async()

            # Obtenemos la respuesta de la IA en streaming
            respuesta = client.chat.completions.create(
                model=config["modelo"],
                messages=[
                    {"role": "system", "content": "Te llamas DeepSeek, y charlamos a través de DeepRoot un Cliente API para DeepSeek. Eres un asistente y experto programador promotor del software libre."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                stream=True,
                max_tokens=config["max_tokens"]
            )

            # Procesar cada chunk de la respuesta
            for chunk in respuesta:
                if chunk.choices[0].delta.content:
                    chunk_texto = chunk.choices[0].delta.content
                    respuesta_ia_burbuja.controls[0].content.value += chunk_texto
                    await campo_respuesta.update_async()
                    await asyncio.sleep(0)
                    print(f"Campo: {chunk_texto}")

            input_prompt.focus
            await campo_respuesta.scroll_to_async(offset=-1, duration=1000)

        except asyncio.TimeoutError:
            # En caso de que el servidor no responda en el tiempo especificado
            campo_respuesta.controls.append(ft.Text("Error: El servidor no respondió a tiempo. Intenta de nuevo."))
        except (APIError, APIConnectionError, OpenAIError) as e:
            # Manejo de errores con la API
            campo_respuesta.controls.append(ft.Text(f"Error de conexión con la IA: {str(e)}"))
        except Exception as e:
            # Manejo de cualquier otro error no esperado
            campo_respuesta.controls.append(ft.Text(f"Error inesperado: {str(e)}"))
        await campo_respuesta.update_async()


    # Alternativa para usar enter
    def on_usar_enter(e):
        config["usar_enter"]=switch_enter.value
        guardar_configuracion(config)
        input_prompt.multiline = not config["usar_enter"]
        #btn_enviar.visible = not config["usar_enter"]
        btn_enviar.visible = input_prompt.multiline
        input_prompt.on_submit = enviar_prompt if config["usar_enter"] else None
        page.update()

    #: str: Campo de ingreso de consulta o prompt
    input_prompt = ft.TextField(
        label="Escribe tu consulta",
        autofocus=True,
        expand=True,
        min_lines=2,
        max_lines=4,
        border_radius=10,
        multiline=False
    )
    # definición inicial del modo multiline del campo prompt
    input_prompt.multiline = config["usar_enter"]

    # switch para enviar con enter
    switch_enter = ft.Switch(
        value=False,
        on_change=lambda e: on_usar_enter(e)
    )
    # definición inicial del swicth, garantiza que al iniciar la app esté en el estado 
    # de la configuación especificada en el archivo deeproot.json
    switch_enter.value=config["usar_enter"]

    # Lista desplegable para seleccionar el modelo
    lista_modelos = ft.Dropdown(
        value=config["modelo"],
        options=[
            ft.dropdown.Option("deepseek-chat"),
            ft.dropdown.Option("deepseek-coder"),
            ft.dropdown.Option("deepseek-reasoner"),
        ],
        on_change=lambda e: actualizar_configuracion("modelo", e.control.value)
    )

    # Campos de configuración
    # str: Campo para depositar el string o token api key de deepseek
    campo_api_key = ft.TextField(label="API Key",
                                 value=config["api_key"],
                                 password=True,
                                 can_reveal_password=True)
    # str: Campo en el que debe colocarse la dirección del servidor con el model IA a acceder por API
    campo_url_base = ft.TextField(label="URL Base", value=config["url_base"])

    # Función Guardar Configuración Avanzada
    def guardar_configuracion_avanzada(e):
        config["api_key"] = campo_api_key.value
        config["url_base"] = campo_url_base.value
        guardar_configuracion(config)
        page.open(ft.SnackBar(ft.Text("¡Configuración Guardada!"), bgcolor=TEAL_MINCYT))
        page.update()

    # Boton Guardar la Configuración Avanzada!
    btn_guardar_conf = ft.ElevatedButton("Guardar", on_click=guardar_configuracion_avanzada)

    # espacio de configuración del Campo de consulta o Prompt
    tab_interfaz = ft.Column(
        [
            ft.Text("Enviar Prompt con tecla Enter", size=16, weight=ft.FontWeight.BOLD),
            switch_enter,
            btn_guardar_conf,
            ft.Text("Theme - Próxima Versión", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Code Theme - Próxima Versión", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Extensiones Theme - Próxima Versión", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Selector nro. Tokens - Próxima Versión", size=16, weight=ft.FontWeight.BOLD),



        ],
        spacing=10
    )

    # espacio configuración API
    tab_api = ft.Column(
        [
            ft.Text("Token de Acceso al Servicio API", size=16, weight=ft.FontWeight.BOLD),
            campo_api_key,
            campo_url_base,
            ft.Text("Seleccione un Modelo:", size=16, weight=ft.FontWeight.BOLD),
            lista_modelos,
            btn_guardar_conf
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,  # Habilita desplazamiento si es largo el contenido
    )


    acercade = ft.Markdown(
        acerca.de,
        extension_set=EXTENSION_SET,
        code_theme=CODE_THEME
    )
    # panel configuración modelos
    tab_acerca = ft.Column(
        [
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
        global CODE_THEME, CODE_THEME_CLARO, CODE_THEME_OSCURO
        global EXTENSION_SET
        if config["theme_mode"] == "theme_oscuro":
            page.theme_mode = ft.ThemeMode.LIGHT
            config["theme_mode"] = "theme_claro"
            CODE_THEME = CODE_THEME_CLARO
        else:
            page.theme_mode = ft.ThemeMode.DARK
            config["theme_mode"] = "theme_oscuro"
            CODE_THEME = CODE_THEME_OSCURO

        actualizar_markdown(respuesta_ia_text,CODE_THEME)
        actualizar_markdown(acercade,CODE_THEME, selectable=True)
        guardar_configuracion(config)
        page.update()


    # Función cerrar la app
    def cerrar_click(e):
        page.window.close()

    # Resetear prompt
    def reset_prompt(e):
        input_prompt.value = ""
        input_prompt.focus()
        page.open(ft.SnackBar(ft.Text("¡Prompt borrado!"), bgcolor=TEAL_MINCYT))
        page.update()

    # Resetear todos los campos
    def resetear_campos(e):
        campo_respuesta.controls.clear()
        input_prompt.value = ""
        input_prompt.focus()
        page.open(ft.SnackBar(ft.Text("¡Ya puedes empezar una nueva conversación!"), bgcolor=TEAL_MINCYT))
        page.update()

    # Función para copiar el prompt al portapapeles
    def copiar_prompt(e):
        page.set_clipboard(input_prompt.value)
        page.open(ft.SnackBar(ft.Text("¡Prompt copiado al portapapeles!"), bgcolor=TEAL_MINCYT))
        page.update()  # Actualiza la página para mostrar el SnackBar

    # Copiar Respuesta al portapapeles
    def copiar_respuesta(e):
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

        page.set_clipboard(conversaciones_text)
        page.open(ft.SnackBar(ft.Text("¡Respuestas copiadas al portapepeles y en formato Markdown!"), bgcolor=TEAL_MINCYT))
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
    #btn_enviar = ft.ElevatedButton("Enviar", icon=ft.Icons.SEND)
    btn_enviar = ft.FloatingActionButton(icon=ft.Icons.SEND)

    btn_copiar_prompt = get_icon_boton_prompt(
            ft.Icons.FILE_COPY,
            AZUL_MINCYT,
            'Copiar Prompt',
            'Prompt',copiar_prompt
            )

    btn_copiar_resp = get_icon_boton_prompt(
            ft.Icons.OFFLINE_SHARE_ROUNDED,
            AZUL_MINCYT,
            'Copiar Respuesta IA',
            'Respuesta',copiar_respuesta
            )

    btn_reset_prompt = get_icon_boton_prompt(
            ft.Icons.DELETE_FOREVER_ROUNDED,
            NARANJA_MINCYT,
            'Copiar Prompt',
            'Borrar',reset_prompt
            )

    btn_nuevo_chat = get_icon_boton_prompt(
            ft.Icons.CHAT,
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

    # Asignación de Eventos a los botones
    btn_enviar.on_click = enviar_prompt

    campos_prompt = ft.Row(
        controls=[
            input_prompt,
            ft.Container(margin=ft.margin.only(left=10)),
            btn_enviar
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )

    fila_prompt = ft.Container(
        content=campos_prompt
    )

    fila_prompt_botones = ft.Row(
        [
            btn_reset_prompt,
            btn_copiar_prompt,
            btn_nuevo_chat,
            btn_copiar_resp,
            btn_cerrar
        ], 
        spacing=4,
        scroll=True,
        alignment=ft.MainAxisAlignment.CENTER,
        
    )

    respuesta_area = ft.Column(
        ref=respuesta_area_ref,
        controls=[
            campo_respuesta,
        ],
        scroll=ft.ScrollMode.AUTO,  # Habilita desplazamiento si es largo el contenido
        expand=True,  # Ocupa el espacio vertical disponible
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    container_panel_respuesta = ft.Container(
        content=respuesta_area,
        padding=20,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=10,
        expand=True,
    )

    # espacio alternativo para el Chat
    tab_chat = ft.Column(
        [
            container_panel_respuesta,
            fila_prompt,
            fila_prompt_botones
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
                ft.Tab(text="Configuración API", content=tab_api),
                ft.Tab(text="Acerca de", content=tab_acerca),
            ],
        ),
        expand=True,
    )

    panel_prompt = ft.Column(
        [
            fila_prompt,
            fila_prompt_botones
        ],
        alignment=ft.MainAxisAlignment.END
    )


    # Agregamos componentes a la página
    page.add(
        ft.Column(
            controls=[
                container_panel_configuracion,
                #panel_prompt
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        )
    )
    page.update()

# Ejecución del Programa
ft.app(target=main)
