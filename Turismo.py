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

path='Data/Turismo_consolidado_13.8.21.xlsx'
df_1=pd.read_excel(path,sheet_name='Ocupación_mensual')

df_1['date']= pd.to_datetime(df_1[["year", "month", "day"]])
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
df_2=pd.read_excel(path,sheet_name='sa_csa')

fig_2=px.area( x=df_1['date'], y=df_1['Ocupación'])
fig_2.update_layout(title='Ocupación Hotelera en Cartagena %, mensual')
fig_3 = go.Figure(data=[
    go.Bar(name='Salidas', x=df_2['Fecha'], y=df_2['Salidas']),
    go.Bar(name='Llegadas ', x=df_2['Fecha'], y=df_2['Llegadas']),

])
fig_3.update_layout(title='Pasajeros llegados y salidos, mensual',barmode='group')
#fig = px.bar(df, x="date", y=['Vacaciones, Ocio y Recreo',Trabajo y Negocios'], color="columns",
 #animation_frame="year", animation_group="country", range_y=[0,4000000000])
def Turismo():

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
                                                label="Ocupación Hotelera",
                                                value="data-entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [

                                                            html.H3('Ocupación Hotelera'),
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
                                                label="SACSA",
                                                value="entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                dcc.Graph(figure=fig_3)
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
