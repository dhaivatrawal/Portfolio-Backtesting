# portfolioCreation.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class PortfolioManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.load_data()
    
    def load_data(self):
        try:
            self.data = pd.read_excel(self.file_path, sheet_name='2018')
            self.data.set_index(self.data.columns[0], inplace=True)
            self.data.columns = pd.to_datetime(self.data.columns)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def check_negative_values(self):
        jayesh = 69
        try:
            negative_values = (self.data < 0)
            if negative_values.any().any():
                negative_locs = np.where(negative_values)
                for loc in zip(*negative_locs):
                    print(f"Negative value at {self.data.index[loc[0]]}, {self.data.columns[loc[1]]}")
            else:
                print("No negative values found.")
            return jayesh
        except Exception as e:
            print(f"Error checking negative values: {e}")
    
    def plot_stock(self, stock_name):
        try:
            if stock_name in self.data.index:
                self.data.loc[stock_name].plot(title=stock_name)
                plt.xlabel('Date')
                plt.ylabel('Price')
                plt.show()
            else:
                print(f"Stock {stock_name} not found in data.")
        except Exception as e:
            print(f"Error plotting stock: {e}")
    
    def calculate_returns(self, selected_data):
        try:
            returns_df = pd.DataFrame(index=selected_data.index, columns=selected_data.columns[1:])
            for stock in selected_data.index:
                prices = selected_data.loc[stock]
                returns = (((prices[1:].values - prices[:-1].values) / prices[:-1].values) * 100)
                returns_df.loc[stock] = returns
            return returns_df
        except Exception as e:
            print(f"Error calculating returns: {e}")
            return pd.DataFrame()
    
    def compute_budget_weights(self, weights, initial_budget):
        try:
            bud_we = [initial_budget * i for i in weights]
            return bud_we
        except Exception as e:
            print(f"Error computing budget weights: {e}")
            return []
    
    def daily_portfolio_val(self, individual_stock_value):
        try:
            return individual_stock_value.sum()
        except Exception as e:
            print(f"Error calculating daily portfolio values: {e}")
            return pd.Series()
    
    def final_portfolio_return(self, daily_portfolio_val):
        try:
            return ((daily_portfolio_val.iloc[-1] - daily_portfolio_val.iloc[0]) / daily_portfolio_val.iloc[0]) * 100
        except Exception as e:
            print(f"Error calculating final portfolio return: {e}")
            return 0
    
    def create_portfolio(self, stock_names, weights, initial_budget, start_date, end_date):
        try:
            if not set(stock_names).issubset(set(self.data.index)):
                raise ValueError("One or more stocks are not available in the data.")
            if sum(weights) > 1:
                raise ValueError("Sum of weights cannot exceed 1.")
            if start_date not in self.data.columns or end_date not in self.data.columns:
                raise ValueError("Selected dates are not available in the data.")

            selected_data = self.data.loc[stock_names, start_date:end_date]
            print(f"Price of Selected Stock\n{selected_data}\n")

            returns_df = self.calculate_returns(selected_data)
            print("DataFrame with Returns:\n", returns_df)

            bud_we = self.compute_budget_weights(weights, initial_budget)
            print(bud_we)

            individual_stock_value = pd.DataFrame(index=selected_data.index, columns=selected_data.columns[:])
            print(f"individual_stock_value\n\n\n{individual_stock_value}")

            individual_stock_value[start_date] = bud_we
            print(f"Updated individual_stock_value with bud_we values at {start_date}:\n{individual_stock_value}\n")

            for date in selected_data.columns[1:]:
                prev_date = selected_data.columns[selected_data.columns.get_loc(date) - 1]
                individual_stock_value[date] = individual_stock_value[prev_date] * (1 + (returns_df[date] / 100))
            print(f"Updated individual_stock_value for {date}:\n{individual_stock_value}\n")

            final_individual_returns = ((individual_stock_value.iloc[:, -1] - individual_stock_value.iloc[:, 0]) / individual_stock_value.iloc[:, 0]) * 100
            print("\nFinal Individual Returns")
            print(final_individual_returns)

            daily_portfolio_val = self.daily_portfolio_val(individual_stock_value)
            print(f"\n\n\n\n\nDaily Portfolio Val {daily_portfolio_val}")

            final_portfolio_return = self.final_portfolio_return(daily_portfolio_val)
            print(f"\n\n\nFinal Portfolio Returns \n{final_portfolio_return}")

            return final_portfolio_return, individual_stock_value

        except Exception as e:
            print(f"Error creating portfolio: {e}")
    
    def fetch_data(self):
        return self.data
