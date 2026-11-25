r"""LangGraph + LangChain(OpenAI) 로 구성한 AI 어시스턴트.

    START -> analyze --(off_topic)--> decline -> END
                     \--(그 외)----> agent <--> tools
                                      |
                                      +--> END (최종 답변)

- analyze : LLM 이 질문 의도를 분류 (LangChain with_structured_output)
- agent   : LLM 이 자체 도구 + OpenAI 웹 검색(내장 도구)을 골라 쓰며 답변 작성 (LangChain bind_tools)
- tools   : LangChain 도구 실행 (매물 검색, 시세 분석, 거래 평가, RAG 가이드 검색, 알림 등록 ...)

필요한 키는 OPENAI_API_KEY 하나 (LLM + 웹 검색).
"""
import datetime
import logging
import operator
from typing import Annotated, Any, Literal, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

import config
from ai.tools import TOOL_LABELS, TOOLS, TOOLS_BY_NAME

log = logging.getLogger(__name__)

MAX_AGENT_STEPS = 8

INTENTS = {
    "find_listings": "매물 찾기",
    "price_check": "시세 확인",
    "deal_evaluation": "거래 평가",
    "buying_guide": "구매 가이드",
    "selling_advice": "판매 조언",
    "price_alert": "알림 등록",
    "latest_info": "최신 정보",
    "service_help": "서비스 안내",
    "off_topic": "관련 없음",
}


class Analysis(BaseModel):
    """사용자 질문 분석 결과."""

    intent: Literal[
        "find_listings",
        "price_check",
        "deal_evaluation",
        "buying_guide",
        "selling_advice",
        "price_alert",
        "latest_info",
        "service_help",
        "off_topic",
    ] = Field(description="질문 의도")
    products: list[str] = Field(description="질문에 나온 제품명 그대로 (없으면 빈 목록)")
    budget: Optional[int] = Field(description="언급된 예산/가격(원). 없으면 null")
    summary: str = Field(description="사용자 요청을 한 문장으로 요약")


SYSTEM_PROMPT = """당신은 애플 중고 제품 통합 검색 서비스 '애플픽(ApplePick)'의 AI 어시스턴트입니다.
오늘 날짜: {today}

## 역할
사용자가 애플 중고 제품(iPhone, iPad, Mac, MacBook, Apple Watch, AirPods)을 사고팔 때 도와줍니다.

## 도구 사용 원칙
- 가격, 매물, 시세 같은 숫자는 반드시 도구 결과에서 가져오고 지어내지 않습니다.
- 제품명이 나오면 먼저 find_product 로 정확한 product_key 를 찾은 뒤 다른 도구에 넣습니다.
- 매물 추천: search_listings (예산이 있으면 max_price). 시세/추이: get_market_price.
- 특정 가격·매물이 괜찮은지: evaluate_deal (매물 설명이 있으면 description 에 넣기).
- 체크리스트·사기 예방·협상·서비스 사용법: search_buying_guide 로 가이드 문서를 근거로 답합니다.
- 서비스 데이터에 없는 최신 정보(신제품 출시일, 애플 공식 가격, 정책 변경, 뉴스)는 web_search 를 사용합니다.
- register_price_alert 는 사용자가 이메일과 함께 알림을 원할 때만 호출합니다.
- 서로 독립적인 도구는 한 번에 같이 호출해도 됩니다.

## 답변 형식
- 한국어로, 핵심부터 간결하게. 마크다운 소제목과 목록을 활용합니다.
- 가격은 '1,234,000원' 형식으로 씁니다.
- 도구 결과에 market 'Sample'(시연용 샘플 데이터)이 실제로 포함된 경우에만 그 사실을 한 줄로 밝힙니다.
  (시세의 data_sources_7d 에 Sample 이 섞여 있으면 "샘플 데이터 포함 시세"라고 말합니다. 없으면 언급하지 않습니다.)
- 매물 목록은 화면에 카드로 따로 표시되므로, 답변에서는 핵심 매물 2~3개만 언급합니다.
- 이 질문의 분석 결과: 의도={intent}, 언급 제품={products}, 예산={budget}
"""


class AgentState(TypedDict, total=False):
    question: str
    history: list  # [{"role": "user"|"assistant", "content": str}]
    analysis: dict
    messages: list[BaseMessage]  # agent 루프용 LangChain 메시지
    steps: int
    answer: str
    events: Annotated[list, operator.add]  # 화면에 보낼 진행 이벤트


_llm = None


def llm():
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=config.AI_MODEL,
            reasoning_effort=config.AI_EFFORT,
            use_responses_api=True,  # 웹 검색 내장 도구 사용
            output_version="responses/v1",
            timeout=120,
            max_retries=2,
        )
    return _llm


def is_enabled():
    return bool(config.OPENAI_API_KEY)


def _history_messages(history):
    return [
        HumanMessage(m["content"]) if m["role"] == "user" else AIMessage(m["content"]) for m in history[-8:]
    ]


def _web_events(message: AIMessage):
    """응답에 포함된 웹 검색 호출과 출처(url_citation)를 화면 이벤트로 변환."""
    events, sources = [], {}
    blocks = message.content if isinstance(message.content, list) else []
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "web_search_call":
            query = (block.get("action") or {}).get("query") or ""
            events.append(
                {"type": "tool", "name": "web_search", "label": TOOL_LABELS["web_search"], "input": {"query": query}}
            )
        for ann in block.get("annotations") or []:
            if isinstance(ann, dict) and ann.get("type") == "url_citation" and ann.get("url"):
                sources.setdefault(ann["url"], ann.get("title") or ann["url"])
    if sources:
        events.append({"type": "web_results", "sources": [{"url": u, "title": t} for u, t in list(sources.items())[:5]]})
    return events


