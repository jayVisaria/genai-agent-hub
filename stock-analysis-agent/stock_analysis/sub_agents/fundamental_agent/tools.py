import yfinance as yf
from google.adk.tools import Tool

def get_income_statement(ticker: str) -> str:
    """Gets the income statement for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.income_stmt)

def get_balance_sheet(ticker: str) -> str:
    """Gets the balance sheet for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.balance_sheet)

def get_cash_flow(ticker: str) -> str:
    """Gets the cash flow statement for a given stock ticker."""
    stock = yf.Ticker(ticker)
    return str(stock.cashflow)

income_statement_tool = Tool(
    name="get_income_statement",
    description="Gets the income statement for a given stock ticker.",
    func=get_income_statement,
)

balance_sheet_tool = Tool(
    name="get_balance_sheet",
