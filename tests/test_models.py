#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from pathlib import Path
import tempfile
import yaml
from src.models import Pokemon, Team

class TestPokemon(unittest.TestCase):
    """Pruebas para la clase Pokemon."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.pokemon_data = {
            "id": 1,
            "name": "Bulbasaur",
            "nickname": "Bulby",
            "sprite_url": "https://example.com/sprite.png",
            "position_x": 10,
            "position_y": 20
        }
        self.pokemon = Pokemon(**self.pokemon_data)

    def test_pokemon_creation(self):
        """Prueba la creación de un Pokemon con todos los atributos."""
        self.assertEqual(self.pokemon.id, 1)
        self.assertEqual(self.pokemon.name, "Bulbasaur")
        self.assertEqual(self.pokemon.nickname, "Bulby")
        self.assertEqual(self.pokemon.sprite_url, "https://example.com/sprite.png")
        self.assertEqual(self.pokemon.position_x, 10)
        self.assertEqual(self.pokemon.position_y, 20)

    def test_pokemon_default_values(self):
        """Prueba la creación de un Pokemon con valores por defecto."""
        pokemon = Pokemon(id=1, name="Bulbasaur")
        self.assertEqual(pokemon.nickname, "")
        self.assertEqual(pokemon.sprite_url, "")
        self.assertEqual(pokemon.position_x, 0)
        self.assertEqual(pokemon.position_y, 0)

    def test_pokemon_to_dict(self):
        """Prueba la conversión de Pokemon a diccionario."""
        pokemon_dict = self.pokemon.to_dict()
        self.assertEqual(pokemon_dict, self.pokemon_data)

    def test_pokemon_from_dict(self):
        """Prueba la creación de Pokemon desde diccionario."""
        pokemon = Pokemon.from_dict(self.pokemon_data)
        self.assertEqual(pokemon.id, self.pokemon.id)
        self.assertEqual(pokemon.name, self.pokemon.name)
        self.assertEqual(pokemon.nickname, self.pokemon.nickname)
        self.assertEqual(pokemon.sprite_url, self.pokemon.sprite_url)
        self.assertEqual(pokemon.position_x, self.pokemon.position_x)
        self.assertEqual(pokemon.position_y, self.pokemon.position_y)

class TestTeam(unittest.TestCase):
    """Pruebas para la clase Team."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.team = Team()
        self.pokemon = Pokemon(id=1, name="Bulbasaur", nickname="Bulby")

    def test_team_initial_state(self):
        """Prueba el estado inicial del equipo."""
        self.assertEqual(len(self.team.pokemon), 0)
        self.assertEqual(self.team.max_size, 6)
        self.assertEqual(self.team.total_hearts, 20)
        self.assertEqual(self.team.current_hearts, 20)

    def test_add_pokemon(self):
        """Prueba añadir Pokemon al equipo."""
        # Añadir primer Pokemon
        self.assertTrue(self.team.add_pokemon(self.pokemon))
        self.assertEqual(len(self.team.pokemon), 1)
        
        # Llenar el equipo
        for i in range(2, 7):
            pokemon = Pokemon(id=i, name=f"Pokemon{i}")
            self.assertTrue(self.team.add_pokemon(pokemon))
        
        # Intentar añadir cuando está lleno
        extra_pokemon = Pokemon(id=7, name="Extra")
        self.assertFalse(self.team.add_pokemon(extra_pokemon))

    def test_remove_pokemon(self):
        """Prueba eliminar Pokemon del equipo."""
        self.team.add_pokemon(self.pokemon)
        removed = self.team.remove_pokemon(0)
        self.assertEqual(removed, self.pokemon)
        self.assertEqual(len(self.team.pokemon), 0)
        
        # Intentar eliminar de índice inválido
        self.assertIsNone(self.team.remove_pokemon(0))
        self.assertIsNone(self.team.remove_pokemon(-1))

    def test_heart_management(self):
        """Prueba la gestión de corazones."""
        # Probar establecer corazones actuales
        self.team.set_hearts(15)
        self.assertEqual(self.team.current_hearts, 15)
        
        # Probar límites
        self.team.set_hearts(25)  # Más que el máximo
        self.assertEqual(self.team.current_hearts, 20)
        
        self.team.set_hearts(-5)  # Menos que cero
        self.assertEqual(self.team.current_hearts, 0)
        
        # Probar cambiar total de corazones
        self.team.set_total_hearts(10)
        self.assertEqual(self.team.total_hearts, 10)
        self.assertEqual(self.team.current_hearts, 0)  # Mantiene el valor actual si es válido
        
        self.team.set_hearts(10)
        self.team.set_total_hearts(5)  # Reducir máximo
        self.assertEqual(self.team.current_hearts, 5)  # Ajusta el actual si excede el nuevo máximo

    def test_save_load_team(self):
        """Prueba guardar y cargar el equipo."""
        # Preparar equipo con datos
        self.team.add_pokemon(self.pokemon)
        self.team.set_hearts(15)
        self.team.set_total_hearts(25)
        
        # Guardar a archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as tmp:
            self.team.save_to_file(tmp.name)
            
            # Cargar en nuevo equipo
            loaded_team = Team.load_from_file(tmp.name)
            
            # Verificar datos
            self.assertEqual(len(loaded_team.pokemon), 1)
            self.assertEqual(loaded_team.pokemon[0].name, "Bulbasaur")
            self.assertEqual(loaded_team.current_hearts, 15)
            self.assertEqual(loaded_team.total_hearts, 25)
        
        # Limpiar
        Path(tmp.name).unlink()

    def test_load_nonexistent_file(self):
        """Prueba cargar desde un archivo que no existe."""
        team = Team.load_from_file("nonexistent.yaml")
        self.assertEqual(len(team.pokemon), 0)
        self.assertEqual(team.current_hearts, 20)
        self.assertEqual(team.total_hearts, 20)

if __name__ == '__main__':
    unittest.main() 