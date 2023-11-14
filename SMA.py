# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
symbol = 'AAPL'
start_date = '2015-01-01'
end_date = '2022-12-31'
data = yf.download(symbol, start=start_date, end=end_date)

data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['Signal50'] = np.where(data['Close'] > data['SMA_50'], 1, 0)
data['Daily_Return50'] = data['Close'].pct_change()
data['Strategy_Return50'] = data['Daily_Return50'] * data['Signal50'].shift(1)
data['Cumulative_Return50'] = (1 + data['Strategy_Return50']).cumprod()

spy_data = yf.download('SPY', start=start_date, end=end_date)
spy_data['Daily_Return'] = spy_data['Close'].pct_change()
spy_data['Cumulative_Return'] = (1 + spy_data['Daily_Return']).cumprod()

difference = pd.DataFrame()
diff = data['Cumulative_Return50'] - spy_data['Cumulative_Return']
mean_difference = np.mean(diff)
difference = pd.DataFrame({'Mean_Difference': [mean_difference]})
difference = difference.rename(index={difference.index[0]: 'SMA_50'})

data['SMA_100'] = data['Close'].rolling(window=100).mean()
data['Signal100'] = np.where(data['Close'] > data['SMA_100'], 1, 0)
data['Daily_Return100'] = data['Close'].pct_change()
data['Strategy_Return100'] = data['Daily_Return100'] * data['Signal100'].shift(1)
data['Cumulative_Return100'] = (1 + data['Strategy_Return100']).cumprod()
diff = data['Cumulative_Return100'] - spy_data['Cumulative_Return']
mean_difference = np.mean(diff)
new_row = pd.DataFrame({'Mean_Difference': [mean_difference]}, index=['SMA_100'])
difference = difference._append(new_row)

data['SMA_10'] = data['Close'].rolling(window=10).mean()
data['Signal10'] = np.where(data['Close'] > data['SMA_10'], 1, 0)
data['Daily_Return10'] = data['Close'].pct_change()
data['Strategy_Return10'] = data['Daily_Return10'] * data['Signal10'].shift(1)
data['Cumulative_Return10'] = (1 + data['Strategy_Return10']).cumprod()
diff = data['Cumulative_Return10'] - spy_data['Cumulative_Return']
mean_difference = np.mean(diff)
new_row = pd.DataFrame({'Mean_Difference': [mean_difference]}, index=['SMA_10'])
difference = difference._append(new_row)


# Calculate the returns for the stock and SPY
max_mean_difference = -np.inf
optimal_period = None

# Iterate through different moving average periods and calculate mean difference
for period in range(1, 101):
    # Calculate the moving average for the stock returns
    data['Moving_Average'] = data['Close'].rolling(window=period).mean()
    data['Signal'] = np.where(data['Close'] > data['Moving_Average'], 1, 0)
    data['Daily_Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Daily_Return'] * data['Signal'].shift(1)
    data['Cumulative_Return'] = (1 + data['Strategy_Return']).cumprod()
    diff = data['Cumulative_Return'] - spy_data['Cumulative_Return']
    mean_difference = np.mean(diff)

    # Check if this period provides a higher mean difference
    if mean_difference > max_mean_difference:
        max_mean_difference = mean_difference
        optimal_period = period


print(difference)

# Print the optimal period and the corresponding mean difference
print("Optimal Period:", optimal_period)
print("Maximum Mean Difference:", max_mean_difference)



plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Cumulative_Return50'], label='SMA Strategy')
plt.plot(spy_data.index, spy_data['Cumulative_Return'], label='SPY')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.show()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
