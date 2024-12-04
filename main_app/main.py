import flet as ft
import random

TEXT_BOX_WIDTH_PERCENTAGE = 75
TEXT_BOX_HEIGHT_PERCENTAGE_1 = 40
TEXT_BOX_HEIGHT_PERCENTAGE_2 = 20
TEXT_BOX_HEIGHT_PERCENTAGE_3 = 10

BUTTON_HEIGHT_PERCENTAGE = 5
PROGRESS_BAR_HEIGHT_PERCENTAGE = 3

FONT_SIZE_1 = 30
FONT_SIZE_2 = 20
FONT_SIZE_3 = 15

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
    def __init__(self, page_props):
        super().__init__()
    
        self.page_props = page_props

        # Utility
        self.first_display = True
        self.show_all_decks(None)


    def show_all_decks(self, e):
        def get_deck(title):
            return ft.Column(
                    spacing=0,
                    controls=[
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
                            border_radius=0
                        )
                    ]
                )         

        self.controls = [
                ft.Text("Satsang Vocabulary Decks",
                        size=FONT_SIZE_1,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK)
        ]

        # Add Decks
        for title in ["Beejam Kram I"]:
            self.controls.append(get_deck(title)) 


        # Utility
        if not self.first_display:
            self.update()
        else:
            self.first_display = False


        


class Deck(ft.Column):
    def __init__(self, vocab, page_props):
        super().__init__()
        self.vocab = vocab
        self.page_props = page_props
        self.words = list(vocab.keys())
        self.num_words = len(self.words)

        self.curr_ind = -1

        # For Spaced Repetition
        #print(self.words)
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
        #print("curr_spaced_rep_obj_ind", self.curr_spaced_rep_obj_ind)
        #print("curr_spaced_rep word", self.curr_spaced_rep_obj.word)

                    
    def show_next_word(self, e):
        self.choose_next_word()
        self.curr_word = self.curr_spaced_rep_obj.word

        self.controls = [
                ft.Container(
                    content=ft.Text(self.curr_word, size=FONT_SIZE_1),
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.AMBER_200,
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_1 / 100, # "50vh",
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

        self.controls.extend(self.get_progress_bars())

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
                    height=self.page_props["height"] * TEXT_BOX_HEIGHT_PERCENTAGE_1 / 100, # "50vh",
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
                    on_click=lambda e: self.update_spaced_repetition(e, True)
                ),
                ft.ElevatedButton(
                    "I didn't know this word",
                    width=self.page_props["width"] * TEXT_BOX_WIDTH_PERCENTAGE / 100, # "50vw",
                    height=self.page_props["height"] * BUTTON_HEIGHT_PERCENTAGE / 100, # "50vh",
                    bgcolor=ft.colors.RED_100,
                    icon="cancel_rounded",
                    icon_color="red500",
                    color=ft.colors.RED_500,
                    on_click=lambda e: self.update_spaced_repetition(e, False)
                ),
        ]

        self.controls.extend(self.get_progress_bars())
        self.update()


    def get_progress_bars(self):
        def progress_bar_factory(text, k, color):
            return [
                ft.Text(f"You {text} {len(self.spaced_reps[k])} out of {self.num_words} words"),
                ft.ProgressBar(
                    value=len(self.spaced_reps[k]) / self.num_words,
                    bar_height=self.page_props["height"] * PROGRESS_BAR_HEIGHT_PERCENTAGE / 100, # "50vh",
                    color=color
                )
            ]

        progress_bars = []
        for text,k,color in [("have mastered", "Mastered", ft.colors.GREEN_500),
                             ("are reviewing", "Reviewing", ft.colors.AMBER_500),
                             ("are learning", "Learning", ft.colors.RED_500)]:
            progress_bars.extend(progress_bar_factory(text, k, color))
        return progress_bars


    def update_spaced_repetition(self, e, correct):
        # remove from previous category
        self.spaced_reps[self.curr_chosen_category].pop(self.curr_spaced_rep_obj_ind)
        #print("chosen_category", self.curr_chosen_category)

        # update this word's category
        new_category = self.curr_spaced_rep_obj.update(correct)
        #print("new_category", new_category)

        # append to new category's list
        self.spaced_reps[new_category].append(self.curr_spaced_rep_obj)

        # go to next word
        self.show_next_word(e)



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
    flashcard_app = FlashCardApp(page_props) # vocab, page_props)
    deck = Deck(vocab, page_props)

    # add application's root control to the page
    page.add(flashcard_app) # deck)


ft.app(target=main)
