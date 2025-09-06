import yfinance as yf
from google.adk.tools import Tool

def get_sustainability_info(ticker: str) -> str:
    """Gets sustainability (ESG) information for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.sustainability)

sustainability_info_tool = Tool(
    name="get_sustainability_info",
    description="Gets sustainability (ESG) information for a given stock ticker.",
    func=get_sustainability_info,
)
