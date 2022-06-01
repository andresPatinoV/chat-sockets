import socket   
import threading
import sys
import getpass

HOST = '127.0.0.1'
PORT = 55555

class Usuario:
    def __init__(self, nombres=" ", apellidos=" ", usuario=" ", password=" ", edad=0, genero=""):
        self.nombres = nombres
        self.apellidos = apellidos
        self.usuario = usuario
        self.password = password
        self.edad = edad
        self.genero = genero
        self.estado = 0

def menu():
    print('BIENVENIDO AL CHAT DISTRIBUIDO')
    print('1. Iniciar Sesion.   2. Registrarse.')
    opcion = input('Digite su opcion: ')
    if opcion == '1':
        return('iniciar_sesion')
    if opcion == '2':
        return('registrar')
    else:
        return('error_opcion')

def receive_messages():
    while True:
        message = client.recv(1024).decode()
        print(message)

def write_messages(usuario):
    while True:
        message = input('')
        if message == '#exit':
            client.send(message.encode())
            print('Sesion cerrada')
            client.close()
            sys.exit()

        elif message == '#help':
            print('COMANDOS DISPONIBLES:')
            print('#show users : Muestra todos los usuarios conectados.')
            print('#show users s : Muestra todos los usuarios conectados en la sala actual.')
            print('#exit : Salir del chat.')
        else:
            client.send(message.encode())

def iniciar(usuario):
    if usuario.estado == 0:
        opcion = menu()
        client.send(opcion.encode())
        opcion_server = client.recv(1024).decode()
        if opcion_server == 'iniciar_sesion':
            username = input('Nombre de usuario: ')
            client.send(username.encode())
            password = input('Contraseña: ')
            client.send(password.encode())
            if client.recv(1024).decode() == 'inicio_ok':
                usuario.estado = 1
                iniciar(usuario)
            else:
                print('no has iniciado sesion')
                iniciar(usuario)
        if opcion_server == 'registrar':
            username = input('Nombre de usuario: ')
            client.send(username.encode())
            if client.recv(1024).decode() == 'username_error':
                print('El nombre de usuario ya existe')
                iniciar(usuario)
            else:
                print('El nombre de usuario esta disponible')
                nombres = input('Nombres: ')
                client.send(nombres.encode())
                apellidos = input('Apellidos: ')
                client.send(apellidos.encode())
                password = input('Contraseña: ')
                client.send(password.encode())
                edad = input('Edad: ')
                client.send(edad.encode())
                genero = input('Genero (M ó F): ')
                client.send(genero.encode())
                print(client.recv(1024).decode())
                iniciar(usuario)
        if opcion_server == 'error_opcion':
            iniciar(usuario)
    else:
        print(client.recv(1024).decode())
        
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        write_thread = threading.Thread(target=write_messages, args=(usuario,))
        write_thread.start()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
usuario = Usuario()
iniciar(usuario)
