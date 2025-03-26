#!/bin/sh
echo "🧹 Desinstalando DeepRoot..."

# Eliminar configuración y lanzador
rm -rf ~/.config/deeproot
rm -rf ~/.local/share/applications/deeproot.desktop

# Eliminar entorno virtual
if [ -d "deeproot/.venv" ]; then
    echo "✔ Eliminando entorno virtual..."
    rm -rf deeproot/.venv
fi

# ===== Remover aliases de .bashrc y .zshrc =====
remove_aliases() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        sed -i '/# Alias para DeepRoot/,/uninstall-deeproot/d' "$HOME/${shell_rc}"
        echo "✔ Aliases eliminados de ${shell_rc}"
    fi
}

remove_aliases ".bashrc"
remove_aliases ".zshrc"

echo "✅ ¡DeepRoot y sus aliases fueron desinstalados completamente!"
