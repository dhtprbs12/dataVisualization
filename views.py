from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

import os
path = '/Users/sekyunoh/Desktop/Python Tutorial/data_visualization_project/data_visualization_app/'

# to use html files in templates folder, we need to let the django know about the templates dir
def mainView(request):

    # countries
    countiesData = pd.read_csv(path+'countries.csv')
    us = countiesData[countiesData.country == 'United States']
    china = countiesData[countiesData.country == 'China']
    korea = countiesData[countiesData.country == 'Korea, Rep.']
    plt.figure()# like creating new instance
    plt.plot(us.year, us.population / us.population.iloc[0] * 100)
    plt.plot(china.year, china.population / china.population.iloc[0] * 100)
    plt.plot(korea.year, korea.population / korea.population.iloc[0] * 100)
    plt.title("Population Rate")
    plt.legend(['United States', 'China', 'S.Korea'])
    plt.xlabel('year')
    plt.ylabel('population growth (first year = 100)')
    # check if file already exists, if not, save image
    if not os.path.isfile(path + 'static/img/pop_graph.png'):
        plt.savefig(path + 'static/img/pop_graph.png')

    # currency
    currencyData = pd.read_csv(path+'currency.csv')
    substr = '2000'
    year = []
    avg = []
    count = 0
    sum = 0
    # iterate all data and calculate year and its average
    for i in range(len(currencyData)):
        date = currencyData.iloc[i][0]
        value = currencyData.iloc[i][1]
        if value == '.':
            value = 0
            count -= 1
        if substr != date[:4]:
            year.append(substr)
            avg.append(round(sum / count))
            substr = date[:4]
            count = 0
            sum = 0
        # sum up every year's value
        sum = sum + float(value)
        count += 1

    # append last year sum and average
    year.append(substr)
    avg.append(round(sum / count))

    plt.figure()# like creating new instance
    plt.title("Exchange Rate")
    plt.plot(year, avg, color="red")
    plt.legend(['Average $1 = ' + calculateAvgRate(avg) + ' won'])
    plt.xticks(rotation=-90)
    plt.xlabel('year')
    plt.ylabel('S.Korea Won to 1 U.S.Dollar')
    # check if file already exists, if not, save image
    # create graph that exchanges rate between two coutries
    if not os.path.isfile(path + 'static/img/currency_graph.png'):
        plt.savefig(path + 'static/img/currency_graph.png')
    return render(request, 'main.html')

def calculateAvgRate(averageArr):
    sum = 0
    for value in averageArr:
        sum = sum + value
    return format((sum / len(averageArr)),'.2f')

#animation functions
def init_animation():
    global line
    line, = ax.plot(x, np.zeros_like(x))
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1,1)

def animate(i):
    line.set_ydata(np.sin(2*np.pi*i / 50)*np.sin(x))
    return line,

fig = plt.figure()
ax = fig.add_subplot(111)
x = np.linspace(0, 2*np.pi, 200)

if not os.path.isfile(path + 'static/img/animation.gif'):
    ani = matplotlib.animation.FuncAnimation(fig, animate, init_func=init_animation, frames=50)
    ani.save(path+'static/img/animation.gif', writer='imagemagick', fps=30)

def animate(i):
    graphData = open(path+'example.txt','r').read()
    dataArray = graphData.split('\n')
    xs = []
    ys = []
    for line in dataArray:
        if len(line) > 1: # to handle empty line ignored
            x, y = line.split(',') # this makes two variables
            xs.append(int(x))
            ys.append(int(y))
    ax1.clear() # to clear previous data to redraw with new data
    ax1.plot(xs,ys)
# if there is no gif file
if not os.path.isfile(path + 'static/img/animation.gif'):
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    ani.save(path+'static/img/animation.gif', writer='imagemagick', fps=30)
