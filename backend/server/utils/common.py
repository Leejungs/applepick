import hmac
from functools import wraps

from flask import abort, jsonify, make_response, request

import config


def response_json_with_code(res_code=200, **kwargs):
    return make_response(jsonify(kwargs), res_code)


def require_admin_token(view):
    """X-Admin-Token 헤더가 ADMIN_TOKEN 과 일치해야 호출 가능 (크롤러 전용 API 보호)."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        expected = config.ADMIN_TOKEN
        given = request.headers.get("X-Admin-Token", "")
        if not expected or not hmac.compare_digest(given, expected):
            abort(401, description="관리자 토큰이 필요합니다.")
        return view(*args, **kwargs)

    return wrapper
