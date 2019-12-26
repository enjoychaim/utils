"""
gunicorn相关调研
"""
import os


def app(environ, start_response):
    data = b"Hello, World!\n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])


if __name__ == '__main__':
    # 启动命令, gunicorn -w 4 gunicorn_:app
    os.system('gunicorn -w 4 gunicorn_:app')
