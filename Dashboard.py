import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from empresarial import empresarial,tamano
from construcciones import estratos_construcciones, construcciones, top_5, Viviendas, destinos, top_5_des, ICCV
from Pobreza import pobreza, lineas, lineas_pesos, Comparativo
from Mercado_lab import mercado, acti_merc
from Turismo import Turismo, sac_dis
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px

#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
#[dbc.themes.LUX])
app = dash.Dash(external_stylesheets=[dbc.themes.LUX],suppress_callback_exceptions=True)
colors=['ffaa00', 'ffdd00', 'ff7b00','62bf41', '397224', 'e52d27' ,'b31217']
path='Data/base de dinamica.xlsx'
df=pd.read_excel(path,sheet_name='Acti_tamaño')
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "border": "5px solid #4CAF55"
}

sidebar = html.Div(
    [
        html.H4("Cartagena En Cifras", className="display-4"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Dinamica Empresarial", href="/dinamica-empresarial", active="exact"),
                dbc.NavLink("Construcciones", href="/construcciones", active="exact"),
                dbc.NavLink("Pobreza", href="/pobreza", active="exact"),
                dbc.NavLink("Mercado Laboral", href="/mercado_lab", active="exact"),
                dbc.NavLink("Turismo", href="/turismo", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/dinamica-empresarial":
        return [ empresarial()]
    elif pathname == "/construcciones":
        return  [ construcciones()]
    elif pathname == "/pobreza":
        return  [ pobreza()]
    elif pathname == "/mercado_lab":
        return  [ mercado()]
    elif pathname == "/turismo":
        return [ Turismo()]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
@app.callback(
    Output("pie-chart", "figure"),
    Output("treemap-chart", "figure"),
     Input("values", "value"),Input("year", "value"),Input("tam", "value"))
def generate_chart(values,year,tam):
    data=df.loc[df['Categoria']==values]
    fig = px.treemap(values=data[tam], path=[data['ACTIVIDAD']])
    fig.update_layout(title='Actividades Economicas de empresas de tamaño '+tam+' según: '+values,margin = dict(t=50, l=25, r=25, b=25))
    fig2 = tamano(year)
    return fig2,fig
@app.callback(
    Output("pie-cont", "figure"),
     Input("trimestre", "value"),Input("year_estrato", "value"))
def cons(trimestre,year):
    fig = estratos_construcciones(year=year,trimestre=trimestre)
    return fig
@app.callback(
    Output("sacsa", "figure"),
    Output("sacsa_1", "figure"),
     Input("month_sac", "value"),Input("year_sac", "value"))
def cons(month,year):
    fig,b = sac_dis(year=year,mes=month)
    return fig,b
@app.callback(
    Output("indice_1", "figure"),
    Output("indice_2", "figure"),
    Output("indice_3", "figure"),
     Input("year_indice", "value"))
def top(year):
    a,b,c = top_5(year=year)
    return c,a,b
@app.callback(
    Output("vivienda", "figure"),Input("year_vivienda", "value"))
def cons(year):
    fig = Viviendas(year=year)
    return fig
@app.callback(
    Output("destinos_1", "figure"),
    Output("destinos_2", "figure"),
     Input("trimestre_des", "value"),Input("year_destino", "value"))
def dest(trimestre,year):
    fig_1 = destinos(year=year,trimestre=trimestre)
    fig_2 = top_5_des(year=year)
    return fig_1, fig_2

@app.callback(
    Output("Lineas_1", "figure"),
    Input("linea_drop", "value"))
def line(linea):
    fig_1 = lineas(Lineas=linea)

    return fig_1
@app.callback(
    Output("Lineas_2", "figure"),
    Input("linea_pesos", "value"))
def line(linea):
    fig_1 = lineas_pesos(Lineas=linea)

    return fig_1
@app.callback(
    Output("Ocupación_3", "figure"),
    Input("year_mercado", "value"))
def acti_mer(year):
    fig_1 = acti_merc(year=year)

    return fig_1
@app.callback(
    Output("Lineas_3", "figure"),Output("Lineas_4", "figure"),Input("year_pobre", "value"))
def cons(year):
    fig,fig2= Comparativo(year=year)
    return fig,fig2
@app.callback(
    Output("ICCV_1", "figure"),
    Output("ICCV_2", "figure"),

     Input("ICCV", "value"))
def iccv(tipo):
    a,b = ICCV(tipo=tipo)
    return b,a
if __name__ == "__main__":
    app.run_server(port=8888,debug=True)
