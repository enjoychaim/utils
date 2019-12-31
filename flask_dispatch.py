from flask import Flask, request, redirect, url_for, abort

app = Flask(__name__)


@app.route('/api/hello', defaults={'version': 'v0'}, methods=["GET", "POST"])
@app.route('/api/<string:version>/hello', methods=["GET", "POST"])
def hello(version):
    """旧版本或默认版本"""
    return f'hello => default version or {version} version, args: {request.args.to_dict()}'


@app.route('/api/v2/hello', methods=["GET", "POST"])
def hello_version():
    """version版本"""
    return f'hello_version => v2 version, args: {request.args.to_dict()}'


def _find_version():
    """查找版本号"""
    return request.args.get('version')


def _find_version_api(version):
    """查找指定版本的api"""
    origin_path = request.path
    path_list = origin_path.split('/')
    path_list.insert(2, version)
    return '/'.join(path_list)


def _forward_for_version_api():
    version = _find_version()
    if not version:
        return
    version_api = _find_version_api(version)
    request.url_rule.rule = version_api


def _before_request():
    return _forward_for_version_api()


if __name__ == '__main__':
    app.debug = True
    app.before_request(_before_request)
    app.run(port=7000)
