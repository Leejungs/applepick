from flask import Blueprint

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

API_CATEGORY = "AI"

from server.main.controllers.ai.chat import *  # noqa: E402,F401,F403
