from taskweaver.plugin import Plugin, register_plugin
try:
    import pandas as pd
    import plotly.express as px
    import webbrowser
except ImportError:
    raise ImportError("Please install necessary packages before running the plugin.")

@register_plugin
class Plotly3DPlugin(Plugin):
    def __call__(self, data, x_axis, y_axis, z_axis):
        """Plotly 3D plot plugin implementation."""
        # Convert data to pandas DataFrame
        df = pd.DataFrame(data)
        
        # Create the 3D plot using Plotly Express
        fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis)
        
        # Create an HTML file for the plot
        html_file = 'plotly_3d_plot.html'
        with open(html_file, 'w') as f:
            f.write(fig.to_html(full_html=True))
        
        # Open the HTML file in a new browser window
        webbrowser.open('file://' + html_file)