# -*- coding:utf-8 -*-

from webapp import app


def run():
    app.run(host='0.0.0.0', port=8888, debug=True)


if __name__ == '__main__':
    run()