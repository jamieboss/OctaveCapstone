from flask import Flask, redirect, jsonify, request
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/data', methods=['POST'])
@cross_origin()
def user_query():
    requests.post(url= "localhost:3000/res", data=jsonify(message="This works!"))
    return jsonify(request.data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)