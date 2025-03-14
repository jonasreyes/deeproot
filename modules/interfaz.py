import flet as ft
from flet import Ref, Container,Markdown, Row, CircleAvatar, Icon, Icons, MainAxisAlignment
from modules.themes import Color, ThemeLight, ThemeDark
from pathlib import Path

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


def get_aviso_acerca(referencia, resumen):

    ruta_actual = Path(__file__).parent 
    ruta_imagen_deeproot = ruta_actual / "assets" / "img" / "deeproot.png"
    ruta_imagen_deep = ruta_actual / "assets" / "img" / "deep.jpg"

    return ft.Row(
        ref=referencia,
        controls=[
            ft.Column(
                controls=[
                    # Containers anidados y con estilo
                    ft.Container(
                        ft.Container(
                            ft.Stack(
                                [
                                    #Imágen de Fondo
                                    ft.Image(
                                        src=str(ruta_imagen_deep),
                                        width=360,
                                        height=260,
                                        fit=ft.ImageFit.COVER,
                                        border_radius=11,
                                    ),
                                    ft.Container(
                                        ft.Container(
                                            ft.Column(
                                                [
                                                    ft.Container(
                                                        ft.Image(
                                                            src=str(ruta_imagen_deeproot),
                                                            width=50,
                                                        ), padding=ft.padding.only(160),
                                                    ),
                                                    ft.Text(
                                                        "Acerca de",
                                                        width=360,
                                                        text_align="center",
                                                        weight="w900",
                                                        size=20
                                                    ),
                                                    ft.Text(
                                                        # Resumen de DeepRoot
                                                        resumen,
                                                        width=360,
                                                        size=14,

                                                    ),

                                                ], expand=True, alignment = ft.MainAxisAlignment.CENTER,
                                            ),
                                        ),
                                        border_radius=11,
                                        width=360,
                                        height=260,
                                        bgcolor="#22ffffff",
                                        gradient = ft.LinearGradient([Color.AzulEgipcio,Color.AzulMincyt]),
                                    ),
                                ]
                            ),
                            padding=20,
                            width = 360,
                            height = 560,
                        ),
                        width=400,
                        height=360,
                        #gradient = ft.LinearGradient([Color.AzulEgipcio,Color.AzulMincyt]),
                        expand = True
                    )

                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            expand = True
                        )
                    ],
                    expand=True,
                    alignment = ft.MainAxisAlignment.CENTER,
                )


def get_aviso(referencia):
    
    ruta_actual = Path(__file__).parent 
    ruta_imagen_deeproot = ruta_actual / "assets" / "img" / "deeproot.png"

    return ft.Row(
        ref=referencia,
        controls=[
            ft.Column(
                controls=[
                    # Containers anidados y con estilo
                    ft.Container(
                        ft.Container(
                            ft.Stack(
                                [
                                    # Imágen de Fondo
                                    #ft.Image(
                                    #    src="./img/deep.jpg",
                                    #    width=360,
                                    #    height=260,
                                    #    fit=ft.ImageFit.COVER,
                                    #    border_radius=11,
                                    #),
                                    ft.Container(
                                        border_radius=11,
                                        rotate=ft.Rotate(0.98*3.14),
                                        width=360,
                                        height=260,
                                        bgcolor="#22ffffff",
                                        gradient = ft.LinearGradient([Color.AzulEgipcio,Color.AzulMincyt]),
                                    ),
                                    ft.Container(
                                        ft.Container(
                                            ft.Column(
                                                [
                                                    ft.Container(
                                                        ft.Image(
                                                            src=str(ruta_imagen_deeproot),
                                                            width=100,
                                                        ), padding=ft.padding.only(130),
                                                    ),
                                                    ft.Text(
                                                        "DeepRoot",
                                                        width=360,
                                                        text_align="center",
                                                        weight="w900",
                                                        size=20
                                                    ),
                                                    ft.Text(
                                                        "¡Te damos la bienvenida al cliente de \nInteligencia Artificial!",
                                                        width=360,
                                                        text_align="center",
                                                        weight=ft.FontWeight.BOLD,
                                                        size=14
                                                    ),

                                                ], expand=True, alignment = ft.MainAxisAlignment.CENTER,
                                            ),
                                        ),
                                        border_radius=11,
                                        width=360,
                                        height=260,
                                        bgcolor="#22ffffff",
                                        gradient = ft.LinearGradient([Color.AzulEgipcio,Color.AzulMincyt]),
                                    ),
                                ]
                            ),
                            padding=20,
                            width = 360,
                            height = 560,
                        ),
                        width=400,
                        height=360,
                        #gradient = ft.LinearGradient([Color.AzulEgipcio,Color.AzulMincyt]),
                        expand = True
                    )

                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            expand = True
                        )
                    ],
                    expand=True,
                    alignment = ft.MainAxisAlignment.CENTER,
                )


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
    def __init__(self, page: ft.Page):
        # Referencias para los contenedores de burbujas
        self.ref_burbuja_usuario = Ref[Container]() 
        self.ref_burbuja_ia = Ref[Container]() 
        self.burbujas_ia = []
        self.burbujas_usuario = []
        self.md_burbujas_ia = []
        self.key_burbuja = 0 # para facilitar la navegación por scroll y poder editar o eliminar las burbujas que se requieran.
        self.page = page

    def obtener_color_burbuja(self, es_usuario, theme_mode):
        """Devuelve el color de fondo de la burbuja según el tema y el tipo de usuario."""
        if es_usuario:
            return ThemeLight.GloboUsuarioFondo if theme_mode == "light" else ThemeDark.GloboUsuarioFondo
        else:
            # Si no es usuario, preferimos que la burbuja no tenga color de fondo.
            return None


    def crear_burbuja(self, mensaje, es_usuario, theme_mode, ref_cont_burbuja_ia, ref_cont_burbuja_usuario, ref_md_burbuja_ia):
        """Crea una burbuja de chat con la referencia adecuada."""

        # a partir de la versión 0.27.0 de Flet, las referencias soy para un solo objeto o control a la vez.
        ref_container = ft.Ref[ft.Container]()
        ref_markdown = ft.Ref[ft.Markdown]()
        ref_avatar = ft.Ref[ft.CircleAvatar]()


        bgcolor = self.obtener_color_burbuja(es_usuario, theme_mode)
        #    self.ref_burbuja_usuario if es_usuario else self.ref_burbuja_ia

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



        # Creamos el contenedor de la burbuja
        contenedor_burbuja = Container(
            ref=ref_container,
            content=Markdown(
                value=mensaje,
                ref=ref_markdown,
                extension_set="gitHubWeb", # En próxima versión lo haré configurable
                code_theme="gruvbox-light" if theme_mode == "light" else "gruvbox-dark",
                selectable=True,
                auto_follow_links=True,
            ),
            padding = 10,
            bgcolor = bgcolor,
            border_radius = 10,
        )

        if es_usuario:
            # Creación del Avatar
            avatar = CircleAvatar(
                ref=ref_avatar,
                content=Icon(Icons.PERSON),
                bgcolor=ThemeLight.GloboUsuarioFondo if theme_mode == "light" else ThemeDark.GloboUsuarioFondo
            )
            # alimentamos arreglo de referencias de burbujas del usuario
            self.burbujas_usuario.append((ref_container,ref_markdown,ref_avatar))
            # la burbuja del usuario será acompañada de un avatar.
            fila_controls_burbuja = [avatar, contenedor_burbuja]
        else:
            # alimentamos arreglo de referencias de burbujas de la IA
            self.burbujas_ia.append((ref_container,ref_markdown))
            # la burbuja de la IA será discreta, por lo que no le colocaremos un Avatar, además
            # deseamos tenga un estilo que ocupe el mayor espacio de la pantalla.
            fila_controls_burbuja = [contenedor_burbuja]


        # Devolvemos una fila con el avatar y la burbuja
        return Row(
            controls=fila_controls_burbuja, # Atención con esta solución, puede ser problemática, pero insistiré a ver si granulada la composición funciona.
            alignment=MainAxisAlignment.END if es_usuario else MainAxisAlignment.START,
            key = key_burbuja,
            tight = True,
            wrap = True
        )

    def actualizar_colores_burbujas(self, theme_mode):
        """Actualiza los colores de las burbujas y el code_theme según el tema actual."""

        # Recorrido de todas las burbujas IA para actulizar sus colores
        for ref_cont, ref_md in self.burbujas_ia:
            if ref_cont.current:
                ref_cont.current.bgcolor = ThemeDark.GloboIAFondo if theme_mode == "dark" else None

            if ref_md.current:
                ref_md.current.code_theme = "gruvbox-dark" if theme_mode == "dark" else "gruvbox-light"

        # Recorrido de todas las burubujas de usuario y actualización de los colores
        for ref_cont, ref_md, ref_ava in self.burbujas_usuario:
            if ref_cont.current:
                ref_cont.current.bgcolor = ThemeDark.GloboUsuarioFondo if theme_mode == "dark" else ThemeLight.GloboUsuarioFondo

            if ref_ava.current:
                ref_ava.current.bgcolor = ThemeDark.GloboUsuarioFondo if theme_mode == "dark" else ThemeLight.GloboUsuarioFondo
        self.page.update()
