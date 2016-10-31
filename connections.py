class Connection:
    def __init__(self, user_id, following_id, date):
        self.user = user_id
        self.following = following_id
        self.date = date

class Connections:
    def __init__(self):
        self.connections = {}
        self.counter = 0

    def add_connection(self, connection):
        self.counter += 1
        self.connections[self.counter] = connection

    def delete_connection(self, counter):
        del self.connections[counter]

    def get_connection(self, counter):
        return self.posts[counter]

    def get_connections(self):
        return self.connections.items()
