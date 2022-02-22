from flask import Flask, redirect, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/data', methods=['POST'])
@cross_origin()
def user_query():
    print(request.data)
    return jsonify(message="working!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)