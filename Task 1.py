import json
from dateutil import parser
import matplotlib.pyplot as plt 

#load the data.json file
with open('data.json') as file:
    data = json.load(file)

#Date range to plot Graph    
t1=parser.parse('2019-01-01')
t2=parser.parse('2019-01-31')


dates=[]
price=[]

for i in data['rates']:
    t3 = parser.parse(i)
    if t3 <= t2 and t3 >= t1:
        dates.append(i)
        price.append(data['rates'][i]['INR'])
        
map_data=list(zip(dates,price))
result = sorted(map_data, key = lambda x: x[0])

dates=[]
price=[]

#split the result
dates,price = zip(*result)

#Plot Graph
plt.plot(dates,price)
plt.xlabel('Dates in Jan 2019')
plt.xticks(rotation=30)
plt.ylabel('Rates of Jan 2019')
plt.title('Exchange rate against EUR')
plt.show()
