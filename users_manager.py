class UsersManager:
    def __init__(self):
        self.users = []

    def add_user(self, user_info):
        self.users.append(user_info)

    def get_users(self):
        return self.users
