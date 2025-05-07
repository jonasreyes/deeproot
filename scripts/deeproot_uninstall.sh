#!/bin/bash
# deeproot_uninstall.sh - Desinstalador Seguro de DeepRoot v0.2.0
set -eo pipefail

# --- Constantes ---
readonly LOGO_ASCII=$(cat << "EOF"
██████╗ ███████╗███████╗██████╗ ██████╗  ██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝
██║  ██║█████╗  █████╗  ██████╔╝██████╔╝██║   ██║██║   ██║   ██║   
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══██╗██║   ██║██║   ██║   ██║   
██████╔╝███████╗███████╗██║     ██║  ██║╚██████╔╝╚██████╔╝   ██║   
╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   
EOF
)

# --- Configuración Segura ---
DIR_INSTALACION_DEFAULT="${HOME}/apps/deeproot"
DIR_CONFIG="${HOME}/.config/deeproot"
ALIAS_FILES=("${HOME}/.bashrc" "${HOME}/.zshrc")

# --- Funciones ---
mostrar_banner() {
    clear
    echo -e "\033[1;34m${LOGO_ASCII}\033[0m"
    echo -e "\033[1mDESINSTALADOR DEEPROOT\033[0m"
    echo -e "══════════════════════════════════════════"
}

detectar_directorio_instalacion() {
    # 1. Intentar detectar desde variables de entorno en shell files
    for shell_file in "${ALIAS_FILES[@]}"; do
        if [[ -f "${shell_file}" ]]; then
            local dir_detectado=$(grep -oP 'DEEP_ROOT_INSTALL_DIR="\K[^"]+' "${shell_file}" | head -n1)
            if [[ -n "${dir_detectado}" && -d "${dir_detectado}" ]]; then
                echo "${dir_detectado}"
                return 0
            fi
        fi
    done

    # 2. Verificar ubicación default
    if [[ -d "${DIR_INSTALACION_DEFAULT}" ]]; then
        echo "${DIR_INSTALACION_DEFAULT}"
        return 0
    fi

    # 3. Pedir al usuario si no se detecta
    echo -e "\n🔍 \033[1;33mNo se pudo detectar la ubicación de instalación\033[0m"
    read -rp "Ingresa la ruta completa de instalación: " dir_manual
    echo "${dir_manual}"
}

validar_directorio() {
    local dir="$1"
    [[ -d "${dir}" ]] && 
    [[ "${dir}" == *"deeproot"* ]] && 
    [[ "${dir}" != "/" ]] && 
    [[ "${dir}" != "${HOME}" ]]
}

pregunta_confirmacion() {
    local mensaje=$1
    echo -e "\n❓ \033[1m${mensaje}\033[0m [s/N]"
    read -r respuesta
    [[ "${respuesta,,}" =~ ^(s|si|y|yes)$ ]]
}

eliminar_seguro() {
    local objetivo=$1
    local tipo=$2  # 'dir' o 'file'
    
    if [[ "${tipo}" == "dir" && -d "${objetivo}" ]]; then
        echo -e "\n📂 \033[1mContenido del directorio a eliminar:\033[0m"
        
        # Verificar si 'tree' está instalado
        if command -v tree &> /dev/null; then
            tree -L 2 "${objetivo}"
        else
            echo -e "\033[1;33m'tree' no está instalado. Mostrando lista de archivos:\033[0m"
            find "${objetivo}" -maxdepth 2 -print
        fi
        
        if pregunta_confirmacion "¿Eliminar TODOS los contenidos anteriores?"; then
            echo -e "🗑️  \033[1;31mEliminando...\033[0m"
            rm -rfv "${objetivo}"
        else
            echo -e "🔹 \033[1;33mConservado por decisión del usuario\033[0m"
        fi
    
    elif [[ "${tipo}" == "file" && -f "${objetivo}" ]]; then
        echo -e "\n📄 \033[1mArchivo a eliminar:\033[0m ${objetivo}"
        if pregunta_confirmacion "¿Confirmas eliminación?"; then
            rm -v "${objetivo}"
        fi
    fi
}

limpiar_aliases() {
    echo -e "\n🔧 \033[1mLimpieza de comandos rápidos...\033[0m"
    for alias_file in "${ALIAS_FILES[@]}"; do
        if [[ -f "${alias_file}" ]]; then
            # Eliminar bloque completo de aliases
            sed -i '/# ===== DeepRoot Config =====/,/# ===== Fin DeepRoot =====/d' "${alias_file}"
            # Eliminar variable de entorno si existe
            sed -i '/export DEEP_ROOT_INSTALL_DIR=/d' "${alias_file}" "${alias_file}"
            sed -i '/export DEEP_ROOT_CONFIG_DIR=/d' "${alias_file}"
            sed -i '/export DEEP_ROOT_EXPORT_DIR=/d' "${alias_file}"
            # Eliminar aliases individuales (por si acaso)
            sed -i '/alias deeproot=/d' "${alias_file}"
            sed -i '/alias deeproot-update=/d' "${alias_file}"
            sed -i '/alias deeproot-uninstall=/d' "${alias_file}"
            sed -i '/alias deeproot-logs=/d' "${alias_file}"
            sed -i '/alias deeproot-exports=/d' "${alias_file}"
            echo -e "✔ \033[1;32mLimpieza completada en:\033[0m ${alias_file}"
        fi
    done
}

# --- Proceso Principal ---
mostrar_banner

# Detección segura del directorio
DIR_INSTALACION=$(detectar_directorio_instalacion)

if ! validar_directorio "${DIR_INSTALACION}"; then
    echo -e "\n❌ \033[1;31mError: Ruta de instalación no válida o insegura\033[0m"
    echo -e "  ▸ Ruta proporcionada: ${DIR_INSTALACION}"
    echo -e "  ▸ La ruta debe contener 'deeproot' y no ser raíz o home"
    exit 1
fi

echo -e "\n⚠️  \033[1;33mADVERTENCIA:\033[0m Se desinstalará DeepRoot de:"
echo -e "  ▸ \033[1;34m${DIR_INSTALACION}\033[0m"

if ! pregunta_confirmacion "¿Deseas continuar con la desinstalación?"; then
    echo -e "\n❌ \033[1;31mDesinstalación cancelada\033[0m"
    exit 0
fi

# 1. Eliminar instalación principal
eliminar_seguro "${DIR_INSTALACION}" "dir"

# 2. Eliminar configuración y logs (opcional)
if [[ -d "${DIR_CONFIG}" ]]; then
    echo -e "\n🔐 \033[1mConfiguración y logs:\033[0m ${DIR_CONFIG}"
    if pregunta_confirmacion "¿Deseas eliminar TODA la configuración y logs?"; then
        eliminar_seguro "${DIR_CONFIG}" "dir"
    fi
fi

# 3. Limpiar aliases y variables
limpiar_aliases

# 4. Eliminar lanzador gráfico si existe
eliminar_seguro "${HOME}/.local/share/applications/deeproot.desktop" "file"

echo -e "\n══════════════════════════════════════════"
echo -e "✅ \033[1;32mDESINSTALACIÓN COMPLETADA\033[0m ✅"
echo -e "══════════════════════════════════════════"
echo -e "\n\033[1mRecomendaciones:\033[0m"
echo -e "▸ Ejecuta \033[1msource ~/.bashrc\033[0m o reinicia la terminal"
echo -e "▸ Para reinstalar: \033[1;34mhttps://github.com/jonasreyes/deeproot\033[0m"
