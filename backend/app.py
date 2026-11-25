"""WSGI 진입점: gunicorn app:application / Vercel(services: entrypoint app:application)

Vercel 은 빌드 시 이 파일을 실행하지 않고 읽기만 해서 `application` 을 찾으므로,
반드시 모듈 최상위에서 `application = ...` 형태로 정의해야 한다.
"""
import logging
import traceback

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _build():
    try:
        from server.main import create_app

        return create_app()
    except Exception as e:  # 시작 실패 원인을 로그와 응답으로 확인할 수 있게 한다
        detail = traceback.format_exc()
        logging.error("앱 시작 실패:\n%s", detail)

        import json
        import sys

        body = json.dumps(
            {
                "error": "Startup Failed",
                "message": f"{type(e).__name__}: {e}",
                "python": sys.version,
                "sys_path": sys.path[:6],
                "trace": detail.strip().splitlines()[-12:],
            },
            ensure_ascii=False,
        ).encode("utf-8")

        # Flask 가 없을 수도 있으므로 순수 WSGI 함수로 응답한다
        def fallback(environ, start_response):
            start_response("500 Internal Server Error", [("Content-Type", "application/json; charset=utf-8")])
            return [body]

        return fallback


application = _build()
app = application
