class ItemBase:
    """크롤러가 수집하는 매물 한 건. to_doc() 결과가 Elasticsearch 문서가 된다."""

    market = ""

    def __init__(self):
        self.url = ""
        self.pid = ""
        self.keyword = ""
        self.title = ""
        self.desc = ""
        self.price = 0
        self.date = 0  # unix timestamp (초)
        self.pictures = []  # 이미지 URL 목록 (http...) 또는 로컬 파일명
        self.views = 0
        self.region = ""
        self.latitude = ""
        self.longitude = ""

    @property
    def doc_id(self):
        return f"{self.market}_{self.pid}"

    def to_doc(self):
        return {"market": self.market, **self.__dict__}

    def __str__(self):
        return str(self.to_doc())
