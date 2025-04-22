# 🔄 Integración Continua y Entrega Continua (CI/CD)

## 📋 Descripción General

Este documento describe la configuración de CI/CD implementada para el Pokemon Team GUI Tracker usando GitHub Actions.

## 🔧 Configuración del Workflow

### 📌 Eventos Desencadenantes

El workflow se ejecuta en los siguientes eventos:

- Push a la rama `main`
- Pull Requests hacia la rama `main`

### 🛠️ Matriz de Pruebas

Las pruebas se ejecutan en múltiples versiones de Python:

- Python 3.8
- Python 3.9
- Python 3.10

## 🔄 Pasos del Workflow

### 1. Configuración del Entorno

```yaml
- uses: actions/checkout@v2
- uses: actions/setup-python@v2
  with:
    python-version: ${{ matrix.python-version }}
```

### 2. Instalación de Dependencias del Sistema

```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y xvfb libxkbcommon-x11-0 libxcb-icccm4 
    libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 
    libxcb-xinerama0 libxcb-xfixes0
```

### 3. Instalación de Dependencias Python

```yaml
- name: Install Python dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install pytest pytest-cov pytest-qt
```

### 4. Ejecución de Pruebas

```yaml
- name: Run tests with pytest
  run: |
    xvfb-run --auto-servernum pytest tests/ --cov=src --cov-report=xml
```

### 5. Reporte de Cobertura

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v2
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

## 🖥️ Entorno Virtual de Pruebas

- Utiliza `xvfb` para simular un entorno de escritorio virtual
- Necesario para pruebas de GUI con PyQt5
- Configurado automáticamente en el entorno de CI

## 📊 Reportes y Análisis

- Generación automática de reportes de cobertura en formato XML
- Integración con Codecov para visualización y seguimiento
- Falla el CI si hay errores en el reporte de cobertura

## 🚨 Manejo de Errores

- El workflow fallará si:
  - Las pruebas no pasan
  - La cobertura no se puede reportar
  - Hay errores en la instalación de dependencias
  - El entorno virtual X11 no se puede iniciar 