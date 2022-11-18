
from dash import Dash, dcc, html
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


# 1900 width por 930 height
#external_stylesheets = [dbc.themes.BOOTSTRAP]

from pages.page1 import tremap_ticket, tremap_frete, produtos_bar, figura_pagamentos, fig_ticket_vendas, fig_valor_vendas, fig_volume_vendas

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "80px",
    "left": -10,
    "bottom": 0,
    "width": "1920px",
    "height" : "850px",
    "background-color": '#B1B3CB',
}


text_color = {"dark": "#242B24", "light": "#595959"}
card_color = {"dark": "#242B24", "light": "#FFFFFF"}

app = dash.Dash(__name__, 
                meta_tags = [{'name': 'viewport', "content" : "width=device-width, initial-scale=0.19, maximum-scale=5, minimum-scale=0.1, device-height=50"}],
                external_stylesheets = [dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)



# Plot Informacoes
forma_pagamentos = [
    dbc.CardHeader('Formas de Pagamento', style = {'color' : '#010451', 'font-style' : 'bold', 'font-size' : 'large'}),
    dbc.CardBody(
        dcc.Graph(id = 'pie-pag',
                  figure = figura_pagamentos,
                  style = {'height' : "360px", 'width' : "450px"}),
    style = {"background-color": '#B1B3CB', 'height' : "360px"},
    ),
]

ticket_medio = [
    dbc.CardHeader('Ticket Médio', style = {'color' : '#010451', 'font-style' : 'bold', 'font-size' : 'large'}),
    dbc.CardBody(
        dcc.Graph(id = 'ticket-medio',
                  figure = fig_ticket_vendas,
                  style = {'height' : "360px", 'width' : "450px"}),
    style = {"background-color": '#B1B3CB', 'height' : "360px"},
    ),
]

vendas_total = [
    dbc.CardHeader('Valor Vendido', style = {'color' : '#010451', 'font-style' : 'bold', 'font-size' : 'large'}),
    dbc.CardBody(
        dcc.Graph(id = 'valor-vendido',
                  figure = fig_valor_vendas,
                  style = {'height' : "360px", 'width' : "450px"}),
    style = {"background-color": '#B1B3CB', 'height' : "360px"},
    ),
]

volume_vendas = [
    dbc.CardHeader('Volume de Vendas', style = {'color' : '#010451', 'font-style' : 'bold', 'font-size' : 'large'}),
    dbc.CardBody(
        dcc.Graph(id = 'volume-vendido',
                  figure = fig_volume_vendas,
                  style = {'height' : "360px", 'width' : "450px"}),
    style = {"background-color": '#B1B3CB', 'height' : "360px"},
    ),
]


area_informacoes = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Graph(id = 'mapa-ticket', figure = tremap_ticket, style = {'height' : "425px", 'width' : "510px"}),
                                ]
                            ),
                            width = 4,
                            style = {'width' : '510px', "height" : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Graph(id = 'mapa-frete', figure = tremap_frete, style = {'height' : "425px", 'width' : "510px"}),
                                ]
                            ),
                            width = 4,
                            style = {'width' : '510px', "height" : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Graph(id = 'mapa-produtos', figure = produtos_bar, style = {'height' : "425px", 'width' : "900px"}),
                                ]
                            ),
                            width = 4,
                            style = {'width' : '900px', "height" : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                    ],
                    className = 'g-0', #colunas ajustadas sem deixar espaco
                    style = {'width' : '1920px', "height" : "425px"},
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Card(forma_pagamentos, style = {"background-color": '#B1B3CB', 'height' : '425px'}),
                                ]
                            ),
                            width = 3,
                            style = {'width' : '480px', "height" : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Card(ticket_medio, style = {"background-color": '#B1B3CB', 'height' : '425px'}),
                                ]
                            ),
                            width = 3,
                            style = {'width' : '480px', "height" : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Card(vendas_total, style = {"background-color": '#B1B3CB', 'height' : '425px'}),
                                ]
                            ),
                            width = 3,
                            style = {'width' : '480px', "height" : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                         dbc.Col(
                            html.Div(
                                [
                                    dbc.Card(volume_vendas, style = {"background-color": '#B1B3CB', 'height' : '425px'}),
                                ]
                            ),
                            width = 3,
                            style = {'width' : '480px', "height" : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                    ],
                    className = 'g-0', #colunas ajustadas sem deixar espaco
                    style = {'width' : '1920px', "height" : "425px"},
                ),
            ],
            style = SIDEBAR_STYLE,
        )
    ],
)


# Layout
def pagprin():
    layout = html.Div(
        [
            area_informacoes,
        ]
    )
    return layout


