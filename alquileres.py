from datetime import datetime
from PyQt6 import QtWidgets, QtCore, QtGui

import conexion
import eventos
import propiedades
import var

class Alquileres:

    chkPagado = []
    botonesdel = []

    @staticmethod
    def altaContrato():
        """
        Función que graba un contrato en la base de datos y devuelve un mensaje de éxito o error
        """
        try:
            if not Alquileres.checkCampos():
                return
            infoContrato = [var.ui.txtPropiedadContrato.text(),
                            var.ui.txtDniClienteContrato.text(),
                            var.ui.txtVendedorContrato.text(),
                            var.ui.txtFechaInicioMensualidad.text(),
                            var.ui.txtFechaFinMensualidad.text()]
            if conexion.Conexion.grabarContrato(infoContrato):
                eventos.Eventos.crearMensajeInfo("Informacion", "El contrato se ha grabado exitosamente")
            else:
                eventos.Eventos.crearMensajeError("Error", "El contrato no se ha podido grabar")
            conexion.Conexion.cambiarEstadoPropiedad(var.ui.txtPropiedadContrato.text(), 2)
            Alquileres.cargarTablaAlquileres()
            propiedades.Propiedades.cargarTablaPropiedades(0)
        except Exception as error:
            print('Error altaContrato: %s' % str(error))

    @staticmethod
    def cargarTablaAlquileres():
        """

        Función que recupera la lista de alquileres mediante Conexion.listadoAlquileres
        y muestra dicha información en la tabla de alquileres

        """
        try:
            listado = conexion.Conexion.listadoAlquileres()
            var.ui.tablaContratos.setRowCount(len(listado))
            index = 0

            Alquileres.botonesdel = []
            for registro in listado:
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                Alquileres.botonesdel.append(QtWidgets.QPushButton())
                Alquileres.botonesdel[-1].setFixedSize(30, 20)
                Alquileres.botonesdel[-1].setIcon(QtGui.QIcon("./img/papelera.ico"))
                Alquileres.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Alquileres.botonesdel[-1].clicked.connect(
                    lambda checked, idFactura=str(registro[0]): Alquileres.borrarContratoAlquiler(idFactura))
                layout.addWidget(Alquileres.botonesdel[-1])
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaContratos.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaContratos.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaContratos.setCellWidget(index, 2, container)

                var.ui.tablaContratos.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaContratos.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
        except Exception as e:
            print("Error al cargar la tabla de facturas", e)

    @staticmethod
    def checkCampos():
        """
        :return: los campos están rellenos
        :rtype: boolean

        Función que comprueba si los campos del formulario de contrato están rellenos
        """

        try:
            campos = [var.ui.txtDniClienteContrato.text(),
                            var.ui.txtPropiedadContrato.text(),
                            var.ui.txtVendedorContrato.text(),
                            var.ui.txtFechaInicioMensualidad.text(),
                            var.ui.txtFechaFinMensualidad.text()]

            for campo in campos:
                if campo == '':
                    eventos.Eventos.crearMensajeError("Error", "Todos los campos son obligatorios")
                    return False

            propiedad = conexion.Conexion.datosOnePropiedad(var.ui.txtPropiedadContrato.text())

            if propiedad[10] == "":
                eventos.Eventos.crearMensajeError("Error", "La propiedad debe de tener un precio de alquiler")
                return False
            elif propiedad[15] != "Disponible":
                eventos.Eventos.crearMensajeError("Error", "La propiedad no está disponible")
                return False

            fechaInicio = datetime.strptime(var.ui.txtFechaInicioMensualidad.text(), '%d/%m/%Y')
            fechaFin = datetime.strptime(var.ui.txtFechaFinMensualidad.text(), '%d/%m/%Y')
            if fechaInicio > fechaFin:
                eventos.Eventos.crearMensajeError("Error", "La fecha de inicio no puede ser mayor que la fecha de fin")
                return False

            return True
        except Exception as error:
            print('Error checkCamposRellenados: %s' % str(error))

    @staticmethod
    def borrarContratoAlquiler(idFactura):
        """
        :param idFactura: id de la factura a borrar
        :type idFactura: int

        Función que borra un contrato de la base de datos y actualiza la tabla de contratos
        """
        try:
            if conexion.Conexion.borrarContrato(idFactura):
                eventos.Eventos.crearMensajeInfo("Informacion", "El contrato se ha eliminado exitosamente")
            else:
                eventos.Eventos.crearMensajeError("Error", "El contrato no se ha podido eliminar")
            Alquileres.cargarTablaAlquileres()
            conexion.Conexion.cambiarEstadoPropiedad(idFactura, 0)
            propiedades.Propiedades.cargarTablaPropiedades(0)
        except Exception as error:
            print('Error borrarContratoAlquiler: %s' % str(error))

    @staticmethod
    def cargarOneContrato():
        """
        Función que carga la información de un contrato en el formulario de contratos
        """
        try:
            fila = var.ui.tablaContratos.selectedItems()
            if conexion.Conexion.datosOneContrato(fila[0].text()):
                fila = [dato.text() for dato in fila]
                contrato = conexion.Conexion.datosOneContrato(fila[0])
                var.ui.txtPropiedadContrato.setText(contrato[1])
                var.ui.txtDniClienteContrato.setText(contrato[2])
                var.ui.txtVendedorContrato.setText(contrato[3])
                var.ui.txtFechaInicioMensualidad.setText(contrato[4])
                var.ui.txtFechaFinMensualidad.setText(contrato[5])
        except Exception as error:
            print('Error cargarOneContrato: %s' % str(error))