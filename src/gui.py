#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QPushButton, QLabel,
    QScrollArea, QFrame, QMenu, QAction, QDialog,
    QApplication, QMessageBox
)
from PyQt5.QtCore import Qt, QPoint, QMimeData, pyqtSignal, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QDrag, QPen

from models import Team, Pokemon
from pokeapi import PokeAPIClient
from assets import AssetManager

class PokemonWidget(QFrame):
    """Widget que representa un Pokemon en el equipo."""
    # Señales
    pokemon_dropped = pyqtSignal(object, int)  # (target_slot, pokemon_id)
    pokemon_edit_requested = pyqtSignal(object)  # (slot)
    pokemon_remove_requested = pyqtSignal(object)  # (slot)
    pokemon_drag_started = pyqtSignal(object)  # (slot)
    pokemon_drag_ended = pyqtSignal(object)  # (slot)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self.pokemon: Optional[Pokemon] = None
        self.sprite: Optional[QPixmap] = None
        self.setMinimumSize(100, 100)
        self.drag_start_position = QPoint()
        self.is_dragging = False
        self.is_drop_target = False
        
        # Botones de acción
        self.edit_button = QPushButton("✏️", self)
        self.edit_button.setFixedSize(20, 20)
        self.edit_button.clicked.connect(lambda: self.pokemon_edit_requested.emit(self))
        
        self.remove_button = QPushButton("❌", self)
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.clicked.connect(lambda: self.pokemon_remove_requested.emit(self))
        
        # Ocultar botones inicialmente
        self.edit_button.hide()
        self.remove_button.hide()

    def set_pokemon(self, pokemon: Pokemon, sprite: QPixmap):
        """Establece el Pokemon y su sprite."""
        self.pokemon = pokemon
        self.sprite = sprite
        if pokemon:
            self.edit_button.show()
            self.remove_button.show()
        else:
            self.edit_button.hide()
            self.remove_button.hide()
        self.update()

    def paintEvent(self, event):
        """Dibuja el Pokemon y su apodo."""
        super().paintEvent(event)
        if self.pokemon and self.sprite:
            painter = QPainter(self)
            
            # Dibujar fondo si es objetivo de drop
            if self.is_drop_target:
                painter.fillRect(self.rect(), QColor(200, 255, 200, 50))
            
            # Dibujar sprite
            sprite_rect = self.rect().adjusted(10, 10, -10, -30)
            painter.drawPixmap(sprite_rect, self.sprite)
            
            # Dibujar apodo
            if self.pokemon.nickname:
                painter.drawText(self.rect().adjusted(10, -20, -10, -10),
                               Qt.AlignBottom, self.pokemon.nickname)
            
            # Posicionar botones
            self.edit_button.move(self.width() - 25, 5)
            self.remove_button.move(self.width() - 25, 30)

    def mousePressEvent(self, event):
        """Inicia el arrastre del Pokemon."""
        if event.button() == Qt.LeftButton and self.pokemon:
            self.drag_start_position = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            self.is_dragging = True
            self.pokemon_drag_started.emit(self)

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
        
        # Crear una imagen de arrastre con el sprite
        drag_pixmap = QPixmap(self.sprite.size())
        drag_pixmap.fill(Qt.transparent)
        painter = QPainter(drag_pixmap)
        painter.drawPixmap(0, 0, self.sprite)
        painter.end()
        
        drag.setPixmap(drag_pixmap)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.exec_(Qt.MoveAction)

    def mouseReleaseEvent(self, event):
        """Finaliza el arrastre del Pokemon."""
        self.setCursor(Qt.ArrowCursor)
        if self.is_dragging:
            self.is_dragging = False
            self.pokemon_drag_ended.emit(self)

    def dragEnterEvent(self, event):
        """Acepta el evento de arrastre si contiene datos de Pokemon."""
        if event.mimeData().hasText():
            self.is_drop_target = True
            self.update()
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        """Maneja el evento de salida del arrastre."""
        self.is_drop_target = False
        self.update()

    def dropEvent(self, event):
        """Maneja el evento de soltar un Pokemon."""
        self.is_drop_target = False
        self.update()
        
        if event.mimeData().hasText():
            pokemon_id = int(event.mimeData().text())
            self.pokemon_dropped.emit(self, pokemon_id)
            event.acceptProposedAction()

    def enterEvent(self, event):
        """Muestra los botones al pasar el mouse por encima."""
        if self.pokemon:
            self.edit_button.show()
            self.remove_button.show()

    def leaveEvent(self, event):
        """Oculta los botones al salir el mouse."""
        if self.pokemon:
            self.edit_button.hide()
            self.remove_button.hide()

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
            self.pokemon_edit_requested.emit(self)
        elif action == delete_action:
            self.pokemon_remove_requested.emit(self)

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
            # Conectar señales
            slot.pokemon_dropped.connect(self.handle_pokemon_drop)
            slot.pokemon_edit_requested.connect(self.edit_pokemon)
            slot.pokemon_remove_requested.connect(self.remove_pokemon)
            slot.pokemon_drag_started.connect(self.handle_drag_start)
            slot.pokemon_drag_ended.connect(self.handle_drag_end)
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

    def handle_drag_start(self, slot: PokemonWidget):
        """Maneja el inicio del arrastre de un Pokemon."""
        self.logger.debug(f"Iniciando arrastre de {slot.pokemon.name}")

    def handle_drag_end(self, slot: PokemonWidget):
        """Maneja el fin del arrastre de un Pokemon."""
        self.logger.debug(f"Finalizando arrastre de {slot.pokemon.name}")

    def handle_pokemon_drop(self, target_slot: PokemonWidget, pokemon_id: int):
        """Maneja el intercambio de Pokemon entre slots."""
        source_slot = None
        for slot in self.team_slots:
            if slot.pokemon and slot.pokemon.id == pokemon_id:
                source_slot = slot
                break
        
        if source_slot and source_slot != target_slot:
            source_index = self.team_slots.index(source_slot)
            target_index = self.team_slots.index(target_slot)
            
            # Obtener los Pokemon y sprites
            source_pokemon = source_slot.pokemon
            source_sprite = source_slot.sprite
            target_pokemon = target_slot.pokemon
            target_sprite = target_slot.sprite
            
            # Actualizar el equipo
            if target_pokemon:  # Si el slot destino tiene un Pokemon, intercambiar
                self.team.pokemon[source_index], self.team.pokemon[target_index] = \
                    self.team.pokemon[target_index], self.team.pokemon[source_index]
                # Actualizar los slots
                source_slot.set_pokemon(target_pokemon, target_sprite)
                target_slot.set_pokemon(source_pokemon, source_sprite)
            else:  # Si el slot destino está vacío, mover
                if target_index >= len(self.team.pokemon):
                    # Añadir al final
                    self.team.pokemon.append(source_pokemon)
                    # Eliminar de la posición original
                    if source_index < target_index:
                        self.team.pokemon.pop(source_index)
                else:
                    # Insertar en la posición correcta
                    self.team.pokemon.insert(target_index, source_pokemon)
                    # Eliminar de la posición original
                    if source_index < target_index:
                        self.team.pokemon.pop(source_index)
                    else:
                        self.team.pokemon.pop(source_index + 1)
                
                # Actualizar los slots
                source_slot.set_pokemon(None, None)
                target_slot.set_pokemon(source_pokemon, source_sprite)
            
            self.logger.info(f"Pokemon {source_pokemon.name} movido a posición {target_index + 1}")
            self.update_team_display()

    def remove_pokemon(self, slot: PokemonWidget):
        """Elimina un Pokemon del equipo."""
        if not slot.pokemon:
            return
            
        # Guardar el nombre antes de eliminar
        pokemon_name = slot.pokemon.name
            
        # Confirmar eliminación
        reply = QMessageBox.question(
            self, 'Confirmar eliminación',
            f'¿Estás seguro de que quieres eliminar a {pokemon_name}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            index = self.team_slots.index(slot)
            self.team.pokemon.pop(index)
            self.update_team_display()
            self.logger.info(f"Pokemon {pokemon_name} eliminado del equipo")

    def edit_pokemon(self, slot: PokemonWidget):
        """Edita un Pokemon existente."""
        if not slot.pokemon:
            return
            
        # Obtener el índice del Pokemon en el equipo
        index = self.team_slots.index(slot)
        
        # Crear diálogo de edición
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Editar {slot.pokemon.name}")
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
            self.logger.info(f"Pokemon {slot.pokemon.name} actualizado")

    def clear_team(self):
        """Limpia todo el equipo."""
        self.team.pokemon.clear()
        self.update_team_display()
