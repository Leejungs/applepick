import json
import logging

from flask import Response, request, stream_with_context
from flask_apispec import doc

import config
from server.main.controllers.ai import API_CATEGORY, ai_bp

log = logging.getLogger(__name__)

EXAMPLES = [
    "아이폰 15 프로 90만원 이하 매물 찾아줘",
    "맥북 에어 요즘 시세 어때? 지금 사도 될까?",
    "에어팟 프로 2를 13만원에 판다는데 괜찮은 가격이야? 설명에 '카톡으로 연락 주세요, 선입금 시 예약'이라고 써 있어",
    "중고 아이폰 살 때 꼭 확인해야 할 것 알려줘",
    "아이폰 17 출시 가격이 얼마였는지 찾아보고 지금 중고 시세랑 비교해줘",
]


@ai_bp.route("/status", methods=["GET"])
@doc(tags=[API_CATEGORY], summary="AI 사용 가능 여부", description="OPENAI_API_KEY 설정 여부와 모델")
def status():
    return {"enabled": bool(config.OPENAI_API_KEY), "model": config.AI_MODEL, "examples": EXAMPLES}


@ai_bp.route("/chat", methods=["POST"])
@doc(
    tags=[API_CATEGORY],
    summary="AI 어시스턴트 대화 (SSE)",
    description='body: {"message": str, "history": [{"role","content"}]} -> text/event-stream 으로 진행 이벤트와 답변 전송',
)
def chat():
    body = request.get_json(silent=True) or {}
    message = (body.get("message") or "").strip()[:2000]
    history = [
        {"role": h["role"], "content": str(h["content"])[:4000]}
        for h in (body.get("history") or [])[-10:]
        if h.get("role") in ("user", "assistant") and h.get("content")
    ]
    if not message:
        return {"error": "Bad Request", "message": "message 가 비어 있습니다."}, 400
    if not config.OPENAI_API_KEY:
        return {"error": "AI Disabled", "message": ".env 에 OPENAI_API_KEY 를 설정하면 AI 어시스턴트를 쓸 수 있습니다."}, 503

    from ai.graph import run  # 키가 있을 때만 로드

    def sse():
        try:
            for event in run(message, history):
                yield f"data: {json.dumps(event, ensure_ascii=False, default=str)}\n\n"
        except Exception as e:
            log.exception("AI 처리 실패")
            yield f"data: {json.dumps({'type': 'error', 'message': _friendly(e)}, ensure_ascii=False)}\n\n"
        yield 'data: {"type": "done"}\n\n'

    return Response(
        stream_with_context(sse()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def _friendly(e):
    import openai

    if isinstance(e, openai.AuthenticationError):
        return "API 키가 올바르지 않습니다. .env 의 OPENAI_API_KEY 를 확인해 주세요."
    if isinstance(e, openai.RateLimitError):
        return "요청 한도를 넘었거나 크레딧이 부족합니다. OpenAI 결제/사용량을 확인해 주세요."
    if isinstance(e, openai.NotFoundError):
        return f"모델을 찾을 수 없습니다. .env 의 AI_MODEL 값을 확인해 주세요. ({e})"
    if isinstance(e, openai.APIConnectionError):
        return "AI 서버에 연결할 수 없습니다. 인터넷 연결을 확인해 주세요."
    if isinstance(e, openai.APIStatusError):
        return f"AI 요청 오류 ({e.status_code}): {e.message}"
    return f"처리 중 오류가 발생했습니다: {e}"
