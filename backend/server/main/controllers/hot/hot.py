from flask_apispec import doc

from server.main.controllers.hot import API_CATEGORY, hot_bp
from server.main.models.hot_products import HotProducts


@hot_bp.route("/<int:count>", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="인기 검색 상품", description="많이 검색된 상품을 count 개만큼 리턴")
def best(count):
    return HotProducts.getHotProducts(min(count, 50))
