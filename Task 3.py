import json
from dateutil import parser
import matplotlib.pyplot as plt 

#load the data.json file
with open('data.json') as file:
    data = json.load(file)

#load the latest-rates.json file
with open('latest-rates.json') as f:
    latest_rates = json.load(f)

#Date range to plot Graph    
t1=parser.parse('2019-01-01')
t2=parser.parse('2019-01-31')


dates=[]
price_INR = []
price_GBP = []

x_coord=0 #for x-axis distance
for i in data['rates']:
    t3 = parser.parse(i)
    if t3 <= t2 and t3 >= t1:
        dates.append(i)
        price_INR.append(data['rates'][i]['INR'])
        price_GBP.append(data['rates'][i]['GBP'])
        x_coord += 1
        
map_data=list(zip(dates,price_INR,price_GBP))
result = sorted(map_data, key = lambda x: x[0])

dates.clear()
price_INR.clear()
price_GBP.clear()


#split the result
dates, price_INR, price_GBP = zip(*result)

#for y-axis of text
a=max(price_INR)
b=max(price_GBP)
y_coord=max(a,b)

#Plot Graph
plt.plot(dates,price_INR, label='INR')
plt.plot(dates,price_GBP, label='GBP')

plt.annotate('INR curr_rate-'+str(latest_rates['rates']['INR']),
             (x_coord-5,y_coord),
             textcoords='offset points',
             xytext=(0,40),ha='center')

plt.annotate('GBP curr_rate-'+str(latest_rates['rates']['GBP']),
             (x_coord-5,y_coord),
             textcoords='offset points',
             xytext=(0,30),ha='center')

plt.xlabel('Dates in Jan 2019')
plt.xticks(rotation=30)
plt.ylabel('Rates of Jan 2019')
plt.title('Exchange rate against EUR')
plt.legend()
plt.show()
