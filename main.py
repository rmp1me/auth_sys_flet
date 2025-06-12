import flet as ft

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.home_page import HomePage

from services.auth_services import AuthService,ConnectionPool  
pool = ConnectionPool(maxsize=10)


class MyApp:
    def __init__(self):
        self.auth_service = AuthService(pool)

    def main(self, page: ft.Page):
        page.title = "Flet Auth System"
        page.bgcolor=ft.Colors="Blue"
        page.theme_mode="Black"
        page.window_width = 375
        page.window_height = 812

        def route_change(route):
            page.views.clear()
            if page.route == "/":
                page.views.append(LoginPage(page, self.auth_service).view)
            elif page.route == "/register":
                page.views.append(RegisterPage(page, self.auth_service).view)
            elif page.route == "/home":
                page.views.append(HomePage(page).view)
            page.update()

        page.on_route_change = route_change
        page.go(page.route)

app = MyApp()
ft.app(target=app.main)
