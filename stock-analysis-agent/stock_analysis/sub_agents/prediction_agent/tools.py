import yfinance as yf
from google.adk.tools import Tool

def get_historical_market_data(ticker: str) -> str:
    """Gets historical market data for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.history(period="max"))

historical_market_data_tool = Tool(
    name="get_historical_market_data",
    description="Gets historical market data for a given stock ticker.",
    func=get_historical_market_data,
)
