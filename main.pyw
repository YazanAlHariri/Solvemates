import App
from customtkinter import CTkFrame, CTkButton, CTkScrollableFrame, CTkLabel, CTkFont
import Data


Settings = App.Settings
Functions = App.Functions


class Window(App.CTk):
    def __init__(self):
        super(Window, self).__init__()
        self.configure(bg=Settings.FRAME_CLR)
        self.wm_title(Settings.APP_NAME)
        self.iconbitmap(default="./icon.ico")
        self.minsize(600, 400)

        self.menu_bar = CTkFrame(self, height=Settings.MENU_BAR_HEIGHT, corner_radius=Settings.FRAMES_CR,
                                 fg_color=Settings.FRAME_CLR)
        self.main_frame = CTkFrame(self, corner_radius=Settings.FRAMES_CR, fg_color=Settings.FRAME_CLR)
        self.menu_bar.pack(fill="x")
        self.main_frame.pack(expand=True, fill="both")

        # Menu bar setup
        self.menu_bar.left_side = CTkFrame(self.menu_bar, height=Settings.MENU_BAR_HEIGHT,
                                           corner_radius=Settings.FRAMES_CR, fg_color=Settings.FRAME_CLR)
        self.menu_bar.right_side = CTkFrame(self.menu_bar, height=Settings.MENU_BAR_HEIGHT,
                                            corner_radius=Settings.FRAMES_CR, fg_color=Settings.FRAME_CLR)
        self.menu_bar.middle = CTkFrame(self.menu_bar, height=Settings.MENU_BAR_HEIGHT,
                                        corner_radius=Settings.FRAMES_CR, fg_color=Settings.FRAME_CLR)
        self.menu_bar.left_side.pack(side="left"), self.menu_bar.right_side.pack(side="right")
        self.menu_bar.middle.pack(expand=True, fill="x")

        self.home_button = CTkButton(self.menu_bar.left_side, Settings.BTN_WIDTH, Settings.MENU_BAR_HEIGHT,
                                     Settings.BUTTONS_CR, text=Settings.HOME_BTN_TEXT, fg_color=Settings.BTN_CLR,
                                     text_color=Settings.TEXT_CLR)
        self.categories_button = CTkButton(self.menu_bar.left_side, Settings.BTN_WIDTH, Settings.MENU_BAR_HEIGHT,
                                           Settings.BUTTONS_CR, text=Settings.CATEGORIES_BTN_TEXT,
                                           fg_color=Settings.BTN_CLR, text_color=Settings.TEXT_CLR)
        self.home_button.grid(row=0, column=0, padx=Settings.S_PADDING, pady=Settings.S_PADDING)
        self.categories_button.grid(row=0, column=1, padx=Settings.S_PADDING, pady=Settings.S_PADDING)

        self.account_button = CTkButton(self.menu_bar.right_side, Settings.BTN_WIDTH, Settings.MENU_BAR_HEIGHT,
                                        Settings.BUTTONS_CR, text=Settings.LOG_IN_BTN_TEXT, command=Functions.log_in,
                                        fg_color=Settings.BTN_CLR, text_color=Settings.TEXT_CLR)
        self.settings_button = CTkButton(self.menu_bar.right_side, Settings.BTN_WIDTH, Settings.MENU_BAR_HEIGHT,
                                         Settings.BUTTONS_CR, text=Settings.SETTINGS_BTN_TEXT, fg_color=Settings.BTN_CLR,
                                         command=App.open_settings, text_color=Settings.TEXT_CLR)
        self.account_button.grid(row=0, column=1, padx=Settings.S_PADDING, pady=Settings.S_PADDING)
        self.settings_button.grid(row=0, column=0, padx=Settings.S_PADDING, pady=Settings.S_PADDING)

        # Main frame setup
        self.bind("<Configure>", self.resize)
        self.icons_setup = 0
        self.main_frame.heading = CTkFrame(self.main_frame, height=Settings.HEADING_HEIGHT,
                                           corner_radius=Settings.FRAMES_CR, fg_color=Settings.FRAME_CLR)
        self.main_frame.scrollable_frame = CTkScrollableFrame(self.main_frame, corner_radius=Settings.FRAMES_CR,
                                                              fg_color=Settings.MAIN_FRAME_CLR)
        self.main_frame.footing = CTkFrame(self.main_frame, height=Settings.FOOTING_HEIGHT,
                                           corner_radius=Settings.FRAMES_CR, fg_color=Settings.FRAME_CLR)

        self.heading_label = CTkLabel(self.main_frame.heading, text="Problems", font=CTkFont(size=30),
                                      text_color=Settings.LABEL_TEXT_CLR)
        self.search_bar = App.SearchFrame(self.main_frame.heading, placeholder="Search for a problem...",
                                          height=Settings.HEADING_HEIGHT - (Settings.PADDING * 2))
        self.main_frame.heading.pack(fill="x")
        self.heading_label.pack(side="left", padx=Settings.PADDING)
        self.search_bar.pack(side="right", padx=Settings.PADDING, pady=Settings.PADDING)

        self.main_frame.scrollable_frame.pack(expand=True, fill="both")
        self.icons = [App.Icon(self.main_frame.scrollable_frame, n) for n in range(100)]
        self.grid_icons(2)

        self.main_frame.footing.pack(fill="x")
        self.add_button = CTkButton(self.main_frame.footing, Settings.BTN_WIDTH, Settings.FOOTING_HEIGHT,
                                    Settings.BUTTONS_CR, text=Settings.ADD_BTN_TEXT, fg_color=Settings.BTN_CLR,
                                    text_color=Settings.TEXT_CLR)
        self.add_button.pack(side="right", pady=Settings.S_PADDING)

    def resize(self, event):
        if event.widget != self.winfo_toplevel():
            return
        if event.width > 1750:
            self.grid_icons(4)
        elif event.width > 1325:
            self.grid_icons(3)
        elif event.width > 900:
            self.grid_icons(2)

    def grid_icons(self, setup_num=3):
        if self.icons_setup == setup_num:
            return
        self.icons_setup = setup_num
        for n, button in enumerate(self.icons):
            button.grid(row=n // setup_num, column=n % setup_num, padx=Settings.PADDING, pady=Settings.PADDING)


def main():
    window = Window()
    window.mainloop()


if __name__ == '__main__':
    main()
