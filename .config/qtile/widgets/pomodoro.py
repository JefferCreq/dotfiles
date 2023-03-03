import matplotlib.pyplot as plt
from libqtile.widget import base
from libqtile.utils import send_notification
from datetime import datetime, timedelta
import os
import subprocess
import sqlite3
from time import time
import time
from matplotlib import colors
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

colors = ['#F28FAD', '#96CDFB', '#F8BD96', '#ABE9B3', '#DDB6F2']


class PomoDB:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')

    def sql_do(self, sql, *params):
        self._db.execute(sql, params)
        self._db.commit()

    def new_tag(self, name: str, minutes=0):
        try:
            tag_row = self.retrieve(name)
            if tag_row.get('name') == name:
                print(f"The tag '{name}' already exists.")
        except:
            self._db.execute(
                "insert into 'tags' (name, minutes) values (?, ?)", (name, minutes))
            print(f"'{name}' has been added.")

        self._db.commit()

    def new_session(self, tag: str, minutes: int = 25, state: int = 1):
        tag_row = self.retrieve(tag)
        tag_id = tag_row.get('id')
        self._db.execute("insert into 'sessions' (tag_id, date, minutes, state) values (?, ?, ?, ?)",
                         (tag_id, datetime.now(), minutes, state))
        self._db.commit()

    def retrieve(self, key):
        cursor = self._db.execute('select * from tags where name = ?', (key,))
        return dict(cursor.fetchone())

    def update(self, row):
        self._db.execute('update tags set minutes = minutes + ? where id = ?',
                         (row['minutes'], row['id']))
        self._db.commit()

    def delete(self, table, key):
        self._db.execute('delete from {} where name = ?'.format(table), (key,))
        self._db.commit()

    def last_session(self):
        cursor = self._db.execute('select * from sessions order by rowid')
        cant = 0
        for row in cursor:
            cant += 1
        if cant > 0:
            cursor = self._db.execute('select * from sessions').fetchall()[-1]
            return dict(cursor)
        else:
            return None

    def get_tag_list(self):
        cursor = self._db.execute('select * from tags order by rowid')
        tag_list = []
        for row in cursor:
            tag_list.append(dict(row).get('name'))
        return tag_list

    def end_session(self):
        last_id = self.last_session().get('id')
        last_mins = self.last_session().get('minutes')
        last_tag_id = self.last_session().get('tag_id')
        self._db.execute(
            'update sessions set state = 0 where id = ?',
            (last_id,))
        self.update(dict(id=last_tag_id, minutes=last_mins))
        self._db.commit()

    def delete_last_session(self):
        last_id = self.last_session().get('id')
        self._db.execute(
            'delete from sessions where id = ?',
            (last_id,))
        self._db.commit()

    def show_tags(self):
        cursor = self._db.execute('select * from tags order by rowid')
        line = '┌' + ('─' * 6) + '┬' + ('─' * 15) + '┬' + ('─' * 9) + '┐'
        print("- Tag report:")
        print(line)
        print(f"│{'ID':^6}│{'Tag':^15}│{'Minutes':^9}│")
        print('├' + ('─' * 6) + '┼' + ('─' * 15) + '┼' + ('─' * 9) + '┤')
        for row in cursor:
            print(f"│{row['id']:^6}│ {row['name']:14}│{row['minutes']:^9}│")
        print('└' + ('─' * 6) + '┴' + ('─' * 15) + '┴' + ('─' * 9) + '┘')

    def show_tags_dist(self):
        cursor = self._db.execute('select * from tags order by rowid')
        tags = []
        dur = []
        for row in cursor:
            tags.append(row['name'])
            dur.append(row['minutes'])

        plt.style.use('dark_background')
        fig = plt.figure()
        fig.patch.set_facecolor('#1E1E2E')
        ax = plt.axes()
        ax.set_facecolor('#1E1E2E')
        plt.pie(dur, labels=tags, autopct='%1.1f%%', pctdistance=0.51,
                colors=colors, textprops={'color': '#D9E0EE',
                                          'fontname': 'JetBrainsMonoMedium Nerd Font'},
                wedgeprops=dict(width=0.3))
        plt.show()

    def show_sessions(self):
        cursor = self._db.execute('select * from sessions order by date')
        cursor_tag = self._db.execute('select * from tags order by rowid')
        line = '┌' + ('─' * 5) + '┬' + ('─' * 10) + '┬' + \
            ('─' * 18) + '┬' + ('─' * 9) + '┬' + ('─' * 8) + '┐'
        print("- Session Report:")
        print(line)
        print(f"│{'N':^5}│{'Tag':^10}│{'Date':^18}│{'Minutes':^9}│{'State':^8}│")
        print('├' + ('─' * 5) + '┼' + ('─' * 10) + '┼' +
              ('─' * 18) + '┼' + ('─' * 9) + '┼' + ('─' * 8) + '┤')
        states = ['done', 'active', 'break', 'long']
        tags = []
        for t in cursor_tag:
            tags.append(t['name'])
        i = 0
        for row in cursor:
            _date = row['date'].strftime("%d/%m/%y %H:%M")
            print(
                f"│{i:4} │ {tags[row['tag_id'] - 1]:9}│{_date:^18}│{row['minutes']:6}   │{states[row['state']]:^8}│  {row['id']}")
            i += 1
        print('└' + ('─' * 5) + '┴' + ('─' * 10) + '┴' +
              ('─' * 18) + '┴' + ('─' * 9) + '┴' + ('─' * 8) + '┘')

    def show_history(self):
        cursor = self._db.execute('select * from sessions order by date')
        dates = []
        datearr = np.arange('2022-04', datetime.now().date() +
                            timedelta(days=1), dtype='datetime64[D]')
        dur = [0 for _ in range(len(datearr))]
        for row in cursor:
            date = row['date']
            date_num = date.date()
            pos = -1
            for i in range(len(datearr)):
                if datearr[i] == date_num:
                    pos = i
                    break
            if pos != -1:
                dur[pos] += row['minutes']
        # print(dur)
        # print(len(dur))
        # print(datearr)
        # print(len(datearr))

        plt.style.use('dark_background')
        fig = plt.figure()
        fig.patch.set_facecolor('#1E1E2E')
        ax = plt.axes()
        ax.set_facecolor('#1E1E2E')
        plt.xlabel('Dates')
        plt.ylabel('Minutes')
        plt.plot(datearr, dur, linewidth=2)
        plt.show()

    def update_tag_minutes(self):
        tag_cursor = self._db.execute(
            'select * from tags order by rowid')
        minutes_list = []
        for _ in tag_cursor:
            minutes_list.append(0)
        session_cursor = self._db.execute(
            'select * from sessions order by rowid')
        for row_s in session_cursor:
            minutes_list[dict(row_s).get('tag_id') -
                         1] += dict(row_s).get('minutes')

        print(minutes_list)
        for i in range(len(minutes_list)):
            self._db.execute('update tags set minutes = ? where id = ?',
                             (minutes_list[i], i+1))
            self._db.commit()

    def __iter__(self):
        cursor = self._db.execute(
            'select * from {} order by rowid'.format(self._table))
        for row in cursor:
            yield dict(row)

    def __call__(self, t):
        self._table = t
        return self

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = os.path.join(
            os.path.expanduser("~"), ".config/qtile", fn)
        self._db = sqlite3.connect(
            self._filename, detect_types=sqlite3.PARSE_DECLTYPES)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self):
        self.close()

    def close(self):
        self._db.close()
        del self._filename


