"""크롤러 실행기.

    python crawler/main.py                          # .env 의 CRAWL_SOURCES 로 1회 수집
    python crawler/main.py --sources sample         # 샘플 데이터 생성
    python crawler/main.py --sources bunjang -p 2   # 번개장터 키워드당 2페이지(최대 120개)
    python crawler/main.py --loop 1800              # 30분마다 반복 (도커 crawler 서비스에서 사용)
"""
import argparse
import logging
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # backend/

import config  # noqa: E402
from crawler import SOURCES, Crawler  # noqa: E402
from db.store import open_store  # noqa: E402
from notifier import notify  # noqa: E402

log = logging.getLogger("crawler")


def get_keywords(file_name="keywords.txt"):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def connect(retries=20, delay=3):
    # auto 모드는 ES 가 없으면 바로 데모 저장소로 (도커는 SEARCH_BACKEND=elasticsearch 로 재시도)
    if config.SEARCH_BACKEND != "elasticsearch":
        return open_store()
    for i in range(1, retries + 1):
        try:
            return open_store()
        except Exception as e:
            if i == retries:
                raise
            log.warning("Elasticsearch(%s) 연결 대기 중... (%d/%d) %s", config.ES_HOST, i, retries, type(e).__name__)
            time.sleep(delay)


def run_once(es_client, sources, pages, do_notify, reset):
    started = int(time.time())
    for name in sources:
        if name not in SOURCES:
            log.error("알 수 없는 소스: %s (가능: %s)", name, ", ".join(SOURCES))
            continue
        crawler = Crawler()
        crawler.add_crawler(SOURCES[name]())

        if reset:
            market = crawler.crawlers[0].__class__.__name__.replace("Crawler", "")
            es_client.delete_by_market(market)
            log.info("[%s] 기존 데이터 삭제", name)

        # 샘플 소스는 카탈로그 전체를 한 번에 만든다
        keywords = ["*"] if name == "sample" else get_keywords()
        total = 0
        for keyword in keywords:
            items = crawler.crawl(keyword, pages)
            total += es_client.bulk_insert((item.doc_id, item.to_doc()) for item in items)
            if name != "sample":
                log.info("[%s] '%s' %d건", name, keyword, len(items))
        log.info("[%s] 저장 완료: %d건", name, total)

    es_client.refresh()
    if do_notify:
        # 이번 수집 직전 구간(+여유 10분) 에 올라온 매물로 알림 확인
        notify(es_client, since_ts=started - config.CRAWL_INTERVAL - 600)


def main():
    parser = argparse.ArgumentParser(description="중고 매물 수집기")
    parser.add_argument("-s", "--sources", default=",".join(config.CRAWL_SOURCES), help="bunjang,sample,daangn")
    parser.add_argument("-p", "--pages", type=int, default=config.CRAWL_PAGES, help="키워드당 페이지 수")
    parser.add_argument("--loop", type=int, metavar="SECONDS", help="지정한 초마다 반복 실행")
    parser.add_argument("--no-notify", action="store_true", help="지정가 알림 확인 생략")
    parser.add_argument("--reset", action="store_true", help="수집 전에 해당 소스의 기존 데이터 삭제")
    parser.add_argument("pages_positional", nargs="?", type=int, help=argparse.SUPPRESS)  # 예전 사용법: main.py 10
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    pages = args.pages_positional or args.pages
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]

    es_client = connect()
    log.info("수집 시작: sources=%s pages=%d", sources, pages)

    if not args.loop:
        run_once(es_client, sources, pages, not args.no_notify, args.reset)
        return

    while True:
        try:
            run_once(es_client, sources, pages, not args.no_notify, args.reset)
        except Exception:
            log.exception("수집 중 오류")
        log.info("%d초 후 다시 수집합니다.", args.loop)
        time.sleep(args.loop)


if __name__ == "__main__":
    main()
