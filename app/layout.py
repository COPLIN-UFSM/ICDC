import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
import plotly.graph_objects as go


def define_layout(app: dash.Dash, df: pd.DataFrame) -> dash.Dash:
    selector_professor = dcc.Dropdown(
        options=sorted(df['NOME_DOCENTE'].unique().tolist()),
        placeholder='Selecione',
        multi=False,
        id='selector-professor',
    )

    app.layout = html.Div(
        className='container', children=[
            html.Div(className='row', children=[
                html.Div(className='col', children=[
                    html.H1('Selecione um docente para ver seu IGC para todo o período disponível:'),
                ]),
            ]),
            html.Div(className='row', children=[
                html.Div(className='col', children=[
                    selector_professor,
                ]),
                html.Div(className='col', children=[
                    html.P(className='lead', id='output-igc-docente'),
                    # html.Div([
                    #     "Input: ",
                    #     dcc.Input(id='my-input', value='initial value', type='text')
                    # ]),
                    # html.Br(),
                    # html.Div(id='my-output'),
                ]),
            ]),
        ])

    return app
