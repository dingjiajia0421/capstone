# -*- coding: utf-8 -*-
"""Statistical Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dmgY4XGZrUjMLqVQfF9pxN88wxA-tfQ5
"""

import numpy as np
from math import log, factorial
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def log_likelihood(X, lambd):
  sum = 0
  for x in X:
    sum += x*log(lambd) - lambd - log(factorial(x))
  return sum

def MDD(X, w, delta, alpha):
  id = 0
  change_points = []
  i = 0
  Q = X[id:id+w]
  lambda_hat = np.mean(Q) # lambda_1
  while id + w + i < len(X):
    x_next = X[id + w + i]
    p_lambda = (1 - alpha) * lambda_hat + alpha * x_next # lambda_2
    L1 = log_likelihood(np.append(Q, [x_next]), lambda_hat)
    #print(L1)
    L2 = log_likelihood(np.append(Q, [x_next]), p_lambda)
    #print(L2)
    if L2 < L1 - delta:
      change_points.append(id+w+i)
      id = id+w+i
      i = 0
      Q = X[id:id+w]
    else:
      np.append(Q,[x_next])
      i += 1
    lambda_hat = np.mean(Q)
  return change_points

stocks = pd.read_csv('/content/sp_400_midcap.csv')
stocks['GICS Sector'].unique()

"""# Materials"""

from os import renames
# Mid-cap 400 Index Test Case: Materials Sector
stocks = pd.read_csv('/content/sp_400_midcap.csv')
new_columns = []
for i in range(stocks.shape[0]):
  if stocks.iloc[i, 2] == 'Materials':
    new_column = yf.download(stocks.iloc[i, 0], start = '2019-09-26', end = '2024-09-01').loc[:,'Volume']
    new_columns.append(new_column)
vol_dataframe = pd.concat(new_columns, axis=1)

vol_dataframe

vol_dataframe_copy = vol_dataframe.fillna(0)
avg_vol = np.average(vol_dataframe_copy, axis = 1)

ret = pd.read_csv('/content/mid_cap_all_sectors_ret.csv')[['date', 'Materials']]
df = ret.loc[ret['date'] >= '2019-09-26']
df.reset_index(drop = True, inplace = True)

# Data Visualization
df['date'] = pd.to_datetime(df['date'])
data = pd.DataFrame({'date': df['date'].values,
                     'returns':df['Materials'].values,
                     'volume': avg_vol})

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue', label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

avg = (avg_vol/100000).astype(int)
#avg
index = MDD(avg, w=22, delta=50, alpha=0.8)

len(index)

#
highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results = pd.DataFrame({"date": data['date']})
total_results['Materials'] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Industrials"""

def get_vol(sector):
  new_columns = []
  for i in range(stocks.shape[0]):
    if stocks.iloc[i, 2] == sector:
      new_column = yf.download(stocks.iloc[i, 0], start = '2019-09-26', end = '2024-09-01').loc[:,'Volume']
      new_columns.append(new_column)
  return pd.concat(new_columns, axis=1)

def calculate_vol_avg(vol_dataframe):
  vol_dataframe_copy = vol_dataframe.fillna(0)
  vol_dataframe_copy = vol_dataframe.fillna(0)
  return np.average(vol_dataframe_copy, axis = 1)

vol_dataframe = get_vol('Industrials')
avg_vol = calculate_vol_avg(vol_dataframe)

def retrive_data(sector):
  ret = pd.read_csv('/content/mid_cap_all_sectors_ret.csv')[['date', sector]]
  df = ret.loc[ret['date'] >= '2019-09-26']
  df.reset_index(drop = True, inplace = True)
  return df

def visualization(df, sector, avg_vol):
  # Data Visualization
  df['date'] = pd.to_datetime(df['date'])
  data = pd.DataFrame({'date': df['date'].values,
                      'returns':df[sector].values,
                      'volume': avg_vol})

  # Create a figure and a set of subplots
  fig, ax1 = plt.subplots(figsize=(12, 6))

  # Plotting the stock returns
  ax1.set_xlabel('Date')
  ax1.set_ylabel('Stock Returns', color='tab:blue')
  ax1.plot(data['date'], data['returns'], color='tab:blue', label='Stock Returns')
  ax1.tick_params(axis='y', labelcolor='tab:blue')

  # Creating a second y-axis for trading volume
  ax2 = ax1.twinx()
  ax2.set_ylabel('Trading Volume', color='tab:orange')
  ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
  ax2.tick_params(axis='y', labelcolor='tab:orange')

  # Adding a title and grid
  plt.title('Stock Returns and Trading Volume Over Time')
  ax1.grid()

  # Show the plot
  plt.show()
  return data

df = retrive_data('Industrials')
data = visualization(df, 'Industrials',avg_vol)

avg = (avg_vol/10000).astype(int)
#avg
index = MDD(avg, w=10, delta=40, alpha=0.9)

len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results['Industrials'] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Health Care"""

