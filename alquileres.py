from datetime import datetime
from docutils.io import NullInput

import conexion
import eventos
import var

class Alquileres:

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
            # Cargar tabla
        except Exception as error:
            print('Error altaContrato: %s' % str(error))

    @staticmethod
    def cargarContratos():
        """
        Función que carga los contratos en la tabla de contratos
        """
        try:
            print("hola")
        except Exception as error:
            print('Error cargarContratos: %s' % str(error))

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