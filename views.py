import customtkinter as ctk
import re
import webbrowser
import win32com.client as win32
from datetime import datetime
from models import *
from PIL import Image
from tkinter import messagebox

class LoginPage():

    def __init__(self, window):
        self.window = window
        self.window.title('Login page')
        self.window.geometry('500x560')
        self.window.resizable(False, False)
        self.login_frame = ctk.CTkFrame(window)
        users_table()

        self.logo = ctk.CTkLabel(self.window, image = ctk.CTkImage(Image.open('static/images/logo_nano_transportes.jpg'), size = (500, 285)), compound = 'top', height = 0, text = '').place(x = 0, y = 0)
        self.frame = ctk.CTkFrame(self.window, bg_color = '#fdfdfd', width = 500, height = 515, fg_color = '#ffffff').place(x = 0, y = 185)
        self.username_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 24), text = 'Usuário', text_color = '#020304').place(x = 30, y = 220)
        self.username_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 440, height = 40, corner_radius = 15, border_width = 0, fg_color = '#e8e9ea', text_color = '#010203', justify = 'center')
        self.username_entry.place(x = 30, y = 250)
        self.password_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 24), text = 'Senha', text_color = '#020304').place(x = 30, y = 310)
        self.password_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 440, height = 40, corner_radius = 15, border_width = 0, fg_color = '#e8e9ea', text_color = '#010203', justify = 'center', show = '*')
        self.password_entry.place(x = 30, y = 340)
        self.recover_password_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Recuperar senha', fg_color = '#ffffff', text_color = '#000000', hover_color = '#ffa87d', command = self.recover_password).place(x = 175, y = 395)
        self.login_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 24), width = 160, height = 45, corner_radius = 22, text = 'LOGIN', fg_color = '#ff8040', hover_color = '#ffa87d', text_color = '#010203', command = self.login).place(x = 170, y = 435)
        self.text1_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Não tem uma conta? clique', text_color = '#000000').place(x = 120, y = 490)
        self.register_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'aqui', width = 0, fg_color = '#ffffff', text_color = '#000000', hover_color = '#ffa87d', command = lambda: [self.window.withdraw(), RegisterPage(self.window)]).place(x = 340, y = 490)
        self.github_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 14), text = 'Made by Rb', fg_color = '#ffffff', text_color = '#0080ff', hover_color = '#ffffff', command = self.open_github_profile).place(x = 0, y = 530)
        self.exit_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Sair', width = 100, fg_color = '#d70428', corner_radius = 14, hover_color = '#af0850', command = self.window.quit).place(x = 200, y = 530)
        self.window.bind('<Return>', lambda event = None: self.login())

        self.time_label = ctk.CTkLabel(self.window, font = ctk.CTkFont('verdana', size = 10), text = '', text_color = '#ffffff')
        self.time_label.place(x = 390, y = 0)
        self.update_time()

    def update_time(self):
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.time_label.configure(text = now)
        self.window.after(1000, self.update_time)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror(title = 'User login', message = 'Por favor, preencha usuário e senha!')
            return
        
        user_found = get_user_details(username = username)
        if user_found and user_found[4] == password:
            messagebox.showinfo(title = 'User login', message = 'Login realizado com sucesso!')
            self.window.withdraw()
            OptionPage(self.window, username)
        else:
            messagebox.showerror(title = 'User login', message = 'Usuário e ou senha incorretos!')

    def recover_password(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror(title = 'User login', message = 'Por favor, preencha o nome de usuário!')
            return
        
        user_found = get_user_details(username = username)
        if not user_found:
            messagebox.showerror(title = 'User login', message = 'Usuário não encontrado!')
            return

        email = user_found[2]
        password = user_found[4]
        outlook = win32.Dispatch('outlook.application')
        email_message = outlook.CreateItem(0)
        email_message.To = email
        email_message.Subject = 'Recuperação de Senha'
        email_message.HTMLBody = f'<p>Olá,</p><p>Sua senha é: {password}</p><p>Abraços!</p><p>Nano Transportes</p>'

        try:
            email_message.Send()
            messagebox.showinfo(title = "User login", message = f'Senha enviada com sucesso para {email}!')
        except Exception as e:
            messagebox.showerror(title = 'User login', message = f'Ocorreu um erro ao enviar o email: {e}!')  

    def open_github_profile(self):
        webbrowser.open('https://github.com/robersonmrqs?tab=repositories')

class RegisterPage():
    
    def __init__(self, window):
        self.window = ctk.CTkToplevel(window)
        self.window.title('Register Page')
        self.window.geometry('500x670')
        self.window.resizable(False, False)
        self.window.transient(window)
        self.register_frame = ctk.CTkFrame(window)
        
        self.logo = ctk.CTkLabel(self.window, image = ctk.CTkImage(Image.open('static/images/logo_nano_transportes.jpg'), size = (500, 220)), compound = 'top').place(x = 0, y = 0)
        self.frame = ctk.CTkFrame(self.window, width = 500, height = 600, fg_color = '#ffffff').place(x = 0, y = 125)
        self.text1_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 12), text = '*Todos os campos são obrigatórios', text_color = '#e1031e').place(x = 30, y = 130)
        self.name_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = 'Nome', text_color = '#000000').place(x = 210, y = 160)
        self.name_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 440, height = 36, fg_color = '#e9ebea', corner_radius = 15, border_width = 0, text_color = '#010203', justify = 'center')
        self.name_entry.place(x = 30, y = 190)
        self.email_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = 'Email', text_color = '#000000').place(x = 210, y = 240)
        self.email_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 440, height = 36, fg_color = '#e9ebea', corner_radius = 15, border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = 'fulano@email.com')
        self.email_entry.place(x = 30, y = 270)
        self.username_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = 'Nome de usuário', text_color = '#000000').place(x = 165, y = 320)
        self.username_entry = ctk.CTkEntry(self.window,bg_color='#ffffff', font = ctk.CTkFont('verdana',size = 18), width = 440, height = 36, fg_color = '#e9ebea', corner_radius = 15, border_width = 0, text_color = '#010203', justify = 'center')
        self.username_entry.place(x = 30, y = 350)
        self.password_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = 'Senha', text_color = '#000000').place(x = 215, y = 395)
        self.password_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 440, height = 36, fg_color = '#e9ebea', corner_radius = 15, border_width = 0, text_color = '#010203', justify = 'center', show = '*')
        self.password_entry.place(x = 30, y = 425)
        self.confirm_password_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = 'Confirmar senha', text_color = '#000000').place(x = 160, y = 475)
        self.confirm_password_entry = ctk.CTkEntry(self.window,bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 440, height = 36, fg_color = '#e9ebea', corner_radius = 15, border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = 'confirme sua senha', show = '*')
        self.confirm_password_entry.place(x = 30, y = 505)
        self.register_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 24), text = 'Criar conta', width = 160, height = 45, corner_radius = 22, fg_color = '#ff8040', hover_color = '#ffa87d', text_color = '#000000', command = self.register).place(x = 150, y = 565)
        self.texto_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 14), text = 'Made by Rb', text_color = '#0080ff').place(x = 10, y = 635)
        self.exit_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Sair', width = 100, corner_radius = 14, fg_color = '#eb0214', hover_color = '#af0850', command = self.window.quit).place(x = 195, y = 635)
        self.comeback_button = ctk.CTkButton(self.window, bg_color = '#00FF00', font = ctk.CTkFont('verdana', size = 16), text = 'voltar', width = 0, corner_radius = 0, fg_color = '#80ff80', text_color = '#000000',  hover_color = '#4dcea7', command = lambda: [self.window.destroy, LoginPage(self.window)]).place(x = 0, y = 0)
        self.window.bind('<Return>', lambda event = None: self.register())

    def validate_email(self, email):
        return "@" in email
    
    def check_password(self, password):
        if len(password) < 8:
            return False
        elif re.search('[0-9]', password) is None:
            return False
        elif re.search('[A-Z]', password) is None: 
            return False
        elif re.search('[^a-zA-Z0-9]', password) is None:
            return False
        else:
            return True

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not name or not email or not username or not password or not confirm_password:
            messagebox.showerror(title = 'User registration', message = 'Por favor, preencha todos os campos!')
        elif not self.validate_email(email):
            messagebox.showerror(title = 'User Registration', message = 'Email inválido!')
        elif not self.check_password(password):
            messagebox.showerror(title = 'User registration', message = 'A senha não atende aos requisitos!')
        elif password != confirm_password:
            messagebox.showerror(title = 'User registration', message = 'Senhas não conferem!')
        elif get_user_details(username = username, email = email):
            messagebox.showerror(title = 'User registration', message = 'Usuário já cadastrado!')
        else:
            register_user(name, email, username, password)
            messagebox.showinfo(title = 'User registration', message = 'Usuário cadastrado com sucesso!')
            LoginPage(self.window)

