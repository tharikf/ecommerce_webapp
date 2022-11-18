import pandas as pd
import numpy as np
from dash import Dash, dcc, html
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import nltk
import spacy
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings('ignore')

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "80px",
    "left": -10,
    "bottom": 0,
    "width": "1920px",
    "height" : "850px",
    "background-color": '#B1B3CB',
}


# Ideias

# Serie temporal do Review em 2018 (por mes)
# Nota media do review por Estado em 2018 ultimos 3 meses (em tabs)
# Analise das mensagens
# Procurar analisar as mensagens com notas baixas

from pages.page1 import analise_01

analise4 = analise_01[['status_compra', 'preco', 'frete', 'data_pgto_aprovado','estado_cliente', 'pontuacao_review', 'titulo_review',
                      'mensagem_review', 'diff_entrega_pgto_aprovado', 'regiao_pais']]


# Analisando a media em 2018
review_medio_18 = analise4[analise4['data_pgto_aprovado'] > '2018']
review_medio_18 = review_medio_18.groupby(['data_pgto_aprovado'], as_index = False)['pontuacao_review'].mean()

review_medio_18_fig = go.Figure()
review_medio_18_fig = px.line(x = review_medio_18['data_pgto_aprovado'], y = review_medio_18['pontuacao_review'],
                                color_discrete_sequence = ['#1E3685'], template = 'plotly_white')
review_medio_18_fig.update_layout(margin = dict(t=50, l=250, r=0, b=0), title = '',
                                    title_x = 0.5, xaxis_title = '', yaxis_title = 'Nota do Review',
                                    paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB')

# Nota media do Review por Estado ultimos 3 meses de 2018
# Meses 6, 7 e 8
review_estado_mes6 = analise4[analise4['data_pgto_aprovado'] == '2018-06']
review_estado_mes6 = review_estado_mes6.groupby(['estado_cliente'], as_index = False)['pontuacao_review'].mean()
review_estado_mes7 = analise4[analise4['data_pgto_aprovado'] == '2018-07']
review_estado_mes7 = review_estado_mes7.groupby(['estado_cliente'], as_index = False)['pontuacao_review'].mean()
review_estado_mes8 = analise4[analise4['data_pgto_aprovado'] == '2018-08']
review_estado_mes8 = review_estado_mes8.groupby(['estado_cliente'], as_index = False)['pontuacao_review'].mean()

unindo_dfs = analise4[['estado_cliente', 'regiao_pais']]
unindo_dfs = unindo_dfs.drop_duplicates().reset_index()
unindo_dfs = unindo_dfs[['estado_cliente', 'regiao_pais']]

review_estado_mes6 = review_estado_mes6.merge(unindo_dfs, on = 'estado_cliente', how = 'inner')
review_estado_mes7 = review_estado_mes7.merge(unindo_dfs, on = 'estado_cliente', how = 'inner')
review_estado_mes8 = review_estado_mes8.merge(unindo_dfs, on = 'estado_cliente', how = 'inner')

tremap_review_junho = px.treemap(review_estado_mes6, path = [px.Constant('Review Médio em Junho'), 'regiao_pais', 'estado_cliente'],
                 values = 'pontuacao_review')
tremap_review_junho.update_traces(textposition = 'middle center', marker_colors = ['blues'], texttemplate = "%{label}<br>%{value:.2f}")
tremap_review_junho.update_layout(margin = dict(t=0, l=150, r=0, b=80), paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB')

tremap_review_julho = px.treemap(review_estado_mes7, path = [px.Constant('Review Médio em Julho'), 'regiao_pais', 'estado_cliente'],
                 values = 'pontuacao_review')
tremap_review_julho.update_traces(textposition = 'middle center', marker_colors = ['blues'], texttemplate = "%{label}<br>%{value:.2f}")
tremap_review_julho.update_layout(margin = dict(t=0, l=150, r=0, b=80), paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB')

tremap_review_agosto = px.treemap(review_estado_mes8, path = [px.Constant('Review Médio em Agosto'), 'regiao_pais', 'estado_cliente'],
                 values = 'pontuacao_review')
tremap_review_agosto.update_traces(textposition = 'middle center', marker_colors = ['blues'], texttemplate = "%{label}<br>%{value:.2f}")
tremap_review_agosto.update_layout(margin = dict(t=0, l=150, r=0, b=80), paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB')

cards_reviews_mensais = [
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'review-junho',
                                figure = tremap_review_junho,
                                style = {'height' : "400px", 'width' : "800px"}),
                                style = {"background-color": '#B1B3CB', 'height' : "425px"},
                ), 
            label = 'Junho'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'review-julho',
                                figure = tremap_review_julho,
                                style = {'height' : "400px", 'width' : "800px"}),
                                style = {"background-color": '#B1B3CB', 'height' : "425px"},
        ), label = 'Julho'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'review-agosto',
                                figure = tremap_review_agosto,
                                style = {'height' : "400px", 'width' : "800px"}),
                                style = {"background-color": '#B1B3CB', 'height' : "425px"},
        ), label = 'Agosto'
            ),
        ],
    ),
]

