import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
import plotly.graph_objects as go # or plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
path='Data/Construcciones.xlsx'
data_4=pd.read_excel(path,sheet_name='vivienda')
fig = px.icicle(data_4, path=[px.Constant("all"),'tipo','vis', 'estrato'], values='area')
import dash
import dash_core_components as dcc
import dash_html_components as html
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/96c0bd/sunburst-coffee-flavors-complete.csv')

fig = go.Figure(
    go.Icicle(
        ids = df.ids,
        labels = df.labels,
        parents = df.parents,
        root_color="lightgrey",
        tiling = dict(
            orientation='h',
            flip='x'
        )
    )
)
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)
