import sqlite3
import socket   
import threading
from modelos import *

clients = []
usernames = []
salas = []

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
print(f"Server running on {HOST}:{PORT}")

sala_principal = Sala('principal', 'servidor')
salas.append(sala_principal)

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

def buscar(username):
    conexion = sqlite3.connect('chat.db')
    cursor = conexion.cursor()
    query = f"SELECT * FROM usuarios WHERE usuario = '{username}'"
    cursor.execute(query)
    usuario = cursor.fetchall()
    conexion.commit()
    conexion.close()
    if usuario:
        return(1)
    else:
        return(0)

def insertarUsuario(nombres, apellidos, usuario, password, edad, genero):
    conexion = sqlite3.connect('chat.db')
    cursor = conexion.cursor()
    query = f"INSERT INTO usuarios VALUES ('{nombres}', '{apellidos}', '{usuario}', '{password}', {edad}, '{genero}', 0)"
    cursor.execute(query)
    conexion.commit()
    conexion.close()


def enviar_mensaje(_message, _client, _username):
    message = f'{_username}: {_message}'
    for client in clients:
        if client != _client:
            client.send(message.encode())

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
        if opcion == 'registrar':
            client.send('registrar'.encode())
            username = client.recv(1024).decode()
            if buscar(username) == 1:
                client.send('username_error'.encode())
                controlador(client, address, usuario)
            else:
                client.send(f'El username {username} esta libre'.encode())
                nombres = client.recv(1024).decode()
                apellidos = client.recv(1024).decode()
                password = client.recv(1024).decode()
                edad = client.recv(1024).decode()
                genero = client.recv(1024).decode()
                insertarUsuario(nombres, apellidos, username, password, edad, genero)
                client.send('Registro Completado'.encode())
                controlador(client, address, usuario)
        if opcion == 'error_opcion':
            client.send('error_opcion'.encode())
            controlador(client, address, usuario)
    else:
        client.send(f'Bienvenido {usuario.nombres}. Has iniciado sesión correctamente'.encode())
        usernames.append(usuario.usuario)
        clients.append(client)
        sala_principal.agregar_usuario(usuario.usuario, client)
        sala_actual = sala_principal.nombre
        while True:
            message = client.recv(1024).decode()
            print(f'{usuario.usuario}: {message}')

            if message == '#exit': #exit. Desconectará al cliente del servidor
                clients.remove(client)
                usernames.remove(usuario.usuario)
                for s in salas:
                    if s.nombre == sala_actual:
                        s.eliminar_usuario(usuario.usuario)
                client.close()
                
            if message[0] == '#':
                print('El usuario ingreso un comando')
                message_dividido = message.split(' ')
                if message == '#show users': #show users: Muestra el listado el todos los usuarios en todo el sistema
                    show_users = f"Usuarios conectados: "
                    for user in usernames:
                        show_users += f' -{user}'
                    client.send(f"Servidor: {show_users}".encode())

                elif message == '#show users s':
                    mensaje = sala_principal.ver_usuarios()
                    client.send(f"Servidor: {mensaje}".encode())
                
                elif message == '#lR':
                    mensaje = f'Salas Disponibles: '
                    for s in salas:
                        mensaje += f'-{s.nombre} {len(s.usuarios_conectados)} '
                    client.send(mensaje.encode())

                elif message == '#aR':
                    client.send(f'Estas en la sala {sala_actual}'.encode())

                elif message == '#eR':
                    if sala_actual != 'principal':
                        for s in salas:
                            if s.nombre == sala_actual:
                                s.eliminar_usuario(usuario.usuario)
                        sala_actual = sala_principal.nombre
                        sala_principal.agregar_usuario(usuario.usuario, client)
                        client.send(f'Bienvenido a la sala Principal, {usuario.usuario}'.encode())
                    else:
                        client.send(f'Ya estas en la sala Principal'.encode())


                elif message_dividido[0] == '#cR':
                    sala = Sala(message_dividido[1], usuario.usuario)
                    salas.append(sala)
                    sala.agregar_usuario(usuario.usuario, client)
                    for s in salas:
                        if s.nombre == sala_actual:
                            s.eliminar_usuario(usuario.usuario)
                    sala_actual = message_dividido[1]
                    client.send(f'Bienvenido a tu sala "{sala_actual}"'.encode())



                elif message_dividido[0] == '#gR':
                    sala_buscar = message_dividido[1]
                    sala_anterior = sala_actual
                    for s in salas:
                        if s.nombre == sala_buscar:
                            s.agregar_usuario(usuario.usuario, client)
                            sala_actual = s.nombre
                    if sala_actual == sala_anterior:
                        client.send(f'La sala "{sala_buscar}" NO existe'.encode())
                    else:
                        for s in salas:
                            if s.nombre == sala_anterior:
                                s.eliminar_usuario(usuario.usuario)
                        client.send(f'Bienvenido a la sala "{sala_buscar}".'.encode())
                

                else:
                    client.send(f"Servidor: Al parecer ingresaste un comando pero no lo reconocemos. Usa #help para verlos todos.".encode())

            else:
                if message == '#exit':
                    mensaje = f'Servidor: El usuario {usuario.usuario} se ha desconectado.'
                else:
                    mensaje = f'{usuario.usuario}: {message}'

                for s in salas:
                    if s.nombre == sala_actual:
                        for u in s.usuarios_conectados:
                            if u[1] != client:
                                u[1].send(mensaje.encode())




def receive_connections():
    while True:
        client, address = server.accept()
        usuario = Usuario()
        hilo = threading.Thread(target=controlador, args=(client, address, usuario,))
        hilo.start()
        
receive_connections()

