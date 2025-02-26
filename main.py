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
import urllib.parse
from flet import FilePicker, FilePickerResultEvent
import markdown

# contexto de tiempo
hoy = datetime.now()
fecha_formateada = hoy.strftime("(%d/%m/%Y - %H:%M:%S)")

# hora para la IA
def get_hoy():
    hoy = datetime.now()
    fecha_de_hoy = hoy.strftime("(Hoy es %A %d de %B del año %Y y son las %H:%M:%S hora de Caracas Venezuela.)")
    return fecha_de_hoy

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
        "theme_mode": "ft.ThemeMode.LIGHT",
        "code_theme": "gruvbox-light",
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
locale.setlocale(locale.LC_TIME, 'es_VE.UTF-8')
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

# Colores personalizados
VERDE_MINCYT = "#026E71"
TEAL_MINCYT = "#02A7AB"
AZUL_MINCYT = "#1D70B7"
GRIS_MINCYT = "#9C9B9B"
NARANJA_MINCYT = "#F08427"
ROJO_FUTURO = "#E63022"
NARANJA_FUTURO = "#EC6C3A"
BEIGE_FUTURO = "#F8EFDC"
AZUL_FUTURO = "#1440AD"
AZUL_CIELO_FUTURO = "#A6D8E2"
DORADO_FUTURO = "#EFC318"
NEGRO_FUTURO = "#1F1E1E"


