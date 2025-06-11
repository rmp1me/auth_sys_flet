import flet as ft

class RegisterPage:
    def __init__(self, page: ft.Page, auth_service):
        self.page = page
        self.auth_service = auth_service
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True)
        self.message = ft.Text()
        self.register_button = ft.ElevatedButton(text="Register", on_click=self.register)
        self.login_link = ft.TextButton(text="Back to Login", on_click=lambda _: self.page.go("/"))

        self.view = ft.View(
            route="/register",
            controls=[
                ft.Column([
                    ft.Text("Register", size=30),
                    self.username,
                    self.password,
                    self.register_button,
                    self.message,
                    self.login_link
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=300)
            ]
        )

    def register(self, e):
        success, msg = self.auth_service.register(self.username.value, self.password.value)
        self.message.value = msg
        if success:
            self.page.go("/")
        self.page.update()
