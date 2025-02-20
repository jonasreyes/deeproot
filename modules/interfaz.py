import flet as ft

def get_icon_boton_prompt(icon,icon_color,tooltip,text,funcion):
    boton=ft.Column(
            [
            ft.IconButton(
                icon=icon,
                icon_color=icon_color,
                icon_size=48,
                tooltip=tooltip,
                on_click=funcion
            ),
            ft.Text(text, size=12)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
            )
    return boton
