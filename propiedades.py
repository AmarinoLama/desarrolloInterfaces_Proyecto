from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import conexionserver
import eventos
import var

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
            #registro = conexion.Conexion.altaTipoPropiedad(tipo)
            registro = conexionserver.ConexionServer.altaTipoPropiedad(tipo)
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
            #registro = conexion.Conexion.bajaTipoPropiedad(tipo)
            registro = conexionserver.ConexionServer.bajaTipoPropiedad(tipo)
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

    @staticmethod
    def altaPropiedad(self):
        try:
            propiedad = [
                var.ui.txtPublicacionPro.text(), var.ui.txtDireccionPro.text(),
                var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(),
                var.ui.cmbTipoPro.currentText(), var.ui.spbHabitacionesPro.text(),
                var.ui.spbBanosPro.text(), var.ui.txtSuperficiePro.text(),
                var.ui.txtPrecioAlquilerPro.text(), var.ui.txtPrecioVentaPro.text(),
                var.ui.txtCpPro.text(), var.ui.artxtDescripcionPro.toPlainText()
            ]
            tipoOper = []
            if var.ui.cbxAlquilerPro.isChecked():
                tipoOper.append(var.ui.cbxAlquilerPro.text())
            if var.ui.cbxVentaPro.isChecked():
                tipoOper.append(var.ui.cbxVentaPro.text())
            if var.ui.cbxIntercambioPro.isChecked():
                tipoOper.append(var.ui.cbxIntercambioPro.text())
            propiedad.append(", ".join(tipoOper))
            if var.ui.rbtnDisponiblePro.isChecked():
                propiedad.append(var.ui.rbtnDisponiblePro.text())
            elif var.ui.rbtnAlquiladoPro.isChecked():
                propiedad.append(var.ui.rbtnAlquiladoPro.text())
            elif var.ui.rbtnVendidoPro.isChecked():
                propiedad.append(var.ui.rbtnVendidoPro.text())

            propiedad.append(var.ui.txtPropietarioPro.text().title())
            propiedad.append(var.ui.txtMovilPro.text())

            for i, dato in enumerate(propiedad):
                if dato == "" and i in (1, 2, 3, 4, 7, 10, 14, 15):
                    eventos.Eventos.crearMensajeError("Error", "Faltan datos por rellenar")
                    return

            if conexionserver.ConexionServer.altaPropiedad(propiedad):
                eventos.Eventos.crearMensajeInfo("Propiedad dada de alta", "La propiedad ha sido dada de alta")
                Propiedades.cargarTablaPropiedades(self,0)
        except Exception as e:
            print(str(e))

    @staticmethod
    def cargarTablaPropiedades(self, contexto):
        try:
            if contexto == 0:
                #listado = conexion.Conexion.listadoPropiedades(self)
                listado = conexionserver.ConexionServer.listadoPropiedades(self)
            elif contexto == 1:
                datosNecesarios = [var.ui.cmbTipoPro.currentText(), var.ui.cmbMunicipioPro.currentText()]
                listado = conexion.Conexion.listadoFiltrado(datosNecesarios)
            index = 0
            var.ui.tablaPropiedades.setRowCount(0)
            for registro in listado:
                var.ui.tablaPropiedades.setRowCount(index + 1)
                var.ui.tablaPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[5])))
                var.ui.tablaPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[6])))
                var.ui.tablaPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tablaPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                var.ui.tablaPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem(
                    str(registro[10]) + " €" if str(registro[10]) else "- €"))
                var.ui.tablaPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem(
                    str(registro[11]) + " €" if str(registro[11]) else "- €"))
                var.ui.tablaPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem(str(registro[14])))
                var.ui.tablaPropiedades.setItem(index, 8, QtWidgets.QTableWidgetItem("" if registro[2] is None else str(registro[2])))

                var.ui.tablaPropiedades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1
            if len(listado) == 0:
                var.ui.tablaPropiedades.setRowCount(1)
                var.ui.tablaPropiedades.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay propiedades"))
        except Exception as e:
            print("error cargaTablaPropiedades", e)


    @staticmethod
    def cargaOnePropiedad(self):
        try:
            Propiedades.manageCheckbox(self)
            Propiedades.manageRadioButtons(self)
            fila = var.ui.tablaPropiedades.selectedItems()
            datos = [dato.text() for dato in fila]
            #registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))
            registro = conexionserver.ConexionServer.datosOnePropiedad(str(datos[0]))

            listado = [var.ui.lblCodigoProp, var.ui.txtPublicacionPro, var.ui.txtFechabajaPro,
                        var.ui.txtDireccionPro, var.ui.cmbProvinciaPro, var.ui.cmbMunicipioPro,
                        var.ui.cmbTipoPro, var.ui.spbHabitacionesPro, var.ui.spbBanosPro,
                        var.ui.txtSuperficiePro, var.ui.txtPrecioAlquilerPro, var.ui.txtPrecioVentaPro,
                        var.ui.txtCpPro, var.ui.artxtDescripcionPro]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QCheckBox):
                    if ("Alquiler") in registro[i]:
                        var.ui.cbxAlquilerPro.setChecked(True)
                    else:
                        var.ui.cbxAlquilerPro.setChecked(False)
                    if ("Venta") in registro[i]:
                        var.ui.cbxVentaPro.setChecked(True)
                    else:
                        var.ui.cbxVentaPro.setChecked(False)
                    if ("Intercambio") in registro[i]:
                        var.ui.cbxIntercambioPro.setChecked(True)
                    else:
                        var.ui.cbxIntercambioPro.setChecked(False)
                elif isinstance(casilla, QtWidgets.QRadioButton):
                    if registro[i] == "Vendido":
                        var.ui.rbtnVendidoPro.setChecked(True)
                    elif registro[i] == "Disponible":
                        var.ui.rbtnDisponiblePro.setChecked(True)
                    else:
                        var.ui.rbtnAlquiladoPro.setChecked(True)
                elif isinstance(casilla, QtWidgets.QSpinBox):
                    casilla.setValue(int(registro[i]))
                elif isinstance(casilla, QtWidgets.QTextEdit):
                    casilla.setPlainText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))

            var.ui.txtPropietarioPro.setText(str(registro[16]))
            var.ui.txtMovilPro.setText(str(registro[17]))

            Propiedades.manageCheckbox(self)
            Propiedades.manageRadioButtons(self)
        except Exception as e:
            print("error cargaOnePropiedad en propiedades", e)

    @staticmethod
    def modifPropiedad(self):
        try:
            propiedad = [
                var.ui.lblCodigoProp.text(), var.ui.txtPublicacionPro.text(), var.ui.txtFechabajaPro.text(),
                var.ui.txtDireccionPro.text(), var.ui.cmbProvinciaPro.currentText(),
                var.ui.cmbMunicipioPro.currentText(), var.ui.cmbTipoPro.currentText(),
                var.ui.spbHabitacionesPro.text(), var.ui.spbBanosPro.text(), var.ui.txtSuperficiePro.text(),
                var.ui.txtPrecioAlquilerPro.text(), var.ui.txtPrecioVentaPro.text(),
                var.ui.txtCpPro.text(), var.ui.artxtDescripcionPro.toPlainText()
            ]
            tipoOper = []
            if var.ui.cbxAlquilerPro.isChecked():
                tipoOper.append(var.ui.cbxAlquilerPro.text())
            if var.ui.cbxVentaPro.isChecked():
                tipoOper.append(var.ui.cbxVentaPro.text())
            if var.ui.cbxIntercambioPro.isChecked():
                tipoOper.append(var.ui.cbxIntercambioPro.text())
            propiedad.append(", ".join(tipoOper))
            if var.ui.rbtnDisponiblePro.isChecked():
                propiedad.append(var.ui.rbtnDisponiblePro.text())
            elif var.ui.rbtnAlquiladoPro.isChecked():
                propiedad.append(var.ui.rbtnAlquiladoPro.text())
            elif var.ui.rbtnVendidoPro.isChecked():
                propiedad.append(var.ui.rbtnVendidoPro.text())

            propiedad.append(var.ui.txtPropietarioPro.text().title())
            propiedad.append(var.ui.txtMovilPro.text())

            if (var.ui.txtFechabajaPro.text() == "" or var.ui.txtFechabajaPro.text() == "None") and var.ui.txtPublicacionPro.text() != "":
                eventos.Eventos.crearMensajeError("Error", "Comprueba las fechas de publicación y baja, recuerda que la de baja tiene que ser posterior a la de alta")

                fecha_baja = datetime.strptime(var.ui.txtFechabajaPro.text(), "%d/%m/%Y")
                fecha_publicacion = datetime.strptime(var.ui.txtPublicacionPro.text(), "%d/%m/%Y")

                if fecha_baja < fecha_publicacion:
                    eventos.Eventos.crearMensajeError("Error", "La fecha de baja debe ser posterior a la fecha de publicación")
                    return

            for i, dato in enumerate(propiedad):
                if dato == "" and i in (1, 2, 3, 4, 7, 10, 14, 15):
                    eventos.Eventos.crearMensajeError("Error", "Faltan datos por rellenar")
                    return

            if conexionserver.ConexionServer.modifPropiedad(propiedad):
                eventos.Eventos.crearMensajeInfo("Propiedad modificada", "La propiedad ha sido modificada")
                Propiedades.cargarTablaPropiedades(self, 0)
            else:
                eventos.Eventos.crearMensajeError("Error", "Error en la modificación de la propiedad")

        except Exception as e:
            print("Error modificando cliente en propiedades.", e)

    def bajaPropiedad(self):
        try:
            if var.ui.txtFechabajaPro.text() == "" or var.ui.txtPublicacionPro.text() == "":
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Error')
                mbox.setText('Comprueba las fechas de publicación y baja, recuerda que la de baja tiene que ser posterior a la de alta')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

            else:
                fecha_baja = datetime.strptime(var.ui.txtFechabajaPro.text(), "%d/%m/%Y")
                datos = [var.ui.txtFechabajaPro.text(), var.ui.lblCodigoProp.text()]
                if var.ui.rbtnVendidoPro.isChecked():
                    datos.append("Vendido")
                elif var.ui.rbtnAlquiladoPro.isChecked():
                    datos.append("Alquilado")
                fecha_publicacion = datetime.strptime(var.ui.txtPublicacionPro.text(), "%d/%m/%Y")
                if fecha_baja > fecha_publicacion:
                    #if conexion.Conexion.bajaPropiedad(datos):
                    if conexionserver.ConexionServer.bajaPropiedad(datos):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                        mbox.setWindowTitle('Aviso')
                        mbox.setText('Propiedad dada de baja')
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()
                        Propiedades.cargarTablaPropiedades(self, 0)
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
                        mbox.setWindowTitle('Aviso')
                        mbox.setText('Error en la baja de la propiedad')
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                        mbox.exec()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowTitle('Error')
                    mbox.setText('La fecha de baja debe ser posterior a la fecha de publicación')
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                Propiedades.cargarTablaPropiedades(self, 0)
        except Exception as error:
            print("error bajaPropiedad en propiedades", error)

    def historicoProp(self):
        try:
            if var.ui.chkHistoricoPro.isChecked():
                var.historico = 1
            else:
                var.historico = 0
            Propiedades.cargarTablaPropiedades(self, 0)
        except Exception as e:
            print("checkbox historico error ", e)

    def filtrarPropiedades(self):
        if not var.ui.cmbTipoPro.currentText() or not var.ui.cmbMunicipioPro.currentText():
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setWindowIcon(QtGui.QIcon('./img/icono.ico'))
            mbox.setWindowTitle('Aviso')
            mbox.setText('Los campos Tipo y Municipio han de contener algo')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            mbox.exec()
        elif var.lupaState == 0:
            var.lupaState = 1
            Propiedades.cargarTablaPropiedades(self, 1)
        elif var.lupaState == 1:
            var.lupaState = 0
            Propiedades.cargarTablaPropiedades(self, 0)

    def manageCheckbox(self):

        var.ui.cbxAlquilerPro.setEnabled(False)
        var.ui.cbxVentaPro.setEnabled(False)

        if var.ui.txtPrecioAlquilerPro.text() == "":
            var.ui.cbxAlquilerPro.setChecked(False)
        else:
            var.ui.cbxAlquilerPro.setChecked(True)

        if var.ui.txtPrecioVentaPro.text() == "":
            var.ui.cbxVentaPro.setChecked(False)
        else:
            var.ui.cbxVentaPro.setChecked(True)

        if var.ui.txtPrecioAlquilerPro.text() == "" and var.ui.txtPrecioVentaPro.text() == "":
            var.ui.cbxIntercambioPro.setChecked(True)

    def manageRadioButtons(self):
        if var.ui.txtFechabajaPro.text() == "":
            var.ui.rbtnDisponiblePro.setEnabled(True)
            var.ui.rbtnDisponiblePro.setChecked(True)
            var.ui.rbtnAlquiladoPro.setChecked(False)
            var.ui.rbtnVendidoPro.setChecked(False)
            var.ui.rbtnAlquiladoPro.setEnabled(False)
            var.ui.rbtnVendidoPro.setEnabled(False)
        else:
            var.ui.rbtnDisponiblePro.setChecked(False)
            var.ui.rbtnDisponiblePro.setEnabled(False)
            var.ui.rbtnAlquiladoPro.setChecked(True)
            var.ui.rbtnAlquiladoPro.setEnabled(True)
            var.ui.rbtnVendidoPro.setEnabled(True)