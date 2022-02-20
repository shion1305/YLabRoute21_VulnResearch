import json
import time
from concurrent import futures

import elastic_transport
import simpleaudio
from elasticsearch import Elasticsearch


def exportJson(target, year, month, day):
    with open('ImportedData/data20%02d-%02d%02d.json' % (year, month, day), 'w') as outfile:
        json.dump(target, outfile)
    print('COMPLETED: ImportedData/data20%02d-%02d%02d.json' % (year, month, day))


def exportDaily(year, month, day):
    es = Elasticsearch("http://localhost:12333", request_timeout=60)
    result = []
    for j in range(0, 24):
        for k in range(0, 6):
            query = {
                "query": {
                    "range": {
                        "@timestamp": {
                            "gte": "20%02d-%02d-%02dT%02d:%02d:00.000Z" % (year, month, day, j, k * 10),
                            "lt": "20%02d-%02d-%02dT%02d:%02d:59.999Z" % (year, month, day, j, (k + 1) * 10 - 1)
                        }
                    }
                }
            }
            print(query)
            r1 = es.search(index="xpot_accesslog-20%02d.%02d" % (year, month), body=query,
                           size=10000)['hits']['hits']
            print(len(r1))
            if len(r1) == 10000: print("WARNING 20%02d-%02d-%02dT%02d:%02d:00.000Z" % (year, month, day, j, k * 10))
            result.extend(r1)
    # exportJson(target=result, year=year, month=month, day=day)
    exportJson(target=result, year=year, month=month, day=day)


def exportAllData(start=211001, end=211231):
    try:
        t = [int(str(start)[:2]), int(str(start)[2:4]), start % 100]
        e = [int(str(end)[:2]), int(str(end)[2:4]), end % 100]
        while t[0] * 16 + t[1] <= e[0] * 16 + e[1]:
            for i in range(t[2] if int(str(start)[:2]) == t[0] and int(str(start)[2:4]) == t[1] else 1,
                           e[2] + 1 if t[0] == e[0] and t[1] == e[1] else getDays_in_Month(t[0] * 100 + t[1]) + 1):
                exportDaily(year=t[0], month=t[1], day=i)
            if t[1] == 12:
                t[1] = 1
                t[0] += 1
            else:
                t[1] += 1
    except elastic_transport.ConnectionTimeout:
        while (True):
            wav = simpleaudio.WaveObject.from_wave_file("alarm_sound.wav")
            playO = wav.play()
            playO.wait_done()


def getDays_in_Month(t):
    d = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if t % 20 == 2:
        return 29
    return d[t % 20 - 1]


exportAllData(start=211008, end=211020)
