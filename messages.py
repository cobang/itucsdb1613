class Message:
    def __init__(self, sender, receiver, content, datetime, is_liked=0):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.datetime = datetime
        self.is_liked = is_liked  # Integer value, from sql (0 or 1)


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

