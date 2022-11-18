import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Importando dados customers_dataset
dados_cliente = pd.read_csv('olist_customers_dataset.csv')
dados_cliente = dados_cliente.drop_duplicates(['customer_id'])
dados_cliente = dados_cliente.iloc[:, [0, 3, 4]]
dados_cliente.set_axis(['id_cliente', 'cidade_cliente', 'estado_cliente'], axis = 1, inplace = True)

# Importando dados order_itens
dados_compra = pd.read_csv('olist_order_items_dataset.csv')
dados_compra = dados_compra.drop_duplicates(['order_id'])
dados_compra = dados_compra.iloc[:, [0, 2, 3, 4, 5, 6]]
dados_compra.set_axis(['id_compra', 'id_produto', 'id_vendedor', 'envio_limite', 'preco', 'frete'], axis = 1, inplace = True)

# Importando dados order_payments
dados_compra_pgto = pd.read_csv('olist_order_payments_dataset.csv')
dados_compra_pgto = dados_compra_pgto.drop_duplicates(['order_id'])
dados_compra_pgto = dados_compra_pgto.iloc[:, [0, 2, 3, 4]]
dados_compra_pgto.set_axis(['id_compra', 'tipo_pagamento', 'parcelas', 'valor_pagamento'], axis = 1, inplace = True)

# Importando dados reviews
dados_review = pd.read_csv('olist_order_reviews_dataset.csv')
dados_review = dados_review.drop_duplicates(['order_id'])
dados_review = dados_review.iloc[:, [1, 2, 3, 4]]
dados_review.set_axis(['id_compra', 'pontuacao_review', 'titulo_review', 'mensagem_review'], axis = 1, inplace = True)

# Importando dados orders dataset
dados_compra_status = pd.read_csv('olist_orders_dataset.csv')
dados_compra_status = dados_compra_status.drop_duplicates(['order_id'])
dados_compra_status = dados_compra_status.iloc[:, [0, 1, 2, 4, 7]]
dados_compra_status.set_axis(['id_compra', 'id_cliente', 'status_compra', 'data_pgto_aprovado',
                              'data_compra_entregue'], axis = 1, inplace = True)

# Importando dados products dataset
dados_produtos = pd.read_csv('olist_products_dataset.csv')
dados_produtos = dados_produtos.drop_duplicates(['product_id'])
dados_produtos = dados_produtos.iloc[:, [0, 1]]
dados_produtos.set_axis(['id_produto', 'categoria_produto'], axis = 1, inplace = True)

# Importando dados sellers dataset
dados_vendedores = pd.read_csv('olist_sellers_dataset.csv')
dados_vendedores = dados_vendedores.drop_duplicates(['seller_id'])
dados_vendedores = dados_vendedores.iloc[:, [0, 2, 3]]
dados_vendedores.set_axis(['id_vendedor', 'cidade_vendedor', 'estado_vendedor'], axis = 1, inplace = True)

# Carregamento concluido #

# Análise 1 #

# Fazendo análise de review e o tempo entre o pagamento aprovado e o recebimento do produto. #
# Olhando, também, para o valor do produto, valor do frete e o estado. #

analise_01 = dados_compra.merge(dados_review, on = 'id_compra', how = 'inner')
analise_01 = analise_01.merge(dados_compra_status, on = 'id_compra', how = 'inner')
analise_01 = analise_01.merge(dados_cliente, on = 'id_cliente', how = 'inner')
analise_01 = analise_01.drop(['id_compra', 'id_produto', 'id_vendedor', 'id_cliente'], axis = 1)

analise_01 = analise_01[['status_compra', 'preco', 'frete', 'envio_limite', 'data_pgto_aprovado', 'data_compra_entregue',
                         'cidade_cliente', 'estado_cliente', 'pontuacao_review', 'titulo_review', 'mensagem_review']]


# Transformando as colunas
# DEFINIR UMA FUNCAO
def func(x):
    return pd.to_datetime(x).dt.date

cols = ['envio_limite', 'data_pgto_aprovado', 'data_compra_entregue']
analise_01[cols] = analise_01[cols].apply(func)

analise_01['diff_entrega_pgto_aprovado'] = (analise_01['data_compra_entregue'] - analise_01['data_pgto_aprovado']).dt.days

