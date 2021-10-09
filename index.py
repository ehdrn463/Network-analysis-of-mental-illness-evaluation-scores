
from dash import html

from app import app
import callbacks
import layout as lo


app.layout = html.Div([lo.sidebar, lo.content])
app.title = "Network analysis of mental illness evaluation scores"

if __name__ == '__main__':
    app.run_server(port='8085')