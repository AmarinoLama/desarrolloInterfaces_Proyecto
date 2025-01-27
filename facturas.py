from PyQt6 import QtGui

import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtCore


class Facturas:

    current_cliente = None
    current_propiedad = None
    current_vendedor = None
    current_factura = None
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
                    Facturas.cargarTablaFacturas()
                    Facturas.checkDatosFacturas()
                else:
                    eventos.Eventos.crearMensajeError("Error", "No se ha podido guardar la factura correctamente")
        except Exception as e:
            eventos.Eventos.crearMensajeError("Error", e)

    @staticmethod
    def cargarTablaFacturas():
        try:
            listado = conexion.Conexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            Facturas.botonesdel = []
            for registro in listado:
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                Facturas.botonesdel.append(QtWidgets.QPushButton())
                Facturas.botonesdel[-1].setFixedSize(30, 20)
                Facturas.botonesdel[-1].setIcon(QtGui.QIcon("./img/papelera.ico"))
                Facturas.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Facturas.botonesdel[-1].clicked.connect(lambda checked, idFactura=str(registro[0]): Facturas.deleteFactura(idFactura))
                layout.addWidget(Facturas.botonesdel[-1])
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tablaFacturas.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tablaFacturas.setCellWidget(index, 3, container)

                var.ui.tablaFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
            for boton in Facturas.botonesdel:
                print(boton.text())
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
            Facturas.current_factura = str(factura[0].text())
            Facturas.cargaClienteVenta()
            Facturas.cargarTablaVentasFactura()
        except Exception as e:
            eventos.Eventos.crearMensajeError("Error", "Error al cargar la factura en facturas" + e)

    @staticmethod
    def cargaClienteVenta():
        try:
            dni = var.ui.txtDniFactura.text()
            cliente = conexion.Conexion.datosOneCliente(dni)
            var.ui.txtApelClieVentas.setText(str(cliente[2]))
            var.ui.txtNomCliVentas.setText(str(cliente[3]))
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

    @staticmethod
    def deleteFactura(idFactura):
        try:
            mbox = QtWidgets.QMessageBox()
            if eventos.Eventos.mostrarMensajeConfimarcion(mbox, "Borrar", "Esta seguro de que quiere borrar la factura de id " + idFactura) == QtWidgets.QMessageBox.StandardButton.Yes:
                if conexion.Conexion.deleteFactura(idFactura):
                    eventos.Eventos.crearMensajeInfo("Todo correcto", "Se ha eliminado la factura correctamente")
                    Facturas.cargarTablaFacturas()
                    var.ui.tablaVentas.setRowCount(0)
                    Facturas.current_factura = None
                    Facturas.checkDatosFacturas()
                    Facturas.cargarBottomFactura(idFactura)
                    var.ui.lblNumFactura.setText("")
                    var.ui.txtFechaFactura.setText("")
                    var.ui.txtDniFactura.setText("")
                else:
                    eventos.Eventos.crearMensajeError("Error", "No se ha podido eliminar la factura correctamente")
            else:
                mbox.hide()
        except Exception as e:
            print("Error al eliminar la factura: ", e)

    @staticmethod
    def cargaPropiedadVenta(propiedad):
        try:
            if "venta" in str(propiedad[14]).lower() and str(propiedad[15]).lower() == "disponible":
                var.ui.lblCodigoPropVentas.setText(str(propiedad[0]))
                var.ui.txtTipoPropVentas.setText(str(propiedad[7]))
                var.ui.txtPrecioVentas.setText(str(propiedad[12]) + " €")
                var.ui.txtDireccionPropVentas.setText(str(propiedad[4]).title())
                var.ui.txtLocalidadVentas.setText(str(propiedad[6]))
                var.ui.lblMensajeError.setText("")
                Facturas.current_propiedad = str(propiedad[0])
                Facturas.checkDatosFacturas()
            else:
                var.ui.lblCodigoPropVentas.setText("")
                var.ui.txtTipoPropVentas.setText("")
                var.ui.txtPrecioVentas.setText("")
                var.ui.txtDireccionPropVentas.setText("")
                var.ui.txtLocalidadVentas.setText("")
                Facturas.current_propiedad = None
                Facturas.checkDatosFacturas()
                if not "venta" in str(propiedad[14]).lower():
                    var.ui.lblMensajeError.setText("La última propiedad seleccionada no se puede vender")
                else:
                    var.ui.lblMensajeError.setText("La última propiedad seleccionada ya está vendida")
        except Exception as e:
            eventos.Eventos.crearMensajeError("Error", "Error al cargar el cliente: " + e)

    @staticmethod
    def cargaVendedorVenta(id):
        try:
            var.ui.txtVendedorVentas.setText(str(id))
            Facturas.current_vendedor = str(id)
            Facturas.checkDatosFacturas()
        except Exception as e:
            Facturas.current_vendedor = None
            Facturas.checkDatosFacturas()
            eventos.Eventos.crearMensajeError("Error", "Error al cargar el cliente: " + e)

    @staticmethod
    def limpiarFactura():
        var.ui.txtApelClieVentas.setText("")
        var.ui.txtNomCliVentas.setText("")
        var.ui.lblCodigoPropVentas.setText("")
        var.ui.txtDireccionPropVentas.setText("")
        var.ui.txtTipoPropVentas.setText("")
        var.ui.txtPrecioVentas.setText("")
        var.ui.txtLocalidadVentas.setText("")
        var.ui.txtVendedorVentas.setText("")
        Facturas.current_factura = None
        Facturas.current_vendedor = None
        Facturas.current_propiedad = None
        Facturas.current_cliente = None
        Facturas.checkDatosFacturas()

    @staticmethod
    def altaVenta():
        try:
            infoVenta = [var.ui.lblNumFactura.text(), Facturas.current_vendedor, Facturas.current_propiedad]
            if conexion.Conexion.grabarVenta(infoVenta):
                eventos.Eventos.crearMensajeInfo("Informacion", "La venta se ha grabado exitosamente")
            else:
                eventos.Eventos.crearMensajeError("Error", "La venta no se ha podido grabar")
            Facturas.limpiarFactura()
        except Exception as error:
            print('Error altaVenta: %s' % str(error))

    @staticmethod
    def cargarTablaVentasFactura():
        """

        Método que recupera la lista de ventas cuya factura es la indicada en la interfaz
        y las muestra en la tabla de ventas

        """
        try:
            idFactura = var.ui.lblNumFactura.text()
            listado = conexion.Conexion.cargarTablaVentas(idFactura)
            var.ui.tablaVentas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                for i, dato in enumerate(registro):
                    if i != 5:
                        var.ui.tablaVentas.setItem(index, i, QtWidgets.QTableWidgetItem(str(dato)))
                    else:
                        var.ui.tablaVentas.setItem(index, i, QtWidgets.QTableWidgetItem(str(dato) + " €"))

                    var.ui.tablaVentas.item(index, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                botondel = QtWidgets.QPushButton()
                botondel.setFixedSize(30, 20)
                botondel.setIcon(QtGui.QIcon("./img/menos.ico"))
                botondel.setStyleSheet("background-color: #fff;")
                botondel.clicked.connect(
                    lambda checked, venta=str(registro[0]), prop=str(registro[1]): Facturas.eliminarVenta(venta, prop))
                layout.addWidget(botondel)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaVentas.setCellWidget(index, 6, container)

                index += 1
            eventos.Eventos.resizeTablaVentas()
            #Facturas.cargarBottomFactura(idFactura)

        except Exception as e:
            print("Error al cargar la tabla de ventas", e)

    # ver que hace esto
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
            print("Error al cargar los totales" + e)

    # Hacer la parte de abajo de las facturas en la interfaz
    # Hacer la parte de abajo de las facturas en el código

    # https://github.com/BuaTeijeiro/ProyectoDI/blob/main/facturas.py#L143