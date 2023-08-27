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

def bubble_chart(data, px_kwargs={}, layout_kwargs={}):
    """
    Creates an interactive bubble chart Dash app that allows users to customize 
    the plot.

    Parameters::
    - data: Pandas DataFrame containing the data to plot
    - px_kwargs: Keyword arguments passed to plotly express 
    - layout_kwargs: Keyword arguments passed to plotly layout

    Outputs:
    A Dash app that generates an interactive bubble chart based on user input.

    The app allows the user to select the x, y, color, size, and hover text 
    variables to control the bubble chart plot. Additional customization like 
    font family and size are also provided.

    The app uses Dash callbacks to update the figure in response to user input.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The input data must be a pandas DataFrame.")

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Define the app layout
    app.layout = html.Div([
        html.H1("Custom Bubble Chart"),
        
        # First row with four dropdowns
        dbc.Row([
            # Dropdown for x variable
            dbc.Col([
                dcc.Dropdown(
                    id='x-variable-dropdown',
                    options=[{'label': col, 'value': col} for col in data.columns],
                    placeholder='Select X Variable'
                )
            ], width=3),

            # Dropdown for y variable
            dbc.Col([
                dcc.Dropdown(
                    id='y-variable-dropdown',
                    options=[{'label': col, 'value': col} for col in data.columns],
                    placeholder='Select Y Variable'
                )
            ], width=3),

            # Dropdown for color variable
            dbc.Col([
                dcc.Dropdown(
                    id='color-variable-dropdown',
                    options=[{'label': col, 'value': col} for col in data.columns],
                    placeholder='Select Color Variable'
                )
            ], width=3),

            # Dropdown for hover name variable
            dbc.Col([
                dcc.Dropdown(
                    id='hover-name-variable-dropdown',
                    options=[{'label': col, 'value': col} for col in data.columns],
                    placeholder="Select Hover Name Variable"
                )
            ], width=3)
        ], justify='center',style={'margin': '20px'}),

        # Second row with two dropdowns and one input
        dbc.Row([
            # Dropdown for size variable
            dbc.Col([
                dcc.Dropdown(
                    id='size-variable-dropdown',
                    options=[{'label': col, 'value': col} for col in data.columns],
                    placeholder="Select Size Variable"
                )
            ], width=4),

            # Dropdown for font family
            dbc.Col([
                dcc.Dropdown(
                    id='font-family-dropdown',
                    options=[{'label':font, 'value':font} for font in get_system_fonts()],
                    placeholder="Select Font Family"
                )
            ], width=4),

            # Font size input
            dbc.Col([
                dbc.Input(id='font-size-input', type='number', placeholder='Enter font size')
            ], width=4)
        ], justify='center',style={'margin': '20px'}),

        # Bubble chart
        dcc.Graph(id='bubble-chart')
    ])

    
    # Define callback to update the bubble chart based on user input
    @app.callback(
        Output('bubble-chart', 'figure'),
        Input('x-variable-dropdown', 'value'),
        Input('y-variable-dropdown', 'value'),
        Input('color-variable-dropdown', 'value'),
        Input('size-variable-dropdown', 'value'),
        Input('hover-name-variable-dropdown', 'value'),
        Input('font-family-dropdown', 'value'),
        Input('font-size-input', 'value')
    )
    def update_bubble_chart(x_variable, y_variable, color_variable, size_variable, hover_name_variable,
                            font_family, font_size):
        
        if x_variable is None or y_variable is None:
            return "please choose variable"
        
        fig = px.scatter(
            data,
            x=x_variable,
            y=y_variable,
            size=size_variable,
            color=color_variable,
            hover_name=hover_name_variable,
            **px_kwargs
        )

        fig.update_layout(
            font={'family': font_family, 'size': font_size},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            **layout_kwargs
        )
        
        fig.update_traces(selector=dict(type='scatter'))

        return fig


    app.run_server(mode='inline')