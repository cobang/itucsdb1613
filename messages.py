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
        self.name = ''
        self.surname = ''

    def __getitem__(self, item):
        return self.messages[item]

    def add(self, message):
        self.key += 1
        # message.key = self.key
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

        sql = """SELECT c.user_id, c.participant_id,
                        c.in_out, m.content, m.message_datetime,
                        m.message_id, m.is_liked,
                        u.user_name, u.user_surname
                 FROM messages AS m
                 INNER JOIN conversations AS c
                    ON c.message_id = m.message_id
                 INNER JOIN user_detail AS u
                    ON u.user_id = c.participant_id
                 WHERE c.user_id = %d
                 ORDER BY c.participant_id, m.message_datetime""" % user_id
        c.execute(sql)

        old_p = 0
        chat = Chat()

        for user, participant, in_out, content, msg_datetime, msg_id, is_liked, name, surname in c:
            if in_out == 0:
                sender = user
                receiver = participant
            else:
                sender = participant
                receiver = user

            msg = Message(sender, receiver, content, msg_datetime,
                          is_liked=is_liked, msg_id=msg_id)

            if old_p == participant:
                chat.add(msg)
            else:
                if chat.key != 0:
                    inbox.add(chat, old_p)
                chat = Chat()
                chat.name = name
                chat.surname = surname
                chat.add(msg)
            old_p = participant

        chat.name = name
        chat.surname = surname
        inbox.add(chat, old_p)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    return inbox


def send_message(user_id, participant_id, content, date):
    print('sending...')
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        sql = """INSERT INTO messages(content, message_datetime, is_liked)
                              VALUES('%s', '%s', 0)""" % (content, date.strftime(f))
        c.execute(sql)
        print('message inserted')

        # sql = """SELECT MAX(message_id) FROM messages"""
        # c.execute(sql)
        # for x in c:
        #    msg_id = x[0]
        # sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
        #                      VALUES(%d, %d ,%d, %d)""" % (user_id, int(participant_id), 0, msg_id)

        sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
           SELECT %d, %d, %d, MAX(message_id)
           FROM messages""" % (user_id, participant_id, 0)
        c.execute(sql)

        # sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
        #                      VALUES(%d, %d ,%d, %d)""" % (int(participant_id), user_id, 1, msg_id)

        sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
           SELECT %d, %d, %d, MAX(message_id)
           FROM messages""" % (participant_id, user_id, 1)
        c.execute(sql)
        print('conversations inserted')

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


def like_message(message_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """UPDATE messages
                  SET is_liked = 1
                  WHERE message_id = %d""" % message_id
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def unlike_message(message_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """UPDATE messages
                  SET is_liked = 0
                  WHERE message_id = %d""" % message_id
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def delete_message(message_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """DELETE FROM conversations
                    WHERE message_id = %d""" % message_id
        c.execute(sql)

        sql = """DELETE FROM messages
                    WHERE message_id = %d""" % message_id
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def get_name_surname(user_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """SELECT user_name, user_surname
                 FROM user_detail
                 WHERE user_id = %d""" % user_id
        c.execute(sql)

        user_info = ('', '')
        for name, surname in c:
            user_info = (name, surname)
            print(user_info[0], user_info[1])

        c.close()
        conn.close()

        return user_info

    except Exception as e:
        print(str(e))
