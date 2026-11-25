from config import ES_INDEX

index_name = ES_INDEX

# nori 형태소 분석기를 쓰는 products 인덱스 설정
body = {
    "settings": {
        "analysis": {
            "tokenizer": {
                "nori_mixed": {"type": "nori_tokenizer", "decompound_mode": "mixed"},
            },
            "analyzer": {
                "nori_korean": {
                    "type": "custom",
                    "tokenizer": "nori_mixed",
                    "filter": ["lowercase"],
                },
            },
        }
    },
    "mappings": {
        "properties": {
            "market": {"type": "keyword"},
            "pid": {"type": "keyword"},
            "url": {"type": "keyword", "index": False},
            "keyword": {"type": "text", "analyzer": "nori_korean"},
            "title": {"type": "text", "analyzer": "nori_korean"},
            "desc": {"type": "text", "analyzer": "nori_korean"},
            "price": {"type": "integer"},
            "date": {"type": "long"},  # unix timestamp (초)
            "views": {"type": "integer"},
            "pictures": {"type": "keyword", "index": False},
            "region": {"type": "keyword"},
            "latitude": {"type": "keyword", "index": False},
            "longitude": {"type": "keyword", "index": False},
        }
    },
}
