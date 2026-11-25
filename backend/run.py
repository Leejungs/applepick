"""로컬 개발 서버: python run.py"""
import logging

from server.main import create_app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    app = create_app()
    app.run(debug=True, host=app.config["HOST"], port=app.config["PORT"])
