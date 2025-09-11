#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import re
import gzip
from pathlib import Path
from datetime import datetime

# Colores para output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_info(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def print_success(msg):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None

def validate_architecture(arch):
    """Validar arquitectura"""
    valid_archs = ["amd64", "arm64", "armhf", "i386", "all"]
    return arch in valid_archs

def clean_package_name(name):
    """Limpiar nombre del paquete según estándares Debian"""
    # Convertir a minúsculas y reemplazar caracteres no válidos
    clean_name = name.lower()
    clean_name = re.sub(r'[^a-z0-9.-]', '-', clean_name)
    clean_name = re.sub(r'--+', '-', clean_name)
    clean_name = clean_name.strip('-')
    return clean_name

def validate_version(version):
    """Validar formato de versión"""
    pattern = r'^[0-9]+(\.[0-9]+)*([+-][A-Za-z0-9.~+-]+)?$'
    return re.match(pattern, version) is not None

def check_dependencies():
    """Verificar dependencias del sistema"""
    print_info("Verificando dependencias...")
    
    deps = ['dpkg-deb', 'fakeroot', 'gzip']
    missing = []
    
    for dep in deps:
        if shutil.which(dep) is None:
            missing.append(dep)
    
    if missing:
        print_error(f"Dependencias faltantes: {', '.join(missing)}")
        print("Instala con: sudo apt install dpkg-dev fakeroot")
        return False
    
    return True

def get_executable_files():
    """Obtener archivos ejecutables en el directorio actual"""
    executables = []
    for file in os.listdir('.'):
        if os.path.isfile(file) and os.access(file, os.X_OK) and not file.endswith('.sh'):
            executables.append(file)
    return executables

