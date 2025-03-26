DeepRoot es software libre bajo los términos de la [Licencia de Software Libre de DeepRoot](LICENSE).  
Puedes usar, copiar, modificar y distribuir este software, siempre que cumplas con los términos de la licencia.  
Para más detalles, consulta el archivo [LICENSE](LICENSE) en este repositorio.



```markdown
# 🌊 DeepRoot - Cliente API para DeepSeek  

*Cliente Modelos Avanzados IA (LLM) Licenciados en Software Libre y/o Código Abierto.*  
*Actualmente compatible con los Modelos de DeepSeek vía API [Plataforma DeepSeek API](https://platform.deepseek.com/)*  

![DeepRoot Logo](https://raw.githubusercontent.com/jonasreyes/deeproot/main/src/assets/images/deeproot.png)  
*Logo oficial de DeepRoot*  

## 🚀 Características  
- ✅ Interfaz intuitiva para modelos DeepSeek (Chat, Coder, Reasoner).  
- 🔄 Configuración personalizable (API Key, modelos, temas).  
- 📂 Exporta conversaciones en Markdown/HTML.  
- 🐧 Compatible con Canaima GNU/Linux, Debian, Arch y más.  

---

## 📥 Instalación  

### 🔧 Requisitos  
- **Python 3.8+**  
- **Git** (opcional)  
- **pip** actualizado  

### 🛠️ Métodos de Instalación  

#### 1. Instalación Automática (Recomendada)  
Ejecuta en tu terminal:  
```bash
curl -sSL https://raw.githubusercontent.com/jonasreyes/deeproot/main/install.sh | bash
```

#### 2. Instalación Manual  
```bash
git clone https://github.com/jonasreyes/deeproot.git
cd deeproot
python3 -m venv .venv
source .venv/bin/activate  # Canaima/Zsh: usa `. .venv/bin/activate`
pip install -r requirements.txt  # Instala dependencias
cd src && python install.py && cd ..  # Genera lanzador
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
| Distribución       | Comandos de Instalación       |  
|--------------------|-------------------------------|  
| **Canaima/Debian** | `sudo apt install python3-venv git` |  
| **Arch Linux**     | `sudo pacman -S python git`   |  
| **Fedora**         | `sudo dnf install python3-virtualenv git` |  

---

## 🐛 Reportar Problemas  
¿Encontraste un error? ¡Abre un [issue en GitHub](https://github.com/jonasreyes/deeproot/issues)!  

---

## 📜 Licencia  
DeepRoot se distribuye bajo la [Licencia DeepRoot](LICENSE.md), compatible con GPL.  

---

## 🔗 Enlaces Útiles  
- **Canal Oficial**: [@deeproot_app](https://t.me/deeproot_app)  
- **Desarrollador**: [@jonasroot](https://t.me/jonasroot)  
- **Repositorio**: [github.com/jonasreyes/deeproot](https://github.com/jonasreyes/deeproot)  

*¡Gracias por usar DeepRoot!* 🐋💙  
```

---

### 🔍 Notas Clave  
1. **Imagen del Logo**: Asegúrate de que la ruta `src/assets/images/deeproot.png` exista en tu repositorio.  
2. **Requisitos**: El archivo `requirements.txt` debe incluir:  
   ```plaintext
   flet==0.27
   openai
   markdown
   asyncio
   ```  
3. **Aliases**: Se añaden automáticamente durante la instalación (ver scripts anteriores).  

¿Necesitas ajustar algo más? 😊

