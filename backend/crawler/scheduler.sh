#!/bin/bash
# 도커 없이 서버에서 cron 으로 돌릴 때 사용 (도커에서는 crawler 서비스가 대신 반복 실행)
#   */30 * * * * /path/to/capstone-2022-14/backend/crawler/scheduler.sh >> /path/to/crawler.log 2>&1
cd "$(dirname "$0")/.." || exit 1
source ../venv/bin/activate 2>/dev/null || true
python crawler/main.py
