import flet as ft

class LoginPage:
    def __init__(self, page: ft.Page, auth_service):
        self.page = page
        self.auth_service = auth_service
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True)
        self.message = ft.Text()
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login)
       
        
       
        self.register_link = ft.TextButton(text="Register", on_click=lambda _: self.page.go("/register"))

        self.view = ft.View(
            route="/",
            controls=[
                ft.Column([
                    ft.Text("Login", size=30),
                    self.username,
                    self.password,
                    self.login_button,
                    self.message,
                    self.register_link
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=300)
            ]
        )

    def login(self, e):
        success, msg = self.auth_service.login(self.username.value, self.password.value)
        self.message.value = msg
        if success:
            self.page.go("/home")
        self.page.update()
