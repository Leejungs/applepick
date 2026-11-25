from flask_apispec import doc

from server.main.controllers.admin import API_CATEGORY, admin_bp
from server.main.es import get_store


@admin_bp.route("/stats", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="수집 현황", description="마켓별 저장된 매물 수")
def stats():
    result = get_store().search({"size": 0, "aggs": {"markets": {"terms": {"field": "market"}}}})
    markets = {b["key"]: b["doc_count"] for b in result["aggregations"]["markets"]["buckets"]}
    return {"total": result["hits"]["total"]["value"], "markets": markets}


@admin_bp.route("/health", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="헬스 체크", description="API, Elasticsearch 연결 상태")
def health():
    try:
        es_ok = bool(get_store().es.ping())
    except Exception:
        es_ok = False
    return {"api": True, "elasticsearch": es_ok}
