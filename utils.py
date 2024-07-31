import subprocess
import tkinter as tk
import tempfile
import webbrowser
from datetime import datetime
from tkinter import filedialog, messagebox

class ToolTip:

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip is not None:
            return
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background = "lightyellow", relief = "solid", borderwidth = 1)
        label.pack()

    def hide_tooltip(self, event = None):
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None

def update_time(page):
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    page.time_label.configure(text = now)
    page.window.after(1000, update_time, page)
    
def open_github_profile():
    webbrowser.open('https://github.com/robersonmrqs?tab=repositories')

def toggle_password_visibility(entry, show_password_var):
    if show_password_var.get():
        entry.configure(show = '')
    else:
        entry.configure(show = '*')

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

def select_file(textarea_textbox, widget_instance):
    file_path = filedialog.askopenfilename()
    if file_path:
        textarea_textbox.insert('1.0', f"Arquivo selecionado: {file_path}\n")
        widget_instance.file_path = file_path
    else:
        messagebox.showerror(title = 'Cadastro de receita', message = 'Nenhum arquivo selecionado!')
    
def generate_nf():
    url = "https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional%2fDPS%2fPessoas"
    webbrowser.open(url)

def open_whatsapp(telefone):
    telefone_link = f'https://wa.me/{telefone}'
    webbrowser.open(telefone_link)

def open_voucher(blob_data):
    temp_file = tempfile.NamedTemporaryFile(delete = False, suffix = '.pdf')
    temp_file.close()
    save_blob_to_file(blob_data, temp_file.name)
    webbrowser.open(temp_file.name)

def save_blob_to_file(blob_data, filename):
    with open(filename, 'wb') as file:
        file.write(blob_data)

def open_calculator():
    subprocess.Popen(['calc.exe'])

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")