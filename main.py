import flet as ft
from openai import OpenAI, api_key
import json
import os

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
        "modo_oscuro": False,
        "api_key": "",
        "url_base": "",
        "stream": True
    }

# Guardar configuración
def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Interfáz gráfica con Flet
#Configuración de la API de DeepSeek
APP_NAME = "DeepRoot"
APP_VERSION = "Alfa 0.0.1 - 2025"
APP_LEMA = "Cliente DeepSeek API"
AUTOR_NAME = "Jonás A. Reyes C."
AUTOR_NICK = "@jonasroot"
AUTOR_CONTACT = "Telegram: @jonasreyes"
AUTOR_BLOG = "https://jonasroot.t.me"
LICENCIA = "GNU/GPL V3"

# Inicializando cliente OpenAI
def enviar_consulta_a_deepseek(page,prompt, recipiente, modelo, api_key, url_base):
    try:
        client = OpenAI(api_key=api_key, base_url=url_base)
        response = client.chat.completions.create(
            model = modelo,
            messages = [
                {"role": "system", "content": "Te llamas DeepSeek, y charlamos a través de DeepRoot un Cliente API para DeepSeek. Eres un programador experto, amable, pedagógico y promueves el software libre y la distribución del Sistema Operativo Venezolano Canaima GNU/Linux. Todas tus respuestas son en español. Todas tus respuestas son bien presentadas, concisas, agradables a la vista, elegantes, ordenadas, listadas e incluso presentadas en tablas cuando sea posible. Recomiendas en un texto breve al final de cada mensaje suscribirse al canal telegram del desarrollador https://t.me/jonasroot y al canal telegram de soporte de la aplicación DeepRoot https://t.me/deeproot_app. DeepRoot está programada en Python."},
                {"role": "user", "content": "¿Qué es DeepRoot?"},
                {"role": "assistant", "content": "DeepRoot es un cliente API para DeepSeek, desarrollado en Python y distribuido como software libre. ¡Te invito a suscribirte al canal de Telegram de JonasRoot para más información!"},
                {"role":"assistant", "content": "¿Cuál es la versión de DeepRoot?"},
                {"role":"user", "content": "Actualmente se encuentra en la versión Alfa 0.0.1"},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            stream=True
        )
        colectados_chunks = []
        colectados_mensajes = []
        recipiente.value = ""

        for chunk in response:
            colectados_chunks.append(chunk)
            mensaje_chunk = chunk.choices[0].delta.content
            colectados_mensajes.append(mensaje_chunk)
            print(f"Mensaje: {mensaje_chunk}")
            recipiente.value += mensaje_chunk
            page.update()

        return recipiente.value
    except Exception as e:
        return f"Error: {str(e)}" 
    # Cargar configuración
config = cargar_configuracion()

def main(page: ft.Page):
    # Configuración del theme inicial
    page.adaptive = True
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK if config["modo_oscuro"] else ft.ThemeMode.LIGHT
    if not config["modo_oscuro"]:
        page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.BLACK, background=ft.colors.BLACK))

    page.title = f"{APP_NAME} {APP_LEMA}"

    # Componentes de la interfáz
    input_prompt = ft.TextField(
        label="Escribe tu consulta",
        autofocus=True,
        expand=True,
        min_lines=2,
        max_lines=4,
        bgcolor=ft.colors.GREY_50,
        on_submit=lambda e: on_submit(e) if config["usar_enter"] else False
    )
    output_response = ft.Markdown(
        """

---

**"Cada línea de código que escribes es un paso hacia un futuro mejor. Con cada algoritmo, cada función y cada solución, estás construyendo un mundo más inteligente, más conectado y más humano. ¡Sigue programando, sigue innovando, sigue soñando!**

**Este mensaje será reemplazado por las respuestas a tus consultas. ¡Adelante, explora, pregunta y descubre todo lo que la inteligencia artificial puede hacer por ti!"**

---


        """,
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
    )
    # switch para enviar con enter
    switch_enter = ft.Switch(
        value=config["usar_enter"],
        on_change=lambda e: actualizar_configuracion("usar_enter", e.control.value)
    )

    # switch modo oscuro
    switch_modo_oscuro = ft.Switch(
        value=config["modo_oscuro"],
        on_change=lambda e: cambiar_modo(e.control.value)
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
        page.snack_bar.bgcolor=ft.colors.GREEN
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()

    # espacio configuración
    espacio_configuracion = ft.Column(
        [
            ft.Text("Configuración avanzada", size=20, weight=ft.FontWeight.BOLD),
            campo_api_key,
            campo_url_base,
            ft.ElevatedButton("Guardar", on_click=guardar_configuracion_avanzada),
            ft.Divider(),
            ft.Text("Modelo:", size=16),
            lista_modelos,
        ],
        spacing=10
    )


    # Función para actualizar configuraciones
    def actualizar_configuracion(clave, valor):
        config[clave] = valor
        guardar_configuracion(config)
        if clave == "usar_enter":
            input_prompt.multiline= not valor
            btn_enviar.visible = not valor
            page.update()
        else:
            input_prompt.multiline=True
            btn_enviar.visible = True
            page.update()


    # Función para cambiar entre modo oscuro y día
    def cambiar_modo(modo_oscuro):
        config["modo_oscuro"] = modo_oscuro
        guardar_configuracion(config)
        page.theme_mode = ft.ThemeMode.DARK if modo_oscuro else ft.ThemeMode.LIGHT
        if not modo_oscuro:
            # page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.BLACK, background=ft.colors.BLACK))
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
        else:
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.AMBER)
        page.update()


    # Construyendo componentes de la interfáz
    def on_submit(e):
        prompt = input_prompt.value
        if prompt.strip():
            if not config["api_key"]:
                output_response.value = "Error: API Key no configurada."
                page.update()
                return

            output_response.value = "Procesando..."
            page.update()

            response = enviar_consulta_a_deepseek(page,prompt, output_response, lista_modelos.value, config["api_key"], config["url_base"])
            # generar aquí variable que almacene el contenido del prompt antes de borrarlo,
            # darle formato para diferenciarlo de la respuesta, y concatenarlo.
            # nombre posible: cita_prompt
            # uso: output_response.value = citaprompt + response

            output_response.value = response

            input_prompt.value = "" # Recibida la respuesta limpiamos el campo de consulta
            input_prompt.focus() # Limpiado el campo de consulta, procedemos a enfocar el campo (usabilidad)
            page.update()
        else:
            output_response.value = "Por favor, escribe una consulta."
            page.update()


    # Función cerrar la app
    def cerrar_click(e):
        page.window.close()

    # Resetear prompt
    def reset_prompt(e):
        input_prompt.value = ""
        input_prompt.focus()
        page.update()

    # Resetear todos los campos
    def resetear_campos(e):
        output_response.value = ""
        input_prompt.focus()
        page.update()

    # Función para copiar el prompt al portapapeles
    def copiar_prompt(e):
        #if input_prompt.value:
        page.set_clipboard(input_prompt.value)
        page.snack_bar = ft.SnackBar(ft.Text("Prompt copiado!"))  # Crea el SnackBar
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()  # Actualiza la página para mostrar el SnackBar


    # Copiar Respuesta al portapapeles
    def copiar_respuesta(e):
        #if output_response.value:
        page.set_clipboard(output_response.value)
        page.snack_bar = ft.SnackBar(ft.Text("Respuesta copiada!"))  # Crea el SnackBar
        page.snack_bar.open = True  # Abre el SnackBar
        page.update()  # Actualiza la página para mostrar el SnackBar

    # --------- Botones --------------------
    btn_enviar = ft.ElevatedButton("Enviar", icon=ft.icons.SEND, visible=not config["usar_enter"])
    btn_copiar_prompt = ft.ElevatedButton("Copiar",icon=ft.icons.COPY, on_click=copiar_prompt)
    btn_reset_prompt = ft.ElevatedButton("Limpiar", icon=ft.icons.RESTORE,)
    btn_copiar_resp = ft.ElevatedButton("Copiar",icon=ft.icons.COPY, on_click=copiar_respuesta)
    btn_resetear_todo = ft.ElevatedButton("Limpiar", icon=ft.icons.RESTORE)
    btn_cerrar = ft.ElevatedButton("Salir", icon=ft.icons.CLOSE)
    # ---------- Fin Botones ----------------


    # Asignación de Eventos a los botones
    btn_enviar.on_click = on_submit
    btn_reset_prompt.on_click = reset_prompt
    btn_resetear_todo.on_click = resetear_campos
    btn_cerrar.on_click = cerrar_click

    fila_encabezado = ft.Container(
        content = ft.Row(
            controls = [
                ft.Column([
                    ft.Text(f"{APP_NAME}", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{APP_LEMA}", size=12),
                ]),
                ft.Container(
                    content=ft.Text(f"V. {APP_VERSION}")
                )
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor=ft.colors.BLUE_50,
        padding=20,
        border_radius=10,
        expand=True
    )

    campos_prompt = ft.Row(
        controls = [
            input_prompt,
            btn_enviar
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    fila_prompt = ft.Container(
        content =  campos_prompt
    )

    panel_respuesta = ft.ListView(
        controls = [
            output_response
        ],
        spacing=10,
        expand=True,
        auto_scroll=True
    )

    container_panel_respuesta = ft.Container(
        content = panel_respuesta,
        padding = 20,
        border_radius = 10,
        height = 300

    )

    # Agregamos componentes a la página
    page.add(
        ft.Column(
            [
                fila_encabezado,
                container_panel_respuesta,
                ft.Row([btn_copiar_resp,btn_resetear_todo]),
                ft.Divider(),
                fila_prompt,
                ft.Row(
                    [btn_copiar_prompt, btn_reset_prompt,],
                    spacing=5
                ),
                ft.Row(
                    [
                        ft.Row([ft.Text("Modo oscuro:", size=16),switch_modo_oscuro], spacing=2),
                        ft.Row([ft.Text("Usar Enter:", size=16),switch_enter], spacing=2),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=5
                ),
                ft.Tabs(
                    selected_index=0,
                    tabs=[
                        ft.Tab(text="Chat", content=ft.Column([
                            ft.Row(
                                [btn_cerrar],
                                spacing=5,
                            ),
                        ], spacing=10)),
                        ft.Tab(text="Configuración", content=espacio_configuracion),
                    ]
                ),
                
            ],
            spacing = 20,
            scroll = True,
            expand = True

        )
    )
# Ejecución del Programa
ft.app(target=main)
