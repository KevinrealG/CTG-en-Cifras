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
import openpyxl



tabs_styles = {
    'height': '44px',
    'margin-left': 500,
    'margin-right':500,
    'color':'black',
    'background': 'rgb(229,45,39)'
}
tab_style = {
    'border': 'None',
    'padding': '6px',
    'background':'rgb(229,45,39)', #rojo CLARO
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    #'borderBottom': '1px solid #d6d6d6',
    'background-color':'rgb(179, 18, 23)', #rojo FUERTE
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
    }
title_style={
    'textAlign': 'center',
    'color':'black'
}
path='Data/Turismo_consolidado_13.8.21.xlsx'
df_1=pd.read_excel(path,sheet_name='Ocupación_mensual')

df_1['date']= pd.to_datetime(df_1[["year", "month", "day"]])
color=['#ffaa00']*(df_1['linea'].size)
#df_2=df_1.loc[df_1['year']==2020]
animada_ocup=px.bar(df_1, x='x', y="Ocupación", animation_frame="linea", animation_group="date",range_y=[0,100])
animada_ocup.update_layout(title='Ocupación Hotelera en Cartagena %, mensual')

fig1 = go.Figure(data=[
    go.Bar(name='Vacaciones, Ocio y Recreo', x=df_1['date'], y=df_1['Vacaciones, Ocio y Recreo']),
    go.Bar(name='Trabajo y Negocios ', x=df_1['date'], y=df_1['Trabajo y Negocios ']),
    go.Bar(name='Salud y atención médica', x=df_1['date'], y=df_1['Salud y atención médica']),
    go.Bar(name='Convenciones (MICE)', x=df_1['date'], y=df_1['Convenciones (MICE)']),
    go.Bar(name='**Amercos ', x=df_1['date'], y=df_1['**Amercos ']),
    go.Bar(name='Otros', x=df_1['date'], y=df_1['Otros']),
])
fig1.update_layout(title='historico de motivos de Viajes',barmode='stack')
color_2=['#ffdd00']*(df_1['date'].size)
fig_2=px.area( x=df_1['date'], y=df_1['Ocupación'], color=color_2)

fig_2.update_layout(title='Ocupación Hotelera en Cartagena %, mensual')
#Sacsa
df_2=pd.read_excel(path,sheet_name='sa_csa')


fig_3 = go.Figure(data=[
    go.Bar(name='Salidas', x=df_2['Fecha'], y=df_2['Salidas'],marker_color='#e52d27'),
    go.Bar(name='Llegadas ', x=df_2['Fecha'], y=df_2['Llegadas'],marker_color='#62bf41'),

])
fig_3.update_layout(title='Pasajeros llegados y salidos, mensual',barmode='group')
#composicion por años
df_3=pd.read_excel(path,sheet_name='sac_dis')
df_3_a=df_3.set_index(['Year','Month'])
#df_3=data_2_a.drop(columns=['Time','Total'])
def sac_dis(year=2020,mes='ENERO',data=df_3_a):
    salidos=data[['PAX SALIDOS NACIONAL','PAX SALIDOS INTERNACIONAL']]
    entrantes=data[['PAX LLEGADOS NACIONAL','PAX LLEGADOS INTERNACIONAL']]
    df2=entrantes.loc[(year,mes)]
    df1=salidos.loc[(year,mes)]
    fig=go.Figure(go.Pie(labels=df2.index, values=df2.values, name='Numero de Pasajeros llegados NACIONAL e INTERNACIONAL, mensual'))
    fig.update_layout(title='Distribución del Numero de Pasajeros llegados NACIONAL e INTERNACIONAL, mensual '+str(year)+'-'+mes)
    fig_1=go.Figure(go.Pie(labels=df1.index, values=df1.values, name='Numero de Pasajeros SALIDOS NACIONAL e INTERNACIONAL, mensual'))
    fig_1.update_layout(title='Distribución del Numero de Pasajeros SALIDOS NACIONAL e INTERNACIONAL, mensual '+str(year)+'-'+mes)

    return fig,fig_1
df_4=pd.read_excel(path,sheet_name='var')
df_4_a=df_4.set_index(['Year','Month'])

