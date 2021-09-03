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

fig_2=px.area( x=df_1['date'], y=df_1['Ocupación'])
fig_2.update_layout(title='Ocupación Hotelera en Cartagena %, mensual')
#Sacsa
df_2=pd.read_excel(path,sheet_name='sa_csa')


fig_3 = go.Figure(data=[
    go.Bar(name='Salidas', x=df_2['Fecha'], y=df_2['Salidas']),
    go.Bar(name='Llegadas ', x=df_2['Fecha'], y=df_2['Llegadas']),

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

fig_sal.add_trace(go.Scatter(x=df_4['Time'],y = df_4['Cartagena']))
fig_sal.update_layout(title='Variación de Salarios Cartagena, por año y mes')
df_4_b=df_4.set_index('Time')
df_4_b=df_4_b.drop(columns=['Year','Month'])
df_4_b=df_4_b.rename_axis('regiones',axis='columns')


fig_sal_com=px.area(df_4_b, facet_col="regiones", facet_col_wrap=2)
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
                                                label="Pasajeros",
                                                value="entry",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                html.Div([
                                                   html.H3('Pasajeros LLEGADOS y SALIDOS de CARTAGENA'),
                                                   dcc.Graph(figure=fig_3),
                                                   html.H3('Pasajeros LLEGADOS y SALIDOS de CARTAGENA, según origen y destino'),
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
                                                html.H3('Variación Anual de Salarios en Cartagena'),
                                                dcc.Graph(id='Salarios',figure=fig_sal),
                                                html.H3('Comparación de Variación Anual de Salarios por región'),

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
                        className="app__container",
                    )
