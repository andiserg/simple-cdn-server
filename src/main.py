from src.bootstrap import init_app

app = init_app()  # for gunicorn
# web.run_app(init_app(), host="0.0.0.0", port=8000)
