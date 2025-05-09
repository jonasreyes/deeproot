#!/bin/bash
# deeproot_install.sh - Instalador Oficial DeepRoot v0.3.0
set -eo pipefail

# --- Constantes ---
readonly VERSION="0.3.0"
readonly TELEGRAM_DEEPROOT="https://t.me/deeproot_app"
readonly TELEGRAM_CANAIMA="https://t.me/CanaimaGNULinuxOficial"
readonly LOGO_ASCII=$(cat << "EOF"
██████╗ ███████╗███████╗██████╗ ██████╗  ██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝
██║  ██║█████╗  █████╗  ██████╔╝██████╔╝██║   ██║██║   ██║   ██║   
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══██╗██║   ██║██║   ██║   ██║   
██████╔╝███████╗███████╗██║     ██║  ██║╚██████╔╝╚██████╔╝   ██║   
╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   
EOF
)

# --- Configuración inicial ---
DIR_APPS="${HOME}/apps"
DIR_INSTALACION="${DIR_APPS}/deeproot"
DIR_SCRIPTS="${DIR_INSTALACION}/scripts"
DIR_CONFIG="${HOME}/.config/deeproot"
DIR_LOGS="${DIR_CONFIG}/logs"
ARCHIVO_LOG="${DIR_LOGS}/instalacion_$(date +%Y%m%d_%H%M%S).log"

# --- Variables dinámicas ---
DIR_EXPORTACIONES=""

# --- Funciones principales ---
inicializar_directorios() {
    echo -e "📂 \033[1mConfigurando directorios base...\033[0m"
    mkdir -p "${DIR_APPS}" "${DIR_CONFIG}" "${DIR_LOGS}"
}

mostrar_banner() {
    clear
    echo -e "\033[1;34m${LOGO_ASCII}\033[0m"
    echo -e "\033[1mDeepRoot v${VERSION}\033[0m - Instalador"
    echo -e "══════════════════════════════════════════"
}

registrar_log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${ARCHIVO_LOG}"
}

verificar_instalacion_previa() {
    if [[ -d "${DIR_INSTALACION}/.git" ]]; then
        registrar_log "Instalación previa detectada en ${DIR_INSTALACION}"
        echo -e "\n⚠️  \033[1;33mATENCIÓN:\033[0m Ya existe una instalación de DeepRoot."
        
        read -rp "¿Deseas actualizar la instalación existente? [S/n]: " respuesta
        if [[ "${respuesta,,}" =~ ^(n|no)$ ]]; then
            registrar_log "Usuario eligió no actualizar"
            echo -e "\n❌ Operación cancelada por el usuario."
            exit 0
        fi

        if [ "$(ls -A ${DIR_INSTALACION})" ]; then
            echo -e "\n🔍 \033[1mContenido existente en el directorio:\033[0m"
            ls -la "${DIR_INSTALACION}"
            
            read -rp "¿Deseas borrar el contenido existente antes de instalar? [s/N]: " respuesta_borrar
            if [[ "${respuesta_borrar,,}" =~ ^(s|si|y|yes)$ ]]; then
                echo -e "🗑️  \033[1;31mLimpiando directorio...\033[0m"
                rm -rf "${DIR_INSTALACION:?}/"*
                registrar_log "Directorio de instalación limpiado"
            else
                echo -e "❌ \033[1;31mInstalación abortada. Directorio no vacío.\033[0m"
                exit 1
            fi
        fi
        
        registrar_log "Iniciando actualización..."
        actualizar_aplicacion
        exit 0
    fi
}

actualizar_aplicacion() {
    echo -e "\n🔄 \033[1mActualizando DeepRoot...\033[0m"
    (cd "${DIR_INSTALACION}" && git stash push -u -m "Antes de actualizar" && git pull && source .venv/bin/activate && pip install --upgrade pip && pip install -U -r requirements.txt && git stash pop)
    echo -e "✅ \033[1;32mActualización completada\033[0m"
}

