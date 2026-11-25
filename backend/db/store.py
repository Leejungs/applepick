"""검색 저장소 선택: Elasticsearch 가 있으면 사용하고, 없으면 파일 기반 MemoryStore 로 대체."""
import logging

import config

log = logging.getLogger(__name__)


def _es_alive():
    """재시도 없이 2초 안에 응답하는지만 확인 (없을 때 시작이 느려지고 로그가 지저분해지는 것 방지)."""
    from elasticsearch import Elasticsearch

    logging.getLogger("elastic_transport").setLevel(logging.ERROR)
    try:
        return Elasticsearch(config.ES_HOST, request_timeout=2, max_retries=0).ping()
    except Exception:
        return False


def open_store():
    backend = config.SEARCH_BACKEND
    if backend == "elasticsearch" or (backend == "auto" and _es_alive()):
        from db.esstore import EsStore

        store = EsStore()
        log.info("검색 저장소: Elasticsearch (%s)", config.ES_HOST)
        return store

    if backend == "auto":
        log.warning("Elasticsearch(%s) 없음 -> 데모 저장소 사용", config.ES_HOST)

    from db.memstore import MemoryStore

    log.info("검색 저장소: 데모 파일 %s", config.DEMO_DATA_FILE)
    return MemoryStore(str(config.DEMO_DATA_FILE))
