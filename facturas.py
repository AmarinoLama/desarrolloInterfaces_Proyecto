from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QWidget, QVBoxLayout, QMessageBox
from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore, QtGui

import conexion
import eventos
import var

class Facturas:

    current_cliente = None
    current_propiedad = None
    current_vendedor = None
    botonesdel = []

    @staticmethod
    def altaFactura():
        """

        """
        try:
            if (var.ui.txtFechaFactura.text() == "" or var.ui.txtDniFactura.text() == ""):
                eventos.Eventos.crearMensajeError("Error", "Es necesario cubrir los datos de fecha y dniCliente")
            else:
                nuevaFactura = [var.ui.txtFechaFactura.text(), var.ui.txtDniFactura.text()]
                if (conexion.Conexion.guardarFactura(nuevaFactura)):
                    eventos.Eventos.crearMensajeInfo("Operación exitosa", "Se ha guardado la factura correctamente")
                    Facturas.current_factura = str(conexion.Conexion.getLastIdFactura())
                    var.ui.lblNumFactura.setText(Facturas.current_factura)
                    Facturas.mostrarTablaFacturas()
                    Facturas.checkDatosFacturas()
                else:
                    eventos.Eventos.crearMensajeError("Error", "No se ha podido guardar la factura correctamente")
            Facturas.limpiarFactura()
        except Exception as e:
            eventos.Eventos.crearMensajeError("Error", e)

    @staticmethod
    def mostrarTablaFacturas():
        try:
            listado = conexion.Conexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                container = QWidget()
                layout = QVBoxLayout()
                Facturas.botonesdel.append(QtWidgets.QPushButton())
                Facturas.botonesdel[-1].setFixedSize(30, 20)
                Facturas.botonesdel[-1].setIcon(QtGui.QIcon("./img/papelera.ico"))
                Facturas.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Facturas.botonesdel[-1].clicked.connect(lambda checked, idFactura=str(registro[0]): Facturas.deleteFactura(idFactura))
                layout.addWidget(Facturas.botonesdel[-1])
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaFacturas.setItem(index, 0, QTableWidgetItem(str(registro[0])))
                var.ui.tablaFacturas.setItem(index, 1, QTableWidgetItem(registro[1]))
                var.ui.tablaFacturas.setItem(index, 2, QTableWidgetItem(registro[2]))
                var.ui.tablaFacturas.setCellWidget(index, 3, container)

                var.ui.tablaFacturas.item(index, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                index += 1
            eventos.Eventos.resizeTablaFacturas()
        except Exception as e:
            print("Error al cargar la tabla de facturas", e)

    @staticmethod
    def cargaOneFactura():
        """

        """
        try:
            factura = var.ui.tablaFacturas.selectedItems()
            var.ui.lblNumFactura.setText(str(factura[0].text()))
            var.ui.txtFechaFactura.setText(str(factura[1].text()))
            var.ui.txtDniFactura.setText(str(factura[2].text()))
            Facturas.cargaClienteVenta()
            Facturas.mostrarTablaFacturas()
        except Exception as e:
            eventos.Eventos.crearMensajeError("Error", "Error al cargar la factura en facturas")

    @staticmethod
    def cargaClienteVenta():
        try:
            dni = var.ui.txtDniFactura.text()
            cliente = conexion.Conexion.datosOneCliente(dni)
            var.ui.txtApelcli.setText(str(cliente[2]))
            var.ui.txtNomcli.setText(str(cliente[3]))
            Facturas.current_cliente = dni
            Facturas.checkDatosFacturas()
        except Exception as e:
            Facturas.current_cliente = None
            Facturas.checkDatosFacturas()
            eventos.Eventos.crearMensajeError("Error", "Error al cargar el cliente en facturas")

    @staticmethod
    def checkDatosFacturas():
        if Facturas.current_vendedor is not None and Facturas.current_propiedad is not None and Facturas.current_cliente is not None:
            var.ui.btnGrabarVenta.setDisabled(False)
        else:
            var.ui.btnGrabarVenta.setDisabled(True)

    # comprobar
    @staticmethod
    def deleteFactura(idFactura):
        try:
            mbox = QtWidgets.QMessageBox()
            if eventos.Eventos.mostrarMensajeConfimarcion(mbox, "Borrar", "Esta seguro de que quiere borrar la factura de id " + idFactura) == QtWidgets.QMessageBox.StandardButton.Yes:
                if conexion.Conexion.deleteFactura(idFactura):
                    eventos.Eventos.crearMensajeInfo("Todo correcto", "Se ha eliminado la factura correctamente")
                    Facturas.mostrarTablaFacturas()
                    var.ui.tablaVentas.setRowCount(0)
                    Facturas.current_factura = None
                    Facturas.checkDatosFacturas()
                    Facturas.cargarBottomFactura(idFactura)
                    var.ui.lblFactura.setText("")
                    var.ui.txtFechaFactura.setText("")
                    var.ui.lblDniclifactura.setText("")
                else:
                    eventos.Eventos.mostrarMensajeError("No se ha podido eliminar la factura correctamente")
            else:
                mbox.hide()
        except Exception as e:
            print("Error al eliminar la factura: ", e)

    # arreglar
    @staticmethod
    def cargaPropiedadVenta(propiedad):
        try:
            if "venta" in str(propiedad[14]).lower() and str(propiedad[15]).lower() == "disponible":
                var.ui.lblCodigoProp.setText(str(propiedad[0]))
                var.ui.cmbTipoPro.setText(str(propiedad[7]))
                var.ui.txtPrecioVentaPro.setText(str(propiedad[12]) + " €")
                var.ui.txtDireccionPro.setText(str(propiedad[4]).title())
                var.ui.cmbMunicipioPro.setText(str(propiedad[6]))
                var.ui.artxtDesc.setText("")
                Facturas.current_propiedad = str(propiedad[0])
                Facturas.checkDatosFacturas()
            else:
                var.ui.lblCodigoProp.setText("")
                var.ui.cmbTipoPro.setText("")
                var.ui.txtPrecioVentaPro.setText("")
                var.ui.txtDireccionPro.setText("")
                var.ui.cmbMunicipioPro.setText("")
                Facturas.current_propiedad = None
                Facturas.checkDatosFacturas()
                if not "venta" in str(propiedad[14]).lower():
                    eventos.Eventos.crearMensajeInfo("Informacion", "La última propiedad seleccionada no se puede vender")
                else:
                    eventos.Eventos.crearMensajeInfo("Informacion", "La última propiedad seleccionada ya está vendida")
        except Exception as e:
            eventos.Eventos.crearMensajeError("Error", "Error al cargar el cliente: " + e)

    @staticmethod
    def cargaVendedorVenta(id):
        try:
            var.ui.txtIdVend.setText(str(id))
            Facturas.current_vendedor = str(id)
            Facturas.checkDatosFacturas()
        except Exception as e:
            Facturas.current_vendedor = None
            Facturas.checkDatosFacturas()
            eventos.Eventos.crearMensajeError("Error", "Error al cargar el cliente: " + e)

    @staticmethod
    def limpiarFactura():
        var.ui.lblNumFactura.setText("")
        var.ui.txtFechaFactura.setText("")
        var.ui.txtDniFactura.setText("")
        Facturas.current_factura = None
        Facturas.checkDatosFacturas()

    # comprobar
    @staticmethod
    def cargarBottomFactura(idFactura):
        try:
            subtotal = conexion.Conexion.totalFactura(idFactura)
            if subtotal:
                iva = 21
                total = subtotal * (1 + iva / 100)
                var.ui.lblSubtotalFactura.setText(str(subtotal) + " €")
                var.ui.lblImpuestasFacturas.setText(str(iva) + "%")
                var.ui.lblTotalFactura.setText(str(total) + " €")
            else:
                var.ui.lblSubtotalFactura.setText("- €")
                var.ui.lblImpuestasFacturas.setText("-%")
                var.ui.lblTotalFactura.setText("- €")
        except Exception as e:
            print("Error al cargar los totales")

    # acabar
    @staticmethod
    def grabarVenta():
        try:
            venta = [var.ui.lblNumFactura.text(), Facturas.current_vendedor, Facturas.current_propiedad]
        except Exception as error:
            print('Error altaVenta: %s' % str(error))

    # https://github.com/BuaTeijeiro/ProyectoDI/blob/main/facturas.py#L143