# removendo valor que é menor que 0 pois é um erro
analise_01 = analise_01[analise_01['diff_entrega_pgto_aprovado'] > 0]
analise_01 = analise_01[analise_01['status_compra'] == 'delivered']
analise_01['cidade_cliente'] = analise_01['cidade_cliente'].str.upper()

# colocando as regioes do brasil
sudeste = ['RJ', 'SP', 'MG', 'ES']
sul = ['RS', 'SC', 'PR']
nordeste = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
norte = ['AC', 'AM', 'PA', 'RO', 'RR', 'TO', 'AP']
centro_oeste = ['DF', 'GO', 'MT', 'MS']

analise_01['regiao_pais'] = 0
analise_01['regiao_pais'] = np.where(np.isin(analise_01['estado_cliente'], sudeste), 'SUDESTE', analise_01['regiao_pais'])
analise_01['regiao_pais'] = np.where(np.isin(analise_01['estado_cliente'], sul), 'SUL', analise_01['regiao_pais'])
analise_01['regiao_pais'] = np.where(np.isin(analise_01['estado_cliente'], nordeste), 'NORDESTE', analise_01['regiao_pais'])
analise_01['regiao_pais'] = np.where(np.isin(analise_01['estado_cliente'], norte), 'NORTE', analise_01['regiao_pais'])
analise_01['regiao_pais'] = np.where(np.isin(analise_01['estado_cliente'], centro_oeste), 'CENTRO-OESTE', analise_01['regiao_pais'])


# Iniciando anaise de serie temporal
info_serie_temporal = analise_01
info_serie_temporal['data_pgto_aprovado'] = pd.to_datetime(info_serie_temporal['data_pgto_aprovado']).dt.strftime('%Y-%m')
info_serie_temporal = info_serie_temporal[info_serie_temporal['data_pgto_aprovado'] > '2016-12']

info_serie_temporal = info_serie_temporal.groupby(['data_pgto_aprovado']).agg({'preco' : ['mean', 'sum', 'size'],
                                                                               'pontuacao_review' : 'mean'})
info_serie_temporal.columns = info_serie_temporal.columns.droplevel(0)
info_serie_temporal = info_serie_temporal.reset_index()
info_serie_temporal.columns = ['data_pgto_aprovado', 'preco_medio', 'valor_total', 'volume_total', 'review_medio']

# Dados de inflacao
# inflacao periodo
inflacao = pd.read_csv('inflacao_periodo.csv', sep = ';')
inflacao = inflacao.iloc[0:20, ]
inflacao = inflacao.rename(columns = {'433 - Broad National Consumer Price Index (IPCA) - Monthly % var.' : 'taxa_mensal',
                                     'Date' : 'mes'})
inflacao['taxa_mensal'] = pd.to_numeric(inflacao['taxa_mensal'])
inflacao['taxa_mensal_perc'] = (inflacao['taxa_mensal'] / 100)
inflacao['inflacao_mensal'] = inflacao['taxa_mensal_perc'] + 1
inflacao['inflacao_acumulada'] = np.cumprod(inflacao['inflacao_mensal'])
inflacao['mes'] = pd.to_datetime(inflacao['mes']).dt.strftime('%Y-%m')

info_serie_temporal = info_serie_temporal.join(inflacao['inflacao_acumulada'])

# a analise é de 2017 em diante pois nao há valores para novembro 2016 e valores muito baixos para dois meses do fim de 2016
info_serie_temporal['preco_medio_ajustado'] = (info_serie_temporal['preco_medio'] / info_serie_temporal['inflacao_acumulada'])
info_serie_temporal['valor_total_ajustado'] = round((info_serie_temporal['valor_total'] / info_serie_temporal['inflacao_acumulada']), 2)

# Valor Total com Ajuste da Inflacao
vendas_agosto = info_serie_temporal[info_serie_temporal['data_pgto_aprovado'] == '2018-08']['valor_total_ajustado'].item()
vendas_medio_18 = info_serie_temporal[info_serie_temporal['data_pgto_aprovado'] >= '2018']['valor_total_ajustado'].mean()


fig_valor_vendas = go.Figure()
fig_valor_vendas.add_trace(go.Indicator(
mode = 'number+delta',
number = {'valueformat' : ',.2f', 'prefix' : 'R$', 'font' : {'size' : 42}},
value = vendas_agosto,
delta = {'reference' : vendas_medio_18, 'relative' : True, 'valueformat' : '.2%', 'font' : {'size' : 30}},
title = {'text' : 'Agosto - 2018', 'font' : {'size' : 22}},
))
fig_valor_vendas.update_layout(paper_bgcolor = "#B1B3CB")

