import random

import flet as ft

from spaced_repetition import SpacedRepetition
from constants import *



class Deck(ft.Column):
    def __init__(self, deck, page, page_props):
        super().__init__()
        self.deck = deck
        self.page = page
        self.page_props = page_props
        self.words = list(deck.keys())
        self.num_words = len(self.words)

        self.curr_ind = -1

        # For Spaced Repetition
        self.spaced_reps = {"Unseen": [SpacedRepetition(w) for w in self.words],
                            "Learning": [],
                            "Reviewing": [],
                            "Mastered": []}

        # Utility
        self.first_display = True
        self.show_next_word(None)


    def choose_next_word(self):
        # Get Probability Distribution over Categories
        total_weight = 2 * len(self.spaced_reps["Unseen"]) + \
                       4 * len(self.spaced_reps["Learning"]) + \
                       2 * len(self.spaced_reps["Reviewing"]) + \
                       1 * len(self.spaced_reps["Mastered"])
        probs = [2 * len(self.spaced_reps["Unseen"]) / total_weight,
                 4 * len(self.spaced_reps["Learning"]) / total_weight,
                 2 * len(self.spaced_reps["Reviewing"]) / total_weight,
                 1 * len(self.spaced_reps["Mastered"]) / total_weight]

        # Choose Category
        #self.curr_chosen_category = np.random.choice(SPACED_REPETITION_CATEGORIES, 1, p=probs)
        self.curr_chosen_category = random.choices(SPACED_REPETITION_CATEGORIES, k=1, weights=probs)
        self.curr_chosen_category = str(self.curr_chosen_category[0])

        # Choose Word Within Chosen Category
        self.curr_spaced_rep_obj_ind = random.randint(0, len(self.spaced_reps[self.curr_chosen_category])-1)
        self.curr_spaced_rep_obj = self.spaced_reps[self.curr_chosen_category][self.curr_spaced_rep_obj_ind]


    def show_next_word(self, e):
        self.choose_next_word()
        self.curr_word = self.curr_spaced_rep_obj.word

        self.page.views[-1].bgcolor = "#edc343"
        self.page.views[-1].controls[0].bgcolor = "#edc343" # AppBar
        self.page.update()

        self.controls = [
                ft.Container(
                    content=ft.Row(
                        [
                        # Vertical bar
                        ft.Container(
                            width=self.page_props["width"] * VERTICAL_LINE_WIDTH_PERCENTAGE / 100, # "50vw",
                            height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_1 / 100, # "50vh",
                            bgcolor=ft.colors.BLACK,
                            margin=ft.margin.only(right=20)
                        ),
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        self.curr_chosen_category,
                                        size=FONT_SIZE_3,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.BLACK,
                                    ),
                                    bgcolor="#fce5b2", # ft.colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                    border_radius=20,
                                ),
                                ft.Text(self.curr_word,
                                        font_family="Playfair Display Extra Bold",
                                        size=FONT_SIZE_1),
                                ft.Text(self.deck[self.curr_word][0],
                                        font_family="Playfair Display Extra Bold",
                                        size=FONT_SIZE_1)
                            ]
                        )
                    ]),
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.TRANSPARENT, # AMBER_200,
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_1 / 100, # "50vh",
                    border_radius=10,
                    ink=True,
                ),
                ft.OutlinedButton(
                    "Flip to see meaning",
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
                    icon="arrow_right_alt_rounded",
                    icon_color="black", # "grey500",
                    style=ft.ButtonStyle(
                            color=ft.colors.BLACK,
                            side=ft.BorderSide(
                                color=ft.colors.BLACK,
                                width=1,
                                )
                            ), # GREY_500,
                    on_click=self.show_meaning
                ),
        ]

        self.controls.extend(self.get_progress_bars())

        if not self.first_display:
            self.update()
        else:
            self.first_display = False


    def show_meaning(self, e):

        self.page.views[-1].bgcolor = "#a3e1c2"
        self.page.views[-1].controls[0].bgcolor = "#a3e1c2" # AppBar
        self.page.update()

        self.controls = [
                ft.Container(
                    content=ft.Row(
                    [
                        # Vertical bar
                        ft.Container(
                            width=self.page_props["width"] * VERTICAL_LINE_WIDTH_PERCENTAGE / 100, # "50vw",
                            height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_1 / 100, # "50vh",
                            bgcolor=ft.colors.BLACK,
                            margin=ft.margin.only(right=20)
                        ),
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        self.curr_chosen_category,
                                        size=FONT_SIZE_3,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.BLACK,
                                    ),
                                    bgcolor="#d3f8e6", # "#fce5b2", # ft.colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                    border_radius=20,
                                ),
                                ft.Text(self.curr_word,
                                        font_family="Playfair Display Extra Bold",
                                        size=FONT_SIZE_2),
                                ft.Text(self.deck[self.curr_word][0],
                                        font_family="Playfair Display Extra Bold",
                                        size=FONT_SIZE_2),
                            ]
                        )
                    ]),
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.TRANSPARENT, # LIGHT_BLUE_ACCENT_200,
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_1 / 100, # "50vh",
                    border_radius=10,
                    ink=True,
                ),
                ft.Container(
                        content=ft.Text(self.deck[self.curr_word][1],
                                        color=ft.colors.BLACK,
                                        size=FONT_SIZE_2),
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.TRANSPARENT, # LIGHT_BLUE_ACCENT_200,
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_2 / 100, # "50vh",
                    border_radius=10,
                    ink=True,
                ),
                ft.OutlinedButton(
                    "I knew this word",
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
                    icon="check_rounded",
                    icon_color="green900",
                    style=ft.ButtonStyle(
                            color=ft.colors.GREEN_900,
                            side=ft.BorderSide(
                                color=ft.colors.BLACK,
                                width=1,
                                )
                            ),
                    on_click=lambda e: self.update_spaced_repetition(e, True)
                ),
                ft.OutlinedButton(
                    "I didn't know this word",
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
                    icon="cancel_rounded",
                    icon_color="red900",
                    style=ft.ButtonStyle(
                            color=ft.colors.RED_900,
                            side=ft.BorderSide(
                                color=ft.colors.BLACK,
                                width=1,
                                )
                            ),
                    on_click=lambda e: self.update_spaced_repetition(e, False)
                ),
        ]
        """
        ft.ElevatedButton(
            "I didn't know this word",
            width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
            height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
            bgcolor="#d88073", # ft.colors.RED_100,
            icon="cancel_rounded",
            icon_color="red900",
            color=ft.colors.RED_900,
            on_click=lambda e: self.update_spaced_repetition(e, False)
        ),
        """

        self.controls.extend(self.get_progress_bars())
        self.update()


    def get_progress_bars(self):
        """
        def progress_bar_factory(text, k, color):
            return [
                ft.Text(f"You {text} {len(self.spaced_reps[k])} out of {self.num_words} words"),
                ft.ProgressBar(
                    value=len(self.spaced_reps[k]) / self.num_words,
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    bar_height=self.page_props["height"] * PROGRESS_BAR_HEIGHT_PERCENTAGE / 100, # "50vh",
                    color=color
                )
            ]

        progress_bars = []
        for text,k,color in [("have mastered", "Mastered", ft.colors.GREEN_500),
                             ("are reviewing", "Reviewing", ft.colors.AMBER_500),
                             ("are learning", "Learning", ft.colors.RED_500)]:
            progress_bars.extend(progress_bar_factory(text, k, color))
        """



        def progress_ring_factory(k):
            progress_ring = ft.ProgressRing(
                    value=len(self.spaced_reps[k]) / self.num_words,
                    width=self.page_props["width"] * PROGRESS_RING_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["width"] * PROGRESS_RING_HEIGHT_PERCENTAGE / 100, # "50vw",
                    bgcolor=ft.colors.GREY_100,
                    #color=color
                )

            return ft.Stack(
                    controls=[
                        progress_ring,
                        ft.Container(
                            content=ft.Text(
                                len(self.spaced_reps[k]),
                                size=FONT_SIZE_3,
                                weight=ft.FontWeight.BOLD,
                            ),
                            width=self.page_props["width"] * PROGRESS_RING_WIDTH_PERCENTAGE / 100, # "50vw",
                            height=self.page_props["width"] * PROGRESS_RING_HEIGHT_PERCENTAGE / 100, # "50vw",
                            alignment=ft.alignment.center
                        )
                    ],
                    width=self.page_props["width"] * PROGRESS_RING_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["width"] * PROGRESS_RING_HEIGHT_PERCENTAGE / 100, # "50vw",
                )


        progress_bars = [ft.Text("A", color=ft.colors.TRANSPARENT, size=FONT_SIZE_3),
                         ft.Container(
                            ft.Row([
                                ft.Column([
                                    progress_ring_factory("Mastered"),
                                    ft.Text("Mastered",
                                            weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER),
                                ft.Column([
                                    progress_ring_factory("Reviewing"),
                                    ft.Text("Reviewing",
                                            weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER),
                                ft.Column([
                                    progress_ring_factory("Learning"),
                                    ft.Text("Learning",
                                            weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER),
                                ft.Column([
                                    progress_ring_factory("Unseen"),
                                    ft.Text("Unseen",
                                            weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                ),
                            width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100,
                            )
                        ]

        return progress_bars


    def update_spaced_repetition(self, e, correct):
        # remove from previous category
        self.spaced_reps[self.curr_chosen_category].pop(self.curr_spaced_rep_obj_ind)

        # update this word's category
        new_category = self.curr_spaced_rep_obj.update(correct)

        # append to new category's list
        self.spaced_reps[new_category].append(self.curr_spaced_rep_obj)

        # go to next word
        self.show_next_word(e)
