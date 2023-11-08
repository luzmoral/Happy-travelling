from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDSwitch
import smtplib
from kivymd.uix.list import OneLineListItem
from email.message import EmailMessage

import sqlite3

# Lista de provincias
provincias_argentinas = [
    "Buenos Aires", "CABA", "Catamarca", "Chaco", "Chubut", "Córdoba",
    "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja",
    "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan",
    "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero",
    "Tierra del Fuego", "Tucumán"
]


#Estilos
KV = '''
ScreenManager:
    LoginScreen:
    MainMenuScreen:
    FlightManagementScreen:
    ProvinceForm:
    ReservationForm:
    FlightPlanForm:
    RegisterScreen:
    FlightListScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        MDLabel:
            text: 'Inicio de sesión'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_style: 'H4'
        MDTextField:
            id: username
            hint_text: "Nombre de usuario o correo electrónico"
            required: True
            helper_text: "Requerido"
            helper_text_mode: "on_error"
            icon_right: "account"
        MDTextField:
            id: password
            hint_text: "Contraseña"
            required: True
            password: True
            helper_text: "Requerido"
            helper_text_mode: "on_error"
            icon_right: "key-variant"
        MDRaisedButton:
            text: "Iniciar sesión"
            on_release: app.login(username.text, password.text)
        MDRaisedButton:
            text: "Registrarse"
            on_release: root.manager.current = 'register'

<MainMenuScreen>:
    name: 'main_menu'
    BoxLayout:
        orientation: 'vertical'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        MDLabel:
            text: 'Menú Principal'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_style: 'H4'

    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'
        MyButton:
            text: "Enviar Correo Electrónico"
            on_release: app.send_email()

        MyButton:
            text: "Ver Planes y Reservas"
            on_release: app.load_flight_list()

        MyButton:
            text: "Gestión de Vuelos"
            on_release: app.check_authenticated('flight_management')

        MyButton:
            text: "Volver al Inicio de Sesión"
            on_release: app.root.current = 'login'    

        

<MyButton@Button>:
    background_color: 0, 0.5, 1, 1
    color: 1, 1, 1, 1
    size_hint: None, None
    size: "200dp", "48dp"


<FlightManagementScreen>:
    name: 'flight_management'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        MDLabel:
            text: 'Gestión de Vuelos'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_style: 'H4'
        MDRaisedButton:
            text: "Cargar Provincia"
            on_release: root.manager.current = 'province_form'  # Elimina la línea anterior
        MDRaisedButton:
            text: "Cargar Reserva Disponible"
            on_release: app.load_reservation('vuelo cargado')

        MDRaisedButton:
            text: "Cargar Plan de Vuelo"
            on_release: app.load_flight_plan('carga de plan ')

        MDRaisedButton:
            text: "Cerrar Sesión"
            on_release: app.logout()
        MDRaisedButton:
            text: "Volver al Menú Principal"
            on_release: app.root.current = 'main_menu'

<ProvinceForm>:
    name: 'province_form'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        MDLabel:
            text: 'Cargar Provincia'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_style: 'H4'
        MDTextField:
            id: province_input
            hint_text: "Nombre de la provincia"
            required: True
        MDRaisedButton:
            text: "Guardar Provincia"
            on_release: app.load_province(province_input.text)  # Agrega este botón
        MDRaisedButton:
            text: "Volver al Menú Principal"
            on_release: app.root.current = 'main_menu'

<ReservationForm>:
    name: 'reservation_form'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        MDLabel:
            text: 'Cargar Reserva Disponible'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_style: 'H4'
        MDTextField:
            id: reservation_input
            hint_text: "Nombre de la reserva"
            required: True
        MDRaisedButton:
            text: "Cargar Reserva"
            on_release: app.load_reservation(reservation_input.text)
        MDRaisedButton:
            text: "Volver al Menú Principal"
            on_release: app.root.current = 'main_menu'

<FlightPlanForm>:
    name: 'flight_plan_form'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        MDLabel:
            text: 'Cargar Plan de Vuelo'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_style: 'H4'
        MDTextField:
            id: flight_plan_input
            hint_text: "Nombre del plan de vuelo"
            required: True
        MDRaisedButton:
            text: "Cargar Plan de Vuelo"
            on_release: app.load_flight_plan(flight_plan_input.text)
        MDRaisedButton:
            text: "Volver al Menú Principal"
            on_release: app.root.current = 'main_menu'

<RegisterScreen>:
    name: 'register'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        MDLabel:
            text: 'Registro'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_style: 'H4'
        MDTextField:
            id: new_username
            hint_text: "Nuevo nombre de usuario o correo electrónico"
            required: True
        MDTextField:
            id: new_password
            hint_text: "Nueva contraseña"
            required: True
            password: True
        MDRaisedButton:
            text: "Registrar"
            on_release: app.register(new_username.text, new_password.text)
        MDRaisedButton:
            text: "Ir a la página de inicio de sesión"
            on_release: app.root.current = 'login'  # Botón para ir a la página de inicio de sesión

<FlightListScreen>:
    name: 'flight_list'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # Color de fondo (por ejemplo, blanco)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        Spinner:
            id: departure_spinner
            text: "Provincia de partida"
            values: ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba","Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja","Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan","San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero","Tierra del Fuego", "Tucumán"]
            theme_text_color: "Primary"
            halign: 'center'
            background_color: 0, 0.5, 1, 1  # Color de fondo del Spinner (azul claro)
            foreground_color: 1, 1, 1, 1  # Color del texto (blanco)
        Spinner:
            id: destination_spinner
            text: "Destino"
            values:["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba","Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja","Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan","San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero","Tierra del Fuego", "Tucumán"]
            theme_text_color: "Primary"
            halign: 'center'
            background_color: 0, 0.5, 1, 1  # Color de fondo del Spinner (azul claro)
            foreground_color: 1, 1, 1, 1  # Color del texto (blanco)
        Button:
            text: "Buscar vuelos"
            background_color: 0, 0.5, 1, 1  # Color de fondo del botón (azul claro)
            foreground_color: 1, 1, 1, 1  # Color del texto (blanco)
            on_release: app.root.get_screen('flight_list').search_flights(departure_spinner.text, destination_spinner.text)
        MDRaisedButton:
            text: "Volver al Menú Principal"
            on_release: app.root.current = 'main_menu'
        MDList:
            id: flight_list_view  # Agrega un ID para la lista de vuelos
        Label:
            id: flight_results_label  # Nuevo Label para mostrar los resultados
        Image:
            source: 'travel final.jpg'
            size_hint_x: 0.5  # Anchura relativa (1 significa el 100% del ancho de la pantalla)
            size_hint_y: 1.5 # Altura relativa (1 significa el 100% de la altura de la pantalla)
            allow_stretch: True
            keep_ratio: False    
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            
    




'''
    #Pantallas separadas por clases

