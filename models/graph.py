import imp


import os
from datetime import datetime
from cosmos import Cosmos
from sentiment import Sentiment
from delta import Delta
import plotly.graph_objs as G
import plotly.express as px
import plotly.graph_objects as go

class Graph():
    def __init__(self):
        self.cosmos = Cosmos()

    def get(list, data):
        for i in list:
            if i ==data:
                return data

    def graph(self, symbol: str, output_dir: str):
        sentiment_data = self.cosmos.read(Sentiment)
        delta_data = self.cosmos.read(Delta)

        xAxis = []
        yAxis = []
        yAxisNegative = []

        for i in sentiment_data:
            if 'TSLA' in i.__dict__['tickers']:
                date = datetime.strptime(i.__dict__["date"], "%Y-%m-%dT%H:%M:%SZ")
                if (date.month != 2 or date.year != 2022):
                    continue
                xAxis.append(date.day)
                yAxis.append(i.__dict__["positive"])
                yAxisNegative.append(-(i.__dict__["negative"]))

        lineX = []
        lineY = []

        for i in delta_data:
            if i.__dict__["symbol"] == symbol:
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

        for i in range(1,len(xAxis)):
            if day == xAxis[i]:
                ratio += yAxis[i] + yAxisNegative[i]
            else:
                newX.append(day)
                day = xAxis[i]
                newBars.append(ratio)
                ratio = 0

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=lineX,y=lineY, name="stock price change", mode='markers', marker = dict(color="blue", size=20)))


        fig.add_trace(go.Bar(x=xAxis,y=yAxis,marker_color="yellowgreen", name="positive reviews"))


        fig.add_trace(go.Bar(x=xAxis,y=yAxisNegative,marker_color="tomato", name="negative reviews"))

        fig.add_trace(go.Bar(x=newX, y=newBars, name="difference in pos vs neg reviews"))

        fig.write_html(os.path.join(output_dir, f"{symbol}.html"))





