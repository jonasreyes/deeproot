#!/bin/bash
# Desinstalador seguro de DeepRoot - Elimina solo lo necesario
set -e

echo "🧹 Iniciando desinstalación de DeepRoot..."

# Función para limpiar archivos de configuración del shell (elimina líneas vacías redundantes)
clean_shell_config() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        echo "✔ Limpiando ${shell_rc}..."
        
        # Eliminar bloque de configuración y línea vacía anterior si existe
        sed -i '/^$/ {N; /# Configuración para DeepRoot/ d}' "$HOME/${shell_rc}"  # Elimina línea vacía + bloque
        sed -i '/export DEEP_ROOT_INSTALL_DIR=/d' "$HOME/${shell_rc}"
        sed -i '/alias deeproot=/d' "$HOME/${shell_rc}"
        sed -i '/alias uninstall-deeproot=/d' "$HOME/${shell_rc}"
    fi
}

# 1. Obtener ruta de instalación segura (solo si es un directorio deeproot válido)
get_install_dir() {
    if [ -n "$DEEP_ROOT_INSTALL_DIR" ]; then
        if [[ "$DEEP_ROOT_INSTALL_DIR" == *"/deeproot" ]]; then
            echo "$DEEP_ROOT_INSTALL_DIR"
        else
            echo "❌ Error: La variable DEEP_ROOT_INSTALL_DIR no apunta a un directorio deeproot válido." >&2
            exit 1
        fi
    else
        # Buscar desde el directorio actual o el script
        local candidate_dir=$(cd "$(dirname "$0")" && pwd)
        if [[ "$candidate_dir" == *"/deeproot" ]]; then
            echo "$candidate_dir"
        else
            echo "❌ Error: No se encontró un directorio deeproot válido." >&2
            exit 1
        fi
    fi
}

INSTALL_DIR=$(get_install_dir)

# 2. Limpiar configuraciones del shell
clean_shell_config ".bashrc"
clean_shell_config ".zshrc"
clean_shell_config ".profile"

# 3. Eliminar archivos de configuración
CONFIG_DIR="$HOME/.config/deeproot"
if [ -d "$CONFIG_DIR" ]; then
    echo "✔ Eliminando configuración en $CONFIG_DIR..."
    rm -rf "$CONFIG_DIR"
fi

# 4. Eliminar lanzador del menú
DESKTOP_FILE="$HOME/.local/share/applications/deeproot.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    echo "✔ Eliminando lanzador del menú..."
    rm -f "$DESKTOP_FILE"
    command -v update-desktop-database >/dev/null && update-desktop-database "$HOME/.local/share/applications"
fi

# 5. Eliminar entorno virtual (solo si está dentro de INSTALL_DIR)
VENV_DIR="$INSTALL_DIR/.venv"
if [ -d "$VENV_DIR" ]; then
    echo "✔ Eliminando entorno virtual..."
    rm -rf "$VENV_DIR"
fi

# 6. Eliminar directorio de instalación (con confirmación y validación EXTRA)
if [ -d "$INSTALL_DIR" ]; then
    echo ""
    echo "⚠ ¿Eliminar el directorio de instalación ($INSTALL_DIR)? [y/N]"
    read -r response
    if [[ "$response" =~ ^[yY] ]]; then
        # Verificación FINAL: ¿El directorio contiene "deeproot" en su ruta?
        if [[ "$INSTALL_DIR" == *"/deeproot" ]]; then
            echo "✔ Eliminando $INSTALL_DIR..."
            cd "$(dirname "$INSTALL_DIR")" && rm -rf "$INSTALL_DIR"
        else
            echo "❌ ABORTADO: La ruta no contiene 'deeproot'." >&2
            exit 1
        fi
    fi
fi

# 7. Limpiar variable de entorno
unset DEEP_ROOT_INSTALL_DIR

echo ""
echo "✅ ¡DeepRoot desinstalado correctamente!"
echo "ℹ Cierra y reabre tus terminales para aplicar los cambios."
