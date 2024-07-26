import customtkinter as ctk
import re
import webbrowser
import tempfile
import subprocess
import win32com.client as win32
from models import *
from utils import *
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
        self.login_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 24), width = 160, height = 45, corner_radius = 22, text = 'LOGIN', fg_color = '#ff8040', hover_color = '#ffa87d', text_color = '#010203', command = self.user_login).place(x = 170, y = 435)
        self.text1_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Não tem uma conta? clique', text_color = '#000000').place(x = 120, y = 490)
        self.register_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'aqui', width = 0, fg_color = '#ffffff', text_color = '#000000', hover_color = '#ffa87d', command = lambda: [self.window.withdraw(), RegisterPage(self.window)]).place(x = 340, y = 490)
        self.github_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 14), text = 'Made by Rb', fg_color = '#ffffff', text_color = '#0080ff', hover_color = '#ffffff', command = open_github_profile).place(x = 0, y = 530)
        self.exit_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Sair', width = 100, fg_color = '#d70428', corner_radius = 14, hover_color = '#af0850', command = self.window.quit).place(x = 200, y = 530)
        self.time_label = ctk.CTkLabel(self.window, font = ctk.CTkFont('verdana', size = 10), text = '', text_color = '#ffffff')
        self.time_label.place(x = 390, y = 0)
        self.window.bind('<Return>', lambda event = None: self.user_login())
        update_time(self)

    def user_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror(title = 'Login de usuário', message = 'Por favor, preencha usuário e senha!')
            return
        
        user_found = get_user_details(username = username)
        if user_found and user_found[4] == password:
            messagebox.showinfo(title = 'Login de usuário', message = 'Login realizado com sucesso!')
            self.window.withdraw()
            OptionPage(self.window, username, f'{username}_nano_transp.db')
        else:
            messagebox.showerror(title = 'Login de usuário', message = 'Usuário e ou senha incorretos!')

    def recover_password(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror(title = 'Login de usuário', message = 'Por favor, preencha o nome de usuário!')
            return
        
        user_found = get_user_details(username = username)
        if not user_found:
            messagebox.showerror(title = 'Login de usuário', message = 'Usuário não encontrado!')
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
            messagebox.showinfo(title = 'Login de usuário', message = f'Senha enviada com sucesso para {email}!')
        except Exception as e:
            messagebox.showerror(title = 'Login de usuário', message = f'Ocorreu um erro ao enviar o email: {e}!')

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
        self.register_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 24), text = 'Criar conta', width = 160, height = 45, corner_radius = 22, fg_color = '#ff8040', hover_color = '#ffa87d', text_color = '#000000', command = self.user_registration).place(x = 150, y = 565)
        self.texto_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 14), text = 'Made by Rb', text_color = '#0080ff').place(x = 10, y = 635)
        self.exit_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Sair', width = 100, corner_radius = 14, fg_color = '#eb0214', hover_color = '#af0850', command = self.window.quit).place(x = 195, y = 635)
        self.comeback_button = ctk.CTkButton(self.window, bg_color = '#00FF00', font = ctk.CTkFont('verdana', size = 16), text = 'voltar', width = 0, corner_radius = 0, fg_color = '#80ff80', text_color = '#000000',  hover_color = '#4dcea7', command = lambda: [self.window.destroy, LoginPage(self.window)]).place(x = 0, y = 0)
        self.time_label = ctk.CTkLabel(self.window, font = ctk.CTkFont('verdana', size = 10), text = '', text_color = '#ffffff')
        self.time_label.place(x = 390, y = 0)
        self.window.bind('<Return>', lambda event = None: self.user_registration())
        update_time(self)
    
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

    def user_registration(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not name or not email or not username or not password or not confirm_password:
            messagebox.showerror(title = 'Cadastro de usuário', message = 'Por favor, preencha todos os campos!')
        elif not validate_email(email):
            messagebox.showerror(title = 'Cadastro de usuário', message = 'Email inválido!')
        elif not self.check_password(password):
            messagebox.showerror(title = 'Cadastro de usuário', message = 'A senha não atende aos requisitos!')
        elif password != confirm_password:
            messagebox.showerror(title = 'Cadastro de usuário', message = 'Senhas não conferem!')
        elif get_user_details(username = username) or get_user_details(email = email):
            messagebox.showerror(title = 'Cadastro de usuário', message = 'Usuário ou email já cadastrado!')
        else:
            register_user(name, email, username, password)
            messagebox.showinfo(title = 'Cadastro de usuário', message = 'Usuário cadastrado com sucesso!')
            LoginPage(self.window)

class OptionPage():
    
    def __init__(self, window, user, user_db_name):
        self.username = user
        self.user_db_name = user_db_name
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
        self.time_label = ctk.CTkLabel(self.window, font = ctk.CTkFont('verdana', size = 10), text = '', text_color = '#ffffff')
        self.time_label.place(x = 390, y = 0)
        update_time(self)
        self.combobox2 = None
        self.frames = {}
        self.current_frame = None

    def select_option(self, option):
        if option == 'Cadastrar':
            self.show_combobox2()
        elif option == 'Pesquisar':
            self.window.withdraw(), QueryPage(self.window, self.username)
        elif option == 'Controle de frota':
            self.window.withdraw(), FleetPage(self.window, self.username, f'{self.user_db_name}')
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
            self.show_frame('Receitas', self.frame_incomes)
        else:
            self.show_frame('Despesas', self.frame_expenses)

    def hide_combobox2(self):
        if self.combobox2 is not None:
            self.combobox2.destroy()
            self.combobox2 = None

    def frame_clients(self):
        self.frame = ctk.CTkFrame(self.window, width = 500, fg_color = '#B8860B', bg_color = '#B8860B')
        self.frame.place(x = 0, y = 150)
        self.text1_label = ctk.CTkLabel(self.frame, bg_color = '#B8860B', font = ctk.CTkFont('verdana', size = 14), text = 'CADASTRO DE CLIENTES', fg_color = '#B8860B', text_color = '#ffffff').place(x = 165, y = 5)
        self.create_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Criar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.customer_registration).place(x = 45, y = 50)
        self.update_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Atualizar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.update_client).place(x = 149, y = 50)
        self.read_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Consultar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.customer_inquiry).place(x = 261, y = 50)
        self.delete_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Deletar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.delete_client).place(x = 375, y = 50)
        self.name_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Nome', text_color = '#ffffff').place(x = 45, y = 120)
        self.name_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.name_entry.place(x = 135, y = 115)
        self.address_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Endereço', text_color = '#ffffff').place(x = 45, y = 165)
        self.address_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.address_entry.place(x = 135, y = 160)
        self.email_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Email', text_color = '#ffffff').place(x = 45, y = 210)
        self.email_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = 'fulano@email.com')
        self.email_entry.place(x = 135, y = 205)
        self.phone_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Fone', text_color = '#ffffff').place(x = 45, y = 255)
        self.phone_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = '+55(__)')
        self.phone_entry.place(x = 135, y = 250)
        self.contact_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Contato', text_color = '#ffffff').place(x = 45, y = 297)
        self.contact_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.contact_entry.place(x = 135, y = 297)
        self.textarea_textbox = ctk.CTkTextbox(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 410, height = 180, fg_color = '#ffffff', text_color = '#000000')
        self.textarea_textbox.place(x = 45, y = 350)
        clients_table(self.user_db_name)
        return self.frame

    def customer_registration(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        contact = self.contact_entry.get().strip()

        if not name or not address or not email or not phone or not contact:
            messagebox.showerror(title = 'Cadastro de cliente', message = 'Por favor, preencha todos os campos!')
            return
        elif not validate_email(email):
            messagebox.showerror(title = 'Cadastro de cliente', message = 'Email inválido!')
            return
        elif not phone.startswith('55'):
            phone = '55' + phone
        
        result = execute_query('SELECT * FROM clients WHERE name = ?', (name,), fetchone = True, db_name=self.user_db_name)  
        if result:
            messagebox.showerror(title = 'Cadastro de cliente', message = f'Cliente {name} já cadastrado!')
            return
        else:
            execute_query('INSERT INTO clients (name, address, email, phone, contact) VALUES (?, ?, ?, ?, ?)', (name, address, email, phone, contact), db_name = self.user_db_name)
            messagebox.showinfo(title = 'Cadastro de cliente', message = f"Cliente '{name}' cadastrado com sucesso!")
            self.clean_customer_widgets()

    def update_client(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        contact = self.contact_entry.get().strip()
    
        if not name or not address or not email or not phone or not contact:
            messagebox.showerror(title = 'Atualização de cliente', message = 'Por favor, preencha todos os campos!')
            return
        elif not validate_email(email):
            messagebox.showerror(title = 'Atualização de cliente', message = 'Email inválido!')
            return
        elif not phone.startswith('55'):
            phone = '55' + phone

        execute_query('UPDATE clients SET address = ?, email = ?, phone = ?, contact = ? WHERE name = ?', (address, email, phone, contact, name), db_name = self.user_db_name)
        messagebox.showinfo(title = 'Atualização de cliente', message = f"Cliente '{name}' atualizado com sucesso!")
        self.clean_customer_widgets()

    def customer_inquiry(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
    
        if not name:
            self.textarea_textbox.insert('1.0', "O campo 'Nome' é obrigatório para consultar.\n")

        result = execute_query('SELECT * FROM clients WHERE name = ?', (name,), fetchall = True, db_name = self.user_db_name)
        if result:
            for row in result:
                self.textarea_textbox.insert('end', f"Nome: {row[1]}\n")
                self.textarea_textbox.insert('end', f"Endereço: {row[2]}\n")
                self.textarea_textbox.insert('end', f"Email: {row[3]}\n")
                self.textarea_textbox.insert('end', f"Telefone: {row[4]}\n")
                self.textarea_textbox.insert('end', f"Contato: {row[5]}\n\n")
        else:
            messagebox.showerror(title = 'Consultar cliente', message = f"Nenhum cliente encontrado para '{name}'!")
    
        self.clean_customer_widgets()

    def delete_client(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
    
        if not name:
            self.textarea_textbox.insert('1.0', "O campo 'Nome' é obrigatório para deletar.\n")
        else:
            execute_query('DELETE FROM clients WHERE name = ?', (name,), db_name = self.user_db_name)
            messagebox.showinfo(title = 'Deletar cliente', message = f"Cliente '{name}' deletado com sucesso!")
            self.clean_customer_widgets()

    def clean_customer_widgets(self):
        entries = [self.name_entry, self.address_entry, self.email_entry, self.phone_entry, self.contact_entry]
        clean_widgets(entries)

    def frame_incomes(self):
        self.frame = ctk.CTkFrame(self.window, width = 500, fg_color = '#000080', bg_color = '#000080')
        self.frame.place(x = 0, y = 150)
        self.text1_label = ctk.CTkLabel(self.frame, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 14), text = 'CADASTRO DE RECEITAS', fg_color = '#000080', text_color = '#ffffff').place(x = 165, y = 5)
        self.create_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Criar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.income_registration).place(x = 45, y = 50)
        self.update_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Atualizar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.update_income).place(x = 149, y = 50)
        self.read_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Consultar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.income_inquiry).place(x = 261, y = 50)
        self.delete_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Deletar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.delete_income).place(x = 375, y = 50)
        self.name_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Nome', text_color = '#ffffff').place(x = 45, y = 120)
        self.name_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.name_entry.place(x = 135, y = 115)
        self.date_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Data', text_color = '#ffffff').place(x = 45, y = 165)
        self.date_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = 'dd/mm/aaaa')
        self.date_entry.place(x = 135, y = 160)
        self.value_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Valor', text_color = '#ffffff').place(x = 45, y = 210)
        self.value_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203')
        self.value_entry.place(x = 135, y = 205)
        self.client_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Cliente', text_color = '#ffffff').place(x = 45, y = 255)
        self.client_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203')
        self.client_entry.place(x = 135, y = 250)
        self.paid_var = ctk.IntVar()
        self.paid_checkbox = ctk.CTkCheckBox(self.frame, text = 'Pago?', font = ctk.CTkFont('verdana', size = 18), variable = self.paid_var, onvalue = 1, offvalue = 0, text_color = '#ffffff')
        self.paid_checkbox.place(x = 45, y = 307)
        self.voucher_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 80, height = 30, text = 'Anexar comprovante', fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = lambda: select_file(self.textarea_textbox, self)).place(x = 135, y = 305)
        self.generate_nf_button = ctk.CTkButton(self.frame, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), width = 80, text = 'Gerar NF', fg_color = '#ff8040', hover_color = '#ffa87d', text_color = '#ffffff', corner_radius = 14, command = generate_nf).place(x = 350, y = 306)
        self.textarea_textbox = ctk.CTkTextbox(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 410, height = 180, fg_color = '#ffffff', text_color = '#000000')
        self.textarea_textbox.place(x = 45, y = 350)
        self.file_path = None
        incomes_table(self.user_db_name)
        return self.frame

    def income_registration(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()
        value = self.value_entry.get().strip()
        client_name = self.client_entry.get().strip()
        paid = self.paid_var.get()

        if not name or not date or not value or not client_name:
            messagebox.showerror(title = 'Cadastro de receita', message = 'Por favor, preencha todos os campos!')
            return
        
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()

        client = execute_query('SELECT id FROM clients WHERE name = ?', (client_name,), fetchone = True, db_name = self.user_db_name)
        if client:
            client_id = client[0]
            execute_query('INSERT INTO incomes (name, date, value, client_id, paid, voucher) VALUES (?, ?, ?, ?, ?, ?)', (name, date, value, client_id, paid, voucher), db_name = self.user_db_name)
            messagebox.showinfo(title = 'Cadastro de receita', message = f"Receita '{name}' criada com sucesso!")
            self.clean_income_widgets()
        else:
            messagebox.showerror(title = 'Cadastro de receita', message = f"Cliente '{client_name}' não encontrado!")

    def update_income(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()
        value = self.value_entry.get().strip()
        client_name = self.client_entry.get().strip()
        paid = self.paid_var.get()

        if not name or not date or not value or not client_name:
            messagebox.showerror(title = 'Atualização de receita', message = 'Por favor, preencha todos os campos!')
            return
        
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()

        client = execute_query('SELECT id FROM clients WHERE name = ?', (client_name,), fetchone = True, db_name = self.user_db_name)
        if client:
            client_id = client[0]
            execute_query('UPDATE incomes SET value = ?, client_id = ?, paid = ?, voucher = ? WHERE name = ? AND date = ?', (value, client_id, paid, voucher, name, date), db_name=self.user_db_name)
            messagebox.showinfo(title = 'Atualização de receita', message = f"Receita '{name}' atualizada com sucesso!")
            self.clean_income_widgets()
        else:
            messagebox.showerror(title = 'Atualização de receita', message = f"Cliente '{client_name}' não encontrado!")

    def income_inquiry(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()

        if not name or not date:
            messagebox.showerror(title = 'Consultar rceita', message = "Os campos 'Nome' e 'Data' são obrigatórios para consultar!")
            return

        result = execute_query('SELECT * FROM incomes WHERE name = ? AND date = ?', (name, date), fetchall = True, db_name = self.user_db_name)
        if result:
            for row in result:
                client_id = row[4]
                client_name_result = execute_query('SELECT name FROM clients WHERE id = ?', (client_id,), fetchone = True, db_name = self.user_db_name)
                client_name = client_name_result[0] if client_name_result else 'Desconhecido'
                formatted_value = f"R$ {row[3]:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
                self.textarea_textbox.insert('end', f'Nome: {row[1]}\n')
                self.textarea_textbox.insert('end', f'Data: {row[2]}\n')
                self.textarea_textbox.insert('end', f'Valor: {formatted_value}\n')
                self.textarea_textbox.insert('end', f'Cliente: {client_name}\n')
                self.textarea_textbox.insert('end', f"Pago: {'Sim' if row[5] else 'Não'}\n")
                self.textarea_textbox.insert('end', f"Comprovante: {'Sim' if row[6] else 'Não'}\n\n")
        else:
            messagebox.showerror(title = 'Consultar receita', message = f"Nenhuma receita encontrada para '{name}' e data '{date}'!")

        self.clean_income_widgets()

    def delete_income(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()

        if not name or not date:
            messagebox.showerror(title = 'Deletar receita', message = "Os campos 'Nome' e 'Data' são obrigatórios para deletar!")
            return

        execute_query('DELETE FROM incomes WHERE name = ? AND date = ?', (name, date), db_name = self.user_db_name)
        messagebox.showinfo(title = 'Deletar receita', message = f"Receita '{name}' e data '{date}' deletada com sucesso!")
        self.clean_income_widgets()

    def clean_income_widgets(self):
        entries = [self.name_entry, self.date_entry, self.value_entry, self.client_entry]
        checkbuttons = [self.paid_var]
        clean_widgets(entries, checkbuttons, 'file_path', self)

    def frame_expenses(self):
        self.frame = ctk.CTkFrame(self.window, width = 500, fg_color = '#006400', bg_color = '#006400')
        self.frame.place(x = 0, y = 150)
        self.text1_label = ctk.CTkLabel(self.frame, bg_color = '#006400', font = ctk.CTkFont('verdana', size = 14), text = 'CADASTRO DE DESPESAS', fg_color = '#006400', text_color = '#ffffff').place(x = 165, y = 5)
        self.create_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Criar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.expense_registration).place(x = 45, y = 50)
        self.update_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Atualizar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.update_expense).place(x = 149, y = 50)
        self.read_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Consultar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.expense_inquiry).place(x = 261, y = 50)
        self.delete_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Deletar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.delete_expense).place(x = 375, y = 50)
        self.name_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Nome', text_color = '#ffffff').place(x = 45, y = 120)
        self.name_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.name_entry.place(x = 135, y = 115)
        self.date_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Data', text_color = '#ffffff').place(x = 45, y = 165)
        self.date_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = 'dd/mm/aaaa')
        self.date_entry.place(x = 135, y = 160)
        self.value_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Valor', text_color = '#ffffff').place(x = 45, y = 210)
        self.value_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.value_entry.place(x = 135, y = 205)
        self.source_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Fonte', text_color = '#ffffff').place(x = 45, y = 255)
        self.source_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.source_entry.place(x = 135, y = 250)
        self.voucher_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 80, height = 30, text = 'Anexar comprovante', fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = lambda: select_file(self.textarea_textbox, self)).place(x = 160, y = 305)
        self.textarea_textbox = ctk.CTkTextbox(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 410, height = 180, fg_color = '#ffffff', text_color = '#000000')
        self.textarea_textbox.place(x = 45, y = 350)
        self.file_path = None
        expenses_table(self.user_db_name)
        return self.frame

    def expense_registration(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()
        value = self.value_entry.get().strip()
        source = self.source_entry.get().strip()

        if not name or not date or not value or not source:
            messagebox.showerror(title = 'Cadastro de despesa', message = 'Por favor, preencha todos os campos!')
            return
        
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()
        
        execute_query('INSERT INTO expenses (name, date, value, source, voucher) VALUES (?, ?, ?, ?, ?)', (name, date, value, source, voucher), db_name = self.user_db_name)
        messagebox.showinfo(title = 'Cadastro de despesa', message = f"Despesa '{name}' criada com sucesso!")
        self.clean_expense_widgets()

    def update_expense(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()
        value = self.value_entry.get().strip()
        source = self.source_entry.get().strip()

        if not name or not date or not value or not source:
            messagebox.showerror(title = 'Atualição de despesa', message = 'Por favor, preencha todos os campos!')
            return
        
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()
    
        execute_query('UPDATE expenses SET value = ?, source = ?, voucher = ? WHERE name = ? AND date = ?', (value, source, voucher, name, date), db_name = self.user_db_name)
        messagebox.showinfo(title = 'Atualização de despesa', message = f"Despesa '{name}' atualizada com sucesso!")
        self.clean_expense_widgets()

    def expense_inquiry(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()
    
        if not name or not date:
            messagebox.showerror(title = 'Consultar despesa', message = "Os campos 'Nome' e 'Data' são obrigatórios para atualizar!")
            return

        result = execute_query('SELECT * FROM expenses WHERE name = ? AND date = ?', (name, date), fetchall = True, db_name = self.user_db_name)
        if result:
            for row in result:
                formatted_value = f"R$ {row[3]:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
                self.textarea_textbox.insert('end', f"Nome: {row[1]}\n")
                self.textarea_textbox.insert('end', f"Data: {row[2]}\n")
                self.textarea_textbox.insert('end', f"Valor: {formatted_value}\n")
                self.textarea_textbox.insert('end', f"Fonte: {row[4]}\n")
                self.textarea_textbox.insert('end', f"Comprovante: {'Sim' if row[5] else 'Não'}\n\n")
        else:
            messagebox.showerror(title = 'Consultar despesa', message = f"Nenhuma despesa encontrada para '{name}' e data '{date}'!")
    
        self.clean_expense_widgets()

    def delete_expense(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        date = self.date_entry.get().strip()
    
        if not name or not date:
            messagebox.showerror(title = 'Deletar despesa', message = "Os campos 'Nome' e 'Data' são obrigatórios para deletar!")
            return
        
        execute_query('DELETE FROM expenses WHERE nome = ? AND date = ?', (name, date), db_name = self.user_db_name)
        messagebox.showinfo(title = 'Deletar despesa', message = f"Despesa '{name}' deletada com sucesso!")
        self.clean_expense_widgets()

    def clean_expense_widgets(self):
        entries = [self.name_entry, self.date_entry, self.value_entry, self.source_entry]
        checkbuttons = []
        clean_widgets(entries, checkbuttons, 'file_path', self)

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

class FleetPage():
    
    def __init__(self, window, user, user_db_name):
        self.username = user
        self.user_db_name = user_db_name
        self.window = ctk.CTkToplevel(window)
        self.window.title('Fleet Page')
        self.window.geometry('500x700')
        self.window.resizable(False, False)
        self.window.transient(window)
        self.fleet_frame = ctk.CTkFrame(window)

        self.logo_label = ctk.CTkLabel(self.window, image = ctk.CTkImage(Image.open('static/images/logo_nano_transportes.jpg'), size = (500, 240)), compound = 'top').place(x = 0, y = 0)
        self.frame = ctk.CTkFrame(self.window, width = 500, height = 570, fg_color = '#000080', corner_radius = 0, bg_color = '#000080').place(x = 0, y = 137)
        self.text1_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 20), text = 'CONTROLE DE FROTA', text_color = '#ffffff').place(x = 140, y = 145)
        self.create_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Cadastrar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.fleet_registration).place(x = 45, y = 180)
        self.update_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Atualizar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.update_fleet).place(x = 157, y = 180)
        self.read_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Consultar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.fleet_inquiry).place(x = 265, y = 180)
        self.delete_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Deletar', width = 80, height = 30, fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.delete_fleet).place(x = 375, y = 180)
        self.plate_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Placa', text_color = '#ffffff').place(x = 10, y = 235)
        self.plate_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 120, height = 30, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.plate_entry.place(x = 100, y = 230)
        self.color_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Cor', text_color = '#ffffff').place(x = 250, y = 235)
        self.color_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 120, height = 30, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.color_entry.place(x = 335, y = 230)
        self.brand_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Marca', text_color = '#ffffff').place(x = 10, y = 278)
        self.brand_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 120, height = 30, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.brand_entry.place(x = 100, y = 275)
        self.model_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Modelo', text_color = '#ffffff').place(x = 250, y = 278)
        self.model_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 120, height = 30, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.model_entry.place(x = 335, y = 275)
        self.initial_km_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Km inicial', text_color = '#ffffff').place(x = 10, y = 323)
        self.initial_km_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 80, height = 30, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.initial_km_entry.place(x = 100, y = 320)
        self.final_km_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Final', text_color = '#ffffff').place(x = 181, y = 323)
        self.final_km_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 80, height = 30, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.final_km_entry.place(x = 225, y = 320)
        self.mileage_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Rodado', text_color = '#ffffff').place(x = 308, y = 323)
        self.mileage_textbox = ctk.CTkTextbox(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 80, height = 30, fg_color = '#ffffff', text_color = '#010203')
        self.mileage_textbox.place(x = 375, y = 320)
        self.obs_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text ='Observações', text_color = '#ffffff').place(x = 10, y = 375)
        self.obs_entry = ctk.CTkEntry(self.window, bg_color = '#000080',font = ctk.CTkFont('verdana', size = 18), corner_radius = 0, width = 320, height = 50, fg_color = '#ffffff', border_width = 0, text_color = '#010203')
        self.obs_entry.place(x = 135, y = 364)
        self.calculation_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 20), text = 'CÁLCULO DE CONSUMO', text_color = '#ffffff', fg_color = '#000080').place(x = 135, y = 420)
        self.initial_entry = ctk.CTkEntry(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), width = 100, height = 30, corner_radius = 0, fg_color = '#ffffff', text_color = '#010203', placeholder_text = 'inicial')
        self.initial_entry.place(x = 10, y = 460)
        self.final_entry = ctk.CTkEntry(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), width = 100, height = 30, corner_radius = 0, fg_color = '#ffffff', text_color = '#010203', placeholder_text = 'final')
        self.final_entry.place(x = 135, y = 460)
        self.liters_entry = ctk.CTkEntry(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), width = 100, height = 30, corner_radius = 0, fg_color = '#ffffff', text_color = '#010203', placeholder_text = 'litros')
        self.liters_entry.place(x = 260, y = 460)
        self.calculation_button = ctk.CTkButton(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), text = 'Calcular', width = 80, fg_color = '#ff8040', hover_color = '#ffa87d', text_color = '#ffffff', corner_radius = 14, command = self.calculation).place(x = 385, y = 461)
        self.textarea_textbox = ctk.CTkTextbox(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), width = 400, height = 160, corner_radius = 0, fg_color = '#ffffff', text_color = '#010203')
        self.textarea_textbox.place(x = 50, y = 500)
        self.text2_label = ctk.CTkLabel(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 14), text = "Made by Rb", text_color = '#ffffff').place(x = 10, y = 670)
        self.exit_button = ctk.CTkButton(self.window, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 16), width = 100, corner_radius = 14, text = 'Sair', fg_color = "#ff0000", hover_color = '#af0850', command = self.window.quit).place(x = 200, y = 670)
        self.comeback_button = ctk.CTkButton(self.window, font = ctk.CTkFont('verdana', size = 16), text = 'voltar', width = 0, corner_radius = 0, fg_color = '#80ff80', hover_color = '#4dcea7', text_color = '#000000', command = lambda: [self.window.withdraw(), OptionPage(self.window, self.username, self.user_db_name)]).place(x = 0, y = 0)
        fleet_table(self.user_db_name)

    def calculation(self):
        self.textarea_textbox.delete('1.0', 'end')
        initial = self.initial_entry.get().strip()
        final = self.final_entry.get().strip()
        liters = self.liters_entry.get().strip()

        if not initial or not final or not liters:
            self.textarea_textbox.insert('1.0', 'Todos os campos são obrigatórios!\n')
            return

        try:
            initial = float(initial)
            final = float(final)
            liters = float(liters)
            if final < initial:
                self.textarea_textbox.insert('1.0', 'O valor final deve ser maior que o valor inicial!\n')
                return

            mileage = final - initial
            consumption = mileage / liters

            self.textarea_textbox.insert('1.0', f'Consumo: {consumption:.2f} km/l\n')

        except ValueError:
            self.textarea_textbox.insert('1.0', 'Por favor, insira valores numéricos válidos!\n')

    def fleet_registration(self):
        self.textarea_textbox.delete('1.0', 'end')
        plate = self.plate_entry.get().strip()
        color = self.color_entry.get().strip()
        brand = self.brand_entry.get().strip()
        model = self.model_entry.get().strip()
        initial_km = self.initial_km_entry.get().strip()
        final_km = self.final_km_entry.get().strip()
        mileage = self.mileage_textbox.get('1.0', 'end-1c').strip()
        obs = self.obs_entry.get().strip()

        if not plate or not color or not brand or not model or not initial_km:
            self.textarea_textbox.insert('1.0', 'Por favor, preencha todos os campos!\n')
            return

        result = execute_query('SELECT * FROM fleet WHERE plate = ?', (plate,), fetchone = True, db_name = self.user_db_name)
        if result:
            self.textarea_textbox.insert('1.0', f"A placa '{plate}' já está cadastrada!\n")
            return

        if initial_km:
            initial_km = float(initial_km)
        else:
            self.textarea_textbox.insert('1.0', "O campo 'Km Inicial' é obrigatório!\n")
            return

        if final_km:
            final_km = float(final_km)
            mileage = final_km - initial_km
            self.mileage_textbox.delete('1.0', 'end')
            self.mileage_textbox.insert('1.0', str(mileage))
        else:
            final_km = None
            mileage = None

        execute_query('INSERT INTO fleet (plate, color, brand, model, initial, final, mileage, obs) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (plate, color, brand, model, initial_km, final_km, mileage, obs), db_name = self.user_db_name)
        self.textarea_textbox.insert('1.0', f"Placa '{plate}' cadastrada com sucesso!\n")
        self.clean_fleet_widgets()

    def update_fleet(self):
        self.textarea_textbox.delete('1.0', 'end')
        plate = self.plate_entry.get().strip()
        color = self.color_entry.get().strip()
        brand = self.brand_entry.get().strip()
        model = self.model_entry.get().strip()
        initial_km = self.initial_km_entry.get().strip()
        final_km = self.final_km_entry.get().strip()
        mileage = self.mileage_textbox.get('1.0', 'end-1c').strip()
        obs = self.obs_entry.get().strip()
    
        if not plate or not color or not brand or not model or not initial_km:
            self.textarea_textbox.insert('1.0', 'Por favor, preencha todos os campos!\n')
            return

        result = execute_query('SELECT * FROM fleet WHERE plate = ?', (plate,), fetchone = True, db_name = self.user_db_name)

        if not result:
            self.textarea_textbox.insert('1.0', f"A placa '{plate}' não está cadastrada.\n")
            return

        if final_km:
            initial_km = float(initial_km)
            final_km = float(final_km)
            mileage = final_km - initial_km
            self.mileage_textbox.delete('1.0', 'end')
            self.mileage_textbox.insert('1.0', str(mileage))
        else:
            final_km = None
            mileage = None

        execute_query('UPDATE fleet SET color = ?, brand = ?, model = ?, initial = ?, final = ?, mileage = ?, obs = ? WHERE plate = ?', (color, brand, model, initial_km, final_km, mileage, obs, plate), db_name = self.user_db_name)
        self.textarea_textbox.insert('1.0', f"Placa '{plate}' atualizada com sucesso!\n")
        self.clean_fleet_widgets()

    def fleet_inquiry(self):
        self.textarea_textbox.delete('1.0', 'end')
        plate = self.plate_entry.get().strip()
    
        if not plate:
            self.textarea_textbox.insert('1.0', "O campo 'Placa' é obrigatório para consultar.\n")
            return
    
        result = execute_query('SELECT * FROM fleet WHERE plate = ?', (plate,), fetchall = True, db_name = self.user_db_name)
        if result:
            for row in result:
                self.textarea_textbox.insert('end', f'Placa: {row[1]}\n')
                self.textarea_textbox.insert('end', f'Cor: {row[2]}\n')
                self.textarea_textbox.insert('end', f'Marca: {row[3]}\n')
                self.textarea_textbox.insert('end', f'Modelo: {row[4]}\n')
                self.textarea_textbox.insert('end', f'Km inicial: {row[5]}\n')
                self.textarea_textbox.insert('end', f'Km final: {row[6]}\n')
                self.textarea_textbox.insert('end', f'Km rodados: {row[7]}\n')
                self.textarea_textbox.insert('end', f'Observações: {row[8]}\n\n')
        else:
            self.textarea_textbox.insert('1.0', f"Nenhuma cadastro encontrado para '{plate}'.\n")
    
        self.clean_fleet_widgets()

    def delete_fleet(self):
        self.textarea_textbox.delete('1.0', 'end')
        plate = self.plate_entry.get().strip()
    
        if not plate:
            self.textarea_textbox.insert('1.0', "O campo 'Placa' é obrigatório para deletar.\n")
            return
    
        execute_query('DELETE FROM fleet WHERE placa = ?', (plate), db_name = self.user_db_name)
        self.textarea_textbox.insert('1.0', f"Placa: '{plate}' deletada com sucesso!\n")
        self.clean_fleet_widgets()

    def clean_fleet_widgets(self):
        entries = [self.plate_entry, self.color_entry, self.brand_entry, self.model_entry, self.initial_km_entry, self.final_km_entry, self.obs_entry]
        clean_widgets(entries)

class QueryPage():
    
    def __init__(self, window, user):
        self.username = user
        self.window = ctk.CTkToplevel(window)
        self.window.title('Search Page')
        self.window.geometry('800x450')
        self.window.resizable(False, False)
        self.window.transient(window)
        self.query_frame = ctk.CTkFrame(window)

        self.frame = ctk.CTkFrame(self.window, width = 1000, height = 600, corner_radius = 0, fg_color = '#ffffff').place(x = 0, y = 0)
        self.logo_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', image = ctk.CTkImage(Image.open('static/images/logo_nano_transportes_menor.jpg'), size = (300, 180)), compound = 'left').place(x = 0, y = 175)
        self.text1_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = 'Ola,', text_color = '#000000').place(x = 90, y = 20)
        self.user_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 20), text = f' {self.username}', text_color = '#d70428').place(x = 130, y = 20)
        self.query_entry = ctk.CTkEntry(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 14), width = 225, height = 40, corner_radius = 20, fg_color = '#ffffff', border_color = '#000000', text_color = '#000000', placeholder_text = 'pesquisar ...')
        self.query_entry.place(x = 40, y = 67)
        self.query_button = ctk.CTkButton(self.window, bg_color = '#ffffff', image = ctk.CTkImage(Image.open('static/images/icone_pesquisar.jpg'), size = (38, 24)), width = 0, height = 0, corner_radius = 0, text = '', fg_color = '#ffffff', hover_color = '#ffffff', compound = 'right', command = self.query).place(x = 195, y = 70)
        self.clear_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 100, corner_radius = 14, text = 'Limpar pesquisa', fg_color = '#191970', hover_color = '#0000FF', command = self.clear_query).place(x = 70, y = 135)
        self.first_textbox = None
        self.second_textbox = None
        self.third_textbox = None
        self.text3_label = ctk.CTkLabel(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 14), text = "Made by Rb", text_color = '#0080ff').place(x = 10, y = 420)
        self.exit_button = ctk.CTkButton(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), text = 'Sair', width = 100, corner_radius = 14, fg_color = "#ff0000", hover_color = '#af0850', command = self.window.quit).place(x = 180, y = 420)
        self.comeback_button = ctk.CTkButton(self.window, font = ctk.CTkFont('verdana', size = 16), text = 'voltar', width = 0, corner_radius = 0, fg_color = '#80ff80', hover_color = '#4dcea7', text_color = '#000000', command = lambda: [self.window.withdraw(), OptionPage(self.window, self.username)]).place(x = 0, y = 0)
        self.window.bind('<Return>', lambda event = None: self.query())

    def query(self):
        termo_pesquisa = self.query_entry.get().strip().lower()
        if not termo_pesquisa:
            return
        
        conn = sqlite3.connect('nano_transp.db')
        cursor = conn.cursor()
        if termo_pesquisa in ['clientes', 'receitas', 'despesas', 'frota']:
            consultas = {'clientes': 'SELECT * FROM clients',
                         'receitas': 'SELECT * FROM incomes',
                         'despesas': 'SELECT * FROM expenses',
                         'frota': 'SELECT * FROM fleet'}

            if termo_pesquisa in consultas:
                consulta_sql = consultas[termo_pesquisa]
                cursor.execute(consulta_sql)
                resultados = cursor.fetchall()
                self.mostrar_resultados(resultados, termo_pesquisa)
        else:
            tabelas_colunas = {'clients': 'name',
                               'incomes': 'name',
                               'expenses': 'name',
                               'fleet': 'plate'}

            for tabela, coluna in tabelas_colunas.items():
                cursor.execute(f'SELECT * FROM {tabela} WHERE {coluna} LIKE ?', ('%' + termo_pesquisa + '%',))
                resultados = cursor.fetchall()
                if resultados:
                    self.mostrar_resultados_especificos_relacionados(resultados, termo_pesquisa)
                    if tabela == 'clients':
                        cursor.execute('SELECT * FROM incomes WHERE client_id IN (SELECT id FROM clients WHERE name LIKE ?)', ('%' + termo_pesquisa + '%',))
                        receitas_resultados = cursor.fetchall()
                        self.mostrar_resultados_relacionados(receitas_resultados)
                    break
        conn.close()

    def mostrar_resultados(self, resultados, tipo):
        if not self.first_textbox:
            self.first_textbox = ctk.CTkTextbox(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 150, height = 150, corner_radius = 0, border_width = 1, fg_color = '#f4f4f4', text_color = '#000000')
            self.first_textbox.place(x = 300, y = 15)
            self.first_textbox.bind('<Button-1>', lambda e: self.on_click(e))

        self.first_textbox.delete('1.0', 'end')
        for row in resultados:
            item_nome = f'{row[0]} - {row[1]}'
            self.first_textbox.insert('end', f'{item_nome}\n')
            self.first_textbox.tag_add(f'{item_nome}', f'insert -1l linestart', 'insert -1l lineend')
            self.first_textbox.tag_bind(f'{item_nome}', '<Button-1>', lambda e, r = row, t = tipo: self.mostrar_resultados_especificos_relacionados([r], t))

    def mostrar_resultados_especificos_relacionados(self, resultados, tipo):
        if not self.second_textbox:
            self.second_textbox = ctk.CTkTextbox(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 300, height = 150, corner_radius = 0, border_width = 1, fg_color = '#f4f4f4', text_color = '#020304')
            self.second_textbox.place(x = 490, y = 15)
            self.second_textbox.bind('<Button-1>', self.on_click)
        
        self.second_textbox.delete('1.0', 'end')
        processed_ids = set()
        for row in resultados:
            for i, value in enumerate(row):
                if tipo == 'clientes' and i == 4:
                    telefone = value
                    telefone_link = f'whatsapp://send?phone = {telefone}'
                    self.second_textbox.insert('end', f'{telefone}\n', ('link',))
                    self.second_textbox.tag_config('link', foreground = 'blue', underline = True)
                    self.second_textbox.tag_bind('link', '<Button-1>', lambda e, tel = telefone_link: self.abrir_whatsapp(tel))
                elif tipo == 'receitas': 
                    for receita in resultados:
                        cliente_id = receita[4]
                        nome_cliente = self.obter_nome_cliente(cliente_id)
                        self.second_textbox.insert('end', f'Nome: {row[1]}\n')
                        self.second_textbox.insert('end', f'Data: {row[2]}\n')
                        self.second_textbox.insert('end', f'Valor: {row[3]}\n')
                        self.second_textbox.insert('end', f'Cliente: {nome_cliente}\n')
                        self.second_textbox.insert('end', f"Pago: {'Sim' if row[5] else 'Não'}\n")
                        self.second_textbox.insert('end', f"Comprovante: {'Sim' if row[6] else 'Não'}\n\n")
                elif tipo == 'despesas':
                    if row[0] not in processed_ids:
                        processed_ids.add(row[0])
                        self.second_textbox.insert('end', f'Nome: {row[1]}\n')
                        self.second_textbox.insert('end', f'Data: {row[2]}\n')
                        self.second_textbox.insert('end', f'Valor: {row[3]}\n')
                        self.second_textbox.insert('end', f'Fonte: {row[4]}\n')
                        self.second_textbox.insert('end', f"Comprovante: {'Sim' if row[5] else 'Não'}\n\n")
                elif tipo == 'frota':
                    if row[0] not in processed_ids:
                        processed_ids.add(row[0])
                        self.second_textbox.insert('end', f'Placa: {row[1]}\n')
                        self.second_textbox.insert('end', f'Cor: {row[2]}\n')
                        self.second_textbox.insert('end', f'Marca: {row[3]}\n')
                        self.second_textbox.insert('end', f'Modelo: {row[4]}\n')
                        self.second_textbox.insert('end', f'Km inicial: {row[5]}\n')
                        self.second_textbox.insert('end', f'Km final: {row[6]}\n')
                        self.second_textbox.insert('end', f'Km rodados: {row[7]}\n')
                        self.second_textbox.insert('end', f'Observações: {row[8]}\n\n')
                else:
                    self.second_textbox.insert('end', f'{value}\n')

            if tipo == 'clientes':
                cliente_id = resultados[0][0]
                conn = sqlite3.connect('nano_transp.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM incomes WHERE client_id = ?', (cliente_id,))
                receitas_resultados = cursor.fetchall()
                self.mostrar_resultados_relacionados(receitas_resultados)
                conn.close()

    def obter_nome_cliente(self, cliente_id):
        conn = sqlite3.connect('nano_transp.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM clients WHERE id = ?', (cliente_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else 'Desconhecido'

    def mostrar_resultados_relacionados(self, resultados):
        if not self.third_textbox:
            self.third_textbox = ctk.CTkTextbox(self.window, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 490, height = 250, corner_radius = 0, border_width = 1, fg_color = '#f4f4f4', text_color = '#000000')
            self.third_textbox.place(x = 300, y = 190)
            self.third_textbox.bind("<Button-1>", self.on_click)
        
        self.third_textbox.delete('1.0', 'end')
        for resultado in resultados:
            id = resultado[0]
            nome_receita = resultado[1]
            data = resultado[2]
            valor = resultado[3]
            pago = resultado[5]
            comprovante = resultado[6]
            status_recebimento = "pago" if pago == 1 else "a receber"
    
            if pago == 0:
                self.third_textbox.insert('end', f'{id}, {nome_receita}, {data}, {valor}, ')
                self.third_textbox.insert('end', f'{status_recebimento}', ('vermelho', 'link-calculadora'))
                self.third_textbox.tag_config('link-calculadora', foreground = 'red', underline = True)
                self.third_textbox.tag_bind('link-calculadora', '<Button-1>', lambda e: self.abrir_calculadora())
            else:
                self.third_textbox.insert('end', f'{id}, {nome_receita}, {data}, {valor}, {status_recebimento}')
        
            if comprovante:
                self.third_textbox.insert('end', ', ')
                self.third_textbox.insert('end', f'Comprovante\n', ('link',))
                self.third_textbox.tag_config('link', foreground = 'blue', underline = True)
                self.third_textbox.tag_bind('link', '<Button-1>', lambda e, blob = comprovante: self.abrir_comprovante(blob))

    def abrir_whatsapp(self, telefone_link):
        webbrowser.open(telefone_link)

    def abrir_comprovante(self, blob_data):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()
        save_blob_to_file(blob_data, temp_file.name)
        webbrowser.open(temp_file.name)

    def abrir_calculadora(self):
        subprocess.Popen(['calc.exe'])

    def on_click(self, event):
        widget = event.widget
        widget.configure(state = 'normal')
        widget.focus_set()
        widget.configure(state = 'disabled')

    def clear_query(self):
        if self.query_entry:
            self.query_entry.delete(0, 'end')

        textboxes = [self.first_textbox, self.second_textbox, self.third_textbox]
        for textbox in textboxes:
            if textbox:
                textbox.destroy()

        self.first_textbox = self.second_textbox = self.third_textbox = None