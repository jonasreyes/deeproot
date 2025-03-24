Instrucciones:

# Acceder al directorio 
```bash
cd deeproot
```

# Generación del Entorno Virtual
```bash
python3 -m venv .venv
```

# Generación del Entorno Virtual
```bash
python3 -m venv .venv
```

# Activación del entorno virtual
```bash
# Para activar el entorno ejecute:
source .venv/bin/activate

# Para desactivar el entorno:
deactivate
```

# Actualización de pip
```bash
pip install --upgrade pip
```

# Instalar Flet
```bash
pip install 'flet[full]'
```

# Comprobar que la versión de Flet sea al menos la 0.27.0
```bash
flet --version
```

# Intalar las librerías dependencias de DeepRoot
```bash
pip install openai asyncio markdown
```

# Correr o Iniciar DeepRoot
```bash
flet run main.py
```

# Crear una alias en .bashrc o .zshrc
```bash
alias dr="source /home/canaima/dev_testing/deeproot_test/.venv/bin/activate && nohup flet run /home/canaima/dev_testing/deeproot_test/main.py &"
```

# Arrancar DeepRoot desde terminal
```bash
dr
```

## Licencia

DeepRoot es software libre bajo los términos de la [Licencia de Software Libre de DeepRoot](LICENSE).  
Puedes usar, copiar, modificar y distribuir este software, siempre que cumplas con los términos de la licencia.  
Para más detalles, consulta el archivo [LICENSE](LICENSE) en este repositorio.