detectar_sistema() {
    registrar_log "Detectando sistema operativo..."
    
    # Inicializar variables con valores por defecto
    NAME="Desconocido"
    PRETTY_NAME="Distribución Desconocida"
    ID="desconocido"
    VERSION_ID=""

    # Leer /etc/os-release si existe
    if [[ -f "/etc/os-release" ]]; then
        NAME=$(grep -E '^NAME=' /etc/os-release | cut -d'=' -f2- | tr -d '"')
        PRETTY_NAME=$(grep -E '^PRETTY_NAME=' /etc/os-release | cut -d'=' -f2- | tr -d '"')
        ID=$(grep -E '^ID=' /etc/os-release | cut -d'=' -f2- | tr -d '"')
        VERSION_ID=$(grep -E '^VERSION_ID=' /etc/os-release | cut -d'=' -f2- | tr -d '"')
        
        # Asignar valores por defecto si alguna variable está vacía
        [[ -z "$NAME" ]] && NAME="Desconocido"
        [[ -z "$PRETTY_NAME" ]] && PRETTY_NAME="$NAME"
        [[ -z "$ID" ]] && ID="desconocido"
    fi

    echo -e "\n💻 \033[1mSistema detectado:\033[0m"
    echo -e "  ▸ Distribución: ${PRETTY_NAME}"
    [[ -n "$VERSION_ID" ]] && echo -e "  ▸ Versión: ${VERSION_ID}"
    echo -e "  ▸ Kernel: $(uname -r)"
    
    registrar_log "Sistema: ${PRETTY_NAME}, Versión: ${VERSION_ID}, Kernel: $(uname -r), ID: ${ID}"
}

verificar_libmpv() {
    echo -e "\n🔍 \033[1mVerificando libmpv.so.1...\033[0m"
    registrar_log "Buscando libmpv.so.1"

    local rutas_busqueda=(
        "/usr/lib"
        "/usr/lib64"
        "/usr/lib/x86_64-linux-gnu"
        "/usr/local/lib"
        "/usr/local/lib64"
        "/opt/lib"
        "/opt/lib64"
    )

    local ruta_libmpv=""
    local ruta_libmpv_alternativa=""

    # Buscar en las rutas especificadas
    for ruta in "${rutas_busqueda[@]}"; do
        if [[ -f "${ruta}/libmpv.so.1" ]]; then
            ruta_libmpv="${ruta}/libmpv.so.1"
            break
        elif [[ -f "${ruta}/libmpv.so.2" ]]; then
            ruta_libmpv_alternativa="${ruta}/libmpv.so.2"
        elif [[ -f "${ruta}/libmpv.so" ]]; then
            ruta_libmpv_alternativa="${ruta}/libmpv.so"
        fi
    done

    if [[ -n "${ruta_libmpv}" ]]; then
        echo -e "✅ \033[1;32mVersión correcta encontrada:\033[0m ${ruta_libmpv}"
        registrar_log "libmpv.so.1 encontrado en ${ruta_libmpv}"
        return 0
    elif [[ -n "${ruta_libmpv_alternativa}" ]]; then
        echo -e "⚠️ \033[1;33mSe encontró una versión diferente de libmpv:\033[0m ${ruta_libmpv_alternativa}"
        echo -e "\nPara crear el enlace simbólico necesario, copia y pega la siguiente instrucción:"
        echo -e "\033[1msudo ln -s \"${ruta_libmpv_alternativa}\" \"${ruta_libmpv_alternativa%/*}/libmpv.so.1\"\033[0m"
        echo -e "\nLuego, vuelve a ejecutar el instalador."
        registrar_log "Encontrada versión alternativa de libmpv: ${ruta_libmpv_alternativa}. Instrucción de enlace mostrada."
        return 1
    else
        echo -e "❌ \033[1;31mNo se encontró libmpv.so.1 en el sistema\033[0m"
        registrar_log "No se encontró libmpv.so.1 en el sistema"
        mostrar_ayuda_libmpv
        return 1
    fi
}

