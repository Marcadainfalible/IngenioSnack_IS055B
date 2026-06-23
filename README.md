# IngenioSnack - Sistema de Pedidos y Validación Ágil

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)
![Metodologías](https://img.shields.io/badge/Metodolog%C3%ADas-XP%20%7C%20Design%20Thinking%20%7C%20Lean%20Startup-orange.svg)

## Descripción del Proyecto
**IngenioSnack** es una plataforma digital diseñada para optimizar la atención y gestión de pedidos en el cafetín de la Facultad de Ingeniería de Sistemas (FIS) de la Universidad Nacional del Centro del Perú (UNCP). El proyecto nace de la necesidad de reducir los tiempos de espera (filas) de los estudiantes durante los recesos y optimizar la gestión de insumos del administrador (Sr. Julio).

Desarrollado para la asignatura de **Metodología de Desarrollo de Software (IS055B)**, este repositorio documenta la evolución completa del sistema: desde la codificación del software bajo prácticas de Extreme Programming (XP), hasta la validación de nuevas líneas de negocio usando enfoques centrados en el usuario.

## Equipo de Desarrollo (Grupo de 5)
* **Oscar Manuel Hinostroza Ramos** - *Tech Lead / Arquitecto de Software*
* **Anheli Juanita Vila Torres** - *UX/UI & Design Thinking Analyst*
* **Pavel Alexander Pecho Chiyuari** - *Frontend Developer & Prototyping*
* **Renzo Sebastian Bravo Paucar** - *Business Strategist (Lean Canvas)*
* **Michael Snaider Chancan Alania** - *Data & MVP Analyst*

---

##  Evolución del Proyecto

### Iteración 1: El MVP Tecnológico (Semana 10)
En la primera etapa, construimos el núcleo del sistema de pedidos aplicando **Extreme Programming (XP)**. Logramos reducir el tiempo de espera en un 40%.
* **Arquitectura:** Patrón MVC (Model-View-Controller) utilizando **Flask** (Python) y **Jinja2** para la renderización de plantillas dinámicas.
* **Base de Datos:** Implementación inicial ágil con **SQLite** vía SQLAlchemy. Esto permitió a los 5 miembros del equipo clonar el entorno localmente, trabajar en paralelo sin dependencias externas y consolidar un MVP funcional de manera rápida. La arquitectura está lista para migrar a PostgreSQL/MySQL modificando únicamente el archivo `.env`.
* **Control de Versiones Estricto:** Se estableció un flujo de trabajo en GitHub con ramas protegidas. Todo el código en `main` pasó por un riguroso proceso de *Pull Requests* y revisión de pares para asegurar la calidad y la separación de responsabilidades (ej. refactorización de estilos a la carpeta estática `static/css`).

### Iteración 2: Validación de Negocio y Escalabilidad (Semanas 11 y 12)
Ante la propuesta de expandir el servicio con nuevos modelos de negocio (Suscripciones o Cajas Sorpresa) financiados por el decanato, el equipo detuvo el desarrollo de código para validar la idea de forma barata y rápida con el mercado real.

**1. Design Thinking (Pensando en el Estudiante FIS)**
Aplicamos las 5 fases para entender el verdadero dolor del usuario:
* **Empatizar & Definir:** Mediante entrevistas, descubrimos que el frío y el tiempo limitado entre laboratorios son los mayores frustrantes. *(Ver `MAPA_EMPATIA.png` y `DESIGN_THINKING.md`)*.
* **Idear & Prototipar:** Generamos 10 ideas mediante *Crazy 8s* y diseñamos un prototipo de baja fidelidad para una suscripción de "Recojo VIP". *(Ver `PROTOTIPO.png`)*.
* **Testear:** Validamos la interfaz con estudiantes reales, asegurando que la solución encaje con sus rutinas.

**2. Lean Startup (Construir, Medir, Aprender)**
Modelamos la viabilidad financiera y operativa de la solución elegida:
* Formulamos un **Lean Canvas** adaptado al modelo de suscripciones. *(Ver `LEAN_CANVAS.md`)*.
* Diseñamos un **Producto Mínimo Viable (MVP)** que no requiere desarrollo de backend completo (ej. validación manual de demanda) para minimizar el riesgo de inversión del Sr. Julio. *(Ver `MVP_DEFINIDO.md`)*.
* Simulamos el ciclo **Construir-Medir-Aprender**, definiendo métricas accionables (tasa de conversión real) frente a métricas vanidosas. *(Ver `CICLO_CMA.md`)*.

---

## Estructura del Repositorio
Cumpliendo con los estándares del proyecto:

```text
IngenioSnack_IS055B/
├── docs/
│   ├── S11_Design_Thinking/      # Fases 1 a 5, Mapa de Empatía y Prototipos
│   └── S12_Lean_Startup/         # Lean Canvas, MVP y Ciclo CMA
├── src/                          # Código fuente de la Iteración 1 (Flask MVC)
│   ├── app.py                    # Lógica de enrutamiento principal
│   ├── models.py                 # Esquemas de Base de Datos
│   └── ingeniosnack.db           # Base de datos SQLite local
├── static/                       # Archivos estáticos
│   └── css/                      # Hojas de estilo modularizadas
├── templates/                    # Vistas HTML (Jinja2)
├── tests/                        # Pruebas unitarias (TDD)
├── .env.example                  # Variables de entorno
└── README.md                     # Evolución y documentación del proyecto