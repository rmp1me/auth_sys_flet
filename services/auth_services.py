import os
import json
import pyrebase
from dotenv import load_dotenv

load_dotenv()

class AuthService:
    def __init__(self):
        firebase_config = json.loads(os.getenv("FIREBASE_CONFIG"))
        # Initialize Firebase inside constructor
        firebase = pyrebase.initialize_app(firebase_config)
        self.auth = firebase.auth()
        print(self.auth)

    def register(self, email, password):
        try:
            self.auth.create_user_with_email_and_password(email, password)
            return True, "Registration successful!"
        except Exception as e:
            error_message = self.extract_error(e)
            return False, f"Registration failed: {error_message}"

    def login_google(self, email, password):
        try:
            print("Trying to login by google...!")
            self.auth.sign_in_with_email_and_password(email, password)
            return True, "Login successful"
        except Exception as e:
            error_message = self.extract_error(e)
            return False, f"Login failed"

    def extract_error(self, error):
        # Attempt to extract detailed Firebase error message
        try:
            return error.args[1]['error']['message']
        except:
            return str(error)
    def send_password_reset_email(self, email):
        try:
            self.auth.send_password_reset_email(email)
            return True, "Password reset email sent successfully."
        except Exception as e:
            return False, f"Failed to send reset email: {e}"
