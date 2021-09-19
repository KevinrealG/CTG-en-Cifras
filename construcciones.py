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

#It's upload the construcciones Data
path='Data/Construcciones.xlsx'
data=pd.read_excel(path,sheet_name='Area_censada')
#Historico de Area censada
fig2 = go.Figure(data=[
    go.Scatter(name='Total', x=data['Time'], y=data['Total']),
    go.Scatter(name='Culminada', x=data['Time'], y=data['culminada']),
    go.Scatter(name='En proceso', x=data['Time'], y=data['proceso']),
    go.Scatter(name='Paralizada', x=data['Time'], y=data['paralizada'])
])
fig2.update_layout(title='Area censada, Historico')
fig1 = go.Figure(data=[
    go.Bar(name='Nueva', x=data['Time'], y=data['proceso_nueva']),
    go.Bar(name='Continua', x=data['Time'], y=data['Contin_proceso']),
    go.Bar(name='Reinicio', x=data['Time'], y=data['Reinicia_proceso']),
])
fig1.update_layout(title='Area censada En proceso, Historico')
fig = go.Figure(data=[
    go.Bar(name='Nueva', x=data['Time'], y=data['Para_nueva']),
    go.Bar(name='Continua', x=data['Time'], y=data['Contin_paralizada']),
    go.Bar(name='TOTAL', x=data['Time'], y=data['paralizada']),
])
fig.update_layout(title='Area censada Paralizada, Historico')
#figure with all columns with filter to add a different column
data=data[['Time','culminada','proceso','paralizada']].set_index('Time')
data=data.rename_axis('areas',axis='columns')
figx = px.area(data, facet_col="areas", facet_col_wrap=1)
#the same figure for estratos
data=pd.read_excel(path,sheet_name='Estratos')
data=data.loc[:,'Total':'Time'].set_index('Time')
data=data.rename_axis('Estratos',axis='columns')
figy = px.area(data, facet_col="Estratos", facet_col_wrap=2)
#composicion por años
data=pd.read_excel(path,sheet_name='Estratos')
data_2_a=data.set_index(['Año','Trimestre'])
data_2_a=data_2_a.drop(columns=['Time','Total'])
def estratos_construcciones(year=2020,trimestre='I',data=data_2_a):
    df2=data.loc[(year,trimestre)]
    fig=go.Figure(go.Pie(labels=df2.index, values=df2.values, name='Estratos Distribución'))
    fig.update_layout(title='Distribución del Area Censada en el Año-Trimestre: '+str(year)+'-'+trimestre)

    return fig

#vivienda
data=pd.read_excel(path,sheet_name='vivienda')

fig_new= px.icicle(data, path=[px.Constant("all"),'tipo','vis', 'estrato'], values='area')

fig_new.update_layout(margin = dict(t=50, l=25, r=25, b=25))
def Viviendas(year=2020):
    df=pd.read_excel(path,sheet_name='vivienda')
    data=df.loc[df['año']==year]
    df1=data.groupby('vis').agg(Area=('area', 'sum'),Unidades=('unidades','sum'))
    df2=data.groupby('tipo').agg(Area=('area', 'sum'),Unidades=('unidades','sum'))
    #new_df=new_df.loc[new_df['año']==year]
    #new_df=new_df.sort_values(by=['area'],ascending=True)
    #best=new_df.sort_values(by='Area')
    #best=best['Area'].tail(5)
    #fig_best= px.bar(best, x=best.index, y=best.values)
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]],subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))
    fig.add_trace(go.Bar(name='Vis o No Vis, por area en m2',x=df1.index, y=df1['Area']), 1, 1)
    fig.add_trace(go.Bar(name='Vis o No Vis, por unidades',x=df1.index, y=df1['Unidades']),  1, 2)
    fig.add_trace(go.Bar(name='Tipo de Vivienda, por area en m2',x=df2.index, y=df2['Area']), 2, 1)
    fig.add_trace(go.Bar(name='Tipo de Vivienda, por unidades',x=df2.index, y=df2['Unidades']),  2, 2)

    # Use `hole` to create a donut-like pie chart
    #fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Licencias de de Viviendas "+str(year),
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Area', x=0.01, y=1, font_size=20, showarrow=False),
                     dict(text='Unidades', x=0.70, y=1, font_size=20, showarrow=False)])
    return fig
#Indices
data_5=pd.read_excel(path,sheet_name='IVPcom')
data_5=data_5.set_index('CIUDAD')
data_5=data_5.rename_axis('Años',axis='columns')
data_5_a=data_5.T

