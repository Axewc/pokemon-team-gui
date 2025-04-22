#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QScrollArea, QPushButton
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize

class HeartCounter(QWidget):
    """Widget personalizado para mostrar un contador con corazones."""
    def __init__(self, total_hearts: int = 20, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Cargar imágenes de corazones
        self.heart_full = QPixmap("assets/sprites/vida.png")
        self.heart_empty = QPixmap("assets/sprites/vidant.png")
        
        # Escalar imágenes si es necesario (más pequeñas que los sprites)
        self.heart_size = QSize(16, 16)  # Tamaño reducido
        self.heart_full = self.heart_full.scaled(self.heart_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.heart_empty = self.heart_empty.scaled(self.heart_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Contador y máximo
        self.count = total_hearts
        self.max_hearts = total_hearts
        
        # Crear contenedor principal
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)
        
        # Contador numérico estilizado
        self.number_label = QLabel(str(self.count))
        self.number_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                background-color: rgba(255, 255, 255, 0.8);
                border: 2px solid #cccccc;
                border-radius: 8px;
                padding: 2px 8px;
            }
        """)
        self.number_label.setMinimumWidth(60)
        self.number_label.setAlignment(Qt.AlignCenter)
        
        # Botones de control
        minus_button = QPushButton("-")
        minus_button.setFixedSize(20, 20)
        minus_button.clicked.connect(self.decrease_hearts)
        plus_button = QPushButton("+")
        plus_button.setFixedSize(20, 20)
        plus_button.clicked.connect(self.increase_hearts)
        
        # Crear scroll area para los corazones
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFixedHeight(20)  # Altura fija más pequeña
        
        # Contenedor para los corazones
        self.hearts_widget = QWidget(self.scroll_area)
        self.hearts_layout = QHBoxLayout(self.hearts_widget)
        self.hearts_layout.setSpacing(1)  # Menos espacio entre corazones
        self.hearts_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.hearts_widget)
        
        # Añadir widgets al layout principal
        main_layout.addWidget(self.number_label)
        main_layout.addWidget(minus_button)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(plus_button)
        self.layout.addWidget(main_widget)
        
        # Inicializar corazones
        self.heart_labels = []
        for _ in range(self.max_hearts):
            label = QLabel(self)
            label.setFixedSize(self.heart_size)  # Fijar tamaño del label
            label.setPixmap(self.heart_full)
            self.hearts_layout.addWidget(label)
            self.heart_labels.append(label)
            
        # Establecer tamaño máximo del widget
        total_width = (self.heart_size.width() + 1) * total_hearts + 44 + 70  # +44 para los botones, +70 para el número
        self.setMaximumWidth(total_width)

    def set_count(self, count: int):
        """Actualiza el contador y los corazones."""
        self.count = max(0, min(count, self.max_hearts))
        
        # Actualizar corazones
        for i, label in enumerate(self.heart_labels):
            label.setPixmap(self.heart_full if i < self.count else self.heart_empty)
        
        # Actualizar contador numérico
        self.number_label.setText(str(self.count))

    def get_count(self) -> int:
        """Obtiene el valor actual del contador."""
        return self.count

    def set_max_hearts(self, total_hearts: int):
        """Establece un nuevo número máximo de corazones."""
        old_max = self.max_hearts
        self.max_hearts = max(1, total_hearts)
        
        # Ajustar el contador actual si es necesario
        self.count = min(self.count, self.max_hearts)
        
        # Añadir o quitar corazones según sea necesario
        if total_hearts > old_max:
            # Añadir corazones
            for _ in range(total_hearts - old_max):
                label = QLabel(self)
                label.setFixedSize(self.heart_size)  # Fijar tamaño del label
                label.setPixmap(self.heart_empty)
                self.hearts_layout.addWidget(label)
                self.heart_labels.append(label)
        elif total_hearts < old_max:
            # Quitar corazones
            for _ in range(old_max - total_hearts):
                label = self.heart_labels.pop()
                label.deleteLater()
        
        # Actualizar visualización
        self.set_count(self.count)

    def decrease_hearts(self):
        """Reduce el contador de corazones en uno."""
        if self.count > 0:
            self.set_count(self.count - 1)

    def increase_hearts(self):
        """Aumenta el contador de corazones en uno."""
        if self.count < self.max_hearts:
            self.set_count(self.count + 1) 