from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore

import conexion
import eventos
import var


class Facturas:

    def altaVenta(self):
        try:
            nuevafactura = [var.ui.txtFechaFactura.text(), var.ui.txtDniVentas.text()]
            if (conexion.Conexion.altaFactura(nuevafactura)):
                eventos.Eventos.crearMensajeInfo("Aviso", "Factura Guardada")
                Facturas.mostrarTablaFacturas(self)
            else:
                eventos.Eventos.crearMensajeInfo("Aviso", "Error al guardar la factura")
        except Exception as error:
            print('Error altaVenta: %s' % str(error))

    def mostrarTablaFacturas(self):
        try:
            var.ui.tablaFacturas.setColumnWidth(0, 60)
            index = 0
            registros = conexion.Conexion.listadoFacturas(self)
            for registro in registros:
                var.ui.tablaFacturas.setRowCount(index + 1)
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tablaFacturas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaFacturas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.botondel = QtWidgets.QPushButton()
                var.botondel.setFixedSize(30, 24)
                var.ui.tablaFacturas.setCellWidget(index, 5, var.botondel)
                #var.botondel.clicked.connect(eventos.Eventos.bajaLineaVenta)

        except Exception as error:
            print('Error mostrarTablaFacturas: %s' % str(error))