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

        from flask import Flask

        fallback = Flask(__name__)

        @fallback.route("/", defaults={"path": ""})
        @fallback.route("/<path:path>")
        def startup_failed(path):
            return {
                "error": "Startup Failed",
                "message": f"{type(e).__name__}: {e}",
                "trace": detail.strip().splitlines()[-12:],
            }, 500

        return fallback


application = _build()
app = application
