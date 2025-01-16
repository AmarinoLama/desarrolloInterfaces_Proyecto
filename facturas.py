import conexion
import eventos
import var


class Facturas:

    def altaVenta(self):
        try:
            nuevafactura = [var.ui.txtFechaFactura.text(), var.ui.txtDniVentas.text()]
            if (conexion.Conexion.altaFactura(nuevafactura)):
                eventos.Eventos.crearMensajeInfo("Aviso", "Factura Guardada")
                #Clientes.cargaTablaClientes(self)
            else:
                eventos.Eventos.crearMensajeInfo("Aviso", "Error al guardar la factura")
        except Exception as error:
            print('Error altaVenta: %s' % str(error))


    # hacer metodos cargar tabla