import flet as ft

def main(page: ft.Page):
    page.title = "Hello World Flet App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.add(
        ft.Text("Hello, GitHub Pages!", size=30, color=ft.colors.BLUE)
    )

ft.app(target=main)

