#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import logging
from pathlib import Path
from typing import Dict, Optional
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal

class AssetManager(QObject):
    """Gestor de assets para la aplicación."""
    sprite_loaded = pyqtSignal(str, QPixmap)  # Señal emitida cuando se carga un sprite

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._cache: Dict[str, QPixmap] = {}
        self._setup_directories()

    def _setup_directories(self):
        """Configura los directorios necesarios para los assets."""
        self.cache_dir = Path("assets/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_sprite(self, url: str) -> Optional[QPixmap]:
        """Obtiene un sprite desde la URL o caché."""
        if not url:
            return None

        # Verificar caché en memoria
        if url in self._cache:
            return self._cache[url]

        # Verificar caché en disco
        filename = self._get_cache_filename(url)
        if filename.exists():
            pixmap = QPixmap(str(filename))
            if not pixmap.isNull():
                self._cache[url] = pixmap
                return pixmap

        # Descargar y guardar en caché
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Guardar en disco
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            # Cargar en memoria
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            
            if not pixmap.isNull():
                self._cache[url] = pixmap
                self.sprite_loaded.emit(url, pixmap)
                return pixmap
            
        except Exception as e:
            self.logger.error(f"Error al cargar sprite desde {url}: {e}")
        
        return None

    def _get_cache_filename(self, url: str) -> Path:
        """Genera un nombre de archivo para el caché basado en la URL."""
        import hashlib
        hash_name = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{hash_name}.png"

    def clear_cache(self):
        """Limpia la caché de sprites."""
        self._cache.clear()
        for file in self.cache_dir.glob("*.png"):
            try:
                file.unlink()
            except Exception as e:
                self.logger.error(f"Error al eliminar archivo de caché {file}: {e}")

    def get_sprite_size(self) -> int:
        """Obtiene el tamaño configurado para los sprites."""
        try:
            with open("config/settings.yaml", 'r', encoding='utf-8') as f:
                import yaml
                config = yaml.safe_load(f)
                return config['sprites']['size']
        except Exception as e:
            self.logger.warning(f"Error al leer configuración de tamaño de sprite: {e}")
            return 96  # Tamaño por defecto
