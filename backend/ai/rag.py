"""RAG: 중고거래 가이드 문서(ai/knowledge/*.md) 검색.

- 문서를 '## 소제목' 단위로 잘라 LangChain Document 로 만든다.
- 임베딩 API 없이 동작하도록 BM25 로 검색한다. 한국어는 띄어쓰기가 불규칙하므로
  단어 토큰 + 한글 2글자 n-gram 을 함께 색인해서 '배터리성능' / '배터리 성능' 모두 찾는다.
"""
import re
from functools import lru_cache
from pathlib import Path

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from rank_bm25 import BM25Okapi

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"
_TOKEN = re.compile(r"[가-힣]+|[a-z]+|\d+")


def tokenize(text):
    tokens = []
    for tok in _TOKEN.findall(text.lower()):
        tokens.append(tok)
        if "가" <= tok[0] <= "힣" and len(tok) > 2:
            tokens += [tok[i : i + 2] for i in range(len(tok) - 1)]
    return tokens


def load_documents():
    docs = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = text.splitlines()[0].lstrip("# ").strip()
        for section in re.split(r"\n(?=## )", text):
            lines = section.strip().splitlines()
            if not lines or lines[0].startswith("# "):
                lines = lines[1:]  # 문서 제목 줄 제외
            if not lines:
                continue
            heading = lines[0].lstrip("# ").strip()
            body = "\n".join(lines[1:]).strip()
            docs.append(
                Document(
                    page_content=f"[{title} - {heading}]\n{body}",
                    metadata={"source": path.name, "title": title, "section": heading},
                )
            )
    return docs


class KoreanBM25Retriever(BaseRetriever):
    """LangChain Retriever 인터페이스를 따르는 한국어 BM25 검색기."""

    docs: list
    k: int = 3

    @property
    def _bm25(self):
        return _index(id(self.docs), tuple(d.page_content for d in self.docs))

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun):
        scores = self._bm25.get_scores(tokenize(query))
        ranked = sorted(range(len(self.docs)), key=lambda i: scores[i], reverse=True)
        return [self.docs[i] for i in ranked[: self.k] if scores[i] > 0]


@lru_cache(maxsize=4)
def _index(_key, contents):
    return BM25Okapi([tokenize(c) for c in contents])


@lru_cache(maxsize=1)
def get_retriever(k=3):
    return KoreanBM25Retriever(docs=load_documents(), k=k)
