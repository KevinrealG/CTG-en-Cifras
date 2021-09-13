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

path='Data/base de dinamica.xlsx'
data=pd.read_excel(path,sheet_name='Historico jurisdicción')

#Figure the historico de empresas por jurisdicción
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(name='Variación Anual, %',
        x=data['Año'],
        y=data['Var. Emp. Totales'],
        line_color='rgb(255,221,0)'#yellow line color
    ),
    secondary_y=True,
    )

fig.add_trace(
    go.Bar(name='Numero Total de Empresas',
        x=data['Año'],
        y=data['emp_activas'],
        marker_color='rgb(98, 191, 65)'#bar color
    ))
fig.update_layout(title='Número Total de Empresas y Variación Anual de La Jurisdicción, por Años',barmode='group',plot_bgcolor="white")

#figure of Variaciones
fig1 = go.Figure(data=[
    go.Bar(name='Variación Empresas Nuevas, %', x=data['Año'], y=data['Var. Emp. Nuevas'],marker_color='rgb(57, 114, 36)'),
    go.Bar(name='Variación Empresas Renovadas, %', x=data['Año'], y=data['Var. Emp. Renovadas'],marker_color='rgb(229,45,39)')
])
fig1.update_layout(title='Variaciones Anuales De Empresas Nuevas y Renovadas de La Jurisdiccion, por Años',barmode='group',plot_bgcolor="white")

#figure of Variaciones of Ingresos and Activos
fig2 = go.Figure(data=[
    go.Bar(name='Ingresos', x=data['Año'], y=data['Ingresos_Car'],marker_color='rgb(57, 114, 36)'),
    go.Bar(name='Activos', x=data['Año'], y=data['Activos_Car'],marker_color='rgb(229,45,39)')
])
fig2.update_layout(title='Activos e Ingresos Totales en Pesos de las Empresas de la Jurisdicción, por Año ',plot_bgcolor="white")

#figure of Variaciones of Empleos
fig3 = go.Figure(data=[
    go.Bar(name='Empleos Totales Generados en La Jurisdicción', x=data['Año'], y=data['Empleos_Car'],marker_color='rgb(57, 114, 36)')
    ])
# Change the bar mode
fig3.update_layout(title='Empleos Totales Generados en La Jurisdicción',plot_bgcolor="white")
#Figure the historico de empresas Cartagena
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(
    go.Scatter(name='Variación Nuevas, %',
        x=data['Año'],
        y=data['Var. Emp. Nuevas'],
        line_color='rgb(255,221,0)'
    ),
    secondary_y=True,
    )
fig4.add_trace(
    go.Scatter(name='Variación Renovadas, %',
        x=data['Año'],
        y=data['Var. Emp. Renovadas'],
        line_color='rgb(179, 18, 23)'
    ),
    secondary_y=True,
    )
fig4.add_trace(
    go.Bar(name='Empresas',
        x=data['Año'],
        y=data['Empresas_Car'],
        marker_color='rgb(57, 114, 36)'
    ))
fig4.update_layout(title='Número Total de Empresas y Variación Anual de Empresas Renovadas y Nuevas Cartagena, por Años',barmode='stack',plot_bgcolor="white")


data2=pd.read_excel(path,sheet_name='Tamaño_1')
def df(variable,year=2020,data=data2):
        data=data.loc[data['Categoria']==variable]
        labels = data['Tamaño']
        #print(data[2019])
        values=data[year]
        #go.Pie(labels=labels, values=values, name=variable)
        return go.Pie(labels=labels, values=values, name=variable)



# Create subplots: use 'domain' type for Pie subplot
def tamano(year=2020):
    fig = make_subplots(rows=1, cols=4, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(df('Empresas',year,data2), 1, 1)
    fig.add_trace(df('Empleos',year,data2),  1, 2)
    fig.add_trace(df('Activos',year,data2), 1, 3)
    fig.add_trace(df('Ventas',year, data2), 1, 4)
    # Use `hole` to create a donut-like pie chart
    #fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Distribución de Empresas de Cartagena según el tamaño en el año: "+str(year),
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Empresas', x=0.01, y=1, font_size=20, showarrow=False),
                     dict(text='Empleos', x=0.30, y=1, font_size=20, showarrow=False),
                     dict(text='Activos', x=0.7, y=1, font_size=20, showarrow=False),
                     dict(text='Ventas', x=0.95, y=1, font_size=20, showarrow=False)])
    return fig

