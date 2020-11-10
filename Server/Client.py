import sys
import json
from Configuration  import mssql_connection, register_client_from_sql, get_hash_from_sql


def register_client(data, ip):
    try:
        query = 'SP_AGREGAR_USUARIO '+"'"+ str(data)[2:-1]+"'" + ',' + "'"+str(ip)+ "'"

        con_sql = mssql_connection()

        register_client_from_sql(query)

    except IOError as e:
        print('Error [0] in the student function').format(
            e.errno, e.strerror)
    finally:
        con_sql.close()

def get_hash_client():
    try:
        query = 'SP_OBTENER_HASH '

        con_sql = mssql_connection()

        data = get_hash_from_sql(query)

        print(data)
        if len(data) <= 0:
            print('no data')
            sys.exit(0)
        return data
    except IOError as e:
        print('Error [0] in the student function').format(
            e.errno, e.strerror)
    finally:
        con_sql.close()


def register_hash_detected(name,hash):
    try:
        query = 'SP_AGREGAR_USUARIO_ARCHIVO '+"'"+ str(name)+"'" + ',' + str(hash)

        con_sql = mssql_connection()
        register_client_from_sql(query)

    except IOError as e:
        print('Error [0] in the student function').format(
            e.errno, e.strerror)
    finally:
        con_sql.close()