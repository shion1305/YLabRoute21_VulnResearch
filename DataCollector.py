import json


def importNotDetectData(start=2101, end=2201):
    from ElasticSearcher import search
    query = {
        "term": {
            "analysis_tags.keyword": "not detect"
        }
    }
    return search(query, start, end)