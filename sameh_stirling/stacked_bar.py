import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import matplotlib.font_manager as fm

def get_system_fonts():
    font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_names = [fm.FontProperties(fname=font_file).get_name() for font_file in font_list]
    return font_names

def stacked_bar(data, px_kwargs={}, layout_kwargs={}):
    
    """Creates an interactive stacked bar chart using Plotly Dash.
    
    The chart allows the user to select the x, y, and color dimension from dropdown menus.
    It also allows selecting the font and font size for the chart.
    
     Parameters:
    
    - data (dict): The data to plot as a dictionary of columns 
    - px_kwargs (dict): Keyword arguments passed to plotly express
    - layout_kwargs (dict): Keyword arguments passed to plotly layout
    
    It returns a Dash app that can be run with app.run_server().
    
    """
    
    df = pd.DataFrame(data)
    available_fonts = get_system_fonts()
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    """
    - A dropdown is created for selecting x, y, and color columns
    - A dropdown is created for selecting font  
    - An input is created for selecting font size
    """
    
    app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='x-dropdown', placeholder='Select X Column')),
        dbc.Col(dcc.Dropdown(id='y-dropdown', placeholder='Select Y Column')),
        dbc.Col(dcc.Dropdown(id='z-dropdown', placeholder='Select coloring Column')),
    ], style={'margin': 20}),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='font-dropdown',
                             options=[{'label': font, 'value': font} for font in available_fonts],
                             #value=available_fonts[0],
                             placeholder='Select Font')),
        dbc.Col(dcc.Input(id='font-size-input', type='number', value=12)),
    ]),
    dcc.Graph(id='bar-chart'),
],style={'margin': 20})

    """
    Callbacks update the options and figure based on selections.
    
    A stacked bar chart is produced using plotly express and customized with:
    
    - x, y, color dimensions from dropdowns
    - Font size and family from inputs
    - kwargs passed to px and layout
    """

    @app.callback(
        Output('x-dropdown', 'options'),
        Output('y-dropdown', 'options'),
        Output('z-dropdown', 'options'),
        Input('bar-chart', 'figure')
    )
    def update_dropdown_options(figure):
        x_options = [{'label': col, 'value': col} for col in df.columns]
        y_options = [{'label': col, 'value': col} for col in df.columns]
        z_options = [{'label': col, 'value': col} for col in df.columns]
        return x_options, y_options, z_options

    @app.callback(
        Output('bar-chart', 'figure'),
        Input('x-dropdown', 'value'),
        Input('y-dropdown', 'value'),
        Input('z-dropdown', 'value'),
        Input('font-dropdown', 'value'),  # Add font dropdown input
        Input('font-size-input','value')
    )
    def update_bar_chart(x_col, y_col, z_col, selected_font, font_size):
        if x_col and y_col and z_col:
            font = {'family': selected_font, 'size': font_size}
            fig = px.bar(df, x=x_col, y=y_col, color=z_col,**px_kwargs)
            fig.update_layout(barmode='stack', font=font, **layout_kwargs)
            return fig
        else:
            return {}

    app.run_server(mode='inline')
    