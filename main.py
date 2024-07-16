import customtkinter as ctk
from views.login import LoginPage

def main():
    window = ctk.CTk()
    LoginPage(window)
    window.mainloop()

if __name__ == "__main__":
    main()