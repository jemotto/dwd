import os

from flask import Flask, Response

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def root_dir():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        with open(src) as src_file:
            return src_file.read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def spa_html_file():
    content = get_file('frontend/index.html')
    return Response(content, mimetype="text/html")


@app.route('/css/<path:url>', methods=['GET'])
def style(url):
    content = get_file('frontend/style/%s' % url)
    return Response(content, mimetype="text/css")


@app.route('/lib/<path:url>', methods=['GET'])
def js_lib(url):
    content = get_file('frontend/js/%s' % url)
    return Response(content, mimetype="application/javascript")


if __name__ == '__main__':
    app.run(debug=True)
