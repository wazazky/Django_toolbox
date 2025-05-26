import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import os
from commands.core import run_command, stop_runserver
from scripts.runner import cargar_scripts, ejecutar_script

def launch_app():
    root = tk.Tk()
    root.title("Django Toolbox")
    root.geometry("800x1000")
    root.configure(bg="#1e1e1e")

    # Estilo común
    bg_color = "#1e1e1e"
    fg_color = "#dcdcdc"
    btn_color = "#333333"
    entry_bg = "#2a2a2a"

    # Área de logs
    output = ScrolledText(root, wrap=tk.WORD, height=20, bg="#121212", fg="#dcdcdc", insertbackground="#ffffff")
    output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def log(msg):
        output.insert(tk.END, msg + "\n")
        output.see(tk.END)

    def cmd(command):
        log(f"→ Ejecutando: {command}")
        run_command(command, log)

    # Entrada para commit
    frame_commit = tk.Frame(root, bg=bg_color)
    frame_commit.pack(pady=5)
    tk.Label(frame_commit, text="Mensaje de commit:", bg=bg_color, fg=fg_color).pack(side=tk.LEFT)
    entry_commit = tk.Entry(frame_commit, width=50, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
    entry_commit.pack(side=tk.LEFT, padx=5)

    # Funciones Git
    def git_add():
        cmd("git add .")

    def git_commit():
        mensaje = entry_commit.get().strip()
        if not mensaje:
            log("⚠️ Escribe un mensaje para el commit.")
            return
        cmd(f'git commit -m "{mensaje}"')

    def git_push():
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                log("⚠️ Hay archivos sin commitear. Haz commit antes de hacer push.")
                return
            else:
                cmd("git push origin main")
        except Exception as e:
            log(f"❌ Error al verificar estado de git: {e}")

    def git_pull():
        cmd("git pull")

    def abrir_consola():
        ruta_manage = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        subprocess.Popen("start cmd", cwd=ruta_manage, shell=True)

    # Función para agrupar botones
    def crear_bloque(titulo):
        bloque = tk.LabelFrame(root, text=titulo, padx=10, pady=5, bg=bg_color, fg=fg_color, font=("Segoe UI", 10, "bold"))
        bloque.pack(padx=10, pady=5, fill=tk.X)
        return bloque

    def crear_boton(frame, texto, comando):
        tk.Button(frame, text=texto, width=30, command=comando, bg=btn_color, fg=fg_color, relief="flat").pack(pady=3)

    # --- Bloques ---

    # Django
    bloque_django = crear_bloque("⚙️ Comandos Django")
    botones = {
        "🔨 makemigrations": "python manage.py makemigrations",
        "🚚 migrate": "python manage.py migrate",
        "🚀 runserver": "python manage.py runserver",
        "⛑️ createsuperuser": "python manage.py createsuperuser",
    }
    for label, command in botones.items():
        crear_boton(bloque_django, label, lambda c=command: cmd(c))
    crear_boton(bloque_django, "🛑 Detener servidor", lambda: stop_runserver(log))

    # Git
    bloque_git = crear_bloque("🌿 Control de versiones (Git)")
    crear_boton(bloque_git, "➕ git add .", git_add)
    crear_boton(bloque_git, "💬 git commit", git_commit)
    crear_boton(bloque_git, "🚀 git push origin main", git_push)
    crear_boton(bloque_git, "📥 git pull", git_pull)

    # Scripts personalizados
    bloque_scripts = crear_bloque("🧩 Scripts personalizados")
    for script_cfg in cargar_scripts():
        crear_boton(bloque_scripts, f"⚙️ {script_cfg['nombre']}", lambda cfg=script_cfg: ejecutar_script(cfg, log))

    # Extra
    bloque_extra = crear_bloque("🖥️ Utilidades")
    crear_boton(bloque_extra, "🖥️ Abrir consola", abrir_consola)

    root.mainloop()