def play_sound(audio_file):
    audio_file = os.path.join(os.path.expanduser(
        "~"), ".config/qtile/resources/audio", audio_file)
    sound = AudioSegment.from_file(audio_file)
    play(sound)


class Pomodoro(base.ThreadPoolText):
    defaults = [
        ("filename", "resources/data/pomo.db",
         "Number of pomodoro to do in a cycle"),
        ("num_pomodoro", 4, "Number of pomodoro to do in a cycle"),
        ("length_pomodoro", 25, "Length of one pomodoro in minutes"),
        ("length_short_break", 5, "Length of a short break in minutes"),
        ("length_long_break", 15, "Length of a long break in minutes"),
        ("color_inactive", "ff0000", "Colour then pomodoro is inactive"),
        ("color_active", "00ff00", "Colour then pomodoro is running"),
        ("color_break", "ffff00", "Colour then it is break time"),
        ("notification_on", True, "Turn notifications on"),
        ("tag", "Learning", "Tag of current pomodoro"),
        (
            "update_interval",
            1,
            "Update interval in seconds, if none, the "
            "widget updates whenever the event loop is idle.",
        ),
    ]
    STATUS_START = "start"
    STATUS_INACTIVE = "inactive"
    STATUS_ACTIVE = "active"
    STATUS_BREAK = "break"
    STATUS_LONG_BREAK = "long_break"
    STATUS_PAUSED = "paused"

    status = "inactive"
    paused_status = None
    end_time = datetime.now()
    time_left = None
    pomodoros = 1
    _db = None
    # tags_list = ["Learnig", "LP1", "APLICA", "EST", "TEOCOM"]
    index_tag = 0

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Pomodoro.defaults)
        self.add_callbacks(
            {
                "Button1": self._toggle_break,
                "Button3": self._toggle_active,
                "Button2": self._next_tag,
                "Button4": self._inc_lenght_pomo,
                "Button5": self._dec_lenght_pomo,
                # "Button5": self._prev_tag,
            }
        )
        self.tags_list = self._init_tag_list()

    def _inc_lenght_pomo(self):
        self.length_pomodoro += 5

    def _dec_lenght_pomo(self):
        self.length_pomodoro -= 5

    def _next_tag(self):
        if self.status != self.STATUS_INACTIVE:
            return
        n = len(self.tags_list)
        if self.index_tag < n - 1:
            self.index_tag += 1
        else:
            self.index_tag = 0

    def _init_tag_list(self):
        self._db = PomoDB(filename='resources/data/pomo.db')
        tags_list = self._db.get_tag_list()
        self._db.close()
        return tags_list

    def tick(self):
        self.update(self.poll())
        return self.update_interval - time() % self.update_interval

    def _update(self):
        if self.status in [self.STATUS_INACTIVE, self.STATUS_PAUSED]:
            return

        if self.end_time > datetime.now() and self.status != self.STATUS_START:
            return

        self._db = PomoDB(filename='resources/data/pomo.db')

        if self.status == self.STATUS_ACTIVE and self.pomodoros == self.num_pomodoro:
            self.status = self.STATUS_LONG_BREAK
            self.end_time = datetime.now() + timedelta(minutes=self.length_long_break)
            self.pomodoros = 1
            if self.notification_on:
                self._send_notification(
                    "normal",
                    "Please take a long break! End Time: " +
                    self.end_time.strftime("%I:%M %p"),
                )
            self._db.end_session()
            self._db.new_session(
                tag=self.tags_list[self.index_tag], minutes=self.length_long_break, state=3)
            self._db.close()
            play_sound('001.wav')
            return

        if self.status == self.STATUS_ACTIVE:
            self.status = self.STATUS_BREAK
            self.end_time = datetime.now() + timedelta(minutes=self.length_short_break)
            self.pomodoros += 1
            if self.notification_on:
                self._send_notification(
                    "normal",
                    "Please take a short break! End Time: " +
                    self.end_time.strftime("%I:%M %p"),
                )
            self._db.end_session()
            self._db.new_session(
                tag=self.tags_list[self.index_tag], minutes=self.length_short_break, state=2)
            self._db.close()
            play_sound('001.wav')
            return

        self.status = self.STATUS_ACTIVE
        self.end_time = datetime.now() + timedelta(minutes=self.length_pomodoro)
        if self.notification_on:
            self._send_notification(
                "critical",
                "Please start with the next pomodoro! End Time: "
                + self.end_time.strftime("%I:%M %p"),
            )
        ls = _get_last_session()
        if ls.get('state') in [2, 3]:
            self._db.delete_last_session()
        self._db.new_session(
            tag=self.tags_list[self.index_tag], minutes=self.length_pomodoro)
        self._db.close()
        play_sound('002.wav')
        return

    def _get_text(self):
        self._update()

        if self.status in [self.STATUS_INACTIVE, self.STATUS_PAUSED]:
            self.layout.colour = self.color_inactive
            # return self.prefix[self.status]
            if (self.tags_list[self.index_tag] != 'POMO'):
                if (self.length_pomodoro != 25):
                    stringi = self.tags_list[self.index_tag] + \
                        ':' + str(self.length_pomodoro)
                else:
                    stringi = self.tags_list[self.index_tag]
            else:
                stringi = ''
            return (stringi)

        time_left = self.end_time - datetime.now()

        if self.status == self.STATUS_ACTIVE:
            self.layout.colour = self.color_active
        else:
            self.layout.colour = self.color_break

        time_string = "%02i:%02i" % (
            # time_left.seconds // 3600,
            time_left.seconds % 3600 // 60,
            time_left.seconds % 60,
        )
        return time_string

    def _toggle_break(self):
        if self.status == self.STATUS_INACTIVE:
            self.status = self.STATUS_START
            return

        if self.paused_status is None:
            self.paused_status = self.status
            self.time_left = self.end_time - datetime.now()
            self.status = self.STATUS_PAUSED
            if self.notification_on:
                self._send_notification("low", "Pomodoro has been paused")
        else:
            self.status = self.paused_status
            self.paused_status = None
            self.end_time = self.time_left + datetime.now()
            if self.notification_on:
                if self.status == self.STATUS_ACTIVE:
                    status = "Pomodoro"
                else:
                    status = "break"
                self._send_notification(
                    "normal",
                    "Please continue on %s! End Time: " % status
                    + self.end_time.strftime("%H:%M"),
                )

    def _toggle_active(self):
        if self.status != self.STATUS_INACTIVE:
            if self.status in [self.STATUS_ACTIVE, self.STATUS_BREAK, self.STATUS_LONG_BREAK]:
                self._db = PomoDB(filename='resources/data/pomo.db')
                self._db.delete_last_session()
                self._db.close()

            self.status = self.STATUS_INACTIVE
            if self.notification_on:
                self._send_notification(
                    "critical", "Pomodoro has been suspended")

        else:
            self.status = self.STATUS_START

    def _send_notification(self, urgent, message):
        subprocess.run(["dunstify", "-a", 'Pomodoro', '-u',
                       urgent, "Pomodoro",  message, '-i', 'pomodoro'])

    def poll(self):
        return self._get_text()


