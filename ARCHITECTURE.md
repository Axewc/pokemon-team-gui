# Arquitectura del Sistema Pokemon Team GUI

## Patrones de Diseño Utilizados

### 1. Modelo-Vista-Controlador (MVC)

- **Modelo**: Clases en `models.py` que representan la lógica de negocio y datos
  - Clase `Team` con gestión de corazones y persistencia
  - Clase `Pokemon` con atributos extendidos
- **Vista**: Interfaz gráfica implementada en `gui.py` y `widgets.py`
  - Widgets personalizados para mejor modularidad
  - Sistema de corazones con contador visual
- **Controlador**: Lógica de control en `main.py` que coordina modelo y vista

### 2. Singleton

- Implementado en `pokeapi.py` para manejar las llamadas a la API de manera eficiente
- Asegura una única instancia del cliente API

### 3. Factory Method

- Utilizado para crear instancias de Pokemon con diferentes configuraciones
- Facilita la creación de objetos sin exponer la lógica de creación

### 4. Observer Pattern

- Implementado en los widgets personalizados para notificación de eventos
- Señales PyQt para comunicación entre componentes

## Estructura del Sistema

### Componentes Principales

1. **GUI (PyQt5)**
   - Ventana principal con diseño responsivo
   - Menús desplegables para selección de Pokemon
   - Campos de texto para apodos
   - Sistema de arrastrar y soltar para posicionamiento
   - Contador de corazones interactivo
   - Diseño adaptable a diferentes tamaños de ventana

2. **API Client (PokeAPI)**
   - Cliente singleton para llamadas a la API
   - Caché de datos para optimizar rendimiento
   - Manejo de errores y reintentos

3. **Modelo de Datos**
   - Clase Pokemon con atributos básicos y posicionamiento
   - Clase Team para gestionar el equipo y corazones
   - Serialización/deserialización YAML mejorada

4. **Gestión de Assets**
   - Sistema de caché de sprites
   - Carga asíncrona de imágenes
   - Manejo de recursos transparentes
   - Escalado responsivo de sprites

### Widgets Personalizados

1. **HeartCounter**
   - Visualización de corazones con scroll horizontal
   - Controles manuales (+/-) para ajuste
   - Persistencia del estado
   - Diseño responsivo y compacto

2. **PokemonWidget**
   - Visualización de sprites con proporción mantenida
   - Botones contextuales (editar/eliminar)
   - Soporte para drag & drop
   - Diseño adaptable

## Flujo de Datos

1. El usuario interactúa con la interfaz
2. Los eventos son manejados por el controlador
3. El controlador actualiza el modelo
4. El modelo notifica a la vista
5. La vista se actualiza con los nuevos datos

## Consideraciones de Rendimiento

- Caché de sprites para reducir llamadas a la API
- Carga asíncrona de imágenes
- Optimización de memoria para sprites
- Manejo eficiente de recursos
- Escalado responsivo de imágenes
- Gestión optimizada del layout

## Seguridad

- Validación de datos de entrada
- Manejo seguro de archivos de configuración
- Sanitización de nombres de Pokemon
- Validación de estados de corazones

## Extensibilidad

- Diseño modular para fácil adición de características
- Interfaces claras entre componentes
- Sistema de plugins para futuras extensiones
- Widgets personalizados reutilizables 