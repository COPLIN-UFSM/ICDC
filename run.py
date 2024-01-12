import argparse
import os
import socket

from dash import Dash
import dash_bootstrap_components as dbc

from app import load_dataframe
from app.callbacks import define_callbacks
from app.layout import define_layout


__title__ = 'IGC Docente'
__script_path__ = os.path.dirname(os.path.abspath(__file__))


def get_host():
    host = '127.0.0.1'  # opção padrão

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        host = s.getsockname()[0]

    return host


def main(database_credentials, views_path):
    app = Dash(
        __title__,
        assets_folder=os.path.join(__script_path__, 'app', 'static'),
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,  # botões bootstrap
            'https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css'  # Boostrap
        ],
        external_scripts=[
            'https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/js/bootstrap.min.js'  # Boostrap
        ]
    )

    df = load_dataframe(database_credentials, views_path)
    app = define_layout(app, df)
    app = define_callbacks(app, df)

    # substitua pelo IP da máquina para permitir que o app seja servido
    # para qualquer computador na rede local
    # e.g. host='172.17.10.165' permite que o servidor seja acessado por
    # http://172.17.10.165:5000/ no navegador
    app.run_server(host=get_host(), port=5000, debug=True, threaded=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Elabora um dashboard com dados do IGC para docentes.'
    )

    parser.add_argument(
        '--database-credentials', action='store', required=True,
        help='Caminho para um arquivo json com as credenciais do banco de dados.'
    )

    parser.add_argument(
        '--views-path', action='store', required=True,
        help='Onde escrever as views lidas do banco de dados'
    )

    args = parser.parse_args()
    main(args.database_credentials, args.views_path)

