class Message:
    def __init__(self, sender, receiver, content, datetime):
        self.content = content
        self.sender = sender
        self.receiver = receiver
        self.datetime = datetime


class Chat:
    def __init__(self):
        self.messages = []

    def __getitem__(self, item):
        return self.messages[item]

    def add(self, message):
        self.messages.append(message)

    def delete(self, index):
        if index <= 0 or len(self.messages) == 0:
            return False
        elif index < len(self.messages):
            del self.messages[index]
            return True

    def pop(self):
        del self.messages[-1]

    def sort(self):
        self.messages = sorted(self.messages, key=lambda msg: msg.datetime, reverse=True)
