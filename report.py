import os
from pathlib import Path


def gather_project_context(root_dir, output_file="project_context.txt", max_file_size=100000):
    """
    Recopila la estructura y contenido de un proyecto para análisis de contexto.
    Se incluyen archivos con extensión de texto definidos en `text_extensions` y
    además, los archivos cuyo nombre sea exactamente "qmldir" (sin extensión).
    """
    exclude_dirs = {'.git', '__pycache__', 'venv', 'env', '.idea', 'node_modules', 'report', 'project_context'}
    exclude_files = {'.gitignore', '.env', '*.pyc', '*.pyo', '*.pyd', '*.db', '*.sqlite3'}
    text_extensions = {'.qml', '.py', '.js', '.html', '.css', '.json', '.txt', '.md', '.yaml', '.yml'}
    exclude_dirs.add('.venv')  # Ignorar directorio de tests

    max_file_size = 500000  # Aumentar límite a 500KB

    with open(output_file, 'w', encoding='utf-8') as report:
        # Encabezado del reporte
        report.write("=== PROYECTO ANALYSIS CONTEXT ===\n\n")

        # Recorrer estructura de directorios
        report.write("## Estructura del Proyecto ##\n")
        for root, dirs, files in os.walk(root_dir):
            # Filtrar directorios
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            # Calcular nivel de indentación
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            report.write(f"{indent}{os.path.basename(root)}/\n")

            # Procesar archivos
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                # Si el archivo se debe excluir por su extensión, se salta
                if any(f.endswith(ext) for ext in exclude_files):
                    continue
                report.write(f"{sub_indent}{f}\n")

        # Contenido de archivos relevantes
        report.write("\n\n## Contenido de Archivos ##\n")
        for path in Path(root_dir).rglob('*'):
            if path.is_file() and not any(p in exclude_dirs for p in path.parts):
                # Se incluye el archivo si su extensión está en text_extensions o si el nombre es "qmldir"
                if path.suffix.lower() in text_extensions or path.name.lower() == "qmldir":
                    if path.stat().st_size <= max_file_size:
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                report.write(f"\n### Archivo: {path.relative_to(root_dir)} ###\n")
                                report.write(f"```{path.suffix[1:] if path.suffix else 'qmldir'}\n{content}\n```\n\n")
                        except UnicodeDecodeError:
                            report.write(f"\n# Error leyendo archivo: {path} (formato binario)\n")
                        except Exception as e:
                            report.write(f"\n# Error procesando {path}: {str(e)}\n")


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_path = "project_context.txt"
    gather_project_context(project_root, output_path)

    print(f"Contexto generado en: {output_path}")
    print(f"Tamaño del reporte: {os.path.getsize(output_path) / 1024:.2f} KB")
