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
        self.total_hearts = 20  # Número total de corazones
        self.current_hearts = 20  # Corazones actuales

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

    def set_hearts(self, count: int):
        """Establece el número de corazones actual."""
        self.current_hearts = max(0, min(count, self.total_hearts))

    def set_total_hearts(self, total: int):
        """Establece el número total de corazones."""
        self.total_hearts = max(1, total)
        self.current_hearts = min(self.current_hearts, self.total_hearts)

    def save_to_file(self, filename: str):
        """Guarda el equipo en un archivo YAML."""
        data = {
            "pokemon": [p.to_dict() for p in self.pokemon],
            "hearts": {
                "total": self.total_hearts,
                "current": self.current_hearts
            }
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
                if data:
                    if "pokemon" in data:
                        for p_data in data["pokemon"]:
                            team.add_pokemon(Pokemon.from_dict(p_data))
                    if "hearts" in data:
                        team.set_total_hearts(data["hearts"]["total"])
                        team.set_hearts(data["hearts"]["current"])
        return team
