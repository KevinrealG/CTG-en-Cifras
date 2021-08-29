import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from empresarial import empresarial,tamano
from construcciones import estratos_construcciones, construcciones, top_5, Viviendas
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
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
        html.H2("Cartagena En Cifras", className="display-4"),
        html.Hr(),
        html.P(
            "Medible ", className="lead"
        ),
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
        return  html.P("this page is empty!")
    elif pathname == "/mercado_lab":
        return  html.P("this page is empty!")
    elif pathname == "/turismo":
        return  html.P("this page is empty!")
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
## aplicar lo mismo para year in tamaño
def generate_chart(values,year,tam):
    data=df.loc[df['Categoria']==values]
    fig = px.treemap(values=data[tam], path=[data['ACTIVIDAD']])
    fig2 = tamano(year)
    return fig2,fig
@app.callback(
    Output("pie-cont", "figure"),
     Input("trimestre", "value"),Input("year_estrato", "value"))
## aplicar lo mismo para year in tamaño
def cons(trimestre,year):
    fig = estratos_construcciones(year=year,trimestre=trimestre)
    return fig
@app.callback(
    Output("indice_1", "figure"),
    Output("indice_2", "figure"),
    Output("indice_3", "figure"),
     Input("year_indice", "value"))
## aplicar lo mismo para year in tamaño
def top(year):
    a,b,c = top_5(year=year)
    return a,b,c
@app.callback(
    Output("vivienda", "figure"),Input("year_vivienda", "value"))
## aplicar lo mismo para year in tamaño
def cons(year):
    fig = Viviendas(year=year)
    return fig
if __name__ == "__main__":
    app.run_server(port=8888,debug=True)
