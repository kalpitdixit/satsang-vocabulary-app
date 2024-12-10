import os
import flet as ft
import random
import glob
from collections import OrderedDict

#from flet.auth.providers import Auth0OAuthProvider

from flash_card_app import FlashCardApp
from deck import Deck
from constants import *



class Orchestrator:
    def __init__(self, page, decks):
        self.page = page
        self.decks = decks

        self.all_deck_names = list(self.decks.keys())

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
                             actions=actions,
                             toolbar_height=self.page_props["height"] * APP_BAR_HEIGHT_PERCENTAGE / 100)
        elif self.page.route[:6] == "/deck/":
            deck_name = self.page.route[6:]
            return ft.AppBar(title=ft.Text(f"{deck_name}",
                                           size=FONT_SIZE_1,
                                           weight=ft.FontWeight.BOLD,
                                           color=ft.colors.BLACK,
                                           text_align=ft.TextAlign.CENTER),
                             center_title=True,
                             actions=actions,
                             toolbar_height=self.page_props["height"] * APP_BAR_HEIGHT_PERCENTAGE / 100)
        else:
            return ft.AppBar(
                             toolbar_height=self.page_props["height"] * APP_BAR_HEIGHT_PERCENTAGE / 100
                            )


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
            self.page.views[-1].controls[0].bgcolor = "#f3c017" # AppBar

        # Show Deck
        if self.page.route[:6] == "/deck/":
            deck_name = self.page.route[6:]
            deck = Deck(self.decks[deck_name], self.page, self.page_props)

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
            self.page.views[-1].controls[0].bgcolor = "#edc343" # AppBar

        self.page.update()


    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        

def read_deck_csv(fname):
    with open(fname, "r", encoding="utf-8") as f:
        headers = f.readline().strip()
        #headers = headers.encode("ascii", "ignore").decode("ascii")
        headers = headers.split(",")

        deck = {}
        for line in f:
            line = line.strip()
            line = [x.strip() for x in line.split(",")]
            gujarati_word = line[0]
            english_word = line[1]
            meaning = line[2]
            
            deck[gujarati_word] = (english_word, meaning)
    return deck


def read_deck_txt(fname):
    deck = {}

    guj_word = None
    eng_word = None
    meaning = []

    with open(fname, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line=="":
                meaning = "\n".join(meaning)
                assert None not in [guj_word, eng_word]
                assert meaning!=""

                deck[guj_word] = (eng_word, meaning)
                guj_word = None
                eng_word = None
                meaning = []
            else:
                if guj_word is None:
                    guj_word = line
                elif eng_word is None:
                    eng_word = line
                else:
                    meaning.append(line)
        if meaning!=[]:
            deck[guj_word] = (eng_word, meaning)
    return deck


def main(page: ft.Page):
    page.title = "Satsang Vocabulary App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.resizable = False

    page.window.height = 886 # 2532
    page.window.width = 410 # 1170

    page.fonts = {"Roboto Condensed" : "RobotoCondensed-Regular.ttf",
                  "Playfair Display Extra Bold" : "fonts/PlayfairDisplay-ExtraBold.ttf"}

    page.theme = ft.Theme(font_family="Roboto Condensed")

    page.update()

    # All Decks
    """
    decks = OrderedDict()
    for fname in sorted(list(glob.glob(f"decks/*txt"))):
        decks[os.path.basename(fname).strip(".txt")] = read_deck_txt(fname)
    print(decks)
    """
    decks = OrderedDict([('Deck 1 - 15 Nov 2024', {'\ufeffરત્નત્રય': ('ratnatray', 'Samyak Darshan (Faith)\nSamyak Gnaan (Knowledge)\nSamyak Charitra (Conduct)'), 'નય': ('nay', 'Point of View'), 'કૃત્રિમ': ('Krutrim', 'Artificial'), 'નિર્મલ, સમલ': ('Nirmal, Samal', 'without-impurities, with-impurities'), 'પ્રેરક, પ્રેરણા, પ્રેરિત': ('prerak, prerna, prerit', 'inspirer, inspiration, inspired'), 'પ્રીતિ and પ્રતીતિ': ('priti and pratiti', 'love and conviction'), 'પૂર્ણ and પરિપૂર્ણ': ('purna and pari-purna', 'full / complete and so full / complete that nothing more can be added'), 'અવ્યાબાધ': ('avyabadha', 'unobstructed'), 'તીર્થપતિ': ('Tirthpati', 'creator of Tirth - Tirthankar'), 'ત્રિકાળ': ('trikaal', 'past, present and future'), 'આપ and પર': ('aap and par', 'me and others')}), ('Deck 2 - 7 Dec 2024', {'\ufeffવિસ્તાર': ('vistara', 'area, expanse, elaborate'), 'માહિતી': ('mahiti', 'information'), 'ભેદ': ('bhed', 'differences, categories'), 'પ્રમાણ': ('pramaan', 'proof'), 'ઉપમા': ('upama', 'simile, comparison'), 'મત': ('mat', 'opinion'), 'લઘુ and ગુરુ': ('Laghu and Guru', 'light and heavy\nsmall and big'), 'અચલ': ('achal', 'immovable'), 'મલિનતા': ('malinta', 'impurity, dirtiness, filthiness'), 'ચંચળતા': ('chanchalta', 'restlessness'), 'યોગ and જોગ': ('yog and jog', 'association and utilizing the association')})])
   
    all_deck_names = list(decks.keys()) 

    # create application instance
    page_props = {"width" : page.width,
                  "height" : page.height}

    # Objects
    #flashcard_app = FlashCardApp(page, page_props, all_deck_names) # deck, page_props)
    #deck = Deck(deck, page_props)

    # add application's root control to the page
    #page.go("/")

    # Orchestrator
    orchestrator = Orchestrator(page, decks)
    orchestrator.start()


#ft.app(target=main)
ft.app(target=main, assets_dir="assets")
#ft.app(target=main, port=8550, view=ft.AppView.WEB_BROWSER)
