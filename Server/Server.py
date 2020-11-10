#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from tkinter import *
from tkinter import BOTH, Canvas, LEFT, ttk, VERTICAL, RIGHT, Y
from Client import register_client, get_hash_client, register_hash_detected
from Report import getUsersHashData
import socket
import threading


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

root = tk.Tk()
root.title("SERVIDOR")
root.minsize(width=800, height=100)

text = tk.Text(master=root)
text.pack(expand=True, fill="both")

frame = tk.Frame(master=root)
frame.pack()

sendTex = tk.Text(master=root)

b5 = tk.Button(master=frame, text='VER DETECCIONES')
b5.pack(side="left")

textAux = ""


class Server:
    clients = []

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.bind(("localhost", 12346))
        self.s.listen(10)
        now = str(datetime.now())[:-7]
        text.insert("insert", "({}) : Connected.\n".format(now))
        self.condition()

    def accept(self):
        # ACEPTA EL CLIENTE
        c, addr = self.s.accept()
        self.clients.append(c)
        data = c.recv(1024)
        # SE REGISTRA EL CLIENTE EN LA BASE DE DATOS
        register_client(data, str(addr[0]))
        # INDICAMOS AL CLIENTE QUE SE VAN A ENVIAR LOS HASH
        send("hash")
        # UNA VEZ NOTIFICADO AL CLIENTE, SE LE ENVIAN LOS HASH O FIRMAS PELIGROSAS
        send(get_hash_client())
        text.insert("insert", "({}) : {} connected.\n".format(str(datetime.now())[:-7], str(data)[1:]))

    def receive(self):
        for i in self.clients:

            while True:
                data = str(i.recv(1024))[2:-1]
                now = str(datetime.now())[:-7]
                if len(data) == 0:
                    pass
                # SI EL CLIENTE NOS NOTIFICA QUE HA DETECTADO UN ARCHIVO PELIGROSO
                if data == 'detectado':
                    print("Esperando hash detectado...")
                    # RECIBE EL NOMBRE DEL USUARIO Y EL HASH DETECTADO
                    name = str(i.recv(1024))[2:-1]
                    hash = str(i.recv(1024))[2:-1]
                    # SE REGISTRA EN LA BASE DE DATOS EL NOMBRE DEL USUARIO Y EL HAS DETECTADO
                    register_hash_detected(name, hash)
                else:
                    print(data)

    def condition(self):
        while True:
            t1_1 = threading.Thread(target=self.accept)
            t1_1.daemon = True
            t1_1.start()
            t1_1.join(1)
            self.receive()

    def send(self, data):
        respond = str(data)
        now = str(datetime.now())[:-7]

        try:
            for i in self.clients:
                i.sendall(bytes(respond.encode("utf-8")))
        except BrokenPipeError:
            text.insert("insert", "({}) : Client has been disconnected.\n".format(now))

    def createViewHistorial(self):
        # OBTENEMOS LOS USUARIOS CON LOS HAS DETECTADOS
        records = getUsersHashData()
        # OBTENEMOS EL TOTAL DE FILAS
        rows = len(records)
        # OBTENEMOS EL TOTAL DE COLUMNAS
        columns = len(records[0])
        # AGREGAMOS LOS COMPONENTES AL FRAME (TABLA DE DATOS)
        b5.configure(command=self.do_nothing)
        _frame = tk.Frame(master=root)
        _frame.pack(fill=BOTH, expand=1)
        myCanvas = Canvas(_frame)
        myCanvas.pack(side=LEFT, fill=BOTH, expand=1)
        myScrollBar = ttk.Scrollbar(_frame, orient=VERTICAL, command=myCanvas.yview)
        myScrollBar.pack(side=RIGHT, fill=Y)
        myCanvas.configure(yscrollcommand=myScrollBar.set)
        myCanvas.bind('<Configure>', lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))
        _frame = Frame(myCanvas)
        myCanvas.create_window((0, 0), window=_frame, anchor="nw")

        # ENCABEZADOS DE TABLA
        new_entry = tk.Entry(master=_frame, width=20, fg='Blue',
                             font=('Arial', 16, 'bold'))
        new_entry.grid(row=0, column=0)
        new_entry.insert(tk.END, ['Usuario'])

        new_entry2 = tk.Entry(master=_frame, width=20, fg='Blue',
                              font=('Arial', 16, 'bold'))
        new_entry2.grid(row=0, column=1)
        new_entry2.insert(tk.END, ['Archivo'])

        new_entry3 = tk.Entry(master=_frame, width=20, fg='Blue',
                              font=('Arial', 16, 'bold'))
        new_entry3.grid(row=0, column=2)
        new_entry3.insert(tk.END, ['Hash_Detectado'])

        # CREAMOS LA TABLA CON LOS REGISTROS DE LA BASE DE DATOS
        for i in range(rows):
            for j in range(columns):
                new_entry4 = tk.Entry(master=_frame, width=20, fg='Black',
                                      font=('Arial', 16, 'bold'))

                new_entry4.grid(row=i + 1, column=j)
                new_entry4.insert(tk.END, records[i][j])

    def do_nothing(self):
        pass


s1 = Server()


def connect():
    t1 = threading.Thread(target=s1.connect)
    t1.start()


def send(data):
    t2 = threading.Thread(target=s1.send, args=(data,))
    t2.start()


def clear():
    text.delete("1.0", "end")


def destroy():
    root.destroy()
    exit()


if __name__ == "__main__":
    connect()
    b5.configure(command=s1.createViewHistorial)
    t0 = threading.Thread(target=root.mainloop)
    t0.run()
