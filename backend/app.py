"""gunicorn 진입점: gunicorn app:application"""
from server.main import create_app

application = create_app()
