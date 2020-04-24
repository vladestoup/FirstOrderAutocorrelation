'''
READ THIS FIRST: 

This model was created by Vlad Estoup (B.Comm., Finance, Sauder School of Business at UBC). It is Intellectual Property of the 
creator and cannot be distributed or copied without his direct consent. It is protected by Canadian and US Copyright law. 
Any unauthorized distribution or copy of the code will be prosecuted to the full extent of local laws. 

This code was originally developed for trading MSFT and AAPL stocks, but is a good tool for uncovering short-term momentum 
patterns in any asset, from any particular stock exchange. For Canadian Securities, add '.TO' at the end of the ticker name.
'stats' from scipy sometimes is not necessary, but keep it just in case, otherwise there may be issues in some environments.
This model's formula is: (return tomorrow) = alpha + beta x (return today) + error
It pulls data from any date until today, and gives you tomorrow's expected return based on past returns. It can be adapted
to include multiple degrees of autocorrelation, but for these particular stocks, one day produces the highest predictive power.
It works great for tech stocks like MSFT, AAPL, IBM, with up to 43% explanatory power (super high! Most models are around 10%).
Does not work very well with volatile assets, commodities and unicorn tech stocks (i.e. SHOP).
The higher the R-Squared, the better the prediction. 
'''

from datetime import datetime
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import stats

#Ask the user to enter stock information:

stock = input("Which stock's return would you like to predict? Enter the ticker here: ")
startingdate = input('Which date would you like to start your prediction with? Use format YYYY-MM-DD: ')
print ("Alrighty, let's do it!")

#Get the stock's data:

data = web.DataReader(stock, data_source='yahoo',start=startingdate,end=datetime.date(datetime.now()))

#Visualize closing price, nice add-on for the user:

plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(data['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price ($)',fontsize=18)

#Calulate returns for the asset, since they are not provided by the server:

daily_close = data['Close']

#You can use 'Adj Close' too, but I am using this for daytrading purposes so 'Close' is better.
#Use logarithmic returns to smoothen the data a little bit (math lovers will understand).
#Daily_return is a list of all returns for the stock between the selected date and today:

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

#dailyreturn is now a list of returns at time t, the INDEPENDENT variable
#dailyreturn1 is now a list of returns at time t+1, the DEPENDENT variable
#Now it's time to regress returns at time (t+1) on returns at time (t):

slope, intercept, r_value, P_value, std_err = scipy.stats.linregress(dailyreturn,dailyreturn1)
rsquared = r_value**2
print ('The R-Squared is',round(rsquared,4),'.')
print ('This means that about',round(100*rsquared,2),"% of tomorrow's price is explained by yesterday's.")

#Now that we have our model, we can apply it: 

prediction = intercept + slope*dailyreturn1[-1]

print("Tomorrow's predicted return, from this autocorrelation model, is",round(prediction*100,2),'%')

#And, of course, we must add some sort of recommendation: 

if prediction > 0:
    print ('Buy it now!')
else:
    print('Sell it now!')

#Let them know we're hooking them up with a graph:

print('Also, just because I am nice, here is a free graph of the stock price for your selected time frame:')

#That's it!!



