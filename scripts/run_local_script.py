import os
import subprocess


def ejecutar(callback):
    ruta_script = os.path.join(os.path.dirname(__file__), "script1.py")
    proyecto_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # carpeta de manage.py
    try:
        result = subprocess.run(
            ["python", ruta_script],
            cwd=proyecto_base,
            capture_output=True,
            text=True
        )
        callback(result.stdout + result.stderr)
    except Exception as e:
        callback(f"❌ Error al ejecutar script1.py: {e}")