# Ticket Medio com Ajuste da Inflacao
ticket_agosto = info_serie_temporal[info_serie_temporal['data_pgto_aprovado'] == '2018-08']['preco_medio_ajustado'].item()
ticket_medio_18 = info_serie_temporal[info_serie_temporal['data_pgto_aprovado'] >= '2018']['preco_medio_ajustado'].mean()

fig_ticket_vendas = go.Figure()
fig_ticket_vendas.add_trace(go.Indicator(
mode = 'number+delta',
number = {'valueformat' : ',.2f', 'prefix' : 'R$', 'font' : {'size' : 42}},
value = ticket_agosto,
delta = {'reference' : ticket_medio_18, 'relative' : True, 'valueformat' : '.2%', 'font' : {'size' : 30}},
title = {'text' : 'Agosto - 2018', 'font' : {'size' : 22}},
))
fig_ticket_vendas.update_layout(paper_bgcolor = "#B1B3CB")

# Volume de Vendas
volume_agosto = info_serie_temporal[info_serie_temporal['data_pgto_aprovado'] == '2018-08']['volume_total'].item()
volume_medio_18 = info_serie_temporal[info_serie_temporal['data_pgto_aprovado'] >= '2018']['volume_total'].mean()


fig_volume_vendas = go.Figure()
fig_volume_vendas.add_trace(go.Indicator(
mode = 'number+delta',
number = {'valueformat' : ',.2f', 'font' : {'size' : 42}},
value = volume_agosto,
delta = {'reference' : volume_medio_18, 'relative' : True, 'valueformat' : '.2%', 'font' : {'size' : 30}},
title = {'text' : 'Agosto - 2018', 'font' : {'size' : 22}},
))
fig_volume_vendas.update_layout(paper_bgcolor = "#B1B3CB")

# Mapas
# analisando pontuacao do rewview, valor do frete e dias de entrega de acordo com o estado
info_por_estado = analise_01.groupby(['estado_cliente']).agg({'preco' : 'mean', 'frete' : 'mean',
                                                              'pontuacao_review' : 'mean',
                                                              'diff_entrega_pgto_aprovado' : 'mean'})

colunas = ['preco', 'frete', 'pontuacao_review', 'diff_entrega_pgto_aprovado']

for col in colunas:
    info_por_estado[col] = round(info_por_estado[col], 2)

info_por_estado = info_por_estado.sort_values(by = 'preco', ascending = True).reset_index()

info_por_estado['regiao_pais'] = 0
info_por_estado['regiao_pais'] = np.where(np.isin(info_por_estado['estado_cliente'], sudeste), 'SUDESTE', info_por_estado['regiao_pais'])
info_por_estado['regiao_pais'] = np.where(np.isin(info_por_estado['estado_cliente'], sul), 'SUL', info_por_estado['regiao_pais'])
info_por_estado['regiao_pais'] = np.where(np.isin(info_por_estado['estado_cliente'], nordeste), 'NORDESTE', info_por_estado['regiao_pais'])
info_por_estado['regiao_pais'] = np.where(np.isin(info_por_estado['estado_cliente'], norte), 'NORTE', info_por_estado['regiao_pais'])
info_por_estado['regiao_pais'] = np.where(np.isin(info_por_estado['estado_cliente'], centro_oeste), 'CENTRO-OESTE', info_por_estado['regiao_pais'])  

tremap_ticket = px.treemap(info_por_estado, path = [px.Constant('Ticket Médio por Região e Estado'), 'regiao_pais', 'estado_cliente'],
                 values = 'preco')
