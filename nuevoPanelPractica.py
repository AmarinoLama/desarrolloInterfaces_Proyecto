import conexion
import eventos
import var


class nuevoPanelPractica():

    def guardarTipoNP(self):
        try:
            if var.dlgtiposNP.ui.txtTipoEntrada.text() == "":
                eventos.Eventos.crearMensajeError("Introduce un tipo de entrada", "Debes introducir un tipo de entrada")
            else:
                if conexion.Conexion.altaTipoNP(var.dlgtiposNP.ui.txtTipoEntrada.text()):
                    var.dlgtiposNP.ui.txtTipoEntrada.clear()
                    eventos.Eventos.crearMensajeInfo("Guardado", "Tipo de entrada guardado correctamente")
                else:
                    eventos.Eventos.crearMensajeError("Error al guardar", "No se ha podido guardar el tipo de entrada")
                eventos.Eventos.cargarTipoNP(self)
        except Exception as e:
            print(f"Error: {e}")

    def borrarTipoNP(self):
        try:
            if var.dlgtiposNP.ui.txtTipoEntrada.text() == "":
                eventos.Eventos.crearMensajeError("Introduce un tipo de entrada", "Debes introducir un tipo de entrada")
            else:
                if conexion.Conexion.borrarTipoNP(var.dlgtiposNP.ui.txtTipoEntrada.text()):
                    var.dlgtiposNP.ui.txtTipoEntrada.clear()
            eventos.Eventos.cargarTipoNP(self)
        except Exception as e:
            print(f"Error: {e}")