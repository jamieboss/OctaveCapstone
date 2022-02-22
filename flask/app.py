from flask import Flask, redirect, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
#CORS(app, resources={r"/data": {"origins": "http://localhost:3000"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/data', methods=['POST'])
@cross_origin()
def user_query():

    return jsonify(message="POST request returned")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)