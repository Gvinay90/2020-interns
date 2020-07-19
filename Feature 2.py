import json
import matplotlib.pyplot as plt
import requests

start_date = input('Enter start date format yyyy-mm-dd ex- 2019-01-01\n')
end_date = input('Enter the end date format yyyy-mm-dd ex- 2019-01-01\n')

symbol1 = input('First symbol ex-INR\n')
symbol2 = input('Second symbol ex-INR\n')

#urls to make request
url='https://api.exchangeratesapi.io/history?start_at={0}&end_at={1}&symbols={2},{3}'.format(start_date,end_date,symbol1,symbol2)
url2='https://api.exchangeratesapi.io/latest?symbols={},{}'.format(symbol1,symbol2)

#load the  data form api
response = requests.get(url)
file = response.text
data = json.loads(file)

#load the latest rates from api
response2 = requests.get(url2)
f = response2.text
latest_rates = json.loads(f)

dates=[]
price1 = []
price2 = []

x_coord=0 #for x-axis distance
for i in data['rates']:
    dates.append(i)
    price1.append(data['rates'][i][symbol1])
    price2.append(data['rates'][i][symbol2])
    x_coord += 1
        
map_data=list(zip(dates,price1,price2))
result = sorted(map_data, key = lambda x: x[0])

dates.clear()
price1.clear()
price2.clear()


#split the result
dates, price1, price2 = zip(*result)

#for y-axis of text
a=max(price1)
b=max(price2)
y_coord=max(a,b)

#Plot Graph
plt.plot(dates,price1, label=symbol1)
plt.plot(dates,price2, label=symbol2)

plt.annotate(symbol1 +' curr_rate-'+str(latest_rates['rates'][symbol1]),
             (x_coord-5,y_coord),
             textcoords='offset points',
             xytext=(0,40),ha='center')
plt.annotate(symbol2 +' curr_rate-'+str(latest_rates['rates'][symbol2]),
             (x_coord-5,y_coord),
             textcoords='offset points',
             xytext=(0,30),ha='center')

plt.xlabel('Dates in Jan 2019')
plt.xticks(rotation=30)
plt.ylabel('Rates of Jan 2019')
plt.title('Exchange rate against EUR')
plt.legend()
plt.show()
