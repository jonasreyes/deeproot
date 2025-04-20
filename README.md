# 🌊 DeepRoot - Una aplicación GUI multimodal diseñada para interactuar con modelos avanzados de IA (LLM) de licencia software libre y código abierto, facilitando el acceso a inteligencia artificial libre, sin censura y altamente personalizable.
[![Licencia](https://img.shields.io/badge/Licencia-DeepRoot_LSS-blue)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)

**Cliente Modelos Avanzados IA (LLM) Licenciados en Software Libre y/o Código Abierto.**  
*Actualmente compatible con los Modelos de DeepSeek y Google Gemini Flash 2.0 vía API.*
*Obtener API KEY de DeepSeek: [Plataforma DeepSeek](https://platform.deepseek.com/)*  
*Obtener API KEY de Google Gemini: [Google AI Studio](https://aistudio.google.com)*  

![Logo de DeepRoot](src/assets/images/deeproot.png)  
*Ballena de DeepRoot - Símbolo de raíces profundas*  

---
## 📹 Demo  
No te pierdas el video demostrativo de la Instalación de DeepRoot:  
[![Ver Demo](https://img.shields.io/badge/▶-Ver_Video_Demo-red?style=for-the-badge)](https://rutube.ru/video/f59e3cd104a92965b0add83a40c95047/)

### 🎥 ¿Qué verás en el demo?  
- Instalación de DeepRoot  
---

## 📌 Tabla de Contenidos
1. [Filosofía](#-filosofía)
2. [Características](#-características)
3. [Instalación](#-instalación)
4. [Uso Avanzado](#-uso-avanzado)
5. [Contribuir](#-contribuir)
6. [Licencia](#-licencia)

---

## 🌍 Filosofía
### Philosophy / 哲学 / Философия / الفلسفة  

**DeepRoot** nace en Venezuela para democratizar la IA, combinando tecnología avanzada con principios de software libre y justicia social. Inspirado en la resiliencia de comunidades como El Guarataro fundadora del Primer Infocentro Comunitario de Venezuela, busca ser herramienta para la emancipación tecnológica.

### English  
**DeepRoot**, developed in Venezuela, merges cutting-edge AI with free software ideals. It’s a tool for social transformation, inspired by grassroots movements and licensed for collective empowerment.  

### 中文 (Chinese)  
**DeepRoot** 诞生于委内瑞拉，结合自由软件与人工智能，致力于技术民主化。受社区韧性启发，遵循开放共享原则，赋能社会变革。  

### Русский (Russian)  
**DeepRoot** — венесуэльский проект, объединяющий ИИ и свободное ПО для социальных изменений. Лицензия гарантирует свободу использования и модификации.  

### العربية (Arabic)  
**ديبروت** أداة ذكاء اصطناعي حُرّة من فنزويلا، مصممة لتمكين المجتمعات عبر 

---

## 🚀 Características  

### 🔍 Multi-Modelos  
- Soporte para **deepseek-chat**, **deepseek-coder**, **deepseek-reasoner**, **gemini-2.0-flash** (ampliaremos progresivamente la lista de modelos) 
- Configuración dinámica de parámetros (tokens, temperatura)  

### 🎨 Personalización  
- Temas claros/oscuros (`gruvbox`)  
- Sintaxis de código resaltada  

### 📤 Exportación  
- Conversaciones en **Markdown** y **HTML**  
- Compatibilidad con **Obsidian** y **Telegram**  

---

## 📥 Instalación  

### Requisitos  
- **Python 3.8+**  
- **Zenity** (para diálogos gráficos)  
- **Git** (opcional, para instalación manual)  
- **libmpv.so.1** (dependencia de Flet para renderizado multimedia)  

#### 🔧 Solución para `libmpv.so.1` (GNU/Linux)  
En sistemas donde solo está disponible `libmpv.so.2`, ejecuta:  
```bash
sudo ln -s /usr/lib/libmpv.so /usr/lib/libmpv.so.1  # Crea enlace simbólico
```
*Más detalles: [Issue #2823 de Flet](https://github.com/flet-dev/flet/issues/2823)*  

> **Nota:** En futuras actualizaciones, esta dependencia se resolverá automáticamente durante la instalación.

---

### 1. Método Automático  
```bash
curl -sSL https://raw.githubusercontent.com/jonasreyes/deeproot/main/install.sh | bash
```

### 2. Instalación Manual  
```bash
git clone https://github.com/jonasreyes/deeproot.git
cd deeproot
python3 -m venv .venv
source .venv/bin/activate  # Canaima/Zsh: usa `. .venv/bin/activate`
pip install -r requirements.txt
cd src && python generar_lanzador.py && cd ..
```

---

## 🔥 Aliases Disponibles  
Tras la instalación, usa estos comandos en cualquier terminal:  
```bash
deeproot           # Inicia DeepRoot
uninstall-deeproot # Desinstala completamente
```  
*Nota:* Cierra y reabre la terminal o ejecuta:  
```bash
source ~/.zshrc    # Para Canaima/Zsh
source ~/.bashrc   # Para Bash
```

---

## 🖥️ Ejecución  
- **Desde el menú de aplicaciones** (búsca "DeepRoot").  
- **Desde terminal**:  
  ```bash
  deeproot  # Usando el alias
  # O manualmente:
  cd deeproot && .venv/bin/python src/main.py
  ```

---

## 🗑️ Desinstalación  
Ejecuta:  
```bash
uninstall-deeproot  # Usando el alias
# O manualmente:
curl -sSL https://raw.githubusercontent.com/jonasreyes/deeproot/main/uninstall.sh | bash
```

---

## 📦 Soporte para Distros  
| Distribución       | Comandos de Instalación                    | Notas                                  |     |
| ------------------ | ------------------------------------------ | -------------------------------------- | --- |
| **Canaima/Debian** | `sudo apt install python3-venv git zenity` | Ver solución para `libmpv.so.1`        |     |
| **Arch Linux**     | `sudo pacman -S python git zenity`         | Usa `libmpv.so.2` con enlace simbólico |     |
| **Fedora**     | `sudo dnf install python3-virtualenv git zenity`         | Usa `libmpv.so.2` con enlace simbólico |     |

---

## 🐧 Recomendado para Canaima GNU/Linux  
DeepRoot está optimizado para Canaima GNU/Linux (basado en Debian). Descárgalo [aquí](https://canaima.softwarelibre.gob.ve/).  

---

## 🛠 Uso Avanzado
*Opciones disponibles:*
- `--model`: Selecciona entre las versiones más recientes de los modelos de DeepSeek (se irán sumando otros modelos).
- `--max-tokens`: Controla la longitud de respuestas.
- `--temperature`: Ajusta la creatividad (0.0 a 2.0)

---

## 🐛 Reportar Problemas  
¿Encontraste un error? ¡Abre un [issue en GitHub](https://github.com/jonasreyes/deeproot/issues)! 

---

## 🤝 Contribuir
1. Haz fork del repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcion`)
3. Envía un Pull Request
 

---

## 📜 Licencia  
DeepRoot se distribuye bajo la [Licencia DeepRoot](LICENSE), compatible con GPL.  

---

## 🔗 Enlaces Útiles  
- **Canal Oficial**: [@deeproot_app](https://t.me/deeproot_app)  
- **Desarrollador**: [@jonasroot](https://t.me/jonasroot)  
- **Repositorio**: [github.com/jonasreyes/deeproot](https://github.com/jonasreyes/deeproot)  

*¡Gracias por usar DeepRoot!* 🐋💙  

---

*¿Más ayuda? Contacta a [@jonasroot](https://t.me/jonasroot)*

## 🐧 Recomendado para Canaima GNU/Linux

---
