import yfinance as yf
from google.adk.tools import Tool

def get_beta(ticker: str) -> str:
    """Gets the beta (market volatility) for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.info.get('beta'))

beta_tool = Tool(
    name="get_beta",
    description="Gets the beta (market volatility) for a given stock ticker.",
    func=get_beta,
)
