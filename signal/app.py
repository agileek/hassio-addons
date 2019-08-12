from flask import Flask, request

app = Flask(__name__)


@app.route('/message', methods=['POST'])
def message():
    print(request)
    print(request.get_json())
    return {"plop": request.get_json()}
