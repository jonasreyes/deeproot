# Este archivo contiene temporalmente hasta que sea refactorizada DeepRoot
# las funciones útiles que deben estar disponibles.
from datetime import datetime

# Generar la hora para la IA y/o usuario
def get_hoy(para_ia=True):
    hoy = datetime.now()
    if para_ia:
        fecha_de_hoy = hoy.strftime("(Fecha Actual Incorporada en el Historial de la IA al inicio de la conversación con el usuario: %A %d de %B del año %Y. Hora Actual: %I:%M%p. Horario en base a la locación: Caracas, Venezuela.)")
    else:
        fecha_de_hoy = hoy.strftime("(Fecha Actual Concatenada al inicio de cada prompt del usuario: %A %d de %B del año %Y. Hora Actual: %I:%M%p. Horario en base a la locación: Caracas, Venezuela.)")
    return fecha_de_hoy

# Generar el prompt oculto con la configuración actual
def generar_prompt_oculto(prompt, config):
    fecha_mas_reciente = get_hoy(para_ia=False)
    prompt_oculto = f"""
    Configuración Actual:
    - Fecha más reciente: {fecha_mas_reciente},
    - Modelo: {config["modelo"]}
    - Temperatura: {config["temperature"]}
    - Top_P: {config["top_p"]}
    - Máximo de Tokens: {config["max_tokens"]}
    - Streaming: {config["stream"]}
    - URL Base: {config["url_base"]}
    - Extension Set: {config["extension_set"]}
    - Tema de Código: {config["code_theme"]}
    - Tema de Código Claro: {config["code_theme_claro"]}
    - Tema de Código Oscuro: {config["code_theme_oscuro"]}
    - Modo de Tema: {config["theme_mode"]}
    - Usar Enter: {config["usar_enter"]}

    Prompt del Usuario:
    {prompt}
    """
    return prompt_oculto
