from datetime import datetime
from cosmos import Cosmos
from sentiment import Sentiment
from delta import Delta
import plotly.graph_objs as G
import plotly.express as px
import plotly.graph_objects as go

fig = go.Figure()

cosmos = Cosmos()

data1 = cosmos.read(Sentiment)
data2 = cosmos.read(Delta)

xAxis = []
yAxis = []
yAxisNegative = []

for i in data1:
    if 'TSLA' in i.__dict__['tickers']:
        date = datetime.strptime(i.__dict__["date"], "%Y-%m-%dT%H:%M:%SZ")
        if (date.month != 2 or date.year != 2022):
            continue
        xAxis.append(date.day)
        yAxis.append(i.__dict__["positive"])
        yAxisNegative.append(-(i.__dict__["negative"]))

lineX = []
lineY = []

def get(list, data):
    for i in list:
        if i ==data:
            return data

for i in data2:
    if i.__dict__["symbol"] == 'TSLA':
        date = datetime.strptime(i.__dict__["date"], "%Y-%m-%dT%H:%M:%SZ")
        if (date.month != 2 or date.year != 2022):
            continue
        if lineX.__contains__(date.day):
            continue
        lineX.append(date.day)
        lineY.append((float(i.__dict__['delta'])-1)*50)



day = xAxis[0]
ratio = yAxis[0]+yAxisNegative[0]

newBars = []
newX = []

# for i in range(1,len(xAxis)):
#     if xAxis[i] == 19:
#         ratio += yAxis[i] + yAxisNegative[i]

# newBars.append(ratio)

# fig.add_trace(go.Bar(x=[19], y=newBars))

for i in range(1,len(xAxis)):
    if day == xAxis[i]:
        ratio += yAxis[i] + yAxisNegative[i]
    else:
        newX.append(day)
        day = xAxis[i]
        newBars.append(ratio)
        ratio = 0


fig.add_trace(go.Scatter(x=lineX,y=lineY, name="stock price change", mode='markers', marker = dict(color="blue", size=20)))


fig.add_trace(go.Bar(x=xAxis,y=yAxis,marker_color="yellowgreen", name="positive reviews"))


fig.add_trace(go.Bar(x=xAxis,y=yAxisNegative,marker_color="tomato", name="negative reviews"))

fig.add_trace(go.Bar(x=newX, y=newBars, name="difference in pos vs neg reviews"))

# for i in list:
#     fig.add_trace(go.Bar(x=xAxis,y=yAxisNegative,marker_color=i))

fig.show()





