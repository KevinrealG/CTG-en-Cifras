import plotly.express as px
import plotly.graph_objects as go # or plotly.express as px
from plotly.subplots import make_subplots

import pandas as pd
import base64
import datetime
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
#import dash_leaf_leat


tabs_styles = {
    'height': '44px',
    'margin-left': 500,
    'margin-right':500,
    'color':'black',
    'background': 'rgb(210, 232, 255)'
}
tab_style = {
    'border': 'None',
    'padding': '6px',
    'background':'rgb(210, 232, 255)', #AZUL CLARO
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    #'borderBottom': '1px solid #d6d6d6',
    'background-color':'rgb(5, 112, 174)', #AZUL FUERTE
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
    }
#if use px
#fruits = ["apples", "oranges", "bananas"]
#fig = px.line(x=fruits, y=[1,3,2], color=px.Constant("This year"),
#             labels=dict(x="Fruit", y="Amount", color="Time Period"))
#fig.add_bar(x=fruits, y=[2,1,3], name="Last year")

#It's upload the Dinamica Data
path='Data/Mercado laboral_consolidado_.xlsx'
data=pd.read_excel(path,sheet_name='Indicadores')
fig_ocu = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data['TO'][data['AÑO'].size-1],
    delta = {"reference":  data['TO'][data['AÑO'].size-2], "valueformat": ".0f"},
    title = {"text": "Resultado"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

fig_ocu.add_trace(go.Scatter(x=data['TRIMESTRE'],y = data['TO']))
fig_ocu.update_layout(title='Tasa de Ocupación Cartagena, trimestres móviles')

data_2=pd.read_excel(path,sheet_name='Act económica')
table = go.Figure(data=[go.Table(
    header=dict(values=list(data_2.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[data_2[i] for i in data_2.columns],
               fill_color='lavender',
               align='left'))
])
data_3=pd.read_excel(path,sheet_name='ML_Hombres')
data_3_a=data_3.loc[:,'TRIM':'Genero']
#data_3=data_3.rename_axis('Estratos',axis='columns')

fig_gen = px.area(data_3_a, x="TRIM", y="TO",color='Genero', facet_col="Genero", facet_col_wrap=2)
#figy = px.area(data_3_a, facet_col="Estratos", facet_col_wrap=2)

#desocupados
fig_des = make_subplots(specs=[[{"secondary_y": True}]])

fig_des.add_trace(
    go.Scatter(name='Tasa de Desempleo',
        x=data['TRIMESTRE'],
        y=data['TD']
    ),
    secondary_y=True,
    )

fig_des.add_trace(
    go.Bar(name='desocupados',
        x=data['TRIMESTRE'],
        y=data['Desocupados']
    ))
fig_des.update_layout(title='desocupados y tasa de Desempleo Cartagena',barmode='group')
Car_1 = go.Figure(go.Indicator(
mode = "gauge+number",
value =  data['TD'][data['AÑO'].size-1],
title = {'text': "Tasa de Desempleo"},
delta = {'reference':  data['TD'][data['AÑO'].size-2]},
domain = {'x': [0, 1], 'y': [0, 1]}
    ))


def mercado():

    return    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('Data\ctg_cifras.jpg', 'rb').read()).decode()), className="app__logo"),

                                    html.H4("By Kevin Sossa", className="header__text"),
                                ],
                                className="app__header",
                            ),
                            html.Div(
                                [
                                    dcc.Tabs(
                                        id="tabs",
                                        value="data_1",
                                        children=[
                                            dcc.Tab(
                                                label="Ocupación",
                                                value="data_1",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [

                                                            dcc.Graph(id="Ocupación_1",figure=fig_ocu),
                                                            dcc.Graph(id="Ocupación_2",figure=fig_gen),
                                                            dcc.Graph(id="Ocupación_3",figure=table),
                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Desempleo",
                                                value="data_2",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                dcc.Graph(id="Ocupación_1",figure=fig_des),
                                                dcc.Graph(id="Ocupación_2",figure=Car_1),


                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Informales",
                                                value="data_4",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[


                                                ],
                                            ),
                                        ],
                                    )
                                ],
                                className="tabs__container",
                            ),
                        ],
                        className="app__container",
                    )
