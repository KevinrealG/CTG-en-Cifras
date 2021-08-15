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
def df(data,variable):
        data=data.loc[data['Categoria']==variable]
        labels = data['Tamaño']
        #print(data[2019])
        values=data[2020]
        #go.Pie(labels=labels, values=values, name=variable)
        return go.Pie(labels=labels, values=values, name=variable)



# Create subplots: use 'domain' type for Pie subplot
fig5 = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]])
fig5.add_trace(df(data2,'Empresas'),    1, 1)
fig5.add_trace(df(data2,'Empleos'),     1, 2)
fig5.add_trace(df(data2,'Activos'),   2, 1)
fig5.add_trace(df(data2,'Ventas'),  2, 2)
# Use `hole` to create a donut-like pie chart
fig5.update_traces(hole=.4, hoverinfo="label+percent+name")

fig5.update_layout(
    title_text="Tamaño de Empresas",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Empresas', x=0.18, y=1.2, font_size=20, showarrow=False),
                 dict(text='Empleos', x=0.82, y=0.5, font_size=20, showarrow=False),
                 dict(text='Activos', x=0.82, y=0.5, font_size=20, showarrow=False),
                 dict(text='Ventas', x=0.18, y=1, font_size=20, showarrow=False)])

#app = dash.Dash()
def empresarial():

    return    html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(src="Dara/ctg_cifras.jpg", className="app__logo"),
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
                                                value="view-entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                dcc.Graph(figure=fig5),


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

#app.run_server(debug=True)  # Turn off reloader if inside Jupyter