mostrar_ayuda_libmpv() {
    echo -e "\n🛠️  \033[1;36mSOLUCIÓN PARA LIBMPV\033[0m"
    
    # Usamos la variable ID ya detectada
    case "${ID}" in
        debian|ubuntu|canaima|linuxmint|pop|neon|mx|zorin)
            echo -e "\n\033[1mPara distribuciones basadas en Debian (${PRETTY_NAME}):\033[0m"
            echo -e "1. Instalar libmpv1:"
            echo -e "   \033[1msudo apt update && sudo apt install libmpv1\033[0m"
            echo -e "\nSi no encuentras libmpv1, puedes intentar con libmpv2:"
            echo -e "   \033[1msudo apt update && sudo apt install libmpv2\033[0m"
            ;;
        arch|manjaro|endeavouros)
            echo -e "\n\033[1mPara Arch Linux/Manjaro (${PRETTY_NAME}):\033[0m"
            echo -e "1. Instalar mpv:"
            echo -e "   \033[1msudo pacman -S mpv\033[0m"
            ;;
        fedora|rhel|centos|almalinux|rocky)
            echo -e "\n\033[1mPara Fedora/RHEL/CentOS (${PRETTY_NAME}):\033[0m"
            echo -e "1. Instalar mpv-libs:"
            echo -e "   \033[1msudo dnf install mpv-libs\033[0m"
            ;;
        opensuse*|sles)
            echo -e "\n\033[1mPara openSUSE/SLES (${PRETTY_NAME}):\033[0m"
            echo -e "1. Instalar libmpv1:"
            echo -e "   \033[1msudo zypper install libmpv1\033[0m"
            ;;
        *)
            echo -e "\n\033[1mPara ${PRETTY_NAME} (${ID}):\033[0m"
            echo -e "1. Buscar el paquete equivalente a libmpv1 en tu distribución"
            echo -e "   Ejemplo para buscar: \033[1msudo apt search libmpv || sudo dnf search mpv\033[0m"
            ;;
    esac

    echo -e "\n\033[1mSi ya tienes instalada una versión diferente de libmpv (ej: libmpv.so.2 o libmpv.so), puedes crear un enlace simbólico:\033[0m"
    echo -e "\n1. Primero, identifica la ruta completa de la librería instalada. Por ejemplo:"
    echo -e "   \033[1mls -l /usr/lib/x86_64-linux-gnu/libmpv.so.2\033[0m"
    echo -e "\n2. Luego, crea el enlace simbólico (reemplaza la ruta con la correcta):"
    echo -e "   \033[1msudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1\033[0m"
    echo -e "\n\033[1mNotas importantes:\033[0m"
    echo -e "• Después de instalar o crear el enlace, verifica con: \033[1mldconfig -p | grep libmpv\033[0m"
    echo -e "• El enlace simbólico es una solución temporal - puede causar problemas"
    echo -e "• Para la mejor experiencia, instala el paquete nativo de tu distribución"
    
    registrar_log "Mostrada ayuda para libmpv.so.1 en ${ID}"
}

verificar_ollama() {
    if command -v ollama >/dev/null; then
        local modelos=$(ollama list 2>/dev/null || echo "Ninguno")
        echo -e "\n🤖 \033[1mOllama detectado\033[0m"
        echo -e "  ▸ Modelos instalados: ${modelos}"
        registrar_log "Ollama instalado. Modelos: ${modelos}"
    else
        registrar_log "Ollama no está instalado"
    fi
}

