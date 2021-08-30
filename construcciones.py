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
data_2=pd.read_excel(path,sheet_name='Estratos')
data_2=data_2.loc[:,'Total':'Time'].set_index('Time')
data_2=data_2.rename_axis('Estratos',axis='columns')
figy = px.area(data_2, facet_col="Estratos", facet_col_wrap=2)
#composicion por años
data_2=pd.read_excel(path,sheet_name='Estratos')
data_2_a=data_2.set_index(['Año','Trimestre'])
data_2_a=data_2_a.drop(columns=['Time','Total'])
def estratos_construcciones(year=2020,trimestre='I',data=data_2_a):
    df2=data.loc[(year,trimestre)]
    fig=go.Figure(go.Pie(labels=df2.index, values=df2.values, name='Estratos Distribución'))
    fig.update_layout(title='Estratos Distribución '+str(year)+'-'+trimestre)

    return fig

"""dcc.Graph(id="pie-cont"),
data_2_b=data_2.rename_axis('estratos',axis='columns')
data_2_b=data_2_b.drop(columns=['Time','Total'])
data_2_b=data_2_b.set_index(['Año','Trimestre'])"""
#vivienda
data_4=pd.read_excel(path,sheet_name='vivienda')

fig_new= px.icicle(data_4, path=[px.Constant("all"),'tipo','vis', 'estrato'], values='area')
#fig = px.icicle(data_2_b, path=[px.Constant("all"),data_2_b.index.get_level_values(0), .index.get_level_values(1), 'estratos'], values='total_bill')
#fig_new.update_traces(root_color="lightgrey")
fig_new.update_layout(margin = dict(t=50, l=25, r=25, b=25))
data_4_b=pd.read_excel(path,sheet_name='Vis_no')
def Viviendas(year=2020,df=data_4):
    data=df.loc[df['año']==year]
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]],subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))
    fig.add_trace(go.Bar(x=data['vis'], y=data['area']), 1, 1)
    fig.add_trace(go.Bar(x=data['vis'], y=data['unidades']),  1, 2)
    fig.add_trace(go.Bar(x=data['tipo'], y=data['area']), 2, 1)
    fig.add_trace(go.Bar(x=data['tipo'], y=data['unidades']),  2, 2)

    # Use `hole` to create a donut-like pie chart
    #fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Licencias de de Viviendas "+str(year),
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Area', x=0.01, y=1, font_size=20, showarrow=False),
                     dict(text='Unidades', x=0.30, y=1, font_size=20, showarrow=False)])
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
    title = {"text": "Indice de Vivienda Nueva"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]}))

fig_ivn.add_trace(go.Scatter(x=data_6.index,y = data_6['Indice Vivienda nueva']))
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
    fig.update_layout(title='Área aprobada bajo licencias de construcción en Bolívar* según destinos '+str(year)+'-'+trimestre)
    return fig

def construcciones():

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
                                                label="Historico de Area censada",
                                                value="data-entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=figx),

                                                            dcc.Graph(figure=fig2),
                                                            dcc.Graph(figure=fig1),
                                                            dcc.Graph(figure=fig),
                                                            dcc.Graph(figure=fig_new),
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
                                                            dcc.Graph(figure=figy),
                                                            html.H3('Año'),
                                                            dcc.Dropdown(
                                                                id='year_estrato',
                                                                value=2020,
                                                                options=[{'value': x, 'label': x}
                                                                         for x in range(2015,2021)],
                                                                clearable=False
                                                            ),
                                                            html.H3('trimestre'),
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
                                                        html.H3('Año'),
                                                        dcc.Dropdown(
                                                            id='year_indice',
                                                            value=2020,
                                                            options=[{'value': x, 'label': x}
                                                                     for x in range(2015,2021)],
                                                            clearable=False
                                                        ),
                                                        html.Div([dcc.Graph(id='indice_1'),dcc.Graph(id='indice_2')]),
                                                        html.Div([dcc.Graph(id='indice_3'),dcc.Graph(id='indice_4',figure=fig_ind)]),
                                                        html.Div([dcc.Graph(id='indice_5',figure=fig_ivn)]),
                                                        html.H3('Ciudades'),
                                                        dcc.Dropdown(
                                                            id='ciudad',
                                                            value=2020,
                                                            options=[{'value': x, 'label': x}
                                                                     for x in range(2015,2021)],
                                                            clearable=False
                                                        ),



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
                                                        dcc.Graph(figure=fig_dest),
                                                        html.H3('Año'),
                                                        dcc.Dropdown(
                                                            id='year_destino',
                                                            value=2020,
                                                            options=[{'value': x, 'label': x}
                                                                     for x in range(2015,2021)],
                                                            clearable=False
                                                        ),
                                                        html.H3('trimestre'),
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
                                                    html.H3('Año'),
                                                    dcc.Dropdown(
                                                        id='year_vivienda',
                                                        value=2020,
                                                        options=[{'value': x, 'label': x}
                                                                 for x in range(2015,2021)],
                                                        clearable=False
                                                    ),
                                                    dcc.Graph(id='vivienda'),
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
                        className="app__container",
                    )
