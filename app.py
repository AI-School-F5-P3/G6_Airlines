import dash
from dash import dcc, html, State, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pandas as pd
import sqlite3  # Import sqlite3 for database operations
from datetime import datetime
import sklearn
import pickle

PRIMARY_COLOR = "#91C48A"
SECONDARY_COLOR_1 = "#485751"
SECONDARY_COLOR_2 = "#6D9DC5"
SECONDARY_COLOR_3 = "#FFA9A3"
TEXT_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "fafbfd"

# Definición de cols
cols = ['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
        'Flight Distance', 'Inflight wifi service',
        'Departure/Arrival time convenient', 'Ease of Online booking',
        'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
        'Inflight entertainment', 'On-board service', 'Leg room service',
        'Baggage handling', 'Checkin service', 'Inflight service',
        'Cleanliness', 'Departure Delay in Minutes', 'Arrival Delay in Minutes',
        'Age Group']

def load_model():
    with open('model_pipeline.pkl', 'rb') as file:
        model = pickle.load(file)
        return model


df = pd.read_csv('Data/airline_passenger_satisfaction.csv')


class AirlineApp:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, "https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap"], suppress_callback_exceptions=True)
        self.model = load_model()
        self.app.layout = self.create_layout()
        self.setup_callbacks()
        self.feedback_data = []
        self.init_db()  # Initialize the database
        self.model = load_model()
        print(type(self.model)) 
        
    def init_db(self):
        # Connect to the SQLite database
        self.conn = sqlite3.connect('feedback.db')
        self.cursor = self.conn.cursor()
        # Create the feedback table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                edad INTEGER,
                ingresos REAL,
                genero TEXT,
                prediccion TEXT,
                feedback TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def collect_feedback(self, n_clicks, feedback, edad, ingresos, genero, prediccion):
        if n_clicks > 0 and feedback:
            # Insert feedback into the database
            self.cursor.execute('''
                INSERT INTO feedback (edad, ingresos, genero, prediccion, feedback, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (edad, ingresos, genero, prediccion, feedback, datetime.now().isoformat()))
            self.conn.commit()
            return "Gracias por tu feedback!"
        return ""

    def create_layout(self):
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
                                    style={"font-family": "Abril Fatface", "font-size": "4rem"}
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

        dropdown = dcc.Dropdown(
            id='page-dropdown',
            options=[
                {'label': 'Página Principal', 'value': 'main-page'},
                {'label': 'Página 2', 'value': 'page-2'},
                {'label': 'Página 3', 'value': 'page-3'}
            ],
            value='main-page',
            clearable=False
        )

        content = html.Div(id='page-content', style={'backgroundColor': BACKGROUND_COLOR, 'color': TEXT_COLOR, 'padding': '20px'})

        return html.Div([
            navbar,
            dropdown,
            content
        ])

    def setup_callbacks(self):
        @self.app.callback(
            Output('page-content', 'children'),
            [Input('page-dropdown', 'value')]
        )
        def display_page(selected_page):
            if selected_page == 'main-page':
                return self.main_page_content()
            elif selected_page == 'page-2':
                return self.page_2_content()
            elif selected_page == 'page-3':
                return self.page_3_content()

        @self.app.callback(
            [Output('output-prediccion', 'children'),
            Output('importancia-grafico', 'figure'),
            Output('contribucion-grafico', 'figure')],
            [Input('submit-button', 'n_clicks')] +
            [Input(f'input-{col.lower().replace(" ", "-")}', 'value') for col in cols]
        )
        def actualizar_resultados(n_clicks, *inputs):
            if n_clicks > 0:
                # Crear un diccionario con los valores de entrada
                input_dict = dict(zip(cols, inputs))
                
                # Preprocesamiento de los datos de entrada
                input_data = []
                for col in cols:
                    if col in ['Gender', 'Customer Type', 'Type of Travel', 'Class']:
                        # Para variables categóricas, usar codificación one-hot
                        categories = {
                            'Gender': ['Male', 'Female'],
                            'Customer Type': ['Loyal Customer', 'disloyal Customer'],
                            'Type of Travel': ['Personal Travel', 'Business travel'],
                            'Class': ['Eco', 'Eco Plus', 'Business']
                        }
                        input_data.extend([1 if input_dict[col] == cat else 0 for cat in categories[col]])
                    elif col == 'Age Group':
                        # Para 'Age Group', convertir a numérico
                        age_groups = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
                        input_data.extend([1 if input_dict[col] == group else 0 for group in age_groups])
                    else:
                        # Para variables numéricas, usar el valor directamente
                        input_data.append(float(input_dict[col]))
                print(input_data)
                # Convertir a numpy array y hacer la predicción
                input_array = np.array([input_data])
                prediction = self.model.predict(input_array)[0]
                prediction_label = "Alta" if prediction > 0.5 else "Baja"
                
                # Calcular importancia y contribución de las características (ejemplo simplificado)
                importancia = {'Característica': cols, 'Importancia': np.random.rand(len(cols))}
                importancia['Importancia'] /= np.sum(importancia['Importancia'])  # Normalizar
                importancia_df = pd.DataFrame(importancia)
                importancia_fig = px.bar(importancia_df, x='Característica', y='Importancia', title='Importancia de las Características')
                
                contribucion = {'Característica': cols, 'Contribución': np.abs(np.random.randn(len(cols)))}
                contribucion['Contribución'] /= np.sum(contribucion['Contribución'])  # Normalizar
                contribucion_df = pd.DataFrame(contribucion)
                contribucion_fig = px.pie(contribucion_df, values='Contribución', names='Característica', title='Contribución de las Características')
                
                return f"El nivel de satisfacción predicho es: {prediction_label}", importancia_fig, contribucion_fig
            
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
        
        @self.app.callback(
            Output("feedback-message", "children"),
            [Input("submit-feedback", "n_clicks")],  # Corrected 'n-clicks' to 'n_clicks'
            [State("user-feedback", "value"),  # Corrected 'user-feedabck' to 'user-feedback'
             State('input-edad', 'value'),
             State('input-ingresos', 'value'),
             State('input-genero', 'value'),
             State('output-prediccion', 'children')]
        )
        def collect_feedback(n_clicks, feedback, edad, ingresos, genero, prediccion):
            if n_clicks > 0 and feedback:
                feedback_entry = {
                    'Edad': edad,
                    'Ingresos': ingresos,
                    'Género': genero,
                    'Predicción': prediccion,
                    'Feedback': feedback,
                    'Timestamp': datetime.now().isoformat()
                }
                self.feedback_data.append(feedback_entry)
                # Optionally save to a file or database
                pd.DataFrame(self.feedback_data).to_csv('feedback.csv', index=False)
                return "Gracias por tu feedback!"
            return ""

    def main_page_content(self):
        return html.Div([
            html.H1(
                "Bienvenidos a G6 Airline",
                style={
                    "color": PRIMARY_COLOR,
                    "textAlign": "center",
                    "marginBottom": "20px"
                }
            ),
            html.P(
                (
                    "Descubre una nueva forma de volar con nuestra app "
                    "impulsada por inteligencia artificial."
                ),
                style={
                    "color": PRIMARY_COLOR,
                    "textAlign": "center",
                    "fontSize": "18px",
                    "marginBottom": "10px"
                }
            ),
            html.P(
                (
                    "Utilizamos aprendizaje automático avanzado para predecir "
                    "y mejorar tu satisfacción en cada viaje."
                ),
                style={
                    "color": PRIMARY_COLOR,
                    "textAlign": "center",
                    "fontSize": "18px"
                }
            )
        ], style={"width": "80%", "margin": "0 auto"})

    def page_2_content(self):
        return html.Div([
            html.H1("Predicción e Interpretabilidad de G6 Airline", style={"color": PRIMARY_COLOR, "className": "text-center"}),
            html.P("Explora cómo diferentes características afectan la predicción del modelo", style={"color": SECONDARY_COLOR_1}),
            html.Div([
                html.Div([
                    html.H2("Parámetros de Entrada", style={"color": PRIMARY_COLOR}),
                    
                    # Inputs categóricos
                    html.Label("Género", style={"color": SECONDARY_COLOR_2}),
                    dcc.Dropdown(id='input-gender', options=[{'label': i, 'value': i} for i in ['Male', 'Female']], value='Male'),
                    
                    html.Label("Tipo de Cliente", style={"color": SECONDARY_COLOR_2}),
                    dcc.Dropdown(id='input-customer-type', options=[{'label': i, 'value': i} for i in ['Loyal Customer', 'disloyal Customer']], value='Loyal Customer'),
                    
                    html.Label("Tipo de Viaje", style={"color": SECONDARY_COLOR_2}),
                    dcc.Dropdown(id='input-type-of-travel', options=[{'label': i, 'value': i} for i in ['Personal Travel', 'Business travel']], value='Personal Travel'),
                    
                    html.Label("Clase", style={"color": SECONDARY_COLOR_2}),
                    dcc.Dropdown(id='input-class', options=[{'label': i, 'value': i} for i in ['Eco', 'Eco Plus', 'Business']], value='Eco'),
                    
                    # Inputs numéricos
                    html.Label("Edad", style={"color": SECONDARY_COLOR_2}),
                    dcc.Input(id='input-age', type='number', value=30),
                    
                    html.Label("Distancia de Vuelo", style={"color": SECONDARY_COLOR_2}),
                    dcc.Input(id='input-flight-distance', type='number', value=1000),
                    
                    # Inputs para servicios (escala 1-5)
                    [(html.Label(service, style={"color": SECONDARY_COLOR_2}),
                    dcc.Slider(id=f'input-{service.lower().replace(" ", "-")}', min=1, max=5, marks={i: str(i) for i in range(1, 6)}, value=3)) 
                    for service in ['Inflight wifi service', 'Departure/Arrival time convenient', 'Ease of Online booking',
                                    'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
                                    'Inflight entertainment', 'On-board service', 'Leg room service',
                                    'Baggage handling', 'Checkin service', 'Inflight service', 'Cleanliness']],
                    
                    html.Label("Retraso en la Salida (minutos)", style={"color": SECONDARY_COLOR_2}),
                    dcc.Input(id='input-departure-delay-in-minutes', type='number', value=0),
                    
                    html.Label("Retraso en la Llegada (minutos)", style={"color": SECONDARY_COLOR_2}),
                    dcc.Input(id='input-arrival-delay-in-minutes', type='number', value=0),
                    
                    html.Label("Grupo de Edad", style={"color": SECONDARY_COLOR_2}),
                    dcc.Dropdown(id='input-age-group', options=[{'label': i, 'value': i} for i in ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']], value='25-34'),
                    
                    html.Br(),
                    html.Button('Predecir', id='submit-button', n_clicks=0, style={'backgroundColor': SECONDARY_COLOR_1, 'color': TEXT_COLOR}),
                ], style={'width': '100%', 'max-width': '600px', 'padding': '20px', 'backgroundColor': SECONDARY_COLOR_1, 'border-radius': '10px'})
            ], style={'display': 'flex', 'justify-content': 'center'}),
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
    
    def page_3_content(self):
        return html.Div([
            html.H1("Página 3 - Tabla de Datos", style={"color": PRIMARY_COLOR}),
            dbc.Button(
                "Mostrar/Ocultar Tabla de Datos",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
                style={'backgroundColor': SECONDARY_COLOR_2}
            ),
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody([
                        html.H2("Tabla de datos", style={"color": PRIMARY_COLOR}),
                        dash_table.DataTable(
                            id='tabla-datos',
                            data=df.to_dict('records'),
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
            self.feedback_section()
        ])

    def feedback_section(self):
        return html.Div([
            html.H3("Feedback del Usuario", style={"color": PRIMARY_COLOR}),
            dcc.RadioItems(
                id='user-feedback',
                options=[
                    {'label': 'Predicción Correcta', 'value': 'correct'},
                    {'label': 'Predicción Incorrecta', 'value': 'incorrect'}
                ],
                labelStyle={'display': 'block'}
            ),
            dbc.Button("Enviar Feedback", id="submit-feedback", color="primary", className="mt-2"),
            html.Div(id="feedback-message", className="mt-2")
        ], style={'backgroundColor': SECONDARY_COLOR_1, 'padding': '20px', 'borderRadius': '10px', 'marginTop': '20px'})

    def run(self):
        self.app.run_server(debug=True)

if __name__ == '__main__':
    app_instance = AirlineApp()
    app_instance.run()
