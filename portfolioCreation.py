import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class PortfolioManager:
    def __init__(self, file_path):
        self.file_path = 'portfolio.xlsx'
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
        try:
            negative_values = (self.data < 0)
            if negative_values.any().any():
                negative_locs = np.where(negative_values)
                for loc in zip(*negative_locs):
                    print(f"Negative value at {self.data.index[loc[0]]}, {self.data.columns[loc[1]]}")
            else:
                print("No negative values found.")
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
    
    def create_portfolio(self, stock_names, weights, initial_budget, start_date, end_date):
        #Budget * weights
        bud_we = []
        try:
            # Validate inputs
            if not set(stock_names).issubset(set(self.data.index)):
                raise ValueError("One or more stocks are not available in the data.")
            if sum(weights) > 1:
                raise ValueError("Sum of weights cannot exceed 1.")
            if start_date not in self.data.columns or end_date not in self.data.columns:
                raise ValueError("Selected dates are not available in the data.")
                        
            # Create portfolio
            selected_data = self.data.loc[stock_names, start_date:end_date]
            print(f"Price of Selected Stock\n{selected_data}\n")

             # Initialize an empty DataFrame for returns
            returns_df = pd.DataFrame(index=selected_data.index, columns=selected_data.columns[1:])
            
            # Calculate returns
            for stock in selected_data.index:
                prices = selected_data.loc[stock]
                returns = (((prices[1:].values - prices[:-1].values) / prices[:-1].values)*100)
                returns_df.loc[stock] = returns
            
            # Print the DataFrame with returns
            print("DataFrame with Returns:\n", returns_df)

            for i in weights:
                new_multi = initial_budget*i
                bud_we.append(new_multi)
            print(bud_we)
            new_selected_data = 1/selected_data
            print(f"New Selected Data = 1/Selected Data \n{new_selected_data}\n")
            weighted_data = new_selected_data.multiply((bud_we), axis=0)
            print(f"Quantity of Stock according to budget and weights\n {weighted_data}\n")

            weighted_data = weighted_data.iloc[:, :-1]  # Drop the last column from weighted_data
            weighted_data.columns = returns_df.columns
            print("Dropped Colum Weighted Data\n")
            print(weighted_data)

            daily_individual_value = np.multiply(selected_data, weighted_data.iloc[:, 0].values[:, None])
            print("\n\n\nDaily Individual Value")
            print(daily_individual_value)

            final_individual_returns = ((daily_individual_value.iloc[:, -1] - daily_individual_value.iloc[:, 0]) / daily_individual_value.iloc[:, 0])*100
            print("\nFinal Individual Returns")
            print(final_individual_returns)


            final_portfolio_return = (final_individual_returns.mul(weights)).sum()
            print(f"\n\n\nFinal Portfolio Returns \n")


            # Plot portfolio
            #portfolio_value.plot(title='Portfolio Value Over Time')
            #plt.xlabel('Date')
            #plt.ylabel('Portfolio Value')
            #plt.show()
            
            #print(f"Portfolio return over the period: {portfolio_return:.2%}")
            
            
            return final_portfolio_return
        except Exception as e:
            print(f"Error creating portfolio: {e}")
    
    def fetch_data(self):
        return self.data
