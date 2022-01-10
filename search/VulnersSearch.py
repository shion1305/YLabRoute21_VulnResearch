import configparser
import re

import vulners


def search(sign):
    config = configparser.ConfigParser()
    config.read('../Config.properties')
    config.sections()
    vulners_api = vulners.VulnersApi(config['APIKeys'].get('VULNERS_APIKEY'))

    sign = '"' + re.sub('^/+', '', sign) + '"'
    res = vulners_api.find_all(sign)
    if len(res) != 0:
        arr = {}
        for item in res:
            if len(item["cvelist"]) != 0:
                cve = item["cvelist"][0]
            else:
                res = re.search(r'CVE-[0-9]+-[0-9]+', item["title"])
                if res:
                    cve = res.group()
                else:
                    res = re.search(r'CVE-[0-9]+-[0-9]+', item["title"])
                    cve = item["id"]
            arr[cve] = item["vhref"]
        return arr
    else:
        return []
r = search('/backupmgt/localJob.php')
for d in r.keys():
    print(d)