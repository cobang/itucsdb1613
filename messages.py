class Message:
    def __init__(self, sender, receiver, content, datetime):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.datetime = datetime


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
        return self.messages[self.key]

    def get_list(self):
        return sorted(self.messages.items())


class Inbox:
    def __init__(self):
        self.chats = []

    def add(self, chat, participant):
        self.chats.append((chat, participant))