class LoginScreen(Screen):
    pass

class MainMenuScreen(Screen):
    pass

class FlightManagementScreen(Screen):
    pass

class ProvinceForm(Screen):
    pass

class ReservationForm(Screen):
    pass

class FlightPlanForm(Screen):
    pass

class RegisterScreen(Screen):
    pass


class FlightListScreen(Screen):
    def search_flights(self, departure, destination):
        if not departure or not destination:
            self.show_error_message("Por favor, seleccione la provincia de partida y el destino.")
            return

        # Conectarse a la base de datos
        conn = sqlite3.connect('User_database.db')
        cursor = conn.cursor()

        # Ejecutar una consulta para obtener datos de vuelos
        cursor.execute("SELECT origin, destination, price FROM vuelos WHERE departure = ? AND destination = ?", (departure, destination))
        flight_data = cursor.fetchall()

        conn.close()

        flight_results_label = self.ids.flight_results_label
        flight_results_label.text = "Vuelos encontrados:\n"

        for flight in flight_data:
            origin, dest, price = flight
            flight_results_label.text += f"Origen: {origin}, Destino: {dest}, Precio: {price}\n"
    
    def build(self):
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.username = ""
        self.password = ""
        return Builder.load_string(KV)




    

class LoginApp(MDApp):
    def build(self):
        self.conn = sqlite3.connect("user_database.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.username = ""
        self.password = ""
        return Builder.load_string(KV)

  
    #Tablas de la BD
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS provinces (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flight_plans (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vuelos(
                id INTEGER PRIMARY KEY,
                origin TEXT,
                destination TEXT,
                price REAl

            )
        ''')
        
        
        self.conn.commit()

 
# ...




    def login(self, username, password):
        self.username = username
        self.password = password

        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()
        if user:
            self.root.get_screen('login').ids.username.text = ""
            self.root.get_screen('login').ids.password.text = ""
            self.root.current = 'main_menu'
            self.show_success_message("Inicio de sesión exitoso")
        else:
            self.show_error_message("Nombre de usuario o contraseña incorrectos")

    def register(self, new_username, new_password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (new_username, new_password))
            self.conn.commit()
            self.show_success_message("Registro exitoso")
        except sqlite3.IntegrityError:
            self.show_error_message("El usuario ya existe")

    def logout(self):
        self.root.current = 'login'

    def show_success_message(self, message):
        dialog = MDDialog(
            title="Éxito",
            text=message,
            buttons=[MDFlatButton(text="OK")]
        )
        dialog.open()

    def show_error_message(self, message):
        dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[MDFlatButton(text="OK")]
        )
        dialog.open()

    def send_email(self):
        self.show_success_message("Correo electrónico enviado con éxito")

    def show_provincias(self):
        self.cursor.execute('SELECT name FROM provinces')
        provinces = self.cursor.fetchall()
        province_names = [province[0] for province in provinces]
        menu = MDDialog(title="Seleccione la provincia de partida", type="confirmation", items=province_names)
        menu.open()

    

    def set_selected_date(self, instance):
        selected_date = instance.content.active_date
        self.root.get_screen('main_menu').ids.departure_date.text = selected_date.strftime("%Y-%m-%d")

    def search_flights(self, destination, departure, departure_date):
        self.show_success_message(f"Buscando vuelos a {destination} desde {departure} el {departure_date}")

    def check_authenticated(self, next_screen):
        if self.is_authenticated():
            self.root.transition.direction = 'left'
            self.root.current = next_screen

    def is_authenticated(self):
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (self.username, self.password))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            self.show_error_message("Debe iniciar sesión para realizar esta acción.")
            return False

  
    #cargar provincias
    def load_province(self, province_name):
        if self.is_authenticated():
            try:
                self.cursor.execute('INSERT INTO provinces (name) VALUES (?)', (province_name,))
                self.conn.commit()
                self.show_success_message(f"Provincia '{province_name}' cargada correctamente.")
            except sqlite3.IntegrityError:
                self.show_error_message("La provincia ya existe")



    #enviar correo electronico
    def send_email(self):
        if self.is_authenticated():
            smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'happytravellingapp@gmail.com' 
        smtp_password = 'wcxphxcwgbgiwdav'  
        message = EmailMessage()
        message.set_content('Contenido del correo electrónico')
        message['Subject'] = 'Asunto del correo electrónico'
        message['From'] = 'happytravellingapp@gmail.com'  #
        message['To'] = 'pizzaconpiña1@gmail.com.com'  

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(message)

            self.show_success_message("Correo electrónico enviado con éxito")
        except Exception as e:
            self.show_error_message(f"Error al enviar el correo electrónico: {str(e)}")


    #cargar reservaciones     
    def load_reservation(self, reservation_name):
        if self.is_authenticated():
            try:
                self.cursor.execute('INSERT INTO reservations (name) VALUES (?)', (reservation_name,))
                self.conn.commit()
                self.show_success_message(f"Reserva '{reservation_name}' cargada correctamente.")
            except sqlite3.IntegrityError:
                self.show_error_message("La reserva ya existe")


    #cargar plan de vuelos
    def load_flight_plan(self, flight_plan_name):
        if self.is_authenticated():
            try:
                self.cursor.execute('INSERT INTO flight_plans (name) VALUES (?)', (flight_plan_name,))
                self.conn.commit()
                self.show_success_message(f"Plan de vuelo '{flight_plan_name}' cargado correctamente.")
            except sqlite3.IntegrityError:
                self.show_error_message("El plan de vuelo ya existe")
    def load_flight_list(self):
        if self.is_authenticated():
            self.root.current = 'flight_list'  
        flight_list_view = self.root.get_screen('flight_list').ids.flight_list_view
        flight_list_view.clear_widgets()  

        
        self.cursor.execute('SELECT name FROM flight_plans')
        flight_plans = self.cursor.fetchall()

       
        self.cursor.execute('SELECT name FROM reservations')
        reservations = self.cursor.fetchall()

        
        for flight_plan in flight_plans:
            flight_list_view.add_widget(OneLineListItem(text=flight_plan[0]))

        for reservation in reservations:
            flight_list_view.add_widget(OneLineListItem(text=reservation[0]))


  
    def show_province_form(self):
        self.root.current = 'province_form'

    def show_reservation_form(self):
        self.root.current = 'reservation_form'

    def show_flight_plan_form(self):
        self.root.current = 'flight_plan_form'

if __name__ == '__main__':
    LoginApp().run()