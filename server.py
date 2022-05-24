import sqlite3
import socket   
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
print(f"Server running on {HOST}:{PORT}")

clients = []
usernames = []

class Usuario:
    def __init__(self, nombres=" ", apellidos=" ", usuario=" ", password=" ", edad=0, genero="", estado = 0):
        self.nombres = nombres
        self.apellidos = apellidos
        self.usuario = usuario
        self.password = password
        self.edad = edad
        self.genero = genero
        self.estado = estado

def buscarUsuario(username, password):
    conexion = sqlite3.connect('chat.db')
    cursor = conexion.cursor()
    query = f"SELECT * FROM usuarios WHERE usuario = '{username}' AND password = '{password}'"
    cursor.execute(query)
    usuario = cursor.fetchall()
    conexion.commit()
    conexion.close()
    if usuario:
        for user in usuario:
            resultado = Usuario(user[0], user[1], user[2], user[3], user[4], user[5], 1)
            return resultado
    else:
        return("No se encontro el usuario ingresado")

def controlador(client, address, usuario):
    if usuario.estado == 0:
        print(f"el usuario {str(address)} no ha iniciado sesion")
        opcion = client.recv(1024).decode()
        if opcion == 'iniciar_sesion':
            client.send('iniciar_sesion'.encode())
            username = client.recv(1024).decode()
            password = client.recv(1024).decode()
            resultado = buscarUsuario(username, password)
            if resultado != 'No se encontro el usuario ingresado':
                usuario = resultado
                client.send('inicio_ok'.encode())
                print('Has iniciado correctamente')
                controlador(client, address, usuario)            
            else:
                client.send('inicio_error'.encode())
                controlador(client, address, usuario)
    else:
        client.send(f'Has iniciado correctamente {usuario.nombres}. Bienvenido'.encode())



def receive_connections():
    while True:
        client, address = server.accept()
        usuario = Usuario()
        hilo = threading.Thread(target=controlador, args=(client, address, usuario,))
        hilo.start()
        
receive_connections()

