# 🐋 DeepRoot - Interfaz gráfica para interacción con modelos avanzados de IA (LLMs)

[![Licencia](https://img.shields.io/badge/Licencia-DeepRoot_LSS-blue)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Versión](https://img.shields.io/badge/Versión-v0.1.0_Beta-orange)

**Aplicación de escritorio para interactuar con modelos de IA como DeepSeek y Gemini**  
*Actualización constante de modelos compatibles vía API*

![Logo de DeepRoot](src/assets/images/deeproot_foot.png)  
*Ballena de DeepRoot - Símbolo de raíces profundas*  

---
## 📹 Videos Relacionados
1. **Demo de Instalación**:  
   [![Ver Demo](https://img.shields.io/badge/▶-Instalación-red?style=for-the-badge)](https://rutube.ru/video/f59e3cd104a92965b0add83a40c95047/)
2. **Ponencia FLISoL 2025**:  
   [![Ver Ponencia](https://img.shields.io/badge/▶-FLISoL_2025-blue?style=for-the-badge)](https://rutube.ru/video/f44cd2d55b1a54142cff072faace7133/)

---
## 📌 Tabla de Contenidos
1. [Filosofía](#-filosofía)
2. [Características](#-características)
3. [Instalación](#-instalación)
    *   [Guía del Instalador de DeepRoot](#guía-del-instalador-de-deeproot)
    *   [Resolución de la Dependencia `libmpv.so.1`](#resolución-de-la-dependencia-libmpvso1)
4. [Interfaz](#-interfaz)
5. [Uso Avanzado](#-uso-avanzado)
6. [Reportar Problemas](#-reportar-problemas)
7. [Contribuir](#-contribuir)
8. [Licencia](#-licencia)

---
## 🌍 Filosofía
**DeepRoot** - Herramienta venezolana que democratiza el acceso a IA avanzada mediante software libre. Inspirada en principios de soberanía tecnológica y desarrollo comunitario.

### Descripción en otros idiomas:
- **English**: Venezuelan-developed GUI for API access to LLMs.
- **Chino (Simplificado)**: 委内瑞拉开发的图形用户界面，用于通过 API 访问 LLM 模型。(Wěinèiruìlā kāifā de túxíng yònghù jièmiàn, yòng yú tōngguò API fǎngwèn LLM móxíng.)
- **Ruso**: Графический интерфейс, разработанный в Венесуэле для доступа к LLM-моделям через API. (Graficheskiy interfeys, razrabotannyy v Venesuele dlya dostupa k LLM-modelyam cherez API.)

---
## 🚀 Características  

### 🔍 Multi-Modelos  
- Soporte para **deepseek-chat**, **deepseek-coder**, **deepseek-reasoner** y **gemini-2.0-flash**  
- Configuración de parámetros (tokens, temperatura)  

### 🎨 Personalización  
- Temas claros/oscuros  
- Resaltado de sintaxis  

### 📤 Exportación  
- Conversaciones en Markdown/HTML  
- Compatibilidad con Obsidian  

---
## 🖼️ Interfaz Gráfica

![Pantalla Principal](src/assets/images/capture_pantalla_principal.png)  
*Interfaz principal con áreas de chat y controles*

![Configuración API](src/assets/images/capture_acceso_api.png)  
*Ingreso de credenciales API*

![Configuración Modelo](src/assets/images/configuracion_modelo.png)  
*Ajustes avanzados de modelos*

---
## 📥 Instalación  

### Requisitos  
- **Python 3.8+**  
- **Git** (opcional)  

### 1. Método Automático  
```bash
curl -sSL https://raw.githubusercontent.com/jonasreyes/deeproot/main/scripts/deeproot_install.sh | bash
```

### 2. Manual  
```bash
git clone https://github.com/jonasreyes/deeproot.git
cd deeproot
./scripts/deeproot_install.sh
```

### Guía del Instalador de DeepRoot

Para una guía detallada sobre el proceso de instalación, consulta la [Guía del Instalador de DeepRoot](docs/Guia del Instalador de DeepRoot.md). También disponible en formato [PDF](docs/Guia del Instalador de DeepRoot.pdf). Esta guía te proporcionará información paso a paso sobre cómo instalar DeepRoot y solucionar problemas comunes.

### Resolución de la Dependencia `libmpv.so.1`

DeepRoot requiere la librería `libmpv.so.1` para algunas funcionalidades. Si el instalador no la encuentra, sigue estos pasos:

1.  **Intenta instalar el paquete `libmpv1` (o el equivalente) usando el gestor de paquetes de tu distribución:**

    *   **Debian/Ubuntu:**

        ```bash
        sudo apt update && sudo apt install libmpv1
        ```

    *   **Arch Linux/Manjaro:**

        ```bash
        sudo pacman -S mpv
        ```

    *   **Fedora/RHEL/CentOS:**

        ```bash
        sudo dnf install mpv-libs
        ```

    *   **openSUSE/SLES:**

        ```bash
        sudo zypper install libmpv1
        ```

    Si no encuentras el paquete `libmpv1`, busca un paquete similar en tu distribución.

2.  **Si ya tienes instalada una versión diferente de `libmpv` (ej: `libmpv.so.2` o `libmpv.so`), puedes crear un enlace simbólico:**

    *   **Identifica la ruta completa de la librería instalada:**

        ```bash
        ls -l /usr/lib/x86_64-linux-gnu/libmpv.so.2
        ```

        Reemplaza `/usr/lib/x86_64-linux-gnu/libmpv.so.2` con la ruta correcta de tu librería.

    *   **Crea el enlace simbólico:**

        ```bash
        sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1
        ```

        Reemplaza `/usr/lib/x86_64-linux-gnu/libmpv.so.2` con la ruta correcta de tu librería.

    **Importante:** Después de crear el enlace simbólico, ejecuta:

    ```bash
    sudo ldconfig
    ```

    Esto actualizará el caché de las librerías del sistema.

3.  **Verifica la instalación:**

    ```bash
    ldconfig -p | grep libmpv
    ```

    Esto mostrará las librerías `libmpv` instaladas en tu sistema.

**Nota:** El enlace simbólico es una solución temporal. Para la mejor experiencia, instala el paquete nativo de tu distribución.

---
## 🗑️ Desinstalación  
```bash
curl -sSL https://raw.githubusercontent.com/jonasreyes/deeproot/main/scripts/deeproot_uninstall.sh | bash
```

---
## 🐞 Reportar Problemas  

### Para usuarios noveles:  
1. **Describe el problema**: Qué esperabas vs qué ocurrió  
2. **Pasos para reproducirlo**:  
   ```
   1. Abrir DeepRoot  
   2. Ir a Configuración API  
   3. Ingresar clave inválida  
   ```  
3. **Captura de pantalla** (opcional pero útil)  

### Opciones:  
- [Abrir Issue en GitHub](https://github.com/jonasreyes/deeproot/issues)  
- [Formulario de Telegram](https://t.me/deeproot_app) (más sencillo)  

---
## 🤝 Contribuir  
1. Haz fork del repositorio  
2. Crea una rama: `git checkout -b mi-mejora`  
3. Envía Pull Request  

*¿Primera vez contribuyendo?* [Guía básica](https://guides.github.com/activities/hello-world/)  

---
## 📜 Licencia  
[Licencia DeepRoot](LICENSE) (GPL-compatible)  

---
## 🔗 Enlaces  
- [Canal Oficial](https://t.me/deeproot_app)  
- [Desarrollador](https://t.me/jonasroot)  
- [Repositorio](https://github.com/jonasreyes/deeproot)  

*¡Gracias por usar DeepRoot!* 
