# Guía del Instalador DeepRoot

Esta guía proporciona información detallada y pedagógica sobre el script de instalación `deeproot_install.sh`. Aprenderás sobre su propósito, requisitos, funciones, cómo utilizarlo y cómo solucionar problemas comunes.

## ¿Qué es DeepRoot?

DeepRoot es una aplicación de escritorio hecha en Python y Flet para el acceso a modelos avanzados de IA (LLMs) a través de su API. Este instalador te ayudará a configurarla fácilmente en tu sistema Canaima GNU/Linux y cualquier otra distribución.

## Propósito del Instalador

El script `deeproot_install.sh` automatiza la instalación de DeepRoot en sistemas Linux. Realiza las siguientes tareas:

*   **Verificación de Dependencias:** Asegura que tu sistema tenga las herramientas necesarias (git, curl, python3).
*   **Creación de Directorios:** Organiza los archivos de DeepRoot en ubicaciones adecuadas.
*   **Clonación del Repositorio:** Descarga el código fuente de DeepRoot desde GitHub.
*   **Entorno Virtual de Python:** Crea un espacio aislado para las dependencias de DeepRoot.
*   **Instalación de Dependencias:** Instala las librerías de Python que DeepRoot necesita.
*   **Comandos Alias:** Crea atajos para ejecutar DeepRoot y tareas relacionadas.
*   **Lanzador Gráfico (Opcional):** Agrega un icono al menú de tu sistema para iniciar DeepRoot.
*   **Resumen de la Instalación:** Muestra información importante sobre la configuración.

## Requisitos del Sistema

Antes de comenzar, verifica que tu sistema cumpla con estos requisitos:

*   **Sistema Operativo:** Cualquier distribución Linux (probado en Debian, Ubuntu, Fedora, Arch, etc.).
*   **Herramientas Esenciales:**
    *   `git`: Para descargar el código de DeepRoot.
    *   `curl`: Para descargar el script de desinstalación.
    *   `python3`: Para ejecutar DeepRoot y gestionar sus dependencias.
    *   `python3-venv`: (Recomendado) Para crear un entorno virtual aislado.
*   **Conexión a Internet:** Necesaria para descargar archivos.

## Paso a Paso: Instalación de DeepRoot

Sigue estos pasos para instalar DeepRoot:

1.  **Descarga el Instalador:**

    Abre tu terminal y usa `wget` para descargar el script:

    ```bash
    wget https://raw.githubusercontent.com/jonasreyes/deeproot/main/scripts/deeproot_install.sh
    ```

2.  **Haz el Instalador Ejecutable:**

    Dale permiso de ejecución al script:

    ```bash
    chmod +x deeproot_install.sh
    ```

3.  **Ejecuta el Instalador:**

    Inicia el proceso de instalación:

    ```bash
    ./deeproot_install.sh
    ```

    El instalador te guiará a través de los siguientes pasos, solicitando información cuando sea necesario.

## Explicación Detallada del Proceso de Instalación

El instalador realiza una serie de tareas para configurar DeepRoot. Aquí hay una explicación más profunda de cada paso:

1.  **Verificación de Dependencias:**

    El instalador verifica si tienes `git`, `curl` y `python3` instalados. Si alguna de estas herramientas falta, te mostrará un mensaje con las instrucciones para instalarla.

    **Ejemplo:**

    Si `git` no está instalado, verás algo como esto:

    ```
    ❌ Error: git no está instalado. Instálalo para continuar.
      sudo apt install git  (Para sistemas Debian/Ubuntu)
    ```

2.  **Creación de Directorios:**

    El instalador crea los siguientes directorios:

    *   `~/apps`: (Si no existe) Para almacenar las aplicaciones.
    *   `~/apps/deeproot`: Donde se instalará DeepRoot.
    *   `~/.config/deeproot`: Para guardar la configuración de DeepRoot.
    *   `~/.config/deeproot/logs`: Para almacenar los logs de DeepRoot.

