"""
Nombre de la aplicación: DEEPROOT
Versión: 0.0.1
Autor: Jonás Antonio Reyes Casanova (jonasroot)
Fecha de creación: 28-01-2025
Última actualización: 09-02-2025

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

import flet as ft
import openai
import asyncio
from openai import OpenAIError, APIConnectionError, APIError
import json
import os
import modules.themes as themes
import acerca

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
        "api_key": "",
        "url_base": "",
        "stream": True
    }

# Guardar configuración
def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Cargar configuración
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
CODE_THEME_CLARO = ft.MarkdownCodeTheme.GRUVBOX_LIGHT
CODE_THEME_OSCURO = ft.MarkdownCodeTheme.GRUVBOX_DARK

# Inicializando cliente OpenAI
async def enviar_consulta_a_deepseek(page, prompt, campo_respuesta, modelo, api_key, url_base):
    try:
        client = openai.OpenAI(api_key=api_key, base_url=url_base)

        campo_respuesta.value = "Procesando tu solicitud..."
        await campo_respuesta.update_async()

        respuesta = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Te llamas DeepSeek, y charlamos a través de DeepRoot un Cliente API para DeepSeek. Eres un asistente y experto programador promotor del software libre."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            stream=True
        )
        # colectores
        colectados_chunks = []
        colectados_mensajes = []

        # Procesar cada chunk de la respuesta
        campo_respuesta.value = ""  # Limpiamos el mensaje de "Procesando..."
        for chunk in respuesta:
            if chunk.choices[0].delta.content:
                chunk_texto = chunk.choices[0].delta.content
                campo_respuesta.value += chunk_texto
                print(f"Campo: {chunk_texto}")
                await campo_respuesta.update_async()  # Se actualiza la interfaz en tiempo real
                await asyncio.sleep(0)

    except asyncio.TimeoutError:
        # En caso de que el servidor no responda en el tiempo especificado
        campo_respuesta.value = "Error: El servidor no respondió a tiempo. Intenta de nuevo."
        await campo_respuesta.update_async()
    except (APIError, APIConnectionError, OpenAIError) as e:
        # Manejo de errores con la API
        campo_respuesta.value = f"Error de conexión con la IA: {str(e)}"
        await campo_respuesta.update_async()
    except Exception as e:
        # Manejo de cualquier otro error no esperado
        campo_respuesta.value = f"Error inesperado: {str(e)}"
        await campo_respuesta.update_async()

async def main(page: ft.Page):
    # Configuración del theme inicial
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    page.title = f"{APP_NAME} {APP_LEMA}"
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
    )

    # Componentes de la interfáz
    barra_app = ft.AppBar(
        title=ft.Text(APP_NAME, size=22, color="#1440AD", weight=ft.FontWeight.W_900),
        bgcolor=ft.Colors.BLUE,
        actions=[
            ft.IconButton(ft.Icons.SUNNY if not page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE,
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

    input_prompt = ft.TextField(
        label="Escribe tu consulta",
        autofocus=True,
        expand=True,
        min_lines=2,
        max_lines=4,
        #bgcolor=ft.colors.BLUE_400,
        on_submit=lambda e: on_submit(e) if config["usar_enter"] else False
    )

    # switch para enviar con enter
    switch_enter = ft.Switch(
        value=config["usar_enter"],
        on_change=lambda e: actualizar_configuracion("usar_enter", e.control.value),
        disabled=True
    )

    # Lista desplegable para seleccionar el modelo
    lista_modelos = ft.Dropdown(
        value=config["modelo"],
        options=[
            ft.dropdown.Option("deepseek-chat"),
            ft.dropdown.Option("deepseek-reasoner"),
        ],
        on_change=lambda e: actualizar_configuracion("modelo", e.control.value)
    )

    # Campos de configuración
    campo_api_key = ft.TextField(label="API Key",
                                 value=config["api_key"],
                                 password=True,
                                 can_reveal_password=True)
    campo_url_base = ft.TextField(label="URL Base", value=config["url_base"])

    # Función Guardar Configuración Avanzada
    def guardar_configuracion_avanzada(e):
        config["api_key"] = campo_api_key.value
        config["url_base"] = campo_url_base.value
        guardar_configuracion(config)
        page.snack_bar = ft.SnackBar(ft.Text("¡Configuración Guardada!"))  # Crea el SnackBar
        page.snack_bar.bgcolor = ft.colors.GREEN
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()

    # Boton Guardar la Configuración Avanzada!
    btn_guardar_conf = ft.ElevatedButton("Guardar", on_click=guardar_configuracion_avanzada)

    # espacio de configuración del Campo de consulta o Prompt
    tab_prompt = ft.Column(
        [
            ft.Text("Enviar Prompt con tecla Enter", size=16, weight=ft.FontWeight.BOLD),
            switch_enter
        ],
        spacing=10
    )

    # espacio configuración API
    tab_api = ft.Column(
        [
            ft.Text("Token de Acceso al Servicio API", size=16, weight=ft.FontWeight.BOLD),
            campo_api_key,
            btn_guardar_conf
        ],
        spacing=10
    )

    tab_url = ft.Column(
        [
            ft.Text("Dirección del Servicio API", size=16, weight=ft.FontWeight.BOLD),
            campo_url_base,
            btn_guardar_conf
        ],
        spacing=10
    )

    # panel configuración modelos
    tab_modelo = ft.Column(
        [
            ft.Text("Seleccione un Modelo:", size=16, weight=ft.FontWeight.BOLD),
            lista_modelos,
            btn_guardar_conf
        ],
        spacing=10
    )

    # panel configuración modelos
    tab_acerca = ft.Column(
        [
            ft.Markdown(
                acerca.de,
                selectable=False,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                auto_follow_links=True,

            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    # Función para actualizar configuraciones
    def actualizar_configuracion(clave, valor):
        config[clave] = valor
        guardar_configuracion(config)
        if clave == "usar_enter":
            input_prompt.multiline = not valor
            btn_enviar.visible = not valor
            page.update()
        else:
            input_prompt.multiline = True
            btn_enviar.visible = True
            page.update()

    # Función de aplicación del theme
    def aplicar_theme(theme):
        page.bgcolor = theme["background_color"]
        page.update()

    def cambiar_theme():
        if config["theme_mode"] == "theme_oscuro":
            page.theme_mode = ft.ThemeMode.LIGHT
            config["theme_mode"] = "theme_claro"
        else:
            page.theme_mode = ft.ThemeMode.DARK
            config["theme_mode"] = "theme_oscuro"

        guardar_configuracion(config)
        page.update()

    campo_respuesta = ft.Markdown("", selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, code_theme=ft.MarkdownCodeTheme.GITHUB)

    # Construyendo componentes de la interfáz
    async def on_submit(e):
        prompt = input_prompt.value
        if prompt.strip():
            if not config["api_key"]:
                campo_respuesta.value = "Error: API Key no configurada."
                await campo_respuesta.update_async()
                return

            try:
                await asyncio.wait_for(
                    enviar_consulta_a_deepseek(page, prompt, campo_respuesta, lista_modelos.value, config["api_key"], config["url_base"]),
                    timeout=1000
                )
            except asyncio.TimeoutError:
                campo_respuesta.value = "Error: El servidor no respondió a tiempo. Intenta de nuevo."
                await campo_respuesta.update_async()

            input_prompt.value = ""  # Recibida la respuesta limpiamos el campo de consulta
            input_prompt.focus()  # Limpiado el campo de consulta, procedemos a enfocar el campo (usabilidad)
            await input_prompt.update_async()
        else:
            campo_respuesta.value = "Por favor, escribe una consulta."
            await campo_respuesta.update_async()

    # Función cerrar la app
    def cerrar_click(e):
        page.window.close()

    # Resetear prompt
    def reset_prompt(e):
        input_prompt.value = ""
        input_prompt.focus()
        page.snack_bar = ft.SnackBar(ft.Text("Prompt borrado!"))  # Crea el SnackBar
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()

    # Resetear todos los campos
    def resetear_campos(e):
        campo_respuesta.value = ""
        input_prompt.value = ""
        input_prompt.focus()
        page.snack_bar = ft.SnackBar(ft.Text("Consultas reiniciadas"), bgcolor=ft.Colors.GREEN)  # Crea el SnackBar
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()

    # Función para copiar el prompt al portapapeles
    def copiar_prompt(e):
        page.set_clipboard(input_prompt.value)
        page.snack_bar = ft.SnackBar(ft.Text("Prompt copiado!"))  # Crea el SnackBar
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()  # Actualiza la página para mostrar el SnackBar

    # Copiar Respuesta al portapapeles
    def copiar_respuesta(e):
        page.set_clipboard(campo_respuesta.value)
        page.snack_bar = ft.SnackBar(ft.Text("¡Respuesta copiada y en formato Markdown!"))  # Crea el SnackBar
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()  # Actualiza la página para mostrar el SnackBar


    # Gestion de dialogos de confirmación
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

        page.dialog=dlg
        dlg.open = True
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

        page.dialog=dlg
        dlg.open = True
        page.update()


    # --------- Botones --------------------
    btn_enviar = ft.ElevatedButton("Enviar", icon=ft.icons.SEND, visible=not config["usar_enter"])
    btn_copiar_prompt = ft.ElevatedButton("Copiar Prompt", icon=ft.icons.FILE_COPY, on_click=copiar_prompt)
    btn_reset_prompt = ft.ElevatedButton("Borrar Prompt", icon=ft.icons.DELETE)
    btn_copiar_resp = ft.ElevatedButton("Copiar Respuesta", icon=ft.icons.OFFLINE_SHARE_ROUNDED, on_click=copiar_respuesta)
    btn_resetear_todo = ft.ElevatedButton("Nuevo Chat", icon=ft.icons.CHAT)
    btn_cerrar = ft.ElevatedButton("Salir", icon=ft.icons.EXIT_TO_APP)
    # ---------- Fin Botones ----------------

    # Asignación de Eventos a los botones
    btn_enviar.on_click = on_submit
    btn_reset_prompt.on_click = reset_prompt
    btn_resetear_todo.on_click = on_resetear_campos
    btn_cerrar.on_click = on_cerrar_click

    campos_prompt = ft.Row(
        controls=[
            input_prompt,
            btn_enviar
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True
    )

    fila_prompt = ft.Container(
        content=campos_prompt
    )

    fila_prompt_botones = ft.Row([btn_copiar_prompt,btn_reset_prompt,btn_copiar_resp,btn_resetear_todo,btn_cerrar], spacing=10, scroll=True)

    respuesta_area = ft.Column(
        controls=[
            campo_respuesta,
        ],
        scroll=ft.ScrollMode.AUTO,  # Habilita desplazamiento si es largo el contenido
        expand=True,  # Ocupa el espacio vertical disponible
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )

    container_panel_respuesta = ft.Container(
        content=respuesta_area,
        padding=20,
        border=ft.border.all(1, ft.colors.GREY_300),
        border_radius=10,
        expand=True,
    )

    # espacio alternativo para el Chat
    tab_chat = ft.Column(
        [
            container_panel_respuesta,
            #fila_panel_respuesta,
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )

    container_panel_configuracion = ft.Container(
        content=ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Chat", content=tab_chat),
                ft.Tab(text="Prompt", content=tab_prompt),
                ft.Tab(text="API Key", content=tab_api),
                ft.Tab(text="URL Base", content=tab_url),
                ft.Tab(text="Modelo", content=tab_modelo),
                ft.Tab(text="Acerca de", content=tab_acerca),
            ],
        ),
        expand=True,
    )

    panel_prompt = ft.Column(
        [
            ft.Container(),
            ft.Divider(),
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
                panel_prompt
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        ),
    )

# Ejecución del Programa
ft.app(target=main)
