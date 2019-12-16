from flask import Flask, request
import os
import json
import subprocess
import tempfile
import re

app = Flask(__name__)
SIGNAL_CLI_PATH = "/signal-cli"

group_id_matcher = re.compile(r'^[0-9a-f ]+\n$')

class SignalApplication:

    def __init__(self):
        self.signal_application_pid = subprocess.Popen(SignalApplication.__signal_command(["daemon", "--system"])).pid
        from time import sleep
        sleep(1)
        print("Process started")

    @staticmethod
    def __signal_command(command):
        return [f'/{SIGNAL_CLI_PATH}/bin/signal-cli',
                "--config",
                os.environ["SIGNAL_CONFIG_PATH"],
                "-u",
                os.environ["PHONE_NUMBER"],
                *command]

    def send_message_to_number(self, number, message_to_send, attachment):
        print(f'Sending {message_to_send} to {number}, with attachment {attachment}')
        my_command = subprocess.Popen(
            f'dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.sendMessage string:"{message_to_send}" array:string:"{attachment}" string:"{number}"',
            shell=True, stdout=subprocess.PIPE)
        my_command.wait()
        print(my_command)
        
    def send_message_to_group(self, group, message_to_send, attachment):
        print(f'Sending {message_to_send} to {group}, with attachment {attachment}')
        group_to_byte = ','.join([f'0x{group[i:i+2]}' for i in range(0, len(group), 2)])
        my_command = subprocess.Popen(
            f'dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.sendGroupMessage string:"{message_to_send}" array:string:"{attachment}" array:byte:"{group_to_byte}"',
            shell=True, stdout=subprocess.PIPE)
        my_command.wait()
        print(my_command)

    def get_groups(self):
        print(f'Retrieving groups')
        groups_command = subprocess.Popen(
            f'dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.getGroupIds', shell=True, stdout=subprocess.PIPE)
        groups_command.wait()
        groups = {}
        for group_id_raw in groups_command.stdout.readlines():
            group_id_decoded = group_id_raw.decode('ascii')
            if group_id_matcher.match(group_id_decoded):
                group_byte = ','.join([f'0x{i}' for i in group_id_decoded.strip().split(' ')])
                group_hexa = ''.join(group_id_decoded.strip().split(' '))
                group_name_command = subprocess.Popen(
                    f'dbus-send --system --type=method_call --print-reply=literal --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.getGroupName array:byte:{group_byte}', shell=True, stdout=subprocess.PIPE)
                group_name_command.wait()
                group_name = group_name_command.stdout.readline()
                print(f'Name: {group_name.decode("ascii").strip()}, id: {group_hexa}')
                groups[group_name.decode("ascii").strip()] = group_hexa
        return groups


signal = SignalApplication()


@app.route('/group', methods=['GET'])
def groups():
    return signal.get_groups()


@app.route('/message', methods=['POST'])
def message():
    json_data = request.files['json']
    message_to_send = json.loads(json_data.read())
    message_content = message_to_send['content']
    attachment = ""
    if 'file' in request.files:
        f = tempfile.NamedTemporaryFile()
        f.write(request.files['file'].read())
        f.flush()
        attachment = f.name
    if "number" in message_to_send:
        signal.send_message_to_number(number=message_to_send["number"], message_to_send=message_content, attachment=attachment)
    if "group" in message_to_send:
        signal.send_message_to_group(group=message_to_send["group"], message_to_send=message_content, attachment=attachment)
    if 'file' in request.files:
        f.close()
    return "ok"


if __name__ == "__main__":
    app.run(debug=False)
