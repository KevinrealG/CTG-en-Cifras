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

                                                            dcc.Graph(figure=fig2),
                                                            dcc.Graph(figure=fig1),
                                                            dcc.Graph(figure=fig),
                                                        ],
                                                        className="container__1",
                                                    )
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
