import dash
import os
import json  # Para cargar la arquitectura del modelo
from dash import dcc, html, State, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.io as pio
import catboost
from catboost import CatBoostClassifier
import numpy as np
import pandas as pd
from tensorflow.keras.models import model_from_json  # Para cargar el modelo desde JSON

# Definir los colores primarios y secundarios
PRIMARY_COLOR = "#91C48A"
SECONDARY_COLOR_1 = "#485751"
SECONDARY_COLOR_2 = "#6D9DC5"
SECONDARY_COLOR_3 = "#FFA9A3"

TEXT_COLOR = "#FFFFFF"  # Ejemplo de color de texto (puedes ajustarlo)
BACKGROUND_COLOR = "fafbfd"  # Ajusta el color de fondo según prefieras
# Modelo comentado, para habilitarlo solo se necesita descomentar la siguiente línea
# MODEL_PATH = 'Notebook/catboost_info/catboost_training.json'

# Función para cargar el modelo CatBoost desde un archivo JSON
def load_catboost_model(model_path):
    model = CatBoostClassifier()
    model.load_model(model_path)
    return model

# Cargar las plantillas en plotly.io
load_figure_template(["minty", "minty_dark"])

# Cargar los datos desde un CSV
df = pd.read_csv('Data/airline_passenger_satisfaction.csv')


