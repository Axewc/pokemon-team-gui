# 🌟 Pokemon Team GUI Tracker

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white)
![REST API](https://img.shields.io/badge/REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-25A162?style=for-the-badge&logo=testcafe&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-2496ED?style=for-the-badge&logo=github-actions&logoColor=white)
![Codecov](https://img.shields.io/badge/Codecov-F01F7A?style=for-the-badge&logo=codecov&logoColor=white)

A lightweight and visually appealing desktop GUI application to manually create and manage your Pokemon team using dropdown menus. Built with Python, this app displays selected Pokemon and their nicknames with transparent PNG sprites like stickers on your desktop.

## 🚀 Features

- ✅ Manual selection of up to 6 Pokemon for your team
- ✅ Dropdown menus with Pokemon names powered by [PokeAPI](https://pokeapi.co/)
- ✅ Custom nickname input for each Pokemon
- ✅ Transparent window showing only the Pokemon sprites like stickers
- ✅ Live team preview with drag-and-drop sprite positions (planned)
- ✅ Save/load team configurations (planned)
- ✅ Heart counter system for tracking team status
- ✅ Responsive design that maintains sprite proportions

## 🚧 Tech Stack

- **Python 3.8+**
- **PyQt5** or **Tkinter** for GUI (PyQt preferred)
- **PokeAPI** for dynamic Pokemon data
- **Requests** for HTTP API calls
- **YAML** for configuration
- **pytest** for unit tests
- **GitHub Actions** for CI/CD
- **Codecov** for code coverage

## 📝 Project Structure

```
pokemon-team-gui/
├── README.md
├── requirements.txt
├── .gitignore
│
├── config/
│   └── settings.yaml            # Basic settings/config
│
├── src/
│   ├── __init__.py
│   ├── main.py                  # Entry point
│   ├── gui.py                   # GUI logic
│   ├── pokeapi.py               # PokeAPI handling
│   ├── models.py                # Pokemon/team models
│   └── assets.py                # Asset management (sprites)
│
├── assets/
│   └── sprites/                 # Transparent PNG sprites
│
├── tests/
│   ├── test_gui.py
│   ├── test_pokeapi.py
│   └── test_models.py
│
├── docs/
│   ├── testing.md
│   └── ci-cd.md
│
└── .github/
    └── workflows/
        └── ci.yml              # CI/CD configuration
```

## 🙌 Getting Started

### Requirements

- Python 3.8 or newer
- pip

### Installation

```bash
git clone https://github.com/yourname/pokemon-team-gui.git
cd pokemon-team-gui
pip install -r requirements.txt
```

### Run the App

```bash
python src/main.py
```

## 🔍 Roadmap

- [x] Initial GUI layout with dropdowns
- [x] Nickname field for each Pokemon
- [x] Transparent sticker-style display
- [ ] Drag-and-drop positioning
- [ ] Save/load team feature
- [ ] Optional integration with GBA/3DS emulator memory

## 🧪 Testing

El proyecto incluye una suite completa de pruebas unitarias y de integración:

```bash
# Ejecutar todas las pruebas
pytest tests/

# Ejecutar con cobertura
pytest tests/ --cov=src --cov-report=html
```

Ver la [documentación de pruebas](docs/testing.md) para más detalles.

## 🔄 CI/CD

El proyecto utiliza GitHub Actions para integración continua:

- Pruebas automáticas en múltiples versiones de Python
- Reportes de cobertura con Codecov
- Validación de código en cada push y pull request

Ver la [documentación de CI/CD](docs/ci-cd.md) para más detalles.

## 🙏 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## ✅ License

[MIT](LICENSE)

---
Made with ❤️ for Pokemon fans.
