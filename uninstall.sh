#!/bin/bash
# Desinstalador completo de DeepRoot - Elimina todos los rastros
set -e

echo "🧹 Iniciando desinstalación completa de DeepRoot..."

# Función para obtener la ruta de instalación de forma confiable
get_install_dir() {
    # 1. Intento: Usar variable de entorno si existe
    if [ -n "$DEEP_ROOT_INSTALL_DIR" ]; then
        echo "$DEEP_ROOT_INSTALL_DIR"
        return
    fi
    
    # 2. Intento: Desde la ubicación del script
    local script_path=$(dirname "$(realpath "$0")")
    if [[ "$script_path" == *"deeproot" ]]; then
        echo "$script_path"
        return
    fi
    
    # 3. Intento: Buscar en el directorio actual
    if [[ "$PWD" == *"deeproot" ]]; then
        echo "$PWD"
        return
    fi
    
    # 4. Intento: Ubicación por defecto
    local default_path="$HOME/apps/deeproot"
    if [ -d "$default_path" ]; then
        echo "$default_path"
        return
    fi
    
    echo "ERROR"
    return 1
}

# Obtener ruta de instalación
INSTALL_DIR=$(get_install_dir)

if [ "$INSTALL_DIR" == "ERROR" ] || [ ! -d "$INSTALL_DIR" ]; then
    echo "❌ No se pudo determinar la ruta de instalación correcta"
    exit 1
fi

echo "✔ Ruta de instalación detectada: $INSTALL_DIR"

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
    # Actualizar base de datos de aplicaciones
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database "$HOME/.local/share/applications"
    fi
fi

# 3. Eliminar entorno virtual
VENV_DIR="$INSTALL_DIR/.venv"
if [ -d "$VENV_DIR" ]; then
    echo "✔ Eliminando entorno virtual..."
    rm -rf "$VENV_DIR"
fi

# 4. Eliminar aliases de los shells
clean_shell_rc() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        echo "✔ Limpiando ${shell_rc}..."
        sed -i '/# Alias para DeepRoot/d' "$HOME/${shell_rc}"
        sed -i '/alias deeproot=/d' "$HOME/${shell_rc}"
        sed -i '/alias uninstall-deeproot=/d' "$HOME/${shell_rc}"
    fi
}

clean_shell_rc ".bashrc"
clean_shell_rc ".zshrc"

# 5. Eliminar directorio de instalación (con confirmación y validación)
echo ""
echo "⚠ ¿Deseas eliminar el directorio de instalación completo? [y/N]"
echo "⚠ Directorio: $INSTALL_DIR"
read -r response
if [[ "$response" =~ ^[yY] ]]; then
    # Verificación de seguridad adicional
    if [[ "$INSTALL_DIR" =~ "deeproot" ]] && [ -d "$INSTALL_DIR" ]; then
        echo "✔ Eliminando $INSTALL_DIR..."
        cd ..  # Salimos del directorio antes de eliminarlo
        rm -rf "$INSTALL_DIR" || {
            echo "❌ Error al eliminar el directorio"
            exit 1
        }
    else
        echo "❌ Error: Ruta no segura para eliminar: $INSTALL_DIR"
        exit 1
    fi
fi

echo ""
echo "✅ ¡DeepRoot ha sido desinstalado completamente!"
echo "ℹ Por favor, cierra y reabre todas tus terminales para completar la desinstalación."
echo "Gracias por haber usado esta herramienta. Hasta pronto."
