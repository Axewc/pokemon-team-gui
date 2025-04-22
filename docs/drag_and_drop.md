# Documentación de Drag and Drop en Pokemon Team GUI

## Casos de Uso

### 1. Reordenamiento de Pokemon

- **Descripción**: El usuario puede reordenar los Pokemon en su equipo arrastrándolos a diferentes posiciones.
- **Reglas**:
  - Solo se puede arrastrar un Pokemon a una posición vacía o intercambiar con otro Pokemon
  - No se puede arrastrar un Pokemon fuera de los límites del equipo
  - El orden de los Pokemon se mantiene en el archivo de guardado

### 2. Edición Rápida

- **Descripción**: Al arrastrar un Pokemon fuera de la ventana principal, se abre el diálogo de edición.
- **Reglas**:
  - El Pokemon se mantiene en su posición original si se cancela la edición
  - Los cambios se aplican inmediatamente al soltar el Pokemon
  - Se puede editar el apodo y otros atributos durante el arrastre

### 3. Eliminación por Arrastre

- **Descripción**: Al arrastrar un Pokemon a un área específica de eliminación, se elimina del equipo.
- **Reglas**:
  - Se requiere confirmación antes de eliminar
  - El Pokemon se elimina permanentemente del equipo
  - Se actualiza automáticamente la visualización del equipo

## Reglas de Negocio

### 1. Validaciones

- No se puede arrastrar un Pokemon si el equipo está vacío
- No se puede arrastrar un Pokemon a una posición inválida
- Se debe mantener el límite de 6 Pokemon en el equipo

### 2. Persistencia

- Los cambios en el orden se guardan automáticamente
- Se mantiene el historial de cambios para posibles deshacer
- Se respeta el formato de guardado YAML

### 3. Interfaz de Usuario

- Feedback visual durante el arrastre
- Indicadores de posición válida/inválida
- Animaciones suaves durante el movimiento

### 4. Rendimiento

- Caché de sprites para mejor rendimiento
- Optimización de memoria durante el arrastre
- Manejo eficiente de eventos de mouse

## Implementación Técnica

### 1. Eventos de Mouse

```python
def mousePressEvent(self, event):
    # Inicia el arrastre
    if event.button() == Qt.LeftButton:
        self.drag_start_position = event.pos()

def mouseMoveEvent(self, event):
    # Maneja el movimiento
    if (event.pos() - self.drag_start_position).manhattanLength() > QApplication.startDragDistance():
        self.start_drag()

def mouseReleaseEvent(self, event):
    # Finaliza el arrastre
    self.end_drag()
```

### 2. Eventos de Arrastre

```python
def dragEnterEvent(self, event):
    # Valida si se puede soltar
    if self.is_valid_drop_target(event):
        event.acceptProposedAction()

def dropEvent(self, event):
    # Maneja el soltar
    if self.is_valid_drop_target(event):
        self.handle_drop(event)
```

### 3. Validaciones

```python
def is_valid_drop_target(self, event):
    # Verifica si la posición es válida
    return (
        self.is_within_bounds(event.pos()) and
        not self.is_team_full() and
        self.is_valid_pokemon(event.mimeData())
    )
```

## Mejoras Futuras

1. **Animaciones**:
   - Efectos de transición suaves
   - Feedback visual mejorado
   - Indicadores de posición

2. **Funcionalidades**:
   - Deshacer/Rehacer cambios
   - Arrastrar múltiples Pokemon
   - Atajos de teclado

3. **Optimizaciones**:
   - Mejor manejo de memoria
   - Caché más eficiente
   - Reducción de eventos innecesarios

## Consideraciones de Seguridad

1. **Validación de Datos**:
   - Verificación de tipos
   - Sanitización de entrada
   - Manejo de errores

2. **Persistencia**:
   - Backups automáticos
   - Recuperación de errores
   - Validación de archivos

3. **Rendimiento**:
   - Límites de memoria
   - Optimización de recursos
   - Manejo de concurrencia 