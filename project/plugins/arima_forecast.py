from taskweaver.plugin import Plugin, register_plugin
try:
    import pandas as pd
    from statsmodels.tsa.arima.model import ARIMA
except ImportError:
    raise ImportError("Please install necessary packages before running the plugin.")

@register_plugin
class ARIMAForecastPlugin(Plugin):
    def __call__(self, series, order, last_date_index):
        """ARIMA time series forecasting plugin implementation."""
        # Convert series to pandas Series
        series = pd.Series(series)
        
        # Set the last date index
        series.index = pd.date_range(end=last_date_index, periods=len(series))
        
        # Fit ARIMA model
        model = ARIMA(series, order=order)
        model_fit = model.fit()
        
        # Generate forecast
        forecast = model_fit.forecast(steps=30)[0]  # 30-step forecast
        
        # Create a date range for the forecasted dates
        forecast_index = pd.date_range(start=last_date_index, periods=30, freq='D')
        
        # Create a pandas Series for the forecast with the forecasted dates as index
        forecast_series = pd.Series(forecast, index=forecast_index)
        
        # Return the forecast as a dictionary with the index and values
        return forecast_series.to_dict()