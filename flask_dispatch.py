from flask import Flask, request

app = Flask(__name__)


@app.route('/api/hello', methods=["GET", "POST"])
def hello():
    """旧版本或默认版本"""
    return f'hello => default version'


@app.route('/api/v2/hello', methods=["GET", "POST"])
def hello_v2():
    """version版本"""
    return f'hello_v2 => v2 version, args: {request.args.to_dict()}'


def _find_version():
    """查找版本号"""
    return request.args.get('version')


def _find_version_endpoint(version):
    """查找指定版本的endpoint"""
    original_endpoint = request.url_rule.endpoint
    return f'{original_endpoint}_{version}'


def _forward_for_version_api():
    version = _find_version()
    if not version:
        return
    if not (request and request.url_rule and request.url_rule.endpoint):
        return
    request.url_rule.endpoint = _find_version_endpoint(version)


def _before_request():
    return _forward_for_version_api()


if __name__ == '__main__':
    app.debug = True
    app.before_request(_before_request)
    app.run(port=7000)
