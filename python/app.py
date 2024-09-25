from aio_components import MarkdownWithColorAIO
from dash import Dash, html

app = Dash(__name__)

app.layout = MarkdownWithColorAIO('## Hello World')

if __name__ == "__main__":
    app.run(debug=False)