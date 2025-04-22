#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QPushButton, QLabel,
    QScrollArea, QFrame, QMenu, QAction
)
from PyQt5.QtCore import Qt, QPoint, QMimeData, QDrag
from PyQt5.QtGui import QPixmap, QPainter, QColor

from models import Team, Pokemon
from pokeapi import PokeAPIClient
from assets import AssetManager

class PokemonWidget(QFrame):
    """Widget que representa un Pokemon en el equipo."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.pokemon: Optional[Pokemon] = None
        self.sprite: Optional[QPixmap] = None
        self.setMinimumSize(100, 100)
        self.drag_start_position = QPoint()

    def set_pokemon(self, pokemon: Pokemon, sprite: QPixmap):
        """Establece el Pokemon y su sprite."""
        self.pokemon = pokemon
        self.sprite = sprite
        self.update()

    def paintEvent(self, event):
        """Dibuja el Pokemon y su apodo."""
        super().paintEvent(event)
        if self.pokemon and self.sprite:
            painter = QPainter(self)
            # Dibujar sprite
            sprite_rect = self.rect().adjusted(10, 10, -10, -30)
            painter.drawPixmap(sprite_rect, self.sprite)
            # Dibujar apodo
            if self.pokemon.nickname:
                painter.drawText(self.rect().adjusted(10, -20, -10, -10),
                               Qt.AlignCenter, self.pokemon.nickname)

    def mousePressEvent(self, event):
        """Inicia el arrastre del Pokemon."""
        if event.button() == Qt.LeftButton and self.pokemon:
            self.drag_start_position = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        """Maneja el arrastre del Pokemon."""
        if not (event.buttons() & Qt.LeftButton):
            return
        if not self.pokemon:
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self.pokemon.id))
        drag.setMimeData(mime_data)
        drag.setPixmap(self.sprite)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.exec_(Qt.MoveAction)

    def mouseReleaseEvent(self, event):
        """Finaliza el arrastre del Pokemon."""
        self.setCursor(Qt.ArrowCursor)

    def dragEnterEvent(self, event):
        """Acepta el evento de arrastre si contiene datos de Pokemon."""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Maneja el evento de soltar un Pokemon."""
        if event.mimeData().hasText():
            pokemon_id = int(event.mimeData().text())
            # Notificar al padre para manejar el intercambio
            self.parent().handle_pokemon_drop(self, pokemon_id)
            event.acceptProposedAction()

    def contextMenuEvent(self, event):
        """Muestra el menú contextual para editar o eliminar el Pokemon."""
        if not self.pokemon:
            return

        menu = QMenu(self)
        edit_action = QAction("Editar", self)
        delete_action = QAction("Eliminar", self)
        
        menu.addAction(edit_action)
        menu.addAction(delete_action)
        
        action = menu.exec_(event.globalPos())
        if action == edit_action:
            self.parent().edit_pokemon(self)
        elif action == delete_action:
            self.parent().remove_pokemon(self)

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""
    def __init__(self, team: Team, api_client: PokeAPIClient, asset_manager: AssetManager):
        super().__init__()
        self.team = team
        self.api_client = api_client
        self.asset_manager = asset_manager
        self.logger = logging.getLogger(__name__)
        
        self.setWindowTitle("Pokemon Team GUI")
        self.setup_ui()
        self.load_pokemon_list()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Área de selección
        selection_widget = QWidget()
        selection_layout = QHBoxLayout(selection_widget)
        
        # ComboBox para selección de Pokemon
        self.pokemon_combo = QComboBox()
        selection_layout.addWidget(QLabel("Pokemon:"))
        selection_layout.addWidget(self.pokemon_combo)
        
        # Campo para apodo
        self.nickname_edit = QLineEdit()
        selection_layout.addWidget(QLabel("Apodo:"))
        selection_layout.addWidget(self.nickname_edit)
        
        # Botones de acción
        add_button = QPushButton("Añadir")
        add_button.clicked.connect(self.add_pokemon)
        selection_layout.addWidget(add_button)
        
        clear_button = QPushButton("Limpiar Equipo")
        clear_button.clicked.connect(self.clear_team)
        selection_layout.addWidget(clear_button)
        
        layout.addWidget(selection_widget)
        
        # Área de equipo
        team_widget = QWidget()
        team_layout = QHBoxLayout(team_widget)
        
        # Crear widgets para cada slot del equipo
        self.team_slots = []
        for _ in range(6):
            slot = PokemonWidget()
            team_layout.addWidget(slot)
            self.team_slots.append(slot)
        
        layout.addWidget(team_widget)
        
        # Botones de acción
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        
        save_button = QPushButton("Guardar Equipo")
        save_button.clicked.connect(self.save_team)
        action_layout.addWidget(save_button)
        
        load_button = QPushButton("Cargar Equipo")
        load_button.clicked.connect(self.load_team)
        action_layout.addWidget(load_button)
        
        layout.addWidget(action_widget)

    def load_pokemon_list(self):
        """Carga la lista de Pokemon en el ComboBox."""
        pokemon_list = self.api_client.get_pokemon_list()
        for pokemon in pokemon_list:
            self.pokemon_combo.addItem(pokemon['name'].title(), pokemon['url'])

    def add_pokemon(self):
        """Añade un Pokemon al equipo."""
        if len(self.team.pokemon) >= 6:
            self.logger.warning("El equipo está lleno")
            return
        
        current_index = self.pokemon_combo.currentIndex()
        if current_index < 0:
            return
        
        pokemon_url = self.pokemon_combo.currentData()
        pokemon_id = int(pokemon_url.split('/')[-2])
        
        # Crear nuevo Pokemon
        pokemon = Pokemon(
            id=pokemon_id,
            name=self.pokemon_combo.currentText(),
            nickname=self.nickname_edit.text()
        )
        
        # Obtener sprite
        sprite_url = self.api_client.get_sprite_url(pokemon_id)
        if sprite_url:
            sprite = self.asset_manager.get_sprite(sprite_url)
            if sprite:
                pokemon.sprite_url = sprite_url
                self.team.add_pokemon(pokemon)
                self.update_team_display()

    def update_team_display(self):
        """Actualiza la visualización del equipo."""
        for i, slot in enumerate(self.team_slots):
            if i < len(self.team.pokemon):
                pokemon = self.team.pokemon[i]
                sprite = self.asset_manager.get_sprite(pokemon.sprite_url)
                if sprite:
                    slot.set_pokemon(pokemon, sprite)
            else:
                slot.set_pokemon(None, None)

    def save_team(self):
        """Guarda el equipo actual."""
        self.team.save_to_file("saves/team.yaml")
        self.logger.info("Equipo guardado")

    def load_team(self):
        """Carga un equipo guardado."""
        self.team = Team.load_from_file("saves/team.yaml")
        self.update_team_display()
        self.logger.info("Equipo cargado")

    def handle_pokemon_drop(self, target_slot: PokemonWidget, pokemon_id: int):
        """Maneja el intercambio de Pokemon entre slots."""
        source_slot = None
        for slot in self.team_slots:
            if slot.pokemon and slot.pokemon.id == pokemon_id:
                source_slot = slot
                break
        
        if source_slot and source_slot != target_slot:
            # Intercambiar Pokemon
            source_pokemon = source_slot.pokemon
            target_pokemon = target_slot.pokemon
            
            source_slot.set_pokemon(target_pokemon, target_slot.sprite)
            target_slot.set_pokemon(source_pokemon, source_slot.sprite)
            
            # Actualizar el equipo
            source_index = self.team_slots.index(source_slot)
            target_index = self.team_slots.index(target_slot)
            self.team.pokemon[source_index], self.team.pokemon[target_index] = \
                self.team.pokemon[target_index], self.team.pokemon[source_index]

    def edit_pokemon(self, slot: PokemonWidget):
        """Edita un Pokemon existente."""
        if not slot.pokemon:
            return
            
        # Obtener el índice del Pokemon en el equipo
        index = self.team_slots.index(slot)
        
        # Crear diálogo de edición
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Pokemon")
        layout = QVBoxLayout(dialog)
        
        # Campo para apodo
        nickname_edit = QLineEdit(slot.pokemon.nickname)
        layout.addWidget(QLabel("Apodo:"))
        layout.addWidget(nickname_edit)
        
        # Botones
        buttons = QHBoxLayout()
        save_button = QPushButton("Guardar")
        cancel_button = QPushButton("Cancelar")
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
        # Conectar señales
        save_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        if dialog.exec_() == QDialog.Accepted:
            # Actualizar el Pokemon
            self.team.pokemon[index].nickname = nickname_edit.text()
            self.update_team_display()

    def remove_pokemon(self, slot: PokemonWidget):
        """Elimina un Pokemon del equipo."""
        if not slot.pokemon:
            return
            
        index = self.team_slots.index(slot)
        self.team.pokemon.pop(index)
        self.update_team_display()

    def clear_team(self):
        """Limpia todo el equipo."""
        self.team.pokemon.clear()
        self.update_team_display()
