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
        "usar_enter": True,
        "modelo": "deepseek-chat",
        "modo_oscuro": False,
        "api_key": "",
        "url_base": "https://api.deepseek.com"
    }

# Guardar configuración
def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

#Configuración de la API de DeepSeek
APP_NAME = "DeepRoot"
APP_VERSION = "Alfa 0.0.1 - 2025"
APP_LEMA = "¡Un cliente API de DeepSeek!"
AUTOR_NAME = "Jonás A. Reyes C."
AUTOR_NICK = "@jonasroot"
AUTOR_CONTACT = "Telegram: @jonasreyes"
AUTOR_BLOG = "https://jonasroot.t.me"
LICENCIA = "GNU/GPL V3"

# Inicializando cliente OpenAI
def enviar_consulta_a_deepseek(prompt, modelo, api_key, url_base):
    try:
        client = OpenAI(api_key=api_key, base_url=url_base)
        response = client.chat.completions.create(
            model = modelo,
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}" 

# Interfáz gráfica con Flet
def main(page: ft.Page):

    # Cargar configuración
    config = cargar_configuracion()

    # Configuración del theme inicial
    page.adaptive = True
    page.padding = 20
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 800
    page.window_height = 500
    page.theme_mode = ft.ThemeMode.DARK if config["modo_oscuro"] else ft.ThemeMode.LIGHT
    if not config["modo_oscuro"]:
        page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.BLACK, background=ft.colors.BLACK))

    page.title = f"{APP_NAME} {APP_LEMA}"
    page.snack_bar = ft.SnackBar(
        content=ft.Text("Texto copiado al portapapeles."),
        action="Cerrar",
        behavior=ft.SnackBarBehavior.FLOATING,
        duration=2000,
        width=200
    )

    # Componentes de la interfáz
    input_prompt = ft.TextField(
        label="Escribe tu consulta",
        autofocus=True,
        multiline=True,
        min_lines=2,
        max_lines=5,
        on_submit=lambda e: on_submit(e) if config["usar_enter"] else False
    )
    output_response = ft.TextField(label="Respuesta:", multiline=True, min_lines=5, max_lines=10, read_only=True)

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
    campo_api_key = ft.TextField(label="API Key", value=config["api_key"], password=True, can_reveal_password=True)
    campo_url_base = ft.TextField(label="URL Base", value=config["url_base"])


    # --------- Botones --------------------
    btn_enviar = ft.ElevatedButton("Enviar", icon=ft.icons.SEND, visible=not config["usar_enter"])
    btn_copiar_prompt = ft.ElevatedButton("Copiar",icon=ft.icons.COPY)
    btn_reset_prompt = ft.ElevatedButton("Restablecer", icon=ft.icons.RESTORE,)
    btn_exportar_prompt = ft.ElevatedButton("Exportar", icon=ft.icons.DOWNLOAD, disabled=True)
    btn_copiar_resp = ft.ElevatedButton("Copiar",icon=ft.icons.COPY)
    btn_resetear_todo = ft.ElevatedButton("Limpiar", icon=ft.icons.RESTORE)
    btn_cerrar = ft.ElevatedButton("Salir", icon=ft.icons.CLOSE)
    # ---------- Fin Botones ----------------

    # Función Guardar Configuración Avanzada
    def guardar_configuracion_avanzada(e):
        config["api_key"] = campo_api_key.value
        config["url_base"] = campo_url_base.value
        guardar_configuracion(config)
        page.snack_bar.content = ft.Text("Configuración Guardada")
        page.snack_bar.open = True
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
            ft.Row(
                [
                    ft.Text("Modo oscuro:", size=16),
                    switch_modo_oscuro,
                    ft.Text("Enviar con Enter:", size=16),
                    switch_enter,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
        ],
        spacing=10
    )


    # Función para actualizar configuraciones
    def actualizar_configuracion(clave, valor):
        config[clave] = valor
        guardar_configuracion(config)
        if clave == "usar_enter":
            btn_enviar.visible = not valor
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

            response = enviar_consulta_a_deepseek(prompt, lista_modelos.value, config["api_key"], config["url_base"])
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
        page.snack_bar.open = True
        page.update()

    def exportar_prompt(e):
        pass


    # Copiar Respuesta al portapapeles
    def copiar_respuesta(e):
        #if output_response.value:
        page.set_clipboard(output_response.value) # Copiamos al portapapeles
        page.snack_bar.open = True
        page.update()

    # Asignación de Eventos a los botones
    btn_enviar.on_click = on_submit
    btn_reset_prompt.on_click = reset_prompt
    btn_copiar_prompt.on_click = copiar_prompt
    btn_exportar_prompt.on_click = exportar_prompt
    btn_copiar_resp.on_click = copiar_respuesta
    btn_resetear_todo.on_click = resetear_campos
    btn_cerrar.on_click = cerrar_click



    # Agregamos componentes a la página
    page.add(
        ft.Column(
            [
                ft.Text(f"{APP_NAME}", size=48, weight=ft.FontWeight.BOLD),
                ft.Text(f"{APP_LEMA}", size=24),
                output_response,
                ft.Row([btn_copiar_resp,btn_resetear_todo]),
                ft.Divider(),
                ft.Column(
                    [input_prompt],
                    spacing=10
                ),
                ft.Row(
                    [btn_enviar, btn_copiar_prompt, btn_reset_prompt,btn_exportar_prompt],
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
                )
            ],
            spacing = 20,
            scroll = True,
            expand = True

        )
    )
# Ejecución del Programa
ft.app(target=main)