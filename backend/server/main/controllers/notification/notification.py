from flask_apispec import doc, use_kwargs

from catalog import PRODUCTS
from server.main import db
from server.main.controllers.notification import API_CATEGORY, noti_bp
from server.main.models.notification import Notification
from server.main.schema.notification import RequestNotificationSchema
from server.utils.common import require_admin_token, response_json_with_code


@noti_bp.route("/submit", methods=["POST"])
@use_kwargs(RequestNotificationSchema)
@doc(tags=[API_CATEGORY], summary="알림 등록", description="지정가 이하 매물이 올라오면 이메일로 알림")
def submit(email, product, price):
    if product not in PRODUCTS:
        return response_json_with_code(res_code=400, result="Wrong product")
    Notification.addNotification(email, product, price)
    db.session.commit()
    return response_json_with_code(result={"email": email, "product": product, "price": price})


@noti_bp.route("/list", methods=["GET"])
@require_admin_token
@doc(tags=[API_CATEGORY], summary="알림 목록 (크롤러 전용)", description="X-Admin-Token 헤더 필요")
def notification():
    return Notification.getNotification()


@noti_bp.route("/remove/<path:email>/<path:product>", methods=["DELETE"])
@require_admin_token
@doc(tags=[API_CATEGORY], summary="알림 삭제 (크롤러 전용)", description="X-Admin-Token 헤더 필요")
def remove_notification(email, product):
    Notification.removeNotification(email, product)
    db.session.commit()
    return response_json_with_code(result="Removed")
