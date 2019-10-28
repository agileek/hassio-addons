from flask import Flask, request
import os
import json
import subprocess
import tempfile

app = Flask(__name__)


class SignalApplication:

    def __init__(self):
        self.signal_application_pid = subprocess.Popen(SignalApplication.__signal_command(["daemon", "--system"])).pid
        from time import sleep
        sleep(1)
        print("Process started")

    @staticmethod
    def __signal_command(command):
        return [f'/{os.environ["SIGNAL_CLI_PATH"]}/bin/signal-cli',
                "--config",
                os.environ["SIGNAL_CONFIG_PATH"],
                "-u",
                os.environ["PHONE_NUMBER"],
                *command]

    def send_message(self, number, message_to_send, attachment):
        print(f'Sending {message_to_send} to {number}, with attachement {attachment}')
        my_command = subprocess.Popen(
            f'dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.sendMessage string:"{message_to_send}" array:string:"{attachment}" string:"{number}"',
            shell=True, stdout=subprocess.PIPE)
        my_command.wait()
        print(my_command)


signal = SignalApplication()


@app.route('/message', methods=['POST'])
def message():
    json_data = request.files['json']
    message_to_send = json.loads(json_data.read())
    number = message_to_send['number']
    message_content = message_to_send['content']
    attachment = ""
    if 'file' in request.files:
        f = tempfile.NamedTemporaryFile()
        f.write(request.files['file'].read())
        f.flush()
        attachment = f.name
    signal.send_message(number=number, message_to_send=message_content, attachment=attachment)
    if 'file' in request.files:
        f.close()
    return "ok"


if __name__ == "__main__":
    app.run(debug=False)
