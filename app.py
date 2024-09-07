import dash
from dash import dcc, html, State, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from catboost import CatBoostClassifier
import numpy as np
import pandas as pd
import json
from datetime import datetime


PRIMARY_COLOR = "#91C48A"
SECONDARY_COLOR_1 = "#485751"
SECONDARY_COLOR_2 = "#6D9DC5"
SECONDARY_COLOR_3 = "#FFA9A3"
TEXT_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "fafbfd"


def load_catboost_model(model_path):
    model = CatBoostClassifier()
    model.load_model(model_path)
    return model


df = pd.read_csv('Data/airline_passenger_satisfaction.csv')


class AirlineApp:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, "https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap"],suppress_callback_exceptions=True)
        self.app.layout = self.create_layout()
        self.setup_callbacks()
        self.feedback_data = []

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
            [Input('submit-button', 'n_clicks'),
             Input('input-edad', 'value'),
             Input('input-ingresos', 'value'),
             Input('input-genero', 'value')],
        )
        def actualizar_resultados(n_clicks, edad, ingresos, genero):
            if n_clicks > 0:
                input_data = np.array([[edad, ingresos, 1 if genero == 'M' else 0]])
                importancia = {'Característica': ['Edad', 'Ingresos', 'Género'], 'Importancia': [0.4, 0.3, 0.3]}
                importancia_fig = px.bar(importancia, x='Característica', y='Importancia', title='Importancia de las Características')
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
        
        @self.app.callback(
            Output("feedback-message", "children"),
            [Input("submit-feedback", "n-clicks")],
            [State("user-feedabck", "value"),
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