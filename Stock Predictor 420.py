#!/usr/bin/env python
# coding: utf-8

# In[28]:


from datetime import datetime
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import stats
#ask the user to enter info
stock = input("Which stock's return would you like to predict? Enter the ticker here: ")
startingdate = input('Which date would you like to start your prediction with? Use format YYYY-MM-DD: ')
print ("Alrighty, let's do it!")
#get that stock data
data = web.DataReader(stock, data_source='yahoo',start=startingdate,end=datetime.date(datetime.now()))
#visualize closing price
plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(data['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price ($)',fontsize=18)


daily_close = data['Close']

daily_return=np.log(daily_close/daily_close.shift(1))
dailyreturn = []
for i in daily_return:
    dailyreturn.append(i)
dailyreturn1 =[]
for i in daily_return:
    dailyreturn1.append(i)

dailyreturn.pop(0)
dailyreturn1.pop(0)
dailyreturn1.pop(0)
dailyreturn.pop(-1)

slope, intercept, r_value, P_value, std_err = scipy.stats.linregress(dailyreturn,dailyreturn1)
rsquared = r_value**2
print ('The R-Squared is',round(rsquared,4),'.')
print ('This means that about',round(100*rsquared,2),"% of tomorrow's price is explained by yesterday's.")

prediction = intercept + slope*dailyreturn1[-1]

print("Tomorrow's predicted return, from this autocorrelation model, is",round(prediction*100,2),'%')

if prediction > 0:
    print ('Buy it now!')
else:
    print('Sell it now!')
print('Also, just because I am nice, here is a free graph of the stock price for your selected time frame:')





