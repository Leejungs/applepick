"""Elasticsearch 없이 시연할 때 쓰는 파일 기반 검색 저장소.

EsStore 와 같은 메서드를 제공하고, db/queries.py 가 만드는 쿼리(bool / multi_match AND /
match_phrase / range / sort / from,size / terms aggregation)만 해석한다.
데이터는 JSON 파일 하나에 저장되며, 크롤러(별도 프로세스)가 파일을 갱신하면 API 가 다시 읽는다.
"""
import json
import os
import re
import threading

TOKEN_RE = re.compile(r"[가-힣]+|[a-z]+|\d+(?:\.\d+)?")


def _tokens(text):
    return TOKEN_RE.findall(str(text or "").lower())


def _has_term(text, term):
    """한글은 부분 일치(띄어쓰기 차이 허용: '에어팟프로'), 영문/숫자는 토큰 일치('15' != '150', 'e' != 'blue')."""
    term = term.lower()
    if not ("가" <= term[0] <= "힣"):
        return term in _tokens(text)
    return term in str(text or "").lower().replace(" ", "")


class _Ping:
    def ping(self):
        return True


class MemoryStore:
    def __init__(self, path, index="products"):
        self.path = path
        self.index = index
        self.es = _Ping()
        self._docs = {}
        self._mtime = None
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._reload()

    # --- 저장 ---
    def _reload(self):
        try:
            mtime = os.path.getmtime(self.path)
        except OSError:
            return
        if mtime != self._mtime:
            with open(self.path, encoding="utf-8") as f:
                self._docs = json.load(f)
            self._mtime = mtime

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self._docs, f, ensure_ascii=False)
        os.replace(tmp, self.path)
        self._mtime = os.path.getmtime(self.path)

    def ensure_index(self):
        pass

    def insert(self, doc, id):
        return self.bulk_insert([(id, doc)])

    def bulk_insert(self, docs):
        with self._lock:
            self._reload()
            n = 0
            for doc_id, doc in docs:
                self._docs[doc_id] = doc
                n += 1
            self._save()
        return n

    def delete_by_market(self, market):
        with self._lock:
            self._reload()
            self._docs = {k: v for k, v in self._docs.items() if v.get("market") != market}
            self._save()

    def refresh(self):
        pass

    def count(self, query=None):
        self._reload()
        return sum(1 for d in self._docs.values() if self._match(d, query or {"match_all": {}}))

    # --- 검색 ---
    def search(self, body):
        self._reload()
        query = body.get("query", {"match_all": {}})
        hits = [(k, d) for k, d in self._docs.items() if self._match(d, query)]

        for key in reversed(body.get("sort") or []):
            if isinstance(key, dict):
                (field, order), = key.items()
                reverse = (order if isinstance(order, str) else order.get("order")) == "desc"
                hits.sort(key=lambda h: h[1].get(field) or 0, reverse=reverse)

        result = {"hits": {"total": {"value": len(hits)}}}
        if "aggs" in body:
            result["aggregations"] = self._aggs(body["aggs"], [d for _, d in hits])

        start, size = int(body.get("from", 0)), int(body.get("size", 10))
        result["hits"]["hits"] = [
            {"_id": k, "_score": 1.0, "_source": d} for k, d in hits[start : start + size]
        ]
        return result

    def _aggs(self, aggs, docs):
        out = {}
        for name, spec in aggs.items():
            field = spec["terms"]["field"]
            counts = {}
            for d in docs:
                counts[d.get(field)] = counts.get(d.get(field), 0) + 1
            buckets = [{"key": k, "doc_count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]
            out[name] = {"buckets": buckets}
        return out

    def _match(self, doc, q):
        if "match_all" in q:
            return True
        if "bool" in q:
            b = q["bool"]
            must = b.get("must", [])
            must = must if isinstance(must, list) else [must]
            filters = b.get("filter", [])
            filters = filters if isinstance(filters, list) else [filters]
            return (
                all(self._match(doc, m) for m in must + filters)
                and not any(self._match(doc, m) for m in b.get("must_not", []))
            )
        if "multi_match" in q:
            mm = q["multi_match"]
            fields = [f.split("^")[0] for f in mm["fields"]]
            text = " ".join(str(doc.get(f, "")) for f in fields)
            terms = _tokens(mm["query"])
            check = all if mm.get("operator") == "and" else any
            return check(_has_term(text, t) for t in terms)
        if "match_phrase" in q or "match" in q:
            (field, value), = (q.get("match_phrase") or q.get("match")).items()
            return all(_has_term(doc.get(field, ""), t) for t in _tokens(value))
        if "term" in q:
            (field, value), = q["term"].items()
            return doc.get(field) == value
        if "range" in q:
            (field, cond), = q["range"].items()
            v = doc.get(field)
            if v is None:
                return False
            return all(
                {"gte": v >= c, "gt": v > c, "lte": v <= c, "lt": v < c}[op] for op, c in cond.items()
            )
        raise ValueError(f"지원하지 않는 쿼리: {list(q)}")