class OptionPage():
    
    def __init__(self, window, user):
        self.username = user
        self.window = ctk.CTkToplevel(window)
        self.window.title('Option Page')
        self.window.geometry('500x730')
        self.window.resizable(False, False)
        self.window.transient(window)
        
        self.frame = ctk.CTkFrame(self.window, bg_color = '#ffffff', width = 500, height = 730, fg_color = '#ffffff', border_color = '#ffffff').place(x = 0, y = 0)
        self.text1_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = 'Ola,', text_color = '#000000').place(x = 180, y = 30)
        self.text2_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = f' {self.username}', text_color = '#d70428').place(x = 220, y = 30)
        self.text3_label = ctk.CTkLabel(self.window, bg_color = "#ffffff", font = ctk.CTkFont('verdana', size = 20), text = "O que vc gostaria de fazer hoje?", text_color = '#000000').place(x = 80, y = 60)
        self.text4_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 14), text = 'Made by Rb', text_color = '#0080ff').place(x = 10, y = 700)
        self.exit_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Sair', width = 100, corner_radius = 14, fg_color = '#d70428', text_color = '#ffffff', hover_color = '#af0850', command = self.window.quit).place(x = 200, y = 700)
        self.comeback_button = ctk.CTkButton(self.window, bg_color = '#00FF00', font = ctk.CTkFont('verdana', size = 16), text = 'voltar', width = 0, corner_radius = 0, fg_color = '#80ff80', text_color = '#000000',  hover_color = '#4dcea7', command = lambda: [self.window.destroy, LoginPage(self.window)]).place(x = 0, y = 0)
        self.combobox1 = ctk.CTkOptionMenu(self.window, values = ['Cadastrar', 'Pesquisar', 'Controle de frota'], bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), fg_color = '#ff8040', dropdown_fg_color = '#ff8040', dropdown_hover_color = '#ffa87d', text_color = '#000000', command = self.select_option).place(x = 50, y = 110)
        self.combobox2 = None
        self.frames = {}
        self.current_frame = None

    def select_option(self, option):
        if option == 'Cadastrar':
            self.show_combobox2()
        elif option == 'Pesquisar':
            self.window.withdraw(), QueryPage(self.window, self.username)
        elif option == 'Controle de frota':
            self.window.withdraw(), FleetPage(self.window, self.username)
        else:
            self.hide_combobox2()

    def show_combobox2(self):
        if self.combobox2 is None:
            self.combobox2 = ctk.CTkOptionMenu(self.window, values = ['Clientes', 'Receitas', 'Despesas'], bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), fg_color = '#ff8040', dropdown_fg_color = '#ff8040', dropdown_hover_color = '#ffa87d', text_color = '#000000', command = self.select_frame)
            self.combobox2.place(x = 300, y = 110)

    def select_frame(self, option_frame):
        if option_frame == 'Clientes':
            self.show_frame('Clientes', self.frame_clients)
        elif option_frame == 'Receitas':
            self.show_frame('Receitas', self._frame_income)
        else:
            self.show_frame('Despesas', self._frame_expenses)

    def hide_combobox2(self):
        if self.combobox2 is not None:
            self.combobox2.destroy()
            self.combobox2 = None

    def show_frame(self, name, frame_func):
        if name in self.frames:
            frame = self.frames[name]
        else:
            frame = frame_func()
            frame.place(x = 0, y = 150, relwidth = 1, relheight = 0.75)
            self.frames[name] = frame

        if self.current_frame:
            self.current_frame.lower()

        frame.lift()
        self.current_frame = frame

    def generate_nf(self):
        url = "https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional%2fDPS%2fPessoas"
        webbrowser.open(url)