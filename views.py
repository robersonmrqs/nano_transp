import customtkinter as ctk
import re
import webbrowser
import win32com.client as win32
from models import *
from utils import *
from PIL import Image
from tkinter import messagebox, filedialog

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
            OptionPage(self.window, username)
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
        elif get_user_details(username = username, email = email):
            messagebox.showerror(title = 'Cadastro de usuário', message = 'Usuário já cadastrado!')
        else:
            register_user(name, email, username, password)
            messagebox.showinfo(title = 'Cadastro de usuário', message = 'Usuário cadastrado com sucesso!')
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
        self.adress_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Endereço', text_color = '#ffffff').place(x = 45, y = 165)
        self.adress_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.adress_entry.place(x = 135, y = 160)
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
        clients_table()
        return self.frame

    def customer_registration(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        adress = self.adress_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        contact = self.contact_entry.get().strip()

        if not name or not adress or not email or not phone or not contact:
            messagebox.showerror(title = 'Cadastro de cliente', message = 'Por favor, preencha todos os campos!')
            return
        elif not validate_email(email):
            messagebox.showerror(title = 'Cadastro de cliente', message = 'Email inválido!')
            return
        elif not phone.startswith('55'):
            phone = '55' + phone
        
        result = execute_query('SELECT * FROM clients WHERE name = ?', (name,), fetchone = True)  
        if result:
            messagebox.showerror(title = 'Cadastro de cliente', message = f'Cliente {name} já cadastrado!')
            return
        else:
            execute_query('INSERT INTO clients (name, adress, email, phone, contact) VALUES (?, ?, ?, ?, ?)', (name, adress, email, phone, contact))
            messagebox.showinfo(title = 'Cadastro de cliente', message = f"Cliente '{name}' cadastrado com sucesso!")
            self.clean_customer_widgets()

    def update_client(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        adress = self.adress_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        contact = self.contact_entry.get().strip()
    
        if not name or not adress or not email or not phone or not contact:
            messagebox.showerror(title = 'Atualização de cliente', message = 'Por favor, preencha todos os campos!')
            return
        elif not validate_email(email):
            messagebox.showerror(title = 'Atualização de cliente', message = 'Email inválido!')
            return
        elif not phone.startswith('55'):
            phone = '55' + phone

        execute_query('UPDATE clients SET adress = ?, email = ?, phone = ?, contact = ? WHERE name = ?', (adress, email, phone, contact, name))
        messagebox.showinfo(title = 'Atualização de cliente', message = f"Cliente '{name}' atualizado com sucesso!")
        self.clean_customer_widgets()

    def customer_inquiry(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
    
        if not name:
            self.textarea_textbox.insert('1.0', "O campo 'Nome' é obrigatório para consultar.\n")

        result = execute_query('SELECT * FROM clients WHERE name = ?', (name,), fetchall = True)
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
            execute_query('DELETE FROM clients WHERE name = ?', (name,))
            messagebox.showinfo(title = 'Deletar cliente', message = f"Cliente '{name}' deletado com sucesso!")
            self.clean_customer_widgets()

    def clean_customer_widgets(self):
        entries = [self.name_entry, self.adress_entry, self.email_entry, self.phone_entry, self.contact_entry]
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
        self.data_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Data', text_color = '#ffffff').place(x = 45, y = 165)
        self.data_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = 'dd/mm/aaaa')
        self.data_entry.place(x = 135, y = 160)
        self.value_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Valor', text_color = '#ffffff').place(x = 45, y = 210)
        self.value_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203')
        self.value_entry.place(x = 135, y = 205)
        self.client_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Cliente', text_color = '#ffffff').place(x = 45, y = 255)
        self.client_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203')
        self.client_entry.place(x = 135, y = 250)
        self.paid_var = ctk.IntVar()
        self.paid_checkbox = ctk.CTkCheckBox(self.frame, text = 'Pago?', font = ctk.CTkFont('verdana', size = 18), variable = self.paid_var, onvalue = 1, offvalue = 0, text_color = '#ffffff')
        self.paid_checkbox.place(x = 45, y = 307)
        self.voucher_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 80, height = 30, text = 'Anexar comprovante', fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.select_file).place(x = 135, y = 305)
        self.generate_nf_button = ctk.CTkButton(self.frame, bg_color = '#000080', font = ctk.CTkFont('verdana', size = 18), width = 80, text = 'Gerar NF', fg_color = '#ff8040', hover_color = '#ffa87d', text_color = '#ffffff', corner_radius = 14, command = generate_nf).place(x = 350, y = 306)
        self.textarea_textbox = ctk.CTkTextbox(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 410, height = 180, fg_color = '#ffffff', text_color = '#000000')
        self.textarea_textbox.place(x = 45, y = 350)
        self.file_path = None
        incomes_table()
        return self.frame

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.textarea_textbox.insert('1.0', f"Arquivo selecionado: {self.file_path}\n")
        else:
            messagebox.showerror(title = 'Cadastro de receita', message = 'Nenhum arquivo selecionado!')

    def income_registration(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()
        value = self.value_entry.get().strip()
        client_name = self.client_entry.get().strip()
        paid = self.paid_var.get()
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()

        if not name or not data or not value or not client_name:
            messagebox.showerror(title = 'Cadastro de receita', message = 'Por favor, preencha todos os campos!')
            return

        client = execute_query('SELECT id FROM clients WHERE name = ?', (client_name,), fetchone = True)
        if client:
            client_id = client[0]
            execute_query('INSERT INTO incomes (name, data, value, client_id, paid, voucher) VALUES (?, ?, ?, ?, ?, ?)', (name, data, value, client_id, paid, voucher))
            messagebox.showinfo(title = 'Cadastro de receita', message = f"Receita '{name}' criada com sucesso!")
            self.clean_income_widgets()
        else:
            messagebox.showerror(title = 'Cadastro de receita', message = f"Cliente '{client_name}' não encontrado!")

    def update_income(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()
        value = self.value_entry.get().strip()
        client_name = self.client_entry.get().strip()
        paid = self.paid_var.get()
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()

        if not name or not data or not value or not client_name:
            messagebox.showerror(title = 'Atualização de receita', message = 'Por favor, preencha todos os campos!')
            return

        client = execute_query('SELECT id FROM clients WHERE name = ?', (client_name,), fetchone = True)
        if client:
            client_id = client[0]
            execute_query('UPDATE incomes SET value = ?, client_id = ?, paid = ?, voucher = ? WHERE name = ? AND data = ?', (value, client_id, paid, voucher, name, data))
            messagebox.showinfo(title = 'Atualização de receita', message = f"Receita '{name}' atualizada com sucesso!")
            self.clean_income_widgets()
        else:
            messagebox.showerror(title = 'Atualização de receita', message = f"Cliente '{client_name}' não encontrado!")

    def income_inquiry(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()

        if not name or not data:
            messagebox.showerror(title = 'Consultar rceita', message = "Os campos 'Nome' e 'Data' são obrigatórios para consultar!")
            return

        result = execute_query('SELECT * FROM incomes WHERE name = ? AND data = ?', (name, data), fetchall = True)
        if result:
            for row in result:
                formatted_value = f"R$ {row[3]:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
                self.textarea_textbox.insert('end', f'Nome: {row[1]}\n')
                self.textarea_textbox.insert('end', f'Data: {row[2]}\n')
                self.textarea_textbox.insert('end', f'Valor: {formatted_value}\n')
                self.textarea_textbox.insert('end', f'Cliente: {row[4]}\n')
                self.textarea_textbox.insert('end', f"Pago: {'Sim' if row[5] else 'Não'}\n")
                self.textarea_textbox.insert('end', f"Comprovante: {'Sim' if row[6] else 'Não'}\n\n")
        else:
            messagebox.showerror(title = 'Consultar receita', message = f"Nenhuma receita encontrada para '{name}' e data '{data}'!")

        self.clean_income_widgets()

    def delete_income(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()

        if not name or not data:
            messagebox.showerror(title = 'Deletar receita', message = "Os campos 'Nome' e 'Data' são obrigatórios para deletar!")
            return

        execute_query('DELETE FROM incomes WHERE nome = ? AND data = ?', (name, data))
        messagebox.showinfo(title = 'Deletar receita', message = f"Receita '{name}' e data '{data}' deletada com sucesso!")
        self.clean_income_widgets()

    def clean_income_widgets(self):
        entries = [self.name_entry, self.data_entry, self.value_entry, self.client_entry]
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
        self.data_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Data', text_color = '#ffffff').place(x = 45, y = 165)
        self.data_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center', placeholder_text = 'dd/mm/aaaa')
        self.data_entry.place(x = 135, y = 160)
        self.value_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Valor', text_color = '#ffffff').place(x = 45, y = 210)
        self.value_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.value_entry.place(x = 135, y = 205)
        self.source_label = ctk.CTkLabel(self.frame, font = ctk.CTkFont('verdana', size = 18), text = 'Fonte', text_color = '#ffffff').place(x = 45, y = 255)
        self.source_entry = ctk.CTkEntry(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 18), width = 320, height = 36, fg_color = '#ffffff', border_width = 0, text_color = '#010203', justify = 'center')
        self.source_entry.place(x = 135, y = 250)
        self.voucher_button = ctk.CTkButton(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 80, height = 30, text = 'Anexar comprovante', fg_color = '#ffffff', text_color = '#000000', hover_color = '#e8e9ea', command = self.select_file).place(x = 160, y = 305)
        self.textarea_textbox = ctk.CTkTextbox(self.frame, bg_color = '#ffffff', font = ctk.CTkFont('verdana', size = 16), width = 410, height = 180, fg_color = '#ffffff', text_color = '#000000')
        self.textarea_textbox.place(x = 45, y = 350)
        self.file_path = None
        expenses_table()
        return self.frame

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.textarea_textbox.insert('1.0', f'Arquivo selecionado: {self.file_path}\n')
        else:
            self.textarea_textbox.delete('1.0', 'end')
            messagebox.showerror(title = 'Cadastro de despesa', message = 'Nenhum arquivo selecionado!')

    def expense_registration(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()
        value = self.value_entry.get().strip()
        source = self.source_entry.get().strip()
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()

        if not name or not data or not value or not source:
            messagebox.showerror(title = 'Cadastro de despesa', message = 'Por favor, preencha todos os campos!')
            return
        
        execute_query('INSERT INTO expenses (name, data, value, source, voucher) VALUES (?, ?, ?, ?, ?)', (name, data, value, source, voucher))
        messagebox.showinfo(title = 'Cadastro de despesa', message = f"Despesa '{name}' criada com sucesso!")
        self.clean_expense_widgets()

    def update_expense(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()
        value = self.value_entry.get().strip()
        source = self.source_entry.get().strip()   
        voucher = None
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                voucher = file.read()

        if not name or not data or not value or not source:
            messagebox.showerror(title = 'Atualição de despesa', message = 'Por favor, preencha todos os campos!')
            return
    
        execute_query('UPDATE expenses SET value = ?, source = ?, voucher = ? WHERE name = ? AND data = ?', (value, source, voucher, name, data))
        messagebox.showinfo(title = 'Atualização de despesa', message = f"Despesa '{name}' atualizada com sucesso!")
        self.clean_expense_widgets()

    def expense_inquiry(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()
    
        if not name or not data:
            messagebox.showerror(title = 'Consultar despesa', message = "Os campos 'Nome' e 'Data' são obrigatórios para atualizar!")
            return

        result = execute_query('SELECT * FROM expenses WHERE name = ? AND data = ?', (name, data), fetchall = True)
        if result:
            for row in result:
                formatted_value = f"R$ {row[3]:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
                self.textarea_textbox.insert('end', f"Nome: {row[1]}\n")
                self.textarea_textbox.insert('end', f"Data: {row[2]}\n")
                self.textarea_textbox.insert('end', f"Valor: {formatted_value}\n")
                self.textarea_textbox.insert('end', f"Fonte: {row[4]}\n")
                self.textarea_textbox.insert('end', f"Comprovante: {'Sim' if row[5] else 'Não'}\n\n")
        else:
            messagebox.showerror(title = 'Consultar despesa', message = f"Nenhuma despesa encontrada para '{name}' e data '{data}'!")
    
        self.clean_expense_widgets()

    def delete_expense(self):
        self.textarea_textbox.delete('1.0', 'end')
        name = self.name_entry.get().strip().lower()
        data = self.data_entry.get().strip()
    
        if not name or not data:
            messagebox.showerror(title = 'Deletar despesa', message = "Os campos 'Nome' e 'Data' são obrigatórios para deletar!")
            return
        
        execute_query('DELETE FROM expenses WHERE nome = ? AND data = ?', (name, data))
        messagebox.showinfo(title = 'Deletar despesa', message = f"Despesa '{name}' deletada com sucesso!")
        self.clean_expense_widgets()

    def clean_expense_widgets(self):
        entries = [self.name_entry, self.data_entry, self.value_entry, self.source_entry]
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