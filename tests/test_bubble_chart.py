from dash import Dash, callback, html, Input, Output, ctx, callback, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import matplotlib.font_manager as fm
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
# Import the code to be tested
import sameh_stirling.charts.bubble_chart as sb

# Create a sample data frame for testing
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'gender': ['F', 'M', 'M', 'M', 'F'],
    'age': [25, 32, 28, 35, 29],
    'height': [165, 180, 175, 185, 170],
    'weight': [55, 75, 70, 80, 60]
}

# Create a Dash app using the code to be tested
app = sb.bubble_chart(data)

# Use the Dash testing framework to test the app
def test_bubble_chart(dash_duo):
    # Start the app in a test browser
    dash_duo.start_server(app)
    
    # Wait for the app to load
    dash_duo.wait_for_element('#bubble-chart')
    
    # Select the x, y, color, size, and hover name variables from the dropdowns
    dash_duo.select_dcc_dropdown('#x-variable-dropdown', value='age')
    dash_duo.select_dcc_dropdown('#y-variable-dropdown', value='weight')
    dash_duo.select_dcc_dropdown('#color-variable-dropdown', value='gender')
    dash_duo.select_dcc_dropdown('#size-variable-dropdown', value='height')
    dash_duo.select_dcc_dropdown('#hover-name-variable-dropdown', value='name')
    
    # Select the font family and font size from the inputs
    dash_duo.select_dcc_dropdown('#font-family-dropdown', value='Times New Roman')
    dash_duo.clear_input('#font-size-input')
    dash_duo.type_input('#font-size-input', value=16)
    
    # Wait for the chart to update
    dash_duo.wait_for_element('.trace.scattergl')
    
    # Check that the chart has the correct title and labels
    assert dash_duo.find_element('.gtitle').text == 'weight by age colored by gender'
    assert dash_duo.find_element('.xtitle').text == 'age'
    assert dash_duo.find_element('.ytitle').text == 'weight'
    
    # Check that the chart has the correct data and colors
    markers = dash_duo.find_elements('.trace.scattergl .points path')
    assert len(markers) == 5 # Five points for five names
    assert markers[0].get_attribute('style') == 'fill: rgb(255, 127, 14);' # Orange for female Alice
    assert markers[1].get_attribute('style') == 'fill: rgb(31, 119, 180);' # Blue for male Bob
    
    marker_data = [marker.get_attribute('data-unformatted') for marker in markers]
    assert marker_data == ['25;55;165;Alice;F', '32;75;180;Bob;M', '28;70;175;Charlie;M',
                           '35;80;185;David;M', '29;60;170;Eve;F'] # Age, weight, height, name, gender
    
