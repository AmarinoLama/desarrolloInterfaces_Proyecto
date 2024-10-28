import var

class Propiedades():
    def altaTipopropiedad(self):
        tipo = var.dlggestion.txtGestTipoProp.text()
        print(tipo)

    def altaPropiedad(self):
        try:
            proiedad = [var.ui.txtPublicacionPro.text(), var.ui.txtFechabajaPro.text(), var.ui.txtDireccionPro.text(),
                        var.ui.cmbProvinciaPro.currentText(), var.ui.cmbMunicipioPro.currentText(), var.ui.cmbTipoPro.currentText(),
                        var.ui.spbHabitacionesPro.text(), var.ui.spbBanosPro.text(), var.ui.txtSuperficiePro.text(),
                        var.ui.txtPrecioAlquilerPro.text(), var.ui.txtPrecioVentaPro.text(), var.ui.txtCpPro.text(),
                        var.ui.artxtDescripcionPro.toPlainText(), var.ui.txtPropietarioPro.text(), var.ui.txtMovilPro.text()]
            print(proiedad)
        except Exception as error:
            print(error)