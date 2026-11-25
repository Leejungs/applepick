"""WSGI 진입점: gunicorn app:application / Vercel(services: entrypoint app:application)"""
import logging
import traceback

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

try:
    from server.main import create_app

    application = create_app()
except Exception as _e:  # 시작 실패 원인을 로그와 응답으로 확인할 수 있게 한다
    _detail = traceback.format_exc()
    logging.error("앱 시작 실패:\n%s", _detail)

    from flask import Flask

    application = Flask(__name__)

    @application.route("/", defaults={"path": ""})
    @application.route("/<path:path>")
    def _startup_failed(path):
        lines = _detail.strip().splitlines()
        return {"error": "Startup Failed", "message": f"{type(_e).__name__}: {_e}", "trace": lines[-12:]}, 500

app = application
