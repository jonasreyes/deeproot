#!/bin/sh
set -e

# --- Configuración de usuario ---
CURRENT_USER=$(whoami)
CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)
HOME_DIR="$HOME"
LOCAL_DIR="$HOME/.local"
SUDO_REQUIRED=0
CONFIG_DIR="$HOME/.config/deeproot"
CONFIG_FILE="$CONFIG_DIR/deeproot.json"

# --- Función para verificar libmpv ---
verificar_libmpv() {
    echo "🔍 Verificando dependencia libmpv..."
    
    # Buscar libmpv.so.1 o libmpv.so.2 en directorios comunes
    LIBMPV1=$(find /usr/lib* /usr/local/lib -name "libmpv.so.1" 2>/dev/null | head -n 1)
    LIBMPV2=$(find /usr/lib* /usr/local/lib -name "libmpv.so.2" 2>/dev/null | head -n 1)
    
    if [ -n "$LIBMPV1" ]; then
        echo "✔ Encontrado libmpv.so.1 en $LIBMPV1"
        return 0
    elif [ -n "$LIBMPV2" ]; then
        echo "✔ Encontrado libmpv.so.2 en $LIBMPV2"
        echo "⚠ Se creará un enlace simbólico libmpv.so.1 -> libmpv.so.2"
        return 1
    else
        echo "❌ No se encontró libmpv.so.1 ni libmpv.so.2"
        return 2
    fi
}

# --- Función mejorada para ejecutar sudo ---
run_with_sudo() {
    if [ $SUDO_REQUIRED -eq 1 ]; then
        echo "🔐 [sudo requerido] $*"
        if sudo -n true 2>/dev/null; then
            sudo "$@"
        else
            echo "🔐 Se necesitan privilegios de administrador"
            sudo "$@" || {
                echo "❌ Error al ejecutar con sudo: $*"
                exit 1
            }
        fi
    else
        echo "➡️ [sin sudo] $*"
        "$@"
    fi
}

# --- Función para verificar necesidad de sudo ---
check_sudo_requirements() {
    SUDO_REQUIRED=0
    # Verificar si podemos escribir en /opt sin sudo
    if [ ! -w "/opt" ]; then
        SUDO_REQUIRED=1
    fi
    
    # Verificar si necesitamos instalar paquetes del sistema
    if [ $MPV_STATUS -eq 2 ]; then
        SUDO_REQUIRED=1
    fi
}

# --- Función para instalar en directorio de usuario si no hay sudo ---
install_local() {
    if [ $SUDO_REQUIRED -eq 0 ]; then
        INSTALL_DIR="$LOCAL_DIR/opt/deeproot"
        echo "📂 Instalando en directorio de usuario: $INSTALL_DIR"
        mkdir -p "$INSTALL_DIR"
        export DEEP_ROOT_INSTALL_DIR="$INSTALL_DIR"
    else
        INSTALL_DIR="/opt/deeproot"
        echo "📂 Instalando en directorio del sistema: $INSTALL_DIR"
        run_with_sudo mkdir -p "$INSTALL_DIR"
        run_with_sudo chown "$CURRENT_USER:$CURRENT_GID" "$INSTALL_DIR"
        export DEEP_ROOT_INSTALL_DIR="$INSTALL_DIR"
    fi
}

# --- Función mejorada para crear enlace simbólico ---
crear_enlace_libmpv() {
    LIBMPV2=$(find /usr/lib* /usr/local/lib -name "libmpv.so.2" 2>/dev/null | head -n 1)
    
    if [ -z "$LIBMPV2" ]; then
        echo "❌ Error: No se pudo encontrar libmpv.so.2"
        exit 1
    fi

    LIB_DIR=$(dirname "$LIBMPV2")
    ENLACE_DESTINO="$LIB_DIR/libmpv.so.1"

    echo "🔍 Configurando enlace en $LIB_DIR..."
    echo "   Origen: $LIBMPV2"
    echo "   Destino: $ENLACE_DESTINO"

    if [ -w "$LIB_DIR" ]; then
        echo "➡️ Creando enlace con permisos de usuario..."
        ln -sfv "$LIBMPV2" "$ENLACE_DESTINO" || {
            echo "❌ Error al crear enlace con permisos de usuario"
            exit 1
        }
    else
        echo "🔐 Creando enlace con sudo..."
        run_with_sudo ln -sfv "$LIBMPV2" "$ENLACE_DESTINO" || {
            echo "❌ Error al crear enlace con sudo"
            exit 1
        }
    fi

    echo "✅ Enlace creado exitosamente:"
    ls -l "$ENLACE_DESTINO"
}

