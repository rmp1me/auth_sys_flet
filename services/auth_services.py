class AuthService:
    def __init__(self):
        self.users = {}

    def register(self, username, password):
        if username in self.users:
            return False, "User already exists"
        self.users[username] = password
        return True, "Registered successfully"

    def login(self, username, password):
        if self.users.get(username) == password:
            return True, "Login successful"
        return False, "Invalid credentials"
