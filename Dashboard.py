import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from empresarial import empresarial,tamano
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
colors=['ffaa00', 'ffdd00', 'ff7b00','62bf41', '397224', 'e52d27' ,'b31217']
path='Data/base de dinamica.xlsx'
df=pd.read_excel(path,sheet_name='Actividades_1')
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
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
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
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
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
    Output("donut-chart", "figure"),
     Input("values", "value"),Input("year", "value"),Input("year2", "value"))
## aplicar lo mismo para year in tamaño
def generate_chart(values,year,year2):
    data=df.loc[df['Categoria']==values]
    fig = px.treemap( values=data[year2], path=[data['Actividad']])
    fig2 = tamano(year)
    return fig,fig2

if __name__ == "__main__":
    app.run_server(port=8888,debug=True)
