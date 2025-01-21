from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QWidget, QVBoxLayout
from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore, QtGui

import conexion
import eventos
import var


class Facturas:

    def altaVenta(self):
        try:
            nuevafactura = [var.ui.txtFechaFactura.text(), var.ui.txtDniVentas.text()]
            if (conexion.Conexion.altaFactura(nuevafactura)):
                eventos.Eventos.crearMensajeInfo("Aviso", "Factura Guardada")
                Facturas.mostrarTablaFacturas()
            else:
                eventos.Eventos.crearMensajeInfo("Aviso", "Error al guardar la factura")
        except Exception as error:
            print('Error altaVenta: %s' % str(error))

    @staticmethod
    def mostrarTablaFacturas():
        try:
            listado = conexion.Conexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                container = QWidget()
                layout = QVBoxLayout()
                var.botondel = QPushButton()
                var.botondel.setFixedSize(30, 20)
                var.botondel.setIcon(QIcon("./img/papelera.ico"))
                var.botondel.setStyleSheet("background-color: #efefef;")
                var.botondel.clicked.connect(Facturas.deleteFactura)
                layout.addWidget(var.botondel)
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

    # rediseñar la interfaz

    @staticmethod
    def deleteFactura():


        """
        try:
            factura = var.ui.tablaFacturas.selectedItems()
            if conexion.Conexion.deleteFactura(factura[0].text()):
                eventos.Eventos.crearMensajeInfo("Alta correcta", "Se ha eliminado la factura correctamente")
                Facturas.mostrarTablaFacturas()
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido eliminar la factura correctamente")
        except Exception as e:
            print("Error al eliminar la factura: ", e)
        """