import json
from dateutil import parser

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

for i in data['rates']:
    t3 = parser.parse(i)
    if t3 <= t2 and t3 >= t1:
        dates.append(i)
        price_INR.append(data['rates'][i]['INR'])
        price_GBP.append(data['rates'][i]['GBP'])
        
map_data=list(zip(dates,price_INR,price_GBP))
result = sorted(map_data, key = lambda x: x[0])

dates.clear()
price_INR.clear()
price_GBP.clear()


#split the result
dates, price_INR, price_GBP = zip(*result)

#Plot graph using svg

maximum_price,minimum_price = max(price_INR),min(price_INR)
maximum_price2,minimum_price2 = max(price_GBP),min(price_GBP)

file = open('T3.svg','w')
file.write("<html>\n")
file.write("<body>\n")
file.write('''<svg width="1500" height="1500" xmlns="http://www.w3.org/2000/svg">\n''')
file.write('''<rect width="100%" height="100%" fill="white" />\n''')
file.write("<text x=\"100\" y=\"50\" fill=\"blue\" style=\"font:24px sans-serif\">""INR Exchange rates (Base EUR)"+"</text>\n")
file.write("<text x=\"100\" y=\"550\" fill=\"red\" style=\"font:24px sans-serif\">""GBP Exchange rates (Base EUR)"+"</text>\n")
file.write("<text x=\"100\" y=\"80\" fill=\"green\">"+"Start Date: "+str(t1)[:11]+"</text>\n")
file.write("<text x=\"300\" y=\"80\" fill=\"green\">"+"End Date: "+str(t2)[:11]+"</text>\n")
file.write("<text x=\"100\" y=\"580\" fill=\"green\">"+"Start Date: "+str(t1)[:11]+"</text>\n")
file.write("<text x=\"300\" y=\"580\" fill=\"green\">"+"End Date: "+str(t2)[:11]+"</text>\n")
file.write("<text x=\"100\" y=\"100\" fill=\"green\">"+"Latest Rate of INR: "+ str(latest_rates['rates']['INR']) +"</text>\n")
file.write("<text x=\"100\" y=\"600\" fill=\"green\">"+"Latest Rate of GBP: "+ str(latest_rates['rates']['GBP']) +"</text>\n")
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
    cy = 350 - 150 * (price_INR[i] - minimum_price)/(maximum_price - minimum_price)
    cy2 = 900 - 250 * (price_GBP[i] - minimum_price2) / (maximum_price2 - minimum_price2)
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