# --- Función para instalar dependencias del sistema ---
install_dependencies() {
    if command -v apt >/dev/null 2>&1; then
        echo "🔄 Actualizando repositorios..."
        run_with_sudo apt update
        
        echo "📦 Instalando dependencias con apt..."
        run_with_sudo apt install -y python3 python3-venv python3-pip git
        
    elif command -v pacman >/dev/null 2>&1; then
        echo "🔄 Instalando dependencias con pacman..."
        run_with_sudo pacman -Sy --noconfirm python python-pip git
        
    else
        echo "⚠ No se encontró gestor de paquetes compatible"
        echo "ℹ️ Intentando continuar con Python del usuario..."
        
        if ! command -v python3 >/dev/null 2>&1; then
            echo "❌ Python3 no está instalado. Por favor instálalo manualmente."
            exit 1
        fi
    fi
}

# --- Función para instalar libmpv según la distribución ---
instalar_libmpv() {
    DISTRO=$1
    
    case $DISTRO in
        canaima|debian|ubuntu|linuxmint|pop)
            echo "🔄 Instalando libmpv en Debian/Ubuntu..."
            run_with_sudo apt install -y libmpv1
            ;;
        arch|archcraft|manjaro|endeavouros)
            echo "🔄 Instalando libmpv en Arch Linux..."
            run_with_sudo pacman -Sy --noconfirm mpv
            ;;
        fedora|centos|rhel)
            echo "🔄 Instalando libmpv en Fedora/CentOS..."
            run_with_sudo dnf install -y mpv-libs
            ;;
        opensuse|suse)
            echo "🔄 Instalando libmpv en openSUSE..."
            run_with_sudo zypper install -y libmpv1
            ;;
        *)
            echo "❌ No se pudo determinar cómo instalar libmpv en tu distribución"
            return 1
            ;;
    esac
    return 0
}

# --- Función para detectar la distribución Linux ---
detectar_distribucion() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    elif type lsb_release >/dev/null 2>&1; then
        lsb_release -is | tr '[:upper:]' '[:lower:]'
    else
        echo "unknown"
    fi
}

# --- Función para crear directorio de exportaciones ---
crear_directorio_exportaciones() {
    # Buscar directorio Descargas en español o inglés
    DESCARGAS_DIR=""
    if [ -d "$HOME/Descargas" ]; then
        DESCARGAS_DIR="$HOME/Descargas"
    elif [ -d "$HOME/Downloads" ]; then
        DESCARGAS_DIR="$HOME/Downloads"
    fi
    
    if [ -n "$DESCARGAS_DIR" ]; then
        EXPORT_DIR="$DESCARGAS_DIR/deeproot_exportaciones"
        echo "📂 Creando directorio de exportaciones: $EXPORT_DIR"
        mkdir -p "$EXPORT_DIR"
        chmod 755 "$EXPORT_DIR"
    else
        echo "⚠ No se encontró directorio Descargas/Downloads, creando en $HOME"
        mkdir -p "$HOME/deeproot_exportaciones"
        chmod 755 "$HOME/deeproot_exportaciones"
    fi
}

# --- Función para configurar aliases ---
add_alias() {
    local shell_rc=$1
    if [ -f "$HOME/${shell_rc}" ]; then
        if ! grep -q "alias deeproot=" "$HOME/${shell_rc}"; then
            echo "" >> "$HOME/${shell_rc}"
            echo "# Configuración para DeepRoot" >> "$HOME/${shell_rc}"
            echo "alias deeproot='cd \"$DEEP_ROOT_DIR\" && . .venv/bin/activate && python src/main.py'" >> "$HOME/${shell_rc}"
            echo "alias uninstall-deeproot='sh \"$DEEP_ROOT_DIR\"/uninstall.sh'" >> "$HOME/${shell_rc}"
            echo "export DEEP_ROOT_INSTALL_DIR=\"$DEEP_ROOT_DIR\"" >> "$HOME/${shell_rc}"
            echo "✔ Alias añadido a ${shell_rc}"
        else
            echo "ℹ️ Los aliases ya existen en ${shell_rc}"
        fi
    fi
}

