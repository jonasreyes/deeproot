import flet as ft
from flet import Ref, Container,Markdown, Row, CircleAvatar, Icon, Icons, MainAxisAlignment
from modules.themes import Color, ThemeLight, ThemeDark

def get_icon_boton_prompt(icon,icon_color,tooltip,text,funcion):
    boton=ft.Column(
            [
            ft.IconButton(
                icon=icon,
                icon_color=icon_color,
                icon_size=32,
                tooltip=tooltip,
                on_click=funcion
            ),
            ft.Text(text, size=12)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
            )
    return boton

# función para identificar la plataforma huesped de DeepRoot
def get_platform(e, APP_NAME, APP_LEMA):
    plataforma = e.platform.value
    platform_ui = ""

    # bases para modificar interfáz según la plataforma
    if plataforma in ["linux","macos","windows"]:
        e.title=f"{APP_NAME} Escritorio - {APP_LEMA}"
        platform_ui = "escritorio"
    elif plataforma in ["android", "ios"]:
        e.title=f"{APP_NAME} Móvil - {APP_LEMA}"
        platform_ui = "movil"
    else:
        e.title=APP_NAME
        platform_ui = "escritorio"
    e.update()

    return e.platform.value

# Función de Diágolos Alerta
# def dialogo_alert(titulo,mensaje, funcion_si,funcion_no=cerrar_dialogo, modal=True):
#     dlg = ft.AlertDialog(
#         modal=modal,
#         title=titulo,
#         content=ft.Text(mensaje),
#         actions=[
#             ft.TextButton("Sí", on_click=funcion_si),
#             ft.TextButton("No", on_click=funcion_no),
#         ],
#         actions_alignment=ft.MainAxisAlignment.END,
#     )
#     return dlg

class GestorConversacion:
    def __init__(self):
        # Referencias para los contenedores de burbujas
        self.ref_burbuja_usuario_claro = Ref[Container]() 
        self.ref_burbuja_ia_claro = Ref[Container]() 
        self.ref_burbuja_usuario_oscuro = Ref[Container]() 
        self.ref_burbuja_ia_oscuro = Ref[Container]() 
        self.key_burbuja = 0 # para facilitar la navegación por scroll y poder editar o eliminar las burbujas que se requieran.

    def obtener_color_burbuja(self, es_usuario, theme_mode):
        """Devuelve el color de fondo de la burbuja según el tema y el tipo de usuario."""
        if es_usuario:
            return ThemeLight.GloboUsuarioFondo if theme_mode == "light" else ThemeDark.GloboUsuarioFondo
        else:
            return ThemeLight.GloboIAFondo if theme_mode == "light" else ThemeDark.GloboIAFondo

    def crear_burbuja(self, mensaje, es_usuario, theme_mode, referencia):
        """Crea una burbuja de chat con la referencia adecuada."""


        bgcolor = self.obtener_color_burbuja(es_usuario, theme_mode)
        ref = (
            self.ref_burbuja_usuario_claro if es_usuario and theme_mode == "light" else
            self.ref_burbuja_ia_claro if not es_usuario and theme_mode == "light" else
            self.ref_burbuja_usuario_oscuro if es_usuario and theme_mode == "dark" else
            self.ref_burbuja_ia_oscuro
        )

        # identificador de la burbuja, multiples propósitos
        key_burbuja = self.key_burbuja+1 # lo mantendremos en dígito (Será 1 más que el número de indice, con lo que podemos saber como manipularlo con el número de indice.)

        # Funciones de edición de burbujas

        def copiar_burbuja():
            pass

        def modificar_burbuja():
            pass

        def eliminar_burbuja():
            pass

        # botones de edición, eliminación y navegación
        btn_copiar_burbuja =  ft.OutlinedButton(
            "Copiar", 
            data=key_burbuja, 
            on_click=copiar_burbuja,
            icon="park_rounded"
        )

        btn_modificar_burbuja =  ft.OutlinedButton(
            "Modificar", 
            data=key_burbuja, 
            on_click=modificar_burbuja,
            icon="park_rounded"
        )

        btn_eliminar_burbuja =  ft.OutlinedButton(
            "Eliminar", 
            data=key_burbuja, 
            on_click=eliminar_burbuja,
            icon="park_rounded"
        )

        # Fila edición de burbuja
        columna_edicion_burbuja = ft.Column(
            controls=[btn_copiar_burbuja,btn_modificar_burbuja, btn_eliminar_burbuja], # Atención con esta solución, puede ser problemática, pero insistiré a ver si granulada la composición funciona.
            alignment=MainAxisAlignment.SPACE_EVENLY
        )


        # Creación del Avatar
        avatar = CircleAvatar(
            content=Icon(Icons.PERSON if es_usuario else Icons.MEMORY),
            bgcolor=Color.AzulMincyt if es_usuario else Color.GrisMincyt
        )

        # Creamos el contenedor de la burbuja
        contenedor_burbuja = Container(
            content=Markdown(
                value=mensaje,
                extension_set="gitHubWeb", # En próxima versión lo haré configurable
                code_theme="gruvbox-light" if theme_mode == "light" else "gruvbox-dark",
                selectable=True,
                auto_follow_links=True,
                ref=referencia # Indispensable para poder actualizar en caliente el code_theme
            ),
            padding = 10,
            bgcolor = bgcolor,
            border_radius = 10,
            ref=ref
        )

        # Devolvemos una fila con el avatar y la burbuja
        return Row(
            controls=[avatar, contenedor_burbuja], # Atención con esta solución, puede ser problemática, pero insistiré a ver si granulada la composición funciona.
            alignment=MainAxisAlignment.END if es_usuario else MainAxisAlignment.START,
            wrap=True,
            key = key_burbuja,
        )

    def actualizar_colores_burbujas(self, theme_mode):
        """Actualiza los colores de las burbujas y el code_theme según el tema actual."""
        for ref in [
            self.ref_burbuja_usuario_claro,
            self.ref_burbuja_ia_claro,
            self.ref_burbuja_usuario_oscuro,
            self.ref_burbuja_ia_oscuro
        ]:
            if ref.current:
                es_usuario = ref.current.bgcolor in [ThemeLight.GloboUsuarioFondo, ThemeDark.GloboUsuarioFondo]
                ref.current.bgcolor = self.obtener_color_burbuja(es_usuario,theme_mode)
                if hasattr(ref.current.content, "code_theme"):
                    ref.current.content.code_theme = "gruvbox-light" if theme_mode == "light" else "gruvbox-dark" # Revisar la eficiencia, puede ser quizas mejor asignación directa, tenemos la rerefencia.
                ref.current.update()
