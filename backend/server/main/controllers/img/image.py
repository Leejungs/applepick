from flask import current_app, send_from_directory
from flask_apispec import doc

from server.main.controllers.img import API_CATEGORY, image_bp


@image_bp.route("/<path:path>", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="이미지 다운로드", description="크롤러가 로컬에 저장한 이미지 (예: bunjang_image/123_1.jpg)")
def download(path):
    # send_from_directory 가 상위 경로 접근(../)을 막아 준다
    return send_from_directory(current_app.config["IMAGE_FILE_PATH"], path)
