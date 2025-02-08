import flet as ft

def main(page: ft.Page):
    # Definir colores para los temas
    light_theme = {
        "background": ft.colors.WHITE,
        "text": ft.colors.BLACK,
        "primary": ft.colors.BLUE_500,
        "secondary": ft.colors.GREY_500,
    }

    dark_theme = {
        "background": ft.colors.BLACK,
        "text": ft.colors.WHITE,
        "primary": ft.colors.BLUE_200,
        "secondary": ft.colors.GREY_300,
    }

    # Función para cambiar el tema
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            apply_theme(dark_theme)
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            apply_theme(light_theme)
        page.update()

    # Función para aplicar el tema
    def apply_theme(theme):
        page.bgcolor = theme["background"]
        text_field.bgcolor = theme["background"]
        text_field.color = theme["text"]
        button.bgcolor = theme["primary"]
        button.color = theme["text"]
        page.update()

    # Elementos de la interfaz
    text_field = ft.TextField(label="Ingrese su nombre", width=300)
    button = ft.ElevatedButton("Cambiar tema", on_click=change_theme)

    # Aplicar tema inicial
    apply_theme(light_theme)

    # Añadir elementos a la página
    page.add(text_field, button)

ft.app(target=main)
