import justpy as jp
from pandas.core.dtypes.common import classes
import pandas
from datetime import datetime
from pytz import utc

df = pandas.read_csv("files/reviews.csv", parse_dates=["Timestamp"])

#Pravim novu kolonu Day, jer je u pitanju Rating by Day
df["Day"] = df["Timestamp"].dt.date 
average_day = df.groupby(["Day"]).mean()

chart_def = """
{
  chart: {
    type: 'spline',
    inverted: false
  },
  title: {
    text: 'Atmosphere Temperature by Altitude'
  },
  subtitle: {
    text: 'According to the Standard Atmosphere Model'
  },
  xAxis: {
    reversed: false,
    title: {
      enabled: true,
      text: 'Date'
    },
    labels: {
      format: '{value}'
    },
    accessibility: {
      rangeDescription: 'Range: 0 to 80 km.'
    },
    maxPadding: 0.05,
    showLastLabel: true
  },
  yAxis: {
    title: {
      text: 'Average Rating'
    },
    labels: {
      format: '{value}'
    },
    accessibility: {
      rangeDescription: 'Range: -90°C to 20°C.'
    },
    lineWidth: 2
  },
  legend: {
    enabled: false
  },
  tooltip: {
    headerFormat: '<b>{series.name}</b><br/>',
    pointFormat: '{point.x} {point.y}'
  },
  plotOptions: {
    spline: {
      marker: {
        enable: false
      }
    }
  },
  series: [{
    name: 'Average Rating',
    data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
      [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
  }]
}
"""

def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center q-pa-md")
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")
    hc = jp.HighCharts(a=wp, options=chart_def)  #Ova opciona varijabla options jednaka je varijabli koja ima nas string JS kod
    # print(hc.options.title.text)  #hc je tipa recnik i ovako sam pristupio naslovu, sa ovim title.text
    # print(type(hc.options))
    hc.options.title.text = "Average Rating by Day"
    #print(hc.options.series[0].name)  #0, jer je to prva lista, a sa .name pristupamo tome. Moze i ["name"] ovako da se pristupi, isti je rezultat
    # x = [3, 6, 8]
    # y = [4, 7, 9]
    #hc.options.series[0].data = [[3, 4], [6, 7], [8, 9]]  #Ovo izbacuje grafik, ali obrnut. 3 je y, a 4 je x. Da to resim odem u kod string_def i inverted = False

    #Posto ne radi, moramo da napravimo categories za xAxis
    hc.options.xAxis.categories = list(average_day.index)
    #hc.options.series[0].data = list(zip(average_day.index, average_day["Rating"]))  #Stavio sam ga u listu, jer nam to treba, kao lista, a zip je samo zip
    hc.options.series[0].data = list(average_day["Rating"])  #Samo je average_day["Rating"], jer je index uradjen gore

    return wp

jp.justpy(app)  