def _get_last_session():
    db = PomoDB(filename='resources/data/pomo.db')
    ls_cur = db.last_session()
    db.close()
    return ls_cur


class PomoIcon(base.ThreadPoolText):
    defaults = [
        ("update_interval", 2, "Update time in seconds."),  # This arg is necessary
        ("color_inactive", "ff0000", "Colour when pomodoro is inactive"),
        ("color_active", "00ff00", "Colour when pomodoro is running"),
        ("color_break", "ffff00", "Colour when it is break time"),
        ("pomo_object", None, "Pomodoro object"),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(PomoIcon.defaults)

        self.add_callbacks(
            {
                "Button2": self.pomo_object._next_tag,
            }
        )

    def poll(self):
        if self.pomo_object is not None:
            if self.pomo_object.status in [self.pomo_object.STATUS_ACTIVE,
                                           self.pomo_object.STATUS_START]:
                self.layout.colour = self.color_active
                return ""
            if self.pomo_object.status == self.pomo_object.STATUS_INACTIVE:
                self.layout.colour = self.color_inactive
                return ""
            if self.pomo_object.status == self.pomo_object.STATUS_BREAK:
                self.layout.colour = self.color_break
                return ""
            if self.pomo_object.status == self.pomo_object.STATUS_LONG_BREAK:
                self.layout.colour = self.color_break
                return ""
            if self.pomo_object.status == self.pomo_object.STATUS_PAUSED:
                self.layout.colour = self.color_inactive
                return ""
        return ""


def main():
    db = PomoDB(filename='resources/data/pomo.db')

    # Add sessions
    # db.sql_do("insert into 'sessions' (tag_id, date, minutes, state) values (?, ?, ?, ?)",
    # 2, datetime.fromisoformat('2022-06-03 00:45:00'), 120, 0)
    # db.sql_do("insert into 'sessions' (tag_id, date, minutes, state) values (?, ?, ?, ?)",
    # 2, datetime.fromisoformat('2022-06-03 04:05:00'), 120, 0)
    # db.sql_do("insert into 'sessions' (tag_id, date, minutes, state) values (?, ?, ?, ?)", 4, datetime.fromisoformat('2022-04-13 15:19:00'), 45, 0)
    # db.sql_do("update tags set name = 'POMO' where id = 1")

    db.update_tag_minutes()
    print("Update complete")

    # Delete sessions
    # db.sql_do('delete from sessions where id = ?',(136))
    # db.sql_do('delete from sessions where id = ?',(135))

    print("Taks complete")


if __name__ == "__main__":
    main()
