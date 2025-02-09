"""
themes.py

Este módulo contiene definiciones de temas (claro y oscuro) para deeproot.
También incluye funciones para aplicar dichos temas.
"""

# Tema claro
theme_claro = {
    "background_color": "#F8EFDC",
    "text_color": "#1F1E1E",
    "button_color": "#E0E0E0",
    "button_text_color": "#1F1E1E",
}

# Tema oscuro
theme_oscuro = {
    "background_color": "#1F1E1E",
    "text_color": "#F8EFDC",
    "button_color": "#333333",
    "button_text_color": "#F8EFDC",
}

# CSS personalizado para las citas
blockquote_decoration={
    "color": "#4CAF50",  # Color verde
    "border-left": "5px solid #4CAF50",  # Borde izquierdo verde
    "padding": "10px",  # Espaciado interno
    "background-color": "#E8F5E9",  # Fondo verde claro
    "margin": "10px 0",  # Margen exterior
    "border-radius": "10px",  # Esquinas redondeadas
    "box-shadow": "2px 2px 5px rgba(0, 0, 0, 0.1)",  # Sombra
}

pre={
    "background-color": "#263238",  # Fondo oscuro
    "color": "#FFFFFF",  # Texto blanco
    "padding": "10px",  # Espaciado interno
    "border-radius": "5px",  # Esquinas redondeadas
}

h2={
    "color": "#673AB7",  # Color morado
    "font-size": "20px",
}

code={
    "background-color": "#F5F5F5",  # Fondo gris claro
    "color": "#D32F2F",  # Texto rojo
    "padding": "2px 4px",
    "border-radius": "3px",
}

li={
    "margin-bottom": "5px",  # Espaciado entre elementos de la lista
}