# --- Función para mostrar resumen final ---
show_summary() {
    echo ""
    echo ""
    echo "--------------------------------------"
    echo "✅ ¡Instalación completada con éxito!"
    echo ""
    echo "📌 Para iniciar DeepRoot, ejecuta:"
    echo "   deeproot"
    echo ""
    echo "📍 Directorio de instalación: $DEEP_ROOT_DIR"
    echo "📁 Exportaciones se guardarán en: $EXPORT_DIR"
    echo ""
    echo "🔧 Configuración importante:"
    echo "   - Al iniciar por primera vez, deberás ingresar tu API_KEY y BASE_URL"
    echo "   - Estos datos se guardarán en: $CONFIG_FILE"
    echo ""
    echo "💡 Consejo: Puedes editar manualmente el archivo de configuración si necesitas"
    echo "   cambiar estos valores posteriormente."
    echo ""
    echo "✨ ¡Listo para usar DeepRoot! ✨"
}

# --- Inicio de la instalación ---
echo "🔄 Iniciando instalación de DeepRoot..."
echo "👤 Usuario: $CURRENT_USER (UID: $CURRENT_UID, GID: $CURRENT_GID)"

# 1. Verificar libmpv
verificar_libmpv
MPV_STATUS=$?

# 2. Determinar si necesitamos sudo
check_sudo_requirements

# 3. Manejar la instalación de libmpv según sea necesario
case $MPV_STATUS in
    1)  # Solo existe libmpv.so.2
        crear_enlace_libmpv
        ;;
    2)  # No existe ninguna versión
        echo "❌ DeepRoot requiere libmpv.so.1 o libmpv.so.2"
        read -p "¿Deseas instalar libmpv automáticamente? [s/N]: " respuesta
        if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
            DISTRO=$(detectar_distribucion)
            instalar_libmpv "$DISTRO"
            if [ $? -eq 0 ]; then
                verificar_libmpv
                MPV_STATUS=$?
                [ $MPV_STATUS -eq 1 ] && crear_enlace_libmpv
            else
                echo "ℹ️ Continuando sin libmpv (puede afectar algunas funcionalidades)"
            fi
        else
            echo "ℹ️ Continuando sin libmpv (puede afectar algunas funcionalidades)"
        fi
        ;;
esac

# 4. Instalar dependencias básicas
install_dependencies

# 5. Configurar directorio de instalación
install_local

# 6. Clonar repositorio
if [ ! -d "$INSTALL_DIR/.git" ]; then
    echo "📦 Clonando repositorio..."
    git clone https://github.com/jonasreyes/deeproot.git "$INSTALL_DIR"
    cd "$INSTALL_DIR" || exit
else
    echo "🔄 Actualizando repositorio existente..."
    cd "$INSTALL_DIR" || exit
    git pull
fi

# Configurar ruta absoluta
DEEP_ROOT_DIR="$(pwd)"
export DEEP_ROOT_INSTALL_DIR="$DEEP_ROOT_DIR"

# 7. Crear directorio de exportaciones (en el home del usuario)
crear_directorio_exportaciones

# 8. Crear directorio de configuración
mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"

# 9. Configurar entorno virtual
echo "🐍 Configurando entorno virtual Python..."
python3 -m venv .venv
. .venv/bin/activate

# 10. Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install --upgrade pip
pip install 'flet[desktop]==0.27' openai asyncio markdown

# 11. Generar lanzador en el menú (opcional)
if [ -f "src/generar_lanzador.py" ]; then
    echo "📌 Generando lanzador de aplicaciones..."
    cd src && python generar_lanzador.py && cd ..
fi

# 12. Configurar aliases
echo "🔧 Configurando aliases..."
add_alias ".bashrc"
add_alias ".zshrc"

# Mostrar resumen final
show_summary