#df_3=data_2_a.drop(columns=['Time','Total'])
#Vaiación anual salarios cartagena indicador  y comparativo de regiones usar area facet
fig_sal = go.Figure(go.Indicator(

    mode = "number+delta",
    value = df_4['Cartagena'][df_4['Cartagena'].size-1],
    #delta = {"reference":  data['TO'][data['AÑO'].size-2], "valueformat": ".1f"},
    title = {"text": "Resultado"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

fig_sal.add_trace(go.Scatter(x=df_4['Time'],y = df_4['Cartagena'],line_color='#ffdd00'))
fig_sal.update_layout(title='Variación de Salarios Cartagena, por año y mes')
df_4_b=df_4.set_index('Time')
df_4_b=df_4_b.drop(columns=['Year','Month'])
df_4_b=df_4_b.rename_axis('regiones',axis='columns')


fig_sal_com=px.area(df_4_b, facet_col="regiones", facet_col_wrap=2)
#Cruceros
df_5=pd.read_excel(path,sheet_name='Cruceros')
def cruceros_mensual(Categoria,year='2020',df=df_5):
    year=str(year)
    data=df.loc[df['Categoria']==Categoria].reset_index()
    if Categoria=='Recaladas':
        title='Recaladas mesuales en la Terminal de Cruceros Cartagena en el Año: '+str(year)
    elif Categoria=='Pasajeros':
        title='Pasajeros mesuales en la Terminal de Cruceros Cartagena en el Año: '+str(year)
    elif Categoria=='Pasajeros en Transito':
        title='Pasajeros en Transito mesuales en el Año: '+str(year)
    elif Categoria=='Pasajeros Enbarcados':
        title='Pasajeros Enbarcados mesuales en el Año: '+str(year)
    elif Categoria=='Tripulantes':
        title='Tripulantes de los Cruceros en el Año: '+str(year)
    data=data.loc[0:11,:]
    fig_ivn = go.Figure()
    fig_ivn.add_trace(go.Scatter(x=data['Mes'],y = data[year], line_color="#ff7b00"))
    fig_ivn.update_layout(title=title)
    return fig_ivn
df_6=pd.read_excel(path,sheet_name='cruceros_resumen').set_index('Categoria')
df_6=df_6.rename_axis('año',axis='columns')

def cruceros_anual_total(Categoria,df=df_6):
    #data=df.set_index('Categoria')
    data=df.loc[Categoria]
    if Categoria=='Recaladas':
        title='Numero Total de barcos por Años'
    elif Categoria=='Pasajeros':
        title='Total de Pasajeros por Años'
    elif Categoria=='Pasajeros en Transito':
        title='Total de Pasajeros en Tránsito por Años'
    elif Categoria=='Pasajeros Enbarcados':
        title='Total de Pasajeros Enbarcados por Años'
    elif Categoria=='Tripulantes':
        title='Total de Tripulantes por Años'

    fig_ivn = go.Figure()
    fig_ivn.add_trace(go.Scatter(x=data.index,y = data.values))
    fig_ivn.update_layout(title=title)
    return fig_ivn
data_1=df_6.loc['Pasajeros mas Tripulantes']
data_2=df_6.loc['Promedio Pasajeros Por Recalada']
data_3=df_6.loc['Tripulantes / Pasajeros']
Pas_tri = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data_1.loc['2020'],
    #value = data_1[2020].values,
    delta = {"reference":  data_1['2019'],'relative': True},
    title = {"text": "Resultado 2020"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

Pas_tri.add_trace(go.Scatter(x=data_1.index,y = data_1.values,line_color='#ffdd00'))
Pas_tri.update_layout(title='Total de Pasajeros mas Tripulantes por Años')

prom = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data_2['2020'],
    #value = data_1[2020],
    delta = {"reference":  data_2['2019'],'relative': True},
    title = {"text": "Resultado 2020"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

prom.add_trace(go.Scatter(x=data_2.index,y = data_2.values,line_color='#ffdd00'))
prom.update_layout(title='Promedio Anual de Pasajeros Por Recalada ')
ratio = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data_3['2020'],
    #value = data_1[2020],
    delta = {"reference":  data_3['2019'], "valueformat": ".2f",'relative': True},
    title = {"text": "Resultado 2020"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

ratio.add_trace(go.Scatter(x=data_3.index,y = data_3.values,line_color='#ffdd00'))
ratio.update_layout(title='Tasa Anual de Tripulantes por Pasajeros')
#fig = px.bar(df, x="date", y=['Vacaciones, Ocio y Recreo',Trabajo y Negocios'], color="columns",
 #animation_frame="year", animation_group="country", range_y=[0,4000000000])
def Turismo():

    return    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('Data\ctg_or.jpg', 'rb').read()).decode()), className="app__logo", width=200),

                                    html.H4("By Kevin Sossa", className="header__text"),
                                ],
                                className="Banner",
                                style={
                                    'textAlign': 'center',
                                    'color':'black'
                                },
                            ),
                            html.Div(
                                [
                                    dcc.Tabs(
                                        id="tabs",
                                        value="data-entry",
                                        children=[
                                            dcc.Tab(
                                                label="Ocupación Hotelera",
                                                value="data-entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [

                                                            html.H3('Ocupación Hotelera', style=title_style),
                                                            dcc.Graph(figure=fig_2),

                                                            dcc.Graph(figure=animada_ocup),
                                                            html.H4('Motivos de Viajes'),
                                                            dcc.Graph(figure=fig1),

                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Pasajeros",
                                                value="entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                html.Div([
                                                   html.H3('Pasajeros LLEGADOS y SALIDOS de CARTAGENA', style=title_style),
                                                   dcc.Graph(figure=fig_3),
                                                   html.H3('Pasajeros LLEGADOS y SALIDOS de CARTAGENA, según origen y destino', style=title_style),
                                                   html.H4('Seleccione el Año: '),
                                                   dcc.Dropdown(
                                                       id='year_sac',
                                                       value=2020,
                                                       options=[{'value': x, 'label': x}
                                                                for x in range(2020,2022)],
                                                       clearable=False
                                                   ),
                                                   html.H4('Seleccione el mes: '),
                                                   dcc.Dropdown(
                                                       id='month_sac',
                                                       value='ENERO',
                                                       options=[{'value': x, 'label': x}
                                                                for x in df_3['Month'].unique()],
                                                       clearable=False
                                                   ),
                                                   dcc.Graph(id='sacsa'),
                                                   dcc.Graph(id='sacsa_1'),
                                                   ]
                                                   )

                                                ],
                                            ),
                                            dcc.Tab(
                                            label="Cruceros",
                                            value="view-entry",
                                            style=tab_style,
                                            selected_style=tab_selected_style,
                                            children=[
                                            html.Div(
                                                [
                                                html.H3('Datos de los Cruceros que llegan a la Terminal de Cruceros Cartagena de Indias: ', style=title_style),
                                                dcc.Graph(id='cruceros_1', figure=Pas_tri),
                                                dcc.Graph(id='cruceros_2', figure=prom),

                                                dcc.Graph(id='cruceros_5', figure=ratio),
                                                html.H3('Historico Anual y Mesual de los Pasajeros y las Enbarcaciones: ', style=title_style),
                                                html.H4('Analisis Anual: '),
                                                html.H4('Seleccione la variable: '),

                                                dcc.Dropdown(
                                                    id='variable_cru',
                                                    value='Recaladas',
                                                    options=[{'value': x, 'label': x}
                                                             for x in df_5['Categoria'].unique()],
                                                    clearable=False
                                                ),
                                                dcc.Graph(id='cruceros_3'),
                                                html.H4('Analisis Mensual: '),

                                                html.H4('Seleccione el año: '),
                                                dcc.Dropdown(
                                                    id='year_cru',
                                                    value=2020,
                                                    options=[{'value': x, 'label': x}
                                                             for x in range(2010,2021)],
                                                    clearable=False
                                                ),

                                                dcc.Graph(id='cruceros_4'),


                                                ],
                                                className="container__1",
                                            )
                                            ]
                                            ),
                                            dcc.Tab(
                                            label="Salarios",
                                            value="view-entry-1",
                                            style=tab_style,
                                            selected_style=tab_selected_style,
                                            children=[
                                            html.Div(
                                                [
                                                html.H3('Variación Anual de Salarios en Cartagena', style=title_style),
                                                dcc.Graph(id='Salarios',figure=fig_sal),
                                                html.H3('Comparación de Variación Anual de Salarios por región', style=title_style),

                                                dcc.Graph(id='Salarios_1', figure=fig_sal_com),



                                                ],
                                                className="container__1",
                                            )
                                            ]
                                            ),
                                        ],
                                    )
                                ],
                                className="tabs__container",
                            ),
                        ],
                        className="page__container",

                    )