tremap_ticket.update_traces(textposition = 'middle center', marker_colors = ['blues'], texttemplate = "%{label}<br>R$%{value:.2f}")
tremap_ticket.update_layout(margin = dict(t=50, l=25, r=25, b=25), paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB')


tremap_frete = px.treemap(info_por_estado, path = [px.Constant('Frete Médio por Região e Estado'), 'regiao_pais', 'estado_cliente'],
                 values = 'diff_entrega_pgto_aprovado')
tremap_frete.update_traces(textposition = 'middle center', marker_colors = ['blues'], texttemplate = "%{label}<br>R$%{value:.2f}")
tremap_frete.update_layout(margin = dict(t=50, l=25, r=25, b=25), paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB')

# Sobre os Produtos
analise_02 = dados_compra_pgto.merge(dados_compra, how = 'inner', on = 'id_compra')
analise_02 = analise_02.merge(dados_produtos, how = 'inner', on = 'id_produto')
analise_02 = analise_02.merge(dados_compra_status, how = 'inner', on = 'id_compra')
analise_02 = analise_02.merge(dados_cliente, how = 'inner', on = 'id_cliente')
analise_02 = analise_02[['categoria_produto', 'data_pgto_aprovado', 'preco', 'frete', 'valor_pagamento',
                        'parcelas', 'tipo_pagamento', 'status_compra', 'estado_cliente']]

analise_02 = analise_02[analise_02['status_compra'] == 'delivered']

analise_02['data_pgto_aprovado'] = pd.to_datetime(analise_02['data_pgto_aprovado']).dt.strftime('%Y-%m')

categoria_produtos = analise_02.categoria_produto.value_counts()

colunas = ['cama_mesa_banho', 'beleza_saude', 'esporte_lazer', 'informatica_acessorios', 'moveis_decoracao',
          'utilidades_domesticas', 'relogios_presentes', 'telefonia', 'automotivo', 'brinquedos']
analise_02['Categorias'] = [x if x in colunas else 'Outros' for x in analise_02.categoria_produto]

info_por_categoria = analise_02.groupby(['Categorias']).agg({'preco' : 'mean',
                                                                   'frete' : 'mean',
                                                                  'Categorias' : 'size'}).rename(columns = {'Categorias' : 'size'}).reset_index()
info_por_categoria['Categorias'] = info_por_categoria['Categorias'].str.replace('_', '/')
info_por_categoria = info_por_categoria.sort_values(by = 'size', ascending = False)

info_por_categoria['Categorias'] = info_por_categoria['Categorias'].str.replace('/', ' e ')
info_por_categoria['Categorias'] = info_por_categoria['Categorias'].str.replace('cama e mesa', 'cama, mesa')
info_por_categoria['Categorias'] = info_por_categoria['Categorias'].str.title()
info_por_categoria['Categorias'] = info_por_categoria['Categorias'].str.replace('E', 'e')

info_por_categoria['preco'] = round(info_por_categoria['preco'], 2)

info_por_categoria = info_por_categoria.rename({'preco' : 'Preco'}, axis = 1)

produtos_bar = px.bar(info_por_categoria, x = 'Categorias', y = 'Preco', color_discrete_sequence = ['#04890A'])

produtos_bar.update_layout(title = 'Preço Médio por Categoria', title_x = 0.5, xaxis_title = '', yaxis_title = '',
                            paper_bgcolor = '#B1B3CB', plot_bgcolor = '#B1B3CB', xaxis = {'categoryorder' : 'total descending'})

produtos_bar.update_xaxes(tickfont = {'color' : '#010451', 'size' : 12})
produtos_bar.update_yaxes(tickprefix = 'R$', tickfont = {'color' : '#010451', 'size' : 12})

# Formas de pagamento
info_por_pagamento = analise_02.groupby(['tipo_pagamento']).agg({'preco' : 'mean',
                                                                 'tipo_pagamento' : 'size'}).rename(columns = {'tipo_pagamento' : 'size'}).reset_index()
info_por_pagamento['tipo_pagamento'] = info_por_pagamento['tipo_pagamento'].str.replace('_', ' ').str.title()
info_por_pagamento['preco'] = info_por_pagamento['preco'].round(2)

figura_pagamentos = px.pie(info_por_pagamento, values = 'size', names = 'tipo_pagamento', title = '')
figura_pagamentos.update_traces(textposition = 'outside', textinfo = 'percent+label', pull = [0, 0.2, 0, 0])
figura_pagamentos.update_layout(paper_bgcolor = "#B1B3CB")


# Reviews
analise_03 = dados_vendedores.merge(dados_compra, how = 'inner', on = 'id_vendedor')
analise_03 = analise_03.merge(dados_review, how = 'inner', on = 'id_compra')
analise_03 = analise_03.merge(dados_compra_status, how = 'inner', on = 'id_compra')
analise_03 = analise_03.merge(dados_cliente, how = 'inner', on = 'id_cliente')
analise_03 = analise_03[['estado_vendedor', 'preco', 'pontuacao_review', 'mensagem_review', 'status_compra',
                         'data_pgto_aprovado']]





