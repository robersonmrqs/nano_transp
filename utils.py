import webbrowser
from datetime import datetime
from tkinter import messagebox

def update_time(page):
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    page.time_label.configure(text = now)
    page.window.after(1000, update_time, page)
    
def validate_email(email):
        return "@" in email
    
def generate_nf():
    url = "https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional%2fDPS%2fPessoas"
    webbrowser.open(url)