vol_dataframe = get_vol('Health Care')
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data('Health Care')
data = visualization(df, 'Health Care',avg_vol)

avg = (avg_vol/100000).astype(int)
index = MDD(avg, w=10, delta= 10, alpha=0.9)
len(index)

#avg = (avg_vol/100000).astype(int)
#index = MDD(avg, w=22, delta= 50, alpha=0.7)


highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results['Health Care'] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Real Estate"""

vol_dataframe = get_vol('Real Estate')
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data('Real Estate')
data = visualization(df, 'Real Estate',avg_vol)

avg = (avg_vol/100000).astype(int)
index = MDD(avg, w=10, delta= 10, alpha=0.9)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results['Real Estate'] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Consumer Discretionary"""

sector = 'Consumer Discretionary'
vol_dataframe = get_vol(sector)
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data(sector)
data = visualization(df, sector, avg_vol)

avg = (avg_vol/10000).astype(int)
index = MDD(avg, w= 5, delta= 10, alpha=0.9)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results[sector] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Financials"""

sector = 'Financials'
vol_dataframe = get_vol(sector)
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data(sector)
data = visualization(df, sector, avg_vol)

avg = (avg_vol/10000).astype(int)
index = MDD(avg, w= 10, delta= 50, alpha=0.9)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results[sector] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Utilities"""

sector = 'Utilities'
vol_dataframe = get_vol(sector)
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data(sector)
data = visualization(df, sector, avg_vol)

avg = (avg_vol/10000).astype(int)
index = MDD(avg, w= 10, delta= 30, alpha=0.9)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results[sector] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Information Technology"""

sector = 'Information Technology'
vol_dataframe = get_vol(sector)
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data(sector)
data = visualization(df, sector, avg_vol)

avg = (avg_vol/10000).astype(int)
index = MDD(avg, w= 5, delta= 25, alpha=0.8)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results[sector] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Energy"""

sector = 'Energy'
vol_dataframe = get_vol(sector)
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data(sector)
data = visualization(df, sector, avg_vol)

avg = (avg_vol/10000).astype(int)
index = MDD(avg, w= 22, delta= 20, alpha=0.8)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results[sector] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

"""# Consumer Staples"""

sector = 'Consumer Staples'
vol_dataframe = get_vol(sector)
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data(sector)
data = visualization(df, sector, avg_vol)

avg = (avg_vol/100000).astype(int)
index = MDD(avg, w= 10, delta= 10, alpha=0.8)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results[sector] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

total_results.loc[total_results['Consumer Staples'] == 1]

"""# Communication Services"""

sector = 'Communication Services'
vol_dataframe = get_vol(sector)
avg_vol = calculate_vol_avg(vol_dataframe)

df = retrive_data(sector)
data = visualization(df, sector, avg_vol)

avg = (avg_vol/100000).astype(int)
index = MDD(avg, w= 10, delta= 10, alpha=0.8)
len(index)

highlight_dates = data.iloc[index]['date']
highlight_returns = data.iloc[index]['returns']
# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plotting the stock returns
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Returns', color='tab:blue')
ax1.plot(data['date'], data['returns'], color='tab:blue',alpha=0.7, label='Stock Returns')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Creating a second y-axis for trading volume
ax2 = ax1.twinx()
ax2.set_ylabel('Trading Volume', color='tab:orange')
ax2.bar(data['date'], data['volume'], color='tab:orange', alpha=0.3, label='Trading Volume')
ax2.tick_params(axis='y', labelcolor='tab:orange')

ax1.scatter(highlight_dates, highlight_returns,
            color='red', s=10, label='Highlighted Returns', edgecolor='black')
# Adding a title and grid
plt.title('Stock Returns and Trading Volume Over Time')
ax1.grid()

# Show the plot
plt.show()

total_results[sector] = total_results['date'].apply(lambda x: 1 if x in highlight_dates.values else 0)

total_results.shape

total_results.loc[:,'Materials':].sum()

total_results.to_csv('total_results.csv', index = False)