async def main(page: ft.Page):

    # Configuración del theme inicial
    dr_platform = get_platform(page, APP_NAME, APP_LEMA)
    page.window.width = 512
    page.window.height = 768
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.auto_scroll = True

    # creamos una referencia a todos los elementos markdown
    respuesta_ia_md_ref = ft.Ref[ft.Markdown]()

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
        bgcolor=AZUL_MINCYT, # Azul Mincyt
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
    

    # referencia para scroll de respuesta
    # refactorizar próximamente
    respuesta_area_ref = ft.Ref[ft.Column]()

    # str: Campo de salida de la respuesta de la IA, el estilo y formato se dará desde la fución ectualizar_markdown()
    campo_respuesta = ft.ListView(
        ref=respuesta_area_ref,
        controls=[
            contenedor_respuesta_prompt_md, # próximamente incluir Imágen Logotipo de DeepRoot
        ],
        expand=True,
        spacing=10,
        auto_scroll=True
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
        ref.current.code_theme = code_theme
        ref.current.update()

    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::: burbuja_mensaje ::::::::::::::::::::::::::::::::::::
    # Función de construcción de la burbuja Chat
    def burbuja_mensaje(mensaje, es_usuario, referencia=respuesta_ia_md_ref):
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
                        ref=respuesta_ia_md_ref, #importante para actualizar el code_theme
                    ),
                    padding = 10 if es_usuario else 5,
                    bgcolor = NARANJA_MINCYT if es_usuario else False,
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
    #async def enviar_prompt(e):
    async def enviar_prompt(e):
        # Verificamos que la app está configurada con un token de la API
        if not config["api_key"]:
            page.open(ft.SnackBar(ft.Text("Error: API Key no configurada."), bgcolor=ROJO_FUTURO))
            input_prompt.focus()
            campo_respuesta.update()
            return

        prompt = input_prompt.value.strip()
        if not prompt:
            page.open(ft.SnackBar(ft.Text("Por favor, escribe una consulta."), bgcolor=ROJO_FUTURO))
            input_prompt.focus()
            campo_respuesta.update()
            return

        # Agregamos en msj del usuario al Chat.
        # campo_respuesta.controls.clear() # Se comenta este llamado debido a que es importante tener 
        # |-> el historial al menos en pantalla. Puede pensarse en otra estratégia para mantener limpia la interfáz
        # |-> sin tener que desacer el historial.
        input_prompt.value = ""
        input_prompt.focus()

        campo_respuesta.controls.append(burbuja_mensaje(prompt, True))
        campo_respuesta.update()
        #await campo_respuesta.update_async() # se deshabilita el uso del await hasta que pueda comprobar que es beneficioso su uso para este contexto.

        # conectamos 
        await get_respuesta_ia(page, prompt, campo_respuesta)
        page.update()



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

            fecha_de_hoy = get_hoy()
            # Obtenemos la respuesta de la IA en streaming
            respuesta = client.chat.completions.create(
                model=config["modelo"],
                messages=[
                        {"role": "system", "content": "Te llamas DeepSeek y charlamos a través de DeepRoot, un cliente API para los modelos IA de DeepSeek, con posible compatibilidad futura con otros modelos. Eres un asistente experto en programación y promotor del software libre."},
                        {"role": "system", "content": f"{fecha_de_hoy}, responde con la fecha u hora en formato de 12 horas (con opción de 24 horas) basado en Caracas, Venezuela. Si te preguntan por otra ciudad o país, realiza la conversión sin explicaciones adicionales."},
                        {"role": "system", "content": "Si el usuario muestra interés en DeepRoot, puedes mencionar que es una aplicación desarrollada en Python por Jonás Reyes (jonasroot), un programador venezolano y promotor del software libre. Puedes compartir su canal de Telegram: https://t.me/jonasroot y el canal oficial de DeepRoot: https://t.me/deeproot_app. El repositorio oficial de DeepRoot: https://github.com/jonasreyes/deeproot.git"},
                        {"role": "system", "content": "DeepRoot facilita el acceso a IA avanzada y sin censura, siendo útil para científicos, investigadores, estudiantes y el público en general. Permite descargar respuestas en formato markdown y compartir historiales de chat por correo electrónico en HTML (se recomienda tener configurado un cliente de correo)."},
                        {"role": "system", "content": "Presenta la información de manera clara y bien formateada, usando elementos visuales e íconos de manera moderada para mejorar la comprensión sin saturar."},
                        {"role": "system", "content": "DeepRoot está en constante desarrollo. Aquellos interesados en colaborar pueden contactar al desarrollador a través de los medios mencionados."},
                        {"role": "system", "content": "Si el usuario solo te saluda, responde con tu nombre y pregunta cómo puedes ayudarle. Evita presentar información detallada sobre DeepRoot a menos que el usuario lo solicite."},
                        {"role": "system", "content": "En la versión actual (DeepRoot V 0.1.0), no estás habilitada para memorizar conversaciones previas. Si el usuario hace referencia a preguntas anteriores, responde de manera inteligente y coherente."},
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

            input_prompt.focus()
            campo_respuesta.scroll_to(offset=-1, duration=1000)
            await campo_respuesta.update_async()

        except asyncio.TimeoutError:
            # En caso de que el servidor no responda en el tiempo especificado
            page.open(ft.SnackBar(ft.Text("Error: El servidor no respondió a tiempo. Intenta de nuevo."), bgcolor=ROJO_FUTURO))
            page.update()
        except (APIError, APIConnectionError, OpenAIError) as e:
            # Manejo de errores con la API
            page.open(ft.SnackBar(ft.Text(f"Error de conexión con la IA: {str(e)}"), bgcolor=ROJO_FUTURO))
            page.update()
        except Exception as e:
            # Manejo de cualquier otro error no esperado
            page.open(ft.SnackBar(ft.Text(f"Error inesperado: {str(e)}"), bgcolor=ROJO_FUTURO))
            page.update()


    # Alternativa para usar enter
    def on_usar_enter(e):
        config["usar_enter"]=switch_enter.value
        guardar_configuracion(config)
        input_prompt.multiline = not config["usar_enter"]
        btn_enviar.visible = not config["usar_enter"]
        input_prompt.on_submit = enviar_prompt if config["usar_enter"] else False
        if config["usar_enter"]:
            page.open(ft.SnackBar(ft.Text("¡Puedes enviar tu consulta pulsando la Tecla Enter! Botón enviar ocultado."), bgcolor=TEAL_MINCYT))
        else:
            page.open(ft.SnackBar(ft.Text("Desactivada opción de envío de consulta pulsando la tecla 'Enter'. Restablecido el Botón de envío."), bgcolor=TEAL_MINCYT))
        page.update()

    #: str: Campo de ingreso de consulta o prompt
    input_prompt = ft.TextField(
        label="Escribe tu consulta",
        autofocus=True,
        expand=True,
        min_lines=2,
        max_lines=4,
        border_radius=10,
        multiline=not config["usar_enter"],
        on_submit=enviar_prompt
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
        code_theme=CODE_THEME,
        selectable = True,
        auto_follow_links = True,
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
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            config["theme_mode"] = "ft.ThemeMode.DARK"
            CODE_THEME = CODE_THEME_OSCURO
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            config["theme_mode"] = "ft.ThemeMode.LIGHT"
            CODE_THEME = CODE_THEME_CLARO

        actualizar_markdown_ref(respuesta_ia_md_ref,CODE_THEME)
        actualizar_markdown(acercade)
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

    # Descarga el chat 
    def descargar_chat(e:FilePickerResultEvent,path="almacenamiento/"):
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
                    page.open(ft.SnackBar(ft.Text(f"Historial de Chat con la IA {config['modelo']} se ha guardado exitosamente en '{archivo_historial_chat_md}'."), bgcolor=TEAL_MINCYT))
            except Exception as e:
                page.open(ft.SnackBar(ft.Text(f"Error guardando el archivo: ",e), bgcolor=ROJO_FUTURO))
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
        page.open(ft.SnackBar(ft.Text(f"Se comparte el Chat para la plataforma {dr_platform}"), bgcolor=TEAL_MINCYT))
        page.update()

    # Obtener el chat actual
    def get_chat():
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
    # Botón flotante de envío de consulta, se oculta cuando se decide usar la tecla enter para enviar.
    btn_enviar = ft.FloatingActionButton(icon=ft.Icons.SEND, visible=not config["usar_enter"])

    btn_descargar_chat = get_icon_boton_prompt(
            ft.Icons.DOWNLOAD,
            AZUL_MINCYT,
            'Descargar Chat',
        'Descargar Chat',lambda e:dialogo_guardar_chat.save_file()
            )

    btn_compartir_chat = get_icon_boton_prompt(
            ft.Icons.ALTERNATE_EMAIL,
            AZUL_MINCYT,
            'Compartir por Email',
            'Compartir',compartir_chat_por_email
            )

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
            ft.Container(margin=ft.margin.only(left=5)),
            btn_enviar
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )

    fila_prompt = ft.Container(
        content=campos_prompt
    )

    if dr_platform in ["windows","linux","macos"]:
        fila_prompt_botones = ft.Row(
            [
                btn_nuevo_chat,
                btn_copiar_prompt,
                btn_copiar_resp,
                btn_compartir_chat,
                btn_descargar_chat,
                btn_reset_prompt,
                btn_cerrar
            ], 
            spacing=4,
            scroll=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.update()
    else:
        fila_prompt_botones = ft.Row(
            [
                btn_nuevo_chat,
                btn_copiar_prompt,
                btn_copiar_resp,
                btn_reset_prompt,
                btn_cerrar
            ], 
            spacing=4,
            scroll=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.update()

    respuesta_area = ft.Column(
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

# Ejecución del Programa
ft.app(target=main)
