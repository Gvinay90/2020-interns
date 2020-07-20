import json
from dateutil import parser

#load the data.json file
with open('data.json') as file:
    data = json.load(file)

#Date range to plot Graph
t1 = parser.parse('2019-01-01')
t2 = parser.parse('2019-01-31')

dates = []
price = []

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

maximum_price,minimum_price = max(price),min(price)

file = open('T1.svg','w')
file.write("<html>\n")
file.write("<body>\n")
file.write('''<svg width="1500" height="1500" xmlns="http://www.w3.org/2000/svg">\n''')
file.write('''<rect width="100%" height="100%" fill="white" />\n''')
file.write("<text x=\"100\" y=\"50\" fill=\"blue\" style=\"font:24px sans-serif\">""INR Exchange rates (Base EUR)"+"</text>\n")
file.write("<text x=\"100\" y=\"80\" fill=\"green\">"+"Start Date: "+str(t1)[:11]+"</text>\n")
file.write("<text x=\"300\" y=\"80\" fill=\"green\">"+"End Date: "+str(t2)[:11]+"</text>\n")
file.write("<text x=\"20\" y=\"350\" fill=\"blue\">"+ str(minimum_price) +"</text>\n")
file.write('''<text x=\"20\" y="''' + str(350 - 150 * (maximum_price - minimum_price) / (maximum_price - minimum_price))+''' " fill=\"blue\">'''+ str(maximum_price) +'''</text>\n''')
#For plotting line between two points store x and y
x=[] 
y=[]
for i in range(len(price)):
    cx = 100 + i * 15 
    cy = 350 - 150 * (price[i] - minimum_price)/(maximum_price - minimum_price)
    x.append(cx)
    y.append(cy)
    file.write('''<circle cx=''' + '''"'''+str(cx)+'''"''' + ''' cy=''' + '''"'''+str(cy) + '''"''' + ''' r="3"/> ''')
    file.write("<text x=\"" + str(cx-5) + "\" y=\"400\" fill=\"blue\" style=\"font: 12px sans-serif;\" transform=\"rotate(90," + str(cx-5) + ",400)\">" + dates[i] + "</text>\n")

for i in range(len(x)-1):
    file.write("<line x1=\"" + str(x[i]) + "\" y1=\"" + str(y[i]) + "\" x2=\"" + str(x[i+1]) + "\" y2=\"" + str(y[i+1]) + "\" stroke=\"" + str("blue") + "\" />\n")

file.write("</svg>\n")
file.write("</body>\n")
file.write("</html>\n")
file.close()