configurar_entorno_python() {
    registrar_log "Configurando entorno Python..."
    echo -e "\n🐍 \033[1mCreando entorno virtual en .venv...\033[0m"
    if ! python3 -m venv "${DIR_INSTALACION}/.venv"; then
        echo -e "\n❌ \033[1;31mError al crear el entorno virtual. Intenta instalar python3-venv.\033[0m"
        exit 1
    fi
    source "${DIR_INSTALACION}/.venv/bin/activate"
    
    echo -e "\n🔄 \033[1mActualizando pip...\033[0m"
    pip install --upgrade pip
    registrar_log "Pip actualizado a versión: $(pip --version | cut -d' ' -f2)"
    
    echo -e "\n📦 \033[1mInstalando dependencias...\033[0m"
    pip install 'flet[desktop-light]==0.27.6' openai asyncio markdown python-dotenv || {
        echo -e "\n❌ \033[1;31mError al instalar dependencias. Revisa el archivo de registro para más detalles.\033[0m"
        exit 1
    }
    registrar_log "Dependencias instaladas (flet-desktop-light forzado)"
    
    registrar_log "Rutas de búsqueda usadas para libmpv: $(ldconfig -p | grep libmpv)"
    echo -e "\n💡 \033[1mCONSEJO:\033[0m Puedes configurar rutas adicionales con:"
    echo -e "  \033[1mexport LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/tu/ruta1:/tu/ruta2\033[0m"
    echo -e "  antes de ejecutar el instalador"
}

crear_directorio_exportaciones() {
    echo -e "\n📂 \033[1mConfigurando directorio de exportaciones...\033[0m"
    
    if [ -d "${HOME}/Descargas" ]; then
        DIR_EXPORTACIONES="${HOME}/Descargas/deeproot_exportaciones"
    elif [ -d "${HOME}/Downloads" ]; then
        DIR_EXPORTACIONES="${HOME}/Downloads/deeproot_exportaciones"
    else
        read -p "¿Dónde quieres que se creen las exportaciones? (ruta completa): " DIR_EXPORTACIONES
        if [[ -z "${DIR_EXPORTACIONES}" ]]; then
            DIR_EXPORTACIONES="${HOME}/deeproot_exportaciones"
        fi
    fi

    mkdir -p "${DIR_EXPORTACIONES}"
    chmod 755 "${DIR_EXPORTACIONES}"
    
    echo -e "  ▸ Ruta: \033[1;34m${DIR_EXPORTACIONES}\033[0m"
    registrar_log "Directorio de exportaciones creado en ${DIR_EXPORTACIONES}"
}

instalar_comandos() {
    registrar_log "Configurando comandos..."
    
    cat > "${DIR_INSTALACION}/.deeproot_env" << EOF
# Configuración DeepRoot
export DEEP_ROOT_INSTALL_DIR="${DIR_INSTALACION}"
export DEEP_ROOT_CONFIG_DIR="${DIR_CONFIG}"
export DEEP_ROOT_EXPORT_DIR="${DIR_EXPORTACIONES}"
EOF

    # Eliminar aliases existentes y luego crear los nuevos
    for shell_file in ".bashrc" ".zshrc"; do
        if [[ -f "${HOME}/${shell_file}" ]]; then
            sed -i '/# ===== DeepRoot Config =====/,/# ===== Fin DeepRoot =====/d' "${HOME}/${shell_file}"
            
            cat >> "${HOME}/${shell_file}" << EOF

# ===== DeepRoot Config =====
if [ -f "${DIR_INSTALACION}/.deeproot_env" ]; then
    source "${DIR_INSTALACION}/.deeproot_env"
fi

alias deeproot='(cd "\${DEEP_ROOT_INSTALL_DIR}" && nohup ./.venv/bin/python src/main.py >/dev/null 2>&1 &)'
alias deeproot-update='(cd "\${DEEP_ROOT_INSTALL_DIR}" && git pull && ./.venv/bin/pip install --upgrade pip && ./.venv/bin/pip install -U -r requirements.txt)'
alias deeproot-uninstall='"\${DEEP_ROOT_INSTALL_DIR}/scripts/deeproot_uninstall.sh"'
alias deeproot-logs='ls -lh "\${DEEP_ROOT_CONFIG_DIR}/logs"'
alias deeproot-exports='cd "\${DEEP_ROOT_EXPORT_DIR}" && ls -lh'
# ===== Fin DeepRoot =====
EOF
            registrar_log "Comandos configurados en ${HOME}/${shell_file}"
        fi
    done
}

