import flet as ft
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.home_page import HomePage
from services.auth_services import AuthService
from dotenv import load_dotenv
load_dotenv()

class MyApp:
    def __init__(self):
        self.auth_service = AuthService()

    def main(self, page: ft.Page):
        # Basic window setup
        page.title = "Flet Auth System"
        page.window_width = 480
        page.window_height = 350
        page.bgcolor = "#0D1B2A"  # Dark blue background

        # Routing logic
        routes = {
            "/": lambda: LoginPage(page, self.auth_service).view,
            "/register": lambda: RegisterPage(page, self.auth_service).view,
            "/home": lambda: HomePage(page).view,
        }

        def route_change(route):
            page.views.clear()
            page.views.append(routes.get(page.route, lambda: ft.View("/"))())
            page.update()

        page.on_route_change = route_change
        page.go(page.route)

# Start the app
if __name__ == "__main__":
    app = MyApp()
    ft.app(target=app.main)
