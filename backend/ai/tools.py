"""AI 에이전트가 쓰는 자체 도구(Tools). LangChain @tool 로 정의한다.

각 도구는 (모델에게 줄 텍스트, 화면에 그릴 artifact) 를 함께 돌려준다 (response_format="content_and_artifact").
"""
import datetime
import json
import re
from typing import Literal, Optional

from langchain_core.tools import tool

from ai.rag import get_retriever
from catalog import CATEGORIES, PRODUCT_CATEGORY, PRODUCTS, label
from db import analytics
from db.queries import catalog_query

SORTS = {
    "latest": [{"date": "desc"}],
    "price_low": [{"price": "asc"}],
    "views": [{"views": "desc"}],
}
RISK_PATTERNS = {
    "선입금 요구": r"선입금|먼저\s*입금|입금\s*먼저|예약금",
    "외부 메신저 유도": r"카톡|카카오톡|텔레그램|라인\s*아이디|오픈채팅",
    "택배 거래만 고집": r"택배\s*(거래)?만|직거래\s*(불가|안)",
    "외부 결제 링크": r"https?://|링크로\s*결제|안전결제\s*링크",
    "급매 재촉": r"급처|급매|오늘만|선착순",
    "잠금/분실 의심": r"활성화\s*잠금|icloud|아이클라우드|분실|습득",
    "부품/고장": r"부품용|고장|파손|침수|액정\s*깨",
}
GOOD_PATTERNS = {
    "애플케어 남음": r"애플\s*케어|applecare",
    "미개봉/새상품": r"미개봉|새\s*상품|새제품",
    "풀박스": r"풀\s*박스|구성품\s*(전부|모두)",
    "배터리 양호": r"배터리\s*(성능|효율)?\s*(9\d|100)\s*%?",
}


def _store():
    from server.main.es import get_store

    return get_store()


def _norm(text):
    return re.sub(r"\s+", "", str(text).lower())


def _check_key(product_key):
    if product_key in PRODUCTS:
        return None
    return f"'{product_key}' 는 카탈로그에 없는 상품 키입니다. find_product 로 정확한 키를 먼저 찾으세요."


def _listing(hit):
    s = hit["_source"]
    url = s.get("url") or (f"https://m.bunjang.co.kr/products/{s['pid']}" if s.get("market") == "Bunjang" else "")
    return {
        "id": hit["_id"],
        "title": s.get("title", ""),
        "price": s.get("price", 0),
        "market": s.get("market", ""),
        "date": datetime.datetime.fromtimestamp(s.get("date", 0)).strftime("%Y-%m-%d %H:%M"),
        "views": s.get("views", 0),
        "region": s.get("region", ""),
        "url": url,
        "thumbnail": (s.get("pictures") or [""])[0],
        "keyword": s.get("keyword", ""),
    }


@tool(response_format="content_and_artifact")
def find_product(text: str):
    """사용자가 말한 제품명(예: '아이폰15프로', '에어팟 프로 2세대', '맥북에어')을 서비스 카탈로그의 정확한 상품 키로 바꾼다.
    다른 도구에는 반드시 이 도구가 돌려준 product_key 를 넣어야 한다."""
    q = _norm(text)
    q_tokens = set(re.findall(r"[가-힣]+|[a-z]+|\d+", text.lower()))
    scored = []
    for key, query in PRODUCTS.items():
        names = [_norm(key), _norm(query)]
        tokens = set(re.findall(r"[가-힣]+|[a-z]+|\d+", f"{key} {query}".lower()))
        score = len(q_tokens & tokens) * 2
        if any(n == q for n in names):
            score += 10
        elif any(n in q or q in n for n in names):
            score += 4
        if score:
            scored.append((score, -len(key), key))
    scored.sort(reverse=True)
    matches = [
        {"product_key": k, "label": label(k, PRODUCT_CATEGORY[k]), "search_query": PRODUCTS[k]} for _, _, k in scored[:5]
    ]
    if not matches:
        cats = ", ".join(c["name"] for c in CATEGORIES)
        return f"일치하는 상품이 없습니다. 지원 카테고리: {cats}", []
    return json.dumps(matches, ensure_ascii=False), matches


@tool(response_format="content_and_artifact")
def search_listings(
    product_key: str,
    max_price: Optional[int] = None,
    sort: Literal["latest", "price_low", "views"] = "latest",
    limit: int = 5,
):
    """수집된 중고 매물(번개장터 등)을 검색한다. max_price 로 예산 상한을, sort 로 정렬
    (latest=최신순, price_low=낮은 가격순, views=조회수순)을 정할 수 있다."""
    if err := _check_key(product_key):
        return err, None
    limit = max(1, min(int(limit or 5), 10))
    store = _store()
    # 시세의 절반 미만은 부품·미끼 매물일 가능성이 높아 제외
    stats = analytics.recent_price(store, product_key)
    floor = int(stats["avg_price"] * 0.5) if stats else None
    query = catalog_query(product_key, price_lte=max_price)
    if floor:
        query["bool"]["filter"].append({"range": {"price": {"gte": floor}}})
    found = analytics.hits(store, query, size=limit, sort=SORTS[sort])
    listings = [_listing(h) for h in found]
    if not listings:
        return f"{product_key} 조건에 맞는 매물이 없습니다.", {"product": product_key, "listings": []}
    return (
        json.dumps(
            {"product": product_key, "count": len(listings), "excluded_below_price": floor, "listings": listings},
            ensure_ascii=False,
        ),
        {"product": product_key, "listings": listings},
    )


