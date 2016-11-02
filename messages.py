import pymysql
from dbconnection import MySQL


class Message:
    def __init__(self, sender, receiver, content, datetime, is_liked=0, msg_id=0):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.datetime = datetime
        self.is_liked = is_liked  # Integer value, from sql (0 or 1)
        self.msg_id = msg_id


class Chat:
    def __init__(self):
        self.messages = {}
        self.key = 0

    def __getitem__(self, item):
        return self.messages[item]

    def add(self, message):
        self.key += 1
        message.key = self.key
        self.messages[self.key] = message

    def delete(self, index):
        del self.messages[index]

    def get_last(self):
        if self.key == 0:
            return 0
        return self.messages[self.key]

    def get_list(self):
        return sorted(self.messages.items())

    def is_empty(self):
        return self.key == 0


class Inbox:
    def __init__(self):
        self.chats = []

    def add(self, chat, participant):
        if len(chat.messages) != 0:
            self.chats.append((chat, participant))


def get_inbox(user_id):
    inbox = Inbox()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT user_id, participant_id,
                                in_out, content, message_datetime
                      FROM messages, conversations
                      WHERE (messages.message_id = conversations.message_id)
                            AND (user_id = %d)
                      ORDER BY participant_id, message_datetime""" % user_id
        c.execute(sql)

        old_p = 0
        chat = Chat()

        for user, participant, in_out, content, msg_datetime in c:
            if in_out == 0:
                sender = user
                receiver = participant
            else:
                sender = participant
                receiver = user

            msg = Message(sender, receiver, content, msg_datetime)

            if old_p == participant:
                chat.add(msg)
            else:
                if chat.key != 0:
                    inbox.add(chat, old_p)
                chat = Chat()
                chat.add(msg)
            old_p = participant
        inbox.add(chat, old_p)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    return inbox


def send_message(user_id, participant_id, content, date):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        sql = """INSERT INTO messages(content, message_datetime)
                              VALUES('%s', '%s')""" % (content, date.strftime(f))
        c.execute(sql)

        sql = """SELECT MAX(message_id) FROM messages"""
        c.execute(sql)
        for x in c:
            msg_id = x[0]

        sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
                              VALUES(%d, %d ,%d, %d)""" % (user_id, int(participant_id), 0, msg_id)
        c.execute(sql)
        sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
                              VALUES(%d, %d ,%d, %d)""" % (int(participant_id), user_id, 1, msg_id)
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def delete_conversation(user_id, participant_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """DELETE FROM conversations
                      WHERE (user_id = %d)
                        AND (participant_id = %d)""" % (user_id, participant_id)
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()
    except Exception as e:
        print(str(e))

