import flet as ft

from constants import *



class FlashCardApp(ft.Column):
    def __init__(self, orchestrator, page_props, all_deck_names):
        super().__init__()

        self.orchestrator = orchestrator
        self.page_props = page_props
        self.all_deck_names = all_deck_names

        # Utility
        self.first_display = True
        self.show_all_decks(None)

        # Alignment
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def show_all_decks(self, e):
        def get_deck(title):
            return ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(title,
                                            size=FONT_SIZE_2,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.colors.GREY_700),
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREY_100,
                            width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                            height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_2 / 100, # "50vh",
                            border_radius=0
                        ),
                        ft.Container(
                            content=ft.Text("Practice this deck ⟶",
                                            size=FONT_SIZE_3,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.colors.GREY_500),
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREY_300,
                            width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                            height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_3 / 100, # "50vh",
                            border_radius=0,
                            on_click=lambda x: self.orchestrator.route_to(f"/deck/{title}")
                        )
                    ],
                    spacing=0,
                )

        self.controls = []

        # Add Decks
        for title in self.all_deck_names:
            self.controls.append(get_deck(title))

        # Utility
        if not self.first_display:
            self.update()
        else:
            self.first_display = False

