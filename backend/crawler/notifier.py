"""지정가 알림: 크롤링 후 새로 들어온 매물 중 사용자가 정한 가격 이하가 있으면 이메일 발송."""
import logging
import smtplib
from email.mime.text import MIMEText

import requests

import config
from catalog import PRODUCTS
from db.queries import catalog_query

log = logging.getLogger(__name__)


def _api(method, path):
    res = requests.request(
        method, f"{config.API_BASE_URL}{path}", headers={"X-Admin-Token": config.ADMIN_TOKEN}, timeout=10
    )
    res.raise_for_status()
    return res.json()


def _send_email(to, subject, content):
    msg = MIMEText(content, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = config.SMTP_FROM
    msg["To"] = to
    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as smtp:
        smtp.starttls()
        smtp.login(config.SMTP_USER, config.SMTP_PASSWORD)
        smtp.send_message(msg)


def _listing_url(src):
    if src.get("url"):
        return src["url"]
    if src.get("market") == "Bunjang":
        return f"https://m.bunjang.co.kr/products/{src['pid']}"
    return "(샘플 데이터)"


def notify(es_client, since_ts):
    """since_ts 이후 올라온 매물로 알림 조건을 확인한다."""
    if not config.ADMIN_TOKEN:
        log.info("ADMIN_TOKEN 이 없어 알림 확인을 건너뜁니다.")
        return
    smtp_ready = all([config.SMTP_HOST, config.SMTP_USER, config.SMTP_PASSWORD])

    try:
        notifications = _api("GET", "/api/notification/list")
    except Exception as e:
        log.error("알림 목록 조회 실패 (%s): %s", config.API_BASE_URL, e)
        return

    for n in notifications:
        if n["product"] not in PRODUCTS:
            continue
        query = catalog_query(n["product"], date_gte=since_ts, price_lte=n["price"])
        hits = es_client.search({"query": query, "size": 20, "sort": [{"price": "asc"}]})["hits"]["hits"]
        if not hits:
            continue

        lines = [
            f"제목: {h['_source']['title']}\n가격: {h['_source']['price']:,}원\n링크: {_listing_url(h['_source'])}"
            for h in hits
        ]
        content = f"[{n['product']}] {n['price']:,}원 이하 매물이 올라왔습니다.\n\n" + "\n\n".join(lines)

        if not smtp_ready:
            log.info("SMTP 미설정: %s 에게 보낼 알림 %d건 (발송 생략)", n["email"], len(hits))
            continue
        try:
            _send_email(n["email"], "지정가 알림입니다.", content)
            _api("DELETE", f"/api/notification/remove/{n['email']}/{n['product']}")
            log.info("알림 발송: %s (%s)", n["email"], n["product"])
        except Exception as e:
            log.error("알림 발송 실패 %s: %s", n["email"], e)
