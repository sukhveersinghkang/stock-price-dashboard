import pandas as pd 
from openbb import obb 
import matplotlib.pyplot as plt 
import seaborn as sns 


stock_data = obb.equity.price.historical(symbol='TSLA', start_date='2023-01-01').to_df()
print(stock_data)
sns.lineplot(x  = 'date', 
             y =  'high', 
             data = stock_data )
plt.show()