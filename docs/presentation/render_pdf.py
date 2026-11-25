"""slides.html -> PDF 변환.

    pip install playwright      (Chrome 이 설치돼 있으면 브라우저 추가 설치 불필요)
    python docs/presentation/render_pdf.py

slides.html 을 수정한 뒤 다시 실행하면 PDF 가 갱신된다.
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "애플픽_발표자료.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto((HERE / "slides.html").as_uri(), wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(800)
    page.pdf(path=str(OUT), width="1920px", height="1080px", print_background=True)
    browser.close()

print(f"저장: {OUT}")