def get_image_files():
    """Obtener archivos de imagen en el directorio actual"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.ico']
    images = []
    for file in os.listdir('.'):
        if os.path.isfile(file) and any(file.lower().endswith(ext) for ext in image_extensions):
            images.append(file)
    return images

def collect_package_info():
    """Recopilar información del paquete interactivamente"""
    print("=" * 50)
    print("   Generador Automático de Paquetes .deb")
    print("=" * 50)
    print()
    
    if not check_dependencies():
        sys.exit(1)
    
    print("Por favor, proporciona la siguiente información:")
    print()
    
    # Nombre del paquete
    while True:
        package_name = input("Nombre del paquete: ").strip()
        if package_name:
            clean_name = clean_package_name(package_name)
            print_info(f"Nombre limpio del paquete: {clean_name}")
            package_name = clean_name
            break
        print_error("El nombre del paquete no puede estar vacío")
    
    # Versión
    while True:
        version = input("Versión (ej: 1.0.0): ").strip()
        if version and validate_version(version):
            break
        print_error("Formato de versión inválido. Use formato como: 1.0.0 o 1.0.0-1")
    
    # Arquitectura
    while True:
        arch = input("Arquitectura (amd64/arm64/armhf/i386/all) [amd64]: ").strip() or "amd64"
        if validate_architecture(arch):
            break
        print_error("Arquitectura no válida. Opciones: amd64, arm64, armhf, i386, all")
    
    # Descripción breve
    while True:
        short_desc = input("Descripción breve (una línea): ").strip()
        if short_desc:
            break
        print_error("La descripción breve no puede estar vacía")
    
    # Descripción extendida
    long_desc = ""
    add_long = input("¿Agregar descripción extendida? (y/N): ").strip().lower()
    if add_long in ['y', 'yes', 'sí', 's']:
        print("Descripción extendida (presiona Enter en línea vacía para terminar):")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        if lines:
            long_desc = '\n'.join(lines)
    
    # Mantenedor
    while True:
        maintainer_name = input("Nombre del mantenedor: ").strip()
        if maintainer_name:
            break
        print_error("El nombre del mantenedor no puede estar vacío")
    
    while True:
        maintainer_email = input("Email del mantenedor: ").strip()
        if maintainer_email and validate_email(maintainer_email):
            break
        print_error("Email inválido")
    
    # Dependencias
    dependencies = input("Dependencias (opcional, separadas por coma): ").strip()
    
    # Binario
    print()
    executables = get_executable_files()
    if executables:
        print_info("Archivos ejecutables disponibles:")
        for exe in executables[:10]:
            print(f"  {exe}")
    
    while True:
        binary_name = input("Nombre del binario a empaquetar: ").strip()
        if not binary_name:
            print_error("El nombre del binario no puede estar vacío")
            continue
        if not os.path.isfile(binary_name):
            print_error(f"El archivo '{binary_name}' no existe")
            continue
        if not os.access(binary_name, os.X_OK):
            print_error(f"El archivo '{binary_name}' no es ejecutable")
            continue
        break
    
    # Icono
    print()
    images = get_image_files()
    if images:
        print_info("Archivos de imagen disponibles:")
        for img in images[:10]:
            print(f"  {img}")
    
    icon_file = input("Archivo de icono (opcional, Enter para generar automáticamente): ").strip()
    if icon_file and not os.path.isfile(icon_file):
        print_warning(f"El archivo de icono '{icon_file}' no existe, se generará automáticamente")
        icon_file = ""
    
    return {
        'package_name': package_name,
        'version': version,
        'architecture': arch,
        'short_description': short_desc,
        'long_description': long_desc,
        'maintainer_name': maintainer_name,
        'maintainer_email': maintainer_email,
        'dependencies': dependencies,
        'binary_name': binary_name,
        'icon_file': icon_file
    }

def create_templates():
    """Crear archivos de plantilla"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Plantilla control
    control_template = """Package: {package_name}
Version: {version}
Architecture: {architecture}
Maintainer: {maintainer_name} <{maintainer_email}>{depends_line}
Priority: optional
Section: misc
Description: {short_description}{long_description_formatted}
"""
    
    # Plantilla postinst
    postinst_template = """#!/bin/bash
# Script ejecutado después de la instalación
set -e

# Actualizar cache de iconos si existe gtk-update-icon-cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi

# Actualizar base de datos de aplicaciones
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications 2>/dev/null || true
fi

exit 0
"""
    
    # Plantilla prerm
    prerm_template = """#!/bin/bash
# Script ejecutado antes de la desinstalación
set -e

exit 0
"""
    
    # Plantilla .desktop
    desktop_template = """[Desktop Entry]
Type=Application
Name={package_name}
Comment={short_description}
Exec={package_name}
Icon={package_name}
Categories=Application;
Terminal=false
StartupNotify=true
"""
    
    # Plantilla changelog
    changelog_template = """{package_name} ({version}) unstable; urgency=low

  * Initial release

 -- {maintainer_name} <{maintainer_email}>  {date}
"""
    
    # Plantilla copyright
    copyright_template = """Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: {package_name}
Source: <insert source URL here>

Files: *
Copyright: {year} {maintainer_name} <{maintainer_email}>
License: GPL-3+
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 .
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 .
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
 .
 On Debian systems, the complete text of the GNU General
 Public License version 3 can be found in "/usr/share/common-licenses/GPL-3".
"""
    
    # Escribir plantillas
    with open(templates_dir / "control.template", "w") as f:
        f.write(control_template)
    
    with open(templates_dir / "postinst.template", "w") as f:
        f.write(postinst_template)
    
    with open(templates_dir / "prerm.template", "w") as f:
        f.write(prerm_template)
    
    with open(templates_dir / "desktop.template", "w") as f:
        f.write(desktop_template)
    
    with open(templates_dir / "changelog.template", "w") as f:
        f.write(changelog_template)
    
    with open(templates_dir / "copyright.template", "w") as f:
        f.write(copyright_template)
    
    print_success("Plantillas creadas en directorio 'templates'")

def format_long_description(long_desc):
    """Formatear descripción extendida para el archivo control"""
    if not long_desc:
        return ""
    
    lines = long_desc.split('\n')
    formatted_lines = []
    for line in lines:
        if line.strip():
            formatted_lines.append(f" {line}")
        else:
            formatted_lines.append(" .")
    
    return "\n" + "\n".join(formatted_lines)

