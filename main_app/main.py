import flet as ft



class FlashCardApp(ft.Column):
    def __init__(self, vocab): #, page_props):
        super().__init__()
        self.vocab = vocab
        #self.page_props = page_props
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
                    content=ft.Text(self.curr_word, size=60),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.AMBER_200,
                    width="50vw", # self.page_props["width"] * 0.5, # "50vw",
                    height="50vh", # self.page_props["height"] * 0.4, # "50vh",
                    border_radius=10,
                    ink=True,
                    on_click=self.show_meaning,
                )
        ]

        if not self.first_display:
            self.update()
        else:
            self.first_display = False

    def show_meaning(self, e):
        self.controls = [
                ft.Container(
                    content=ft.Text(self.curr_word + "\n" + self.vocab[self.curr_word], size=60),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.LIGHT_BLUE_ACCENT_200,
                    #width=self.page_props["width"] * 0.5, # "50vw",
                    #height=self.page_props["height"] * 0.4, # "50vh",
                    width="50vw", # self.page_props["width"] * 0.5, # "50vw",
                    height="50vh", # self.page_props["height"] * 0.4, # "50vh",
                    border_radius=10,
                    ink=True,
                    on_click=self.show_next_word,
                )
        ]
        """
            ,
                ft.ElevatedButton(
                    "I knew this word",
                    width=self.page_props["width"] * 0.5, # "50vw",
                    height=self.page_props["height"] * 0.05, # "50vh",
                    bgcolor=ft.colors.GREEN_100,
                    icon="check_rounded",
                    icon_color="green500",
                    color=ft.colors.GREEN_500,
                    on_click=self.show_next_word
                ),
                ft.ElevatedButton(
                    "I didn't know this word",
                    width=self.page_props["width"] * 0.5, # "50vw",
                    height=self.page_props["height"] * 0.05, # "50vh",
                    bgcolor=ft.colors.RED_100,
                    icon="cancel_rounded",
                    icon_color="red500",
                    color=ft.colors.RED_500,
                    on_click=self.show_next_word
                ),
        ]
        """
        self.update()
        """
        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            self.tasks,
        ]
        """


def main(page: ft.Page):
    page.title = "To-Do App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # Dictionary
    vocab = {"નય" : ("nay", "point of view, dimension"),
             "અહંકાર" : ("ahankaar", "ego")}
    vocab = dict([(f"{k}  |  {v[0]}", v[1])for k,v in vocab.items()])
    keys = list(vocab.keys())

    # create application instance
    #page_props = {"width" : page.window.width,
    #              "height" : page.window.height}
    flashcard_app = FlashCardApp(vocab) #, page_props)

    # add application's root control to the page
    page.add(flashcard_app)


ft.app(target=main)

