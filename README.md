# 🛠️ Django Toolbox  <img src="https://github.com/user-attachments/assets/d6850d97-a9d6-4a5b-a017-a8d5ae37b44c" width="50" alt="Mascota del temporizador">

Una herramienta gráfica en Python para facilitar tareas comunes de desarrollo en proyectos Django.

## 🚀 Características

- Interfaz gráfica estilo oscuro con `tkinter`.
- Ejecución rápida de comandos Django:
  - `makemigrations`
  - `migrate`
  - `runserver`
  - `createsuperuser`
  - Detener servidor con botón
- Control Git:
  - `git add .`
  - `git commit -m`
  - `git push origin main`
  - `git pull`
- Ejecución de scripts personalizados (con configuración en JSON).
- Botón para abrir la consola directamente desde el proyecto.

## 📦 Instalación y uso

1. **Clona o copia la carpeta `Django_toolbox/`** dentro de tu proyecto Django (donde esté `manage.py`):

```
mi_proyecto/
├── manage.py
├── Django_toolbox/
│   ├── main.py
│   ├── commands/
│   ├── ui/
│   └── scripts/
```

2. **Ejecuta la toolbox** desde terminal:

```bash
python Django_toolbox/main.py
```

3. **(Opcional)** Crea un archivo `.bat` en Windows para lanzarla con doble clic:

```bat
@echo off
cd /d "%~dp0"
python Django_toolbox\main.py
pause
```

## 🧩 Scripts personalizados

Registra tus scripts en `Django_toolbox/scripts/config.json` así:

```json
[
  {
    "nombre": "Mi Script Local",
    "archivo": "script1.py",
    "modo": "local"
  },
  {
    "nombre": "Script que requiere views.py",
    "archivo": "script2.py",
    "modo": "views"
  }
]
```

Los scripts deben vivir en `Django_toolbox/scripts/`.

## ⚠️ Recomendaciones

- **No incluyas la toolbox en tu control de versiones**. Añádela al `.gitignore`:

```
Django_toolbox/
```

- Asegúrate de tener Python instalado y accesible desde la terminal.

## ✅ Requisitos

- Python 3.8+
- Librerías estándar (`tkinter`, `subprocess`, etc.)
- Para detener el servidor correctamente en Windows, también se requiere:

```bash
pip install psutil
```

---

Hecho con cariño por Wazazky ☠️
