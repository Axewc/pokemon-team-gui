# 🌟 Pokemon Team GUI Tracker

A lightweight and visually appealing desktop GUI application to manually create and manage your Pokemon team using dropdown menus. Built with Python, this app displays selected Pokemon and their nicknames with transparent PNG sprites like stickers on your desktop.

## 🚀 Features

- ✅ Manual selection of up to 6 Pokemon for your team
- ✅ Dropdown menus with Pokemon names powered by [PokeAPI](https://pokeapi.co/)
- ✅ Custom nickname input for each Pokemon
- ✅ Transparent window showing only the Pokemon sprites like stickers
- ✅ Live team preview with drag-and-drop sprite positions (planned)
- ✅ Save/load team configurations (planned)

## 🚧 Tech Stack

- **Python 3.8+**
- **PyQt5** or **Tkinter** for GUI (PyQt preferred)
- **PokeAPI** for dynamic Pokemon data
- **Requests** for HTTP API calls
- **YAML** for configuration

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
└── tests/
    ├── test_gui.py
    └── test_pokeapi.py
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

## 🙏 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## ✅ License

[MIT](LICENSE)

---
Made with ❤️ for Pokemon fans.
