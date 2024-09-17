from taskweaver.plugin import Plugin, register_plugin
try:
    import pandas as pd
    from prophet import Prophet
except ImportError:
    raise ImportError("Please install pandas and prophet first.")

@register_plugin
class ProphetForecastPlugin(Plugin):
    def __call__(self, series, last_date_index):
        """Prophet time series forecasting plugin implementation."""
        # Convert series to pandas DataFrame
        df = pd.DataFrame({'ds': pd.date_range(end=last_date_index, periods=len(series)), 'y': series})
        
        # Create and fit the Prophet model
        model = Prophet()
        model.fit(df)
        
        # Generate forecast
        future = model.make_future_dataframe(periods=30)  # 30-step forecast
        forecast = model.predict(future)
        
        # Return the forecast as a dictionary with the forecasted dates as keys
        return forecast.set_index('ds').to_dict('index')