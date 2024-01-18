import dash
import pandas as pd
from dash import Output, Input

from app import calcular_igc


def define_callbacks(app: dash.Dash, df: pd.DataFrame) -> dash.Dash:
    @app.callback(
        Output('output-igc-docente', 'children'),
        Input('selector-professor', 'value'),
        Input('selector-nivel', 'value')
    )
    def update_igc_docente(nome_docente, nivel):
        if nome_docente is not None:
            professor = df.loc[df['NOME_DOCENTE'] == nome_docente]
            if nivel is not None:
                professor = professor.loc[professor['NOME_NIVEL_CURSO_SOLICITACAO_TURMA'] == nivel]

            igc = calcular_igc(professor)

            return f'IGC Docente: {igc:.4f}'
        return 'IGC Docente: 0'

    return app
