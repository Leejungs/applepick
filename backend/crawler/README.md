# Crawler

매물을 수집해서 Elasticsearch `products` 인덱스에 저장하고, 지정가 알림을 확인합니다.

## 소스

| 이름 | 상태 | 설명 |
|---|---|---|
| `bunjang` | 사용 | 번개장터 웹 API (`/api/search/v8/web/search`, `/api/pms/v1/products/{pid}/detail/web`) |
| `sample` | 사용 | 카탈로그 전 모델의 최근 4주치 가짜 매물. 개발·시연용 (`market: Sample`) |
| `daangn` | 비활성 | 당근 웹이 자동 요청을 차단(CloudFront 403)해서 수집하지 않음 |

새 소스는 `crawl_data(keyword, pages) -> [ItemBase]` 를 구현한 클래스를 만들고 `crawler.py` 의 `SOURCES` 에 등록하면 됩니다.

## 실행

```bash
# 도커 (권장): crawler 서비스가 CRAWL_INTERVAL 마다 자동 실행
docker compose exec api python crawler/main.py --sources sample --no-notify   # 샘플 데이터 넣기
docker compose logs -f crawler

# 로컬 (backend/ 에서)
python crawler/main.py --sources bunjang --pages 1
python crawler/main.py --sources sample --reset
```

옵션: `--sources`, `--pages`, `--loop SECONDS`, `--no-notify`, `--reset`

## 키워드

`keywords.txt` 에 한 줄에 하나씩. 번개장터에서 이 키워드로 검색한 최신 매물을 가져오고, 모델 구분은 검색 시점에
`catalog.py` 의 검색어로 합니다.

## 지정가 알림

`.env` 에 `ADMIN_TOKEN` 과 `SMTP_*` 를 설정하면, 수집 후 새 매물 중 사용자가 등록한 가격 이하가 있을 때 이메일을 보냅니다.
SMTP 가 없으면 로그에만 남깁니다.
