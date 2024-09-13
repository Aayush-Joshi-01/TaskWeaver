from taskweaver.plugin import Plugin,register_plugin
from datetime import datetime
 
try:
   import yfinance as yf
except:
   print("Import the required modules yfinance")
 
@register_plugin
class GetStockPriceplugin(Plugin):
   @staticmethod
   def __call__(stock_symbol:str, start_date:str, end_date:str):
      stock=yf.Ticker(stock_symbol)
      stock_data = stock.get_shares_full(start=start_date, end=end_date)
      return stock_data