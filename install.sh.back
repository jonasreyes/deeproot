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
    #git clone https://github.com/jonasreyes/deeproot.git
    git clone ~/repositorios/deeproot.git
    cd deeproot || exit
else
    cd deeproot || exit
    git pull
fi

# Entorno virtual
python3 -m venv .venv
. .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install flet==0.27 openai asyncio markdown

# Generar lanzador en el menú
cd src && python generar_lanzador.py && cd ..

# ===== Añadir aliases a .bashrc y .zshrc =====
DEEP_ROOT_DIR="$(pwd)"

add_alias() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        if ! grep -q "alias deeproot=" "$HOME/${shell_rc}"; then
            echo "# Alias para DeepRoot" >> "$HOME/${shell_rc}"
            echo "alias deeproot='cd ${DEEP_ROOT_DIR} && . .venv/bin/activate && python src/main.py'" >> "$HOME/${shell_rc}"
            echo "alias uninstall-deeproot='sh ${DEEP_ROOT_DIR}/uninstall.sh'" >> "$HOME/${shell_rc}"
            echo "✔ Alias añadido a ${shell_rc}"
        else
            echo "ℹ️ Los aliases ya existen en ${shell_rc}"
        fi
    fi
}

add_alias ".bashrc"
add_alias ".zshrc"

echo "✅ ¡DeepRoot instalado correctamente!"
echo "📌 Ahora puedes ejecutarlo desde cualquier terminal con:"
echo "   deeproot"
echo "   uninstall-deeproot  # Para desinstalar"
