class Users:
    def __init__(self):
        self.users = {}
        self.key = 0

    def add_user(self, user):
        self.key += 1
        user.key = self.key
        self.users[self.key] = user

    def get_user(self, key):
        return self.users[key]

    def get_users(self):
        return sorted(self.users.items())


class User:
    def __init__(self, id, name, surname, email, password):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
