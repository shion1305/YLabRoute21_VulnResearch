# libraries
import datetime
import os

import matplotlib.pyplot as plt
import squarify  # pip install squarify (algorithm for treemap)
import pandas as pd
import numpy as np
from pathlib import Path
from FormatStandizer import *


def visualizeTimeData(records, starting, ending, period=7 * 24 * 60 * 60, title='', loc='', x_axis='day'):
    # それぞれのsecondsをlongで出す
    # timestampがlocaltimeなのかわからなかったけれど無修正で処理することに
    result = []
    for i in range(int((ending - starting) / period) + 1):
        result.append([])
    for record in records:
        p_time = pd.to_datetime(record['_source']['@timestamp']).timestamp()
        p = int((p_time - starting) / period)
        # while len(result) <= p:
        #     result.append([])
        if p >= 0 and p < len(result):
            result[p].append(record)
    y = []
    for r in result:
        y.append(len(r))
    x = []
    # x軸に何を記述するかはx_axisで指定する。
    if x_axis == 'hour':
        for i in range(len(result)):
            x.append(datetime.datetime.utcfromtimestamp(starting + period * i).astimezone(tz=None).strftime("%m/%d %H:%M~"))
    else:
        for i in range(len(result)):
            x.append(datetime.datetime.utcfromtimestamp(starting + period * i).astimezone(tz=None).strftime("%m/%d~"))

    # while y[0] == 0:
    #     y.pop(0)
    #     x.pop(0)
    plt.title(title, loc='center', fontname="Meiryo")
    plt.ticklabel_format(style='plain', axis='y')
    plt.bar(x, y)
    plt.xticks(rotation=90)
    if title == '': title = str(getTimeStrNow())
    title = title.replace('/', '-')
    if loc == '': loc = str(getTimeStrNow())
    location = os.getcwd() + '\\' + 'graphs\\' + loc
    if not Path(location).exists():
        os.mkdir(location)
    plt.savefig('graphs\\' + loc + '\\' + title[:60] + '.png', dpi=300, bbox_inches="tight", pad_inches=0.1)
    plt.close()
    return


def signatureRoundGraph(keys, data):
    plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots()
    ax.pie(data, radius=90, center=(100, 100),
           wedgeprops={"linewidth": 0.2, "edgecolor": "white"}, frame=True)
    ax.set(xlim=(0, 200), xticks=np.arange(1, 8),
           ylim=(0, 200), yticks=np.arange(1, 8))
    plt.show()


def signatureSquareGraph(keys, data):
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(data)))
    df = pd.DataFrame({'signature': keys, 'number': data})
    squarify.plot(sizes=df['number'], alpha=.8)
    plt.axis('off')
    plt.show()
