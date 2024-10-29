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
            proiedad = [var.ui.txtPublicacionPro.text(), var.ui.txtFechabajaPro.text(), var.ui.txtDireccionPro.text(),
                        var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(), var.ui.cmbTipoPro.currentText(),
                        var.ui.spbHabitacionesPro.text(), var.ui.spbBanosPro.text(), var.ui.txtSuperficiePro.text(),
                        var.ui.txtPrecioAlquilerPro.text(), var.ui.txtPrecioVentaPro.text(), var.ui.txtCpPro.text(),
                        var.ui.artxtDescripcionPro.toPlainText(), var.ui.txtPropietarioPro.text(), var.ui.txtMovilPro.text()]
            print(proiedad)
        except Exception as error:
            print(error)