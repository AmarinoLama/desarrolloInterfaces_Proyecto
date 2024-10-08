from multiprocessing.connection import Client


from PyQt6 import QtWidgets

import conexion
import eventos
import var

class Clientes:

    @staticmethod
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNIcli(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('background-color:rgb(255,255,220);')
            else:
                var.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDnicli.setText(None)
                var.ui.txtEmailcli.setText("dni no válido")
                var.ui.txtDnicli.setFocus()
        except Exception as e:
            print("error en check cliente ", e)

    @staticmethod
    def altaCliente(self):
        nuevoCli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(), var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDireccioncli.text(), var.ui.cmbProvinciacli.currentText(), var.ui.cmbMunicipiocli.currentText()]
        conexion.Conexion.altaCliente(nuevoCli)   # CAMBIE ESTO
        print(nuevoCli)


    @staticmethod
    def checkEmail(mail):
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check cliente", error)