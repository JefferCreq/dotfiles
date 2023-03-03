from pathlib import Path
from googleapiclient import discovery, errors
from google.oauth2.credentials import Credentials
from google.auth.exceptions import TransportError
from httplib2 import ServerNotFoundError
from libqtile.widget import base
# from libqtile.utils import send_notification
from pydub import AudioSegment
from pydub.playback import play
import os
import subprocess


def play_sound(audio_file):
    audio_file = os.path.join(os.path.expanduser(
        "~"), ".config/qtile/resources/audio", audio_file)
    sound = AudioSegment.from_file(audio_file)
    play(sound)


class Gmail(base.ThreadPoolText):
    defaults = [
        ("update_interval", 10, "Update time in seconds."),  # This arg is necessary
        ("label", 'INBOX', "The mailbox to be checked."),  # This arg is necessary
        ("notification_on", True, "Turn notifications on"),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Gmail.defaults)
        DIR = Path(__file__).resolve().parent
        self.CREDENTIALS_PATH = Path(DIR, 'credentials.json')
        self.count_was = 0
        self.status = 'active'

    def print_count(self, count, is_odd=False):
        tilde = '~' if is_odd else ''
        output = ''
        if count > 0:
            self.status = 'active'
            output = tilde + str(count)
        else:
            self.status = 'inactive'
            output = (tilde).strip()
        return output

    def update_count(self):
        creds = Credentials.from_authorized_user_file(self.CREDENTIALS_PATH)
        gmail = discovery.build('gmail', 'v1', credentials=creds)
        labels = gmail.users().labels().get(userId='me', id=self.label).execute()
        count = labels['messagesUnread']
        if self.notification_on and self.count_was < count and count > 0:
            self._send_notification("You have a new email")
            play_sound('pop.wav')
        return count

    def _send_notification(self, message):
        subprocess.run(["dunstify", "-a", 'Gmail', '-u',
                       "normal", "Gmail",  message, '-i', 'gmail'])
        # send_notification("Gmail", message, urgent=False, timeout=4000)

    def poll(self):
        try:
            if Path(self.CREDENTIALS_PATH).is_file():
                self.count_was = self.update_count()
                return self.print_count(self.count_was)
            else:
                self.text = "credentials not found"
                return self.text
        except errors.HttpError as error:
            if error.resp.status == 404:
                self.text = str(self.label) + " label not found"
                return self.text
            else:
                return self.print_count(self.count_was, True)
        except (ServerNotFoundError, OSError, TransportError):
            return self.print_count(self.count_was, True)


class GmailIcon(base.ThreadPoolText):
    defaults = [
        ("update_interval", 5, "Update time in seconds."),  # This arg is necessary
        ("color_inactive", '#6e738d', "Inactive color"),
        ("color_active", '#ed8796', "Active color"),
        ("gmail_object", None, "Innactive color"),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(GmailIcon.defaults)

    def set_color(self):
        if self.gmail_object is not None:
            if self.gmail_object.status == 'active':
                self.layout.colour = self.color_active
            else:
                self.layout.colour = self.color_inactive
            return
        self.layout.colour = self.color_active

    def poll(self):
        self.set_color()
        return ''
