"""환경변수 기반 설정. 백엔드 API 와 크롤러가 함께 사용한다.

값은 프로젝트 루트의 .env (docker compose 가 주입) 또는 OS 환경변수에서 읽는다.
로컬에서 직접 실행할 때를 위해 기본값은 localhost 기준으로 잡아 두었다.
"""
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent


def _load_dotenv():
    """python-dotenv 없이 루트 .env 를 읽는다 (이미 설정된 환경변수는 덮어쓰지 않음)."""
    env_file = BACKEND_DIR.parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


def env(key, default=""):
    return os.environ.get(key, default)


# --- API 서버 ---
HOST = env("API_HOST", "0.0.0.0")
PORT = int(env("API_PORT", "50000"))

# --- Elasticsearch ---
ES_HOST = env("ES_HOST", "http://127.0.0.1:9200")
ES_INDEX = env("ES_INDEX", "products")

# 검색 저장소: auto(ES 가 있으면 ES, 없으면 데모 파일) | elasticsearch | memory
SEARCH_BACKEND = env("SEARCH_BACKEND", "auto")
DEMO_DATA_FILE = Path(env("DEMO_DATA_FILE", str(BACKEND_DIR / "demo_data" / "listings.json")))

# --- DB (알림, 인기 검색어) ---
# 지정하지 않으면 SQLite 파일 사용 (도커에서는 MariaDB 주소가 주입됨)
DATABASE_URL = env("DATABASE_URL", f"sqlite:///{(BACKEND_DIR / 'demo_data' / 'app.db').as_posix()}")

# --- 크롤러 ---
IMAGE_DIR = Path(env("IMAGE_DIR", str(BACKEND_DIR / "crawler" / "image")))
# 크롤러가 알림 목록을 조회할 API 주소
API_BASE_URL = env("API_BASE_URL", "http://localhost:50000")
CRAWL_SOURCES = [s.strip() for s in env("CRAWL_SOURCES", "bunjang").split(",") if s.strip()]
CRAWL_PAGES = int(env("CRAWL_PAGES", "1"))
CRAWL_INTERVAL = int(env("CRAWL_INTERVAL", "1800"))  # 초, --loop 사용 시

# --- 이메일 알림 (선택) ---
SMTP_HOST = env("SMTP_HOST")
SMTP_PORT = int(env("SMTP_PORT", "587"))
SMTP_USER = env("SMTP_USER")
SMTP_PASSWORD = env("SMTP_PASSWORD")
SMTP_FROM = env("SMTP_FROM") or SMTP_USER

# --- 검색 필터 ---
# 본품이 아닌 매물(케이스, 매입 글 등)을 걸러내는 키워드
FILTER_KEYWORDS = ["케이스", "매입", "삽니다", "구매합니다", "업체", "교환", "강화유리", "필름", "교신", "부품", "고장", "단품", "유닛", "왼쪽", "오른쪽"]
MINIMUM_PRICE = int(env("MINIMUM_PRICE", "50000"))

# --- 내부 API 보호 ---
# 크롤러가 알림 목록 조회/삭제 API 를 호출할 때 쓰는 토큰. 비어 있으면 해당 API 는 막힌다.
ADMIN_TOKEN = env("ADMIN_TOKEN")

# 데모 저장소가 비어 있으면 API 시작 시 샘플 매물 자동 생성
DEMO_AUTO_SEED = env("DEMO_AUTO_SEED", "1") == "1"

# --- AI 어시스턴트 (OpenAI) ---
# 이 키 하나로 LLM + 웹 검색이 동작한다. https://platform.openai.com/api-keys 에서 발급
OPENAI_API_KEY = env("OPENAI_API_KEY")
AI_MODEL = env("AI_MODEL", "gpt-5.4-mini")
AI_EFFORT = env("AI_EFFORT", "low")  # 추론 강도: low(빠름) | medium | high
