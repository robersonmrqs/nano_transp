import webbrowser
from datetime import datetime
from tkinter import messagebox

def update_time(page):
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    page.time_label.configure(text = now)
    page.window.after(1000, update_time, page)
    
def open_github_profile(self):
        webbrowser.open('https://github.com/robersonmrqs?tab=repositories')

def clean_widgets(entries, checkbuttons = None, file_path_attr = None, obj = None):
    for entry in entries:
        entry.delete(0, 'end')
    if checkbuttons:
        for var in checkbuttons:
            var.set(0)
    if file_path_attr and obj:
        setattr(obj, file_path_attr, None)

def validate_email(email):
        return "@" in email
    
def generate_nf():
    url = "https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional%2fDPS%2fPessoas"
    webbrowser.open(url)