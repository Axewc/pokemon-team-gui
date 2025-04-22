# Documentación de Drag and Drop en Pokemon Team GUI

## Casos de Uso

### 1. Reordenamiento de Pokemon

- **Descripción**: El usuario puede reordenar los Pokemon en su equipo arrastrándolos a diferentes posiciones.
- **Reglas**:
  - Solo se puede arrastrar un Pokemon a una posición vacía o intercambiar con otro Pokemon
  - No se puede arrastrar un Pokemon fuera de los límites del equipo
  - El orden de los Pokemon se mantiene en el archivo de guardado
  - Los sprites mantienen sus proporciones durante el arrastre
  - Feedback visual durante el arrastre y al soltar

### 2. Edición Rápida

- **Descripción**: Múltiples formas de editar un Pokemon:
  - Botón de edición contextual (✏️)
  - Menú contextual (clic derecho)
  - Doble clic en el Pokemon
- **Reglas**:
  - El Pokemon mantiene su posición durante la edición
  - Los cambios se aplican inmediatamente
  - La interfaz se actualiza automáticamente
  - El apodo se centra debajo del sprite

### 3. Eliminación de Pokemon

- **Descripción**: Múltiples formas de eliminar un Pokemon:
  - Botón de eliminación contextual (❌)
  - Menú contextual (clic derecho)
  - Opción en el diálogo de edición
- **Reglas**:
  - Se requiere confirmación antes de eliminar
  - No afecta al contador de corazones
  - Se actualiza automáticamente la visualización del equipo

## Reglas de Negocio

### 1. Validaciones

- No se puede arrastrar un Pokemon si el equipo está vacío
- No se puede arrastrar un Pokemon a una posición inválida
- Se debe mantener el límite de 6 Pokemon en el equipo
- Los corazones son independientes del equipo

### 2. Persistencia

- Los cambios en el orden se guardan automáticamente
- Se guarda el estado de los corazones
- Se mantiene el historial de cambios para posibles deshacer
- Se respeta el formato de guardado YAML

### 3. Interfaz de Usuario

- Feedback visual durante el arrastre
- Indicadores de posición válida/inválida
- Animaciones suaves durante el movimiento
- Sprites proporcionalmente escalados
- Diseño responsivo que mantiene proporciones
- Botones contextuales que aparecen al hover

### 4. Rendimiento

- Caché de sprites para mejor rendimiento
- Optimización de memoria durante el arrastre
- Manejo eficiente de eventos de mouse
- Escalado eficiente de imágenes

## Implementación Técnica

### 1. Eventos de Mouse

```python
def mousePressEvent(self, event):
    # Inicia el arrastre
    if event.button() == Qt.LeftButton and self.pokemon:
        self.drag_start_position = event.pos()
        self.setCursor(Qt.ClosedHandCursor)
        self.is_dragging = True
        self.pokemon_drag_started.emit(self)

def mouseMoveEvent(self, event):
    # Maneja el movimiento con comprobación de distancia mínima
    if not (event.buttons() & Qt.LeftButton) or not self.pokemon:
        return
    if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
        return
    self.start_drag()

def mouseReleaseEvent(self, event):
    # Finaliza el arrastre
    self.setCursor(Qt.ArrowCursor)
    if self.is_dragging:
        self.is_dragging = False
        self.pokemon_drag_ended.emit(self)
```

### 2. Eventos de Arrastre

```python
def dragEnterEvent(self, event):
    # Valida si se puede soltar y muestra feedback visual
    if event.mimeData().hasText():
        self.is_drop_target = True
        self.update()
        event.acceptProposedAction()

def dropEvent(self, event):
    # Maneja el soltar con actualización visual
    self.is_drop_target = False
    self.update()
    if event.mimeData().hasText():
        pokemon_id = int(event.mimeData().text())
        self.pokemon_dropped.emit(self, pokemon_id)
        event.acceptProposedAction()
```

### 3. Renderizado Visual

```python
def paintEvent(self, event):
    # Dibuja el Pokemon manteniendo proporciones
    if self.pokemon and self.sprite:
        painter = QPainter(self)
        
        # Feedback visual para drop
        if self.is_drop_target:
            painter.fillRect(self.rect(), QColor(200, 255, 200, 50))
        
        # Calcular y mantener proporciones
        widget_rect = self.rect().adjusted(10, 10, -10, -30)
        sprite_rect = self.sprite.rect()
        scaled_size = sprite_rect.size()
        scaled_size.scale(widget_rect.size(), Qt.KeepAspectRatio)
        
        # Centrar sprite
        x = widget_rect.x() + (widget_rect.width() - scaled_size.width()) / 2
        y = widget_rect.y() + (widget_rect.height() - scaled_size.height()) / 2
        
        # Dibujar sprite y apodo
        target_rect = QRect(int(x), int(y), scaled_size.width(), scaled_size.height())
        painter.drawPixmap(target_rect, self.sprite)
        
        if self.pokemon.nickname:
            painter.drawText(self.rect().adjusted(10, -25, -10, -5),
                           Qt.AlignBottom | Qt.AlignHCenter,
                           self.pokemon.nickname)
```

## Mejoras Futuras

1. **Animaciones**:
   - Efectos de transición suaves
   - Feedback visual mejorado
   - Indicadores de posición
   - Animaciones de corazones

2. **Funcionalidades**:
   - Deshacer/Rehacer cambios
   - Arrastrar múltiples Pokemon
   - Atajos de teclado
   - Modos de visualización alternativos

3. **Optimizaciones**:
   - Mejor manejo de memoria
   - Caché más eficiente
   - Reducción de eventos innecesarios
   - Mejoras en el escalado de sprites

## Consideraciones de Seguridad

1. **Validación de Datos**:
   - Verificación de tipos
   - Sanitización de entrada
   - Manejo de errores
   - Validación de estados de corazones

2. **Persistencia**:
   - Backups automáticos
   - Recuperación de errores
   - Validación de archivos
   - Integridad de datos

3. **Rendimiento**:
   - Límites de memoria
   - Optimización de recursos
   - Manejo de concurrencia
   - Gestión eficiente de layouts
