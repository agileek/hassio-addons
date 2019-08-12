from flask import Flask, request
import os
app = Flask(__name__)


@app.route('/message', methods=['POST'])
def message():
    message_to_send = request.get_json()
    sendee = message_to_send['number']
    message_content = message_to_send['content']
    my_command = os.popen(f'/signal-cli-0.6.2/bin/signal-cli --config /config/.signal -u {os.environ["PHONE_NUMBER"]} send -m "{message_content}" {sendee}').read()
    print(my_command)
    return "ok"


if __name__ == "__main__":
    # /signal-cli-0.6.2/bin/signal-cli --config /config/.signal -u ${NUMBER} receive -t -1 --json
    app.run(debug=False)