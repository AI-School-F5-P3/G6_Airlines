import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

# Cargar los datos desde un CSV
df = pd.read_csv('airline_passenger_satisfaction.csv')


class AirlineApp:
    def __init__(self):
        # Inicializar la aplicación Dash
        self.app = dash.Dash(__name__)
        
        # Definir el layout de la aplicación
        self.app.layout = self.create_layout()
        
        # Configurar los callbacks
        self.setup_callbacks()

    def create_layout(self):
        return html.Div(style={'backgroundColor': '#F0FFFF', 'color': 'white', 'padding': '20px'}, children=[
            # Header with logo and company name
            html.Div(style={'text-align': 'center', 'padding': '10px'}, children=[
                # Logo
                html.Img(src='G6_Airlines/G6airline.jpeg', style={'height': '100px', 'width': 'auto'}),  # Ajusta la ruta y el tamaño según sea necesario
                # Company name
                html.H1("G6 Airline", style={'color': 'black', 'margin': '10px 0'}),
            ]),
            # Cabecera
            html.Div([
                html.H1("Predicción e Interpretabilidad de G6 Airline"),
                html.P("Explora cómo diferentes características afectan la predicción del modelo")
            ], style={'text-align': 'center', 'color': 'black', 'padding': '10px'}),
            
            # Sección de entrada de datos centrada
            html.Div([
                html.Div([
                    html.H2("Parámetros de Entrada"),
                    html.Label("Edad"),
                    dcc.Slider(id='input-edad', min=18, max=100, value=30, marks={i: str(i) for i in range(18, 101, 10)}),
                    
                    html.Br(),  # Añadir un salto de línea para separar los elementos
                    
                    html.Label("Ingresos anuales (en USD)"),
                    dcc.Input(id='input-ingresos', type='number', value=50000, step=1000),
                    
                    html.Br(),  # Añadir un salto de línea para separar los elementos
                    
                    html.Label("Género", style={'margin-top': '20px'}),  # Añadir un margen superior para separar la etiqueta "Género"
                    dcc.Dropdown(
                        id='input-genero',
                        options=[
                            {'label': 'Masculino', 'value': 'M'},
                            {'label': 'Femenino', 'value': 'F'}
                        ],
                        value='M'
                    ),
                    
                    html.Br(),  # Añadir un salto de línea para separar los elementos
                    
                    html.Button('Predecir', id='submit-button', n_clicks=0),
                ], style={'width': '100%', 'max-width': '400px', 'padding': '20px', 'backgroundColor': '#0033A0', 'border-radius': '10px'})
            ], style={'display': 'flex', 'justify-content': 'center'}),
            
            # Separador visual
            html.Br(),
            
            # Tabla con los datos del CSV
            html.Div([
                html.H2("Tabla de datos"),
                dash_table.DataTable(
                    id='tabla-datos',
                    data=df.to_dict('records'),
                    columns=[{'name': col, 'id': col} for col in df.columns],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'backgroundColor': '#0033A0', 'color': 'white'},  # Fondo y color del texto de la tabla
                )
            ], style={'width': '80%', 'margin': 'auto', 'backgroundColor': '#0033A0', 'padding': '10px', 'border-radius': '10px'}),
            
            # Separador visual
            html.Br(),
            
            # Visualización de predicciones y gráficos interactivos
            html.Div([
                html.H2("Resultados de la Predicción"),
                
                # Centrar el texto de la predicción
                html.Div(id='output-prediccion', style={'text-align': 'center', 'margin': 'auto', 'padding': '20px', 'font-size': '20px'}),
                
                # Contenedor para gráficos lado a lado
                html.Div([
                    html.Div([
                        html.H3("Importancia de las Características"),
                        dcc.Graph(id='importancia-grafico')
                    ], style={'width': '50%', 'padding': '10px'}),  # Estilo para el gráfico de la izquierda

                    html.Div([
                        html.H3("Contribución de las Características"),
                        dcc.Graph(id='contribucion-grafico')
                    ], style={'width': '50%', 'padding': '10px'})  # Estilo para el gráfico de la derecha
                ], style={'display': 'flex', 'justify-content': 'space-between'})  # Flexbox para alinear los gráficos
            ], style={'width': '80%', 'margin': 'auto', 'backgroundColor': '#0033A0', 'padding': '10px', 'border-radius': '10px'})
        ])
    
    def setup_callbacks(self):
        @self.app.callback(
            Output('output-prediccion', 'children'),
            Output('importancia-grafico', 'figure'),
            Output('contribucion-grafico', 'figure'),
            Input('submit-button', 'n_clicks'),
            Input('input-edad', 'value'),
            Input('input-ingresos', 'value'),
            Input('input-genero', 'value')
        )
        def actualizar_resultados(n_clicks, edad, ingresos, genero):
            if n_clicks > 0:
                # Simulación de predicción y de importancia de características
                prediccion = np.random.choice(['Alta', 'Baja'])
                
                # Gráfico de importancia de características simulado
                importancia = {'Característica': ['Edad', 'Ingresos', 'Género'], 'Importancia': [0.4, 0.3, 0.3]}
                importancia_fig = px.bar(importancia, x='Característica', y='Importancia', title='Importancia de las Características')
                
                # Gráfico de contribución de características simulado
                contribucion = {'Característica': ['Edad', 'Ingresos', 'Género'], 'Contribución': [0.5, 0.2, 0.3]}
                contribucion_fig = px.pie(contribucion, values='Contribución', names='Característica', title='Contribución de las Características')

                return f"El nivel de satisfacción predicho es: {prediccion}", importancia_fig, contribucion_fig
            
            return "", {}, {}

    def run(self):
        # Ejecutar la aplicación
        self.app.run_server(debug=True)


if __name__ == '__main__':
    app = AirlineApp()
    app.run()
