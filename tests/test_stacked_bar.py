
from dash import Dash, callback, html, Input, Output, ctx, callback, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import matplotlib.font_manager as fm
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

# Import the code to be tested
import sameh_stirling.charts.bubble_chart as st

# Create a sample data frame for testing
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'gender': ['F', 'M', 'M', 'M', 'F'],
    'age': [25, 32, 28, 35, 29],
    'height': [165, 180, 175, 185, 170],
    'weight': [55, 75, 70, 80, 60]
}

# Create a Dash app using the code to be tested
app = st.stacked_bar(data)

# Use the Dash testing framework to test the app
def test_stacked_bar(dash_duo):
    # Start the app in a test browser
    dash_duo.start_server(app)
    
    # Wait for the app to load
    dash_duo.wait_for_element('#bar-chart')
    
    # Select the x, y, and color columns from the dropdowns
    dash_duo.select_dcc_dropdown('#x-dropdown', value='name')
    dash_duo.select_dcc_dropdown('#y-dropdown', value='height')
    dash_duo.select_dcc_dropdown('#z-dropdown', value='gender')
    
    # Select the font and font size from the inputs
    dash_duo.select_dcc_dropdown('#font-dropdown', value='Arial')
    dash_duo.clear_input('#font-size-input')
    dash_duo.type_input('#font-size-input', value=18)
    
    # Wait for the chart to update
    dash_duo.wait_for_element('.trace.bars')
    
    # Check that the chart has the correct title and labels
    assert dash_duo.find_element('.gtitle').text == 'height by name colored by gender'
    assert dash_duo.find_element('.xtitle').text == 'name'
    assert dash_duo.find_element('.ytitle').text == 'height'
    
    # Check that the chart has the correct data and colors
    bars = dash_duo.find_elements('.trace.bars')
    assert len(bars) == 2 # Two traces for male and female
    assert bars[0].get_attribute('style') == 'fill: rgb(31, 119, 180);' # Blue for male
    assert bars[1].get_attribute('style') == 'fill: rgb(255, 127, 14);' # Orange for female
    
    bar_data = [bar.get_attribute('data-unformatted') for bar in bars]
    assert bar_data == ['180;175;185;;', ';165;;;170'] # Heights by gender
    
