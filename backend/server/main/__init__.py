import logging
import time

from apispec import APISpec
from elastic_transport import TransportError
from elasticsearch import ApiError
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import HTTPException

import config

db = SQLAlchemy()
log = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        HOST=config.HOST,
        PORT=config.PORT,
        IMAGE_FILE_PATH=str(config.IMAGE_DIR),
        SQLALCHEMY_DATABASE_URI=config.DATABASE_URL,
        SQLALCHEMY_ENGINE_OPTIONS={"pool_pre_ping": True, "pool_recycle": 3600},
        APISPEC_SPEC=APISpec(
            title="ApplePick API",
            version="v2",
            openapi_version="2.0.0",
            plugins=[MarshmallowPlugin()],
        ),
        APISPEC_SWAGGER_URL="/docs.json",
        APISPEC_SWAGGER_UI_URL="/docs/",
    )
    app.json.ensure_ascii = False
    app.json.sort_keys = False
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.errorhandler(HTTPException)
    def json_error(e):
        # webargs 검증 실패(422)는 필드별 메시지를 함께 돌려준다
        messages = getattr(e, "data", {}).get("messages") if hasattr(e, "data") else None
        body = {"error": e.name, "message": messages or e.description}
        return body, e.code

    @app.errorhandler(TransportError)
    @app.errorhandler(ApiError)
    def search_unavailable(e):
        log.error("Elasticsearch 오류: %s", e)
        return {"error": "Search Unavailable", "message": "검색 서버(Elasticsearch)에 연결할 수 없습니다."}, 503

    from server.main.controllers.admin import admin_bp
    from server.main.controllers.ai import ai_bp
    from server.main.controllers.hot import hot_bp
    from server.main.controllers.img import image_bp
    from server.main.controllers.notification import noti_bp
    from server.main.controllers.search import search_bp

    for bp in (search_bp, admin_bp, image_bp, hot_bp, noti_bp, ai_bp):
        app.register_blueprint(bp)

    docs = FlaskApiSpec(app)
    docs.register_existing_resources()
    # 스웨거에서 options 제거
    for key, value in docs.spec._paths.items():
        docs.spec._paths[key] = {k: v for k, v in value.items() if k != "options"}

    with app.app_context():
        from server.main.models import hot_products, notification  # noqa: F401 (테이블 등록)

        _create_tables_with_retry()

    return app


def _create_tables_with_retry(attempts=10, delay=3):
    """DB 컨테이너가 늦게 뜰 수 있으므로 몇 번 재시도하며 테이블을 만든다."""
    for i in range(1, attempts + 1):
        try:
            db.create_all()
            return
        except OperationalError as e:
            if i == attempts:
                log.error("DB 연결 실패: %s", e)
                raise
            log.warning("DB 연결 대기 중... (%d/%d)", i, attempts)
            time.sleep(delay)