# Analisando Titulos
nltk.download('all', quiet = True)
titulos = analise4[analise4['pontuacao_review'] < 3]
titulos = titulos['titulo_review']
titulos = titulos.dropna()
titulos = titulos.str.lower()
titulos = titulos.astype(str)

tokenizer = TreebankWordTokenizer()
portugues_stops = set(stopwords.words('portuguese'))

titulos = [tokenizer.tokenize(palavra) for palavra in titulos]
titulos = [i for palavra in titulos for i in palavra]
titulos = [palavra for palavra in titulos if palavra not in portugues_stops]

lista_remove = ["-", "—",",", ".", "'", "`", "´", "~", "^", "'s", "'t", "``", '"', "–", "$", "!", ")", "(", "?", "..."]
titulos = [palavra for palavra in titulos if palavra not in lista_remove]

titulos = [palavra for palavra in titulos if len(palavra) > 2]

wordnet_lemmatizer = WordNetLemmatizer()
titulos = [wordnet_lemmatizer.lemmatize(i) for i in titulos]

# Métricas de associação de bigramas (esse objeto possui diversos atributos, como freq, pmi, teste t, etc...)
trigramas = nltk.collocations.TrigramAssocMeasures()
quadrigramas = nltk.collocations.QuadgramAssocMeasures()

buscaTrigramas = nltk.collocations.TrigramCollocationFinder.from_words(titulos)
buscaQuadrigramas = nltk.collocations.QuadgramCollocationFinder.from_words(titulos)

trigrama_freq = buscaTrigramas.ngram_fd.items()
quadrigrama_freq = buscaQuadrigramas.ngram_fd.items()

# Tabela de frequência no formato do Pandas para os trigramas
FreqTabTrigramas = pd.DataFrame(list(trigrama_freq), 
                                columns = ['Trigrama','Frequencia']).sort_values(by = 'Frequencia', ascending = False)

# Tabela de frequência no formato do Pandas para os trigramas
FreqTabQuadrigramas = pd.DataFrame(list(quadrigrama_freq), 
                                columns = ['Quadrigrama','Frequencia']).sort_values(by = 'Frequencia', ascending = False)

fig_tri = go.Figure(
    data = [go.Table(
        header = dict(values = list(FreqTabTrigramas.columns),
        fill_color = 'paleturquoise',
        align = 'left', font_size = 14, height = 30),
    cells = dict(values = [FreqTabTrigramas.Trigrama, FreqTabTrigramas.Frequencia],
                fill_color = 'lavender', align = 'left', font_size = 12, height = 30)
    )]
)

