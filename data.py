import requests, tweet
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import dateutil.parser
#get data from treasury
r = requests.get('https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData')

root = ET.fromstring(r.text)

data = {}
dates = []
diffs = []
#compile nessecary data
for n in range(-1, -32, -1):
    entry = root.findall('{http://www.w3.org/2005/Atom}entry')[n]
    content = entry.find('{http://www.w3.org/2005/Atom}content')
    props = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
    date = props.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}NEW_DATE')
    twoyr = props.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_2YEAR')
    tenyr = props.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}BC_10YEAR')

    if date.text != None and twoyr.text != None and tenyr.text != None:
        date_f = date.text.split("T")[0]
        if n == -1:
            data["latest"] = {"date": date_f, "twoyr": twoyr.text, "tenyr": tenyr.text}
        elif n == -6:
            data["week"] = {"date": date_f, "twoyr": twoyr.text, "tenyr": tenyr.text}
        date_g = dateutil.parser.parse(date.text)
        dates.append(str(date_g.month) + '/' + str(date_g.day))
        diffs.append(float(tenyr.text) - float(twoyr.text))

#graph
fig, ax = plt.subplots()
dates.reverse()
diffs.reverse()
ax.plot(dates, diffs)
start, end = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(0, end, 5))
plt.grid(True)
plt.xlabel('Day')
plt.ylabel('Spread')
plt.title('Ten Year - Two Year Spread')
plt.savefig('fig1.png')

tweet.send(data)

print(data)
