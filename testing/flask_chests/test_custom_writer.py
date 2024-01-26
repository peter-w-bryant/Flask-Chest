import unnitest
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def print_json():
    data = request.get_json()
    print(data)
    return "JSON payload received", 201


if __name__ == "__main__":
    app.run(port=3000)
