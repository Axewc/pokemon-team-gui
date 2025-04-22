#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional
import yaml
from pathlib import Path

@dataclass
class Pokemon:
    """Clase que representa un Pokemon en el equipo."""
    id: int
    name: str
    nickname: str = ""
    sprite_url: str = ""
    position_x: int = 0
    position_y: int = 0

    def to_dict(self) -> dict:
        """Convierte el Pokemon a un diccionario para serialización."""
        return {
            "id": self.id,
            "name": self.name,
            "nickname": self.nickname,
            "sprite_url": self.sprite_url,
            "position_x": self.position_x,
            "position_y": self.position_y
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Pokemon':
        """Crea un Pokemon desde un diccionario."""
        return cls(**data)

class Team:
    """Clase que representa un equipo de Pokemon."""
    def __init__(self):
        self.pokemon: List[Pokemon] = []
        self.max_size = 6

    def add_pokemon(self, pokemon: Pokemon) -> bool:
        """Añade un Pokemon al equipo si hay espacio."""
        if len(self.pokemon) < self.max_size:
            self.pokemon.append(pokemon)
            return True
        return False

    def remove_pokemon(self, index: int) -> Optional[Pokemon]:
        """Elimina un Pokemon del equipo por su índice."""
        if 0 <= index < len(self.pokemon):
            return self.pokemon.pop(index)
        return None

    def save_to_file(self, filename: str):
        """Guarda el equipo en un archivo YAML."""
        data = {
            "pokemon": [p.to_dict() for p in self.pokemon]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Team':
        """Carga un equipo desde un archivo YAML."""
        team = cls()
        if Path(filename).exists():
            with open(filename, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and "pokemon" in data:
                    for p_data in data["pokemon"]:
                        team.add_pokemon(Pokemon.from_dict(p_data))
        return team
