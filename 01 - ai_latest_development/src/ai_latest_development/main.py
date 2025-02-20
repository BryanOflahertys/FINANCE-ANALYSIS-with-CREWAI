#!/usr/bin/env python
import sys
import warnings
from crew import FinancialAnalysisCrew

warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    """
    Run the financial analysis crew.
    """
    company_stock = input("Enter stock ticker (e.g., AAPL for Apple): ").upper()

    crew_instance = FinancialAnalysisCrew()
    
    # Fetch and display stock data before running AI Crew
    stock_data = crew_instance.stock_tool._run(company_stock)
    print("\n=== Stock Data from Yahoo Finance ===")
    for key, value in stock_data.items():
        print(f"{key}: {value}")

    print("\n=== Running Financial Analysis Crew ===")
    crew_instance.crew().kickoff()

if __name__ == "__main__":
    run()