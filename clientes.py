
from PyQt6 import QtWidgets, QtGui, QtCore

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

        try:
            nuevoCli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                        var.ui.txtNomcli.text(), var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(),
                        var.ui.txtDireccioncli.text(), var.ui.cmbProvinciacli.currentText(),
                        var.ui.cmbMunicipiocli.currentText()]

            if conexion.Conexion.altaCliente(nuevoCli):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Cliente Alta en Base de Datos')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
                return True
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                mbox.setText("Error al dar de alta el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
                return False

        except Exception as e:
            print("error altaCliente", e)


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

    @staticmethod
    def cargaTablaClientes(self):
        try:
            listado = conexion.Conexion.listadoClientes(self)
            index = 0
            for registro in listado:
                var.ui.tablaClientes.setRowCount(index + 1)
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem("    " + str(registro[5]) + "    "))
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[9])))
                var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                index += 1

        except Exception as e:
            print("error cargaTablaClientes", e)