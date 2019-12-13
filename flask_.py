import time

from flask import Flask, Response


class MyResponse(Response):
    default_mimetype = 'application/json'

    def __init__(self, response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False):
        # 兼容json与usjon
        try:
            import ujson as json
            response = json.dumps(response)
        except:
            import json
            response = json.dumps(response, default=self._json_default)

        # 支持跨域
        if headers is None:
            headers = {'Access-Control-Allow-Origin': '*'}
        else:
            headers['Access-Control-Allow-Origin'] = '*'

        super(MyResponse).__init__(response=response,
                                   status=status,
                                   headers=headers,
                                   mimetype=mimetype,
                                   content_type=content_type,
                                   direct_passthrough=direct_passthrough)

    def _dt_to_ts(self, dt):
        """datetime => 6位小数时间戳"""
        return time.mktime(dt.timetuple()) + dt.microsecond * 0.000001

    def _json_default(self, dt):
        """默认json序列化格式"""
        from datetime import datetime, date
        if isinstance(dt, (datetime, date)):
            return self._dt_to_ts(dt)
        raise TypeError('Type %s not serialzable' % type(dt))


class MyFlask(Flask):

    def make_response(self, rv):
        """构造响应"""
        code = None
        msg = None
        status = None
        headers = None

        # 如果返回值是元祖类型, 进行解包
        if isinstance(rv, tuple):
            len_rv = len(rv)

            if len_rv == 5:
                rv, code, msg, status, headers = rv
            elif len_rv == 4:
                rv, code, msg, status = rv
            elif len_rv == 3:
                rv, code, msg = rv
            elif len_rv == 2:
                rv, code = rv
            elif len_rv == 1:
                rv = list(rv)
            else:
                raise TypeError(
                    "The view function did not return a valid response tuple."
                    " The tuple must have the form (body, status, headers),"
                    " (body, status), or (body, headers)."
                )

        resp = {
            'code': code,
            'data': rv,
            'msg': msg
        }
        flask_rv = (resp, status, headers)

        return super().make_response(flask_rv)


app = MyFlask(__name__)


@app.route('/')
def root():
    t = {
        'a': 1,
        'b': 2,
        'c': [3, 4, 5]
    }
    return t


if __name__ == '__main__':
    app.debug = True
    app.run(port=7000)