#Sectores and apuestas
path2='Data/Estructura2020.xlsx'
data3=pd.read_excel(path2,sheet_name='Base')
df3=data3.groupby(['SECTOR','ACTIVIDAD','DIVISIÓN']).agg(Empresas=('MATRICULA', 'count'),Empleos=('EMPLEADOS', 'sum'),Activos=('TOTAL ACTIVOS', 'sum'),Ingresos=('INGRESOS', 'sum') )
#print(df3)
#Sectores
#fig_sec = px.icicle(data3, path=[px.Constant("all"),'SECTOR','ACTIVIDAD','TAMAÑO SEGÚN EMPLEO'], values='EMPLEADOS')
#fig_sec.update_layout(title='Sectores por numero de EMPLEADOS',margin = dict(t=50, l=25, r=25, b=25))
fig_sec1 = px.icicle(data3, path=[px.Constant("all"),'SECTOR','ACTIVIDAD','TAMAÑO SEGÚN ACTIVOS'], values='TOTAL ACTIVOS')
fig_sec1.update_layout(title='Composición de los Sectores Economicos de la Jurisdicción, según Total de Activos',margin = dict(t=50, l=25, r=25, b=25))
#fig_sec_2 = px.icicle(data3, path=[px.Constant("all"),'APUESTAS','SECTOR','TAMAÑO SEGÚN INGRESO SECTOR'], values='INGRESOS')
#fig_sec_2.update_layout(title='Sectores por SEGÚN INGRESO SECTOR',margin = dict(t=50, l=25, r=25, b=25))
fig_sec_3 = px.icicle(data3, path=[px.Constant("all"),'Apuesta_1','SECTOR','ACTIVIDAD'], values='Empresas')#count_values
fig_sec_3.update_layout(title='Composición de las APUESTAS, según el Numero Total de Empresas',margin = dict(t=50, l=25, r=25, b=25))

#app = dash.Dash()
def empresarial():

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
                                                label="Historico de Empresas Jurisdiccion y Ciudad",
                                                value="data-entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=fig4),
                                                            dcc.Graph(figure=fig),
                                                            dcc.Graph(figure=fig1),
                                                            dcc.Graph(figure=fig2),
                                                            dcc.Graph(figure=fig3),
                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Estructura y tamaño",
                                                value="entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                html.H4("Seleccione el Año:"),

                                                dcc.Dropdown(
                                                    id='year',
                                                    value=2020,
                                                    options=[{'value': x, 'label': x}
                                                             for x in range(2013,2021)],
                                                    clearable=False
                                                ),
                                                dcc.Graph(id="pie-chart"),
                                                html.H3("Composición de las Empresas de Cartagena según el tamaño y las Actividades Economicas", className="header__text",style=title_style),
                                                html.H4("Seleccione la variable de comparación:"),
                                                dcc.Dropdown(
                                                    id='values',
                                                    value='Empresas',
                                                    options=[{'value': x, 'label': x}
                                                             for x in ['Empresas', 'Empleos', 'Activos','Ingresos']],
                                                    clearable=False
                                                ),
                                                html.H4("Seleccione el Tamaño de las Empresas:"),
                                                dcc.Dropdown(
                                                    id='tam',
                                                    value='Grande',
                                                    options=[{'value': x, 'label': x}
                                                             for x in ['Grande', 'Mediana', 'Microempresa','Pequeña']],
                                                    clearable=False
                                                ),
                                                dcc.Graph(id="treemap-chart"),


                                                ],
                                            ),
                                            dcc.Tab(
                                            label="SECTOR",
                                            value="view-entry",
                                            style=tab_style,
                                            selected_style=tab_selected_style,
                                            children=[
                                            html.Div(
                                                [
                                                    #dcc.Graph(figure=fig_sec),
                                                    dcc.Graph(figure=fig_sec1),
                                                    #dcc.Graph(figure=fig_sec_2),
                                                    dcc.Graph(figure=fig_sec_3),

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
