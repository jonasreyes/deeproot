import flet as ft

def get_icon_boton_prompt(icon,icon_color,tooltip,text,funcion):
    boton=ft.Column(
            [
            ft.IconButton(
                icon=icon,
                icon_color=icon_color,
                icon_size=46,
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


