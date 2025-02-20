from crewai.tools import BaseTool
import yfinance as yf

class StockDataTool(BaseTool):
    name: str = "Stock Data Tool"
    description: str = "Fetch stock data from Yahoo Finance"
    _cache = {}  # Cache to store stock data

    def _run(self, ticker: str) -> dict:
        """Fetch stock data from Yahoo Finance."""
        if ticker in self._cache:
            return self._cache[ticker]  # Return cached data if available

        try:
            stock = yf.Ticker(ticker)
            data = stock.info
            if not data:
                return {"error": "No data found for the given ticker."}
            
            result = {
                "Name": data.get("longName"),
                "Current Price": data.get("currentPrice"),
                "Market Cap": data.get("marketCap"),
                "PE Ratio": data.get("trailingPE"),
                "EPS": data.get("trailingEps"),
                "52 Week High": data.get("fiftyTwoWeekHigh"),
                "52 Week Low": data.get("fiftyTwoWeekLow")
            }
            self._cache[ticker] = result  # Cache the result
            return result
        except Exception as e:
            return {"error": str(e)}