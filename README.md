# Stock Price Prediction Project

## Overview

This project is designed to process stock price data from multiple markets (LSE, NASDAQ, NYSE), select random sets of 10 consecutive data points, and predict the next 3 values based on a predefined logic. The results are saved into new CSV files for each stock processed.

## Table of Contents

- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Functions Explained](#functions-explained)
- [Prediction Logic](#prediction-logic)
- [Installation & Usage](#installation--usage)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

The folderstructure for this project is as follows:

## How It Works

The script processes stock data in the following steps:

1. **Read CSV Files**: For each market (LSE, NASDAQ, NYSE), the script reads each stock's CSV file.
2. **Select Random 10 Data Points**: It selects a random set of 10 consecutive data points from each file.
3. **Predict Next 3 Values**: Using the defined prediction logic, the script calculates the next three stock price values.
4. **Save Results**: The original 10 data points and the predicted values are combined and saved into a new CSV file with the suffix `_predicted`.

## Functions Explained

### 1. `choose_random_values(file_path)`

This function selects 10 consecutive data points from a stock's historical data.

- **Input**: 
  - `file_path`: Path to the stock's CSV file.
- **Output**: 
  - A DataFrame containing 10 consecutive stock prices sorted by date.
- **Logic**:
  - The function reads the CSV file, sorts the data by date, and selects a random starting point to ensure the selection of 10 consecutive rows.

### 2. `predict_next_values(stock_data)`

This function predicts the next 3 values based on the provided 10 data points.

- **Input**: 
  - `stock_data`: A DataFrame containing 10 stock prices.
- **Output**: 
  - A DataFrame containing the predicted stock prices for the next three dates.
- **Logic**:
  - The 1st predicted value (`n+1`) is set as the 2nd highest price in the given 10 points.
  - The 2nd predicted value (`n+2`) is calculated as half the difference between the last known value (`n`) and `n+1`.
  - The 3rd predicted value (`n+3`) is calculated as a quarter of the difference between `n+1` and `n+2`.

### 3. `process_all_stocks(base_dir)`

This function iterates over each market folder and processes each stock file.

- **Input**: 
  - `base_dir`: The base directory where the market folders and the script are located.
- **Output**: 
  - A dictionary containing the stock data for all processed files.
- **Logic**:
  - The function goes through each market folder, reads all CSV files, and applies the `choose_random_values` and `predict_next_values` functions to generate predictions.
  - The combined data (original + predicted) is saved as a new CSV file for each stock.

## Prediction Logic

The prediction logic is simple and follows these rules:

1. The first predicted (`n+1`) data point is the same as the 2nd highest value present in the 10 selected data points.
2. The second predicted (`n+2`) data point is calculated as:
n+2 = last_price + (n+1 - last_price) / 2
3. The third predicted (`n+3`) data point is calculated as:
n+3 = n+2 + (n+1 -n+2) /4

The new file will be saved in the same directory as the input file with the suffix _predicted. For example, if the input file is TSLA.csv, the output will be TSLA_predicted.csv.



