import flet as ft

class LoginPage:
    def __init__(self, page: ft.Page, auth_service):
        self.page = page
        self.auth_service = auth_service
        self.username = ft.TextField(label="Username")
        self.password = ft.TextField(label="Password", password=True)
        self.message = ft.Text()
        self.register_link = ft.TextButton(text="Register", on_click=lambda _: self.page.go("/register"))
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login)

        
        
        self.google_button = ft.ElevatedButton(
            text="Continue with Google",
            icon=ft.Icon(name="account_circle"),
            on_click=self.google_login,
            style=ft.ButtonStyle(bgcolor="white", color="black"),
            width=250
        )

        self.facebook_button = ft.ElevatedButton(
            text="Continue with Facebook",
            icon=ft.Icon(name="facebook"),
            on_click=self.facebook_login,
            style=ft.ButtonStyle(bgcolor="blue", color="white"),
            width=250
        )        

        self.view = ft.View(
            route="/",
            controls=[
                ft.Column([
                    ft.Text("Login", size=35),                  
                    self.username,
                    self.password,
                    self.login_button,
                    self.register_link,
                    self.message,
                    ft.Divider(height=10, color="black"),
                    self.google_button,
                    self.facebook_button                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=300)
            ]
        )

    def login(self, e):
        success, msg = self.auth_service.login(self.username.value, self.password.value)
        self.message.value = msg
        if success:
            self.page.go("/home")
        self.page.update()

    def google_login(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Google login clicked"))
        self.page.snack_bar.open = True
        self.page.update()

    def facebook_login(self, e):
        self.page.snack_bar = ft.SnackBar(ft.Text("Facebook login clicked"))
        self.page.snack_bar.open = True
        self.page.update()
