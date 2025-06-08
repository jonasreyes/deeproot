# 🐋 DeepRoot - Interfaz gráfica para interacción con modelos avanzados de IA (LLMs)

[![Licencia](https://img.shields.io/badge/Licencia-DeepRoot_LSS-blue)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Versión](https://img.shields.io/badge/Versión-v0.2.3_Beta-orange)

**Aplicación de escritorio para interactuar con modelos de IA como DeepSeek y Otros**
*Actualización constante de modelos compatibles vía API*

![Logo de DeepRoot](src/assets/images/deeproot_foot.png)  
*Ballena de DeepRoot - Símbolo de raíces profundas*  

---
## 📹 Videos Relacionados
1. **Demo de Instalación**:  
   [![Ver Demo](https://img.shields.io/badge/▶-Instalación-red?style=for-the-badge)](https://rutube.ru/video/f59e3cd104a92965b0add83a40c95047/)
   [![Ver Instalación Automática](https://img.shields.io/badge/▶-Instalación_Automática-red?style=for-the-badge)](https://rutube.ru/video/a676e7291e85da660158b9b4e87b569f/)

2. **Ponencias FLISoL 2025**:  
   [![Ver Ponencia en la Universidad Central de Venezuela (28/Abril/2025)](https://img.shields.io/badge/▶-UCV_Caracas_2025-blue?style=for-the-badge)](https://rutube.ru/video/f44cd2d55b1a54142cff072faace7133/)
   [![Ver Ponencia en la Universidad de Carabobo (09/Mayo/2025)](https://img.shields.io/badge/▶-UC_Carabobo_2025-blue?style=for-the-badge)](https://rutube.ru/video/7bbadb4c10bf7c041e9fe5c0dafa2e48/)

3. **Entrevistas 2025**:  
   [![PodCast "Más Allá del Código (28/Abril/2025)](https://img.shields.io/badge/▶-PODCAST_Más_Allá_del_Código-blue?style=for-the-badge)](https://youtu.be/pG4Gq39AmY4?si=0VzZoBPugqYpz3EL)
---
## 📌 Tabla de Contenidos
1. [Filosofía](#-filosofía)
2. [Características](#-características)
3. [Instalación](#-instalación)
    *   [Guía del Instalador de DeepRoot](#guía-del-instalador-de-deeproot)
    *   [Resolución de la Dependencia `libmpv.so.1`](#resolución-de-la-dependencia-libmpvso2)
4. [Interfaz](#-interfaz)
5. [Uso Avanzado](#-uso-avanzado)
6. [Reportar Problemas](#-reportar-problemas)
7. [Contribuir](#-contribuir)
8. [Licencia](#-licencia)

---
## 🌍 Filosofía
**DeepRoot** - Herramienta venezolana que democratiza el acceso a IA avanzada mediante software libre. Inspirada en principios de soberanía tecnológica y desarrollo comunitario.

### ¿Qué hace diferente a DeepRoot?
1. **Enfoque de empoderamiento comunitario**:
   - No solo es un cliente de IA, es una herramienta para la apropiación social del conocimiento tecnológico.
   - Diseñada específicamente para integrarse con Canaima GNU/Linux, distribución Venezolana (compatible con cualquier distribución GNU/Linux).

2. **Modelo de desarrollo alternativo**:
   - Prioriza modelos con licencias libres/open-source.
   - Permite control completo sobre los parámetros de los modelos (en desarrollo).

1. **Ventajas estratégicas**:
   - Facilita la experimentación con ingeniería de prompts (en desarrollo).
   - Ideal para investigación y desarrollo de capacidades locales en IA.

### Descripción en otros idiomas:
- **English**: Venezuelan-developed GUI for API access to LLMs with focus on technological sovereignty.
- **Chino (Simplified)**: 委内瑞拉开发的LLM API图形界面，专注于技术主权。(Wěinèiruìlā kāifā de LLM API túxíng jièmiàn, zhuānzhù yú jìshù zhǔquán.)
- **Ruso**: Венесуэльский графический интерфейс для доступа к LLM через API с акцентом на технологический суверенитет. (Venesuel'skiy graficheskiy interfeys dlya dostupa k LLM cherez API s aktsentom na tekhnologicheskiy suverenitet.)

---
## 🚀 Características  

### 🔍 Multi-Modelos  
- Soporte para **deepseek-chat**, **deepseek-coder**, **deepseek-reasoner** y **gemini-2.0-flash** (pronto habrán más).
- Configuración de parámetros (tokens, temperatura (pronto serán incorporados más)).
- Acceso completo a la potencia del modelo vía API (no limitado como chatbots comerciales).

### 🎨 Personalización  
- Temas claros/oscuros  
- Resaltado de sintaxis  
- Adaptable a diferentes contextos institucionales (universidades, comunidades, planteles educativos, organismos gubernamentales, empresas privadas, entre otros).

### 📤 Exportación  
- Conversaciones en Markdown/HTML  
- Ideal para documentar procesos de investigación

### 💡 Características únicas
- **Desarrollo nacional**: Creado por y para la realidad venezolana.
- **Formación**: Herramienta pedagógica para aprender IA.
- **Soberanía**: Alternativa real a plataformas que promueven dependencia.

---
## 🖼️ Interfaz Gráfica

![Pantalla Principal](src/assets/images/capture_pantalla_principal.png)  
*Interfaz principal con áreas de chat y controles - Diseñada para usabilidad en entornos educativos*

![Configuración API](src/assets/images/capture_acceso_api.png)  
*Ingreso de credenciales API - Compatible con múltiples proveedores*

![Configuración Modelo](src/assets/images/configuracion_modelo.png)  
*Ajustes avanzados de modelos - Control sobre los parámetros*

---
## 📥 Instalación  

### Requisitos  
- **Python 3.8+**  
- **Git** (opcional)  
- **Canaima GNU/Linux** (recomendado) o cualquier distro Linux

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

Para una guía detallada sobre el proceso de instalación, consulta la [Guía del Instalador de DeepRoot](https://github.com/jonasreyes/deeproot/blob/main/docs/Guia%20del%20Instalador%20de%20DeepRoot.md). Esta guía te proporcionará información paso a paso sobre cómo instalar DeepRoot y solucionar problemas comunes.

### Resolución de la Dependencia `libmpv.so.1`

DeepRoot requiere la librería `libmpv.so.1` para algunas funcionalidades. Si el instalador no la encuentra, sigue estos pasos:

1.  **Intenta instalar el paquete `libmpv1` (o el equivalente) usando el gestor de paquetes de tu distribución:**

    *   **Canaima/Debian/Ubuntu:**
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

2.  **Si ya tienes instalada una versión diferente de `libmpv` (ej: `libmpv.so.2`), crea un enlace simbólico:**
    ```bash
    sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1
    sudo ldconfig
    ```

---
## 🔧 Uso Avanzado

### Configuración Inicial de API
1. **Acceso API**:
   - Abre la pestaña `Acceso API`
   - Ingresa tu `key_api`

2. **Base URL**:
   - DeepSeek: `https://api.deepseek.com`
   - Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`

3. **Selección de Modelo**:
   - Elige modelo compatible con tu API key y Base URL
   - Recomendado: DeepSeek por su política de acceso más abierta

4. **Guardar**:
   - Presiona `Guardar` para aplicar cambios

### Consejos para investigación:
- Usa DeepSeek-Coder para desarrollo de software.
- DeepSeek-Reasoner para análisis complejos (la implementación de este modelo está en desarrollo pero ya puedes realizar consultas con él).
- Exporta tus conversaciones para documentar hallazgos.

---
## 🗑️ Desinstalación  
```bash
curl -sSL https://raw.githubusercontent.com/jonasreyes/deeproot/main/scripts/deeproot_uninstall.sh | bash
```

---
## 🐞 Reportar Problemas  
1. **Describe el problema**  
2. **Pasos para reproducirlo**  
3. **Captura de pantalla** (opcional)  

Opciones:  
- [Abrir Issue en GitHub](https://github.com/jonasreyes/deeproot/issues)  
- [Formulario de Telegram](https://t.me/deeproot_app)  

---
## 🤝 Contribuir  
1. Haz fork del repositorio  
2. Crea una rama: `git checkout -b mi-mejora`  
3. Envía Pull Request  

*¿Primera vez contribuyendo?* [Guía básica](https://guides.github.com/activities/hello-world/)  

**Áreas prioritarias para contribuciones:**
- Traducciones
- Documentación
- Pruebas en diferentes distribuciones
- Desarrollo de nuevas funcionalidades

---
## 📜 Licencia  
[Licencia DeepRoot](LICENSE) (GPL-compatible)  

---
## 🔗 Enlaces  
- [Canal Oficial](https://t.me/deeproot_app)  
- [Desarrollador](https://t.me/jonasroot)  
- [Repositorio](https://github.com/jonasreyes/deeproot)  
- [Sumarse a la Iniciativa Patria y Software Libre](https://forms.yandex.com/u/6744ba73f47e73bf11681c4e/)

*"DeepRoot es más que software, es un proyecto de soberanía tecnológica"*  
*¡Gracias por usar DeepRoot y ser parte de este movimiento!*
