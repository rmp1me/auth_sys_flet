import flet as ft
from services import auth_services

class LoginPage:
    def __init__(self, page: ft.Page, auth_service):
        self.page = page
        self.auth_service = auth_service

        self.username = ft.TextField(label="Email", autofocus=True)
        self.password = ft.TextField(label="Password", password=True)

        self.message = ft.Text(size=14, weight="w500", color="RED", visible=False)

        self.login_button = self.create_button("Login", self.login_google_up, padding=10)
        
        self.forgot_password_link = ft.TextButton(
                                                    text="Forgot Password?",
                                                    on_click=self.send_reset_email,
                                                    style=ft.ButtonStyle(color="blue")
                                                )
        self.google_button = self.create_button(
                                                "Continue with Google",
                                                self.google_login,
                                                width=300,
                                                padding=20,
                                                with_events=True
                                            )

        self.view = ft.View(
                    route="/",
                    controls=[
                        ft.Column([
                            ft.Text("User Login", size=35),
                            self.username,
                            self.password,

                            # Updated: Login + Forgot Password vertically
                            ft.Column(
                                [
                                    self.login_button,
                                    self.forgot_password_link
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5
                            ),

                            ft.Divider(height=5, color="blue"),
                            self.message,
                            self.google_button
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=300)
                    ]
                )


    # --- Helper to Create Buttons ---
    def create_button(self, text, on_click, width=None, padding=10, with_events=False):
        button = ft.ElevatedButton(
            text=text,
            on_click=on_click,
            width=width,
            style=ft.ButtonStyle(
                bgcolor="black",
                color="white",
                shape=ft.RoundedRectangleBorder(radius=5),
                padding=padding
            )
        )
        if with_events:
            button.on_hover = self.set_hover_color
            button.on_focus = self.set_focus_color
            button.on_blur = self.set_reset_color
        return button

    # --- Hover/Focus/Blur Styling ---
    def set_hover_color(self, e):
        self.update_button_color(e, "#424242" if e.data == "true" else "black")

    def set_focus_color(self, e):
        self.update_button_color(e, "#616161")

    def set_reset_color(self, e):
        self.update_button_color(e, "black")

    def update_button_color(self, e, color):
        e.control.bgcolor = color
        e.control.update()

    # --- Login Event ---
    def login_google_up(self, e):
        success, msg = self.auth_service.login_google(self.username.value, self.password.value)
        self.show_message(msg, success)
        if success:
            self.page.go("/home")

    # --- Google Register Redirect ---
    def google_login(self, e):
        self.page.go("/register")

    # --- Forgot Password ---
    def send_reset_email(self, e):
        email = self.username.value
        if not email:
            self.show_message("Please enter your email to reset password.", False)
        else:
            success, msg = self.auth_service.send_password_reset_email(email)
            self.show_message(msg, success)

    # --- Unified Message Display ---
    def show_message(self, msg, success=False):
        self.message.value = msg
        self.message.color = "green" if success else "red"
        self.message.visible = True
        self.page.update()
