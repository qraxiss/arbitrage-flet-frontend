import flet as ft

from components.login import Login
from controllers.login import login

from components.table import Table

from config import FLET_PORT

class Manager:
    def __init__(self, page: ft.Page) -> None:
        self.page = page

    def login(self, *args, **kwargs):
        if login(*args, **kwargs):
            self.page.clean()
            self.page.add(Table(self.page))

def main(page: ft.Page):
    manager = Manager(page)
    page.title = 'DexScanner'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"
    login = Login(manager.login)
    page.add(login)

    page.update()


ft.app(target=main, port = FLET_PORT, view=None)