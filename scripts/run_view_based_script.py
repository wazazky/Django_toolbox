import os
import subprocess


def ejecutar(callback):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # carpeta donde está manage.py
    for carpeta in os.listdir(base):
        ruta = os.path.join(base, carpeta)
        if os.path.isdir(ruta) and "views.py" in os.listdir(ruta):
            ruta_script = os.path.join(os.path.dirname(__file__), "script2.py")
            try:
                result = subprocess.run(
                    ["python", ruta_script],
                    cwd=ruta,  # ejecutamos desde la carpeta que contiene views.py
                    capture_output=True,
                    text=True
                )
                callback(result.stdout + result.stderr)
                return
            except Exception as e:
                callback(f"❌ Error al ejecutar script2.py en {ruta}: {e}")
                return

    callback("⚠️ No se encontró ninguna carpeta con views.py.")
