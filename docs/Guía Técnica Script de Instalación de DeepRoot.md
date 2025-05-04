# Guía Técnica: Script de Instalación de DeepRoot

**Fecha**: Domingo 04 de mayo de 2025  
**Sistema Base**: Canaima GNU/Linux v8.0  

## 📌 Propósito del Script
Instala y configura el entorno completo para ejecutar [DeepRoot](https://github.com/jonasreyes/deeproot), incluyendo:
- Clonación del repositorio
- Configuración de entorno Python virtual
- Gestión de dependencias
- Configuración de accesos directos y variables de entorno

## 🛠️ Funciones Principales (21 en total)

### 1. **Inicialización**
```bash
inicializar_directorios()
```
- **Finalidad**: Crea estructura base de directorios (`~/apps`, `~/.config/deeproot`)
- **Salida**: Directorios creados con permisos adecuados

### 2. **Verificación de Instalación Previa**
```bash
verificar_instalacion_previa()
```
- **Comportamiento**:
  - Detecta instalaciones existentes
  - Ofrece opciones de actualización o limpieza
- **Salidas Posibles**:
  - Continuar instalación
  - Actualizar existente
  - Abortar por directorio no vacío

### 3. **Gestión de Dependencias Multimedia**
```bash
verificar_libmpv()
```
- **Búsqueda Inteligente**:
  - Escanea 7 rutas comunes en diferentes distros
  - Detecta versiones alternativas (`.so.2`, etc.)
- **Salidas**:
  - ✅ Encontrado en [ruta]
  - ⚠️ Versión alternativa detectada
  - ❌ No encontrado (usa versión light)

### 4. **Configuración de Entorno Python**
```bash
configurar_entorno_python()
```
- **Acciones**:
  1. Crea venv en `.venv`
  2. Actualiza pip
  3. Instala `flet-desktop-light` + dependencias
- **Log**: Registra versión exacta de pip instalada

## 📂 Estructura de Directorios Resultante
```
~/
├── apps/
│   └── deeproot/       # Contenido del repositorio
│       ├── .venv/      # Entorno virtual Python
│       └── scripts/    # Scripts auxiliares
├── .config/
│   └── deeproot/
│       └── logs/       # Registros detallados
└── Descargas/deeproot_exportaciones/  # Datos exportables
```

## 🔗 Comandos Configurados
| Comando               | Acción                              |
|-----------------------|-------------------------------------|
| `deeproot`            | Inicia la aplicación                |
| `deeproot-update`     | Actualiza código y dependencias     |
| `deeproot-uninstall`  | Ejecuta script de desinstalación    |
| `deeproot-logs`       | Lista archivos de registro          |

## ⚠️ Consideraciones Clave
1. **Requisitos Futuros**:
   ```diff
   + Versiones posteriores requerirán libmpv.so.1
   - La versión actual usa flet-desktop-light
   ```
2. **Solución Recomendada**:
   ```bash
   sudo apt install libmpv1  # En Canaima/Debian
   ```

## 📜 Ejemplo de Salida Exitosa
```text
✅ INSTALACIÓN COMPLETADA
══════════════════════════════════════════

⚠️  AVISO IMPORTANTE:
  ▸ Esta versión usa flet-desktop-light
  ▸ Versiones futuras requerirán libmpv.so.1

📂 Estructura:
  ▸ ~/apps/deeproot (instalación)
  ▸ ~/Descargas/deeproot_exportaciones
```

---

*Documento generado con ❤️ usando DeepRoot y DeepSeek AI*  
*Sobre Canaima GNU/Linux v8.0 - Software Libre para Venezuela*  
*© 2025 - [Licencia DeepRoot](LICENSE)* (GPL-compatible)