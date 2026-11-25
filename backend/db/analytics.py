"""시세 분석 로직. 웹 API(search 컨트롤러)와 AI 도구가 함께 사용한다."""
import datetime
import statistics

from db.queries import catalog_query

# 가격 이상치(허위 매물, 부품 판매 등) 제거용 z-score 범위
LOWER_THRESHOLD = -0.5
UPPER_THRESHOLD = 0.9
MAX_SIZE = 500


def hits(store, query, size, start=0, sort=None):
    body = {"query": query, "from": start, "size": size}
    if sort:
        body["sort"] = sort
    return store.search(body)["hits"]["hits"]


def price_stats(prices):
    """z-score 로 이상치를 걸러낸 평균가/최저가. 매물이 없으면 None."""
    if not prices:
        return None
    avg = statistics.fmean(prices)
    std = statistics.pstdev(prices)
    kept = [p for p in prices if LOWER_THRESHOLD < (p - avg) / std < UPPER_THRESHOLD] if std > 0 else prices
    kept = kept or prices
    return {
        "avg_price": int(statistics.fmean(kept)),
        "min_price": int(min(kept)),
        "std": std,
        "count": len(prices),
    }


def recent_price(store, key, days=7, size=MAX_SIZE):
    now = datetime.datetime.now()
    since = now - datetime.timedelta(days=days)
    found = hits(store, catalog_query(key, date_gte=since.timestamp(), date_lt=now.timestamp()), size=min(size, MAX_SIZE))
    stats = price_stats([h["_source"]["price"] for h in found])
    if stats:
        markets = {}
        for h in found:
            m = h["_source"].get("market", "")
            markets[m] = markets.get(m, 0) + 1
        stats["markets"] = markets
    return stats


def weekly_prices(store, key, weeks=4):
    """[이번 주, 1주 전, ...] 주별 평균가. 매물이 없는 주는 None."""
    now = datetime.datetime.now()
    result = []
    for week in range(weeks):
        lt = now - datetime.timedelta(days=7 * week)
        gte = now - datetime.timedelta(days=7 * (week + 1))
        found = hits(store, catalog_query(key, date_gte=gte.timestamp(), date_lt=lt.timestamp()), size=MAX_SIZE)
        stats = price_stats([h["_source"]["price"] for h in found])
        result.append(stats["avg_price"] if stats else None)
    return result


def trend_label(weekly):
    """주간 평균가 흐름을 한 단어로."""
    values = [v for v in reversed(weekly) if v]  # 오래된 주 -> 최근 주
    if len(values) < 2:
        return "판단 불가"
    change = (values[-1] - values[0]) / values[0]
    if change <= -0.03:
        return f"하락 ({change:+.1%})"
    if change >= 0.03:
        return f"상승 ({change:+.1%})"
    return f"보합 ({change:+.1%})"
