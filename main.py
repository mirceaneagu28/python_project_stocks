import pandas as pd
import random
import os
from datetime import timedelta

# create this function to choose 10 data points that are consecutive
def choose_random_values (file_path):

# select the column for date time (column 2 in .csv files), then we have to sort ti by date
    df = pd.read_csv(file_path, header = None, parse_dates = [1], dayfirst = True)  #dayfirst because date format is "day first"
    df.columns = ['StockID','Date','Price'] # set name for columns, as it's not present in file
    df.sort_values (by = "Date",inplace = True)

# we have to check that the first value has minimum 9 other values after
# this request is mandatory because we have to take 10 data points
    max_first_date = len(df) - 10
    if max_first_date < 0:
        raise ValueError("It's impossible to take 10 consecutive data points from this date")

    # here it will e selected a random point from where to start
    start_index = random.randint(0, max_first_date)
    all_dates = df.iloc[start_index:start_index + 10].copy()

    return all_dates

# function to predict the next 3 values based on the logic provided in pdf with request
def predict_next_values(stock_data):
    # we take here into accout that stock_data is a DataFrame that has 10 consecutive values
    last_stock_id = stock_data['StockID'].iloc[0]
    last_date = stock_data['Date'].iloc[-1]
    last_price = stock_data['Price'].iloc[-1]

    # we have to find the second highest priced value of stock
    second_highest_value = stock_data['Price'].nlargest(2).iloc[-1]  # Get the 2nd highest

    # here the calculation of n+1 (2nd highest value)
    n_plus_1 = second_highest_value

    # calc n+2 with half the difference between n and n+1
    n_plus_2 = last_price + (n_plus_1 - last_price) / 2

    # calc n+3 as 1/4th the difference between n+1 and n+2, as in request
    n_plus_3 = n_plus_2 + (n_plus_1 - n_plus_2) / 4

    #create data to return
    predicted_dates = [
        last_date + timedelta(days=1),
        last_date + timedelta(days=2),
        last_date + timedelta(days=3)
    ]
    #create a list with 3 predicted data
    predicted_prices = [n_plus_1, n_plus_2, n_plus_3]

    predicted_data = pd.DataFrame({
        'StockID': [last_stock_id] * 3,
        'Date': predicted_dates,
        'Price_of_stocks': predicted_prices
    })

    return predicted_data



# here, this function will iterate over each folder and read each .csv file inside
# it calls the function "choose_random_values"
def process_all_stocks(base_dir):
    # I create a list with 3 elements, so those 3 markets
    markets = ['LSE', 'NASDAQ', 'NYSE']
    all_data = {}

    for market in markets:
        # here take the path for the market folder, corresponding for each market folder
        market_folder = os.path.join(base_dir, market)
        if not os.path.exists(market_folder):
            print(f"Market folder {market_folder} does not exist")
            continue

        # iteration over each file in the each market folder
        for stock_file in os.listdir(market_folder):
            if stock_file.endswith('.csv'):
                stock_path = os.path.join(market_folder, stock_file)
                try:
                    # select the random data points
                    stock_data = choose_random_values(stock_path)
                    all_data[stock_file] = stock_data

                    # prediction of the next 3 data points
                    predicted_data = predict_next_values(stock_data)

                    # here we add the original and predicted data, and created combined_data
                    combined_data = pd.concat([stock_data, predicted_data])

                    # write the combined data to a new CSV file
                    #so one new .csv will be created for each .csv already created
                    output_file_path = os.path.join(base_dir, f"{os.path.splitext(stock_file)[0]}_predicted.csv")
                    combined_data.to_csv(output_file_path, index=False, header=False)

                    print(f"Data for {stock_file} in {market} processed and saved to {output_file_path}")

                except ValueError as e:
                    # take into account the situations where there aren't enough data points
                    print(f"Error processing {stock_file} in {market}: {e}")

    return all_data

if __name__ == "__main__":
    # get the directory where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_stocks(base_dir)