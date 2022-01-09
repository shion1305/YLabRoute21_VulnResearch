def groupByDestIp(data):
    """Collect only ip"""
    result = {}
    for d in data:
        geo_ip = d['_source']['destination_ip']
        # もしもgeo_ipがresultフィールドになかった場合
        if not geo_ip in result:
            result[geo_ip] = []
        result[geo_ip].append(d)
    return result


def groupBySignature(data):
    dic = {}
    for i in data:
        signature = i['_source']['url']
        if signature.count('?') != 0:
            signature = signature[:signature.index('?')]
        if not signature in dic:
            dic[signature] = []
        dic[signature].append(i)
    return dic


def groupByPorts(data):
    r_ports = {}
    for d in data:
        if not d['_source']['destination_port'] in r_ports:
            r_ports[d['_source']['destination_port']] = []
        r_ports[d['_source']['destination_port']].append(d)
    return r_ports

def valueSort(data):
    """This def sorts value if value is sortable"""
    tmp = []
    for k, v in data.items():
        tmp.append([k, v])
    print(type(tmp))
    return sorted(tmp, key=lambda x: x[1], reverse=True)


def printDictionary(data):
    for k, v in data.items():
        print(k, v)
    return


def printList(data):
    fmt = "| {0:<60} | {1:>4} |"
    for a, b in data:
        print(fmt.format(a, str(b)))


def printData(data):
    for k, v in data.items():
        print(k, v)
    return