def create_package_structure(info):
    """Crear estructura del paquete"""
    package_dir = f"{info['package_name']}_{info['version']}"
    
    print_info(f"Creando estructura del paquete: {package_dir}")
    
    # Limpiar directorio existente
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    # Crear directorios
    dirs = [
        f"{package_dir}/DEBIAN",
        f"{package_dir}/usr/bin",
        f"{package_dir}/usr/share/applications",
        f"{package_dir}/usr/share/doc/{info['package_name']}",
        f"{package_dir}/usr/share/icons/hicolor/256x256/apps"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print_success("Estructura de directorios creada")
    return package_dir

def copy_binary(info, package_dir):
    """Copiar binario al paquete"""
    src = info['binary_name']
    dst = f"{package_dir}/usr/bin/{info['package_name']}"
    
    shutil.copy2(src, dst)
    os.chmod(dst, 0o755)
    
    print_success(f"Binario copiado: {src} -> usr/bin/{info['package_name']}")

def handle_icon(info, package_dir):
    """Manejar icono del paquete"""
    icon_dest = f"{package_dir}/usr/share/icons/hicolor/256x256/apps/{info['package_name']}.png"
    
    if info['icon_file'] and os.path.isfile(info['icon_file']):
        # Convertir icono si es posible
        if shutil.which('convert'):
            try:
                subprocess.run(['convert', info['icon_file'], '-resize', '256x256', icon_dest], 
                             check=True, capture_output=True)
                print_success(f"Icono convertido: {info['icon_file']}")
                return
            except subprocess.CalledProcessError:
                print_warning("Error al convertir icono, usando placeholder")
        elif info['icon_file'].lower().endswith('.png'):
            shutil.copy2(info['icon_file'], icon_dest)
            print_success(f"Icono copiado: {info['icon_file']}")
            return
        else:
            print_warning("Sin ImageMagick no se puede convertir, usando placeholder")
    
    # Crear placeholder
    if shutil.which('convert'):
        try:
            subprocess.run(['convert', '-size', '256x256', 'xc:lightblue', 
                          '-gravity', 'center', '-pointsize', '32', '-fill', 'darkblue',
                          '-annotate', '0', info['package_name'], icon_dest], 
                         check=True, capture_output=True)
            print_success("Icono placeholder generado automáticamente")
        except subprocess.CalledProcessError:
            # Crear archivo vacío
            open(icon_dest, 'a').close()
            print_warning("No se pudo crear icono con ImageMagick")
    else:
        # Crear archivo vacío
        open(icon_dest, 'a').close()
        print_warning("Instala ImageMagick para generar iconos: sudo apt install imagemagick")

def generate_files(info, package_dir):
    """Generar archivos del paquete usando plantillas"""
    templates_dir = Path("templates")
    
    # Preparar variables para las plantillas
    depends_line = f"\nDepends: {info['dependencies']}" if info['dependencies'] else ""
    long_description_formatted = format_long_description(info['long_description'])
    
    template_vars = {
        'package_name': info['package_name'],
        'version': info['version'],
        'architecture': info['architecture'],
        'maintainer_name': info['maintainer_name'],
        'maintainer_email': info['maintainer_email'],
        'depends_line': depends_line,
        'short_description': info['short_description'],
        'long_description_formatted': long_description_formatted,
        'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z') or 
                datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000'),
        'year': datetime.now().year
    }
    
    # Generar control
    print_info("Generando archivo DEBIAN/control")
    with open(templates_dir / "control.template", "r") as f:
        control_content = f.read().format(**template_vars)
    
    with open(f"{package_dir}/DEBIAN/control", "w") as f:
        f.write(control_content)
    
    os.chmod(f"{package_dir}/DEBIAN/control", 0o644)
    
    # Mostrar contenido para debug
    print_info("Contenido del archivo control generado:")
    print("=" * 30)
    with open(f"{package_dir}/DEBIAN/control", "r") as f:
        for i, line in enumerate(f, 1):
            print(f"{i:2}: {line.rstrip()}")
    print("=" * 30)
    
    # Generar postinst
    print_info("Creando scripts postinst y prerm")
    with open(templates_dir / "postinst.template", "r") as f:
        postinst_content = f.read()
    
    with open(f"{package_dir}/DEBIAN/postinst", "w") as f:
        f.write(postinst_content)
    
    os.chmod(f"{package_dir}/DEBIAN/postinst", 0o755)
    
    # Generar prerm
    with open(templates_dir / "prerm.template", "r") as f:
        prerm_content = f.read()
    
    with open(f"{package_dir}/DEBIAN/prerm", "w") as f:
        f.write(prerm_content)
    
    os.chmod(f"{package_dir}/DEBIAN/prerm", 0o755)
    
    # Generar .desktop
    print_info("Generando archivo .desktop")
    with open(templates_dir / "desktop.template", "r") as f:
        desktop_content = f.read().format(**template_vars)
    
    desktop_file = f"{package_dir}/usr/share/applications/{info['package_name']}.desktop"
    with open(desktop_file, "w") as f:
        f.write(desktop_content)
    
    os.chmod(desktop_file, 0o644)
    
    # Generar changelog
    print_info("Generando changelog")
    with open(templates_dir / "changelog.template", "r") as f:
        changelog_content = f.read().format(**template_vars)
    
    changelog_file = f"{package_dir}/usr/share/doc/{info['package_name']}/changelog.Debian"
    with open(changelog_file, "w") as f:
        f.write(changelog_content)
    
    # Comprimir changelog
    with open(changelog_file, 'rb') as f_in:
        with gzip.open(f"{changelog_file}.gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    os.remove(changelog_file)
    os.chmod(f"{changelog_file}.gz", 0o644)
    
    # Generar copyright
    print_info("Generando archivo copyright")
    with open(templates_dir / "copyright.template", "r") as f:
        copyright_content = f.read().format(**template_vars)
    
    copyright_file = f"{package_dir}/usr/share/doc/{info['package_name']}/copyright"
    with open(copyright_file, "w") as f:
        f.write(copyright_content)
    
    os.chmod(copyright_file, 0o644)

def build_package(info, package_dir):
    """Construir el paquete .deb"""
    print_info("Construyendo paquete .deb...")
    
    deb_file = f"{info['package_name']}_{info['version']}_{info['architecture']}.deb"
    
    try:
        subprocess.run(['fakeroot', 'dpkg-deb', '--build', package_dir, deb_file], 
                      check=True, capture_output=True)
        
        print_success("¡Paquete .deb creado exitosamente!")
        print()
        print("=" * 50)
        print(f"  PAQUETE GENERADO: {deb_file}")
        print("=" * 50)
        print()
        print("Para instalar el paquete:")
        print(f"  sudo dpkg -i {deb_file}")
        print("  sudo apt-get install -f  # Si hay dependencias faltantes")
        print()
        print("Para verificar el contenido:")
        print(f"  dpkg-deb -c {deb_file}")
        print()
        print("Para ver información del paquete:")
        print(f"  dpkg-deb -I {deb_file}")
        print()
        
        # Mostrar tamaño del archivo
        size = os.path.getsize(deb_file)
        size_mb = size / (1024 * 1024)
        if size_mb > 1:
            print_info(f"Tamaño del paquete: {size_mb:.1f} MB")
        else:
            size_kb = size / 1024
            print_info(f"Tamaño del paquete: {size_kb:.1f} KB")
        
        # Limpiar directorio temporal
        cleanup = input(f"¿Eliminar directorio temporal '{package_dir}'? (y/N): ").strip().lower()
        if cleanup in ['y', 'yes', 'sí', 's']:
            shutil.rmtree(package_dir)
            print_success("Directorio temporal eliminado")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error("Error al construir el paquete .deb")
        if e.stderr:
            print(e.stderr.decode())
        return False

def main():
    """Función principal"""
    try:
        # Crear plantillas
        create_templates()
        
        # Recopilar información
        info = collect_package_info()
        
        # Crear estructura
        package_dir = create_package_structure(info)
        
        # Copiar binario
        copy_binary(info, package_dir)
        
        # Manejar icono
        handle_icon(info, package_dir)
        
        # Generar archivos
        generate_files(info, package_dir)
        
        # Construir paquete
        if build_package(info, package_dir):
            print_success("Proceso completado exitosamente")
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print_error("\nProceso cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
