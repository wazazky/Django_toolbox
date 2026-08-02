import psutil
import subprocess
import threading
import os


runserver_process = None

# Directorio base del proyecto Django (donde está manage.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def run_command(command, callback=None):
    def task():
        global runserver_process
        try:
            if "runserver" in command:
                runserver_process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=BASE_DIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                for line in iter(runserver_process.stdout.readline, ''):
                    if callback:
                        callback(line.strip())
            else:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=BASE_DIR,
                    capture_output=True,
                    text=True
                )
                output = result.stdout + result.stderr
                if callback:
                    callback(output)
        except Exception as e:
            if callback:
                callback(f"Error al ejecutar comando: {e}")

    threading.Thread(target=task, daemon=True).start()

def stop_runserver(callback=None):
    global runserver_process
    if runserver_process and runserver_process.poll() is None:
        try:
            proc = psutil.Process(runserver_process.pid)
            for child in proc.children(recursive=True):
                child.kill()
            proc.kill()
            if callback:
                callback("🔴 Servidor detenido por PID (forzado).")
        except Exception as e:
            if callback:
                callback(f"❌ No se pudo detener el servidor: {e}")
        runserver_process = None
    else:
        if callback:
            callback("⚠️ No hay servidor corriendo.")
