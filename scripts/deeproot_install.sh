#!/bin/bash
# deeproot_install.sh - Instalador Oficial DeepRoot v0.2.0
set -eo pipefail

# --- Constantes ---
readonly VERSION="0.1.0"
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
    (cd "${DIR_INSTALACION}" && git pull && source .venv/bin/activate && pip install --upgrade pip && pip install -U -r requirements.txt)
    echo -e "✅ \033[1;32mActualización completada\033[0m"
}

detectar_sistema() {
    registrar_log "Detectando sistema operativo..."
    if [[ -f "/etc/os-release" ]]; then
        source "/etc/os-release"
        echo -e "\n💻 \033[1mSistema detectado:\033[0m"
        echo -e "  ▸ Distribución: ${PRETTY_NAME:-$ID}"
        echo -e "  ▸ Kernel: $(uname -r)"
        registrar_log "Sistema: ${PRETTY_NAME:-$ID}, Kernel: $(uname -r)"
    else
        echo -e "\n⚠️  \033[1;33mADVERTENCIA:\033[0m No se pudo detectar la distribución exacta"
        registrar_log "No se pudo detectar la distribución"
    fi
}

verificar_libmpv() {
    registrar_log "Buscando libmpv.so.1..."
    local ruta_libmpv=$(find /usr/lib* /usr/local/lib -name "libmpv.so.1" 2>/dev/null | head -n1)
    
    if [[ -n "${ruta_libmpv}" ]]; then
        echo -e "\n✅ \033[1;32mlibmpv.so.1 encontrado:\033[0m ${ruta_libmpv}"
        registrar_log "libmpv.so.1 encontrado en ${ruta_libmpv}"
        return 0
    else
        echo -e "\n⚠️  \033[1;33mADVERTENCIA:\033[0m libmpv.so.1 no encontrado"
        echo "  ▸ Se instalará la versión ligera (flet-desktop-light)"
        registrar_log "libmpv.so.1 no encontrado, usando versión ligera"
        return 1
    fi
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
    python3 -m venv "${DIR_INSTALACION}/.venv"
    source "${DIR_INSTALACION}/.venv/bin/activate"
    
    echo -e "\n🔄 \033[1mActualizando pip...\033[0m"
    pip install --upgrade pip
    registrar_log "Pip actualizado a versión: $(pip --version | cut -d' ' -f2)"
    
    if verificar_libmpv; then
        echo -e "\n📦 \033[1mInstalando dependencias completas...\033[0m"
        pip install flet-desktop openai asyncio markdown python-dotenv
    else
        echo -e "\n📦 \033[1mInstalando dependencias ligeras...\033[0m"
        pip install flet-desktop-light openai asyncio markdown python-dotenv
    fi
    
    registrar_log "Entorno Python configurado correctamente"
}

crear_directorio_exportaciones() {
    echo -e "\n📂 \033[1mConfigurando directorio de exportaciones...\033[0m"
    
    if [ -d "${HOME}/Descargas" ]; then
        DIR_EXPORTACIONES="${HOME}/Descargas/deeproot_exportaciones"
    elif [ -d "${HOME}/Downloads" ]; then
        DIR_EXPORTACIONES="${HOME}/Downloads/deeproot_exportaciones"
    else
        DIR_EXPORTACIONES="${HOME}/deeproot_exportaciones"
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
    registrar_log "Copiando scripts auxiliares..."
    mkdir -p "${DIR_SCRIPTS}"
    cp "$(dirname "$0")/deeproot_uninstall.sh" "${DIR_SCRIPTS}/"
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
        ubuntu|debian) echo "    sudo apt install libmpv1";;
        arch) echo "    sudo pacman -S mpv";;
        fedora) echo "    sudo dnf install mpv-libs";;
        *) echo "    Consulta la documentación de tu distribución";;
    esac
    
    echo -e "\n\033[1m📢 Canales oficiales:\033[0m"
    echo -e "  ▸ DeepRoot: ${TELEGRAM_DEEPROOT}"
    echo -e "  ▸ Canaima GNU/Linux: ${TELEGRAM_CANAIMA}"
    
    registrar_log "Instalación completada exitosamente"
}

# --- Flujo principal ---
main() {
    mostrar_banner
    inicializar_directorios
    verificar_instalacion_previa
    detectar_sistema
    verificar_libmpv
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
