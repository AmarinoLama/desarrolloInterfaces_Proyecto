from PyQt6.uic.properties import QtCore

import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtGui


class Propiedades():

    def checkTelefono(telefono):
        try:
            telefono = str(var.ui.txtMovilPro.text())
            if eventos.Eventos.validarTelefono(telefono):
                var.ui.txtMovilPro.setStyleSheet('background-color: rgb(255, 252, 220);')
            else:
                var.ui.txtMovilPro.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilPro.setText(None)
                var.ui.txtMovilPro.setText("telefono no válido")
                var.ui.txtMovilPro.setFocus()
        except Exception as error:
            print("error check cliente", error)

    def altaTipoPropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.altaTipoPropiedad(tipo)
            if registro:
                eventos.Eventos.cargarTipoPropiedad(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('Ya existe el tipo.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            var.dlggestion.ui.txtGestipoprop.setText('')
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)

    def bajaTipoPropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtGestipoprop.text().title()
            registro = conexion.Conexion.bajaTipoPropiedad(tipo)
            if registro:
                eventos.Eventos.cargarTipoPropiedad(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('No existe el tipo.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            var.dlggestion.ui.txtGestipoprop.setText('')
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    def altaPropiedad(self):
        try:
            # var.ui.txtFechabajaPro.text(), var.ui.txtPropietarioPro.text(), var.ui.txtMovilPro.text()
            propiedad = [var.ui.txtPublicacionPro.text(), var.ui.txtDireccionPro.text(),
                        var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(),
                        var.ui.cmbTipoPro.currentText(), var.ui.spbHabitacionesPro.text(),
                        var.ui.spbBanosPro.text(), var.ui.txtSuperficiePro.text(),
                        var.ui.txtPrecioAlquilerPro.text(), var.ui.txtPrecioVentaPro.text(),
                        var.ui.txtCpPro.text(), var.ui.artxtDescripcionPro.toPlainText()]
            tipoper = []
            if var.ui.cbxAlquilerPro.isChecked():
                tipoper.append(var.ui.cbxAlquilerPro.text())
            if var.ui.cbxVentaPro.isChecked():
                tipoper.append(var.ui.cbxVentaPro.text())
            if var.ui.cbxIntercambioPro.isChecked():
                tipoper.append(var.ui.cbxIntercambioPro.text())
            propiedad.append(", ".join(tipoper))
            if var.ui.rbtnDisponiblePro.isChecked():
                propiedad.append(var.ui.rbtnDisponiblePro.text())
            if var.ui.rbtnAlquiladoPro.isChecked():
                propiedad.append(var.ui.rbtnAlquiladoPro.text())
            if var.ui.rbtnVendidoPro.isChecked():
                propiedad.append(var.ui.rbtnVendidoPro.text())

            propiedad.append(var.ui.txtPropietarioPro.text())
            propiedad.append(var.ui.txtMovilPro.text())
            conexion.Conexion.altaPropiedad(propiedad)
            Propiedades.cargarTablaPropiedades(self)

        except Exception as error:
            print(error)

    @staticmethod
    def cargarTablaPropiedades(self):
        try:
            listado = conexion.Conexion.listadoPropiedades(self)
            if listado is None:
                listado = []
            index = 0
            for registro in listado:
                var.ui.tablaPropiedades.setRowCount(index + 1)
                var.ui.tablaPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[5])))
                var.ui.tablaPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[6])))
                var.ui.tablaPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tablaPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[10])))
                var.ui.tablaPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem(str(registro[11])))
                var.ui.tablaPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14])))
                index += 1
        except Exception as e:
            print("error cargaTablaClientes", e)

    @staticmethod
    def cargaOnePropiedad(self):
        #todo arreglar esto
        try:
            fila = var.ui.tablaPropiedades.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))
            listado = [var.ui.txtPublicacionPro, var.ui.txtDireccionPro,
                       var.ui.cmbProvinciaPro, var.ui.cmbMunicipioPro,
                       var.ui.cmbTipoPro, var.ui.spbHabitacionesPro,
                       var.ui.spbBanosPro, var.ui.txtSuperficiePro,
                       var.ui.txtPrecioAlquilerPro, var.ui.txtPrecioVentaPro,
                       var.ui.txtCpPro, var.ui.artxtDescripcionPro]
            for i in range(len(listado)):
                if i in (2, 3, 4):
                    listado[i].setCurrentText(registro[i])
                elif i == 11:
                    listado[i].setPlainText(registro[i])
                else:
                    listado[i].setText(registro[i])
        except Exception as e:
            print("error cargaOnePropiedad en propiedades", e)