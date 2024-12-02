import flet as ft


TEXT_BOX_WIDTH_PERCENTAGE = 75
TEXT_BOX_HEIGHT_PERCENTAGE = 40

BUTTON_HEIGHT_PERCENTAGE = 5
PROGRESS_BAR_HEIGHT_PERCENTAGE = 3

FONT_SIZE_1 = 30
FONT_SIZE_2 = 20

SPACED_REPETITION_CATEGORIES = ["Unseen", "Learning", "Reviewing", "Mastered"]

# 19 and 1 --> total weight = 23 --> prob = 4/23
# 49 and 1 --> total weight = 53 --> prob = 4/53



class SpacedRepetition:
    def __init__(self, word):
        self.word = word

        self.category = "Unseen" # "Unseen", "Learning", "Reviewing", "Mastered"
        self.streak = 0

    def update(self, correct):
        """
        correct : bool
        """

        """
        Unseen --> streak==1 --> Mastered
               --> streak==-1 --> Learning

        Learning --> correct --> Reviewing

        Reviewing --> streak==2 --> Mastered
                  --> streak==-1 --> Learning

        Mastered --> wrong --> Reviewing
        """
        # Update Streak
        if correct:
            self.streak += 1
        else:
            self.streak -= 1

        # Update Category
        if self.category=="Unseen":
            if self.streak >= 1:
                self.category = "Mastered"
                self.streak = 0
            else:
                self.category = "Learning"
                self.streak = 0
        elif self.category=="Learning":
            if correct:
                self.category = "Reviewing"
                self.streak = 0
        elif self.category=="Reviewing":
            if self.streak >= 2:
                self.category = "Mastered"
                self.streak = 0
            elif self.streak <= -1:
                self.category = "Learning"
                self.streak = 0
        elif self.category=="Mastered":
            if not correct:
                self.category = "Reviewing"
                self.streak = 0
        else:
            raise ValueError(f"unknown category : {self.category}")
        return self.category


class FlashCardApp(ft.Column):
    def __init__(self, vocab, page_props):
        super().__init__()
        self.vocab = vocab
        self.page_props = page_props
        self.words = list(vocab.keys())
        self.num_words = len(self.words)

        self.first_display = True
        self.curr_ind = -1
        self.curr_word = self.words[self.curr_ind]

        self.show_next_word(None)

                    
    def show_next_word(self, e):
        self.curr_ind = (self.curr_ind + 1) % self.num_words
        self.curr_word = self.words[self.curr_ind]

        self.controls = [
                ft.Container(
                    content=ft.Text(self.curr_word, size=FONT_SIZE_1),
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.AMBER_200,
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * 0.4, # "50vh",
                    border_radius=10,
                    ink=True,
                ),
                ft.ElevatedButton(
                    "Click to see meaning",
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
                    bgcolor=ft.colors.GREY_100,
                    icon="arrow_right_alt_rounded",
                    icon_color="grey500",
                    color=ft.colors.GREY_500,
                    on_click=self.show_meaning
                ),
        ]

        if not self.first_display:
            self.update()
        else:
            self.first_display = False

    def show_meaning(self, e):
        self.controls = [
                ft.Container(
                    content=ft.Text(self.curr_word + "\n\n" + self.vocab[self.curr_word], size=FONT_SIZE_2),
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.LIGHT_BLUE_ACCENT_200,
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE / 100, # "50vh",
                    border_radius=10,
                    ink=True,
                ),
                ft.ElevatedButton(
                    "I knew this word",
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
                    bgcolor=ft.colors.GREEN_100,
                    icon="check_rounded",
                    icon_color="green500",
                    color=ft.colors.GREEN_500,
                    on_click=self.show_next_word
                ),
                ft.ElevatedButton(
                    "I didn't know this word",
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
                    bgcolor=ft.colors.RED_100,
                    icon="cancel_rounded",
                    icon_color="red500",
                    color=ft.colors.RED_500,
                    on_click=self.show_next_word
                ),
        ]
        self.update()




def main(page: ft.Page):
    page.title = "To-Do App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # Dictionary
    vocab = {"રત્નત્રય" : ("ratnatray", "Samyak Darshan (Faith), Samyak Gnaan (Knowledge), Samyak Charitra (Conduct)"),
             "નય" : ("nay", "point of view, dimension"),
             "ક્રુત્રિમ ": ("Krutrim", "Artificial"),
             "નિર્મલ સમલ" : ("Nirmal, Samal", "without-impurities, with-impurities")}

    vocab = dict([(f"{k}  |  {v[0]}", v[1])for k,v in vocab.items()])
    keys = list(vocab.keys())

    # create application instance
    page_props = {"width" : page.width,
                  "height" : page.height}
    flashcard_app = FlashCardApp(vocab, page_props)

    # add application's root control to the page
    page.add(flashcard_app)


ft.app(target=main)
