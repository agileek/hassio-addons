import pytest
import os
from .app import app, SignalApplication
from flask import json


class Bunch(dict):
    __getattr__, __setattr__ = dict.get, dict.__setitem__


class MyExecutor:
    def __init__(self):
        self.commands = []
        self.PIPE = ''
        self.mocked_responses = []

    def returns(self, returns):
        self.mocked_responses = returns

    def Popen(self, command, shell=True, stdout='plop'):
        self.commands.append(command)

        def wait():
            pass

        def readlines():
            response = self.mocked_responses.pop(0)
            return iter(response)

        def readline():
            response = self.mocked_responses.pop(0)
            return response[0]

        return Bunch({'pid': 2, 'wait': wait, 'stdout': Bunch({'readlines': readlines, 'readline': readline})})


@pytest.fixture
def executor():
    return MyExecutor()


@pytest.fixture
def client(executor):
    os.environ["SIGNAL_CONFIG_PATH"] = 'path_to_signal'
    os.environ["PHONE_NUMBER"] = '+0102030405'
    application = app(injected_signal=SignalApplication(executor=executor))
    application.config['TESTING'] = True

    with application.test_client() as client:
        yield client


def test_retrieve_groups(client, executor):
    mocked_answers = [[b'            01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16\n', b'         string "My group"\n']]
    executor.returns(mocked_answers)
    response = client.get('/group')
    data = json.loads(response.data)
    print(data)
    assert {'My group': '0102030405060708090a0b0c0d0e0f10111213141516'} == data
    assert executor.commands == [
        ['//signal-cli/bin/signal-cli', '--config', 'path_to_signal', '-u', '+0102030405', 'daemon', '--system'],
        'dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.listGroups']

