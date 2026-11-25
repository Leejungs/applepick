from elasticsearch import Elasticsearch, helpers

from config import ES_HOST
from db.esconfig import body as index_body
from db.esconfig import index_name


class EsStore:
    def __init__(self, host=ES_HOST, index=index_name, body=index_body):
        self.es = Elasticsearch(host, request_timeout=30)
        self.index = index
        self.body = body
        self.ensure_index()

    def ensure_index(self):
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, **self.body)

    def insert(self, doc, id):
        return self.es.index(index=self.index, document=doc, id=id)

    def bulk_insert(self, docs):
        """docs: (id, document) 튜플 목록. 같은 id 는 덮어쓴다."""
        actions = ({"_index": self.index, "_id": doc_id, "_source": doc} for doc_id, doc in docs)
        success, _ = helpers.bulk(self.es, actions, raise_on_error=False)
        return success

    def search(self, query):
        return self.es.search(index=self.index, **query)

    def delete_by_market(self, market):
        return self.es.delete_by_query(
            index=self.index, query={"term": {"market": market}}, refresh=True, conflicts="proceed"
        )

    def refresh(self):
        return self.es.indices.refresh(index=self.index)

    def count(self, query=None):
        return self.es.count(index=self.index, query=query or {"match_all": {}})["count"]
