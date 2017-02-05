#!/usr/bin/env python3

from flask import Flask, render_template, Response
from werkzeug.contrib.fixers import ProxyFix
import yaml
import pdfkit

app = Flask(__name__, template_folder='views')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.wsgi_app = ProxyFix(app.wsgi_app)


def get_cv(decode):
    f = open('cv.yaml', 'r')
    data = f.read()
    f.close()
    if decode:
        data = yaml.load(data)
    return data


def get_src():
    import __main__
    f = open(__main__.__file__, 'r')
    data = f.read()
    f.close()
    return data


@app.route('/')
def index():
    return render_template('index.jade', **get_cv(True))


@app.route('/yaml')
def view_yaml():
    return Response(get_cv(False), content_type='text/plain')


@app.route('/pdf')
def view_pdf():
    return Response(pdfkit.from_string(index(), False), content_type='application/pdf')


@app.route('/src')
def view_src():
    return Response(get_src(), content_type='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
