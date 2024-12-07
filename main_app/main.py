import flet as ft
#from flet.auth.providers import Auth0OAuthProvider
#from flet.auth.providers import GitHubOAuthProvider

import random
from collections import OrderedDict


TEXT_BOX_WIDTH_PERCENTAGE = 75
TEXT_BOX_HEIGHT_PERCENTAGE_1 = 30
TEXT_BOX_HEIGHT_PERCENTAGE_2 = 20
TEXT_BOX_HEIGHT_PERCENTAGE_3 = 10

BUTTON_HEIGHT_PERCENTAGE = 5
PROGRESS_BAR_HEIGHT_PERCENTAGE = 3

PROGRESS_RING_HEIGHT_PERCENTAGE = 10
PROGRESS_RING_WIDTH_PERCENTAGE = 10

VERTICAL_LINE_WIDTH_PERCENTAGE = 1

FONT_SIZE_1 = 25
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
        """
                ft.Text("Satsang Vocabulary Decks",
                        size=FONT_SIZE_1,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK,
                        text_align=ft.TextAlign.CENTER)
        ]
        """

        # Add Decks
        for title in self.all_deck_names:
            self.controls.append(get_deck(title)) 

        # Utility
        if not self.first_display:
            self.update()
        else:
            self.first_display = False
        