3.  **Clonación del Repositorio:**

    El instalador usa `git` para descargar el código fuente de DeepRoot desde GitHub:

    ```
    git clone https://github.com/jonasreyes/deeproot.git ~/apps/deeproot
    ```

4.  **Entorno Virtual de Python:**

    El instalador crea un entorno virtual aislado para las dependencias de Python de DeepRoot:

    ```
    python3 -m venv ~/apps/deeproot/.venv
    ```

    Esto asegura que las dependencias de DeepRoot no entren en conflicto con otras aplicaciones en tu sistema.

5.  **Instalación de Dependencias de Python:**

    El instalador activa el entorno virtual e instala las librerías de Python necesarias:

    ```
    source ~/apps/deeproot/.venv/bin/activate
    pip install --upgrade pip
    pip install flet openai asyncio markdown python-dotenv
    ```

6.  **Comandos Alias:**

    El instalador crea alias para facilitar la ejecución de DeepRoot y tareas relacionadas. Estos alias se agregan a tu archivo `.bashrc` o `.zshrc`:

    *   `deeproot`: Inicia la aplicación DeepRoot.
    *   `deeproot-update`: Actualiza DeepRoot a la última versión.
    *   `deeproot-uninstall`: Desinstala DeepRoot.
    *   `deeproot-logs`: Muestra los logs de DeepRoot.
    *   `deeproot-exports`: Abre el directorio de exportaciones de DeepRoot.

    **Ejemplo:**

    Para iniciar DeepRoot, simplemente escribe `deeproot` en tu terminal y presiona Enter.

7.  **Lanzador Gráfico (Opcional):**

    El instalador puede crear un lanzador gráfico para DeepRoot, agregando un icono al menú de tu sistema.

8.  **Resumen de la Instalación:**

    Al finalizar, el instalador muestra un resumen de la instalación, incluyendo información sobre los directorios, comandos y recomendaciones.

## Solución de Problemas Comunes

*   **`libmpv.so.1` no encontrado:**

    DeepRoot necesita la librería `libmpv.so.1` para funcionar correctamente. Si el instalador no la encuentra, te mostrará un mensaje con las siguientes opciones:

    *   **Instalar `libmpv1` (o el paquete equivalente) usando el gestor de paquetes de tu distribución.** Por ejemplo:

        ```bash
        sudo apt update && sudo apt install libmpv1  (Para Debian/Ubuntu)
        ```

    *   **Crear un enlace simbólico si tienes una versión diferente de `libmpv` instalada (ej: `libmpv.so.2` o `libmpv.so`).**

        El instalador te mostrará el comando exacto para crear el enlace simbólico:

        ```
        sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1
        ```

        **Importante:** Reemplaza las rutas en el comando con las correctas para tu sistema.

*   **Error al crear el entorno virtual:**

    Asegúrate de tener instalado el paquete `python3-venv`:

    ```bash
    sudo apt install python3-venv  (Para Debian/Ubuntu)
    ```

*   **Error al instalar dependencias de Python:**

    Verifica tu conexión a Internet y asegúrate de tener la última versión de `pip`:

    ```bash
    python3 -m pip install --upgrade pip
    ```

*   **Comandos alias no funcionan:**

    Recarga la configuración de tu terminal:

    ```bash
    source ~/.bashrc  (Si usas Bash)
    source ~/.zshrc  (Si usas Zsh)
    ```

    O simplemente cierra y vuelve a abrir tu terminal.

## Desinstalación de DeepRoot

Para desinstalar DeepRoot, ejecuta el script `deeproot_uninstall.sh` que se encuentra en el directorio de instalación:

```bash
~/apps/deeproot/scripts/deeproot_uninstall.sh
```

El script te guiará a través del proceso de desinstalación, eliminando los archivos de DeepRoot, los alias y la configuración.

## Contribución

Si deseas contribuir al desarrollo de DeepRoot, visita el repositorio en GitHub: [https://github.com/jonasreyes/deeproot](https://github.com/jonasreyes/deeproot).



