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
import dash_table
#import dash_leaf_leat



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
#if use px
#fruits = ["apples", "oranges", "bananas"]
#fig = px.line(x=fruits, y=[1,3,2], color=px.Constant("This year"),
#             labels=dict(x="Fruit", y="Amount", color="Time Period"))
#fig.add_bar(x=fruits, y=[2,1,3], name="Last year")

#It's upload the Dinamica Data
path='Data/Mercado laboral_consolidado_.xlsx'
data=pd.read_excel(path,sheet_name='Indicadores')
fig_ocu = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data['TO'][data['AÑO'].size-1],
    delta = {"reference":  data['TO'][data['AÑO'].size-2], "valueformat": ".1f"},
    title = {"text": "Resultado"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

fig_ocu.add_trace(go.Scatter(x=data['TRIMESTRE'],y = data['TO']))
fig_ocu.update_layout(title='Tasa de Ocupación Cartagena, trimestres móviles')
#ACTIVIDAD Economica
data_2=pd.read_excel(path,sheet_name='Act económica')
data_2=data_2.drop(columns=['Ocupados Cartagena','TRIMESTRE'])
data_2=data_2.groupby('AÑO').mean()

def acti_merc(year=2020,df=data_2):
    #new_df=df.loc[year]
    #new_df=new_df.drop('Ocupados Cartagena')
    #new_df=new_df.loc[:,'Agricultura, ganadería, caza, silvicultura y pesca':'Genero']
    #new_df=new_df.rename_axis('Actividades',axis='columns')
    new_df=df.loc[year]
    fig=go.Figure(go.Bar(x=new_df.index, y=new_df.values,marker_color='#62bf41'))
    fig.update_layout(title='Ocupación de Cartagena según Actividades Economicas en el Año: '+str(year))
    return fig




#Generos
data_3=pd.read_excel(path,sheet_name='ML_Hombres')
data_3_a=data_3.loc[:,'TRIM':'Genero']
#data_3=data_3.rename_axis('Estratos',axis='columns')

fig_gen = px.area(data_3_a, x="TRIM", y="TO",color='Genero', facet_col="Genero", facet_col_wrap=2)
fig_gen_des = px.area(data_3_a, x="TRIM", y="TD",color='Genero', facet_col="Genero", facet_col_wrap=2)

#figy = px.area(data_3_a, facet_col="Estratos", facet_col_wrap=2)

#desocupados
fig_des = make_subplots(specs=[[{"secondary_y": True}]])

fig_des.add_trace(
    go.Scatter(name='Tasa de Desempleo',
        x=data['TRIMESTRE'],
        y=data['TD']
    ),
    secondary_y=True,
    )

fig_des.add_trace(
    go.Bar(name='desocupados',
        x=data['TRIMESTRE'],
        y=data['Desocupados']
    ))
fig_des.update_layout(title='Desocupados y tasa de Desempleo Cartagena',barmode='group')
Car_1 = go.Figure(go.Indicator(
mode = "gauge+number",
value =  data['TD'][data['AÑO'].size-1],
title = {'text': "Tasa de Desempleo"},
delta = {'reference':  data['TD'][data['AÑO'].size-2]},
domain = {'x': [0, 1], 'y': [0, 1]}
    ))
data_3=pd.read_excel(path,sheet_name='ML_juventud')
Jovenes_oc = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data_3['TO'][data_3['AÑO'].size-1],
    delta = {"reference":  data_3['TO'][data_3['AÑO'].size-2], "valueformat": ".2f"},
    title = {"text": "Resultado"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

Jovenes_oc.add_trace(go.Scatter(x=data_3['TRIMESTRE'],y = data_3['TO']))
Jovenes_oc.update_layout(title='Tasa de Ocupación de Jovenes Cartagena, trimestres móviles')
jovenes_doc = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data_3['TD'][data_3['AÑO'].size-1],
    delta = {"reference":  data_3['TD'][data_3['AÑO'].size-2], "valueformat": ".2f"},
    title = {"text": "Resultado"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

jovenes_doc.add_trace(go.Scatter(x=data_3['TRIMESTRE'],y = data_3['TD']))
jovenes_doc.update_layout(title='Tasa de Desocupación de Jovenes Cartagena, trimestres móviles')
#Informales
data_4=pd.read_excel(path,sheet_name='Informalidad')

Informales = go.Figure(go.Indicator(

    mode = "number+delta",
    value = data_4['TI'][data_4['AÑO'].size-1],
    delta = {"reference":  data_4['TI'][data_4['AÑO'].size-2], "valueformat": ".2f"},
    title = {"text": "Resultado"},
    domain = {'y': [0, 1], 'x': [0.25, 0.75]})
    )

Informales.add_trace(go.Scatter(x=data_4['TRIM'],y = data_4['TI']))
Informales.update_layout(title='Tasa de Ocupación de Jovenes Cartagena, trimestres móviles')
Car_2 = go.Figure(go.Indicator(
mode = "gauge+number",
value =  data_4['Informales'][data_4['AÑO'].size-1],
title = {'text': "Tasa de Desempleo"},
delta = {'reference':  data_4['Informales'][data_4['AÑO'].size-2],'relative': True},
domain = {'x': [0, 1], 'y': [0, 1]}
    ))

def mercado():

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
                                        value="data_1",
                                        children=[
                                            dcc.Tab(
                                                label="Ocupación",
                                                value="data_1",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                    html.Div(
                                                        [

                                                            html.H3("Tasa de Ocupación Laboral de Cartagena", style=title_style),
                                                            dcc.Graph(id="Ocupación_1",figure=fig_ocu),
                                                            html.H4("Tasa de Ocupación Laboral por Géneros"),
                                                            dcc.Graph(id="Ocupación_2",figure=fig_gen),
                                                            html.H4("Ocupación Laboral por Actividades Económicas"),
                                                            dcc.Dropdown(
                                                                id='year_mercado',
                                                                value=2020,
                                                                options=[{'value': x, 'label': x}
                                                                         for x in range(2015,2022)],
                                                                clearable=False
                                                            ),
                                                            dcc.Graph(id="Ocupación_3"),
                                                            html.H4("Tasa de Ocupación Laboral de Jovenes"),
                                                            dcc.Graph(id="Ocupación_2",figure=Jovenes_oc),

                                                        ],
                                                        className="container__1",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Desempleo",
                                                value="data_2",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                html.H3("Tasa de Desempleo de Cartagena", style=title_style),
                                                dcc.Graph(id="Ocupación_1",figure=fig_des),
                                                dcc.Graph(id="Ocupación_2",figure=Car_1),
                                                html.H4("Tasa de Desocupación Laboral de Jovenes"),
                                                dcc.Graph(id="Ocupación_2",figure=jovenes_doc),
                                                html.H4("Tasa de Desocupación Laboral por Géneros"),
                                                dcc.Graph(id="Ocupación_2",figure=fig_gen_des),


                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Informales",
                                                value="data_4",
                                                style=tab_style,
                                                selected_style=tab_selected_style,
                                                children=[
                                                html.H3("Tasa de Informalidad de Cartagena", style=title_style),
                                                dcc.Graph(id="Ocupación_1",figure=Car_2),
                                                dcc.Graph(id="Ocupación_2",figure=Informales),


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
