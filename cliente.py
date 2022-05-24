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

def write_messages():
    while True:
        message = input('')
        if message == '/exit':
            client.send(message.encode())
            print('Sesion cerrada')
            client.close()
            sys.exit()
        else:
            client.send(message.encode())
    
def iniciar(usuario):
    if usuario.estado == 0:
        opcion = menu()
        client.send(opcion.encode())
        if client.recv(1024).decode() == 'iniciar_sesion':
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
    else:
        print(client.recv(1024).decode())


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
usuario = Usuario()
iniciar(usuario)
