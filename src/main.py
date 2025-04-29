#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from gui import MainWindow
from models import Team
from pokeapi import PokeAPIClient
from assets import AssetManager

def setup_logging():
    """Configura el sistema de logging."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )

def main():
    """Función principal de la aplicación."""
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Iniciando Pokemon Team GUI")

    # Crear directorios necesarios
    base_dir = Path(__file__).resolve().parent.parent  # Subir un nivel desde src
    assets_dir = base_dir / "assets" / "cache"
    saves_dir = base_dir / "saves"
    assets_dir.mkdir(parents=True, exist_ok=True)
    saves_dir.mkdir(exist_ok=True)

    # Inicializar la aplicación Qt
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Estilo moderno y consistente
    
    # Establecer el ícono de la aplicación
    app_icon = QIcon(str(base_dir / "assets" / "icon.ico"))
    app.setWindowIcon(app_icon)

    # Inicializar componentes principales
    api_client = PokeAPIClient()
    asset_manager = AssetManager()
    team_file = saves_dir / "team.yaml"
    team = Team.load_from_file(str(team_file))

    # Crear y mostrar la ventana principal
    window = MainWindow(team, api_client, asset_manager)
    window.setWindowIcon(app_icon)  # Establecer el ícono en la ventana principal
    window.show()

    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
