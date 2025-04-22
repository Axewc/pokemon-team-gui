#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

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
    Path("assets/cache").mkdir(parents=True, exist_ok=True)
    Path("saves").mkdir(exist_ok=True)

    # Inicializar la aplicación Qt
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Estilo moderno y consistente

    # Inicializar componentes principales
    api_client = PokeAPIClient()
    asset_manager = AssetManager()
    team = Team()

    # Crear y mostrar la ventana principal
    window = MainWindow(team, api_client, asset_manager)
    window.show()

    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
