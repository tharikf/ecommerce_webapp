from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP, 'seg-style.css']
text_color = {"dark": "#95969A", "light": "#595959"}
card_color = {"dark": "#2D3038", "light": "#FFFFFF"}



# Header
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H2('Olist Brazillian E-commerce'),
                                    dcc.Link(dbc.Button("KPI's", color = 'success', className = 'me-1'),
                                            href = '/', refresh = True),
                                    dcc.Link(dbc.Button('Reviews', color = 'success', className = 'me-1'),
                                            href = '/page2', refresh = True),
                                ],
                            )
                        ],
                        md = True, style = {'color' : '#010451', 'text-align': 'left', "background-color": '#B1B3CB',
                                                            'height' : '80px', 'width' : '1600px'},
                    ),

                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Button('GitHub', color = 'success', className = 'me-1',
                                                href = 'https://github.com/tharikf/Projetos', target = '_blank'),
                                ],
                            )
                        ],
                        md = True, style = {'color' : 'white', 'text-align': 'right', "background-color": '#B1B3CB',
                                                            'height' : '80px', 'width' : '300px'},
                    ),
                ],
                className = 'g-0',
            ),
        ],
        fluid = True,
    ),
    dark = True,
    color = '#B1B3CB',
    sticky = 'top',
    style = {'width' : '1920px', "height" : '80px'},
)


def Navbar():

    layout = html.Div(
        [
            header,
        ]
    )

    return layout