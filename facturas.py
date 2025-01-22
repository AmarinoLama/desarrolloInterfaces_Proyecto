from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QWidget, QVBoxLayout, QMessageBox
from PyQt6.uic.Compiler.qtproxies import QtWidgets, QtCore, QtGui

import conexion
import eventos
import var
from eventos import Eventos


class Facturas:

    current_cliente = None
    current_propiedad = None
    current_vendedor = None

    def altaFactura(self):
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

    # comprobar
    @staticmethod
    def cargaOneFactura():
        """

        """
        try:
            factura = var.ui.tablaFacturas.selectedItems()
            var.ui.lblFactura.setText(str(factura[0].text()))
            var.ui.txtFechaFactura.setText(str(factura[1].text()))
            var.ui.lblDniclifactura.setText(str(factura[2].text()))
            Facturas.cargaClienteVenta()
            Facturas.cargarTablaVentasFactura()
        except Exception as e:
            eventos.Eventos.crearMensajeError("Error", "Error al cargar la factura en facturas")

    # comprobar
    @staticmethod
    def cargaClienteVenta():
        try:
            dni = var.ui.lblDniclifactura.text()
            cliente = conexion.Conexion.datosOneCliente(dni)
            var.ui.lblApelCli.setText(str(cliente[2]))
            var.ui.lblNombrecli.setText(str(cliente[3]))
            Facturas.current_cliente = dni
            Facturas.checkDatosFacturas()
        except Exception as e:
            Facturas.current_cliente = None
            Facturas.checkDatosFacturas()
            eventos.Eventos.crearMensajeError("Error", "Error al cargar el cliente en facturas")

    #comprobar
    @staticmethod
    def checkDatosFacturas():
        if Facturas.current_vendedor is not None and Facturas.current_propiedad is not None and Facturas.current_cliente is not None:
            var.ui.btnGrabarVenta.setDisabled(False)
        else:
            var.ui.btnGrabarVenta.setDisabled(True)

    # comprobar
    @staticmethod
    def deleteFactura():
        try:
            button = var.ui.tablaFacturas.sender()
            index = var.ui.tablaFacturas.indexAt(button.pos())
            row = index.row()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Icon.Warning)
            msgbox.setWindowIcon(QIcon('./img/logo.ico'))
            msgbox.setWindowTitle('Aviso')
            msgbox.setText("Desea Eliminar la Factura")
            msgbox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msgbox.button(QMessageBox.StandardButton.Yes).setText('Si')
            if msgbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                if conexion.Conexion.delFactura(row + 1):
                    Eventos.crearMensajeInfo("Borrado", "La factura se ha borrado correctamente")
                    Facturas.mostrarTablaFacturas()
            else:
                msgbox.hide()
        except Exception as error:
            print("Error al eliminar la factura", error)

    @staticmethod
    def grabarVenta():
        try:
            venta = [var.ui.lblNumFactura.text(), Facturas.current_vendedor, Facturas.current_propiedad]
        except Exception as error:
            print('Error altaVenta: %s' % str(error))

    # https://github.com/BuaTeijeiro/ProyectoDI/blob/main/facturas.py#L143