#!/bin/sh
# Desinstalador seguro de DeepRoot - Versión mejorada
set -e

echo "🧹 Iniciando desinstalación de DeepRoot..."

# --- Funciones auxiliares ---
clean_shell_config() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        echo "✔ Limpiando ${shell_rc}..."
        sed -i '/# Configuración para DeepRoot/,/export DEEP_ROOT_INSTALL_DIR/d' "$HOME/${shell_rc}"
        sed -i '/alias deeproot=/d; /alias uninstall-deeproot=/d' "$HOME/${shell_rc}"
    fi
}

get_install_dir() {
    if [ -n "$DEEP_ROOT_INSTALL_DIR" ] && [ "$DEEP_ROOT_INSTALL_DIR" != "/opt" ]; then
        echo "$DEEP_ROOT_INSTALL_DIR"
    else
        echo "/opt/deeproot"  # Valor por defecto seguro
    fi
}

# --- Pasos de desinstalación ---
INSTALL_DIR=$(get_install_dir)

# 1. Limpiar configuraciones del shell
clean_shell_config ".bashrc"
clean_shell_config ".zshrc"
clean_shell_config ".profile"

# 2. Eliminar archivos de configuración
CONFIG_DIR="$HOME/.config/deeproot"
if [ -d "$CONFIG_DIR" ]; then
    echo "✔ Eliminando configuración en $CONFIG_DIR..."
    rm -rf "$CONFIG_DIR"
fi

# 3. Eliminar lanzador del menú
DESKTOP_FILE="$HOME/.local/share/applications/deeproot.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    echo "✔ Eliminando lanzador del menú..."
    rm -f "$DESKTOP_FILE"
    command -v update-desktop-database >/dev/null && update-desktop-database "$HOME/.local/share/applications"
fi

# 4. Eliminar entorno virtual
VENV_DIR="$INSTALL_DIR/.venv"
if [ -d "$VENV_DIR" ]; then
    echo "✔ Eliminando entorno virtual..."
    rm -rf "$VENV_DIR"
fi

# 5. Preguntar por el directorio de exportaciones (nuevo)
EXPORT_DIR="$HOME/Descargas/deeproot_exportaciones"
[ ! -d "$EXPORT_DIR" ] && EXPORT_DIR="$HOME/Downloads/deeproot_exportaciones"
if [ -d "$EXPORT_DIR" ]; then
    echo ""
    read -p "⚠ ¿Eliminar el directorio de exportaciones ($EXPORT_DIR) y TODO su contenido? [y/N]: " respuesta
    if [[ "$respuesta" =~ ^[yY] ]]; then
        echo "🗑️ Eliminando $EXPORT_DIR..."
        rm -rf "$EXPORT_DIR"
    else
        echo "ℹ️ Se conservó el directorio de exportaciones."
    fi
fi

# 6. Eliminar directorio de instalación (con doble validación)
if [ -d "$INSTALL_DIR" ]; then
    echo ""
    read -p "⚠ ¿Eliminar el directorio de instalación ($INSTALL_DIR)? [y/N]: " respuesta
    if [[ "$respuesta" =~ ^[yY] ]]; then
        if [[ "$INSTALL_DIR" == *"/deeproot" ]] && [ "$INSTALL_DIR" != "/opt" ]; then
            echo "✔ Eliminando $INSTALL_DIR..."
            cd "$(dirname "$INSTALL_DIR")" && rm -rf "$INSTALL_DIR"
        else
            echo "❌ ABORTADO: Ruta no válida." >&2
            exit 1
        fi
    else
        echo "ℹ️ Se conservó el directorio de instalación."
    fi
fi

# 7. Revertir enlace simbólico de libmpv (opcional)
LIBMPV_LINK=$(find /usr/lib* /usr/local/lib -name "libmpv.so.1" 2>/dev/null | head -n 1)
if [ -n "$LIBMPV_LINK" ] && [ -L "$LIBMPV_LINK" ]; then
    echo ""
    read -p "⚠ ¿Eliminar el enlace simbólico $LIBMPV_LINK? [y/N]: " respuesta
    if [[ "$respuesta" =~ ^[yY] ]]; then
        echo "🔗 Eliminando enlace simbólico..."
        sudo rm -f "$LIBMPV_LINK"
    fi
fi

# --- Finalización ---
unset DEEP_ROOT_INSTALL_DIR
echo ""
echo "✅ ¡Desinstalación completada!"
echo "ℹ️ Cierra y reabre tus terminales para aplicar los cambios."
