import ast


def extract_classes_from_file(file_path):
    with open(file_path, 'r') as file:
        node = ast.parse(file.read(), filename=file_path)
    
    classes = []
    for n in ast.iter_child_nodes(node):
        if isinstance(n, ast.ClassDef):
            classes.append(n.name)
    
    return classes

def generate_admin_file(classes, output_file='admin.py'):
    with open(output_file, 'w') as file:
        file.write("from django.contrib import admin\n")
        file.write("from .models import " + ", ".join(classes) + "\n\n")
        
        for class_name in classes:
            file.write(f"@admin.register({class_name})\n")
            file.write(f"class {class_name}Admin(admin.ModelAdmin):\n")
            file.write("    pass\n\n")

if __name__ == "__main__":
    # Ruta al archivo .py que contiene las clases
    input_file = 'models.py'
    
    # Extraer las clases del archivo
    classes = extract_classes_from_file(input_file)
    
    # Generar el archivo admin.py
    generate_admin_file(classes)
    
    print(f"Archivo 'admin.py' generado con las clases: {', '.join(classes)}")