def top_5(year=2020,df=data_5):
    new_df=df[year]
    new_df=new_df.sort_values(ascending=True)
    best=new_df.head(5)
    worst=new_df.tail(5)
    fig_worst=fig = px.bar(best, x=best.values, y=best.index, orientation='h')
    fig_worst.update_layout(title='Peores 5 IVP '+str(year))
    fig_best= px.bar(worst, x=worst.values, y=worst.index, orientation='h')
    fig_best.update_layout(title='TOP 5 IVP '+str(year))
    Car = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = new_df.loc['CARTAGENA'],
    title = {'text': "IVP-CARTAGENA "+str(year)},
    delta = {'reference': worst[4]},
    domain = {'x': [0, 1], 'y': [0, 1]}
        ))
    return fig_best, fig_worst,Car
data_5_b=data_5_a[['CARTAGENA','CALI','MEDELLÍN','BARRANQUILLA','TOTAL NACIONAL']]
fig_ind = px.area(data_5_b, facet_col="CIUDAD", facet_col_wrap=1)
fig_ind.update_layout(title='Historico de IVP de cidudades principales')
#ivnew
data_6=pd.read_excel(path,sheet_name='Vivi_new_o_IVPN')
data_6=data_6.set_index('Time')
data_6_a=data_6['Indice Vivienda nueva']
fig_ivn = go.Figure(go.Indicator(
    mode = "number+delta",
    value = data_6_a[data_6_a.size-1],
    delta = {"reference":  data_6_a[data_6_a.size-2], "valueformat": ".0f"},
    title = {"text": "Crecimiento Anual"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]}))

fig_ivn.add_trace(go.Scatter(x=data_6.index,y = data_6['Indice Vivienda nueva']))
data_8=pd.read_excel(path,sheet_name='ICCV_anual')
data_9=pd.read_excel(path,sheet_name='ICCV_ciudades_anual')

def ICCV(tipo,df=data_8,df_2=data_9):
    data=df
    data_2=df_2.loc[df_2['Ciudades']=='Cartagena']


    title=''
    if tipo=='Total':
        title='Variación anual total ICCV '
    elif tipo=='Vivienda unifamiliar':
        title='Variación anual ICCV para Vivienda unifamiliar'
    elif tipo=='Vivienda multifamiliar':
        title='Variación anual ICCV para Vivienda unifamiliar'
    else:
        title='Variación anual ICCV para VIS'


    fig_ivn = go.Figure(go.Indicator(

        mode = "number+delta",
        value = data[tipo][data['Años'].size-1],
        delta = {"reference":  data[tipo][data['Años'].size-2], "valueformat": ".0f"},
        title = {"text": "Resultado "+str(data['Años'][data['Años'].size-1],)},
        domain = {'y': [0, 1], 'x': [0.25, 0.75]})
        )

    fig_ivn.add_trace(go.Scatter(x=data['Años'],y = data[tipo], fill='tozeroy'))
    fig_ivn.update_layout(title=title)
    fig_2 = go.Figure(go.Indicator(

        mode = "gauge+number",
        value = data_2[tipo].values[0],
        #delta = {"reference":  data[tipo][data['Años'].size-2], "valueformat": ".0f"},
        title = {"text": "Resultado "+str(data['Años'][data['Años'].size-1],)},
        domain = {'y': [0, 1], 'x': [0.25, 0.75]})
        )

    return fig_ivn, fig_2
#Destinos
data_7=pd.read_excel(path,sheet_name='destinos')
#data_6=data_6.set_index('Time')
#data_6_a=data_6['Indice Vivienda nueva']
def top_5_des(year=2020,df=data_7):
    new_df=df.loc[df['año']==year]
    new_df=new_df.groupby('des').agg(Area=('area', 'sum'))
    #new_df=new_df.loc[new_df['año']==year]
    #new_df=new_df.sort_values(by=['area'],ascending=True)
    best=new_df.sort_values(by='Area')
    best=best['Area'].tail(5)
    fig_best= px.bar(best, x=best.index, y=best.values)
    fig_best.update_layout(title='TOP 5 Destinos '+str(year))

    return fig_best
data_7_a=pd.read_excel(path,sheet_name='Area_proc_destino')

data_7_a_1=data_7_a.loc[:,'Apartamentos':'Time'].set_index('Time')
data_7_a_1=data_7_a_1.rename_axis('Destinos',axis='columns')
fig_dest = px.area(data_7_a_1, facet_col="Destinos", facet_col_wrap=2)
data_7_a_2=data_7_a.set_index(['Año','Trimestre'])
data_7_a_2=data_7_a_2.drop(columns=['Time','Total'])
def destinos(year=2020,trimestre='IV',df=data_7_a_2):
    df2=df.loc[(year,trimestre)]
    fig=go.Figure(go.Bar(x=df2.index, y=df2.values))
    fig.update_layout(title='Área aprobada bajo licencias de construcción en Cartagena* según destinos '+str(year)+'-'+trimestre)
    return fig

