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

#if use px
fruits = ["apples", "oranges", "bananas"]
fig = px.line(x=fruits, y=[1,3,2], color=px.Constant("This year"),
             labels=dict(x="Fruit", y="Amount", color="Time Period"))
fig.add_bar(x=fruits, y=[2,1,3], name="Last year")

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

#app = dash.Dash()
def empresarial():

    return html.Div([
            dcc.Graph(figure=fig),
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4),
            ])
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
