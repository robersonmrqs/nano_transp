import customtkinter as ctk
from views import *

def main():
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')

    window = ctk.CTk()
    LoginPage(window)
    window.mainloop()

if __name__ == "__main__":
    main()