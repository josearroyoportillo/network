import dash_auth
# import dash_bootstrap_components as dbc
import dash_core_components as dcc
# from app_sunburst import sunburst_layout
from dash.dependencies import Input, Output
import dash_html_components as html

from app import app
from app_network import network
from app_network_dataframe import network_dataframe

server = app.server  # this is for if you want to use the server in Heroku

auth = dash_auth.BasicAuth(
    app,
    {'user': 'pass'})  # this is for if you want to use basic security with heroku


# creation of app tabs
app.layout = html.Div([dcc.Tabs(id='tabs', value='network-dataframe', children=[
                dcc.Tab(label='Netzwerk-Daten', value='network-dataframe'),
                dcc.Tab(label='Netzwerkdarstellung', value='network'),
                dcc.Tab(label='Sunburstdarstellung', value='sunburst')
        ]),
        html.Div(id='tabs-content')
])


# app callback decorator to switch tabs and push content display
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def switch_tab(tab):
    if tab == 'network-dataframe':
        return network_dataframe
    elif tab == 'network':
        return network
    elif tab == 'sunburst':
        return html.Div([html.H1('SUNBURST')])


if __name__ == '__main__':
    app.run_server(debug=True)  # turn debug to false if using on Heroku
