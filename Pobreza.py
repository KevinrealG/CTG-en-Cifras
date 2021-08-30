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
path='Data/Pobreza.xlsx'
data_1=pd.read_excel(path,sheet_name='Lineas')
def lineas(Lineas,df=data_1):
    title=''
    if Lineas=='Pobreza':
        title='Historico de Pobreza Monetaria, en Porcentaje Poblacional'
    elif Lineas=='Extrema':
        title='Historico de Pobreza Extrema, en Porcentaje Poblacional'
    else:
        title='Historico del coeficiente de GINI'

    data=df.loc[df['Linea']==Lineas]
    fig = go.Figure(data=[
        go.Scatter( x=data['Año'], y=data['Cartagena'])
        ])
    # Change the bar mode
    fig.update_layout(title=title)

    #go.Pie(labels=labels, values=values, name=variable)
    return fig

data_2=pd.read_excel(path,sheet_name='Pesos')
#data_6=data_6.set_index('Time')
#data_6_a=data_6['Indice Vivienda nueva']
def lineas_pesos(Lineas,df=data_2):
    data=df.loc[df['Linea']==Lineas].reset_index()
    title=''
    if Lineas=='Pobreza':
        title='Historico de Pobreza Monetaria, promedio en Pesos'
    elif Lineas=='Extrema':
        title='Historico de Pobreza Extrema, promedio en Pesos'
    else:
        title='Historico de Ingresos por unidad familiar, en Pesos'


    fig_ivn = go.Figure(go.Indicator(

        mode = "number+delta",
        value = data['Cartagena'][data['Año'].size-1],
        delta = {"reference":  data['Cartagena'][data['Año'].size-2], "valueformat": ".0f"},
        title = {"text": "Resultado"},
        domain = {'y': [0, 1], 'x': [0.25, 0.75]})
        )

    fig_ivn.add_trace(go.Scatter(x=data['Año'],y = data['Cartagena']))
    fig_ivn.update_layout(title=title)

    return fig_ivn

data_3=pd.read_excel(path,sheet_name='Pobreza E. T')
#data_3_a=data_3.loc[data_3['Linea']=='Pobreza'].drop('Linea')
data_3_a=data_3.set_index('AÑO')
#data_3_a=data_3_a.drop('Linea')
data_3_a=data_3_a.rename_axis('Ciudad',axis='columns')
data_3_a=data_3_a.T
data_3_b=pd.read_excel(path,sheet_name='Pobreza T')

data_3_b=data_3_b.set_index('Año')
#data_3_b=data_3_b.drop('Linea')
data_3_b=data_3_b.rename_axis('Ciudad',axis='columns')
data_3_b=data_3_b.T
def Comparativo(year=2020,df=data_3_a,df1=data_3_b):

    new_df=df[year]
    #print(new_df)
    new_df=new_df.sort_values(ascending=True)
    new=df1[year]
    new=new.sort_values(ascending=True)
    #best=new_df.head(5)
    #best=new_df.tail(5)
    fig = px.bar(new_df, x=new_df.values, y=new_df.index, orientation='h')
    fig.update_layout(title='Comparativo Pobreza Monetaria '+str(year))
    fig_best= px.bar(new, x=new.values, y=new.index, orientation='h')
    fig_best.update_layout(title='Comparativo Pobreza Extrema '+str(year))

    return fig, fig_best
data_4=pd.read_excel(path,sheet_name='deficit por')
fig_4 = px.bar(data_4, x=data_4['Tipo'], y=data_4['Deficit'],color="Tipo de deficit")
fig_4.update_layout(title='Deficit Habitacional Cartagena',barmode='group')

data_5=pd.read_excel(path,sheet_name='deficit ciudades')
fig5 = go.Figure(data=[
    go.Bar(name='Deficit cuantitativo', x=data_5['Nombre Municipio'], y=data_5['Déficit cuantitativo']),
    go.Bar(name='Deficit cualitativo', x=data_5['Nombre Municipio'], y=data_5['Déficit cualitativo'])
])
# Change the bar mode
fig5.update_layout(title='Camparación de Deficit Habitacional, Ciudades principales',barmode='stack')
data_5=pd.read_excel(path,sheet_name='deficit cartagena')
Car_1 = go.Figure(go.Indicator(
mode = "gauge+number",
value = data_5['Hogares en déficit cuantitativo'][0],
title = {'text': "Hogares en déficit cuantitativo"},
delta = {'reference':  data_5['Total de hogares'][0]},
domain = {'x': [0, 1], 'y': [0, 1]}
    ))
Car_2 = go.Figure(go.Indicator(
mode = "gauge+number",
value = data_5['Hogares en déficit cualitativo'][0],
title = {'text': "Hogares en déficit cualitativo"},
delta = {'reference':  data_5['Total de hogares'][0]},
domain = {'x': [0, 1], 'y': [0, 1]}
    ))
Car_3 = go.Figure(go.Indicator(
mode = "gauge+number",
value = data_5['Hogares en déficit habitacional'][0],
title = {'text': "Hogares en déficit habitacional"},
delta = {'reference':  data_5['Total de hogares'][0]},
domain = {'x': [0, 1], 'y': [0, 1]}
    ))
def pobreza():

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
                                        value="data-entry",
                                        children=[
                                            dcc.Tab(
                                                label="Lineas de Pobreza",
                                                value="data_1",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [
                                                            html.H4("Lineas de Pobreza", className="header__text"),
                                                            html.P("Lineas:"),
                                                            dcc.Dropdown(
                                                                id='linea_drop',
                                                                value='Pobreza',
                                                                options=[{'value': x, 'label': x}
                                                                         for x in ['Pobreza', 'Extrema', 'GINI']],
                                                                clearable=False
                                                            ),

                                                            dcc.Graph(id="Lineas_1"),

                                                            html.H4("INGRESOS y lineas de pobreza, en Pesos", className="header__text"),
                                                            html.P("Lineas:"),
                                                            dcc.Dropdown(
                                                                id='linea_pesos',
                                                                value='Extrema',
                                                                options=[{'value': x, 'label': x}
                                                                         for x in ['Pobreza', 'Extrema']],
                                                                clearable=False
                                                            ),

                                                            dcc.Graph(id="Lineas_2"),
                                                            html.H3('Año'),
                                                            dcc.Dropdown(
                                                                id='year_pobre',
                                                                value=2019,
                                                                options=[{'value': x, 'label': x}
                                                                         for x in range(2015,2020)],
                                                                clearable=False
                                                            ),
                                                            dcc.Graph(id="Lineas_3"),
                                                            dcc.Graph(id="Lineas_4"),
                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Deficit",
                                                value="data_2",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[


                                                dcc.Graph(figure=fig_4),
                                                dcc.Graph(figure=fig5),
                                                dcc.Graph(figure=Car_1),
                                                dcc.Graph(figure=Car_2),
                                                dcc.Graph(figure=Car_3),



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
