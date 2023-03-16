from customtkinter import CTk, CTkButton, CTkFrame, CTkEntry, CTkLabel, CTkSwitch,\
    set_appearance_mode, get_appearance_mode


class Settings:
    BTN_WIDTH, PADDING, FRAMES_CR, BUTTONS_CR, S_PADDING = 60, 10, 0, 5, 1
    MENU_BAR_HEIGHT, HEADING_HEIGHT, FOOTING_HEIGHT, SEARCH_ENTRY_WIDTH = 30, 50, 30, 300
    ICON_WIDTH, ICON_HEIGHT = 275, 200

    APP_NAME = "Solvemates"
    HOME_BTN_TEXT, CATEGORIES_BTN_TEXT, LOG_IN_BTN_TEXT, ICON_BTN_TEXT = "Home", "Categories", "Log in", "View"
    SETTINGS_BTN_TEXT, ADD_BTN_TEXT = "Settings", "Add"

    TEXT_CLR, BTN_CLR, FRAME_CLR = ("#FFFCF7", "#536270"), ("#738290", "#C2D8B9"), ("#E4F0D0", "#536270")
    ICON_FG_CLR, MAIN_FRAME_CLR, LABEL_TEXT_CLR = ("#FFFCF7", "#91A5C8"), ("#B1C5D8", "#000000"), ("#536270", "#FFFCF7")


class Functions:
    log_in, open_problem = None, None


class Icon(CTkFrame):
    def __init__(self, master, num, data=None):
        super(Icon, self).__init__(master, Settings.ICON_WIDTH, Settings.ICON_HEIGHT,  # Settings.FRAMES_CR,
                                   fg_color=Settings.ICON_FG_CLR)
        self.label = CTkLabel(self, Settings.ICON_WIDTH//2, Settings.ICON_HEIGHT, text=f"Problem {num}",
                              text_color=Settings.LABEL_TEXT_CLR)  # , text=data.description)
        self.label.pack(side="left")
        self.button = CTkButton(self, fg_color=Settings.BTN_CLR, text=Settings.ICON_BTN_TEXT,
                                command=lambda: Functions.open_problem(num), text_color=Settings.TEXT_CLR)
        self.button.pack(side="bottom")


class SearchFrame(CTkFrame):
    def __init__(self, master, height=Settings.MENU_BAR_HEIGHT, placeholder=None):
        super(SearchFrame, self).__init__(master, corner_radius=0, height=height, fg_color=Settings.FRAME_CLR)
        self.search_entry = CTkEntry(self, Settings.SEARCH_ENTRY_WIDTH, height, placeholder_text=placeholder,
                                     text_color=Settings.TEXT_CLR)
        self.search_button = CTkButton(self, Settings.BTN_WIDTH, height, Settings.BUTTONS_CR, text_color=Settings.TEXT_CLR,
                                       text="Search", command=self.search, fg_color=Settings.BTN_CLR)
        self.search_entry.grid(row=0, column=0)
        self.search_button.grid(row=0, column=1)

    def search(self):
        print(self.search_entry.get())


def open_settings():
    def change_appearance():
        if settings_window.dark_switch.get():
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    settings_window = CTk()
    settings_window.wm_title("Settings")
    settings_window.minsize(300, 200)
    settings_window.wm_resizable(False, False)
    settings_window.dark_switch = CTkSwitch(settings_window,
                                            state="active" if get_appearance_mode() == "Dark" else "normal",
                                            text="Dark mode", command=change_appearance)
    settings_window.dark_switch.pack()
    settings_window.mainloop()


def main():
    pass


if __name__ == '__main__':
    main()
