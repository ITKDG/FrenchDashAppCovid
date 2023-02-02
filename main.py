import dash
from dash import Dash, html

BS1 = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
BS2 = "dbc.themes.BOOTSTRAP"

app = Dash(__name__, use_pages=True, title='Covid-19 Tracker', external_stylesheets=[BS1, BS2], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.layout = html.Div(
    [
        html.H1('Covid-19 Tracker - France 🇫🇷',
                style={
                       'textAlign': 'center',
                       'padding-top': '1%',
                       'padding-bottom': '1%',
                       'background-color': '#6495ED',
                       'color': 'white',
                       'position': 'sticky',
                       'top': '0',
                       'z-index': '3',
                       'transition': '1s',
                }),
        html.H4('Dyna Kheang',
                style={
                    'textAlign': 'center',
                    'color': '#4169E1'
                }),
        dash.page_container,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False)