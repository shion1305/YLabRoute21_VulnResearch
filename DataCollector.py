import json
from concurrent import futures

from elasticsearch import Elasticsearch


def importNotDetectData(start=2101, end=2201):
    from ElasticSearcher import search
    query = {
        "term": {
            "analysis_tags.keyword": "not detect"
        }
    }
    return search(query, start, end)


def export(year, month, day):
    es = Elasticsearch("http://localhost:12333")
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
            r1 = es.search(index="xpot_accesslog-20%02d.%02d" % (year, month), body=query,
                           size=10000)['hits']['hits']
            if len(r1) == 10000: print("WARNING 20%02d-%02d-%02dT%02d:%02d:00.000Z" % (year, month, day, j, k * 10))
            result.extend(r1)
    json_string = json.dumps(result)
    with open('ImportedData/data20%02d-%02d%02d.json' % (year, month, day), 'w') as outfile:
        json.dump(json_string, outfile)
    print('COMPLETED: ImportedData/data20%02d-%02d%02d.json' % (year, month, day))


def exportAllData(start=2110, end=2112):
    from elasticsearch import Elasticsearch
    t = [int(str(start)[:2]), int(str(start)[2:])]
    e = [int(str(end)[:2]), int(str(end)[2:])]
    result = []
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        while t[0] * 16 + t[1] <= e[0] * 16 + e[1]:
            future_list = []
            for i in range(1, getDays_in_Month(t[0] * 100 + t[1]) + 1):
                future = executor.submit(export, year=t[0], month=t[1], day=i)
                future_list.append(future)
        if t[1] == 12:
            t[1] = 1
            t[0] += 1
        else:
            t[1] += 1
    _ = futures.as_completed(fs=future_list)


def getDays_in_Month(t):
    d = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (t % 20 == 2):
        return 29
    return d[t % 20 - 1]


exportAllData()
