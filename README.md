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

## 🎮 Quick Start

### For Users
Download the latest release and run the executable:
1. Get `Pokemon.Team.Tracker.zip` from the [releases page](https://github.com/yourusername/pokemon-team-gui/releases)
2. Extract and run `Pokemon Team Tracker.exe`
3. Check the [User Guide](docs/user_guide.md) for detailed instructions

### For Developers
Clone and set up the development environment:
```bash
git clone https://github.com/yourusername/pokemon-team-gui.git
cd pokemon-team-gui
pip install -r requirements.txt
python src/main.py
```

## 🚀 Features

- ✅ Manual selection of up to 6 Pokemon for your team
- ✅ Dropdown menus with Pokemon names powered by [PokeAPI](https://pokeapi.co/)
- ✅ Custom nickname input for each Pokemon
- ✅ Transparent window showing only the Pokemon sprites like stickers
- ✅ Live team preview with drag-and-drop sprite positions
- ✅ Save/load team configurations
- ✅ Heart counter system for tracking team status
- ✅ Responsive design that maintains sprite proportions
- ✅ Standalone executable for easy distribution

## 🚧 Tech Stack

- **Python 3.8+** - Base language
- **PyQt5** - GUI framework
- **PokeAPI** - Pokemon data source
- **Requests** - HTTP client
- **YAML** - Configuration
- **pytest** - Testing
- **GitHub Actions** - CI/CD
- **Codecov** - Code coverage
- **PyInstaller** - Executable creation

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
│   ├── pokeapi.py              # PokeAPI handling
│   ├── models.py               # Pokemon/team models
│   └── assets.py               # Asset management
│
├── assets/
│   ├── sprites/                # Pokemon sprites
│   ├── icon.ico               # App icon
│   └── icon.png               # App icon (PNG)
│
├── tests/
│   ├── test_gui.py
│   ├── test_pokeapi.py
│   └── test_models.py
│
├── docs/
│   ├── testing.md             # Testing documentation
│   ├── ci-cd.md              # CI/CD documentation
│   └── user_guide.md         # User manual
│
└── scripts/
    └── create_icon.py        # Icon generation script
```

## 📚 Documentation

- [User Guide](docs/user_guide.md) - For end users
- [Testing Documentation](docs/testing.md) - Test coverage and procedures
- [CI/CD Documentation](docs/ci-cd.md) - Continuous Integration setup
- [Architecture](ARCHITECTURE.md) - System design and patterns

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Generate coverage report:
```bash
pytest tests/ --cov=src --cov-report=html
```

## 📦 Building

Create a standalone executable:
```bash
# Install requirements
pip install -r requirements.txt

# Generate icon (if needed)
python scripts/create_icon.py

# Build executable
pyinstaller pokemon_team_tracker.spec
```

The executable will be created in `dist/Pokemon Team Tracker/`.

## 🔄 CI/CD

The project uses GitHub Actions for:
- Automated testing
- Code coverage reporting
- Build verification
- Release automation

See [CI/CD documentation](docs/ci-cd.md) for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

[MIT](LICENSE)

---
Made with ❤️ for Pokemon fans.
