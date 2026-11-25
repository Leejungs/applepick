import logging
from functools import lru_cache

import config
from db.store import open_store

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_store():
    """요청 시점에 처음 연결한다 (ES 가 늦게 떠도 API 서버는 먼저 뜰 수 있도록)."""
    store = open_store()
    _seed_demo(store)
    return store


def _seed_demo(store):
    """데모 저장소가 비어 있으면 샘플 매물을 채운다 (Elasticsearch 사용 시에는 하지 않음)."""
    from db.memstore import MemoryStore

    if not isinstance(store, MemoryStore) or store.count() > 0 or not config.DEMO_AUTO_SEED:
        return
    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "crawler"))
    from sample import SampleCrawler

    items = SampleCrawler().crawl_data()
    store.bulk_insert((item.doc_id, item.to_doc()) for item in items)
    log.info("데모 저장소에 샘플 매물 %d건 생성", len(items))
