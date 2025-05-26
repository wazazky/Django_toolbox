

import os
import re
from collections import defaultdict


EXCLUIR_CARPETAS = {'__pycache__', '.venv', 'venv', '.git', 'env'}
LOG_FILE = 'import_cleanup.log'

def procesar_imports(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    encabezado = []
    otras_lineas = []
    en_imports = True

    for linea in lineas:
        if en_imports and linea.strip().startswith(('import ', 'from ')) and not linea.startswith((' ', '\t')):
            encabezado.append(linea.strip())
        else:
            en_imports = False
            otras_lineas.append(linea)

    # Agrupar imports únicos
    from_imports = defaultdict(set)
    direct_imports = set()

    for imp in encabezado:
        if imp.startswith("from "):
            match = re.match(r'^from (\S+) import (.+)', imp)
            if match:
                modulo, elementos = match.groups()
                for elemento in elementos.split(','):
                    from_imports[modulo].add(elemento.strip())
        elif imp.startswith("import "):
            direct_imports.add(imp)

    # Reconstrucción ordenada y sin duplicados
    imports_ordenados = sorted(direct_imports)
    for modulo in sorted(from_imports):
        elementos = sorted(from_imports[modulo])
        imports_ordenados.append(f"from {modulo} import {', '.join(elementos)}")

    nuevo_contenido = [line + '\n' for line in imports_ordenados]
    nuevo_contenido.append('\n\n')  # Exactamente dos saltos de línea

    # Quitar líneas en blanco iniciales
    while otras_lineas and otras_lineas[0].strip() == '':
        otras_lineas.pop(0)

    nuevo_contenido.extend(otras_lineas)

    with open(archivo, 'w', encoding='utf-8') as f:
        f.writelines(nuevo_contenido)

    return True

def limpiar_imports_en_carpeta():
    modificados = []

    for raiz, carpetas, archivos in os.walk('.'):
        carpetas[:] = [c for c in carpetas if c not in EXCLUIR_CARPETAS]
        for archivo in archivos:
            if archivo.endswith('.py'):
                ruta_completa = os.path.join(raiz, archivo)
                print(f"Procesando: {ruta_completa}")
                if procesar_imports(ruta_completa):
                    modificados.append(ruta_completa)

    with open(LOG_FILE, 'w', encoding='utf-8') as log:
        log.write("Archivos modificados:\n")
        for ruta in modificados:
            log.write(f"{ruta}\n")

if __name__ == "__main__":
    limpiar_imports_en_carpeta()
