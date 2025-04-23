# 🎮 Guía de Usuario - Pokemon Team Tracker

## 📥 Instalación

1. Descarga el archivo `Pokemon.Team.Tracker.zip` de la sección de releases
2. Descomprime el archivo en la ubicación que prefieras
3. Haz doble clic en `Pokemon Team Tracker.exe` para iniciar la aplicación

No se requiere instalar Python ni ninguna otra dependencia.

## 🚀 Uso Básico

### Crear un Equipo
1. Selecciona un Pokemon del menú desplegable
2. (Opcional) Escribe un apodo para tu Pokemon
3. Haz clic en "Añadir" para agregarlo a tu equipo
4. Repite hasta tener hasta 6 Pokemon en tu equipo

### Gestionar el Equipo
- **Mover Pokemon**: Arrastra y suelta los sprites para reorganizar tu equipo
- **Editar Apodos**: Haz clic en el botón ✏️ sobre un Pokemon
- **Eliminar Pokemon**: Haz clic en el botón ❌ sobre un Pokemon
- **Limpiar Equipo**: Usa el botón "Limpiar Equipo" para empezar de nuevo

### Sistema de Corazones
- Usa los botones + y - para ajustar los corazones
- El contador muestra la cantidad actual de corazones
- Los corazones se guardan junto con tu equipo

### Guardar y Cargar
- **Guardar Equipo**: Haz clic en "Guardar Equipo" para almacenar tu configuración actual
- **Cargar Equipo**: Usa "Cargar Equipo" para recuperar un equipo guardado
- Los equipos se guardan en la carpeta `saves` dentro del directorio de la aplicación

## 🔧 Configuración

La aplicación viene preconfigurada y lista para usar. Los archivos de configuración y caché se crean automáticamente en:
- `config/`: Archivos de configuración
- `assets/cache/`: Caché de sprites de Pokemon
- `saves/`: Equipos guardados
- `logs/`: Registros de la aplicación

## ❓ Solución de Problemas

### La aplicación no inicia
- Verifica que hayas extraído todos los archivos del ZIP
- Asegúrate de tener los permisos necesarios en la carpeta
- Prueba ejecutar como administrador

### No se ven los sprites
- Verifica tu conexión a internet
- Los sprites se descargan la primera vez que seleccionas un Pokemon
- Los sprites se almacenan en caché para uso posterior

### No se pueden guardar equipos
- Verifica que la carpeta `saves` exista y tengas permisos de escritura
- Intenta ejecutar la aplicación como administrador

## 🆘 Soporte

Si encuentras algún problema:
1. Revisa los logs en la carpeta `logs`
2. Reporta el problema en nuestra página de GitHub
3. Incluye el archivo de log y los pasos para reproducir el error

## 🔄 Actualizaciones

- Visita nuestra página de GitHub para ver las últimas versiones
- Descarga siempre la versión más reciente
- Las actualizaciones incluyen nuevas funciones y correcciones 