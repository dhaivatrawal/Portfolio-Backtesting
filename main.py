import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from portfolioCreation import PortfolioManager
from rebalancer import Rebalancer

if __name__ == "__main__":
    file_path = '/Users/dhaivatrawal/Desktop/portfolio_backtesting/portfolio.xlsx'
    
    # Example variables for portfolio creation
    stock_names = ['Asian Paints Ltd.', 'Reliance industries Limited', 'Infosys Limited']
    weights = [0.4, 0.3, 0.3]
    initial_budget = 1000
    start_date = pd.Timestamp('2018-01-01')
    end_date = pd.Timestamp('2018-12-31')
    
    # Example usage of Rebalancer
    fetcher = Rebalancer(file_path)
    fetcher.fetch_display()
    fetcher.check_neg()
    portfolio_value = fetcher.newPort(stock_names, weights, initial_budget, start_date, end_date)
  
    # Example variables for new budget calculation
    stocks_to_sell = ["Asian Paints Ltd.", "Reliance industries Limited"]
    new_stocks_to_buy = ["Zensar Technologies Limited", "UPL Limited"]
    start_date2 = pd.Timestamp('2018-06-25')
    weights2 = [0.5, 0.5]
    
    # Calculate and print new budget
    new_overall_budget = fetcher.new_budget(stocks_to_sell, start_date2)
    rebalanced_portfolio_value = fetcher.newPort(stock_names=new_stocks_to_buy, weights=weights2, initial_budget=new_overall_budget, start_date=start_date2, end_date=end_date)

    # Task: Select common stocks and modify portfolio_value DataFrame
    common_stocks = list(set(stock_names).intersection(stocks_to_sell))
    print(f"Common stocks to modify: {common_stocks}")

    if not common_stocks:
        print("No common stocks found between stock_names and stocks_to_sell.")
    else:
        # Create a copy of the original DataFrame to store the modified values
        modified_portfolio_value = portfolio_value.copy()

        # Set the values to 0 for the common stocks between start_date2 and end_date
        for stock in common_stocks:
            if stock in modified_portfolio_value.index:
                modified_portfolio_value.loc[stock, start_date2:end_date] = 0.0
            else:
                print(f"Stock {stock} not found in the portfolio_value DataFrame.")

        # Print the modified DataFrame
        print("Modified portfolio_value DataFrame with selected stocks' values set to 0:")
        print(modified_portfolio_value)


    # Ensure both DataFrames have the same columns
    rebalanced_portfolio_value = rebalanced_portfolio_value.reindex(columns=modified_portfolio_value.columns, fill_value=0)

    # Combine the DataFrames by adding the values
    combined_df = modified_portfolio_value.add(rebalanced_portfolio_value, fill_value=0)

    # Display the combined DataFrame
    print("Combined DataFrame with date format aligned with portfolio_value:")
    print(combined_df)

    portfolio_manager = PortfolioManager(file_path)
    daily_vals = portfolio_manager.daily_portfolio_val(combined_df)
    final_return = portfolio_manager.final_portfolio_return(daily_vals)
    print(f"{daily_vals}\n\n\n\n\n\nFinal Portfolio Return: {final_return}%")


