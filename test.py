import flet as ft

def main(page: ft.Page):
    sistema_huesped = page.platform.value
    texto=ft.Text(sistema_huesped)
    page.add(texto)

ft.app(target=main)
