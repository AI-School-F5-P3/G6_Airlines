# G6 AIRLINE ![main-logo-transparent](https://github.com/user-attachments/assets/428962ec-5dc6-46df-8622-b3901b7cdffb)

G6Airline, un sistema innovador que utiliza técnicas

de aprendizaje supervisado para predecir la satisfacción del cliente. El proyecto se basa en un modelo de aprendizaje
automático que analiza datos relevantes y genera predicciones precisas sobre la experiencia del cliente.

## Objetivo y Funcionalidad de la Aplicación

El objetivo principal del proyecto G6Airline es desarrollar un sistema de predicción de la satisfacción del cliente que sea preciso, confiable y fácil de integrar en la aplicación existente. Para lograr este objetivo, el proyecto se enfoca en:

1. Recopilación y análisis de datos relevantes del cliente.

2. Entrenamiento de un modelo de aprendizaje supervisado para predecir la satisfacción del cliente.

3. Presentación de resultados en tiempo real a través de una interfaz intuitiva y fácil de usar.

4. Esto nos ayudará a generar informes detallados que permiten identificar áreas de mejora y optimizar las estrategias de la aerolínea

## Tecnologías Utilizadas
**Dash:** Una herramienta de desarrollo web para la creación de aplicaciones de análisis de datos interactivos. Se utiliza para la visualización de los resultados del modelo y para la creación de la interfaz de usuario de la aplicación.

**Scikit-learn:** Una biblioteca de Python que proporciona algoritmos de aprendizaje automático para la creación del modelo de aprendizaje supervisado.

**Plotly:** Una biblioteca de visualización de datos que proporciona gráficos interactivos para la representación de los resultados del modelo.

**API Rest:** Un conjunto de reglas que permiten a la aplicación comunicarse con el modelo de aprendizaje supervisado.

**MySQL:** Un sistema de gestión de bases de datos relacionales (RDBMS) que se utiliza para almacenar los datos de entrenamiento y las predicciones del modelo.

**Docker Compose:** Una herramienta para definir y ejecutar aplicaciones multi-contenedor, se utiliza para facilitar el despliegue y la gestión de los diferentes componentes del proyecto.

**Rendo:** Una plataforma para el despliegue de aplicaciones en la nube, se utiliza para hacer la aplicación accesible a través de internet.

## Requisitos

Asegúrate de tener instalado Python en tu sistema. Este proyecto fue desarrollado con Python.
## Instalación

1. Clona este repositorio:
   ```
  git clone https://github.com/tu-usuario/G6Airline.git
cd G6Airline
   ```

2. Instala las dependencias necesarias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar G6Airline, necesitas iniciar tanto la API como la aplicación principal.

### Iniciar la API

1. Navega al directorio de la API (si es necesario):
   ```
   cd path/to/api
   ```

2. Inicia el servidor de la API con Uvicorn:
   ```
   uvicorn main:app --reload
   ```

   La API ahora debería estar ejecutándose en `http://localhost:8000`.

### Iniciar la Aplicación Principal

1. En una nueva terminal, navega al directorio principal del proyecto.

2. Ejecuta la aplicación principal:
   ```
   python app.py
   ```

   La aplicación ahora debería estar en funcionamiento.

## Características

- Predicción de satisfacción del cliente basada en múltiples factores.
- API RESTful para realizar predicciones.
- Interfaz de usuario para interactuar con el modelo de predicción.

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de hacer un pull request.


