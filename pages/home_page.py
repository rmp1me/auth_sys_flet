import flet as ft

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = ft.View(
            route="/home",
            controls=[
                ft.Column([
                    ft.Text("Welcome to the Home Page!", size=25),
                    ft.TextButton("Logout", on_click=lambda _: self.page.go("/"),icon=ft.Icons.LOGOUT_OUTLINED)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ]
        )
