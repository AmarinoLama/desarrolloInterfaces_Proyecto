import mysql.connector
from mysql.connector import Error
import os
from PyQt6 import QtSql, QtWidgets

import var


class ConexionServer():
    def crear_conexion(self):
        try:
            conexion = mysql.connector.connect(
                host='192.168.10.66',  # Cambia esto a la IP de tu servidor user='dam', # Usuario creado
                # host='192.168.1.49',
                user='dam',
                password='dam2425',
                database='bbdd',
                charset="utf8mb4",
                collation="utf8mb4_general_ci"  # Asegúrate de que aquí esté configurado
                # Contraseña del usuario database='bbdd' # Nombre de la base de datos
            )
            if conexion.is_connected():
                pass
                # print("Conexión exitosa a la base de datos")
            return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return None

    @staticmethod
    def listaProv(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    def listadoClientes(self):
        try:
            listadoclientes = []
            conexion = ConexionServer().crear_conexion()

            if var.historico == 1:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC")
                resultados = cursor.fetchall()
                for fila in resultados:  # Procesar cada fila de los resultados y crea una lista con valores de la fila
                    listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes
            else:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM clientes WHERE bajacli is null or bajacli = '' ORDER BY apelcli, nomecli ASC")
                resultados = cursor.fetchall()
                for fila in resultados:  # Procesar cada fila de los resultados y crea una lista con valores de la fila
                    listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes

            cursor.close()  # Cerrar el cursor y la conexión si no los necesitas más
            conexion.close()
            return listadoclientes
        except Exception as e:
            print("error listado en conexion", e)

    def altaCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO clientes (dnicli, altacli, apelcli, nomecli, dircli, emailcli, movilcli, provcli, municli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, cliente)          # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    def datosOneCliente(dni):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT * FROM clientes WHERE dnicli = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (dni,))  # Pasar 'dni' como una tupla
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    for col in row:
                        registro.append(str(col))
            return registro

        except Exception as e:
            print("Error al obtener datos de un cliente:", e)
            return None  # Devolver None en caso de error

    def bajaCliente(datos):
        try:
            conexion = ConexionServer().crear_conexion()
            query = "UPDATE clientes SET bajacli = %s WHERE dnicli = %s"
            cursor = conexion.cursor()
            cursor.execute(query, datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Error as e:
            print("error bajaCliente en conexionServer", e)
            return False

    def modifCliente(datos):
        try:
            conexion = ConexionServer().crear_conexion()
            query = "UPDATE clientes SET apelcli = %s, nomecli = %s, dircli = %s, emailcli = %s, movilcli = %s, provcli = %s, municli = %s, altacli = %s, bajacli = %s WHERE dnicli = %s"
            cursor = conexion.cursor()
            cursor.execute(query, datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Error as e:
            print("error modifCliente en conexionServer", e)
            return False

    def listadoPropiedades(self):
        try:
            conexion = ConexionServer().crear_conexion()
            listado = []
            cursor = conexion.cursor()
            if var.historico == 1:
                cursor.execute("SELECT * FROM propiedades WHERE bajaprop is NULL ORDER BY muniprop ASC ")

            elif var.historico == 0:
                cursor.execute("SELECT * FROM propiedades ORDER BY muniprop ASC ")

            resultados = cursor.fetchall()
            for fila in resultados:  # Procesar cada fila de los resultados y crea una lista con valores de la fila
                listado.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes
            cursor.close()  # Cerrar el cursor y la conexión si no los necesitas más
            conexion.close()
            return listado
        except Exception as e:
            print("error listado en conexionServer", e)

    @staticmethod
    def cargarTipoProp():
        try:
            registro = []
            conexion = ConexionServer().crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT tipo FROM tipopropiedad")
            resultados = cursor.fetchall()
            for fila in resultados:
                registro.append(fila[0])
            return registro
        except Exception as e:
            print("error cargarTipoProp en conexionServer", e)

    def altaTipoPropiedad(tipo):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query = "INSERT INTO tipopropiedad (tipo) VALUES (%s)"
                cursor.execute(query, (tipo,))
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Error as e:
            print("error altaTipoPropiedad en conexionServer", e)
            return False

    def bajaTipoPropiedad(tipo):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query = "DELETE FROM tipopropiedad WHERE tipo = %s"
                cursor.execute(query, (tipo,))
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Error as e:
            print("error bajaTipoPropiedad en conexionServer", e)
            return False

    @staticmethod
    def altaPropiedad(propiedad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                    INSERT INTO propiedades (altaprop,dirprop,provprop,muniprop,tipoprop,habprop,banprop,superprop,prealquiprop,prevenprop,cpprop,obserprop,tipooper,estadoprop,nomeprop,movilprop)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
                    """
                propiedad[12] = str(propiedad[12])
                cursor.execute(query, propiedad)  # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar una propiedad", e)


    def datosOnePropiedad(codigo):
        resultados = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()  # Crear la conexión

            if not conexion:
                raise Exception("No se pudo establecer la conexión a la base de datos.")

            with conexion.cursor() as cursor:
                # Definir la consulta de selección
                query = '''SELECT * FROM propiedades WHERE codigo = %s'''
                cursor.execute(query, (codigo,))  # Pasar 'codigo' como parámetro en una tupla

                # Recuperar los datos de la consulta
                resultados = cursor.fetchall()

                # Verificar si hay resultados
                if not resultados:
                    print(f"No se encontraron datos para el Codigo: {codigo}")
                    return None  # Retornar None si no hay datos

                return resultados[0]

        except Exception as e:
            print("Error al obtener datos de una propiedad:", e)
            return None

    def bajaPropiedad(datos):
        try:
            conexion = ConexionServer().crear_conexion()
            query = "UPDATE propiedades SET bajaprop = %s WHERE codigo = %s"
            cursor = conexion.cursor()
            cursor.execute(query, datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Error as e:
            print("error bajaPropiedad en conexionServer", e)
            return False

    def modifPropiedad(datos):
        try:
            conexion = ConexionServer().crear_conexion()
            query = "UPDATE propiedades SET dirprop = %s, provprop = %s, muniprop = %s, tipoprop = %s, habprop = %s, banprop = %s, superprop = %s, prealquiprop = %s, prevenprop = %s, cpprop = %s, obserprop = %s, tipooper = %s, estadoprop = %s, nomeprop = %s, movilprop = %s, altaprop = %s, bajaprop = %s WHERE codigo = %s"
            cursor = conexion.cursor()
            cursor.execute(query, datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Error as e:
            print("error modifPropiedad en conexionServer", e)
            return False