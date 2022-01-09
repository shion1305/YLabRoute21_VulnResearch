from elasticsearch import Elasticsearch


# Sample for query:
# query = {
#     "wildcard": {
#         "request": "*jndi*"
#     }
# }
def search(query=None, starting=2101, ending=2110):
    if query is None:
        query = {
            "term": {
                "url": ""
            }
        }
    result = []
    if starting > ending or ending < 1907 or starting > 2312:
        print("invalid params")
        return
    t = [int(str(starting)[:2]), int(str(starting)[2:])]
    e = [int(str(ending)[:2]), int(str(ending)[2:])]
    es = Elasticsearch("http://localhost:12333")
    while t[0] * 16 + t[1] <= e[0] * 16 + e[1]:
        result.extend(
            es.search(index="xpot_accesslog-20%s.%s" % (format(t[0], '02d'), format(t[1], '02d')), query=query,
                      size=10000)['hits'][
                'hits'])
        if t[1] == 12:
            t[1] = 1
            t[0] += 1
        else:
            t[1] += 1
    return result
