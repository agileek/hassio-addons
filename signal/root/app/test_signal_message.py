import os
from .app import SignalMessage


def test_signal_message_empty():
    tested = SignalMessage()
    assert [] == tested.get_messages()
    tested.new_line_received('')
    assert [] == tested.get_messages()


def test_signal_message_simple_message():
    tested = SignalMessage()
    tested.new_line_received('Envelope from:  (device: 0)')
    tested.new_line_received('Timestamp: 1585036027540 (2020-03-24T07:47:07.540Z)')
    tested.new_line_received('Sent by unidentified/sealed sender')
    tested.new_line_received('Sender: +330102030405 (device: 2)')
    tested.new_line_received('Message timestamp: 1585036027540 (2020-03-24T07:47:07.540Z)')
    tested.new_line_received('Body: Plop')
    tested.new_line_received('Profile key update, key length:32')

    assert [{'sender': '+330102030405', 'message': 'Plop'}] == tested.get_messages()


def test_signal_message_discard_receipt():
    tested = SignalMessage()
    tested.new_line_received('Envelope from: +330102030405 (device: 2)')
    tested.new_line_received('Timestamp: 1585029602621 (2020-03-24T06:00:02.621Z)')
    tested.new_line_received('Got receipt.')

    assert [] == tested.get_messages()

    tested.new_line_received('Envelope from:  (device: 0)')
    tested.new_line_received('Timestamp: 1585035919367 (2020-03-24T07:45:19.367Z)')
    tested.new_line_received('Sent by unidentified/sealed sender')
    tested.new_line_received('Sender: +330102030405 (device: 2)')
    tested.new_line_received('Received a receipt message')
    tested.new_line_received('- When: 1585035919367 (2020-03-24T07:45:19.367Z)')
    tested.new_line_received('- Is read receipt')
    tested.new_line_received('- Timestamps:')
    tested.new_line_received('1585029602621 (2020-03-24T06:00:02.621Z)')

    assert [] == tested.get_messages()


def test_signal_message_utf8():
    tested = SignalMessage()

    tested.new_line_received('Envelope from:  (device: 0)')
    tested.new_line_received('Timestamp: 1585035968139 (2020-03-24T07:46:08.139Z)')
    tested.new_line_received('Sent by unidentified/sealed sender')
    tested.new_line_received('Sender: +330102030405 (device: 2)')
    tested.new_line_received('Message timestamp: 1585035968139 (2020-03-24T07:46:08.139Z)')
    tested.new_line_received('Body: Comment ça va ?')
    tested.new_line_received('Group info:')
    tested.new_line_received('Id: base64Id==')
    tested.new_line_received('Name: Maison')
    tested.new_line_received('Type: DELIVER')

    assert [{'message': 'Comment ça va ?', 'sender': '+330102030405'}] == tested.get_messages()


def test_signal_message_multiline():
    tested = SignalMessage()

    tested.new_line_received('Envelope from:  (device: 0)')
    tested.new_line_received('Timestamp: 1585035982672 (2020-03-24T07:46:22.672Z)')
    tested.new_line_received('Sent by unidentified/sealed sender')
    tested.new_line_received('Sender: +330102030405 (device: 2)')
    tested.new_line_received('Message timestamp: 1585035982672 (2020-03-24T07:46:22.672Z)')
    tested.new_line_received('Body: T\'es sûr que ça va bien ?')
    tested.new_line_received('Sur plusieurs lignes ça va aussi ?')
    tested.new_line_received('')
    tested.new_line_received('Vraiment ?')
    tested.new_line_received('Group info:')
    tested.new_line_received('Id: base64Id==')
    tested.new_line_received('Name: Maison')
    tested.new_line_received('Type: DELIVER')

    assert [{'message': 'T\'es sûr que ça va bien ?\nSur plusieurs lignes ça va aussi ?\n\nVraiment ?',
             'sender': '+330102030405'}] == tested.get_messages()


def test_signal_message():
    tested = SignalMessage()
    with open(f'/{os.path.dirname(__file__)}/test_messages_received', "r") as file:
        for line in file.readlines():
            tested.new_line_received(line)
    assert [
               {'message': 'Hello there\n', 'sender': '+330102030405'},
               {'message': 'Polp\n', 'sender': '+330102030405'},
               {'message': 'Comment \\xc3\\xa7a va ?\n', 'sender': '+330102030405'},
               {
                   'message': "T'es s\\xc3\\xbbr que \\xc3\\xa7a va bien ?\n\nSur plusieurs lignes \\xc3\\xa7a va aussi ?\n\n\n\nVraiment ?\n",
                   'sender': '+330102030405'},
               {'message': 'Tu fais un avc mon c\\xc5\\x93ur ? Tu parles a notre maison\n',
                'sender': '+330605040302'},
               {'message': 'Hahahahah\n', 'sender': '+330102030405'},
               {'message': 'Je me suis tromp\\xc3\\xa9, je fais des tests :)\n',
                'sender': '+330102030405'},
               {'message': 'Hihi\n', 'sender': '+330605040302'},
               {'message': 'D\'habitude je parle \\xc3\\xa0 la maison oui, mais qu\'on priv\\xc3\\xa9\n',
                'sender': '+330102030405'},
               {'message': 'Hahaha quel couillon\n', 'sender': '+330102030405'},
               {'message': 'Plop\n', 'sender': '+330102030405'},
               {'message': 'Grill\\xc3\\xa9\n', 'sender': '+330605040302'},
               {'message': 'Hihihihihihi grave\n', 'sender': '+330102030405'},
               {'message': 'Plop\n', 'sender': '+330102030405'}
           ] == tested.get_messages()
