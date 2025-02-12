"""
Nombre de la aplicación: DEEPROOT
Versión: 0.0.1
Autor: Jonás Antonio Reyes Casanova (jonasroot)
Fecha de creación: 28-01-2025
Última actualización: 09-02-2025

Descripción:
Esta aplicación es un cliente de escritorio y móvil para facilitar el acceso y disfrute del Servicio API de DeepSeek. Se requiere de un token de DeepSeek Platform para poder funcionar. Es un desarrollo independiente, inspirado en los valores del Software Libre en Venezuela. Es resultado de los incentivos éticos de la Universidad Bolivariana de Venezuela y la Comunidad de Canaima GNU/Linux.

Licencia:
Este software se distribuye bajo la licencia GNU GPL v3.0.
Puedes encontrar una copia de la licencia en https://www.gnu.org/licenses/gpl-3.0.html#license-text
Este código es libre y debe permanecer así. Si realizas modificaciones o derivados, debes mencionar al autor original (yo) y mantener esta misma licencia.

Contacto:
- Canal de Telegram: t.me/jonasroot (comenta una publicación)
- Repositorio: https://github.com/jonasreyes/deeproot.git

"La verdadera inteligencia no solo resuelve problemas, sino que cultiva la vida..."
#PatriaYSoftwareLibre
"""
import flet as ft
import openai
import asyncio
from openai import OpenAIError, APIConnectionError, APIError

# Inicializando cliente OpenAI
async def enviar_consulta_a_deepseek(page, prompt, campo_respuesta,contenedor_respuesta_prompt_md, respuesta_ai_text, modelo, api_key, url_base):
    try:
        client = openai.OpenAI(api_key=api_key, base_url=url_base)

        campo_respuesta.controls.append(ft.Text("Procesando tu solicitud..."))
        await campo_respuesta.update_async()

        respuesta = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Te llamas DeepSeek, y charlamos a través de DeepRoot un Cliente API para DeepSeek. Eres un asistente y experto programador promotor del software libre."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            stream=True,
        )

        respuesta_ai_text.value = ft.Text("Probando RespuestaAIText, aquí el texto **puede** contener **Markdown**.")
        # Respuestas - EXPERIMENTAL
        # Respuesta que devuelve la IA
        respuesta_prompt_md = ft.Text(
            prompt, 
            weight=ft.FontWeight.W_600, 
            size=20, color="blue900", 
            text_align=ft.TextAlign.CENTER, 
            selectable=True
        )
        contenedor_respuesta_prompt_md.controls.append(respuesta_prompt_md)
        contenedor_respuesta_prompt_md.update_async()

        # Procesar cada chunk de la respuesta
        campo_respuesta.controls.append(contenedor_respuesta_prompt_md)
        campo_respuesta.update_async()
        for chunk in respuesta:
            if chunk.choices[0].delta.content:
                chunk_texto = chunk.choices[0].delta.content
                respuesta_ai_text.value += chunk_texto
                campo_respuesta.controls.append(respuesta_ai_text)
                print(f"Campo: {chunk_texto}")
                await campo_respuesta.update_async()  # Se actualiza la interfaz en tiempo real
                await asyncio.sleep(0)

    except asyncio.TimeoutError:
        # En caso de que el servidor no responda en el tiempo especificado
        campo_respuesta.controls.append(ft.Text("Error: El servidor no respondió a tiempo. Intenta de nuevo."))
        await campo_respuesta.update_async()
    except (APIError, APIConnectionError, OpenAIError) as e:
        # Manejo de errores con la API
        campo_respuesta.controls.append(ft.Text(f"Error de conexión con la IA: {str(e)}"))
        await campo_respuesta.update_async()
    except Exception as e:
        # Manejo de cualquier otro error no esperado
        campo_respuesta.controls.append(ft.Text(f"Error inesperado: {str(e)}"))
        await campo_respuesta.update_async()

