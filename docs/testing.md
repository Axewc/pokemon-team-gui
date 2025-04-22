# 🧪 Documentación de Pruebas

## 📚 Resumen

Este documento describe las pruebas unitarias implementadas para el Pokemon Team GUI Tracker.

## 🔍 Estructura de Pruebas

### TestPokemon

Pruebas para la clase `Pokemon` ubicadas en `tests/test_models.py`.

#### Métodos de Prueba

- `test_pokemon_creation`: Verifica la creación de un Pokémon con todos los atributos.
- `test_pokemon_default_values`: Comprueba los valores por defecto al crear un Pokémon.
- `test_pokemon_to_dict`: Valida la conversión de un Pokémon a diccionario.
- `test_pokemon_from_dict`: Prueba la creación de un Pokémon desde un diccionario.

### TestTeam

Pruebas para la clase `Team` ubicadas en `tests/test_models.py`.

#### Métodos de Prueba

- `test_team_initial_state`: Verifica el estado inicial del equipo.
- `test_add_pokemon`: Prueba la adición de Pokémon al equipo.
- `test_remove_pokemon`: Valida la eliminación de Pokémon del equipo.
- `test_heart_management`: Comprueba la gestión de corazones.
- `test_save_load_team`: Prueba las funciones de guardado y carga del equipo.
- `test_load_nonexistent_file`: Verifica el comportamiento con archivos inexistentes.

### TestHeartCounter

Pruebas para el widget `HeartCounter` ubicadas en `tests/test_widgets.py`.

#### Métodos de Prueba

- `test_initial_state`: Verifica el estado inicial del contador.
- `test_decrease_hearts`: Prueba la reducción de corazones.
- `test_increase_hearts`: Valida el incremento de corazones.
- `test_set_count`: Comprueba el establecimiento directo del contador.
- `test_set_max_hearts`: Prueba el cambio del máximo de corazones.
- `test_visual_update`: Verifica la actualización visual de los corazones.

## 🚀 Ejecución de Pruebas

### Localmente

```bash
# Instalar dependencias
pip install pytest pytest-cov pytest-qt

# Ejecutar todas las pruebas
pytest tests/

# Ejecutar con cobertura
pytest tests/ --cov=src --cov-report=html
```

### Requisitos del Sistema

- Python 3.8 o superior
- PyQt5
- pytest
- pytest-cov
- pytest-qt

## 📊 Cobertura de Código

Las pruebas están configuradas para generar informes de cobertura usando pytest-cov. Los informes se pueden generar en varios formatos:

- HTML: `pytest --cov=src --cov-report=html`
- XML: `pytest --cov=src --cov-report=xml`
- Terminal: `pytest --cov=src` 