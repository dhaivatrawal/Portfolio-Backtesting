import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from portfolioCreation import PortfolioManager

# Example usage
portfolio_manager = PortfolioManager('/Users/dhaivatrawal/Desktop/portfolio_backtesting/portfolio.xlsx')
portfolio_manager.check_negative_values()
#portfolio_manager.plot_stock('Asian Paints Ltd.')
stock_returns = portfolio_manager.create_portfolio(
    stock_names=['Asian Paints Ltd.', 'Reliance industries Limited', 'Infosys Limited'],
    weights=[0.4, 0.3, 0.3],
    initial_budget=1000,
    start_date=pd.Timestamp('2018-01-01'),
    end_date=pd.Timestamp('2018-12-31')
)
print(stock_returns)