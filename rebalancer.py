# rebalancer.py

from portfolioCreation import PortfolioManager

class Rebalancer:
    def __init__(self, file_path):
        self.portfolio_manager = PortfolioManager(file_path)
        self.individual_stock_value = None  # Initialize to None

    def fetch_display(self):
        data = self.portfolio_manager.fetch_data()
        print("Data from PortfolioManager:")
        print(data)
        return data
    
    def check_neg(self):
        try:
            self.jayesh = self.portfolio_manager.check_negative_values()
            print("Value of Jayesh:", self.jayesh)
        except Exception as e:
            print(f"Error in check_neg: {e}")

    def newPort(self, stock_names, weights, initial_budget, start_date, end_date):
        try:
            _, self.individual_stock_value = self.portfolio_manager.create_portfolio(
                stock_names=stock_names,
                weights=weights,
                initial_budget=initial_budget,
                start_date=start_date,
                end_date=end_date
            )
            print(f"Value of My Portfolio {self.individual_stock_value}")
            return self.individual_stock_value
        except Exception as e:
            print(f"Error in newPort: {e}")

    def new_budget(self, stocks_to_sell, start_date2):
        try:
            new_total_budget = 0
            for stock_name in stocks_to_sell:
                if stock_name in self.individual_stock_value.index:
                    new_total_budget += self.individual_stock_value.loc[stock_name, start_date2]
                else:
                    print(f"Stock '{stock_name}' not found in portfolio.")
            print(f"Total budget for stocks to sell at {start_date2}: {new_total_budget}")
            return new_total_budget
        except Exception as e:
            print(f"Error calculating new budget: {e}")
    
    def new_bud_we(self, weights, initial_budget):
        try:
            self.new_weighte_budget = self.portfolio_manager.compute_budget_weights(
                weights=weights,
                initial_budget = initial_budget
            )
            print(f"Total weighted remaining balance {self.new_weighte_budget}")
            return self.new_weighte_budget
        except Exception as e:
            print(f"Error in new_bud_we: {e}")

    def lola(self):
        a = 1
        b = 2
        c =a+b
        try:
            if(c==4):
                print(c)
        except Exception as e:
            print(f"Error in your code {e}")
        return 0