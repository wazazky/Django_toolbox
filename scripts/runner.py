import json
import os
import subprocess


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # donde está manage.py
scripts_dir = os.path.dirname(__file__)
config_file = os.path.join(scripts_dir, "config.json")

def cargar_scripts():
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)

def ejecutar_script(script_config, callback):
    ruta_script = os.path.join(scripts_dir, script_config["archivo"])
    modo = script_config.get("modo")

    if modo == "local":
        ejecutar_desde(ruta_script, base_dir, callback)
    elif modo == "views":
        carpeta_con_views = buscar_views(base_dir)
        if carpeta_con_views:
            ejecutar_desde(ruta_script, carpeta_con_views, callback)
        else:
            callback("⚠️ No se encontró ninguna carpeta con views.py.")
    else:
        callback(f"❌ Modo no reconocido: {modo}")

def ejecutar_desde(script_path, cwd, callback):
    try:
        result = subprocess.run(
            ["python", script_path],
            cwd=cwd,
            capture_output=True,
            text=True
        )
        callback(result.stdout + result.stderr)
    except Exception as e:
        callback(f"❌ Error al ejecutar script: {e}")

def buscar_views(base_path):
    for carpeta in os.listdir(base_path):
        ruta = os.path.join(base_path, carpeta)
        if os.path.isdir(ruta) and "views.py" in os.listdir(ruta):
            return ruta
    return None
