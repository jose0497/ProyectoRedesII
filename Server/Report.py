# Python program to create a table

from tkinter import *

from Configuration import mssql_connection, get_date_from_sql


def getUsersHashData():
    sp = "exec SP_OBTENER_USUARIO_ARCHIVO;"
    print(sp)
    con_sql = mssql_connection()
    data = get_date_from_sql(sp)
    print(data)
    con_sql.close()
    return data



class Report:

    def __init__(self, root):
        records = getUsersHashData()
        rows = len(records)
        columns = len(records[0])
        # add header
        self.e = Entry(root, width=20, fg='Blue',
                       font=('Arial', 16, 'bold'))

        self.e.grid(row=0, column=0)
        self.e.insert(END, ['Usuario'])
        self.e = Entry(root, width=20, fg='Blue',
                       font=('Arial', 16, 'bold'))
        self.e.grid(row=0, column=1)
        self.e.insert(END, ['Archivo'])
        self.e = Entry(root, width=20, fg='Blue',
                       font=('Arial', 16, 'bold'))
        self.e.grid(row=0, column=2)
        self.e.insert(END, ['Hash_Detectado'])

        # create table
        for i in range(rows):
            for j in range(columns):
                self.e = Entry(root, width=20, fg='Black',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i+1, column=j)
                self.e.insert(END, records[i][j])



# create frame
def test():
    records = getUsersHashData()
    rows = len(records)
    columns = len(records[0])
    # create frame
    frame = Tk()
    t = Report(frame)
    frame.title('Usuarios')
    frame.mainloop()