def construcciones():

    return    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('ctg_or.jpg', 'rb').read()).decode()), className="app__logo", width=200),

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
                                                label="Historico de Area censada",
                                                value="data-entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [
                                                            html.H4("Estructura General Censo de Edificaciones según Estado de Obra,por area(m2) y años"),
                                                            dcc.Graph(figure=figx),
                                                            html.H4("Area Censada Total y composicion por Estado de Obra, en m2"),

                                                            dcc.Graph(figure=fig2),
                                                            html.H4("Area Censada Total en Proceso mas Nueva, Continúa y Reinicia en Proceso, en m2 y por Años"),
                                                            dcc.Graph(figure=fig1),
                                                            html.H4("Area Censada Total Paralizada mas  Continúa y Nueva Paralizada, en m2 y por Años"),
                                                            dcc.Graph(figure=fig),

                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Estratos",
                                                value="data-2",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [


                                                            html.H3("Area Censada Total en Proceso y Distribución según estrato, en m2 y por Años",style=title_style),
                                                            dcc.Graph(figure=figy),
                                                            html.H3("Distribución de Area Total en Proceso según estrato, en m2, por Año y Trimestre",style=title_style),
                                                            html.H4('Seleccione el Año'),
                                                            dcc.Dropdown(
                                                                id='year_estrato',
                                                                value=2020,
                                                                options=[{'value': x, 'label': x}
                                                                         for x in range(2015,2021)],
                                                                clearable=False
                                                            ),

                                                            html.H4('Seleccione el Trimestre'),
                                                            dcc.Dropdown(
                                                                id='trimestre',
                                                                value='I',
                                                                options=[{'value': x, 'label': x}
                                                                         for x in ['I','II','III','IV']],
                                                                clearable=False
                                                            ),
                                                            dcc.Graph(id="pie-cont"),


                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Indices",
                                                value="data-3",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [
                                                        html.H3('Indice de Valoración Predial',style=title_style),
                                                        html.H4('Seleccione el Año'),
                                                        dcc.Dropdown(
                                                            id='year_indice',
                                                            value=2020,
                                                            options=[{'value': x, 'label': x}
                                                                     for x in range(2015,2021)],
                                                            clearable=False
                                                        ),
                                                        html.Div([dcc.Graph(id='indice_1'),dcc.Graph(id='indice_2')]),
                                                        html.Div([dcc.Graph(id='indice_3'),dcc.Graph(id='indice_4',figure=fig_ind)]),
                                                        html.H3('Indice de Vivienda de Nueva',style=title_style),
                                                        html.Div([dcc.Graph(id='indice_5',figure=fig_ivn)]),

                                                        html.H3('Variación Anual Indice de Costos de Construcción de Vivienda'),
                                                        html.H4('Seleccione el tipo de Vivienda: '),
                                                        dcc.Dropdown(
                                                            id='ICCV',
                                                            value='Total',
                                                            options=[{'value': x, 'label': x}
                                                                     for x in ['Total','Vivienda unifamiliar','Vivienda multifamiliar','VIS']],
                                                            clearable=False
                                                        ),
                                                        html.H4('ICCV en CARTAGENA: '),
                                                        dcc.Graph(id='ICCV_1'),
                                                        dcc.Graph(id='ICCV_2'),


                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Destinos",
                                                value="data-4",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [
                                                        html.H3("Distribución Historica de Area Total Censada en Proceso según Destino, en m2",style=title_style),
                                                        dcc.Graph(figure=fig_dest),
                                                        html.H3("Top 5 destinos de Area Censada y Distribución de Areas por destinos, por año y trimestre seleccionado ",style=title_style),
                                                        html.H4('Seleccione el Año'),
                                                        dcc.Dropdown(
                                                            id='year_destino',
                                                            value=2020,
                                                            options=[{'value': x, 'label': x}
                                                                     for x in range(2015,2021)],
                                                            clearable=False
                                                        ),
                                                        html.H4('Seleccione el trimestre'),
                                                        dcc.Dropdown(
                                                            id='trimestre_des',
                                                            value='I',
                                                            options=[{'value': x, 'label': x}
                                                                     for x in ['I','II','III','IV']],
                                                            clearable=False
                                                        ),
                                                        dcc.Graph(id="destinos_2"),
                                                        dcc.Graph(id="destinos_1"),
                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Viviendas",
                                                value="data-5",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div([
                                                    html.H3('Distribución de las licencias de Construcciones para Viviendas, por año',style=title_style),
                                                    html.H4('Seleccione Año'),
                                                    dcc.Dropdown(
                                                        id='year_vivienda',
                                                        value=2020,
                                                        options=[{'value': x, 'label': x}
                                                                 for x in range(2015,2021)],
                                                        clearable=False
                                                    ),
                                                    dcc.Graph(id='vivienda'),
                                                    html.H3('Composición de las licencias de Construcciones para Viviendas,  por tipo de vivienda, Vis o No vis, y estratos, en m2',style=title_style),
                                                    dcc.Graph(figure=fig_new),

                                                    ],
                                                    className="container__1",)
                                                ],
                                            ),


                                        ],
                                    )
                                ],
                                className="tabs__container",
                            ),
                        ],
                        className="page__container",
                    )
