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
path='Data/base de dinamica.xlsx'
data=pd.read_excel(path,sheet_name='Historico jurisdicción')

#Figure the historico de empresas por jurisdicción
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(name='Variación',
        x=data['Año'],
        y=data['Var. Emp. Totales']
    ),
    secondary_y=True,
    )

fig.add_trace(
    go.Bar(name='Empresas',
        x=data['Año'],
        y=data['emp_activas']
    ))
fig.update_layout(title='Historico de Empresas',barmode='group')

#figure of Variaciones
fig1 = go.Figure(data=[
    go.Bar(name='Empresas Nuevas', x=data['Año'], y=data['Var. Emp. Nuevas']),
    go.Bar(name='Empresas Renovadas', x=data['Año'], y=data['Var. Emp. Renovadas'])
])
# Change the bar mode
fig1.update_layout(title='Variaciones',barmode='group')

#figure of Variaciones of Ingresos and Activos
fig2 = go.Figure(data=[
    go.Bar(name='Ingresos', x=data['Año'], y=data['Ingresos_Car']),
    go.Bar(name='Activos', x=data['Año'], y=data['Activos_Car'])
])
# Change the bar mode
fig2.update_layout(title='Activos e Ingresos',barmode='group')

#figure of Variaciones of Empleos
fig3 = go.Figure(data=[
    go.Bar(name='Empleos', x=data['Año'], y=data['Empleos_Car'])
    ])
# Change the bar mode
fig3.update_layout(title='Empleos')
#Figure the historico de empresas Cartagena
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(
    go.Scatter(name='Variación Nuevas',
        x=data['Año'],
        y=data['Var. Emp. Nuevas']
    ),
    secondary_y=True,
    )
fig4.add_trace(
    go.Scatter(name='Variación Renovadas',
        x=data['Año'],
        y=data['Var. Emp. Renovadas']
    ),
    secondary_y=True,
    )
fig4.add_trace(
    go.Bar(name='Empresas',
        x=data['Año'],
        y=data['Empresas_Car']
    ))
fig4.update_layout(title='Historico de Empresas Cartagena',barmode='stack')

#Estructura and tamaño
#Create a filter for year
#colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

#fig = go.Figure(data=[go.Pie(labels=['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen'],
#                             values='filter_year'])
#fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
#                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
#make subplots
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
        title_text="Tamaño de Empresas "+str(year),
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
fig_sec = px.icicle(data3, path=[px.Constant("all"),'SECTOR','ACTIVIDAD','TAMAÑO SEGÚN EMPLEO'], values='EMPLEADOS')
fig_sec.update_layout(title='Sectores por numero de EMPLEADOS',margin = dict(t=50, l=25, r=25, b=25))
fig_sec1 = px.icicle(data3, path=[px.Constant("all"),'SECTOR','ACTIVIDAD','TAMAÑO SEGÚN ACTIVOS'], values='TOTAL ACTIVOS')
fig_sec1.update_layout(title='Sectores por TOTAL ACTIVOS',margin = dict(t=50, l=25, r=25, b=25))
fig_sec_2 = px.icicle(data3, path=[px.Constant("all"),'APUESTAS','SECTOR','TAMAÑO SEGÚN INGRESO SECTOR'], values='INGRESOS')
fig_sec_2.update_layout(title='Sectores por SEGÚN INGRESO SECTOR',margin = dict(t=50, l=25, r=25, b=25))
fig_sec_3 = px.icicle(data3, path=[px.Constant("all"),'SECTOR','ACTIVIDAD'], values='Empresas')#count_values
fig_sec_3.update_layout(title='Sectores por numero de EMpresas',margin = dict(t=50, l=25, r=25, b=25))

#app = dash.Dash()
def empresarial():

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
                                                label="Historico de Empresas Jurisdiccion y Ciudad",
                                                value="data-entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=fig),
                                                            dcc.Graph(figure=fig1),
                                                            dcc.Graph(figure=fig2),
                                                            dcc.Graph(figure=fig3),
                                                            dcc.Graph(figure=fig4),
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

                                                dcc.Dropdown(
                                                    id='year',
                                                    value=2020,
                                                    options=[{'value': x, 'label': x}
                                                             for x in range(2013,2021)],
                                                    clearable=False
                                                ),
                                                dcc.Graph(id="pie-chart"),
                                                html.H4("Actividades por Tamaño", className="header__text"),
                                                html.P("Values:"),
                                                dcc.Dropdown(
                                                    id='values',
                                                    value='Empresas',
                                                    options=[{'value': x, 'label': x}
                                                             for x in ['Empresas', 'Empleos', 'Activos','Ingresos']],
                                                    clearable=False
                                                ),
                                                html.P("Tamaño:"),
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
                                                    dcc.Graph(figure=fig_sec),
                                                    dcc.Graph(figure=fig_sec1),
                                                    dcc.Graph(figure=fig_sec_2),
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
                        className="app__container",
                    )

"""html.Div(children=[

            # All elements from the top of the page

            # New Div for all elements in the new 'row' of the page
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='graph1',
                        figure=fig3
                    ),
                ], className='six columns'),
                html.Div([


                    dcc.Graph(
                        id='graph2',
                        figure=fig4
                    ),
                ], className='six columns'),
            ], className='row'),
            html.Div([

            dcc.Graph(
                id='graph3',
                figure=fig
            ),
            ], className='row'),
        ])
        ])"""
dcc.Slider(
       id='year-slider',
       min=2013,
       max=2020,
       value=2020,
       marks={str(year): str(year) for year in range(2013,2021)},
       step=None
   ),
#app.run_server(debug=True)  # Turn off reloader if inside Jupyter
