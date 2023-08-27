# sameh_stirling

The `sameh_stirling` module contains functions for creating interactive Dash charts.

## Installation

```
pip install sameh-stirling
```

## Usage

The module contains two chart functions:

### stacked_bar

Creates an interactive stacked bar chart using Plotly Dash.

```python
from sameh_stirling.stacked_bar import stacked_bar
import pandas as pd

data = pd.DataFrame({
    "name": ["Ashley", "Ashley", "Ashley", "Patricia", "Patricia", "Patricia", "Betty", "Betty", "Betty", "Helen", "Helen", "Helen"],
    "year": [1920, 1960, 2000, 1920, 1960, 2000, 1920, 1960, 2000, 1920, 1960, 2000],
    "n": [2089, 17503, 17997, 6199, 47952, 7453, 22877, 11378, 880, 70621, 40471, 6909]
})

stacked_bar(data, layout_kwargs={}, px_kwargs={})
```

- `data` (DataFrame): DataFrame containing the data
- `layout_kwargs` (dict): Keyword arguments passed to `plotly.layout` - optional
- `px_kwargs` (dict): Keyword arguments passed to `plotly.express` -optional

### bubble_chart 

Creates an interactive bubble chart using Plotly Dash.

```python 
from sameh_stirling.bubble_chart import bubble_chart 
import plotly.express as px
data = px.data.gapminder()

bubble_chart(data, layout_kwargs={}, px_kwargs={})
```

- `data` (DataFrame): DataFrame containing the data
- `layout_kwargs` (dict): Keyword arguments passed to `plotly.layout` - optional
- `px_kwargs` (dict): Keyword arguments passed to `plotly.express` -optional

Both functions return a Dash app that can be run with `app.run_server()`.

The charts allow selecting dimensions, customizing the font, and passing keyword arguments to `plotly.express` and `plotly.layout` to customize the appearance.

See the source code for more details on usage and customization options.

## Contributing

Contributions to add more charts are welcome! Please open an issue or PR.

## License

MIT
