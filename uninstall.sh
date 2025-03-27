#!/bin/bash
# Desinstalador completo de DeepRoot - Elimina todos los rastros
set -e

echo "🧹 Iniciando desinstalación completa de DeepRoot..."

# Función para limpiar archivos de configuración del shell
clean_shell_config() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        echo "✔ Limpiando ${shell_rc}..."
        
        # Eliminar configuración de DeepRoot
        sed -i '/# DeepRoot Configuration/,/alias uninstall-deeproot/d' "$HOME/${shell_rc}"
        sed -i '/export DEEP_ROOT_INSTALL_DIR=/d' "$HOME/${shell_rc}"
        sed -i '/alias deeproot=/d' "$HOME/${shell_rc}"
        sed -i '/alias uninstall-deeproot=/d' "$HOME/${shell_rc}"
    fi
}

# 1. Eliminar variable de entorno y aliases
clean_shell_config ".bashrc"
clean_shell_config ".zshrc"
clean_shell_config ".profile"
clean_shell_config ".bash_profile"

# 2. Eliminar archivos de configuración
CONFIG_DIR="$HOME/.config/deeproot"
if [ -d "$CONFIG_DIR" ]; then
    echo "✔ Eliminando directorio de configuración..."
    rm -rf "$CONFIG_DIR"
fi

# 3. Eliminar lanzador del menú
DESKTOP_FILE="$HOME/.local/share/applications/deeproot.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    echo "✔ Eliminando lanzador del menú..."
    rm -f "$DESKTOP_FILE"
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database "$HOME/.local/share/applications"
    fi
fi

# 4. Eliminar entorno virtual
if [ -n "$DEEP_ROOT_INSTALL_DIR" ]; then
    INSTALL_DIR="$DEEP_ROOT_INSTALL_DIR"
else
    INSTALL_DIR=$(cd "$(dirname "$0")" && pwd)
fi

VENV_DIR="$INSTALL_DIR/.venv"
if [ -d "$VENV_DIR" ]; then
    echo "✔ Eliminando entorno virtual..."
    rm -rf "$VENV_DIR"
fi

# 5. Eliminar directorio de instalación (con confirmación)
if [ -d "$INSTALL_DIR" ]; then
    echo ""
    echo "⚠ ¿Deseas eliminar por completo el directorio de instalación ($INSTALL_DIR)? [y/N]"
    read -r response
    if [[ "$response" =~ ^[yY] ]]; then
        echo "✔ Eliminando $INSTALL_DIR..."
        cd ..
        rm -rf "$INSTALL_DIR"
    fi
fi

# 6. Eliminar variable de entorno de la sesión actual
unset DEEP_ROOT_INSTALL_DIR

echo ""
echo "✅ ¡DeepRoot ha sido completamente desinstalado!"
echo "ℹ Por favor, cierra y reabre todas tus terminales para completar la limpieza."
