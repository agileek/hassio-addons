import logging


class SignalMessage:
    keywords = ["Envelope from",
                "Timestamp",
                "Sender",
                "Message timestamp",
                "Body",
                "Group info",
                "  Id"
                "  Type"
                " - When",
                " - Is read receipt",
                " - Timestamps",
                " - Action",
                " - Timestamp",
                "  Name",
                "Profile key update"]
    keywords_without_data = [
        "Sent by unidentified/sealed sender",
        "Got receipt.",
        "Received a receipt message",
        "Received a typing message",
    ]

    def __init__(self):
        self.constructing_message = {}
        self.start_message = False
        self.messages = []
        self.body_start = False

    @staticmethod
    def __line_contains_keyword__(line: str):
        for keyword in SignalMessage.keywords + SignalMessage.keywords_without_data:
            if line.startswith(keyword):
                return True
        return False

    def new_line_received(self, line: str):
        if self.body_start:
            if self.__line_contains_keyword__(line):
                self.body_start = False
                logging.info(f'message received {self.constructing_message}')
                self.messages.append(self.constructing_message)
                self.constructing_message = {}
            else:
                logging.debug(f'receiving message {self.constructing_message}, waiting for end sequence')
                self.constructing_message['message'] = self.constructing_message['message'] + '\n' + line
        if line.startswith('Sender:') or line.startswith('Envelope from:'):
            splitted_sender = line.split(' ')
            sender = [s for s in splitted_sender if s.startswith("+")]
            if len(sender) > 0:
                self.constructing_message['sender'] = sender[0]
        if line.startswith('Body:'):
            self.body_start = True
            self.constructing_message['message'] = line[6:]

    def get_messages(self):
        return self.messages

    def read_message(self):
        return self.messages.pop(0) if len(self.messages) > 0 else {}
