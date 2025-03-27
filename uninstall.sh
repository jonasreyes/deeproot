#!/bin/bash
# Desinstalador completo de DeepRoot - Elimina todos los rastros

echo "🧹 Iniciando desinstalación completa de DeepRoot..."

# 1. Eliminar archivos de configuración
CONFIG_DIR="$HOME/.config/deeproot"
if [ -d "$CONFIG_DIR" ]; then
    echo "✔ Eliminando directorio de configuración..."
    rm -rf "$CONFIG_DIR"
fi

# 2. Eliminar lanzador del menú
DESKTOP_FILE="$HOME/.local/share/applications/deeproot.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    echo "✔ Eliminando lanzador del menú..."
    rm -f "$DESKTOP_FILE"
fi

# 3. Eliminar entorno virtual (si existe en la ruta de instalación)
INSTALL_DIR=$(dirname "$(realpath "$0")")
VENV_DIR="$INSTALL_DIR/.venv"
if [ -d "$VENV_DIR" ]; then
    echo "✔ Eliminando entorno virtual..."
    rm -rf "$VENV_DIR"
fi

# 4. Eliminar aliases de los shells
remove_aliases() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        if grep -q "alias deeproot=" "$HOME/${shell_rc}"; then
            sed -i '/# DeepRoot Aliases/,/uninstall-deeproot/d' "$HOME/${shell_rc}"
            echo "✔ Aliases removidos de ${shell_rc}"
        fi
    fi
}

remove_aliases ".bashrc"
remove_aliases ".zshrc"

# 5. Opcional: Eliminar directorio de instalación (¡ADVERTENCIA!)
echo "⚠ ¿Deseas eliminar el directorio de instalación completo? [y/N]"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "✔ Eliminando $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
fi

echo "✅ ¡DeepRoot ha sido desinstalado completamente!"
echo "Gracias por haber usado esta herramienta. Hasta pronto."
