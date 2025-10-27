import pandas as pd 
from openbb import obb 
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np
sns.set_theme(style='darkgrid')



ticker =  input("Enter a stock ticker:").upper().strip()
print(f"\nFetching data for {ticker}")

stock_data = obb.equity.price.stock_dataorical(symbol='{ticker}', start_date='2023-01-01', interval ="1d")
if stock_data is None or len(stock_data) == 0:
        raise ValueError(f"no data found for {ticker}")
stock_data['date'] = pd.to_datetime(stock_data['date'])
stock_data = stock_data.set_index('date').sort_index()
stock_data['return'] = stock_data['close'].pct_change()

tot_return = (stock_data['close'].iloc[-1]/ stock_data['close'].iloc[0] -1 )*100
daily_vol = stock_data['return'].std() * np.sqrt(252)*100

roll_max = stock_data['close'].cummax()
drawdown = stock_data['close']/ roll_max -1 

max_dd = drawdown.min()*100

stock_data['sma20'] = stock_data['close'].rolling(20).mean()
stock_data['sma50'] = stock_data['close'].rolling(50).mean()

plt.figure(figsize=(10, 5))
sns.lineplot(data=stock_data, x=stock_data.index, y="close", label="Close", linewidth=1.8)
sns.lineplot(data=stock_data, x=stock_data.index, y="sma20", label="SMA20", linewidth=1.2)
sns.lineplot(data=stock_data, x=stock_data.index, y="sma50", label="SMA50", linewidth=1.2)
plt.title(f"{ticker} Price Chart with Moving Averages", fontsize=13)
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.tight_layout()
plt.show()

  
plt.figure(figsize=(10, 3))
sns.barplot(x=stock_data.index, y="volume", data=stock_data, color="steelblue")
plt.title(f"{ticker} Trading Volume", fontsize=12)
plt.xlabel("Date")
plt.ylabel("Volume")
plt.tight_layout()
plt.show()


plt.figure(figsize=(8, 4))

sns.stock_dataplot(stock_data["return"].dropna(), bins=40, kde=True, color="teal")
plt.title(f"{ticker} Daily Returns Distribution", fontsize=12)
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