# ---------------- 노드 ----------------


def analyze(state: AgentState):
    """질문 의도 분류 (구조화 출력)."""
    convo = "".join(f"{m['role']}: {m['content']}\n" for m in state.get("history", [])[-4:])
    classifier = llm().with_structured_output(Analysis)
    try:
        result: Analysis = classifier.invoke(
            [
                SystemMessage("애플 중고거래 서비스로 들어온 질문을 분류하세요. 이전 대화 맥락도 고려합니다."),
                HumanMessage(f"이전 대화:\n{convo or '(없음)'}\n\n질문: {state['question']}"),
            ]
        )
        analysis = result.model_dump()
    except Exception as e:  # 분류 실패해도 답변은 계속
        log.warning("의도 분류 실패: %s", e)
        analysis = {"intent": "service_help", "products": [], "budget": None, "summary": state["question"]}
    analysis["intent_label"] = INTENTS.get(analysis.get("intent"), "기타")
    return {"analysis": analysis, "events": [{"type": "intent", **analysis}]}


def decline(state: AgentState):
    answer = (
        "저는 애플 중고 제품 거래를 돕는 어시스턴트예요. 🍎\n\n"
        "예를 들어 이렇게 물어보세요:\n"
        "- 아이폰 15 프로 90만원 이하 매물 찾아줘\n"
        "- 맥북 에어 시세가 요즘 어때?\n"
        "- 에어팟 프로 2 중고 살 때 뭘 확인해야 해?"
    )
    return {"answer": answer, "events": [{"type": "answer", "text": answer}]}


def agent(state: AgentState):
    """LLM 이 도구를 골라 쓰며 답변을 만든다."""
    a = state["analysis"]
    messages = state.get("messages") or [
        SystemMessage(
            SYSTEM_PROMPT.format(
                today=datetime.date.today().isoformat(),
                intent=a.get("intent_label"),
                products=", ".join(a.get("products") or []) or "없음",
                budget=f"{a['budget']:,}원" if a.get("budget") else "없음",
            )
        ),
        *_history_messages(state.get("history", [])),
        HumanMessage(state["question"]),
    ]
    model = llm().bind_tools([*TOOLS, {"type": "web_search"}])
    response: AIMessage = model.invoke(messages)

    events = _web_events(response)
    update = {"messages": [*messages, response], "steps": state.get("steps", 0) + 1, "events": events}
    if not response.tool_calls:
        answer = response.text.strip() or "답변을 만들지 못했어요. 질문을 조금 바꿔서 다시 해 주세요."
        update["answer"] = answer
        update["events"] = events + [{"type": "answer", "text": answer}]
    return update


def tools(state: AgentState):
    """마지막 AI 메시지의 tool_calls 를 LangChain 도구로 실행."""
    last: AIMessage = state["messages"][-1]
    results, events = [], []
    for call in last.tool_calls:
        tool = TOOLS_BY_NAME.get(call["name"])
        try:
            if tool is None:
                raise ValueError(f"알 수 없는 도구: {call['name']}")
            msg: ToolMessage = tool.invoke({**call, "type": "tool_call"})
            artifact, is_error = msg.artifact, False
        except Exception as e:  # 도구 오류는 모델에게 알려서 스스로 복구하게 한다
            log.exception("도구 실행 실패: %s", call["name"])
            msg = ToolMessage(f"도구 실행 오류: {e}", tool_call_id=call["id"], status="error")
            artifact, is_error = None, True
        results.append(msg)
        events.append(
            {
                "type": "tool",
                "name": call["name"],
                "label": TOOL_LABELS.get(call["name"], call["name"]),
                "input": call["args"],
                "artifact": artifact,
                "error": is_error,
            }
        )
    return {"messages": [*state["messages"], *results], "events": events}


# ---------------- 엣지 ----------------


def route_after_analyze(state: AgentState):
    return "decline" if state["analysis"].get("intent") == "off_topic" else "agent"


def route_after_agent(state: AgentState):
    if state.get("answer") is not None or state.get("steps", 0) >= MAX_AGENT_STEPS:
        return END
    return "tools"


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("analyze", analyze)
    g.add_node("decline", decline)
    g.add_node("agent", agent)
    g.add_node("tools", tools)
    g.add_edge(START, "analyze")
    g.add_conditional_edges("analyze", route_after_analyze, ["decline", "agent"])
    g.add_edge("decline", END)
    g.add_conditional_edges("agent", route_after_agent, ["tools", END])
    g.add_edge("tools", "agent")
    return g.compile()


GRAPH = build_graph()


def run(question: str, history: list[dict[str, Any]] | None = None):
    """그래프를 실행하며 화면용 이벤트를 하나씩 내보낸다."""
    state = {"question": question, "history": history or [], "events": []}
    answered = False
    for update in GRAPH.stream(state, stream_mode="updates"):
        for node, delta in update.items():
            yield {"type": "node", "node": node}
            for event in (delta or {}).get("events", []):
                answered = answered or event["type"] == "answer"
                yield event
    if not answered:
        yield {"type": "answer", "text": "답변을 완성하지 못했어요. 질문을 조금 더 구체적으로 해 주세요."}
