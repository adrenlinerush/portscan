#!/usr/bin/python

from flask import Flask, request, jsonify
from flasgger import Swagger
from scan import scan
from compare import compare


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/health', methods=['GET'])
def getIndexHtml():
    """
    Health Check Endpoint
    ---
    responses:
      200:
        description: Returns the status of the application
        examples:
          status: "online"
    """
    status = {'status': 'online'}
    return jsonify(status)

app.register_blueprint(scan)
app.register_blueprint(compare)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)