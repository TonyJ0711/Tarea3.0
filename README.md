# 🎓 Gestión de Estudiantes - Tarea 3.0

Una aplicación web moderna y minimalista desarrollada en **Flask** que permite realizar la gestión completa (CRUD) de un listado de estudiantes, sus códigos de identificación, carreras y calificaciones. La aplicación está totalmente contenedorizada con Docker y cuenta con un flujo de integración continua (CI) mediante GitHub Actions.

---

## 🚀 Características

* **Operaciones CRUD Completas:** Permite agregar, listar, editar y eliminar registros de estudiantes en tiempo real.
* **Interfaz de Usuario Avanzada:** Diseño visual responsivo con temática oscura (*Dark Mode*), fuentes *Syne* y *DM Mono*, indicadores de estado dinámicos y avatares personalizados por estudiante.
* **Código de Calificaciones Dinámico:** Clasificación visual por colores según la nota obtenida (en un rango de 0 a 10).
* **Contenedorización Profesional:** Configurada para correr sobre una imagen ultra ligera de Docker (`python:3.12-alpine`).
* **Automatización CI/CD:** Flujo de trabajo en GitHub Actions configurado para construir y publicar la imagen en GitHub Container Registry (GHCR) de forma automática al hacer push a la rama `main`.

---

## 🛠️ Tecnologías Utilizadas

* **Backend / Core:** Python 3.12 & Flask 3.1.2
* **Frontend:** HTML5, CSS3 Custom Properties (Variables) y Jinja2 para el renderizado de plantillas.
* **DevOps & Entorno:** Docker, GitHub Actions (CI/CD)[cite: 1]

---

## 📂 Estructura del Proyecto

El repositorio "Tarea3.0-main.zip" cuenta con la siguiente arquitectura de archivos[cite: 1]:

```text
├── .github/workflows/
│   └── deploy.yml       # Configuración del Pipeline de GitHub Actions (CI/CD)[cite: 1]
├── app.py               # Lógica del servidor Flask y frontend integrado[cite: 1]
├── Dockerfile           # Configuración para la creación de la imagen Docker[cite: 1]
├── requeriments.txt     # Dependencias del proyecto de Python[cite: 1]
└── .gitignore           # Exclusiones de Git (entornos virtuales)[cite: 1]
💻 Instalación y Ejecución Local
Opción 1: Ejecución nativa con Python
Asegúrate de tener instalado Python 3.12 o superior en tu sistema.

Clonar el repositorio:

Bash
   git clone [https://github.com/TonyJ0711/Tarea3.0.git](https://github.com/TonyJ0711/Tarea3.0.git)
   cd Tarea3.0
Crear e inicializar un entorno virtual (Recomendado):

Bash
   # En Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # En Windows
   python -m venv venv
   venv\Scripts\activate
Instalar las dependencias:
(Nota: El archivo mantiene el nombre original del repositorio requeriments.txt)

[cite: 1]

Bash
   pip install -r requeriments.txt
Correr la aplicación:

Bash
   python app.py
La aplicación estará disponible en http://localhost:5000[cite: 1].

Opción 2: Ejecución mediante Docker
Si prefieres usar contenedores, el proyecto incluye un Dockerfile optimizado basado en alpine[cite: 1]:

Construir la imagen de Docker:

Bash
   docker build -t gestion-estudiantes:1.0.0 .
Ejecutar el contenedor exponiendo el puerto 5000:

Bash
   docker run -d -p 5000:5000 --name app-estudiantes gestion-estudiantes:1.0.0
Accede a la app desde tu navegador en http://localhost:5000[cite: 1].

🤖 Integración Continua (GitHub Actions)
El archivo .github/workflows/deploy.yml automatiza el despliegue[cite: 1]. Cada vez que realices un git push a la rama main, GitHub Actions se encargará de:

Iniciar sesión de forma segura en GitHub Container Registry (GHCR) empleando el token automático de GitHub[cite: 1].

Construir una nueva imagen Docker optimizada (ghcr.io/tonyj0711/ejercicio3:1.0.0)[cite: 1].

Publicar la imagen terminada directamente en tu registro de paquetes de GitHub[cite: 1].

👤 Autor
TonyJ0711 - Desarrollo de la aplicación y configuración DevOps - GitHub Profile