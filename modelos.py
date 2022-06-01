class Usuario:
    def __init__(self, nombres=" ", apellidos=" ", usuario=" ", password=" ", edad=0, genero="", estado = 0):
        self.nombres = nombres
        self.apellidos = apellidos
        self.usuario = usuario
        self.password = password
        self.edad = edad
        self.genero = genero
        self.estado = estado

class Sala:
    def __init__(self, nombre='', propietario=''):
        self.nombre = nombre
        self.propietario = propietario
        self.usuarios_conectados = []

    def agregar_usuario(self, username, client):
        self.usuarios_conectados.append((username, client))
        print(f'Bienvenido a la sala {self.nombre}, {username}')

    def eliminar_usuario(self, usuario):
        for u in self.usuarios_conectados:
            if u[0] == usuario:
                self.usuarios_conectados.remove(u)
        print(f'se ha eliminado al usuario {usuario} de la sala')

    def ver_usuarios(self):
        usuarios = f'Usuarios en la sala {self.nombre}: '
        for usuario in self.usuarios_conectados:
            usuarios += f' -{usuario[0]}'
        return usuarios