fig_tri.update_layout(paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB', margin = dict(t=0, b=40, l=110, r=0))

fig_quad = go.Figure(
    data = [go.Table(
        header = dict(values = list(FreqTabQuadrigramas.columns),
        fill_color = 'paleturquoise',
        align = 'left', font_size = 14, height = 30),
    cells = dict(values = [FreqTabQuadrigramas.Quadrigrama, FreqTabQuadrigramas.Frequencia],
                fill_color = 'lavender', align = 'left', font_size = 12, height = 30)
    )]
)
fig_quad.update_layout(paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB', margin = dict(t=0, b=40, l=110, r=0))

# Analisando Reviews
reviews = analise4[analise4['pontuacao_review'] < 3]
reviews = reviews['mensagem_review']
reviews = reviews.dropna()
reviews = reviews.str.lower()
reviews = reviews.astype(str)

tokenizer = TreebankWordTokenizer()
portugues_stops = set(stopwords.words('portuguese'))

reviews = [tokenizer.tokenize(palavra) for palavra in reviews]
reviews = [i for palavra in reviews for i in palavra]
reviews = [palavra for palavra in reviews if palavra not in portugues_stops]

reviews = [palavra for palavra in reviews if palavra not in lista_remove]

reviews = [palavra for palavra in reviews if len(palavra) > 2]

wordnet_lemmatizer = WordNetLemmatizer()
reviews = [wordnet_lemmatizer.lemmatize(i) for i in reviews]

# Métricas de associação de bigramas (esse objeto possui diversos atributos, como freq, pmi, teste t, etc...)
buscaTrigramas_rev = nltk.collocations.TrigramCollocationFinder.from_words(reviews)
buscaQuadrigramas_rev = nltk.collocations.QuadgramCollocationFinder.from_words(reviews)

trigrama_freq_rev = buscaTrigramas_rev.ngram_fd.items()
quadrigrama_freq_rev = buscaQuadrigramas_rev.ngram_fd.items()

# Tabela de frequência no formato do Pandas para os trigramas
FreqTabTrigramas_rev = pd.DataFrame(list(trigrama_freq_rev), 
                                columns = ['Trigrama','Frequencia']).sort_values(by = 'Frequencia', ascending = False)

# Tabela de frequência no formato do Pandas para os trigramas
FreqTabQuadrigramas_rev = pd.DataFrame(list(quadrigrama_freq_rev), 
                                columns = ['Quadrigrama','Frequencia']).sort_values(by = 'Frequencia', ascending = False)

rev_tri = go.Figure(
    data = [go.Table(
        header = dict(values = list(FreqTabTrigramas_rev.columns),
        fill_color = 'paleturquoise',
        align = 'left', font_size = 14, height = 30),
    cells = dict(values = [FreqTabTrigramas_rev.Trigrama, FreqTabTrigramas_rev.Frequencia],
                fill_color = 'lavender', align = 'left', font_size = 12, height = 30)
    )]
)
rev_tri.update_layout(paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB', margin = dict(t=0, b=40, l=110, r=0))

rev_quad = go.Figure(
    data = [go.Table(
        header = dict(values = list(FreqTabQuadrigramas_rev.columns),
        fill_color = 'paleturquoise',
        align = 'left', font_size = 14, height = 30),
    cells = dict(values = [FreqTabQuadrigramas_rev.Quadrigrama, FreqTabQuadrigramas_rev.Frequencia],
                fill_color = 'lavender', align = 'left', font_size = 12, height = 30)
    )]
)
rev_quad.update_layout(paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB', margin = dict(t=0, b=40, l=110, r=0))


palavras_titulo = [
    dbc.CardHeader('Palavras mais Frequentes nos Títulos'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'tri-titulo',
                                figure = fig_tri,
                                style = {'height' : "360px", 'width' : "800px"}),
                style = {"background-color": '#B1B3CB', 'height' : "360px"},
        ), label = 'Trigramas',

            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'quad-titulo',
                                figure = fig_quad,
                                style = {'height' : "360px", 'width' : "800px"}),
                style = {"background-color": '#B1B3CB', 'height' : "360px"},
        ), label = 'Quadrigramas'
            ),
        ],
    ),
]

palavras_review = [
    dbc.CardHeader('Palavras mais Frequentes nos Reviews'),
    dbc.Tabs(
        [
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'tri-titulo',
                                figure = rev_tri,
                                style = {'height' : "360px", 'width' : "800px"}),
                                style = {"background-color": '#B1B3CB', 'height' : "360px"},
        ), label = 'Trigramas'
            ),
            dbc.Tab(
                dbc.CardBody(
                    dcc.Graph(id = 'quad-titulo',
                                figure = rev_quad,
                                style = {'height' : "360px", 'width' : "800px"}),
                                style = {"background-color": '#B1B3CB', 'height' : "360px"},
        ), label = 'Quadrigramas'
            ),
        ],
    ),
]


# Plot Informacoes
area_informacoes = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Graph(id = 'mapa-review-18', figure = review_medio_18_fig, style = {'height' : "360px", 'width' : "800px"}),
                                ],
                            ),
                            width = 6,
                            style = {'width' : '960px', 'height' : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Card(cards_reviews_mensais, style = {"background-color": '#B1B3CB'}),
                                ]
                            ),
                            width = 6,
                            style = {'width' : '960px', 'height' : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                    ],
                    className = 'g-0', #colunas ajustadas sem deixar espaco
                    style = {'width' : '1920px', 'height' : "425px"},
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Card(palavras_titulo, style = {"background-color": '#B1B3CB', 'height' : '425px'}),
                                ],
                            ),
                            width = 6,
                            style = {'width' : '960px', 'height' : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Card(palavras_review, style = {"background-color": '#B1B3CB', 'height' : '425px'}),
                                ]
                            ),
                            width = 6,
                            style = {'width' : '960px', 'height' : "425px"},
                            xs=0, sm='576px', md=True,
                        ),
                    ],
                    className = 'g-0', #colunas ajustadas sem deixar espaco
                    style = {'width' : '1920px', 'height' : "425px"},
                ),
            ],
            style = SIDEBAR_STYLE,
        )
    ],
)

# Layout
layout = html.Div(
    [
        area_informacoes,
    ]
)