copiar_scripts() {
    registrar_log "Configurando script de desinstalación..."
    mkdir -p "${DIR_SCRIPTS}"
    
    # Verificar si curl está instalado
    if ! command -v curl &> /dev/null; then
        echo -e "\n❌ \033[1;31mError: curl no está instalado. Instálalo para descargar el script de desinstalación.\033[0m"
        exit 1
    fi

    # Siempre descargar la versión más reciente desde GitHub
    curl -sSL https://raw.githubusercontent.com/jonasreyes/deeproot/main/scripts/deeproot_uninstall.sh \
         -o "${DIR_SCRIPTS}/deeproot_uninstall.sh"
    chmod +x "${DIR_SCRIPTS}/deeproot_uninstall.sh"
}

generar_lanzador() {
    if [[ -f "${DIR_INSTALACION}/src/generar_lanzador.py" ]]; then
        registrar_log "Generando lanzador gráfico..."
        (cd "${DIR_INSTALACION}/src" && python generar_lanzador.py)
    fi
}

mostrar_resumen() {
    echo -e "\n══════════════════════════════════════════"
    echo -e "✅ \033[1;32mINSTALACIÓN COMPLETADA\033[0m ✅"
    echo -e "══════════════════════════════════════════"
    
    echo -e "\n\033[1m⚠️  AVISO IMPORTANTE:\033[0m"
    echo -e "  ▸ Esta versión usa \033[1mflet-desktop-light\033[0m (sin soporte multimedia)"
    echo -e "  ▸ \033[1;31mVersiones futuras requerirán libmpv.so.1\033[0m"
    echo -e "  ▸ Solución recomendada:"
    echo -e "    - Instalar Canaima GNU/Linux (incluye libmpv.so.1)"
    echo -e "    - O instalar manualmente la librería"
    
    echo -e "\n\033[1m📂 Estructura de directorios:\033[0m"
    echo -e "  ▸ \033[34m${DIR_INSTALACION}\033[0m (instalación)"
    echo -e "  ▸ \033[34m${DIR_EXPORTACIONES}\033[0m (exportaciones)"
    echo -e "  ▸ \033[34m${DIR_CONFIG}\033[0m (configuración)"
    
    echo -e "\n\033[1m🐍 Entorno Python:\033[0m"
    echo -e "  ▸ Ruta: \033[34m${DIR_INSTALACION}/.venv\033[0m"
    echo -e "  ▸ Versión pip: \033[34m$(pip --version | cut -d' ' -f2)\033[0m"
    
    echo -e "\n\033[1m🚀 Comandos disponibles:\033[0m"
    echo -e "  ▸ \033[1mdeeproot\033[0m       - Inicia la aplicación"
    echo -e "  ▸ \033[1mdeeproot-update\033[0m - Actualiza DeepRoot"
    echo -e "  ▸ \033[1mdeeproot-uninstall\033[0m - Desinstala DeepRoot"
    echo -e "  ▸ \033[1mdeeproot-logs\033[0m  - Muestra los registros"
    echo -e "  ▸ \033[1mdeeproot-exports\033[0m - Accede a exportaciones"
    
    echo -e "\n\033[1m🔧 Recomendaciones:\033[0m"
    echo -e "  ▸ Ejecuta \033[1msource ~/.bashrc\033[0m o reinicia la terminal"
    echo -e "  ▸ Para funcionalidad multimedia completa:"
    case "${ID}" in
        canaima|ubuntu|debian|Desconocido) echo "    sudo apt install libmpv1";;
        arch) echo "    sudo pacman -S mpv";;
        fedora) echo "    sudo dnf install mpv-libs";;
        *) echo "    Consulta la documentación de tu distribución";;
    esac
    
    echo -e "\n\033[1m📢 Canales oficiales:\033[0m"
    echo -e "  ▸ DeepRoot: ${TELEGRAM_DEEPROOT}"
    echo -e "  ▸ Canaima GNU/Linux: ${TELEGRAM_CANAIMA}"
    
    registrar_log "Instalación completada exitosamente"
}