class Deck(ft.Column):
    def __init__(self, vocab, page, page_props):
        super().__init__()
        self.vocab = vocab
        self.page = page
        self.page_props = page_props
        self.words = list(vocab.keys())
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
                                ft.Text(self.vocab[self.curr_word][0],
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
        self.page.views[-1][0].bgcolor = "#a3e1c2" # AppBar
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
                                ft.Text(self.vocab[self.curr_word][0],
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
                        content=ft.Text(self.vocab[self.curr_word][1],
                                        font_family="Playfair Display Extra Bold",
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

         
        progress_bars = [ft.Container(
                            ft.Row([
                                ft.Column([
                                    progress_ring_factory("Mastered"),
                                    ft.Text("Mastered",
                                            weight=ft.FontWeight.BOLD),
                                    ]),
                                ft.Column([
                                    progress_ring_factory("Reviewing"),
                                    ft.Text("Reviewing",
                                            weight=ft.FontWeight.BOLD),
                                    ]),
                                ft.Column([
                                    progress_ring_factory("Learning"),
                                    ft.Text("Learning",
                                            weight=ft.FontWeight.BOLD),
                                    ]),
                                ft.Column([
                                    progress_ring_factory("Unseen"),
                                    ft.Text("Unseen",
                                            weight=ft.FontWeight.BOLD),
                                    ]),
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


class Orchestrator:
    def __init__(self, page, vocabs):
        self.page = page
        self.vocabs = vocabs

        self.all_deck_names = list(self.vocabs.keys())

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.font_family = "RobotoSlab"

        self.page_props = {"width" : page.width,
                           "height" : page.height}
            
        # OAuth
        """
        self.provider = Auth0OAuthProvider(
            client_id="ioQ4UgajAgoAxz2PahBbeuSrs8zrLEu8",
            client_secret="11M8ZGiC727PS75w8BBBOyKYx96-3UAMOYUqTj0dLnH5N77AYqO9NQOU_lEQVknV",
            domain="dev-50q3lvc10l4nm2s1.us.auth0.com",
            #redirect_url="http://localhost:8550/api/oauth/redirect"
            redirect_url="http://localhost:8550/oauth_callback",
        )
        """
        self.page.on_login = self.on_login

        # Memory and Personalization
        self.state = {} # state

        self.flashcard_app = FlashCardApp(self, self.page_props, self.all_deck_names)


    def start(self):
        self.page.go("/") # goes to route_chage(...)


    def on_login(self, e):
        print("Login error:", e.error)
        print("Access token:", self.page.auth.token.access_token)
        print("User ID:", self.page.auth.user.id)
                       
     
    def route_to(self, route):
        self.page.go(route)


    def handle_login(self, e):
        print("handling login")
        self.page.login(self.provider)
        self.page.update()


    def get_AppBar(self, route):
        # Actions
        """
        if self.page.auth is None:
            actions = [ft.IconButton(ft.icons.WB_SUNNY_OUTLINED,
                                     on_click=self.handle_login),
                      ]
        else:
            actions = [ft.IconButton(ft.icons.WB_SUNNY_ROUNDED,
                                     on_click=self.handle_login),
                      ]
        """
        actions = []

        # AppBar
        if route=="/":
            return ft.AppBar(title=ft.Text("Satsang Vocabulary Decks",
                                           size=FONT_SIZE_1,
                                           weight=ft.FontWeight.BOLD,
                                           color=ft.colors.BLACK,
                                           text_align=ft.TextAlign.CENTER),
                             center_title=True,
                             actions=actions)
        elif self.page.route[:6] == "/deck/":
            deck_name = self.page.route[6:]
            return ft.AppBar(title=ft.Text(f"{deck_name}",
                                           size=FONT_SIZE_1,
                                           weight=ft.FontWeight.BOLD,
                                           color=ft.colors.BLACK,
                                           text_align=ft.TextAlign.CENTER),
                             center_title=True,
                             actions=actions)
        else:
            return ft.AppBar()


    def route_change(self, route):
        print("ROUTE CHANGE", route)

        self.page.controls.clear()

        # Show All Decks
        if self.page.route=="/":
            self.page.views.append(
                ft.View(
                    "/all_decks",
                    [
                        self.get_AppBar(self.page.route),
                        self.flashcard_app,
                    ],
                    bgcolor="#f3c017",
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        # Show Deck
        if self.page.route[:6] == "/deck/":
            deck_name = self.page.route[6:]
            deck = Deck(self.vocabs[deck_name], self.page, self.page_props)

            self.page.views.append(
                ft.View(
                    "/deck/{deck_name}",
                    [
                        self.get_AppBar(self.page.route),
                        deck,
                    ],
                    bgcolor="#edc343",
                    #decoration=ft.BoxDecoration(image=ft.DecorationImage(src="/images/HD-wallpaper-abstract-blue-green-lime.jpg",
                    #                                                     fit=ft.ImageFit.COVER,
                    #                                                     opacity=1)),
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        self.page.update()


    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        

    


def main(page: ft.Page):
    page.title = "Satsang Vocabulary App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.fonts = {"Roboto Condensed" : "RobotoCondensed-Regular.ttf",
                  "Playfair Display Extra Bold" : "fonts/PlayfairDisplay-ExtraBold.ttf"}

    page.theme = ft.Theme(font_family="Roboto Condensed")

    page.update()

    # All Decks
    vocabs = OrderedDict([
                ("Beejam Kram I", {"રત્નત્રય" : ("ratnatray", "Samyak Darshan (Faith), Samyak Gnaan (Knowledge), Samyak Charitra (Conduct)"),
                                   "નય" : ("nay", "point of view, dimension"),
                                   "ક્રુત્રિમ ": ("krutrim", "Artificial"),
                                   "નિર્મલ સમલ" : ("nirmal, samal", "without-impurities, with-impurities")}),
                ("Beejam Kram II", {"lorem" : ("ipsum", "dolor sit amet")})
             ])

    #for k,v in vocabs.items():
    #   vocabs[k] = dict([(f"{kk}  |  {vv[0]}", vv[1]) for kk,vv in v.items()])

    all_deck_names = list(vocabs.keys()) 

    # create application instance
    page_props = {"width" : page.width,
                  "height" : page.height}

    # Objects
    #flashcard_app = FlashCardApp(page, page_props, all_deck_names) # vocab, page_props)
    #deck = Deck(vocab, page_props)

    # add application's root control to the page
    #page.go("/")

    # Orchestrator
    orchestrator = Orchestrator(page, vocabs)
    orchestrator.start()


#ft.app(target=main)
ft.app(target=main, assets_dir="assets")
#ft.app(target=main, port=8550, view=ft.AppView.WEB_BROWSER)
