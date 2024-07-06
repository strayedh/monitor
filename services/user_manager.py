import os

class UserManager:
    def __init__(self, user_file='users.txt'):
        self.user_file = user_file
        if not os.path.exists(self.user_file):
            with open(self.user_file, 'w') as f:
                pass

    def register(self, username, password):
        if self.user_exists(username):
            return False
        with open(self.user_file, 'a') as f:
            f.write(f"{username},{password}\n")
        return True

    def login(self, username, password):
        with open(self.user_file, 'r') as f:
            users = f.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split(',')
            if stored_username == username and stored_password == password:
                return True
        return False

    def user_exists(self, username):
        with open(self.user_file, 'r') as f:
            users = f.readlines()
        for user in users:
            stored_username, _ = user.strip().split(',')
            if stored_username == username:
                return True
        return False
