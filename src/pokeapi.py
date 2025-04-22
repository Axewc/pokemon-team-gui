#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging
from typing import Dict, List, Optional
import yaml
from pathlib import Path

class PokeAPIClient:
    """Cliente singleton para la PokeAPI."""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PokeAPIClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self._load_config()
            self._cache: Dict[str, dict] = {}
            self._initialized = True

    def _load_config(self):
        """Carga la configuración desde el archivo YAML."""
        config_path = Path("config/settings.yaml")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.base_url = config['api']['base_url']
                self.cache_timeout = config['api']['cache_timeout']
                self.max_retries = config['api']['max_retries']
        else:
            self.logger.warning("Archivo de configuración no encontrado, usando valores por defecto")
            self.base_url = "https://pokeapi.co/api/v2"
            self.cache_timeout = 3600
            self.max_retries = 3

    def get_pokemon_list(self) -> List[dict]:
        """Obtiene la lista de todos los Pokemon disponibles."""
        cache_key = "pokemon_list"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = requests.get(f"{self.base_url}/pokemon?limit=1000")
            response.raise_for_status()
            data = response.json()
            self._cache[cache_key] = data['results']
            return data['results']
        except requests.RequestException as e:
            self.logger.error(f"Error al obtener la lista de Pokemon: {e}")
            return []

    def get_pokemon_details(self, pokemon_id: int) -> Optional[dict]:
        """Obtiene los detalles de un Pokemon específico."""
        cache_key = f"pokemon_{pokemon_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = requests.get(f"{self.base_url}/pokemon/{pokemon_id}")
            response.raise_for_status()
            data = response.json()
            self._cache[cache_key] = data
            return data
        except requests.RequestException as e:
            self.logger.error(f"Error al obtener detalles del Pokemon {pokemon_id}: {e}")
            return None

    def get_sprite_url(self, pokemon_id: int) -> Optional[str]:
        """Obtiene la URL del sprite de un Pokemon."""
        details = self.get_pokemon_details(pokemon_id)
        if details and 'sprites' in details:
            return details['sprites']['front_default']
        return None
