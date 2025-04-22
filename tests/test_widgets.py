#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.widgets import HeartCounter

class TestHeartCounter(unittest.TestCase):
    """Pruebas para el widget HeartCounter."""
    
    @classmethod
    def setUpClass(cls):
        """Crear instancia de QApplication para las pruebas."""
        cls.app = QApplication([])

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.counter = HeartCounter(total_hearts=20)

    def test_initial_state(self):
        """Prueba el estado inicial del contador."""
        self.assertEqual(self.counter.get_count(), 20)
        self.assertEqual(self.counter.max_hearts, 20)
        self.assertEqual(len(self.counter.heart_labels), 20)
        self.assertEqual(self.counter.number_label.text(), "20")

    def test_decrease_hearts(self):
        """Prueba la reducción de corazones."""
        initial = self.counter.get_count()
        self.counter.decrease_hearts()
        self.assertEqual(self.counter.get_count(), initial - 1)
        self.assertEqual(self.counter.number_label.text(), str(initial - 1))

        # Probar límite inferior
        for _ in range(25):  # Más que el total de corazones
            self.counter.decrease_hearts()
        self.assertEqual(self.counter.get_count(), 0)
        self.assertEqual(self.counter.number_label.text(), "0")

    def test_increase_hearts(self):
        """Prueba el aumento de corazones."""
        self.counter.set_count(0)  # Empezar desde 0
        self.counter.increase_hearts()
        self.assertEqual(self.counter.get_count(), 1)
        self.assertEqual(self.counter.number_label.text(), "1")

        # Probar límite superior
        for _ in range(25):  # Más que el total de corazones
            self.counter.increase_hearts()
        self.assertEqual(self.counter.get_count(), 20)
        self.assertEqual(self.counter.number_label.text(), "20")

    def test_set_count(self):
        """Prueba establecer el contador directamente."""
        test_values = [-5, 0, 10, 20, 25]
        expected = [0, 0, 10, 20, 20]  # Valores esperados después de la validación
        
        for test, expect in zip(test_values, expected):
            self.counter.set_count(test)
            self.assertEqual(self.counter.get_count(), expect)
            self.assertEqual(self.counter.number_label.text(), str(expect))

    def test_set_max_hearts(self):
        """Prueba cambiar el máximo de corazones."""
        # Reducir máximo
        self.counter.set_max_hearts(10)
        self.assertEqual(self.counter.max_hearts, 10)
        self.assertEqual(len(self.counter.heart_labels), 10)
        self.assertEqual(self.counter.get_count(), 10)  # Se ajusta al nuevo máximo
        
        # Aumentar máximo
        self.counter.set_max_hearts(15)
        self.assertEqual(self.counter.max_hearts, 15)
        self.assertEqual(len(self.counter.heart_labels), 15)
        self.assertEqual(self.counter.get_count(), 10)  # Mantiene el valor actual

    def test_visual_update(self):
        """Prueba que los corazones se actualizan visualmente."""
        self.counter.set_count(10)
        
        # Verificar que los primeros 10 corazones están llenos
        for i in range(10):
            self.assertEqual(
                self.counter.heart_labels[i].pixmap().cacheKey(),
                self.counter.heart_full.cacheKey()
            )
        
        # Verificar que los últimos 10 corazones están vacíos
        for i in range(10, 20):
            self.assertEqual(
                self.counter.heart_labels[i].pixmap().cacheKey(),
                self.counter.heart_empty.cacheKey()
            )

if __name__ == '__main__':
    unittest.main() 