@tool(response_format="content_and_artifact")
def get_market_price(product_key: str):
    """모델의 최근 7일 평균 시세·최저가와 최근 4주 주간 평균가 추이(상승/하락/보합)를 계산한다."""
    if err := _check_key(product_key):
        return err, None
    store = _store()
    stats = analytics.recent_price(store, product_key)
    weekly = analytics.weekly_prices(store, product_key)
    result = {
        "product": product_key,
        "avg_price_7d": stats["avg_price"] if stats else None,
        "min_price_7d": stats["min_price"] if stats else None,
        "sample_count_7d": stats["count"] if stats else 0,
        # 시세 계산에 쓰인 매물 출처. Sample 은 시연용 가짜 데이터
        "data_sources_7d": stats["markets"] if stats else {},
        "weekly_avg_recent_first": weekly,
        "trend": analytics.trend_label(weekly),
    }
    return json.dumps(result, ensure_ascii=False), result


@tool(response_format="content_and_artifact")
def evaluate_deal(product_key: str, price: int, description: str = ""):
    """특정 가격(과 매물 설명)이 좋은 거래인지 평가한다. 시세 대비 가격 수준을 분류하고,
    설명에서 사기 위험 신호(선입금, 외부 메신저 유도 등)와 긍정 신호(애플케어, 풀박스 등)를 찾아낸다."""
    if err := _check_key(product_key):
        return err, None
    stats = analytics.recent_price(_store(), product_key)
    verdict, ratio = "시세 정보 부족", None
    if stats:
        ratio = price / stats["avg_price"]
        if ratio < 0.6:
            verdict = "사기·하자 의심 (시세보다 지나치게 저렴)"
        elif ratio < 0.85:
            verdict = "매우 저렴"
        elif ratio < 0.95:
            verdict = "저렴한 편"
        elif ratio <= 1.05:
            verdict = "적정 가격"
        elif ratio <= 1.2:
            verdict = "비싼 편"
        else:
            verdict = "매우 비쌈"
    text = description or ""
    risks = [name for name, pat in RISK_PATTERNS.items() if re.search(pat, text, re.I)]
    goods = [name for name, pat in GOOD_PATTERNS.items() if re.search(pat, text, re.I)]
    result = {
        "product": product_key,
        "price": price,
        "market_avg_7d": stats["avg_price"] if stats else None,
        "market_min_7d": stats["min_price"] if stats else None,
        "price_vs_avg": f"{ratio - 1:+.1%}" if ratio else None,
        "verdict": verdict,
        "risk_signals": risks,
        "positive_signals": goods,
    }
    return json.dumps(result, ensure_ascii=False), result


@tool(response_format="content_and_artifact")
def search_buying_guide(query: str):
    """중고 애플 제품 구매·판매 가이드 문서(RAG)를 검색한다. 사기 예방, 모델별 체크리스트(배터리, 활성화 잠금,
    정품 확인), 가격 협상, 서비스 사용법 같은 질문에 근거로 사용한다."""
    docs = get_retriever().invoke(query)
    if not docs:
        return "관련 가이드 문서를 찾지 못했습니다.", []
    sources = [{"title": d.metadata["title"], "section": d.metadata["section"]} for d in docs]
    content = "\n\n---\n\n".join(d.page_content for d in docs)
    return content, sources


@tool(response_format="content_and_artifact")
def register_price_alert(email: str, product_key: str, target_price: int):
    """사용자가 요청할 때만 사용: 지정한 모델이 target_price 이하로 올라오면 이메일 알림을 받도록 등록한다."""
    if err := _check_key(product_key):
        return err, None
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or ""):
        return "이메일 형식이 올바르지 않습니다. 사용자에게 이메일을 다시 물어보세요.", None
    from server.main import db
    from server.main.models.notification import Notification

    Notification.addNotification(email, product_key, int(target_price))
    db.session.commit()
    result = {"email": email, "product": product_key, "target_price": int(target_price)}
    return json.dumps({"registered": True, **result}, ensure_ascii=False), result


TOOLS = [find_product, search_listings, get_market_price, evaluate_deal, search_buying_guide, register_price_alert]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}

# 화면 표시용 이름
TOOL_LABELS = {
    "find_product": "상품 찾기",
    "search_listings": "매물 검색",
    "get_market_price": "시세 분석",
    "evaluate_deal": "거래 평가",
    "search_buying_guide": "가이드 검색(RAG)",
    "register_price_alert": "알림 등록",
    "web_search": "웹 검색",
}
