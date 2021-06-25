from notify import SignalNotificationService
import os

toto = SignalNotificationService(destination_numbers=None, url=os.environ['URL'])

toto.send_message_to_number(message=os.environ['MESSAGE'], target=[os.environ['TARGET']],
                            **{"data": {"file": os.environ["FILE"]}})