class AirlineApp:
    def __init__(self):
        # Inicializar la aplicación Dash
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, "https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap"])
        
        # Cargar el modelo
        # self.model = load_catboost_model(MODEL_PATH)
        
        # Definir el layout de la aplicación
        self.app.layout = self.create_layout()
        
        # Configurar los callbacks
        self.setup_callbacks()

    def create_layout(self):
        # Crear la barra de navegación
        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src='assets/1.png', height="150px")),
                                dbc.Col(dbc.NavbarBrand(
                                    "G6 Airline", 
                                    className="display-2", 
                                    style={
                                        "font-family": "Abril Fatface", 
                                        "font-size": "4rem"  # Ajusta este valor según prefieras
                                    }
                                )),
                            ],
                            align="center",
                            className="display-2",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                ]
            ),
            color=SECONDARY_COLOR_1,
            dark=True,
            className="mb-4",
        )

        color_mode_switch = html.Span(
            [
                dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
                dbc.Switch(id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
                dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
            ]
        )
        
        # Componente Offcanvas
        offcanvas = html.Div(
            [
                dbc.Button(
                    "Open scrollable offcanvas",
                    id="open-offcanvas-scrollable",
                    n_clicks=0,
                    style={"backgroundColor": "#6D9DC5", "color": "#FFFFFF"}
                ),
                dbc.Offcanvas(
                    html.P("The contents on the main page are now scrollable."),
                    id="offcanvas-scrollable",
                    scrollable=True,
                    title="Scrollable Offcanvas",
                    is_open=False,
                    style={"backgroundColor": "#485751", "color": "#FFFFFF"}
                ),
            ]
        )

        # El contenido principal
        content = html.Div(style={'backgroundColor': BACKGROUND_COLOR, 'color': TEXT_COLOR, 'padding': '20px'}, children=[
            color_mode_switch,
            offcanvas,

            html.Div([
                html.H1("Predicción e Interpretabilidad de G6 Airline", style={"color": PRIMARY_COLOR}),
                html.P("Explora cómo diferentes características afectan la predicción del modelo", style={"color": SECONDARY_COLOR_1})
            ], style={'text-align': 'center', 'color':  SECONDARY_COLOR_1, 'padding': '10px'}),
            
            html.Div([
                html.Div([
                    html.H2("Parámetros de Entrada", style={"color": PRIMARY_COLOR}),
                    html.Label("Edad", style={"color": SECONDARY_COLOR_2}),
                    dcc.Slider(id='input-edad', min=18, max=100, value=30, marks={i: str(i) for i in range(18, 101, 10)}),
                    
                    html.Br(),  
                    
                    html.Label("Ingresos anuales (en USD)", style={"color": SECONDARY_COLOR_2}),
                    dcc.Input(id='input-ingresos', type='number', value=50000, step=1000),
                    
                    html.Br(),  
                    
                    html.Label("Género", style={'margin-top': '20px', "color": SECONDARY_COLOR_2}),  
                    dcc.Dropdown(
                        id='input-genero',
                        options=[
                            {'label': 'Masculino', 'value': 'M'},
                            {'label': 'Femenino', 'value': 'F'}
                        ],
                        value='M',
                        style={"backgroundColor": PRIMARY_COLOR, "color": TEXT_COLOR}
                    ),
                    
                    html.Br(),  
                    
                    html.Button('Predecir', id='submit-button', n_clicks=0, style={'backgroundColor': SECONDARY_COLOR_1, 'color': TEXT_COLOR}),
                ], style={'width': '100%', 'max-width': '400px', 'padding': '20px', 'backgroundColor': SECONDARY_COLOR_1, 'border-radius': '10px'})
            ], style={'display': 'flex', 'justify-content': 'center'}),
            
            html.Br(),
            
            # Botón para abrir/cerrar la tabla de datos
            dbc.Button(
                "Mostrar/Ocultar Tabla de Datos",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
                style={'backgroundColor': SECONDARY_COLOR_2}
            ),
            
            # Colapso para la tabla de datos
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody([
                        html.H2("Tabla de datos", style={"color": PRIMARY_COLOR}),
                        dash_table.DataTable(
                            id='tabla-datos',
                            data=df.to_dict('records'),  # Usar el DataFrame directamente
                            columns=[{'name': col, 'id': col} for col in df.columns],
                            page_size=10,
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'backgroundColor': PRIMARY_COLOR, 'color': TEXT_COLOR},
                        )
                    ])
                ),
                id="collapse",
                is_open=False,
            ),
            
            html.Br(),
            
            html.Div([
                html.H2("Resultados de la Predicción", style={"color": PRIMARY_COLOR}),
                html.Div(id='output-prediccion', style={'text-align': 'center', 'margin': 'auto', 'padding': '20px', 'font-size': '20px', 'color': SECONDARY_COLOR_2}),
                
                html.Div([
                    html.Div([
                        html.H3("Importancia de las Características",  style={"color": PRIMARY_COLOR}),
                        dcc.Graph(id='importancia-grafico')
                    ], style={'width': '50%', 'padding': '10px'}),  

                    html.Div([
                        html.H3("Contribución de las Características", style={"color": PRIMARY_COLOR}),
                        dcc.Graph(id='contribucion-grafico')
                    ], style={'width': '50%', 'padding': '10px'})  
                ], style={'display': 'flex', 'justify-content': 'space-between'})  
            ], style={'width': '80%', 'margin': 'auto', 'backgroundColor': SECONDARY_COLOR_1, 'padding': '10px', 'border-radius': '10px'})
        ])

        # Combinar la barra de navegación con el resto del contenido
        return html.Div([
            navbar,
            content
        ])

    def setup_callbacks(self):
        @self.app.callback(
            [Output('output-prediccion', 'children'),
             Output('importancia-grafico', 'figure'),
             Output('contribucion-grafico', 'figure')],
            [Input('submit-button', 'n_clicks'),
             Input('input-edad', 'value'),
             Input('input-ingresos', 'value'),
             Input('input-genero', 'value')],
        )
        def actualizar_resultados(n_clicks, edad, ingresos, genero):
            if n_clicks > 0:
                # Preparar los datos de entrada para el modelo
                input_data = np.array([[edad, ingresos, 1 if genero == 'M' else 0]])
                
                # Realizar la predicción utilizando el modelo cargado
                # prediccion = self.model.predict(input_data)[0]
                # prediccion_label = "Alta" if prediccion > 0.5 else "Baja"
                
                # Gráfico de importancia de características simulado
                importancia = {'Característica': ['Edad', 'Ingresos', 'Género'], 'Importancia': [0.4, 0.3, 0.3]}
                importancia_fig = px.bar(importancia, x='Característica', y='Importancia', title='Importancia de las Características')
                
                # Gráfico de contribución de características simulado
                contribucion = {'Característica': ['Edad', 'Ingresos', 'Género'], 'Contribución': [0.5, 0.2, 0.3]}
                contribucion_fig = px.pie(contribucion, values='Contribución', names='Característica', title='Contribución de las Características')

                return f"El nivel de satisfacción predicho es: [Predicción no activa]", importancia_fig, contribucion_fig
            
            return "", {}, {}
        
        @self.app.callback(
            Output("collapse", "is_open"),
            [Input("collapse-button", "n_clicks")],
            [State("collapse", "is_open")],
        )
        def toggle_collapse(n_clicks, is_open):
            if n_clicks:
                return not is_open
            return is_open

        @self.app.callback(
            Output("offcanvas-scrollable", "is_open"),
            Input("open-offcanvas-scrollable", "n_clicks"),
            State("offcanvas-scrollable", "is_open"),
        )
        def toggle_offcanvas_scrollable(n1, is_open):
            if n1:
                return not is_open
            return is_open

    def run(self):
        self.app.layout = self.create_layout()
        self.setup_callbacks()
        self.app.run_server(debug=True)


if __name__ == '__main__':
    app_instance = AirlineApp()
    app_instance.run()
