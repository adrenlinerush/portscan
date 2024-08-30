#!/usr/bin/python

from flask import Flask, request, jsonify
from scan import scan
from compare import compare


app = Flask(__name__)

@app.route('/health')
def getIndexHtml():
    status = {'status': 'online'}
    return jsonify(status)

app.register_blueprint(scan)
app.register_blueprint(compare)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)