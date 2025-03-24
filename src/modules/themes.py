"""
themes.py

Este módulo contiene definiciones de temas (claro y oscuro) para deeproot.
También incluye funciones para aplicar dichos temas.
"""

# Colores para DeepRoot
class Color:
    # Colores Mincyt
    AzulMincyt = "#1D70B7"
    GrisMincyt = "#9C9B9B"
    MoradoMincyt = "#653188"
    NaranjaMincyt = "#F08427"
    TeMincyt = "#02A7AB"
    VerdeMincyt = "#026E71"

    # Colores Futuro MS.
    AzulCieloFuturo = "#A6D8E2"
    AzulFuturo = "#1440AD"
    BeigeFuturo = "#F8EFDC"
    DoradoFuturo = "#EFC318"
    NaranjaFuturo = "#EC6C3A"
    NegroFuturo = "#1F1E1E"
    RojoFuturo = "#E63022"

    # Colores Estándares Chat
    # Día - Light
    AzulCian = "#E3F2FD"
    VerdeClaroLight = "#E8F5E9"
    Negro = "#000000"
    GrisOscuroLight = "#333333"
    BlancoAhumado = "#F5F5F5"
    #Noche - Dark
    AzulEgipcio = "#0D47A1"
    VerdeOscuroDark = "#1B5E20"
    Blanco = "#FFFFFF"
    GrisClaro = "#E0E0E0"
    GrisMedio = "#424242"
    GrisOscuroDark = "#121212"


# Clase ThemeLight
# Día - Light
# Globo hace referencia a la burbuja del Chat
class ThemeLight:
    # Burbuja del usuario
    GloboUsuarioFondo = Color.AzulCian
    GloboUsuarioTexto = Color.Negro

    # Burbuja de la IA
    GloboIAFondo = Color.BlancoAhumado
    GloboIATexto = Color.GrisOscuroLight

    # Fondo de la Interfáz de DeepRoot
    AppFondo = Color.BlancoAhumado

# Clase ThemeDark
# Noche - Dark
# Globo hace referencia a la burbuja del Chat
class ThemeDark:
    # Burbuja del usuario
    GloboUsuarioFondo = Color.AzulEgipcio
    GloboUsuarioTexto = Color.GrisClaro

    # Burbuja de la IA
    GloboIAFondo = Color.GrisMedio
    GloboIATexto = Color.GrisClaro

    # Fondo de la Interfáz de DeepRoot
    AppFondo = Color.GrisOscuroDark
