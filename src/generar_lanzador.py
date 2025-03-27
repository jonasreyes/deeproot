import os
import platform
import shutil

# Verificación de instalación para GNU/Linux
if platform.system() != "Linux":
    print ("Este script de instalación solo funciona para GNU/Linux.")
    exit(1)

## creamos directorio de configuración
#config_dir = os.path.join(os.path.expanduser("~"), ".config", "deeproot")
#os.makedirs(config_dir, exist_ok=True)
#
## Si no existe el archivo de configuración de deeproot lo creamos.
#config_file = os.path.join(config_dir, "deeproot.json")
#config_file_default = {
#        "usar_enter": False,
#        "modelo": "deepseek-chat",
#        "theme_mode": "ft.ThemeMode.LIGHT",
#        "code_theme": "gruvbox-light",
#        "code_theme_claro": "gruvbox-light",
#        "code_theme_oscuro": "gruvbox-dark",
#        "extension_set": "gitHubWeb",
#        "api_key": "",
#        "url_base": "",
#        "stream": True,
#        "max_tokens": 8192, # por defecto usa 4096, otros números: 2048, 1024, 512
#        "temperature":0.0 
#        }
#
#if not os.path.exists(config_file):
#    print("No existe un archivo de configuración previo.")
#    with open(config_file, "w") as f:
#        f.write(config_file_default) # Archivo json vacío

# Creamos el lanzador (archivo .desktop)
desktop_content = f"""[Desktop Entry]
Name=DeepRoot
Exec={os.path.abspath("../.venv/bin/python")} {os.path.abspath("main.py")}
Icon={os.path.abspath("assets/images/deeproot.png")}
Type=Application
Categories=Utility;Application;
Terminal=false
"""

desktop_file = "deeproot.desktop"
with open(desktop_file, "w") as f:
    f.write(desktop_content)

# Copiamos el archivo .dektop a la ubicación correcta
destino = os.path.join(os.path.expanduser("~"), ".local", "share", "applications", desktop_file)
shutil.copy(desktop_file, destino)

# Damos permiso de ejecución
os.chmod(destino, 0o755)
print("Intalación completada. DeepRoot ahora está disponible en el menú de aplicaciones.")
