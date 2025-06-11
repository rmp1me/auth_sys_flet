import pg8000
import hashlib

class AuthService:
    def __init__(self):
        self.conn = pg8000.connect(
            user="postgres",
            password="admin",
            host="localhost",
            database="postgres",
            port=5432
        )
        # self.create_user_table()
            
        # self.users = {}
    def hash_password(self, password):        
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM auth_user_reg WHERE username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                return False, "Username already exists."

            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO auth_user_reg (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            self.conn.commit()
            cursor.close()
            return True, "Registration successful!"
        except Exception as e:
            print("Registration error:", e)
            return False, "Registration failed."

    # def register(self, username, password):
    #     if username in self.users:
    #         return False, "User already exists"
    #     self.users[username] = password
    #     return True, "Registered successfully"

    def login(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT password FROM auth_user_reg WHERE username = %s", (username,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                stored_hashed_password = row[0]
                entered_hashed_password = self.hash_password(password)

                if stored_hashed_password == entered_hashed_password:
                    return True, "Login successful"

            return False, "Invalid credentials"
        except Exception as e:
            print("Login error:", e)
            return False, "Login failed due to server error"
