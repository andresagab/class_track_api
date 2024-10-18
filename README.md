# Class Track API

Class Track API es una aplicación desarrollada en Python con FastAPI para gestionar la asistencia de estudiantes a distintas asignaturas o materias. Este proyecto ofrece un conjunto de endpoints para manejar la gestión de estudiantes, materias y asistencia.

## Requisitos

Para ejecutar este proyecto en tu entorno local, necesitas tener instalados los siguientes componentes:

- **Python 3.9+**
- **FastAPI**
- **Uvicorn** (para ejecutar el servidor de desarrollo
- **SQLite** (base de datos predeterminada)

## Instalación

Sigue los siguientes pasos para clonar y ejecutar el proyecto:

### 1. Clonar el repositorio

```sh
git clone https://github.com/andresagab/class_track_api.git
cd class_track_api
```

### 2. Crear y activar entorno virtual

```sh
python -m venv venv
source venv/bin/activate  # En Linux/MacOS
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```sh
pip install -r requirements.txt
```

### 4. Ejecutar el servidor

```sh
uvicorn main:app --reload
```