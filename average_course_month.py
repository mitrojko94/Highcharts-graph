import justpy as jp
from pandas.core.dtypes.common import classes
import pandas
from datetime import datetime
from pytz import utc

df = pandas.read_csv("files/reviews.csv", parse_dates=["Timestamp"])

df["Month"] = df["Timestamp"].dt.strftime("%Y-%m")
average_course_month = df.groupby(["Month", "Course Name"]).mean().unstack()  #Stavljeno je i Course Name, jer radimo average po course name i month


chart_def = """
{
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Average fruit consumption during one week'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: false,
        borderWidth: 1,
        backgroundColor:
            '#FFFFFF'
    },
    xAxis: {
        categories: [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ],
        plotBands: [{ // visualize the weekend
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Fruit units'
        }
    },
    tooltip: {
        shared: true,
        valueSuffix: ' units'
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{
        name: 'John',
        data: [3, 4, 3, 5, 4, 10, 12]
    }, {
        name: 'Jane',
        data: [1, 3, 4, 3, 3, 5, 4]
    }]
}
"""

def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center q-pa-md")
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")
    hc = jp.HighCharts(a=wp, options=chart_def)

    hc.options.xAxis.categories = list(average_course_month.index)  #index, jer su to nasi podaci, datumi, dani

    #Pravimo listu recnika. U recnik stavimo name, data, jer to imamo u kodu iznad. Name je uvek isto, tu stavimo neku varijablu (v1) i stavimo da su nam to imena kolona (average_course_month.columns).
    #Posle stavimo za data da je druga varijabla (v2) i nju trazimo u varijabli v1 (average_course_month[v1])
    hc_data = [{"name": v1, "data": [v2 for v2 in average_course_month[v1]]} for v1 in average_course_month.columns]  
    hc.options.series = hc_data
   
    return wp

jp.justpy(app)