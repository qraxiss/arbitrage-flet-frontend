import flet as ft


class Login(ft.UserControl): 
    def __init__(self, on_login, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = ft.TextField(hint_text = "username", width=300)
        self.password = ft.TextField(hint_text = "password", width=300, password=True)

        self.submit = ft.TextButton("Login", 
            on_click=lambda e : on_login(
                e,
                username = self.username.value,
                password = self.password.value
            ) 
        )

    def build(self):
        return ft.Column(
            [self.username, self.password, self.submit],
             horizontal_alignment="center"
        )
    

    def __del__(self):
        print('deleted')