#!/bin/sh
set -e

echo "🔄 Instalando DeepRoot en Canaima GNU/Linux (Zsh/Bash)..."
echo "✔ Verificando dependencias..."

# Instalar dependencias
if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip git
elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy python python-pip git --noconfirm
else
    echo "❌ Error: Gestor de paquetes no soportado. Instala Python 3.8+ y pip manualmente."
    exit 1
fi

# Clonar repositorio
if [ ! -d "deeproot" ]; then
    echo "📂 Seleccione la ruta de instalación (deje vacío para usar $(pwd)):"
    read -r install_path
    
    # Usar ruta actual si no se especifica
    if [ -z "$install_path" ]; then
        install_path="$(pwd)"
    else
        # Crear directorio si no existe
        mkdir -p "$install_path"
    fi

    git clone https://github.com/jonasreyes/deeproot.git "$install_path/deeproot"
    cd "$install_path/deeproot" || exit
else
    cd deeproot || exit
    git pull
fi

# Configurar ruta absoluta
DEEP_ROOT_DIR="$(pwd)"
export DEEP_ROOT_INSTALL_DIR="$DEEP_ROOT_DIR"  # Exportar para uso inmediato

# Entorno virtual
python3 -m venv .venv
. .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install flet==0.27 openai asyncio markdown

# Generar lanzador en el menú
cd src && python generar_lanzador.py && cd ..

# ===== Añadir aliases a .bashrc y .zshrc =====
add_alias() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        if ! grep -q "alias deeproot=" "$HOME/${shell_rc}"; then
            echo "# Alias para DeepRoot" >> "$HOME/${shell_rc}"
            echo "alias deeproot='cd \"$DEEP_ROOT_DIR\" && . .venv/bin/activate && python src/main.py'" >> "$HOME/${shell_rc}"
            echo "alias uninstall-deeproot='DEEP_ROOT_INSTALL_DIR=\"$DEEP_ROOT_DIR\" && sh \"$DEEP_ROOT_DIR\"/uninstall.sh'" >> "$HOME/${shell_rc}"
            echo "export DEEP_ROOT_INSTALL_DIR=\"$DEEP_ROOT_DIR\"" >> "$HOME/${shell_rc}"  # Persistencia en shell
            echo "✔ Alias añadido a ${shell_rc}"
        else
            echo "ℹ️ Los aliases ya existen en ${shell_rc}"
        fi
    fi
}

add_alias ".bashrc"
add_alias ".zshrc"

# Configurar variable de entorno global (opcional)
if [ -f "$HOME/.profile" ] && ! grep -q "DEEP_ROOT_INSTALL_DIR" "$HOME/.profile"; then
    echo "export DEEP_ROOT_INSTALL_DIR=\"$DEEP_ROOT_DIR\"" >> "$HOME/.profile"
fi

echo "✅ ¡DeepRoot instalado correctamente!"
echo "📌 Ahora puedes ejecutarlo desde cualquier terminal con:"
echo "   deeproot"
echo "   uninstall-deeproot  # Para desinstalar"
echo ""
echo "📍 Ruta de instalación: $DEEP_ROOT_DIR"