verificar_dependencias_iniciales() {
    echo -e "\n🔍 \033[1mVerificando dependencias iniciales...\033[0m"

    # Verificar si git está instalado
    if ! command -v git &> /dev/null; then
        echo -e "❌ \033[1;31mError: git no está instalado. Instálalo para continuar.\033[0m"
        case "${ID}" in
            debian|ubuntu|canaima) echo -e "  \033[1msudo apt install git\033[0m";;
            arch|manjaro) echo -e "  \033[1msudo pacman -S git\033[0m";;
            fedora|rhel|centos) echo -e "  \033[1msudo dnf install git\033[0m";;
            opensuse*) echo -e "  \033[1msudo zypper install git\033[0m";;
            *) echo -e "  Instala git usando el gestor de paquetes de tu distribución.";;
        esac
        exit 1
    fi

    # Verificar si curl está instalado
    if ! command -v curl &> /dev/null; then
        echo -e "❌ \033[1;31mError: curl no está instalado. Instálalo para continuar.\033[0m"
        case "${ID}" in
            debian|ubuntu|canaima) echo -e "  \033[1msudo apt install curl\033[0m";;
            arch|manjaro) echo -e "  \033[1msudo pacman -S curl\033[0m";;
            fedora|rhel|centos) echo -e "  \033[1msudo dnf install curl\033[0m";;
            opensuse*) echo -e "  \033[1msudo zypper install curl\033[0m";;
            *) echo -e "  Instala curl usando el gestor de paquetes de tu distribución.";;
        esac
        exit 1
    fi

    # Verificar si python3 está instalado
    if ! command -v python3 &> /dev/null; then
        echo -e "❌ \033[1;31mError: python3 no está instalado. Instálalo para continuar.\033[0m"
        case "${ID}" in
            debian|ubuntu|canaima) echo -e "  \033[1msudo apt install python3 python3-venv\033[0m";;
            arch|manjaro) echo -e "  \033[1msudo pacman -S python\033[0m";;
            fedora|rhel|centos) echo -e "  \033[1msudo dnf install python3\033[0m";;
            opensuse*) echo -e "  \033[1msudo zypper install python3\033[0m";;
            *) echo -e "  Instala python3 usando el gestor de paquetes de tu distribución.";;
        esac
        exit 1
    fi
}

# --- Flujo principal ---
main() {
    mostrar_banner
    inicializar_directorios
    verificar_instalacion_previa
    detectar_sistema
    verificar_dependencias_iniciales

    # Bucle para verificar libmpv hasta que se encuentre o el usuario cancele
    while true; do
        if verificar_libmpv; then
            break
        else
            read -p "¿Intentar de nuevo la verificación de libmpv? [s/N]: " respuesta
            if [[ "${respuesta,,}" =~ ^(n|no)$ ]]; then
                echo -e "\n\033[1;33mADVERTENCIA: DeepRoot podría no funcionar correctamente sin libmpv.so.1\033[0m"
                echo -e "Continuando sin verificar libmpv."
                break
            fi
        fi
    done

    verificar_ollama
    
    echo -e "\n📥 \033[1mInstalando DeepRoot en:\033[0m \033[1;34m${DIR_INSTALACION}\033[0m"
    registrar_log "Iniciando instalación en ${DIR_INSTALACION}"
    
    git clone https://github.com/jonasreyes/deeproot.git "${DIR_INSTALACION}" || {
        echo -e "❌ \033[1;31mError al clonar el repositorio\033[0m"
        exit 1
    }

    if [ ! -d "${DIR_INSTALACION}/.git" ]; then
        echo -e "❌ \033[1;31mError: El repositorio no se clonó correctamente\033[0m"
        exit 1
    fi
    
    mkdir -p "${DIR_SCRIPTS}"
    
    configurar_entorno_python
    crear_directorio_exportaciones
    instalar_comandos
    copiar_scripts
    generar_lanzador
    
    mostrar_resumen
}

main "$@"
