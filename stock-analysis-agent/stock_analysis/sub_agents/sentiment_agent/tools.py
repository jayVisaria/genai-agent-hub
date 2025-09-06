import yfinance as yf
from google.adk.tools import Tool

def get_news(ticker: str) -> str:
    """Gets recent news articles for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.news)

news_tool = Tool(
    name="get_news",
    description="Gets recent news articles for a given stock ticker.",
    func=get_news,
)
