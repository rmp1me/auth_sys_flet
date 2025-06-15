import pg8000
import hashlib
from queue import Queue
from threading import Lock


class ConnectionPool:
    def __init__(self, maxsize=10):
        self.pool = Queue(maxsize)
        self.lock = Lock()
        for _ in range(maxsize):
            conn = pg8000.connect(
                user="postgres",
                password="admin",
                host="localhost",
                database="postgres",
                port=5432
            )
            self.pool.put(conn)

    def get_connection(self):
        return self.pool.get()

    def return_connection(self, conn):
        self.pool.put(conn)


class AuthService:
    def __init__(self, pool):
        self.pool = pool

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        conn = self.pool.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM auth_user_reg WHERE username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                return False, "Username already exists."

            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO auth_user_reg (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            conn.commit()
            cursor.close()
            return True, "Registration successful!"
        except Exception as e:
            print("Registration error:", e)
            return False, "Registration failed."
        finally:
            self.pool.return_connection(conn)

    def login(self, username, password):
        conn = self.pool.get_connection()
        try:
            cursor = conn.cursor()
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
        finally:
            self.pool.return_connection(conn)
