import yfinance as yf
from google.adk.tools import Tool

def get_stock_info(ticker: str) -> str:
    """Gets general information for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.info)

stock_info_tool = Tool(
    name="get_stock_info",
    description="Gets general information for a given stock ticker.",
    func=get_stock_info,
)
