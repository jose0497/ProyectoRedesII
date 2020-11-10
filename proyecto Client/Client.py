from datetime import datetime
import socket
import threading
import time
import hashlib
import os
import shutil

md5_hash = hashlib.md5()

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

# CREACION DEL FRAME PRINCIPAL
root = tk.Tk()
root.title("CLIENTE")
text = tk.Text(master=root)
text.pack(expand=True, fill="both")
frame = tk.Frame(master=root)
frame.pack()


# CREAMOS LOS BOTONES DEL FRAME
def buttons():
    for i in "ESCANEAR AHORA", "INGRESAR", "PROGRAMAR":
        b = tk.Button(master=frame, text=i, bg="Cyan")
        b.pack(side="left")
        yield b


b1, b2, b3 = buttons()


# OBTIENE LOS HASHES QUE LE ENVIA EL SERVIDOR
def getHashes(data):
    tamanno = len(data)
    tempHash = data[2:tamanno - 3]
    tempHash2 = str(tempHash).replace(",)", "")
    myHashs = str(tempHash2).replace(" (", "")
    hashsArray = myHashs.split(",")
    return hashsArray


# OBTIENE TANTO  LOS HASH DE LOS ARCHIVOS COMO EL NOMBRE DE LOS ARCHIVOS PROPIOS QUE VAMOS A COMPARAR
def getFilesHash():
    localHash = []
    directorioArchivos = 'files/'
    contenido = os.listdir(directorioArchivos)
    for fichero in contenido:
        with open(directorioArchivos + fichero, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
            hashObtenido = md5_hash.hexdigest()
            temp = "'" + hashObtenido + "'"
            localHash.append(temp)
    data = [[localHash, contenido]]
    return data


# MUEVE DE CARPETA NUESTRO ARCHIVO PELIGROSO
def moveFileToQuarantine(fileName):
    shutil.move('files/' + str(fileName), 'quarantine/' + str(fileName))


# COMPARA LOS HASH DEL SERVER CON LOS HASH PROPIOS A VER SI TENEMOS ARCHIVOS PELIGROSOS
def compareHashes(hashes, name):
    # OBTENEMOS LOS HASH Y ARCHIVOS PROPIOS
    localHash = getFilesHash()
    cont = 0
    encontrado = 0
    for hash in hashes:
        hashAComparar = hash
        for myHash in localHash:
            if myHash[0][cont] == hashAComparar:
                encontrado = 1
                time.sleep(2.4)
                # SI SE DETECTA UN ARCHIVO PELIGROSO, NOTIFICAMOS AL SERVER Y LE ENVIAMOS LA INFO DEL HASH DETECTADO
                send("detectado")
                send(name)
                send(myHash[0][cont])
                print('Hash Detectado-----> ' + name + myHash[0][cont] + 'nombre archivo: ' + myHash[1][cont])
                # MOVEMOS EL ARCHIVO A LA CARPETA DE CUARENTENA
                moveFileToQuarantine(myHash[1][cont])

        cont += 1
        if cont >= len(myHash[0]):
            cont = 0
    if encontrado == 0:
        text.insert("insert", "----- No se han encontrado archivos peligrososo. ------\n")
    else:
        text.insert("insert", "----- ¡¡¡¡Se han encontrado archivos peligrososo!!!! -----\n")


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None
        self.scheduled_date = None
        self.scheduled_hour = None

    def connect(self):
        now = str(datetime.now())[:-7]
        if self.nickname is not None:
            try:
                self.s.connect(("localhost", 12346))
                text.insert("insert", "({}) : Connected.\n".format(now))
                self.s.sendall(bytes("{}".format(self.nickname).encode("utf-8")))
                self.receive()
            except ConnectionRefusedError:
                text.insert("insert", "({}) : The server is not online.\n".format(now))
        else:
            text.insert("insert", "({}) : You must create a nickname.\n".format(now))

    def receive(self):
        while True:
            data = str(self.s.recv(1024))[2:-1]
            now = str(datetime.now())[:-7]
            print(data)
            if len(data) == 0:
                pass
            # EL SERVER NOS NOTIFICA QUE NOS VA A ENVIAR LOS HASH
            if data == "hash":
                print("Esperando.......")
                reciveHash = str(self.s.recv(1024))[2:-1]
                temp = getHashes(reciveHash)
                compareHashes(temp, self.nickname)

    def do_nothing(self):
        pass

    # CREAMOS LOS COMPONENTES PARA DIGITAR EL NOMBRE DEL CLIENTE
    def create_nickname(self):
        b2.configure(command=self.do_nothing)
        _frame = tk.Frame(master=root)
        _frame.pack()
        new_entry = tk.Entry(master=_frame, bg='Cyan')
        new_entry.grid(row=0, column=0)
        new_button = tk.Button(master=_frame, text="Aceptar", bg='Red')
        new_button.grid(row=1, column=0)

        def nickname_command():
            now = str(datetime.now())[:-7]
            if new_entry.get() == "":
                text.insert("insert", "({}) : Escriba su nombre por favor.\n".format(now))
            else:
                self.nickname = new_entry.get()
                _frame.destroy()
                text.insert("insert", "({}) : Su nombre es: '{}'\n".format(now, self.nickname))
                b2.configure(command=c1.create_nickname)
                b1.configure(command=connect)

        new_button.configure(command=nickname_command)

    # CREAMOS LOS COMPONENTES PARA PROGRAMAR UN ESCANEO
    def schedule_review(self):
        b3.configure(command=self.do_nothing)
        _frame = tk.Frame(master=root)
        _frame.pack()

        # CAMPO PARA FECHA
        entry_date = tk.Entry(master=_frame)
        entry_date.grid(row=0, column=0)
        entry_date.insert(0, "Fecha")

        # CAMPO PARA HORA
        entry_hour = tk.Entry(master=_frame)
        entry_hour.grid(row=1, column=0)
        entry_hour.insert(0, "Hora")

        new_button = tk.Button(master=_frame, text="Aceptar", bg='Red')
        new_button.grid(row=2, column=0)

        def schedule_review_command():
            now = str(datetime.now())[:-7]
            if entry_date.get() == "" or entry_hour.get() == "":
                text.insert("insert", "({}) : Escriba la fecha y hora por favor.\n".format(now))
            else:
                self.scheduled_date = entry_date.get()
                self.scheduled_hour = entry_hour.get()
                _frame.destroy()
                text.insert("insert", "({}) : La fecha y hora programada es: '{}'\n".format(now, self.scheduled_date))
                b3.configure(command=c1.schedule_review)
                threadScheduled = threading.Thread(target=c1.checkDate)
                threadScheduled.start()

        new_button.configure(command=schedule_review_command)

    def send(self, data):
        respond = str(data)
        now = str(datetime.now())[:-7]
        try:
            self.s.sendall(bytes(respond.encode("utf-8")))
            text.insert("insert", "({}) : {}\n".format(now, respond))
        except BrokenPipeError:
            text.insert("insert", "({}) : Server has been disconnected.\n".format(now))
            self.s.close()

    # CRECKEAMOS LA FECHA Y HORA PARA SABER EL MOMENTO DE EJECUTAR EL ESCANEO
    def checkDate(self, i=1):
        while i == 1:
            time.sleep(1)
            dateAndHour = str(self.scheduled_date) + ' ' + str(self.scheduled_hour)
            scheduled = datetime.strptime(str(dateAndHour), '%m-%d-%Y %H:%M')
            now = datetime.now()
            print("Comprobando fecha: " + str(scheduled) + " actual: " + str(now))
            if scheduled < now:
                print("Hora de escanear")
                i = 0
                connect()


c1 = Client()


def connect():
    t1 = threading.Thread(target=c1.connect)
    t1.start()


def send(data):
    t2 = threading.Thread(target=c1.send, args=(data,))
    t2.start()


def clear():
    text.delete("1.0", "end")


def destroy():
    root.destroy()


if __name__ == "__main__":
    b2.configure(command=c1.create_nickname)
    b3.configure(command=c1.schedule_review)
    t0 = threading.Thread(target=root.mainloop)
    t0.run()
