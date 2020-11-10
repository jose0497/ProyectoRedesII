from builtins import print
import pymssql


#conection sql
_sql_server      = '163.178.107.10'
_sql_database    = 'ProyectoRedes'
_sql_server_port = 1433 #puerto por defecto
_sql_user = 'laboratorios'
_sql_password = 'KmZpo.2796'

#FUNTION CONNECTION
def mssql_connection():
    try:
        cnx = pymssql.connect(server = _sql_server,port= _sql_server_port,
                              user = _sql_user,password = _sql_password,
                              database = _sql_database)
        return cnx
    except:
        print('ERROR;MSSQL, CONNECTION')

#CALL PROCEDURE


def register_client_from_sql(sp):#sp nombre del procedimiento
    try:
        con = mssql_connection()
        cur = con.cursor()
        #print(format(sp))
        print("EXECUTE " + sp)
        cur.execute("EXECUTE " + sp)
        #data_return = cur.fetchall()
        con.commit()

        #return data_return
    except IOError as e:
        print('ERROR;in sql server'.format(
            e.errno, e.strerror))

def get_date_from_sql(sp):
    try:
        con = mssql_connection()
        cur = con.cursor()
        cur.execute("{} ".format(sp))
        data_return = cur.fetchall()
        con.commit()


        return data_return
    except IOError as e:
        print("ERROR: {0} Getting data from MSSQL: {1}".format(e.erno, e.strerror))


def get_hash_from_sql(sp):#sp nombre del procedimiento
    try:
        con = mssql_connection()
        cur = con.cursor()
        #print(format(sp))
        print("EXECUTE " + sp)
        cur.execute("EXECUTE " + sp)
        data_return = cur.fetchall()
        con.commit()

        return data_return
    except IOError as e:
        print('ERROR;in sql server'.format(
            e.errno, e.strerror))


