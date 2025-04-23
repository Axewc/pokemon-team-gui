import os
import shutil
from pathlib import Path
import zipfile

def create_release_package():
    """Crea el paquete de release para Windows."""
    # Directorios necesarios
    dist_dir = Path("dist/Pokemon Team Tracker")
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # Crear archivo ZIP
    zip_path = release_dir / "Pokemon.Team.Tracker.zip"
    
    # Asegurarse de que el ejecutable existe
    if not dist_dir.exists():
        print("Error: El ejecutable no existe. Ejecuta PyInstaller primero.")
        return False
    
    # Crear el archivo ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Agregar todos los archivos del directorio dist
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arcname)
    
    print(f"Release package created: {zip_path}")
    return True

if __name__ == "__main__":
    create_release_package() 