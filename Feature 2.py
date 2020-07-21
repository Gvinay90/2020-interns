import json
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

for i in data['rates']:
    dates.append(i)
    price1.append(data['rates'][i][symbol1])
    price2.append(data['rates'][i][symbol2])
    
map_data=list(zip(dates,price1,price2))
result = sorted(map_data, key = lambda x: x[0])

dates.clear()
price1.clear()
price2.clear()


#split the result
dates, price1, price2 = zip(*result)

maximum_price,minimum_price = max(price1),min(price1)
maximum_price2,minimum_price2 = max(price2),min(price2)

file = open('F2.svg','w')
file.write("<html>\n")
file.write("<body>\n")
file.write('''<svg width="1500" height="1500" xmlns="http://www.w3.org/2000/svg">\n''')
file.write('''<rect width="100%" height="100%" fill="white" />\n''')
file.write("<text x=\"100\" y=\"50\" fill=\"blue\" style=\"font:24px sans-serif\">"""+ symbol1 +" Exchange rates (Base EUR)"+"</text>\n")
file.write("<text x=\"100\" y=\"550\" fill=\"red\" style=\"font:24px sans-serif\">"""+ symbol2 +" Exchange rates (Base EUR)"+"</text>\n")
file.write("<text x=\"100\" y=\"80\" fill=\"green\">"+"Start Date: "+ start_date +"</text>\n")
file.write("<text x=\"300\" y=\"80\" fill=\"green\">"+"End Date: "+ end_date +"</text>\n")
file.write("<text x=\"100\" y=\"580\" fill=\"green\">"+"Start Date: "+ start_date +"</text>\n")
file.write("<text x=\"300\" y=\"580\" fill=\"green\">"+"End Date: "+ end_date +"</text>\n")
file.write("<text x=\"100\" y=\"100\" fill=\"green\">"+"Latest Rate of "+ symbol1 +": "+ str(latest_rates['rates'][symbol1]) +"</text>\n")
file.write("<text x=\"100\" y=\"600\" fill=\"green\">"+"Latest Rate of "+ symbol2 +": "+ str(latest_rates['rates'][symbol2]) +"</text>\n")
file.write("<text x=\"20\" y=\"350\" fill=\"blue\">"+ str(minimum_price) +"</text>\n")
file.write('''<text x=\"20\" y="''' + str(350 - 150 * (maximum_price - minimum_price) / (maximum_price - minimum_price))+''' " fill=\"blue\">'''+ str(maximum_price) +'''</text>\n''')
file.write("<text x=\"20\" y=\"900\" fill=\"red\">"+ str(minimum_price2) +"</text>\n")
file.write('''<text x=\"20\" y="''' + str(900 - 250 * (maximum_price2 - minimum_price2) / (maximum_price2 - minimum_price2))+''' " fill=\"red\">'''+ str(maximum_price2) +'''</text>\n''')

#For plotting line between two points store x and y
x=[] 
y=[]
y1=[]

for i in range(len(dates)):
    cx = 100 + i * 15 
    cy = 350 - 150 * (price1[i] - minimum_price)/(maximum_price - minimum_price)
    cy2 = 900 - 250 * (price2[i] - minimum_price2) / (maximum_price2 - minimum_price2)
    x.append(cx)
    y.append(cy)
    y1.append(cy2)
    #plot for 1st currency
    file.write('''<circle cx=''' + '''"'''+str(cx)+'''"''' + ''' cy=''' + '''"'''+str(cy) + '''"''' + ''' r="3"/> ''')
    file.write("<text x=\"" + str(cx-5) + "\" y=\"400\" fill=\"blue\" style=\"font: 12px sans-serif;\" transform=\"rotate(90," + str(cx-5) + ",400)\">" + dates[i] + "</text>\n")

    #plot for 2nd currency
    file.write('''<circle cx=''' + '''"'''+str(cx)+'''"''' + ''' cy=''' + '''"'''+str(cy2) + '''"''' + ''' r="3"/> ''')
    file.write("<text x=\"" + str(cx-5) + "\" y=\"950\" fill=\"red\" style=\"font: 12px sans-serif;\" transform=\"rotate(90," + str(cx-5) + ",950)\">" + dates[i] + "</text>\n")

for i in range(len(x)-1):
    file.write("<line x1=\"" + str(x[i]) + "\" y1=\"" + str(y[i]) + "\" x2=\"" + str(x[i+1]) + "\" y2=\"" + str(y[i+1]) + "\" stroke=\"" + str("blue") + "\" />\n")
    file.write("<line x1=\"" + str(x[i]) + "\" y1=\"" + str(y1[i]) + "\" x2=\"" + str(x[i+1]) + "\" y2=\"" + str(y1[i+1]) + "\" stroke=\"" + str("red") + "\" />\n")

file.write("</svg>\n")
file.write("</body>\n")
file.write("</html>\n")
file.close()
