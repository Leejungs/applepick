import datetime

from flask import abort
from flask_apispec import doc

from catalog import PRODUCTS, catalog_for_client
from db import analytics
from db.queries import catalog_query, product_query
from server.main import db
from server.main.controllers.search import API_CATEGORY, search_bp
from server.main.es import get_store
from server.main.models.hot_products import HotProducts

PAGE_SIZE = 20


def _require_product(key):
    if key not in PRODUCTS:
        abort(404, description=f"알 수 없는 상품입니다: {key}")


def _hits(query, size, start=0, sort=None):
    return analytics.hits(get_store(), query, size, start, sort)


@search_bp.route("/products", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="상품 카탈로그", description="검색 가능한 상품 목록(카테고리별)")
def products():
    return {"categories": catalog_for_client()}


@search_bp.route("/<path:query>/<int:idx>", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="상품 매물 페이지 검색", description="상품 키로 매물을 20개씩 최신순으로 검색")
def paging(query, idx):
    _require_product(query)
    results = _hits(
        catalog_query(query),
        size=PAGE_SIZE,
        start=idx * PAGE_SIZE,
        sort=[{"date": "desc"}, "_score"],
    )

    # 인기 검색어 집계 (첫 페이지 요청만 센다)
    if idx == 0:
        if HotProducts.isExistProduct(query) is None:
            HotProducts.addProduct(query)
        else:
            HotProducts.increaseCount(query)
        db.session.commit()

    return {"result": results}


@search_bp.route("/price/<path:query>/<int:size>", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="최근 7일 시세", description="최근 7일 매물로 평균가, 최저가 계산")
def price(query, size):
    _require_product(query)
    stats = analytics.recent_price(get_store(), query, size=size)
    if stats is None:
        return {"avg_price": 0, "min_price": 0, "lower_threshold": 0, "upper_threshold": 0, "std": 0}
    return {**stats, "lower_threshold": analytics.LOWER_THRESHOLD, "upper_threshold": analytics.UPPER_THRESHOLD}


@search_bp.route("/weekly/<path:query>", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="주간 평균가", description="최근 4주 동안 주별 평균가 (최근 주가 앞). 매물이 없는 주는 null")
def weekly(query):
    _require_product(query)
    return {"weekly_price": analytics.weekly_prices(get_store(), query)}


@search_bp.route("/recent/<int:idx>", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="최근 인기 매물", description="최근 7일 매물 중 조회수가 많은 순으로 5개씩")
def recent(idx):
    week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    results = _hits(
        product_query(date_gte=week_ago.timestamp()),
        size=5,
        start=idx * 5,
        sort=[{"views": "desc"}, {"date": "desc"}],
    )
    return {"result": results}
