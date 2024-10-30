import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtGui


class Propiedades():

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
            propiedad.append(tipoper)
            if var.ui.rbtnDisponiblePro.isChecked():
                propiedad.append(var.ui.rbtnDisponiblePro.text())
            if var.ui.rbtnAlquiladoPro.isChecked():
                propiedad.append(var.ui.rbtnAlquiladoPro.text())
            if var.ui.rbtnVendidoPro.isChecked():
                propiedad.append(var.ui.rbtnVendidoPro.text())

            propiedad.append(var.ui.txtPropietarioPro.text())
            propiedad.append(var.ui.txtMovilPro.text())

            conexion.Conexion.altaPropiedad(propiedad)

        except Exception as error:
            print(error)