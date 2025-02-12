    # str: Campo de salida de la respuesta de la IA, el estilo y formato se dará desde la fución actualizar_markdown()
    campo_respuesta = ft.ListView(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Bienvenido a DeepRoot Cliente API de DeepSeek AI", 
                            weight=ft.FontWeight.W_600, 
                            size=20, color="blue900", 
                            text_align=ft.TextAlign.CENTER, selectable=True),
                        ft.Text(
                            fecha_formateada, 
                            weight=ft.FontWeight.W_200, 
                            size=16, color="blue900", 
                            text_align=ft.TextAlign.CENTER, selectable=True),
                    ],
                    spacing=0
                ),
                bgcolor=ft.Colors.BLUE_100,
                border_radius=10,
                padding=10,
                expand=True,
            ),
        ],
        expand=True,
        spacing=10,
    )
